# Meeting Action Items — Design Spec

**Date:** 2026-09-26
**Status:** Awaiting review

## 1. Purpose and success criteria

A web app for one team of 8. Someone pastes meeting notes (Google Docs bullet notes or Zoom/Granola transcripts); the app extracts every action item with owner and due date and puts them straight onto a shared board, where anyone can tick them off.

**It works when:** every action item from a meeting shows up on the board with the right owner, and nobody has to retype items.

Measured by the accuracy eval (section 8) against three launch bars:

1. **No missed items** — every expected item appears on the board (flagged or not).
2. **No silently wrong owners** — an item with the wrong owner and no "needs review" flag is a hard fail. Wrong-but-flagged is acceptable.
3. **Flag rate ≤ 15%** of extracted items, so the review group stays meaningful.

## 2. Decisions and constraints

| Topic | Decision |
|---|---|
| Review model | No approval step. Items go straight to the board; uncertain items carry a visible **needs review** flag with reasons. |
| Owners | Must be one of the fixed roster. Names not on the roster are flagged, **never guessed**. |
| Roster | Priya, Marcus, Sarah, Tomás, Aisha, Dana, Ravi, Lena — kept in a config file in the code (name, work email, aliases). Changing it means a small code change and redeploy. |
| Access | Google sign-in, restricted to the company Google Workspace domain. Notes are confidential. |
| LLM | Anthropic API, Claude Opus 5 (`claude-opus-5`). Sending notes to Anthropic is approved. |
| Extraction approach | One Claude call returning structured output, followed by checks in code (Approach 1). A second "what did we miss?" pass is added **only** if the eval shows missed items. |
| Stack | TypeScript, Next.js (App Router), Auth.js (Google provider), Postgres, Vercel. |
| Out of scope for v1 | Detecting duplicates across meetings, live multi-user updates, an in-app roster editor, integrations (Slack, Jira, Notion), notifications. |

## 3. Architecture

Units, each with one job and testable on its own:

| Unit | Job | Depends on |
|---|---|---|
| `auth` | Google sign-in. Checks on the server that the email is verified and on the company domain. Maps the signed-in user to a roster member by email, where they have one. | Auth.js |
| `roster` | Holds the roster config. `resolveOwner(nameAsWritten)` returns a member or `unknown`. Matching ignores case and accents and checks aliases. | none |
| `extract` | `extractCandidates({notes, meetingDate, roster})` makes one Claude call and returns the raw candidates. | Anthropic SDK |
| `validate` | `validateCandidates(candidates, {notes, meetingDate, meSpeaker})` resolves owners, checks dates and quotes, and attaches review reasons. **Plain code, no API or database calls.** | `roster` |
| `db` | Postgres access for meetings and action items. | Postgres |
| Pages / server actions | Paste page, Board, Meeting page. Each server action checks the session. | all of the above |

**Flow:** Paste form submits → `extract` → `validate` → one database transaction inserts the Meeting and all its ActionItems → redirect to the Meeting page, showing "N items added, M need review."

## 4. Data model

**Meeting**
- `id`
- `title`
- `meeting_date` (date)
- `raw_notes` (text)
- `notes_hash` (sha256 of the whitespace-normalised notes, used for the duplicate-paste warning)
- `me_speaker` (roster member or null)
- `created_by` (email)
- `created_at`

**ActionItem**
- `id`
- `meeting_id` → Meeting
- `task` (text)
- `owner` (roster member key, **nullable** — null means unresolved)
- `owner_as_written` (text, nullable)
- `due_date` (date, nullable)
- `due_as_written` (text, nullable)
- `source_quote` (text)
- `needs_review` (bool)
- `review_reasons` (text[])
- `status` — `open` | `done` | `deleted`
- `status_changed_by`, `status_changed_at`
- `created_at`, `updated_at`

Delete sets the status to `deleted` (the row is hidden, not erased), so undoing a tick and undoing a delete work the same way.

## 5. Extraction pipeline

### 5.1 Claude call (`extract`)

- **Request settings:**
  - Model `claude-opus-5`, adaptive thinking.
  - Streamed, with the SDK collecting the final message, to avoid request timeouts on long transcripts.
  - Server-side refusal fallbacks enabled (`fallbacks: "default"` with the `server-side-fallback-2026-07-01` beta).
  - Structured output via `output_config.format`, with a JSON schema describing a list of items.
- **Input:**
  - the roster (names and aliases)
  - the meeting date
  - the notes

  The "Me" choice is deliberately **not** sent to the model; it is resolved in `validate`.
- **Instructions to the model:**
  - Extract **every** commitment or assigned task, including implied ones in transcripts ("I'll take that" → the speaker).
  - Copy `owner_as_written` exactly as it appears. Never substitute a roster name. For implied owners in transcripts, use the speaker label verbatim (for example `Me`, `Them`, `Speaker 2`, `Priya Shah`).
  - Still extract items whose owner is not on the roster.
  - For a shared task, emit one item per named owner.
  - Resolve relative dates ("next Friday", "end of month") from the meeting date into `due_date`, and keep the original phrase in `due_as_written`. If no date is mentioned, both are null.
  - `source_quote` is a short, verbatim excerpt from the notes.
  - Set `confidence: "low"` with a `reason` when the item or owner is ambiguous.
- **Candidate schema:**
  - `task`
  - `owner_as_written | null`
  - `due_as_written | null`
  - `due_date (YYYY-MM-DD) | null`
  - `source_quote`
  - `confidence: "high" | "low"`
  - `reason | null`
- **Failures:**
  - A `refusal` that survives the fallback → error.
  - `max_tokens` → error. **Never** save a partial list.
  - API errors are retried by the SDK (default retries). If they still fail → error.

### 5.2 Checks in code (`validate`)

Each failed check appends a reason and sets `needs_review = true`.

1. **Owner.**
   - If `owner_as_written` is exactly `Me` (ignoring case and surrounding whitespace) and `meSpeaker` is set, the owner is `meSpeaker`. If `meSpeaker` is not set, it is unresolved.
   - Matching is exact on the whole name (after ignoring case and accents), with no partial or first-word matching, so an unknown "Priya Kumar" can't be silently merged with our Priya. Each member's full name is therefore listed among their aliases in the roster config.
   - Otherwise, `resolveOwner(owner_as_written)`.
   - Unresolved → owner null, reason `unknown owner "<as written>"`.
   - Null `owner_as_written` → reason `no owner`.
   - Labels such as "Them" and "Speaker 2" are always unresolved.
2. **Due date.**
   - `due_as_written` present but `due_date` null or invalid → reason `couldn't resolve "<phrase>"`.
   - `due_date` before `meeting_date` → reason `due date before meeting`.
   - Neither present → no date, no flag.
3. **Quote.** `source_quote` must be a substring of the notes after whitespace is normalised and case is ignored. Otherwise → reason `quote not found in notes`.
4. **Model confidence.** `confidence: "low"` → the model's `reason` is added.

## 6. Pages

**Paste page**
- **Fields:**
  - title
  - meeting date (defaults to today in the browser's timezone)
  - "Who is 'Me'?" dropdown: roster members plus "nobody", defaulting to the signed-in user's roster entry
  - notes text box
- **Extract button:** shows progress.
- **On failure:** an error message; the form keeps everything that was entered.
- **Duplicate paste:** if `notes_hash` matches an existing meeting → "These notes were already added on <date>", with Continue or Cancel.
- **On success:** redirect to the Meeting page with the "N added, M need review" summary.

**Board (home page)**
- Shows all `open` items, grouped by owner in roster order.
- A **Needs review** group comes first and holds flagged items plus items with no owner.
- **Each row shows:**
  - checkbox
  - task
  - owner
  - due date (overdue highlighted; items with no date sorted last within the group)
  - meeting link
  - flag badge listing the reasons
- Expanding a row shows the `source_quote`.
- **Filters:** by owner; needs review only.
- **"Show done" toggle:** shows `done` items.
- **Ticking:** sets `done`, records who and when, and shows a brief **Undo** link.
- **Deleting:** sets `deleted`, with the same **Undo** link.
- **Editing inline:**
  - owner dropdown (roster only)
  - date picker
  - task text
- **Clearing flags:**
  - Changing the owner or date removes the matching reasons (owner-related or date-related).
  - A "Looks right" button clears all reasons.
  - `needs_review` becomes false once no reasons remain.
- **Refresh:** the board reloads when the page is opened and when the browser tab regains focus.

**Meeting page**
- The original notes plus that meeting's items, with the same row controls as the Board.
- An **Add item** button for manual additions (task, owner from the roster, optional date).

## 7. Error handling and security

- **Transactions:** the meeting and its items are inserted in a single transaction; any failure saves nothing.
- **Zero items extracted:** the meeting is saved, and the page shows "No action items found — add one manually if we missed something."
- **Input limits:**
  - Empty notes are rejected.
  - Notes over 400,000 characters are rejected with a message, never trimmed.
- **Access:**
  - Every page and server action checks for a session on the server.
  - The session requires `email_verified` and an email on the configured domain (`ALLOWED_EMAIL_DOMAIN`).
  - Anyone else sees an Access denied page.
- **Logging:** never logs note text, task text or quotes. Only IDs, timings, error types and token usage.
- **Secrets** live in environment variables on Vercel:
  - `ANTHROPIC_API_KEY`
  - `AUTH_GOOGLE_ID` and `AUTH_GOOGLE_SECRET`
  - `AUTH_SECRET`
  - `DATABASE_URL`
- **Notes that contain instructions:** the model has no tools, its output is only structured data, and every item goes through `validate`.
- **Concurrent edits:** last write wins; status changes are idempotent.
- **Pre-launch:** confirm Anthropic's data-retention and training terms for our account with security or compliance.

## 8. Testing

**Automated (run on every change, no real API calls)** — Vitest, plus Playwright for end-to-end:
- **`roster`:** every name, alias and accent variant; unknown names; "Them" and "Speaker N".
- **`validate`:** each rule and reason in section 5.2, including "Me" with and without `meSpeaker`.
- **`extract`**, against a fake client:
  - schema parsing
  - `refusal` → error
  - `max_tokens` → error
  - API error → error
- **Database and server actions:**
  - transaction atomicity
  - tick/undo and delete/undo
  - clearing flags on edit
  - duplicate-paste detection
  - signed-out and wrong-domain requests rejected
- **One Playwright flow**, with extraction faked: sign in → paste → board → fix a flagged item → tick → undo.

**Accuracy eval (real Claude, run on demand)**
- **Data:** the team supplies 10–20 real past meetings covering Docs bullets, Zoom transcripts and Granola transcripts, including at least two with "Me"/"Them" labels. Each comes with a hand-written list of expected items (task, owner, due date).
- **Storage:** everything lives in `evals/data/`, which is **git-ignored** (confidential).
- **The script:**
  - runs `extract` and `validate` for each meeting
  - matches extracted items to expected ones: Claude judges only whether two task descriptions mean the same thing; owner and date are compared exactly in code
- **The report shows:**
  - missed items
  - wrong owners, split into flagged and unflagged
  - wrong dates
  - extra items
  - flag rate
- **Launch bars:** see section 1.

## 9. Future (not v1)

- Possible-duplicate detection across meetings, surfaced as another flag reason.
- A second "what did we miss?" extraction pass, if the eval shows missed items.
- An in-app roster and alias editor.
