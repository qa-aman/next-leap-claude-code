# Action Items Board: Spec (v1)

**Status:** Draft for build · **Author:** Aman (admin) · **Date:** 2026-09-26 · **Target:** v1 in 2 weeks

## 1. Summary

A small internal web app for an 8-person team. Someone pastes meeting notes (Google Doc text or a Zoom transcript). Claude extracts the action items with owner and due date. The person who pasted reviews and fixes them on one screen, then confirms. The items go onto a shared board, where anyone can tick them off.

**Success means:** every action item from a meeting reaches the board with the right owner, and nobody retypes them. When the app isn't sure, it shows a visible flag instead of guessing. **A wrong owner or date is worse than a blank one with a flag.**

## 2. Users and roles

| Role | Who | Can do |
|---|---|---|
| Member | Priya, Marcus, Sarah, Tomás, Aisha, Dana, Ravi, Lena | Paste notes, review own drafts, tick/untick any item, edit own items, take any item for themselves, assign unassigned items |
| Admin | Aman | Everything a member can, plus: edit/reassign/delete any item, manage roster and aliases, discard any draft |

**Initial roster** (the admin can edit it later on the roster page):

| Name | Aliases | Email |
|---|---|---|
| Priya | | TBD |
| Marcus | | TBD |
| Sarah | | TBD |
| Tomás | Tom, Tomas | TBD |
| Aisha | | TBD |
| Dana | | TBD |
| Ravi | | TBD |
| Lena | | TBD |

"Tom" is confirmed by Aman. "Tomas" (no accent) is added because transcripts and typing often drop the accent. Name matching also ignores case and accents in general.

- One team, one board. No sub-teams or groups.
- People outside the roster are never owners (see §5.3).

## 3. Out of scope

v1 is only: paste → extract → review → confirm; the board; permissions and change history; admin roster page; 30-day deletion of raw notes; re-running extraction.

**We are NOT building the following.** If a request touches one of these, stop and ask Aman first.

| Not building | Note |
|---|---|
| Notifications of any kind (email, Slack, reminders) | The Slack digest (Mondays 9:00 IST) is v2 |
| Importing notes from Google Docs, Zoom, Granola, email or Slack | Pasting only |
| Calendar integration | |
| Audio recording or transcription | |
| Mobile app | The web app should still be usable in a phone browser |
| Jira / Linear / Asana sync | |
| Sub-tasks, comments, priorities, recurring items | |
| Multiple teams or boards, or teams/groups as owners | One team of 8, one board |
| People outside the roster as owners | External tasks are ignored (§5.1) |
| Access without login, or shareable public links | Google sign-in on the company domain only |
| Real-time live updates on the board | Refresh on load and when the window regains focus |
| Guessing unclear owners or dates | Blank + flag instead (§5) |
| Keeping raw notes longer than 30 days | Only extracted items and snippets are kept |
| Time zones other than IST | |

## 4. Core flow

### 4.1 Paste

The form has these fields:
- **Meeting name** (required): free text, with autocomplete from existing names (for example "Weekly Product Sync"). Reusing a name groups meetings into a **series**. A new name creates a new series. Matching ignores case and extra whitespace.
- **Meeting date** (required): defaults to today (IST) and can be edited. All relative dates are calculated from this date, never from the paste date.
- **Notes** (required): one large text box. Maximum 20,000 words. Anything longer gets a clear error. Never truncate silently.

**Double-paste guard:** if a meeting with the same series and date already exists (draft or confirmed), show "*Weekly Product Sync, 26 Sep* was already pasted by Priya" with buttons **Open it** and **Paste anyway**.

**Pre-processing (in code, before calling Claude):** strip Zoom/VTT timestamp lines and cue numbers, and join the speaker lines. This cuts tokens and cost without losing content. Keep the original text for storage and viewing.

### 4.2 Extraction

- Runs in a single Claude call per paste (see §7). The whole document fits in one call, so there's no chunking.
- It takes about 30–120 seconds. Show a progress state ("Reading notes… this can take up to 2 minutes"). The user can leave the page; the draft appears in "In review" when it's ready.
- If it fails (timeout, API error, or the job is stuck in "extracting" for more than 5 minutes), the draft shows **Failed – Retry**. The raw notes are already saved, so nothing is lost.

### 4.3 Review (draft)

An editable table of the extracted items. Each row shows:
- Item text (English, starting with a verb, 120 characters or fewer)
- Owner (dropdown of roster members plus "Unassigned")
- Due date (date picker, can be blank) plus the **raw date phrase** from the notes, for example "parso" or "end of Q3"
- Flags (badges; see §6)
- Source snippet (the original sentence, which may be Hinglish), expandable
- Duplicate suggestion, if any: "Looks like an open item: *Send pricing doc* (Sarah, from 19 Sep)" with **Skip (default)** or **Add anyway**

Actions available:
- Edit any field
- Delete a row
- **Add item manually** (a fallback for anything missed)
- **Re-run extraction**
- **Discard draft**
- **Confirm → board**

Rules:
- You can confirm while flags are still open. Flagged items reach the board with their badges.
- Only the person who pasted (and the admin) can edit a draft. Everyone can see a list of drafts ("In review: Weekly Product Sync, 26 Sep, Priya") on the paste page and as a small banner on the board.
- Drafts are saved automatically. Closing the tab loses nothing.
- Re-running on an already-confirmed meeting creates a new draft. Items already on the board are shown as duplicates, so only genuinely missed items get added.

### 4.4 Board

- A single list. **Default sort:** overdue first, then due today, then by due date ascending, with blank dates last.
- **Filters:** Owner (including "Unassigned"), Meeting series, and specific meeting (series + date). Quick filters: **My items** and **Needs attention** (any flag).
- **Row:** checkbox · text · owner · due date · meeting name + date · badges. Overdue rows have a red date and a red left border. Rows due today have an amber date.
- **Expanding a row** shows the source snippet, flags, "created from *meeting* by *paster*", and the change history.
- **Completed items** are hidden by default, with a "Show completed" toggle. A completed item shows "✓ Dana, 27 Sep 14:10". Ticking an item shows an **Undo** toast. Unticking a completed item returns it to open, and that is also recorded.
- No real-time sync. The board refreshes on page load and when the window regains focus. With 8 users, the last write wins; the history shows what happened.

## 5. Extraction rules (what counts, who owns it)

These rules go into the extraction prompt verbatim. They are also what the test set is graded against (§11).

### 5.1 What becomes an item

| Case | Result |
|---|---|
| Clear task with an owner | Item |
| Decision with no task ("we'll go with vendor X") | Ignore |
| Conditional task ("if legal approves, Sarah ships it") | Item. The condition stays in the text; flag `conditional` |
| Already done during the meeting ("Dana already sent it") | Ignore |
| Retracted later in the meeting ("scratch that") | Ignore |
| Owner named once at the top of a section, followed by bullets | Item(s) with that owner |
| Multiple owners ("Priya and Marcus to draft proposal") | **Split** into one item per person, with the same text and date |
| Task for an external person ("John from Acme sends contract") | Ignore |
| Borderline / unsure whether it's a task | **Include it with the flag `maybe_not_task`.** Deleting an item in review is cheap; a missed item is the main failure. |

### 5.2 Owner resolution

- Claude receives the roster: each member's id, name and aliases (for example Tomás: "Tomas", "Tom"). It must return either a roster member id or `null`. **The server rejects any id not in the roster**, which turns it into Unassigned plus a flag.
- **"I'll do it" / "main kar dunga"** means the owner is the speaker. The speaker label is matched to the roster by name or alias (for example "Priya Sharma" matches Priya).
- If the speaker label can't be matched ("iPhone (2)", "Conference Room B"), the item is Unassigned, flagged `unknown_speaker`, and shows the raw label.
- "We'll…", "someone should…", or an unclear pronoun means Unassigned, flagged `owner_unclear`.
- **Name collision with an outsider** ("Sarah from Acme" when Sarah is on the roster): treat as external if the context says so. If unsure, include the item as Unassigned with the flag `owner_unclear` and never assign it to roster-Sarah.
- Owners are never guessed from job title or topic.

### 5.3 Due date resolution: done in **code**, not by Claude

Claude only classifies the date phrase into a structured form. The app computes the actual date deterministically from the meeting date. This keeps the date rules testable and predictable.

Claude returns, for each item:
- `date_phrase`: the exact text, for example "by Friday" or "parso"
- `date_kind`: one of the kinds below, with its parameters

| Kind | Example | Resolution (from meeting date, IST) |
|---|---|---|
| `explicit` | "3/10", "3 Oct", "October 3" | Day/month order (3/10 = 3 October). If no year is given, use the next occurrence on or after the meeting date |
| `today` | "today", "EOD", "aaj" | The meeting date |
| `tomorrow` | "tomorrow" (English only) | Meeting date + 1 |
| `in_n_days` / `in_n_weeks` | "in 3 days", "within 2 weeks" | Meeting date + N days / + N × 7 days |
| `weekday` | "by Friday", "Monday tak" | Next such weekday strictly after the meeting date. **If it's the same weekday as the meeting, leave blank and flag it** |
| `ambiguous` | "kal", "parso", "next Friday", "EOW", "end of Q3", "ASAP", "before the offsite", "soon" | **Blank + flag `date_unclear`**; show the phrase |
| `none` | no date mentioned | Blank, no flag |

- An impossible date (for example 31/02) is treated as `ambiguous`.
- "next Friday" is deliberately ambiguous (this coming Friday, or the one after?), following the "don't guess" rule.
- A date resolved to earlier than the meeting date gets blank + `date_unclear`.

### 5.4 Text and language

- Item text is always English, even when the notes are Hinglish or Hindi.
- The source snippet is a verbatim quote from the notes in the original language, 300 characters or fewer.
- **Snippet check:** the server confirms that the snippet appears in the notes (ignoring whitespace and case). If it doesn't, the item gets the flag `source_unverified`. This catches invented items.
- Mostly romanized Hinglish is expected. Devanagari must also work (no special handling, only a test case).

## 6. Flags

| Flag | Badge text | Raised when | Cleared when |
|---|---|---|---|
| `owner_unclear` | Needs owner | No clear owner | An owner is set |
| `unknown_speaker` | Who is "iPhone (2)"? | "I'll" from an unmatched speaker label | An owner is set |
| `date_unclear` | Date unclear: "parso" | Ambiguous or unresolvable phrase | A date is set, or the owner dismisses the flag |
| `conditional` | Conditional | Task depends on a condition | Owner dismisses it |
| `source_unverified` | Check source | Snippet not found in the notes | Reviewer or owner dismisses it |
| `maybe_not_task` | Is this a task? | Borderline: unsure whether it's a task (§5.1) | Reviewer or owner dismisses it |
| `possible_duplicate` | Possible duplicate | Matches an open item in the same series (review only) | Skip / Add anyway |
| `needs_reassignment` | Needs reassignment | Owner deactivated by admin | The owner is changed by anyone allowed to (§8), including a member taking it for themselves |

## 7. Claude integration

- **Model:** `claude-sonnet-5`, with adaptive thinking and effort `high`. Streaming, `max_tokens` about 64,000.
  - Chosen because the budget is a hard cap under $20 a month.
  - If the test set (§11) still fails after tuning the prompt and effort, revisit the model choice with the admin. Opus 5 is roughly 2.5× the cost.
- **Output:** structured outputs (JSON schema), so the response always parses. Schema per item: `text`, `owner_member_id | null`, `owner_raw`, `speaker_label | null`, `date_phrase | null`, `date_kind` + parameters, `source_snippet`, `flags[]`, `possible_duplicate_of | null`.
- **Prompt inputs:**
  - The rules in §5
  - The roster with aliases
  - The meeting date and weekday
  - The open items in the same series (id, text, owner), for duplicate detection
  - For a re-run of a confirmed meeting: that meeting's items too
  - The pre-processed notes
- Check the stop reason before reading the output. A refusal or a truncated response (`max_tokens`) marks the draft **Failed – Retry**. It is never treated as "no items".
- No retries inside the request beyond the SDK's defaults. The user-facing **Retry** button covers the rest.
- The prompt treats the notes as data. Anything in the notes that looks like an instruction to the app is ignored. All output is rendered as plain text, never HTML.

**Cost estimate** (Sonnet 5 at $2 input / $10 output per million tokens; about 1.4 tokens per word, more for Hinglish):

| | Input tokens | Output + thinking | Cost per run |
|---|---|---|---|
| Typical (5k words) | ~11k | ~5k | ~$0.07 |
| Worst case (15k words) | ~34k | ~10k | ~$0.17 |

About 43 meetings a month plus 20% re-runs is about 52 runs. That comes to **about $4 a month typical and about $9 worst case**, well under the $20 cap with hosting at $0. Safeguards:
1. Strip timestamps (§4.1).
2. Set a **$15 monthly spend limit in the Anthropic Console**, so the hard cap can't be exceeded even by a bug.
3. Track the actual cost per run in the app (log token usage per extraction).

## 8. Permissions and history

| Action | Who |
|---|---|
| Tick / untick | Any member |
| Edit text, due date; dismiss flags | Owner, admin |
| Reassign to anyone | Owner, admin |
| Take the item for yourself | Any member (Aisha can take an item sitting on Marcus) |
| Assign an Unassigned item to anyone | Any member |
| Delete (soft delete, recoverable by admin: the item is hidden, never erased. v1 has no restore screen; on request, Claude restores it in the database and writes the history entry. A restore screen can come in v2 if needed.) | Admin only |
| Edit / confirm a draft | Person who pasted, admin |

- **Every change is logged:** who, when, which field, old value → new value. This covers creation (with meeting and paster), edits, reassignments, ticks, unticks, flag dismissals and deletions. It's visible in the expanded row. The log itself can't be edited. History starts when an item reaches the board (the "created" entry). Edits made to a draft during review are not logged.
- Permissions are enforced on the **server**, not only hidden in the UI.

## 9. Data and retention

**Tables (Postgres):**
- `members`: id, name, email, aliases[], is_admin, active
- `series`: id, name (unique, ignoring case)
- `meetings`: id, series_id, meeting_date, pasted_by, status (`extracting` | `review` | `failed` | `confirmed` | `discarded`), raw_notes (nullable), notes_deleted_at, created_at, confirmed_at, token usage and cost per run
- `items`: id, meeting_id, state (`draft` | `open` | `done` | `deleted`), text, owner_id (nullable), due_date (nullable), date_phrase, flags[], source_snippet, speaker_label, duplicate_of (nullable), completed_by, completed_at, created_at
- `item_events`: id, item_id, actor_id, action, field, old_value, new_value, at
- `extraction_runs`: id, meeting_id, started_at, finished_at, status, stop_reason, input_tokens, output_tokens, cost_usd, error_code (one row per extraction run, including retries and re-runs)

Supporting columns, which store what this spec already requires: `members.created_at`, `series.name_key` (normalized name for the uniqueness check), `meetings.extraction_started_at` and `meetings.error_message` (for the 5-minute stuck rule and Failed – Retry), `items.owner_raw`, `items.duplicate_decision` (Skip / Add anyway) and `items.position` (row order in review).

**30-day rule:** a daily scheduled job sets `raw_notes = null` on every meeting created more than 30 days ago.
- Drafts that are still unconfirmed are discarded along with their draft items.
- Extracted items, snippets, meeting name and date, and history are kept forever.
- After deletion, "View notes" shows "Notes deleted on 26 Oct (30-day policy)", and **Re-run** is disabled.
- Note: the 30-day rule covers this app's database. Text sent to the Claude API follows Anthropic's own API data-retention policy. Database backups on the hosting provider may briefly hold older copies.

**Timezone:** everything is IST. Due dates are dates without times. "Overdue" means `due_date < today in IST`.

## 10. Tech stack and deployment

Chosen for: $0 hosting, commercial use allowed, a well-worn path for building with Claude Code, and one deploy target.

| Piece | Choice | Why |
|---|---|---|
| App | Next.js (TypeScript) | Most common stack; best Claude Code support |
| Hosting | Cloudflare Workers (free plan, via the OpenNext adapter), on a `*.workers.dev` URL | Commercial use allowed on the free plan; no wall-clock limit while a request waits on Claude |
| Database + login | Supabase free tier (Postgres + Google sign-in) | Free, includes auth |
| Scheduled job | Cloudflare Cron Trigger, daily | Runs the 30-day deletion **and** hits the database daily, which stops Supabase's free tier from pausing during quiet weeks |
| AI | Claude API (TypeScript SDK) | See §7 |

**Login:**
- Google sign-in through Supabase. After sign-in, the server allows access only if the email **ends with `@ALLOWED_DOMAIN`** (placeholder: `example.com`) **and** is an active roster member. Google's own domain hint is not relied on for security.
- Until the Workspace exists: set the Google OAuth consent screen to *External – Testing* and add the 8 emails as test users. Switch to *Internal* once the Workspace is set up.
- **Temporary (approved by Aman 2026-09-26):** until the Workspace exists, `ALLOWED_DOMAIN=gmail.com`, and the roster contains only Aman's Gmail. The roster check still refuses every other Gmail account. Switch to the company domain as soon as the Workspace is up.
- Step-by-step account setup: `docs/setup-accounts.md`.
- Database access happens only through the app's server using a secret key. Supabase row-level security is enabled with no public access, so the browser can't read the database directly.

**Configuration (environment variables):** `ANTHROPIC_API_KEY`, `SUPABASE_URL`, `SUPABASE_SERVICE_KEY`, `ALLOWED_DOMAIN`, `ADMIN_EMAIL`.
- Local-only, on Aman's Mac, never deployed or committed: `SUPABASE_DB_URL` (for setting up and updating tables), and the keys of a separate **test** Supabase project (`action-items-test`) that the automated tests use. Tests never touch the live database.

**Background extraction:** extraction runs as a background job (Cloudflare Queues), so it keeps going after the user leaves the page (§4.2).

**Day-1 risk check:** deploy a stub that makes a 2-minute streaming call from Cloudflare to Claude, and confirm (a) it isn't cut off and (b) a background run still finishes after the caller disconnects. If either fails, move only the extraction call to a Supabase Edge Function. Nothing else in the spec changes.
- The stub works only while a setting is switched on. It's switched off as soon as the Phase 1 check passes, and the code is deleted in Phase 5.

## 11. Acceptance: test set (required before v1 sign-off)

**Aman to supply 3–5 real or anonymized notes, each with an answer key** (the correct list of items, owner and due date, with "Unassigned" or "blank" where the notes are genuinely unclear). The set must include at least:
- 1 raw Zoom transcript with speaker labels, including at least one unmatched label
- 1 messy Google Doc (prose)
- 1 Hinglish meeting including "kal" or "parso"
- 1 near-maximum length (~15k words)
- 1 meeting that repeats an open item from an earlier meeting in the same series (tests duplicate detection)

The notes are stored in the repo under `tests/extraction/`, and an admin-only script runs extraction on them and prints a score. `01` is the worked example from the README; Aman's notes are numbered from `02`.

**Pass criteria, per note, over 3 runs each** (Claude's output varies between runs):
1. **Recall:** 100% of answer-key items are present.
2. **Owners:** zero items assigned to the wrong member. Unassigned with a flag where the key has a real owner counts as a miss that must be under 10% of items.
3. **Dates:** zero wrong dates. Blank with a flag is acceptable.
4. **Extras:** 1 or fewer non-items per meeting, and each is clearly removable in review.
5. **Duplicates:** the repeated item is marked as a possible duplicate.

If these fail, tune the prompt first, then effort. If Sonnet 5 still fails, raise the model choice with the admin (§7). Do not relax the criteria.

The format for the notes and answer keys is in `tests/extraction/README.md`.

Also test by hand before sign-off:
- Every permission rule in §8, including that it's rejected on the server
- The 30-day job, by setting a meeting's `created_at` 31 days back
- Retry after a forced failure
- Double-paste warning
- Deactivating a member produces `needs_reassignment`
- A non-roster Google account is refused

## 12. Phases

Five phases, built in order. A phase is done only when its **How we check it** passes. Don't start the next phase until then.

### Phase 1: Deployed skeleton, login, roster (days 1–3)

- Accounts: Cloudflare, Supabase, Anthropic (with the $15 spend limit), Google OAuth.
- Deploy an empty app to the `*.workers.dev` URL.
- Tables from §9.
- Google sign-in with the roster and domain check (§10).
- Admin roster page: add a member, edit aliases, deactivate.
- Long-call and background risk check (§10).

**How we check it:** Open the live URL in a private browser window.
- **Pass** if all four of these hold:
  - A roster account reaches the empty board (screenshot).
  - A non-roster Google account sees "Not authorized" (screenshot).
  - `curl <live-url>/api/dev/long-call` prints `ok` after running for more than 120 seconds.
  - `curl --max-time 10 "<live-url>/api/dev/long-call?background=1"` disconnects after 10 seconds, and about 3 minutes later `curl <live-url>/api/dev/long-call/status` prints `ok`.
- Anything else is a fail.

### Phase 2: Extraction engine, no screens (days 4–6)

- Pre-processing (§4.1).
- Date resolver (§5.3).
- Owner check against the roster (§5.2).
- Snippet check (§5.4).
- The Claude call (§7).
- `npm run eval`, the script that scores extraction against answer keys (§11).

**How we check it:**
- `npm test -- dates` passes, with one test for every row and bullet of §5.3.
- `npm run eval -- 01` on the worked example in `tests/extraction/README.md` reports 5/5 items with correct owners, dates and flags, and neither of the 2 non-items, on 3 runs out of 3.

### Phase 3: Paste, review, confirm (days 7–8)

- Paste form with the double-paste guard.
- Progress state and Failed – Retry.
- Review screen (§4.3): editing, add item manually, duplicates, re-run, discard, confirm.
- Drafts list.

**How we check it:**
- `npm test -- review` passes. It covers:
  - paste → draft → edit → confirm puts the items on the board
  - the same series and date shows the double-paste warning
  - a forced API failure shows Retry, and Retry works
  - re-running a confirmed meeting marks existing items as duplicates
  - a non-paster can't edit the draft
- Plus a screenshot of the review screen for the worked example, showing its 5 rows and their badges.

### Phase 4: Board, permissions, history (days 9–10)

- Board with sort, filters, My items and Needs attention (§4.4).
- Tick and untick with Undo; the Show completed toggle.
- Every permission rule in §8, enforced on the server.
- Change history in the expanded row.
- Deactivating a member → `needs_reassignment`.

**How we check it:**
- `npm test -- permissions` passes. For every row of the §8 table, it tries the action as an allowed user (saved and logged in history) and as a not-allowed user (rejected by the server). It also checks that deactivating a member flags their open items.
- Plus a screenshot of the board showing an overdue item with the red border, an item due today in amber, and a flagged item with its badge.

### Phase 5: Retention, cost, sign-off (days 11–14)

- Daily cron (30-day deletion + keep-awake).
- Cost logging per run.
- Run the real test set and tune the prompt (§11).
- Team walkthrough.

**How we check it:**
- `npm test -- retention` passes:
  - a meeting created 31 days ago loses its notes, and its unconfirmed draft is discarded
  - a meeting created 29 days ago keeps its notes
- `npm run eval` on all of Aman's test notes meets every §11 pass criterion on 3 runs out of 3.

**Blocked until the test notes arrive.**

## 13. Open items

- [ ] Aman: create the test Supabase project `action-items-test` (Step 5 in `docs/setup-accounts.md`).
- [ ] Aman: supply the test set (§11) in the format in `tests/extraction/README.md`, numbered from `02`. Expected by end of the week of 2026-09-28. **Blocks sign-off, but not the build.**
- [ ] Aman: set up accounts (`docs/setup-accounts.md`), then tell Claude it's done.
- [ ] Aman: set up Google Workspace; switch `ALLOWED_DOMAIN` from the temporary `gmail.com` to the company domain. **Needed before the team uses the app, not before the build starts.** Until then, login works with test users (§10).
- [ ] Aman: provide the 8 team emails (the §2 roster table).
- [x] Nicknames: Tom = Tomás (confirmed 2026-09-26). Any others can be added later on the roster page.
- [x] Whole team is on IST (confirmed 2026-09-26).
- [x] Model: Sonnet 5 from the start (decided 2026-09-26; revisit only if the test set fails).
- [ ] After 2 weeks of real use: review the logged cost per run.
- [ ] v2: Slack digest, Mondays 9:00 IST.
