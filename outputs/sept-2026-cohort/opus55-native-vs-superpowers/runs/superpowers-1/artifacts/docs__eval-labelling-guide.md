# How to label test meetings for the action-items app

We're building an app that reads our meeting notes and pulls out every action item, with who owns it and when it's due. Before we launch, we need to check that it really gets them right. To do that, we'll give it some real past meetings and compare what it finds with what **you** say the correct answer is.

Your job is to pick a meeting and write down the correct list of action items. It takes about 10–15 minutes per meeting, and it's the most important check we run before launch, so accuracy matters more than speed.

**We need 10–20 meetings in total.**

## 1. Pick meetings

Aim for a mix:

- **Google Docs bullet notes:** a few.
- **Zoom transcripts:** a few.
- **Granola transcripts:** a few, including **at least two** where speakers show up as "Me" / "Them".
- **Some messy ones:** long transcripts, meetings where people talked over each other, or tasks that were shared or vaguely assigned. The app should be tested on real, messy meetings, not just the tidy ones.

**Don't edit the notes.** Use them exactly as they are, typos included, because that's what the app will see. If a meeting contains something too sensitive to share, pick a different meeting rather than cutting parts out.

**Confidentiality:** your notes will be kept on the project machine, never committed to our code repository, and sent to the Claude API when we run the check. That's the same thing that happens when the app is used for real.

## 2. For each meeting, send these five things

1. **Meeting title:** anything that identifies it.
2. **Meeting date.**
3. **Source:** Google Docs, Zoom, or Granola.
4. **Who is "Me"?** For Granola transcripts, the person who recorded the meeting. Otherwise write "n/a".
5. **The notes,** copied and pasted exactly as they are.

Then fill in the action-item table below.

## 3. Write the action items

Use one row per action item:

| # | Task | Owner | Due date | Comments |
|---|------|-------|----------|----------|
| 1 | | | | |

### What counts as an action item

**Include** anything someone committed to, was asked to do, or agreed to do *after* the meeting:

- Things stated directly: "Priya to send the deck by Friday."
- Things implied in a transcript: "I'll take that", "leave it with me", "sure, I can do that."
- Tasks for people **outside** our team, like a client or another department. Include them, and see the Owner rules below.

**Leave out:**

- decisions ("we're going with option B")
- discussion points and open questions
- vague ideas nobody took on ("we should think about pricing at some point")
- things that were done *during* the meeting

**If you're not sure,** ask yourself: *"Would I expect to see this on our team's to-do board?"* Include it if yes. Either way, add a comment saying it was borderline, so we can discuss it.

### Task

Write it in your own words, short and clear, for example "Send the Q3 deck to the client". It doesn't need to match the notes word for word; we compare by meaning.

### Owner

Write exactly one of these:

- **One of our 8 names:** Priya, Marcus, Sarah, Tomás, Aisha, Dana, Ravi, Lena. Use the official name, not a nickname: write **Tomás**, even if the notes say "Tom".
- **none:** if no owner is stated, the owner is outside our team, or you can't tell who it was (for example "Them" in a transcript and you don't remember who said it).

Special cases:

- **"Me" in a Granola transcript:** write the person you named in "Who is 'Me'?".
- **A task for two or more people** ("Marcus and Aisha to review the doc"): write **one row per person**, with the same task in each.
- **Knowing who "Them" really was:** if you do know, write the real name. The app will flag that item for review rather than guess, and that's fine. We still want the true answer on your list.

### Due date

Write the **actual calendar date** the deadline means, counting from the meeting date:

| Notes say | Meeting on Thu 24 Sep 2026 → write |
|---|---|
| "by Friday" | 25 Sep 2026 (the next Friday after the meeting) |
| "tomorrow" | 25 Sep 2026 |
| "end of today" | 24 Sep 2026 |
| "end of month" | 30 Sep 2026 |
| "by the 3rd" | 3 Oct 2026 |
| "next week", "soon", "ASAP", "after the offsite" | leave blank (no specific date) |
| no deadline mentioned | leave blank |

If a deadline could reasonably mean two different dates, leave it blank and explain in the comments.

## 4. Worked example

**Title:** Weekly sync · **Date:** Thu 24 Sep 2026 · **Source:** Granola · **Who is "Me"?** Dana

> Me: Okay, let's wrap up. Priya, can you send the Q3 deck to the client by Friday?
> Them: Sure, and I'll loop in Jamal on the pricing numbers.
> Me: Great. Tom said he'd book the offsite venue before end of month.
> Me: I'll chase legal on the contract redlines tomorrow.
> Them: Marcus and Aisha should review the onboarding doc next week.
> Jamal will share the churn numbers after the board meeting.

| # | Task | Owner | Due date | Comments |
|---|------|-------|----------|----------|
| 1 | Send the Q3 deck to the client | Priya | 25 Sep 2026 | |
| 2 | Loop in Jamal on the pricing numbers | none | | Said by "Them"; can't tell who |
| 3 | Book the offsite venue | Tomás | 30 Sep 2026 | Notes say "Tom" |
| 4 | Chase legal on the contract redlines | Dana | 25 Sep 2026 | "Me" = Dana |
| 5 | Review the onboarding doc | Marcus | | Shared task, one row each; "next week" isn't a date |
| 6 | Review the onboarding doc | Aisha | | Shared task |
| 7 | Share the churn numbers | none | | Jamal isn't on our team |

## 5. Before you send it

- [ ] The notes are pasted exactly as they were, with nothing edited or trimmed.
- [ ] Every commitment is in the table, including implied ones in transcripts.
- [ ] Every owner is one of the 8 names (Tomás, not Tom) or "none".
- [ ] Shared tasks have one row per person.
- [ ] Due dates are real calendar dates, or blank if there's no specific date.
- [ ] Borderline items have a comment.

Send each meeting to me as a separate document. **Please don't post them in shared channels.**

---

## For whoever loads these into the eval (not needed by labellers)

Each meeting becomes one folder under `evals/data/<meeting-name>/` (git-ignored), in the format described in `evals/README.md`:

- **`meta.json`:**
  - `title`
  - `meetingDate`, as YYYY-MM-DD
  - `meSpeaker`: a roster key or `null` ("n/a" → `null`)
  - `source`: `"docs"`, `"zoom"` or `"granola"`
- **`notes.txt`:** the pasted notes, unchanged.
- **`expected.json`:** one `{ "task", "owner", "dueDate" }` per table row.
  - `owner` is the roster key (`priya`, `marcus`, `sarah`, `tomas`, `aisha`, `dana`, `ravi`, `lena`), or `null` for "none".
  - `dueDate` is YYYY-MM-DD, or `null` if blank.

Before converting, go through the comments with the labeller. Settle every borderline item as either in or out, because the eval treats the list as the exact correct answer.
