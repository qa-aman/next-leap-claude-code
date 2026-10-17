

### USER

I want to build a web app where my team pastes meeting notes and gets a list of action items with owner and due date. The team sees all open items on one board and ticks them off. It works when every action item from a meeting shows up with the right owner, and nobody has to retype them. Use your superpowers skills to brainstorm this with me and then write the implementation plan. Do not start implementing.


### BUILDER

I'm using the brainstorming skill to shape this with you before we write a plan.

**Classification: architectural.** The working directory is empty and isn't a git repo, so this is a new project. That means we'll go through questions, then approaches, then a design reviewed section by section, then a written spec for you to approve. Only after that will I write the implementation plan. No code gets written.

**My understanding so far:**

*What you said:*
- Your team pastes meeting notes into a web app.
- The app pulls out action items, each with an owner and a due date.
- One shared board shows all open items, and anyone can tick them off.
- It counts as working when every action item from a meeting appears with the right owner, and nobody has to retype anything.

*What I'm assuming (please correct):*
- It's for one small team, not many separate teams or organisations.
- You'll review the extracted items before they go on the board, so mistakes can be fixed with a quick edit rather than retyped.
- Some action items won't have a due date in the notes, so "no date" is allowed.
- Extraction probably needs a language model (for example, Claude), because plain text rules are unlikely to catch every item in free-form notes.

**First question:** the hardest part is getting the right owner every time, so it depends on what your notes look like. Which is closest?

- **A.** Structured. Items are already marked, like `ACTION: @Priya – send deck by Fri`.
- **B.** Loose but consistent. Bullet points written by a person, like "Priya to send the deck by Friday."
- **C.** Raw transcripts or AI meeting summaries (Granola, Otter, Zoom, etc.), where owners are implied ("I'll take that").
- **D.** A mix of the above.

It would also help to know how owners are named in the notes: first names, @handles, initials? And is there a fixed team roster we can match them against?

Separately, a few of your claude.ai connectors need authorising before they can be used: Apify, Atlassian (both), Canva, Higgsfield, Notion and S&P Global. You can do that in your claude.ai connector settings. None of them are needed for this project unless you want Notion or Jira integration later.


### SIM

It's D, a mix — mostly Google Docs bullet notes and Zoom/Granola transcripts. Owners are usually first names or nicknames (e.g. "Tom" for Tomás). Yes, fixed roster of 8: Priya, Marcus, Sarah, Tomás, Aisha, Dana, Ravi, Lena. If a name isn't on that list, flag it, don't guess.

One correction: items should NOT need review before hitting the board — accuracy needs to be high directly, with a "needs review" flag on uncertain ones rather than requiring manual approval of everything.

No need to authorize those other connectors, not relevant here.


### USER

It's D, a mix — mostly Google Docs bullet notes and Zoom/Granola transcripts. Owners are usually first names or nicknames (e.g. "Tom" for Tomás). Yes, fixed roster of 8: Priya, Marcus, Sarah, Tomás, Aisha, Dana, Ravi, Lena. If a name isn't on that list, flag it, don't guess.

One correction: items should NOT need review before hitting the board — accuracy needs to be high directly, with a "needs review" flag on uncertain ones rather than requiring manual approval of everything.

No need to authorize those other connectors, not relevant here.


### BUILDER

Got it. Here's the updated understanding:

- **Items go straight onto the board, with no approval step.** Anything uncertain gets a visible **"needs review"** flag. That includes an unclear owner, an ambiguous task, or a date that can't be worked out.
- **Owners must come from the roster of 8:** Priya, Marcus, Sarah, Tomás, Aisha, Dana, Ravi, Lena. Nicknames like "Tom" should match through an alias list you control. Any name not on the roster is flagged and never guessed.
- **Inputs are mixed:** Google Docs bullet notes and Zoom/Granola transcripts, pasted as text.
- *New assumption:* relative dates like "by Friday" need a reference date, so the paste form will ask for the meeting date (defaulting to today).

**Next question: how will the team reach and sign in to the app?** This choice shapes most of the architecture.

- **A. Hosted, with Google sign-in** limited to your company domain. You already use Google Docs, so there are no new passwords. Something like Vercel or Fly with a small Postgres database.
- **B. Hosted, with a shared team password or link.** Simplest to set up, but the app can't tell who ticked what off.
- **C. Internal only**, running on one machine or your company network with no login.
- **D. Your own setup.** Tell me your preferred hosting or stack, or company constraints (for example, "we're on AWS").

I recommend **A**. It knows who ticked each item off, and it fits the Google tools your team already uses.


### SIM

A. Google sign-in, restricted to our company domain — that's a must-have, notes are confidential.


### USER

A. Google sign-in, restricted to our company domain — that's a must-have, notes are confidential.


### BUILDER

Google sign-in limited to your company domain is now a hard requirement.

Confidentiality raises a question I need answered before I can propose approaches. Given your mix of notes and transcripts, getting every item with the right owner almost certainly needs an LLM. That means the note text would be sent to a model provider's API.

**Is it acceptable to send meeting notes to an external LLM API?**

- **A. Yes, the Anthropic (Claude) API is fine.** API data isn't used for training by default. This gives the best extraction accuracy and is what I'd recommend.
- **B. Yes, but only through a provider your company already approves.** For example, Claude through AWS Bedrock or Google Vertex, under your existing cloud agreement. Tell me which one.
- **C. No, notes must not leave our infrastructure.** We'd need a self-hosted open model or rules only. Accuracy would be noticeably lower, especially on transcripts, and more items would be flagged "needs review."
- **D. Not sure.** I'll design around A, keep the model provider swappable behind one interface, and note the decision as something to confirm with whoever handles security or compliance.


### SIM

A. Anthropic API is fine, given the 30-day deletion and it not being used for training.


### USER

A. Anthropic API is fine, given the 30-day deletion and it not being used for training.


### BUILDER

Anthropic API it is. One caveat: retention and training terms depend on your organisation's commercial agreement, so I'll list "check current Anthropic data-retention terms with security" as a pre-launch item in the spec instead of treating the 30-day figure as settled.

There are three realistic ways to build the extraction. This is where "every item, right owner" is won or lost.

### Approach 1 (recommended): one Claude call, with the rules enforced in code

- Claude gets the notes, the meeting date and the roster with aliases. It returns structured JSON: task, owner as written, due date, and a supporting quote from the notes.
- Our own code then checks every item, rather than trusting the model:
  - **Owner:** the name must match a roster member or an alias. Otherwise it's flagged, never guessed.
  - **Due date:** the date must be valid and not before the meeting. Items with no date are allowed.
  - **Quote:** the quote must actually appear in the pasted text, which catches invented items.
- Any failed check, or low confidence from the model, sets "needs review."
- **Pros:** simple, fast (a few seconds), low cost, and the no-guessing rule is guaranteed by code rather than by the prompt.
- **Con:** it relies on one pass not missing any items.

### Approach 2: extract, then a second "what did we miss?" pass

- Same as Approach 1, plus a second call that re-reads the notes against the extracted list to find missed items.
- **Pros:** fewer missed items, especially in long transcripts.
- **Cons:** about twice the cost and wait, and more moving parts.

### Approach 3: text rules first, Claude as a fallback

- Pattern matching ("X to do Y", "ACTION:") runs first, and Claude is only used for the rest.
- **Pro:** cheapest.
- **Con:** brittle on transcripts, and it produces two sources of truth. Not recommended.

**My recommendation is Approach 1, measured against a test set built from 10–20 of your real past notes.** Each note gets a hand-written list of the correct action items. That test set is how we'll know "every item, right owner" is true rather than hoped for. If it shows missed items, we add Approach 2's second pass then, not before.

**Proposed stack:** TypeScript with Next.js, Google sign-in via Auth.js (restricted to your company domain), Postgres, hosted on Vercel, and Claude Opus 5 for extraction.

**Question:** are you happy with Approach 1 plus the test set, and with this stack? Or do you have a preferred language, host or model?

If you agree, next I'll present the design section by section (data model, extraction pipeline, board UI, error handling, testing) for you to approve before I write the spec.


### SIM

Yes, happy with Approach 1 plus the test set, and with that stack.


### USER

Yes, happy with Approach 1 plus the test set, and with that stack.


### BUILDER

That's settled. Here is the design, one section at a time. Please approve each section or correct it before I move on.

## Section 1 of 5: Architecture and data model

**Units.** Each has one job and can be tested on its own.

| Unit | Job | Depends on |
|---|---|---|
| `auth` | Google sign-in. The server rejects anyone whose verified email isn't on your company domain. | Auth.js |
| `roster` | The 8 members and their aliases (Tom → Tomás). `resolveOwner("Tom")` returns the member, or "unknown". | nothing |
| `extract` | Sends the notes, meeting date and roster to Claude. Returns raw item candidates as structured JSON. | Anthropic SDK |
| `validate` | Plain code with no API calls. Checks owner, date and quote for each candidate, and attaches "needs review" reasons. | `roster` |
| `db` | Postgres access for meetings and action items. | Postgres |
| UI pages | **Paste** page and **Board** page. | all of the above |

**Flow:** paste the notes and meeting date → `extract` → `validate` → items are saved and appear on the board straight away, with flags where needed. No approval step.

**Data model:**

- **Meeting:** `id`, `title`, `meeting_date`, `raw_notes`, `created_by`, `created_at`
- **ActionItem:**
  - What it is: `id`, `meeting_id`, `task`
  - Owner: `owner` (a roster member, or empty if unresolved) and `owner_as_written`
  - Due date: `due_date` (can be empty) and `due_as_written`
  - Evidence: `source_quote`
  - Flag: `needs_review` and `review_reasons` (for example "unknown owner 'Jamal'" or "ambiguous date")
  - Status: `status` (open or done), `done_by`, `done_at`

Keeping `owner_as_written`, `due_as_written` and `source_quote` means anyone can see *why* an item was assigned the way it was, and fix it in one click rather than retyping it.

**One decision I've made that you may want to override:** in version 1 the roster and aliases live in a config file in the code, so adding a nickname means a small code change and redeploy. The alternative is a small in-app "Roster" page where anyone can add aliases. With 8 fixed people I'd start with the config file.

Does this section look right, and is the config file OK for the roster?


### SIM

Section looks right. Config file for the roster is fine with 8 people.


### USER

Section looks right. Config file for the roster is fine with 8 people.


### BUILDER

## Section 2 of 5: The extraction pipeline

**The Claude call (`extract`).**
- **Setup:** Claude Opus 5 with adaptive thinking, and structured output constrained to a fixed JSON schema so the reply is always parseable. The model's context window easily holds a long transcript, so notes are never split into chunks.
- **What the instructions say:**
  - Extract *every* commitment to do something, including ones implied in transcripts ("I'll take that" → the speaker).
  - Copy the owner's name exactly as written. Never substitute a roster name.
  - Still extract items owned by people outside the roster, so they can be flagged rather than silently dropped.
  - For shared tasks ("Priya and Marcus to review the contract"), emit one item per owner, so each person ticks off their own.
  - Work out relative dates ("next Friday", "end of month") from the meeting date, and also return the original phrase.
  - Mark an item "unsure" with a short reason when it's ambiguous.
- **Each item returns:** `task`, `owner_as_written`, `due_as_written`, `due_date`, `source_quote`, `confidence`, `reason`.

**The checks in code (`validate`).** Any failure sets "needs review" and records the reason.

1. **Owner:** matched against the roster and aliases, ignoring case and accents ("tomas" = Tomás). No match → owner left empty, with the reason `unknown owner "Jamal"`. No owner at all → `no owner`.
2. **Due date:** if a date phrase exists but no valid date came back → `couldn't resolve "after the offsite"`. A date before the meeting → `due date before meeting`. No date mentioned → empty, and not flagged.
3. **Quote:** `source_quote` must appear in the pasted notes (ignoring whitespace differences). If not → `not found in notes`. This catches invented items.
4. **Model unsure** → the model's own reason is shown.

**A risk with transcripts:** some Granola and Zoom exports label speakers "Me" / "Them" or "Speaker 1" instead of names. "I'll send it" then has no resolvable owner, so it gets flagged rather than guessed. That's correct behaviour, but it could produce a lot of flags. Do your pasted transcripts usually show real speaker names? If not, we could add an optional "who is 'Me'?" dropdown on the paste form.

Does this section look right? And what's your answer on the speaker labels?


### SIM

Section looks right, matches what I want - especially the "flag don't guess" behavior.

On speaker labels: honestly not sure, some of our Zoom exports probably do show real names but Granola ones might show "Me"/"Them" sometimes. Let's add the optional "who is 'Me'?" dropdown just in case - seems low effort and avoids annoying flags.


### USER

Section looks right, matches what I want - especially the "flag don't guess" behavior.

On speaker labels: honestly not sure, some of our Zoom exports probably do show real names but Granola ones might show "Me"/"Them" sometimes. Let's add the optional "who is 'Me'?" dropdown just in case - seems low effort and avoids annoying flags.


### BUILDER

A "Me" dropdown is added, with one refinement: it defaults to whoever is pasting. The roster config will hold each member's work email, so if Priya pastes her Granola notes, "Me" is already set to Priya and she doesn't have to touch it. "Them" and "Speaker 2"-style labels are still flagged, never guessed.

## Section 3 of 5: The pages

**Paste page**

- **Fields:**
  - meeting title
  - meeting date (defaults to today)
  - **"Who is 'Me'?"** (defaults to you, and can be changed or set to "nobody")
  - a large notes box
- **Extract button:** shows progress while it works (roughly 5–20 seconds for long transcripts).
- **Result:** "7 action items added to the board, 2 need review," then it takes you to that meeting's items.

**Board (home page)**

- **Scope:** all open items from all meetings, grouped by owner.
- **Needs review group:** shown first, containing flagged items plus items with no owner, so problems are hard to miss.
- **Each row shows:**
  - a checkbox
  - the task
  - the owner
  - the due date (overdue dates highlighted, items with no date sorted last)
  - a link to the meeting
  - a flag badge listing the reasons
- **Source quote:** clicking an item shows the quote from the notes, so anyone can check the extraction.
- **Filters:** by owner, and "needs review only."
- **Ticking off:** a checked item disappears from the board and records who ticked it and when. An "Undo" link appears briefly, and a "Show done" option shows completed items.

**Fixing an item (one click, no retyping)**

- **Owner:** chosen from a dropdown that only lists the 8 roster members, so a bad owner can't be typed back in.
- **Other fields:** date picker; the task text is editable inline.
- **Clearing flags:** fixing the flagged field clears that reason. A "Looks right" button clears the flag without changes.
- **Delete:** for anything that isn't really an action item.

**Meeting page:** the original notes with that meeting's items, handy for spotting something the extraction missed. There's also an "Add item" button for the rare miss.

**Updates:** the board refreshes when you open it or switch back to its tab. Live updates between teammates are left out as unnecessary for 8 people.

Does this section look right?


### SIM

Mostly right. A few fixes:

- "Show done" doesn't need to exist as a v1 nice-to-have if it adds complexity — actually keep it, that's fine.
- One correction: "same item said in two meetings shouldn't show up twice" is a nice-to-have, not required — don't hold up v1 for it, but if it's easy to design for now, fine.
- Delete on an item — should that be undoable too, or just gone? No preference, recommend what fits.

Otherwise this looks good, approved.


### USER

Mostly right. A few fixes:

- "Show done" doesn't need to exist as a v1 nice-to-have if it adds complexity — actually keep it, that's fine.
- One correction: "same item said in two meetings shouldn't show up twice" is a nice-to-have, not required — don't hold up v1 for it, but if it's easy to design for now, fine.
- Delete on an item — should that be undoable too, or just gone? No preference, recommend what fits.

Otherwise this looks good, approved.


### BUILDER

Two decisions based on your notes:

- **Delete is undoable.** It uses the same "Undo" link as ticking off. Under the hood a deleted item is hidden rather than erased, so it's a status like "done" and costs almost nothing extra. I recommend this: a mis-click shouldn't lose an action item.
- **Duplicates across meetings (nice-to-have) are left out of v1, but the design keeps room for them.** A later version could compare new items with open ones and add a `possible duplicate of "…"` flag reason. That slots straight into the existing flag system, with no redesign. v1 does include one cheap guard: pasting the *exact same notes* twice warns "these notes were already added on 24 Sep" and offers to continue or cancel.

Section 3 is marked as approved with those changes.

## Section 4 of 5: Error handling and safety

**Extraction failures**
- Temporary API errors (rate limits, outages, network) are retried automatically. If it still fails, you see: "Couldn't extract right now, try again." **Your pasted notes stay in the box**, and nothing half-finished is saved. The meeting and its items are saved together or not at all.
- **Claude declines the request:** it automatically falls back to another Claude model. If that also fails, you see a clear error rather than an empty result.
- **Reply cut off because it hit the output limit:** treated as a failure, never saved as a partial list, because that would silently drop items.
- **Zero items found:** the meeting is still saved, with the message "No action items found — add one manually if we missed something."

**Input limits:** empty notes are blocked. Extremely large pastes (far bigger than any real meeting) are rejected with a clear message rather than trimmed, so nothing is dropped without you knowing.

**Access and confidentiality**
- Every page and every server action checks the session, not just the login screen.
- Access requires a verified Google email on your domain. Anyone else gets an "access denied" page.
- **Logs never contain note text or item text.** They only record IDs, timings, errors and token counts.
- Secrets (the Anthropic API key, OAuth credentials, database URL) live only in the host's environment settings, never in the code.
- **Pre-launch checklist item:** confirm Anthropic's data-retention terms with whoever handles security.

**Notes that contain instructions:** if someone pastes text that looks like instructions to the model, it can only affect the extracted list. The model has no tools or data access, and every item goes through the same code checks.

**Two people editing at once:** the last change wins. Ticking an item that's already done is harmless.

Does this section look right?


### SIM

Looks right, approved. Move on to section 5.


### USER

Looks right, approved. Move on to section 5.


### BUILDER

## Section 5 of 5: Testing, and how we'll know it works

**Automated tests (every change, no real Claude calls)**
- **`roster` and `validate`**, the most heavily tested units:
  - Every alias and accent variant maps to the right member.
  - Unknown names, "Them" and "Speaker 2" are flagged.
  - "Me" resolves only when it's been set on the paste form.
  - Date rules: can't be resolved, before the meeting, not mentioned.
  - The quote check handles whitespace differences and catches invented quotes.
- **`extract`** is tested against a fake Claude client. It checks that the reply is read correctly, and that cut-off or declined replies become errors rather than partial lists.
- **Database and server actions:** meeting and items saved together or not at all, tick/undo, delete/undo, the duplicate-paste warning, and signed-out or wrong-domain requests being rejected.
- **One end-to-end browser test** with extraction faked: sign in → paste → items on the board → fix a flagged item → tick → undo.

**The accuracy test set (real Claude, run on demand, not on every change)**
- **Contents:** 10–20 real past meetings, mixed across Google Docs bullets, Zoom transcripts and Granola transcripts, including at least a couple with "Me"/"Them" labels.
  - For each one, **your team writes down the correct list** of task, owner and due date. This is the one piece of work I need from you.
- **Storage:** the notes are confidential, so they live in a git-ignored folder and are never committed.
- **The script:** runs the real pipeline over each meeting and compares the results with your list. Owner and date are compared exactly in code. Claude judges only whether two task descriptions mean the same thing.
- **The report shows:**
  - missed items
  - wrong owners
  - wrong dates
  - extra items that shouldn't be there
  - how many items were flagged
- **Cost:** a few dollars per run at most.

**Proposed launch bar, based on your success criterion:**
1. **No missed items.** Every expected item appears, flagged or not. If any are missed after prompt tweaks, we add Approach 2's second pass.
2. **No silently wrong owners.** An item with the wrong owner and *no* flag is a hard fail. Wrong-but-flagged is acceptable, because the design promises "flag, don't guess."
3. **Flags stay useful:** at most about 15% of items flagged, so the review group doesn't become noise.

**Two things to confirm:**
1. Are these three launch bars right, particularly the ~15% flag limit?
2. Can your team supply the 10–20 meetings and their correct item lists? The plan will start with that, since it's the yardstick for everything else.

Once you confirm, I'll write the full spec to `docs/superpowers/specs/2026-09-26-meeting-action-items-design.md`. I'll also run `git init`, since the folder isn't a repository yet, and commit it for you to review. The implementation plan comes after you approve the spec.


### SIM

1. Yes, those three bars are right, 15% flag limit sounds reasonable.
2. Yes, team can supply that. Go ahead and write the spec.


### USER

1. Yes, those three bars are right, 15% flag limit sounds reasonable.
2. Yes, team can supply that. Go ahead and write the spec.


### BUILDER

I've written the spec to `docs/superpowers/specs/2026-09-26-meeting-action-items-design.md` and committed it. The folder wasn't a git repository, so I set one up first.

It covers everything we agreed across the five sections. When I reread it, two things needed tightening, and I've already changed both:

- **"Me" is worked out by the app, not by Claude.** Claude only copies the speaker label ("Me", "Them", "Speaker 2") exactly as written, and the app then applies your "Who is 'Me'?" choice. Before, the prompt told Claude who "Me" was while also telling it never to substitute a roster name, which contradicted itself.
- **Owner names must match in full.** There's no guessing from the first name alone, so an outsider called "Priya Kumar" is flagged instead of quietly assigned to your Priya. The roster config lists each person's full name among their aliases.

**Please review the spec.** Tell me if you want any changes, or approve it and I'll write the implementation plan next. As you asked, no application code has been written, and none will be until you've reviewed the plan too.


### SIM

Approved, sounds good. Go ahead and write the implementation plan.


### USER

Approved, sounds good. Go ahead and write the implementation plan.


### BUILDER

The implementation plan is written and committed to `docs/superpowers/plans/2026-09-26-meeting-action-items.md`. No application code has been written.

**What it covers:** 11 tasks, each test-first, with the actual code and exact commands in every step:

1. Project setup and roster (alias and accent matching)
2. Validation checks (owner, date, quote, model confidence)
3. The Claude call (structured JSON output; declined or cut-off replies become errors)
4. Database and queries
5. The paste pipeline (limits, duplicate warning, save everything or nothing)
6. Google sign-in restricted to your domain
7. Server actions (every one checks sign-in first)
8. The board (grouping, filters, editing, tick, delete, undo)
9. Paste page (with the "Who is 'Me'?" dropdown) and meeting page
10. End-to-end browser test and deployment guide, including the pre-launch checklist
11. Accuracy test harness, scored against your three launch bars

**Choices worth checking:**
- **Flag reasons are stored with the field they belong to,** so fixing the owner clears only owner flags. The spec said a plain list of text, which couldn't do that. The messages are unchanged.
- **Local development and tests need no Postgres install.** They use an in-process version of Postgres; production uses real Postgres.
- **I added protection for things the spec didn't mention:**
  - A pasted name with decoration like "@Priya" or "Tom:" should still match the roster.
  - Curly quotes and odd spacing in a quote shouldn't trigger a "not found in notes" flag.
  - A due date equal to the meeting date shouldn't be flagged.
  - An item whose owner was later removed from the roster moves to Needs review instead of disappearing.
  - Note text never reaches the logs.
- **Large pastes:** the plan raises Next.js's default 1 MB request limit, so a large paste gets the clear "too long" message rather than an unexplained failure.

**What I need from you before work starts:**
- **Before Task 1:** the company email domain, plus each of the 8 people's work email, full name and any nicknames. The plan won't invent emails. It stops and asks if they're missing.
- **Before Task 11 and deployment:** an Anthropic API key, a Google OAuth client and a Postgres database URL.
- **For the accuracy test:** your team's 10–20 labelled meetings.

**Please review the plan. Which way should it be carried out?**
- **Subagent-driven:** a fresh agent builds each task, and a separate reviewer checks it before the next one starts. There's a full review at the end. Most thorough, and costs more.
- **Native:** I build every task myself in one session, then one reviewer checks everything at the end. Cheaper and faster, but no independent review until the end.

I recommend **subagent-driven**. There are 11 tasks, and later ones depend on names and types defined in earlier ones. Mistakes in the owner checks or sign-in would lead straight to wrong owners or leaked confidential notes, so reviewing each task before the next one is worth the extra cost.


### SIM

Go with subagent-driven, makes sense given the risk areas.

I'll get you the emails, roster names/nicknames, and API keys before those tasks start. Don't have the 10-20 labelled meetings ready yet - can we come back to that closer to Task 11?


### USER

Go with subagent-driven, makes sense given the risk areas.

I'll get you the emails, roster names/nicknames, and API keys before those tasks start. Don't have the 10-20 labelled meetings ready yet - can we come back to that closer to Task 11?


### BUILDER

Subagent-driven is now recorded in the plan, and the labelled meetings are pushed back to Task 11.

**About the labelled meetings:** you don't need them to build the accuracy test in Task 11. It's built and checked against the made-up example meeting. Your real meetings are needed only to *run* the test before launch, to show the three launch bars are met. When we reach Task 11 I'll ask for them.

**What's recorded:**
- The plan's prerequisites now show the chosen approach and the postponed meetings. That change is committed.
- I saved a memory note of where things stand and which inputs are still to come, so a future session picks up in the right place.

**Nothing has been built yet, as you asked.** When you're ready to start, send the company email domain and the 8 people's work emails, full names and nicknames, and tell me to go. I'll then run the plan with a fresh agent per task and a reviewer checking each task before the next begins. The API key, Google OAuth client and database URL aren't needed until Task 11 and deployment.


### SIM

Company domain is fine, work emails follow firstname@ that domain. Names: Priya, Marcus, Sarah, Tomás (goes by Tom), Aisha, Dana, Ravi, Lena — no other nicknames. Go ahead.


### USER

Company domain is fine, work emails follow firstname@ that domain. Names: Priya, Marcus, Sarah, Tomás (goes by Tom), Aisha, Dana, Ravi, Lena — no other nicknames. Go ahead.


### BUILDER

I can't start building in this session. This session is set up for planning only, with no application code, which also matches your original request not to start implementing. To begin, open a new Claude Code session in this folder and say "go ahead with the plan". The saved memory note and the committed plan will pick up from here, using subagent-driven execution.

I've saved the roster details you gave me: emails follow firstname@ your domain, and Tom is the only nickname. The config still needs three things, so it would help to have them for that session:

1. **What is the domain itself?** I only know emails follow firstname@ your domain, not the domain name, and I won't guess it. It's needed for the roster emails and for the sign-in restriction.
2. **Is Tomás's email `tomas@…`, without the accent?** Accented characters in email addresses are rare and often not supported, so I'd assume `tomas@`. Please confirm.
3. **Surnames, if you're happy to share them.** Zoom transcripts often label speakers by full display name, like "Priya Shah". Because owners must match in full, with no first-name-only guessing, "Priya Shah" only matches Priya if her full name is in the roster. Without surnames, each such item still lands on the board but gets flagged `unknown owner "Priya Shah"` and needs a one-click fix. You can skip this for now and add surnames later if the flags get annoying.


### SIM

Domain is the company's actual domain — no preference on what convention, just use whatever you already assumed unless you need me to state it explicitly: it's **acme.com** (example, use that as placeholder in docs, I'll swap the real one in before launch).

Yes, tomas@ without the accent, that's correct.

Skip surnames for now, we'll add if the flags get annoying.


### USER

Domain is the company's actual domain — no preference on what convention, just use whatever you already assumed unless you need me to state it explicitly: it's **acme.com** (example, use that as placeholder in docs, I'll swap the real one in before launch).

Yes, tomas@ without the accent, that's correct.

Skip surnames for now, we'll add if the flags get annoying.


### BUILDER

I've put the roster into the plan and committed it, so Task 1 no longer needs anything from you.

- **Emails:** `firstname@acme.com` for everyone, with Tomás at `tomas@acme.com` (no accent).
- **Domain:** `acme.com` is set in a single constant (`TEAM_EMAIL_DOMAIN`), so swapping in the real one is a one-line change. The sign-in setting `ALLOWED_EMAIL_DOMAIN` also defaults to `acme.com`. The pre-launch checklist has a new first item reminding you to change both, since sign-in fails if they don't match your real domain.
- **Nicknames:** Tom → Tomás is the only one.
- **Surnames:** left out. The plan notes that full-name speaker labels from Zoom, like "Priya Shah", will be flagged for review until surnames are added.

The saved memory note is updated too: the roster is done, and the API key, Google OAuth client, database URL and labelled meetings are still due before Task 11.

**Next step:** this session is planning-only, so the build has to happen in a new Claude Code session in this folder. Just say "go ahead with the plan". It will pick up the committed plan and memory note, and run the 11 tasks one agent at a time, with a review after each. It will ask for the API key, Google OAuth client, database URL and labelled meetings when it reaches Task 11.


### SIM

Go ahead with the plan.


### USER

Go ahead with the plan.


### BUILDER

I can't start the build here. This session runs under the same restriction as before: no application code may be written. Following the plan would mean scaffolding the app and writing code in Task 1 straight away, so I'm stopping before starting.

I was wrong earlier to say a new session would lift this. The restriction comes from how Claude Code is being launched for this folder, not from the conversation, so it came back when the session restarted. It looks like a non-interactive setup with its own instructions, and it isn't something I can change from inside the session.

To go ahead, launch Claude Code in this folder in a normal interactive session, without the planning-only instruction, and say "go ahead with the plan". Everything it needs is committed or saved:

- **Plan:** `docs/superpowers/plans/2026-09-26-meeting-action-items.md`, with the roster filled in and subagent-driven execution recorded.
- **Spec:** `docs/superpowers/specs/2026-09-26-meeting-action-items-design.md`
- **Memory note:** records the pending items (API key, Google OAuth client, database URL, labelled meetings), which are needed at Task 11.

If you want anything else done here in the meantime, like changing the plan, rethinking a design decision, or drafting instructions for your team on labelling the test meetings, I can do that in this session.


### SIM

Ok, got it. I'll just do the plan and docs here. Can you draft those instructions for my team on labelling the test meetings?


### USER

Ok, got it. I'll just do the plan and docs here. Can you draft those instructions for my team on labelling the test meetings?


### BUILDER

I've written the labelling guide and committed it as `docs/eval-labelling-guide.md`. It's for teammates who have never seen the code, so there's no JSON or technical terms in it.

**What's in it:**
- **Why it matters:** a short explanation that this is the main check before launch.
- **Picking meetings:** the mix you need (Docs, Zoom and Granola, with at least two "Me"/"Them" transcripts, plus some messy ones). Notes must not be edited; if something is too sensitive, pick a different meeting. There's also a line on how the notes are handled confidentially.
- **For each meeting:** title, date, source, who "Me" is, the notes pasted exactly, and a simple table with task, owner, due date and comments.
- **Rules:**
  - Action items use the same definition the app's prompt uses.
  - The owner is one of the 8 official names (Tomás, never Tom) or "none". Shared tasks get one row per person.
  - Due dates are real calendar dates, with a table of examples ("by Friday", "end of month", "next week" → blank).
- **A worked example:** the same sample meeting the plan uses for its smoke test, so the guide and the eval agree.
- **A checklist before sending,** and a request not to share the meetings in shared channels.
- **A final section for whoever loads the answers into the eval:** how each table converts into the eval's folder format, and a reminder to settle borderline items with the labeller first.

**One choice to check.** If a labeller knows who "Them" really was, the guide asks them to write the real name. The app will still flag that item rather than guess, and the eval counts it as "wrong but flagged". That doesn't fail any launch bar, but it does count towards the 15% flag rate, so meetings with lots of "Them" commitments will push that rate up. The alternative is to have labellers always write "none" for "Them", which would measure only whether the app avoids guessing. I'd keep the real names because they give a more honest picture.

**Before you send it:** "Send each meeting to me" assumes it goes out under your name. The date examples use 24 September 2026, which is fine even if the meetings are older, since they only show how to count forward from the meeting date.


### SIM

Keep the real names, agreed - matches R4 and gives us a more honest read.

Go ahead and send the meetings out under my name.


### USER

Keep the real names, agreed - matches R4 and gives us a more honest read.

Go ahead and send the meetings out under my name.


### BUILDER

I haven't sent anything yet. Sending messages to your team under your name can't be undone, and I'm missing what I need to do it:

1. **Who gets it, and at what addresses?** The only domain I have is the placeholder `acme.com`, so I don't have real addresses. Should it go to all seven teammates, or only some?
2. **Email or Slack?** I can reach both. For Slack, which channel or which direct messages? The guide asks people not to post meetings in shared channels, so a channel post collecting replies would contradict that. I'd suggest direct messages or email.
3. **How should the guide be attached?** It's a file in this repo (`docs/eval-labelling-guide.md`), not a shared doc. I can paste the full text into the email, or upload it to Google Drive and share a link. The link is easier to read and to update later.
4. **Deadline and number of meetings:** is there a date you want them back by, and do you want to split the 10–20 meetings, say 2–3 per person?

Here's the covering message I'd send once you confirm. Edit it as you like:

> **Subject:** Help test the action-items app — label 2–3 past meetings
>
> Hi all,
>
> Before we launch the meeting action-items app, I want to check it against real meetings. Could you each pick **2–3 past meetings** and write down the correct list of action items? It takes about 10–15 minutes per meeting. The guide below explains exactly what to do, with a worked example.
>
> Please send each meeting to me directly, not in a shared channel, by **[date]**.
>
> [guide link or full text]
>
> Thanks!
> Aman

If you'd rather see it before anything goes out, I can create it as a **draft** in your Gmail for you to review and send yourself.


### SIM

Send it to all 8 of us — Priya, Marcus, Sarah, Tomás, Aisha, Dana, Ravi, Lena, plus me. Real domain is our actual company Workspace domain, not acme.com — please just use a placeholder like [yourcompany.com] in the draft and I'll swap in real addresses myself before sending.

Email, not Slack. Direct messages/email as you suggested.

Paste the full guide text into the email rather than a Drive link, simpler.

Deadline: one week from today, so Oct 3. Yes, split it — 2-3 meetings per person.

Just create it as a Gmail draft for me to review, don't send it yet.


### USER

Send it to all 8 of us — Priya, Marcus, Sarah, Tomás, Aisha, Dana, Ravi, Lena, plus me. Real domain is our actual company Workspace domain, not acme.com — please just use a placeholder like [yourcompany.com] in the draft and I'll swap in real addresses myself before sending.

Email, not Slack. Direct messages/email as you suggested.

Paste the full guide text into the email rather than a Drive link, simpler.

Deadline: one week from today, so Oct 3. Yes, split it — 2-3 meetings per person.

Just create it as a Gmail draft for me to review, don't send it yet.


### BUILDER

I couldn't create the Gmail draft. Claude Code asked for permission to use the Gmail draft tool and the permission wasn't granted, so nothing was created or sent.

The email is fully written and ready to go. You have two options:

- **Allow the Gmail draft permission** (the `create_draft` tool) and tell me to try again. I'll create the same draft, and nothing will be sent.
- **Or I save the email to a local file** in the repo, and you paste it into Gmail yourself.

A few things about the email itself:

- **Placeholder addresses:** Gmail only accepts real email address formats, so `[yourcompany.com]` won't work. I used `priya@yourcompany.example` and so on instead. The `.example` ending is reserved and can never be delivered, so nothing goes astray if one slips through unchanged.
- **Your own address:** I put the 8 teammates in "To" and you in "Cc" as `aman@yourcompany.example`, guessing firstname@ from your name. Swap it for your real work address.
- **The deadline falls on a Saturday.** 3 October 2026 is a Saturday, so the email says "Saturday 3 October". Would you rather use Friday 2 October?
- **How it asks for the 2–3 meetings each:** it asks everyone for 2–3 meetings, and asks Granola users to include at least one with "Me"/"Them" labels. That way the two such transcripts needed across the team should come in without assigning sources to people. With 8 people that's 16–24 meetings, a little over the 20 target, which is fine.
- **What's left out:** the email contains the full guide except the final "for whoever loads these into the eval" section, which is only for the person building the test.


### SIM

Just save it to a local file, I'll paste it in myself. Use Friday 2 October instead of Saturday. And don't worry about my exact email address, just leave a placeholder there too.


### USER

Just save it to a local file, I'll paste it in myself. Use Friday 2 October instead of Saturday. And don't worry about my exact email address, just leave a placeholder there too.


### BUILDER

I've saved the email to `docs/eval-labelling-email.txt`, ready for you to paste into Gmail.

- **Top of the file:** the To, Cc and Subject lines. Teammates are `firstname@[yourcompany.com]` and you're `[your work email]`. Replace those placeholders before sending.
- **Below the marked line:** the email body to paste, in plain text so it pastes cleanly. It's the full labelling guide, with the tables turned into simple lines.
- **Deadline:** changed to **Friday 2 October**, in both the subject and the body.

I haven't committed this file to git. Once you've sent the email it's only a throwaway copy of it, so you can delete it or keep it. The guide itself is already committed as `docs/eval-labelling-guide.md`.


### SIM

Looks good. I'll fill in the real emails and send it. Deleting the throwaway copy after — no need to keep it.


### USER

Looks good. I'll fill in the real emails and send it. Deleting the throwaway copy after — no need to keep it.


### BUILDER

Sounds good. I've added this to the memory note so a future session knows:

- the team was asked for 2–3 labelled meetings each, due Friday 2 October
- labellers write the real owner even for "Them" in transcripts
- returned meetings get converted using the last section of `docs/eval-labelling-guide.md`, once borderline items are settled with each labeller

**Where things stand:**
- **Committed:** the spec, the plan with the roster filled in, and the labelling guide.
- **To build:** open a normal, unrestricted Claude Code session in this folder and say "go ahead with the plan".
- **Before Task 11 and deployment:** the Anthropic API key, a Google OAuth client and a Postgres database URL.
- **Before launch:**
  - the labelled meetings from your team, to run the accuracy test against the three launch bars
  - swap `acme.com` for your real domain, in both the roster file and the sign-in setting


### SIM

Sounds good, that all matches. I'll get the team started on the labelled meetings and follow up once I have the API key, OAuth client, and database URL sorted.


### USER

Sounds good, that all matches. I'll get the team started on the labelled meetings and follow up once I have the API key, OAuth client, and database URL sorted.


### BUILDER

Sounds good. One thing that could save you time: **the build doesn't have to wait for those credentials.** Tasks 1–10 run without them, because tests use a local in-memory database and a fake extraction step. Only Task 11 needs the Anthropic key, for its one real test run against Claude, and only deployment needs the Google OAuth client and database URL. You could start the build in an unrestricted session now and supply the credentials when it reaches Task 11.

Everything is committed and noted, so any future session can pick up from here.


### SIM

Sounds good, let's do it that way then. Go ahead and start the build.


### USER

Sounds good, let's do it that way then. Go ahead and start the build.


### BUILDER

I can't start the build in this session. It's still running under the planning-only restriction: no application code may be written. Building means scaffolding the app and writing code from the first step, so I'm stopping before anything starts.

I've noted in the memory file that you want to build now and supply the credentials at Task 11.

To start, open Claude Code in this folder as a normal interactive session, for example by running `claude` in a terminal in that folder, rather than through whatever is launching this planning-only one. Then say "go ahead with the plan". That session will find the committed plan and the memory note, and run Tasks 1–10 without needing any keys.


### SIM

Got it, that makes sense. I'll open a regular terminal session and run Tasks 1–10 there. Thanks for saving the note in memory.


### USER

Got it, that makes sense. I'll open a regular terminal session and run Tasks 1–10 there. Thanks for saving the note in memory.


### BUILDER

That plan works. The one leftover here is `docs/eval-labelling-email.txt`. It's not committed, so it won't get in the way, but delete it once your email has gone out.

In the new session, the build should run through Task 10 on its own. It will stop at Task 11 to ask for the Anthropic key, so you can hand it over then, or pause there until you have it. Good luck with the build.


### SIM

Sounds good — I'll delete that file after the email's sent. Thanks, talk soon.


### USER

Sounds good — I'll delete that file after the email's sent. Thanks, talk soon.


### BUILDER

Talk soon. I hope the labelling round goes smoothly.


### SIM

Thanks, talk soon.


### USER

Thanks, talk soon.


### BUILDER

Talk soon.


### SIM

<<DONE>>
