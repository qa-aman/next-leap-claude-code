# Meeting Action Items — Design Spec

**Date:** 2026-09-26
**Status:** Approved 2026-09-26

## 1. Purpose

The team pastes meeting notes into a web app and gets back a list of action items, each with an owner and a due date. All open items from all meetings appear on one shared board, where anyone on the team can tick them off.

### Success criteria

1. **Completeness:** every action item in a meeting's notes ends up on the board.
2. **Correct owner:** every item on the board has the right owner from the team roster. An owner is never guessed. If the owner can't be determined with certainty, the item is flagged for a human to resolve.
3. **No retyping:** nobody types an action item in by hand. Fixes happen by picking from dropdowns, adjusting a date, or selecting text in the notes.

Guiding priority, from the user: **"needs review" beats a wrong item.**

### Confirmed decisions

| Topic | Decision |
|---|---|
| Owners | Fixed roster of 8: Priya, Marcus, Sarah, Tomás, Aisha, Dana, Ravi, Lena. Nicknames allowed through configured aliases. Anyone not on the roster is flagged, never guessed. |
| Flow | Paste, then a **review screen**, then the board. Nothing reaches the board with an unresolved owner. |
| Dates | Relative dates ("by Friday") are worked out from the **meeting date**, which the paste form asks for (defaults to today). |
| Access | Google sign-in, limited to the company Google Workspace domain. Individual accounts. |
| Audit | Record who changed an item's owner, text, due date or done status, when, and the old and new values. |
| LLM | Sending notes to the Claude API is approved. |
| Architecture | Approach 1: the LLM extracts, deterministic code decides the owner and the date. One full-stack TypeScript app. |

### Non-goals (v1)

- Notifications (email, Slack, reminders)
- Calendar, Slack, Granola or other integrations; notes arrive by paste only
- Several teams or rosters; one team, one board
- Several owners per item (an item has exactly one owner; see §5.2 for splitting)
- Comments, attachments, priorities, recurring items
- Re-running extraction on notes after they've been committed
- Native mobile app (the web UI should work in a mobile browser, but that isn't optimized)

## 2. Architecture

A single **Next.js (App Router) TypeScript** application serves both the UI and the server-side logic, backed by **Postgres**.

```
Browser ──► Next.js app ──► Postgres
              │
              ├─► Auth.js (Google provider, domain-restricted)
              └─► Claude API (extraction only)
```

- **Auth:** Auth.js with the Google provider.
- **DB access:** Drizzle ORM with SQL migrations.
- **Validation:** Zod for LLM output and for all request bodies.
- **Date parsing:** `chrono-node`, wrapped in our own module with fixed rules (§5.3).
- **LLM:** Anthropic TypeScript SDK. The model is set by the `CLAUDE_MODEL` env var and defaults to `claude-opus-5`. Output is constrained to a JSON schema via structured outputs (`client.messages.parse` + `zodOutputFormat`).
- **Hosting:** host-agnostic. Any Node 20+ host plus managed Postgres (with encryption at rest). HTTPS required.

### Configuration (env vars)

`DATABASE_URL`, `AUTH_SECRET`, `AUTH_GOOGLE_ID`, `AUTH_GOOGLE_SECRET`, `ALLOWED_DOMAIN` (placeholder `ourcompany.com` until the real Workspace domain is set before launch), `ANTHROPIC_API_KEY`, `CLAUDE_MODEL` (optional, default `claude-opus-5`), `EXTRACTOR` (optional; `fake` selects the deterministic test extractor and is refused when `NODE_ENV=production`), `AUTH_TEST_BYPASS` (E2E only; refused when `NODE_ENV=production`), `DATE_LOCALE` (optional, default `en-US`).

## 3. Units and boundaries

Each unit has one job and can be tested on its own. The three core rules are pure functions with no I/O, which makes the correctness-critical logic easy to unit-test.

| Unit | Responsibility | Depends on |
|---|---|---|
| `lib/roster/resolveOwner` (pure) | Owner name as written in the notes + roster → assigned member or flag | nothing |
| `lib/dates/resolveDue` (pure) | Due date as written + meeting date → ISO date, or null + flag | chrono-node |
| `lib/notes/locateQuote` (pure) | Source quote + notes text → character range, or not-found | nothing |
| `lib/extraction/extract` | Notes → raw extracted items (text, owner name as written, due date as written, source quote). The only module that talks to Claude. | Anthropic SDK, Zod |
| `lib/extraction/buildDraft` | Runs extract, then resolveOwner, resolveDue and locateQuote on each item → draft items with flags | the four units above |
| `lib/items/service` | Commit a draft, update an item, complete or reopen an item. Every change writes audit events in the same transaction. | DB |
| `lib/auth` | Auth.js config and domain check; `requireUser()` helper for server actions and routes | Auth.js |
| UI pages | Paste, Review, Board, Team, Item history | server actions |

The extractor sits behind an interface (`Extractor`), so tests and local development can swap in a fake that returns fixed items.

## 4. Data model

```
users            id, email (unique), name, created_at
                 -- created on first sign-in; the logged-in person

team_members     id, display_name (unique), aliases text[], created_at
                 -- the 8-person roster; seeded from a config file, aliases editable in the UI

meetings         id, title, meeting_date (date), notes_text, notes_hash,
                 status ('draft' | 'committed'),
                 extraction_state ('pending' | 'done' | 'failed'), extraction_error (nullable text),
                 created_by → users, created_at, committed_at

action_items     id, meeting_id → meetings,
                 text,
                 owner_member_id → team_members (nullable while draft),
                 owner_raw (nullable)        -- owner name exactly as the LLM returned it
                 owner_suggestions uuid[]    -- members matched in a multiple_owners mention, or a selection suggestion
                 due_date (nullable date),
                 due_raw (nullable)          -- due date exactly as written, e.g. "by Friday"
                 source_quote, source_start (nullable int), source_end (nullable int),
                 flags text[]                -- see §5.2 / §5.3 / §5.4
                 origin ('extracted' | 'manual_selection'), position (int, display order),
                 status ('draft' | 'open' | 'done'),
                 completed_by → users (nullable), completed_at (nullable),
                 created_at, updated_at

item_events      id, item_id → action_items, actor_id → users, at,
                 kind ('created' | 'text' | 'owner' | 'due_date' | 'completed' | 'reopened'),
                 old_value jsonb, new_value jsonb

roster_events    id, member_id → team_members, actor_id → users, at,
                 old_aliases text[], new_aliases text[]
```

Rules:
- Items with status `open` or `done` **must** have a non-null `owner_member_id`. The service layer enforces this, backed by a DB check constraint: `status = 'draft' OR owner_member_id IS NOT NULL`.
- Draft edits are **not** audited. Audit starts when an item reaches the board. The `created` event records the final committed values, plus `owner_raw`/`due_raw`, so the extraction can always be compared with what the reviewer approved.
- Nothing is hard-deleted after commit. Draft items can be deleted on the review screen before commit.

## 5. Core logic

### 5.1 Extraction (`lib/extraction/extract`)

- A single Claude call per meeting. The system prompt explains what counts as an action item: a commitment by a person or group to do something. Decisions, FYIs and discussion points don't count. The prompt tells the model to:
  - return **every** action item, and lean towards including a borderline one rather than leaving it out (the reviewer can delete it);
  - copy the owner **exactly as written**, or return null. It must never infer, normalize or expand names, and it is **not given the roster**;
  - copy the due date **exactly as written**, or return null. It must not compute dates;
  - give a `source_quote`: a verbatim substring of the notes the item came from.
- Output schema (validated with Zod): `{ items: [{ text: string, owner_mention: string|null, due_mention: string|null, source_quote: string }] }`.
- Input limit: notes up to 50,000 characters. Anything longer is rejected on the paste form with a clear message. Chunking is out of scope for v1.
- Notes text is never written to application logs.

### 5.2 Owner resolution (`lib/roster/resolveOwner`)

Input: `owner_mention` and the roster (each member's display name and aliases).

Normalization, applied to both the mention and the roster names: trim, lowercase, remove diacritics (so "Tomas" matches "Tomás" without a configured alias), strip surrounding punctuation (including a leading `@`), drop a trailing possessive "'s", collapse whitespace. A member's display name and each alias are all match keys.

Outcomes:

| Situation | Result | Blocks commit? |
|---|---|---|
| Mention is null or empty | flag `missing_owner` | yes |
| Mention matches exactly one member's key, or splits into parts that all match the same single member | assign that member | — |
| Mention splits (on `and`, `&`, `,`, `/`) into parts that each match a member, with 2+ distinct members | flag `multiple_owners` (with the matched members listed as suggestions) | yes |
| Anything else, including "team", "everyone", "legal" or unknown names | flag `unknown_owner` | yes |

Only exact key matches count. There's **no** fuzzy matching, prefix matching or edit-distance matching. "Tommy" doesn't match Tomás unless "tommy" is a configured alias. This is how "never guessed" is enforced.

Alias uniqueness: after normalization, a key can belong to only one member. The Team page rejects saving an alias that clashes with another member's key. Because of this, a single-name mention can never match two people, so there is no separate "ambiguous" outcome.

On the review screen, a flagged owner is resolved by choosing a member from a dropdown. For `multiple_owners`, the reviewer can pick one member, or click **"Split"**, which duplicates the row once per suggested member with the owner already filled in.

Suggested seed aliases (edited on the Team page): Tomás → `tom`; the others start with none. The team adds more as flags come up.

### 5.3 Due date resolution (`lib/dates/resolveDue`)

Input: `due_mention` and `meeting_date`.

- Null mention → `due_date = null`, no flag. "No date" is a legitimate state.
- Parsed with chrono-node, using `meeting_date` as the reference date and forward-looking dates:
  - Leading filler words (`by`, `before`, `due`, `on`, `until`, `till`, `no later than`) are ignored.
  - A weekday name (or "this <weekday>") means the next occurrence **strictly after** the meeting date. "Friday" said on a Wednesday is 2 days later; said on a Friday, it's 7 days later.
  - "next <weekday>" is ambiguous (this coming one, or the one after?), so it is **not** resolved: `unparsed_due`.
  - "today", "EOD", "end of day" → the meeting date.
  - "tomorrow", "next week" (the Monday after the meeting's week), "end of week" (the Friday of the meeting's week, or the next Friday if the meeting is on a Saturday or Sunday), "end of month" (the last day of the meeting's month) and explicit dates ("Oct 3", "3/10") are all supported. Numeric dates are read in the locale set by the `DATE_LOCALE` env var, default `en-US` (month/day).
  - An explicit date without a year means the next occurrence on or after the meeting date.
- If the mention can't be parsed → `due_date = null`, flag `unparsed_due`. **This does not block commit**; the reviewer sees the original text and can pick a date.
- The review screen always shows the original text next to the computed date, e.g. "by Friday → Fri 2 Oct".

### 5.4 Source quote location (`lib/notes/locateQuote`)

- Look for the quote in the notes as an exact substring first, then as a normalized substring: whitespace runs (including CRLF and non-breaking spaces) collapsed to one space, curly quotes mapped to straight quotes, en/em dashes mapped to `-`. This handles notes pasted from Word or Google Docs.
- Found → store `source_start`/`source_end`.
- Not found → flag `quote_not_found` (doesn't block commit, shown as a warning). The item may have been paraphrased or invented, so the reviewer should check it.

### 5.5 Blocking vs. warning flags

- **Blocking** (the "Add to board" button stays disabled while any item has one; the server re-checks): `missing_owner`, `unknown_owner`, `multiple_owners`.
- **Warning** (highlighted, doesn't block): `unparsed_due`, `quote_not_found`, `possible_duplicate`.

`possible_duplicate` is set on an extracted item whose text (lowercased, punctuation and extra whitespace removed) equals an earlier item's text in the same meeting. This catches notes that list an action inline and again in an "Action items" recap at the end. The reviewer deletes the duplicate or keeps both.

Resolving a flag in the UI (e.g. choosing an owner) removes it from the item's `flags`.

## 6. User flows and screens

### 6.1 Sign-in

- Google sign-in via Auth.js, with the `hd=<ALLOWED_DOMAIN>` parameter as a hint.
- **Server-side enforcement** in the `signIn` callback: allow only if `profile.email_verified === true` **and** `profile.hd === ALLOWED_DOMAIN` **and** the email ends in `@ALLOWED_DOMAIN`. Otherwise, show an "Access restricted to <domain>" page.
- Every page and server action requires a session (middleware, plus `requireUser()` inside each action). There are no public routes except the sign-in and error pages.
- Any user on the domain can sign in. Signed-in users are separate from roster members: owners come from the roster, and the actor recorded in audit events comes from `users`.

### 6.2 Paste (`/new`)

- Fields: meeting title (required), meeting date (defaults to today in the browser's time zone), notes (textarea, max 50,000 characters).
- On submit:
  1. Save the meeting as a `draft`, so the notes are safe before the LLM is called.
  2. If `notes_hash` matches an existing meeting, show a warning ("These notes were already added on <date> as <title>"), with options to continue or open the existing meeting.
  3. Run `buildDraft`, save the draft items, and redirect to the Review screen.

### 6.3 Review (`/meetings/[id]/review`)

- **Left:** the original notes. Text ranges that produced an item are highlighted, and clicking a highlight scrolls to that item. Text that produced nothing stays unhighlighted, which makes missed items easy to spot.
- **Right:** editable item rows, each showing text, an owner dropdown (roster, with the original owner name shown underneath), a date picker (with the original due-date text shown underneath), flag badges, and delete.
- **Add missed item:** select text in the notes and click "Add as item". This creates a row with that text, `origin = manual_selection`, the source range set, and flag `missing_owner`. If the selected text contains exactly one roster key as a whole word, that member is suggested in the dropdown but **not** assigned.
- **Add to board:** enabled only when there are no blocking flags. The server checks again, then in one transaction moves the items from `draft` to `open`, sets the meeting to `committed`, and writes one `created` event per item.
- A draft meeting can be left and resumed later. A "Drafts" list on the Board shows uncommitted meetings.
- If there are zero extracted items, the screen says "No action items found." The reviewer can add items from selections, or commit an empty meeting.

### 6.4 Board (`/board`)

- Shows all `open` items across meetings. Default sort: overdue first, then by due date ascending, with no-date items last.
- Filters: owner (roster member), meeting. There's also a "Show done" toggle for items completed in the last 14 days.
- An item is **overdue** when `due_date` is before today's date in the viewer's browser time zone.
- Each row: checkbox, text, owner, due date (red when overdue), meeting title and date (links to the meeting's notes, scrolled to the source quote).
- **Tick:** sets the item to `done` and records `completed_by`/`completed_at` plus a `completed` event. Unticking a done item reopens it and records a `reopened` event.
- **Inline edit:** text, owner (dropdown), due date. Each changed field writes its own audit event.
- **History:** a per-item panel lists its events: "Marcus changed owner Tomás → Ravi · 26 Sep 14:02".
- The board refreshes when the page regains focus. Live updates are out of scope.

### 6.5 Team (`/team`)

- Lists the 8 roster members and their aliases. Any signed-in user can add or remove aliases. The clash check from §5.2 applies, and every change writes a `roster_events` row.
- The roster itself (adding or removing members) comes from a seed config file (`config/roster.json`) and can't be edited in the UI in v1.
- Alias changes don't retroactively change any items. They affect future extractions only.

## 7. Error handling

| Failure | Behavior |
|---|---|
| Claude API error or timeout (120 s per attempt, one SDK retry), or Claude declines the request (`stop_reason: "refusal"`) or runs out of output tokens | The meeting stays a draft with its notes saved. The Review screen shows "Extraction failed" and a **Retry** button. Nothing is lost. |
| LLM output fails schema validation | One automatic retry. If it fails again, treat it as an API error (above). |
| Notes over the limit | Rejected on the form before saving, with a message. |
| Commit attempted with blocking flags (e.g. an out-of-date client) | Server rejects with 409, and the UI reloads the draft with the flags visible. |
| Concurrent edits to the same item | Last write wins. Both changes appear in the audit log. |
| Sign-in from the wrong domain or an unverified email | "Access restricted" page; no user row is created. |
| Unexpected server error | Generic error page. The error is logged without notes text or item text. |

## 8. Security and confidentiality

- The app is only reachable behind authentication. The domain check is enforced on the server (§6.1).
- HTTPS only. Secure, HTTP-only session cookies (Auth.js defaults).
- Postgres is encrypted at rest by the managed provider.
- Notes and item text are never written to logs or error trackers.
- Notes are sent to the Claude API for extraction (approved). Nothing else goes to third parties.
- Server actions use Next.js's built-in CSRF protection. All inputs are validated with Zod.

## 9. Testing strategy

- **Unit (pure functions, the most important layer):**
  - `resolveOwner`: display names, aliases, diacritics ("Tomas"), possessives ("Priya's"), case, punctuation, empty or null mentions, "Tom and Priya" → `multiple_owners`, "Tommy"/"team"/"legal"/"Sam" → `unknown_owner`, and alias-clash detection.
  - `resolveDue`: a table of meeting-date × phrase cases, including the weekday-on-the-same-weekday edge case, end of week or month, month boundaries, year rollover, numeric dates under the locale, and unparseable input.
  - `locateQuote`: exact match, whitespace-normalized match, not found.
- **Extraction contract:** Zod schema tests with valid and invalid fixtures, and a retry-on-invalid test using a stubbed SDK client.
- **Service/integration (real Postgres in test):**
  - Commit is rejected while blocking flags remain.
  - Commit writes `created` events.
  - Each edited field writes exactly one event with correct old and new values.
  - Complete and reopen are recorded.
  - The DB constraint rejects an open item without an owner.
- **Auth:** unit tests for the `signIn` domain check (right domain; wrong domain; missing `hd`; unverified email; a lookalike domain such as `example.com.evil.io`).
- **End-to-end (Playwright, fake extractor, test-only auth bypass enabled only when `AUTH_TEST_BYPASS=1`; the app refuses to start with it when `NODE_ENV=production`):** paste → review → resolve a flagged owner → add a missed item from a selection → commit → board → tick → history shows the change.
- **Extraction eval (manual, run on demand against the real API; not in CI):** a golden set of 5–10 anonymized real meeting notes from the team, each with its expected items and owners. A script reports item recall, false positives, and owner-name accuracy. Target: 100% recall on the golden set before launch. The team will supply the real notes before launch, so they aren't needed to start building. Until then, the eval harness ships with 2–3 synthetic sample notes to prove the script works. Anything the model misses becomes a prompt fix plus a new golden case.

## 10. Project layout

```
config/roster.json
drizzle/                      migrations
src/
  app/
    (auth)/signin, (auth)/restricted
    new/page.tsx
    meetings/[id]/review/page.tsx
    board/page.tsx
    team/page.tsx
    api/auth/[...nextauth]/route.ts
  lib/
    auth/                     config, requireUser, domain check
    db/                       schema, client
    roster/resolveOwner.ts
    dates/resolveDue.ts
    notes/locateQuote.ts
    extraction/               extract.ts, prompt.ts, schema.ts, fakeExtractor.ts, buildDraft.ts
    items/service.ts
  components/                 NotesPane, ItemRow, OwnerSelect, BoardTable, HistoryPanel
tests/
  unit/, integration/, e2e/
eval/                         golden notes + run-eval script
```
