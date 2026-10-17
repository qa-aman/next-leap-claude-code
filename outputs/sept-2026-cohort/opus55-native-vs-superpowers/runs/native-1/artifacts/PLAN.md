# Action Items Board: Implementation Plan

**Status:** Approved by Aman 2026-09-26 · **Follows:** SPEC.md v1 (source of truth)

This plan covers how each phase in SPEC §12 gets built: what goes where, in what order, and how we check it. If this plan and SPEC.md ever disagree, SPEC.md wins, and Claude stops and asks.

References like "decision Q-n" point to Aman's answers in §9. They have also been written into SPEC.md.

---

## 1. Architecture in one page

```
 Browser (desktop or phone)
   │  Google sign-in (via Supabase) · pages · JSON calls to /api/*
   ▼
 Cloudflare Worker  (Next.js app, deployed with the OpenNext adapter)
   ├─ fetch      → Next.js pages + /api route handlers
   │                 every handler: getActor() → permission check → service → DB
   ├─ queue      → background extraction job (decision Q-1)
   └─ scheduled  → daily cron: 30-day deletion + keeps Supabase awake
   │
   ├──► Supabase Auth      (Google OAuth, session in an httpOnly cookie)
   ├──► Supabase Postgres  (via server-only client with SUPABASE_SERVICE_KEY;
   │                        RLS on, no policies, so the browser can't read anything)
   └──► Claude API         (claude-sonnet-5, streaming, structured output)
```

### Key decisions

| Decision | Choice | Why |
|---|---|---|
| Layering | `route handler → service → db`. Route handlers are thin. Services take `(db, actor, input, now)` and hold all the rules. | Tests call services directly with different actors. Permissions live in one place on the server. |
| Permissions | One pure function `can(actor, action, item)` in `src/lib/permissions.ts`, called by every service that changes data. | Easy to test every row of the §8 table. |
| Atomic writes | Every item change + its history row is written by one Postgres function (RPC) in a single transaction. The RPC also takes the owner the server just checked and refuses if it changed in between. | "Every change is logged" can never half-happen. supabase-js has no transactions, so this is how you get them. |
| Login | Two Supabase clients on the server: an **auth client** (reads/writes the session cookie, only used to identify the user) and a **data client** (service key, no session). Both live only on the server. | Matches §10 with only the env vars listed there. The service key never reaches the browser. |
| Who is the user | `getActor()`: valid Supabase session → email ends with `@ALLOWED_DOMAIN` → an **active** member with that email (case-insensitive). Otherwise → "Not authorized". If the email equals `ADMIN_EMAIL` and no member has it yet, an admin member is created (first-run bootstrap). | §10 exactly. Google's domain hint is not trusted. |
| Dates / IST | `src/lib/time.ts`: `todayIST(now)`, `formatIST()`. All "today" and "overdue" logic takes `now` as a parameter. Due dates stored as Postgres `date` (no time). | Deterministic tests. |
| Name matching | `src/lib/names.ts`: `normalize()` = lowercase + strip accents + collapse whitespace. Used for aliases, speaker labels and series names (series: case + whitespace only, per §4.1). | One implementation, tested once. |
| Extraction | Pure function `extract(input, claudeClient)` in `src/lib/extraction/`. The app, the eval script and the tests all call the same function. Tests pass a fake Claude client. | What the eval measures is exactly what the app runs. |
| Due dates | Claude returns only `date_phrase` + `date_kind` + parameters. `src/lib/extraction/dates.ts` computes the date from the meeting date. | §5.3, CLAUDE.md rule. |
| Claude IDs | The prompt gives Claude short keys (`M1…M9` for members, `E1…` for existing open items). The server maps them back and rejects any key it didn't send. | Fewer copy errors than UUIDs; the "reject unknown ids" rule still applies. |
| Output safety | React renders all text as plain text. `dangerouslySetInnerHTML` is banned (lint rule). The prompt treats notes as data. | §7. |
| Request safety | State-changing API calls must be JSON and have an `Origin` header matching the app URL. Session cookie is `httpOnly`, `Secure`, `SameSite=Lax`. | Blocks cross-site form posts. |
| Styling | Tailwind CSS, simple responsive layout (works in a phone browser). | §3 says no mobile app, but phone browser must work. |
| Tests | Vitest. `npm test -- dates` works because Vitest filters by file name. Unit tests need nothing. Integration tests run against a separate test Supabase project (decision Q-3). | Matches the "How we check it" commands in SPEC §12. |
| Logs | Logs contain ids, counts, tokens and cost only. Never the notes, snippets or item text. | CLAUDE.md: raw notes never copied anywhere, including logs. |

### Configuration

Runtime (Cloudflare secrets, and `.dev.vars` on Aman's Mac for local runs): `ANTHROPIC_API_KEY`, `SUPABASE_URL`, `SUPABASE_SERVICE_KEY`, `ALLOWED_DOMAIN`, `ADMIN_EMAIL`, exactly as in SPEC §10.

Local-only tooling (never deployed, decision Q-10): `SUPABASE_DB_URL` for running migrations, and `.env.test` holding the test project's URL and keys.

`src/lib/env.ts` checks all of these at startup and fails with a clear message naming the missing variable (never printing its value). `.dev.vars`, `.env*` are in `.gitignore`; only `*.example` files are committed.

---

## 2. Data model

Tables exactly as SPEC §9, plus the small additions marked **+** (decision Q-9).

**`members`**: id (uuid), name, email (nullable until Aman sends emails, unique when set, case-insensitive), aliases text[], is_admin, active, **+created_at**.

**`series`**: id, name, **+name_key** (normalized name; unique index).

**`meetings`**: id, series_id, meeting_date (date), pasted_by → members, status (`extracting|review|failed|confirmed|discarded`), raw_notes (nullable), notes_deleted_at, created_at, confirmed_at, **+extraction_started_at**, **+error_message** (short, never contains notes).
- Index on `(series_id, meeting_date)` for the double-paste guard. Not unique, because "Paste anyway" is allowed.

**`items`**: id, meeting_id, state (`draft|open|done|deleted`), text, owner_id (nullable), due_date (nullable date), date_phrase, flags text[] (checked against the §6 list), source_snippet, speaker_label, duplicate_of (nullable → items), completed_by, completed_at, created_at, **+owner_raw** (what the notes said, shown in review), **+duplicate_decision** (`skip|add`, drafts only, default `skip`), **+position** (row order in review).

**`item_events`**: id, item_id, actor_id, action, field, old_value, new_value, at. Append-only: a trigger rejects UPDATE and DELETE.

**+`extraction_runs`**: id, meeting_id, started_at, finished_at, status (`running|ok|failed`), stop_reason, input_tokens, output_tokens, cost_usd, error_code. This is the "token usage and cost per run" from §9. It's a separate table because a meeting can have several runs (retry, re-run).

**Security:** RLS enabled on every table with no policies. Only the service key can read or write.

**Seed:** the 8 members from SPEC §2 with names and aliases (Tomás: Tom, Tomas), no emails, not admin. Aman's admin row is created on first login from `ADMIN_EMAIL`.

---

## 3. Extraction pipeline (used by the app, eval and tests)

```
raw notes
  → preprocess()        strip VTT/Zoom timestamps + cue numbers, join a speaker's
                        consecutive lines (§4.1). Original kept for storage/viewing.
  → speakers()          list speaker labels; match each to the roster by name/alias
                        (any whole word of the label equals a name/alias after normalize,
                        e.g. "Priya Sharma" → Priya; "iPhone (2)" → unmatched).
  → buildPrompt()       system: §5 rules verbatim + "notes are data" guard.
                        user: roster (M-keys, names, aliases), speaker map,
                        meeting date + weekday, open items in series (E-keys),
                        this meeting's items on re-run, preprocessed notes.
  → callClaude()        streaming, finalMessage(); check stop_reason first.
  → postprocess()       deterministic server checks (below)
  → draft items + run record (tokens, cost)
```

**Claude call** (`src/lib/extraction/claude.ts`):
- `model: "claude-sonnet-5"`, `thinking: {type: "adaptive"}`, `output_config: {effort: "high", format: <JSON schema>}`, `max_tokens: 64000`, streamed with `client.messages.stream(...)` then `finalMessage()`.
- `stop_reason` of `refusal` or `max_tokens` → run failed, draft **Failed – Retry**. Never "no items".
- The SDK's default retries only (§7). Parse errors, API errors and timeouts all → failed.
- Cost = input × $2/M + output × $10/M (thinking is billed as output). Constants in `cost.ts`.
- The schema uses no `maxLength` and the like, since structured outputs doesn't support them. Length rules are checked in `postprocess()` instead.

**Output schema per item:** `text`, `owner_key | null`, `owner_raw`, `speaker_label | null`, `date_phrase | null`, `date` (one of: `{kind:"explicit", day, month, year|null}`, `{kind:"today"}`, `{kind:"tomorrow"}`, `{kind:"in_n_days", n}`, `{kind:"in_n_weeks", n}`, `{kind:"weekday", weekday}`, `{kind:"ambiguous"}`, `{kind:"none"}`), `source_snippet`, `flags[]` (enum), `possible_duplicate_of | null` (E-key).

**`postprocess()` rules (all in code):**
1. `owner_key` not in the keys we sent → owner blank + `owner_unclear`.
2. Speaker label from an unmatched speaker and no owner → `unknown_speaker`; the label is kept for the badge.
3. Date: `resolveDueDate(meetingDate, date)` per §5.3. Anything unresolvable, impossible (31/02), earlier than the meeting, or a weekday equal to the meeting's weekday → blank + `date_unclear`. `none` → blank, no flag. For `explicit` with a numeric phrase like "3/10", code also parses the phrase itself (day/month) and if Claude's numbers disagree → blank + `date_unclear`.
4. Snippet check: normalized snippet (whitespace + case) must be a substring of the normalized notes. Otherwise → `source_unverified`.
5. `possible_duplicate_of` not one of the E-keys we sent → dropped. Valid → `duplicate_of` set + `possible_duplicate`.
6. Flags limited to the §6 list (Claude may raise `owner_unclear`, `unknown_speaker`, `date_unclear`, `conditional`, `maybe_not_task`; the server alone raises `source_unverified`, `possible_duplicate`, `needs_reassignment`). An owner that is set removes `owner_unclear`/`unknown_speaker`. A date that is set removes `date_unclear`.
7. Text over 120 or snippet over 300 characters is **not cut**. The review screen marks it and asks the reviewer to shorten it.

---

## 4. File map (whole project)

```
package.json, tsconfig.json, next.config.ts, open-next.config.ts,
wrangler.jsonc (worker, cron, queue), tailwind/postcss config, eslint config,
vitest.config.ts, .gitignore, .dev.vars.example, .env.test.example

worker/index.ts                    custom Worker entry: fetch → OpenNext, queue → extraction,
                                   scheduled → retention

supabase/migrations/
  0001_init.sql                    tables, enums, indexes, RLS on, append-only trigger   (P1)
  0002_extraction.sql              extraction_runs, confirm_meeting(), rerun helpers     (P3)
  0003_items.sql                   apply_item_change(), deactivate_member()              (P4)
  0004_retention.sql               run_retention()                                       (P5)
supabase/seed.sql                  8 roster members + aliases                            (P1)
scripts/migrate.ts                 applies migrations in order, records what's applied   (P1)

src/lib/        env.ts, time.ts, names.ts, flags.ts (flag list + badge text),
                permissions.ts (P4), board-sort.ts (P4)
src/lib/extraction/
                preprocess.ts, speakers.ts, dates.ts, rules.ts (§5 text), prompt.ts,
                schema.ts, claude.ts, cost.ts, postprocess.ts, extract.ts        (P2)
src/server/     db.ts, auth.ts (getActor, requireAdmin), extractor.ts (real/fake)
src/server/services/
                roster.ts (P1), meetings.ts + drafts.ts (P3), items.ts (P4)
src/server/jobs/
                runExtraction.ts (P3), retention.ts (P5)
src/middleware.ts                  send signed-out users to /login

src/app/
  layout.tsx, globals.css
  login/page.tsx, not-authorized/page.tsx
  auth/login/route.ts, auth/callback/route.ts, auth/logout/route.ts
  page.tsx                         the board (empty in P1, full in P4)
  admin/roster/page.tsx            roster page (P1)
  paste/page.tsx                   paste form + drafts list (P3)
  meetings/[id]/page.tsx           progress / failed / review / read-only / view notes (P3)
  api/dev/long-call/route.ts       Phase 1 risk check (decision Q-5)
  api/admin/members/…              list, add, edit, deactivate (P1)
  api/series/route.ts              autocomplete (P3)
  api/meetings/…                   create, drafts, get, retry, rerun, discard, confirm,
                                   draft item add/edit/delete (P3)
  api/items/…                      list, edit, tick, untick, take, assign, dismiss-flag,
                                   delete, events (P4)
src/components/  FlagBadge, OwnerSelect, DateField, Toast, DraftsBanner (shared);
                 ReviewTable, ReviewRow, DuplicateNotice, PasteForm (P3);
                 Board, BoardRow, Filters, HistoryList (P4); RosterTable (P1)

tests/unit/          names, dates, preprocess, speakers, postprocess, rules-sync,
                     eval-grade, permissions, board-sort
tests/integration/   review.test.ts, permissions.test.ts, retention.test.ts
tests/helpers/       testDb.ts (reset + seed test project), actors.ts, fakeClaude.ts
tests/extraction/    README.md (exists), 01-notes.txt + 01-key.md (worked example, decision Q-4),
                     Aman's test notes (P5)
scripts/eval.ts, scripts/eval/parseKey.ts, scripts/eval/grade.ts        (P2)

docs/setup-accounts.md  (exists; add: test Supabase project if Q-3 = yes)
docs/secrets-and-deploy.md  click-by-click: fill in .dev.vars, add Cloudflare secrets,
                            run a migration, deploy                               (P1)
```

---

## 5. Phases

Each phase ends with its check from SPEC §12. Claude runs every command check and pastes the real output. Aman takes the screenshots on the live site (Claude can't sign in with Google), following steps Claude gives him. The next phase starts only after Aman's OK.

### Phase 1: Deployed skeleton, login, roster (days 1–3)

**Aman first** (per `docs/setup-accounts.md`): Steps 1 (Anthropic) and 2 (Cloudflare) are done. Steps 3 (Supabase), 4 (Google) and 5 (test Supabase project) are still to do. Then he follows the new `docs/secrets-and-deploy.md` to put keys in `.dev.vars` and in Cloudflare, typing them in himself, never in chat.

**Build order**
1. Project scaffold: Next.js + TypeScript + Tailwind + OpenNext + Wrangler + Vitest + ESLint. `worker/index.ts` custom entry. `env.ts`.
2. Deploy a "hello" page to `<app>.aman-team.workers.dev`. Confirms the deploy pipeline works before anything else.
3. **Risk check first** (day 1, because it can change the architecture): `/api/dev/long-call` makes a real streaming Claude call that runs for over 120 s. It streams a heartbeat line every ~15 s so the connection stays active, and the last line is `ok`. It costs about $0.10 per run. At the same time, test the background path (decision Q-1).
4. `0001_init.sql` + `seed.sql` + `scripts/migrate.ts`. Run against the live Supabase project.
5. Auth: `auth.ts`, `middleware.ts`, login/callback/logout routes, `/login`, `/not-authorized`. Domain + active-roster check. `ADMIN_EMAIL` bootstrap.
6. `names.ts` + unit tests.
7. Roster service + API + `/admin/roster` page: list; add member (name, email, aliases); edit name/email/aliases; deactivate (with a confirm dialog). Admin-only on the server. In Phase 1, deactivate just sets `active=false`. The `needs_reassignment` part arrives in Phase 4, once items exist.
8. Empty board page ("No items yet") with a nav bar: Board · Paste (disabled until P3) · Roster (admin only) · Sign out.
9. Write `docs/secrets-and-deploy.md`.

**How we check it** (SPEC §12, unchanged)
- A roster account reaches the empty board: Aman's screenshot, private window.
- A non-roster Google account sees "Not authorized": Aman's screenshot with his spare Gmail.
- `time curl <live-url>/api/dev/long-call` ends with `ok` and `time` shows more than 120 s: Claude runs it and pastes the output.
- `curl --max-time 10 "<live-url>/api/dev/long-call?background=1"` disconnects after 10 s, and about 3 minutes later `curl <live-url>/api/dev/long-call/status` prints `ok` (background run, decision Q-1).
- Then the test endpoint's setting is switched off (decision Q-5).
- Also run: `npm test -- names` (supporting unit tests).

### Phase 2: Extraction engine, no screens (days 4–6)

**Build order**
1. `dates.ts` + `tests/unit/dates.test.ts` **first**, test-first. One test per row and bullet of §5.3:
   explicit d/m ("3/10" → 3 Oct), explicit with no year → next occurrence on or after the meeting date (including crossing the year end), "3 Oct" / "October 3" forms, `today`, `tomorrow`, `in_n_days`, `in_n_weeks` (decision Q-8), `weekday` strictly after the meeting date, weekday equal to the meeting's weekday → blank + flag, every `ambiguous` example (kal, parso, next Friday, EOW, end of Q3, ASAP, before the offsite, soon), `none` → blank no flag, impossible date 31/02 → ambiguous, resolved date before the meeting → blank + flag, Claude/phrase disagreement → blank + flag.
2. `preprocess.ts` + tests (VTT header, cue numbers, `00:12:04` prefixes, `-->` lines, speaker joining, Devanagari untouched, word count and the 20,000-word limit).
3. `speakers.ts` + tests ("Priya Sharma" → Priya, "Tomas" → Tomás, "iPhone (2)" / "Conference Room B" → unmatched).
4. `rules.ts` holds the §5 text. `tests/unit/rules-sync.test.ts` reads SPEC.md §5 and fails if the prompt's copy differs, so "verbatim" stays true.
5. `schema.ts`, `prompt.ts`, `claude.ts`, `cost.ts`, `postprocess.ts` (+ tests with hand-made Claude outputs: unknown owner key, bad snippet, bad duplicate key, over-length text), `extract.ts`.
6. Worked example into `tests/extraction/01-notes.txt` + `01-key.md` (decision Q-4).
7. `npm run eval`: `scripts/eval.ts [NN…] [--runs 3]`. For each note: parse the key; use the seed roster; use the key's "Already open" table as open items; run `extract()` N times; grade; print a table plus tokens and cost per run. Admin-only means it runs on Aman's Mac or Claude's session with the API key. It is not a web page.
   **Grading** (`grade.ts`, unit-tested): match key items to extracted items by quote (normalized key quote inside the snippet or the other way round, else ≥60% word overlap), then by owner for split items; one-to-one. Score recall, wrong owners, unassigned-where-key-has-owner (<10%), wrong dates, extras (≤1), non-items present, duplicate flagged. Pass/fail per note, per run.

**How we check it** (SPEC §12, unchanged)
- `npm test -- dates` passes.
- `npm run eval -- 01` reports 5/5 items with correct owners, dates and flags, and neither non-item, on 3 of 3 runs. About $0.20 of API spend.
- If it fails: tune the prompt, then effort (§11). Model changes only with Aman.

### Phase 3: Paste, review, confirm (days 7–8)

**Build order**
1. `0002_extraction.sql`: `extraction_runs`; `confirm_meeting()` RPC (one transaction: skipped duplicates removed; other draft items → `open`; review-only `possible_duplicate` flag dropped; a "created" event per item with meeting and paster; meeting → `confirmed`).
2. `src/server/extractor.ts`: real extractor, and a fake one for tests (returns canned items, or fails on request).
3. `runExtraction` job: marks the run, calls `extract()`, writes draft items + run tokens/cost, sets `review` or `failed`. Every run is logged (ids, tokens, cost only). Runs in the background (decision Q-1). Anything in `extracting` for more than 5 min is shown and stored as `failed`.
4. Services + APIs:
   - **Create paste**: validates name/date/notes and the 20,000-word limit (clear error, no cutting). Finds or creates the series by `name_key`. **Double-paste guard**: an existing non-discarded meeting with the same series + date → `409` with "*Weekly Product Sync, 26 Sep* was already pasted by Priya", unless `force: true` ("Paste anyway"). Saves raw notes, then starts extraction.
   - **Drafts list** (everyone): meetings in `extracting|review|failed`.
   - **Draft actions** (paster or admin only, checked on the server): edit item fields (owner must be an active member), add manual item, delete row, set Skip/Add anyway, dismiss flag, retry, re-run, discard, confirm.
   - **Re-run**: needs raw notes (disabled after the 30-day deletion). Draft → replaces its draft items. Confirmed meeting → new draft on the same meeting, its board items sent as duplicate candidates. Discarding that draft returns the meeting to `confirmed`.
5. Pages:
   - `/paste`: form (meeting name with autocomplete, date defaulting to today IST, notes box with live word count), guard dialog (Open it / Paste anyway), drafts list.
   - `/meetings/[id]`: "Reading notes… this can take up to 2 minutes" (polls every 5 s; you can leave); **Failed – Retry**; review table (§4.3 rows and actions, autosave on each change); read-only for non-pasters; "View notes" (plain text, or "Notes deleted on …").
   - Small "In review: …" banner on the board.
6. `tests/integration/review.test.ts` + test DB helpers.

**How we check it** (SPEC §12, unchanged)
- `npm test -- review` passes, covering: paste → draft → edit → confirm puts items on the board; same series + date → double-paste warning; forced API failure → Failed, Retry works; re-running a confirmed meeting marks existing items as duplicates; a non-paster can't edit the draft (server rejects it).
- Screenshot of the review screen for the worked example (5 rows with badges). Aman pastes `01-notes.txt` on the live site with meeting date 25/09/2026 and takes the screenshot. One real run, about $0.07.

### Phase 4: Board, permissions, history (days 9–10)

**Build order**
1. `permissions.ts` + unit tests: the §8 table as code.
2. `0003_items.sql`: `apply_item_change()` (update + event rows in one transaction; refuses if owner/state changed since the check) and `deactivate_member()` (sets `active=false`; adds `needs_reassignment` to their open items with an event each).
3. `items.ts` service + APIs: tick, untick (also used by Undo), edit text/due date, dismiss flag, reassign, take for yourself, assign unassigned, soft delete (admin; hidden, never erased; no restore screen in v1, decision Q-9), history. Flag clearing follows §6 (decision Q-6). Owners must be active roster members. Every change → `item_events`.
4. `board-sort.ts` + tests: overdue → today → due date ascending → blank last, using `todayIST(now)`.
5. Board page: filters (Owner incl. Unassigned, Series, Meeting), quick filters (My items, Needs attention), row layout, red date + red left border for overdue, amber for today, expand row (snippet, flags, "created from *meeting* by *paster*", history), Show completed toggle, "✓ Dana, 27 Sep 14:10", Undo toast. Refetch on load and on window focus. Controls a user can't use are hidden, and the server rejects them anyway.
6. Roster page: deactivate now calls `deactivate_member()`.
7. `tests/integration/permissions.test.ts`.

**How we check it** (SPEC §12, unchanged)
- `npm test -- permissions` passes: for every row of §8, the allowed user succeeds (change saved + history row written) and a not-allowed user is rejected by the server (nothing saved, no history row). Plus: deactivating a member flags their open items with `needs_reassignment`.
- Screenshot of the board with an overdue item (red border), an item due today (amber) and a flagged item with its badge. Claude gives Aman a short sample note and a past meeting date to paste so all three show up.

### Phase 5: Retention, cost, sign-off (days 11–14)

**Build order**
1. `0004_retention.sql` `run_retention(now)`: for meetings created more than 30 days ago, set `raw_notes = null` and `notes_deleted_at`. Unconfirmed drafts (`extracting|review|failed`) → `discarded` and their draft items deleted. A re-run draft on a confirmed meeting just has its draft items removed and the meeting stays confirmed.
2. `retention.ts` job + `scheduled` handler in `worker/index.ts`. Cron: daily at 02:00 IST (`30 20 * * *` UTC). The same query keeps Supabase awake.
3. Cost logging: already written per run since Phase 3. Check it's complete (retries and re-runs included). Add click-steps for Aman to see cost per run and per month in the Supabase table view. No new screen.
4. `tests/integration/retention.test.ts`.
5. When Aman's test notes arrive: check each answer key against the §5.3 date rules first and raise any disagreement with Aman. Then `npm run eval` on all notes, 3 runs each. Tune the prompt, then effort. Never relax the criteria (§11). About $0.50–$1.50 per full eval run.
6. Hand checks from §11 (Claude writes a checklist, Aman ticks it): every permission rule rejected on the server, 30-day job by moving a meeting's `created_at` back 31 days, retry after a forced failure, double-paste warning, deactivation → `needs_reassignment`, non-roster account refused.
7. Remove `/api/dev/long-call` (decision Q-5). Team walkthrough.

**How we check it** (SPEC §12, unchanged)
- `npm test -- retention` passes (31 days → notes gone + draft discarded; 29 days → notes kept).
- `npm run eval` on all of Aman's notes meets every §11 criterion on 3 of 3 runs.
- **Blocked until the test notes arrive.** The build can finish before that.

---

## 6. Testing setup

- **Unit tests** (no network): dates, preprocess, speakers, names, postprocess, rules-sync, eval grading, permissions, board sort.
- **Integration tests** (review, permissions, retention): run against a separate test Supabase project (decision Q-3). Each test resets the tables and loads the seed. The Claude call is replaced by the fake extractor, so tests cost nothing. The clock is passed in as `now`.
- **Eval** (`npm run eval`): the only test that calls the real Claude API. Prints tokens and cost for every run.

## 7. Deploying

`npm run deploy` = OpenNext build + `wrangler deploy`. Claude runs it after Aman has logged Wrangler in once (click-steps in `docs/secrets-and-deploy.md`). Migrations run with `npm run db:migrate` before a deploy that needs them. No git remote or CI is planned.

## 8. Budget guardrails

- Model fixed at `claude-sonnet-5`; no change without Aman.
- Anthropic Console limit at $15/month (done).
- Planned API spend while building: Phase 1 ~ $0.30, Phase 2 ~ $1–3 (prompt tuning), Phase 3–4 screenshots ~ $0.20, Phase 5 ~ $3–8 (tuning on the real set). Every eval run prints its cost.

---

## 9. Decisions (Aman, 2026-09-26)

All ten were approved as proposed. Each is also written into SPEC.md or the doc named.

| # | Decision | Where recorded |
|---|---|---|
| Q-1 | Extraction runs as a background job (Cloudflare Queues), so it continues after the user leaves the page. The Phase 1 check gains a fourth line: a background call still finishes after the caller disconnects. Fallback: Supabase Edge Function (§10). | SPEC §10, §12 Phase 1 |
| Q-2 | New flag `maybe_not_task`, badge **"Is this a task?"**, for borderline items. Cleared when the reviewer or owner dismisses it. | SPEC §5.1, §6; test-set README |
| Q-3 | Integration tests use a separate free Supabase project, `action-items-test`. | SPEC §10, §13; `docs/setup-accounts.md` Step 5 |
| Q-4 | The worked example is `01`; Aman's test notes start at `02`. | SPEC §11, §13; test-set README |
| Q-5 | `/api/dev/long-call` works only while a setting is on. It's switched off after the Phase 1 check, and the code is deleted in Phase 5. | SPEC §10 |
| Q-6 | `needs_reassignment` is cleared by **any** allowed change of owner, including a member taking the item for themselves. | SPEC §6 |
| Q-7 | History starts when an item reaches the board. Draft edits during review are not logged. | SPEC §8 |
| Q-8 | `in_n_weeks` = meeting date + N × 7 days. | SPEC §5.3 |
| Q-9 | Supporting table and columns (`extraction_runs`, etc.). **No** Show deleted / Restore screen (revised 2026-09-26, leaner option): deleted items are only hidden, and Claude restores one on request in the database, with a history entry. | SPEC §8, §9 |
| Q-10 | Local-only `SUPABASE_DB_URL` on Aman's Mac for migrations. Never deployed or committed. | SPEC §10 |
