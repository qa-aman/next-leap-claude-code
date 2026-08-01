---
name: work-log
description: |
  Build the daily work log for this project from its Claude Code JSONL session
  transcripts. Reads every transcript, works out which days had activity, checks
  which of those days already have a log file in .local/log/, then writes today's
  log and backfills any missing day. Use when Aman says "/work-log", "work log",
  "log my work", "create the work log", "what did I do today", "what did I work on
  on <date>", "backfill my work logs", or wants a record of the work done in this
  repo on a given day. Project-scoped: only this repo's transcripts, only this
  repo's .local/log folder.
created_by: Aman Parmar
last_modified: 01-08-2026
---

# /work-log - Daily Work Log from Session Transcripts

Turns raw Claude Code session transcripts into a readable daily record of what
was actually built. The evidence comes from the transcripts, never from memory
and never from the current conversation alone.

## What this is not

1. This is not `/eod`. `/eod` logs only the current chat into `.local/work-log/`
   and then flushes the memory inbox. `/work-log` reads every session for the day
   from disk and writes into `.local/log/`. Do not touch `.local/work-log/`, and
   do not call `/consolidate-memory` from here.
2. This is project-scoped. It only ever reads this repo's transcript directory
   and only ever writes inside this repo's `.local/log/`.

## Output location

```
.local/log/<MM-monthname-YYYY>/<DD-MM-YYYY>.md
```

For example, 01-08-2026 goes to `.local/log/08-august-2026/01-08-2026.md`.
The extractor prints the exact path, so use what it prints rather than
constructing the path by hand.

## Step 1: Index the days

Run the extractor from the repo root:

```bash
python3 .claude/skills/work-log/scripts/extract_day.py --index
```

It prints every date (IST) that has session activity, the number of sessions,
prompts and files touched on that date, and whether a log file already exists.
The last line lists `MISSING_DATES`.

Read the dates from this output. Never guess today's date and never take it from
memory, the extractor computes it in IST.

## Step 2: Decide the batch

1. Today is always in scope, whether or not it already has a log file.
2. Every date in `MISSING_DATES` is a backfill candidate.
3. If more than 5 days are missing, do not silently process all of them. State
   the count, then use AskUserQuestion to offer: all missing days, the most
   recent 5, or today only. Backfilling 17 days is a real cost and that call is
   Aman's.
4. If nothing is missing and today already has a log, say so in one line, then
   append today's new work per Step 4 if there is activity not already in the
   file. Do not rewrite what is already there.

## Step 3: Pull the evidence for each date

```bash
python3 .claude/skills/work-log/scripts/extract_day.py --date 01-08-2026
```

`--today` is shorthand for today's date. `--date` is repeatable, so a small
batch can be pulled in one call. For a very heavy day, trim the noise with
`--max-bash 0` or `--prompt-chars 300`.

The digest gives you, per session: the session id, its title, its time span in
IST, the git branch, the prompts Aman typed, the files written or edited, the
skills and subagents used, git commit subjects, todos, bash commands and the
paths that were read.

If a day is heavy (say 10 or more sessions), pull it in its own call rather than
batching it with others, so the digest stays readable.

## Step 4: Write the log

One file per date. One task block per end-to-end deliverable, not one per
session and not one per tool call. A single deliverable that spans three
sessions is one task block. Three unrelated things in one session are three
task blocks.

Use this structure exactly:

```markdown
# Work Log - <DD-MM-YYYY>

**Sessions:** 5 | **Active:** 10:20 - 17:45 IST | **Branch:** main

## Summary

<2 to 4 sentences on what the day amounted to. What shipped, what moved, what
stalled. Written so that reading only this paragraph tells the story.>

## Task 1 - <Title> (HH:MM - HH:MM)

### What was done
1. <specific, concrete bullets>
2. <a real decision, with what was decided and why>

### Files changed
1. `<repo-relative path>` - <what changed in it>

### Evidence
1. Session `<8-char id>` - <session title>
2. Commit: `<commit subject>` (only if there was one)
3. Skills used: `<skill>` (only if any)

## Task 2 - ...

## Open threads

1. <anything started and not finished, with where it stopped>

## Sessions on this day

| Session | Title | Time (IST) | Prompts | Files |
|---|---|---|---|---|
| `48664be7` | Create daily work log skill | 14:54 - 15:20 | 4 | 2 |
```

Append-safe rules:

1. If the file already exists, never overwrite it. Read it, then append only the
   task blocks that are not already recorded, continuing the numbering. Update
   the header counts and the sessions table to match.
2. If a day genuinely had no substantive work (a couple of prompts, nothing
   built), write a short file that says so rather than padding it into tasks.

## Writing rules for the log body

1. Write what shipped, not what was attempted. If something was tried and
   abandoned, say so plainly in a bullet. A log that only records wins is not a
   log.
2. Every file path must come from the digest's FILES WRITTEN/EDITED lines. Never
   list a path you did not see there.
3. Same for commit subjects, skills and subagents. If the digest does not show
   it, it does not go in the log.
4. Where the digest is thin (a session with prompts but no file writes), say
   what was explored rather than inventing an outcome. "Explored X, no changes
   made" is a valid task block.
5. Numbered lists, never unnumbered bullets. No em dashes or en dashes. No
   semicolons, use a comma or a colon. No exclamation marks. Dates DD-MM-YYYY.
6. Keep each task block tight. Four to eight bullets under "What was done" is
   usually right. If a block needs more, it is probably two deliverables.
7. Titles state what was built, not the activity. "Add ServiceNow ticket
   classification pipeline" beats "Worked on ServiceNow".

## Step 5: Confirm

Print a short wrap:

1. How many day files were written or appended, and their paths.
2. How many days remain un-backfilled, if any.

A few lines. This is a wrap-up, not a report.

## Notes

1. `.local/` is meant to stay out of version control. If this repo does not
   already ignore it, mention that once rather than silently committing logs.
2. Transcript timestamps are UTC in the JSONL. The extractor converts everything
   to IST, so a session running past midnight UTC lands on the right IST day and
   is split correctly across two day files.
3. Re-running `/work-log` on the same day is safe: Step 4 appends.
