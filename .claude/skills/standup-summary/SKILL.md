---
name: standup-summary
description: |
  Summarize daily team standup notes into a structured markdown digest covering team progress, blockers, decisions, and action items. Use this skill whenever the user wants to process, summarize, condense, or recap daily standup notes, scrum notes, or daily sync notes, even if they don't explicitly say "standup". Trigger on phrases like "summarize the standup", "recap today's standup", "what happened in standup", "digest this standup", "standup summary for [date]", "turn these standup notes into a summary", or when the user points at a `daily-standup-*.md` file and wants it processed. Also trigger when the user wants to surface blockers, decisions, or owner-tagged action items from raw standup notes.
---

# Standup Summary

Turn raw, messy team standup notes into a structured markdown summary that a busy stakeholder can read in 60 seconds and a PM can act on.

## When to use

The input is always a daily standup notes file (typically `10-meetings/daily-standup-DD-MM-YYYY.md` in this repo, but any file path works). The notes are conversational, one block per person, possibly with a decisions/followups section at the bottom.

If the user pastes raw text instead of a file path, treat the pasted text as the source. If neither is provided, ask which file.

## Workflow

1. **Read the source file** end to end before writing anything. Don't skim, you'll miss owners and dates.
2. **Identify the participants** and which one is the PM (usually labeled "Me (PM):" or similar). This matters because the PM's update often contains cross-cutting context (rollout plans, scope decisions, risks).
3. **Extract per person**: what they finished yesterday, what they're doing today, blockers, and any callouts (PTO, handoffs, dependencies).
4. **Pull out cross-cutting items**: decisions made, risks raised, deadlines mentioned, scope changes.
5. **Tag every action item with an owner AND a date.** Owner and date are both required fields, never omit them.
   - If no owner is named, mark it `owner: unassigned`.
   - For the date: if a specific date is stated (e.g. "by Tue 24-03"), use it as `DD-MM-YYYY`. If only a relative time is stated ("by EOD", "after lunch", "this week"), resolve it against the standup date from the filename and write the resolved `DD-MM-YYYY`, optionally with the time qualifier in parentheses, e.g. `20-03-2026 (EOD)`. If no date or time signal exists at all, mark it `due: not stated` so the gap is visible. Don't guess.
6. **Write the output** to `outputs/standup-summary-DD-MM-YYYY.md` using the template below. Date comes from the source file's date, not today's date.
7. **Print a one-line confirmation** with the output path. Don't restate the summary in chat.

## Output template

Use this exact structure. Sections stay even if empty (write "None this standup." so the reader knows nothing was missed).

```markdown
# Standup Summary - DD-MM-YYYY

**Sprint context:** {one line, e.g. "Day 4 of Action Item Confidence Scoring v2 sprint"}
**Attendees:** {names, note anyone absent or late}

## TL;DR
{2-3 bullets. The things a skip-level would want to know. Lead with the most consequential item, not the first one mentioned.}

## Progress by person
| Person | Yesterday | Today | Blockers |
|--------|-----------|-------|----------|
| {name} | {1 line} | {1 line} | {1 line or "None"} |

## Blockers and risks
- {blocker or risk}, owner: {name}, needs: {what unblocks it}

## Decisions made
- {decision}, decided by: {name or "team"}

## Action items
Every item must include both an owner and a due date. Due date is in DD-MM-YYYY, with an optional time qualifier in parentheses. Use `not stated` only if the source genuinely has no date or time signal.
- [ ] {action}, owner: {name}, due: {DD-MM-YYYY, optionally "(EOD)" / "(11am)" / etc.}

## Callouts
- {PTO, handoffs, external dependencies, anything that affects the next 1-2 days}
```

## Writing rules

- One line per cell in the progress table. If someone rambled, compress to the verb and the object ("Finished corpus pull", not "Wrapped up the corpus pull yesterday like we discussed").
- Preserve numbers verbatim. If the engineer said "78% up from 61%", keep both numbers. Don't round.
- Preserve dates verbatim in DD-MM-YYYY. Convert any other formats found in the source.
- Don't invent owners. If the notes say "we should decide X", mark owner as `unassigned`.
- Don't editorialize. No "great progress" or "concerning". Just the facts.
- Distinguish **decisions** (already made) from **action items** (to be done). A common mistake is putting a decision in the action items list.
- The TL;DR is not the same as the first three action items. It's the answer to "if you only read 3 lines, what should you know?" That's usually one big risk, one big win, and one decision, but use judgment.

## Why this structure

Stakeholders read the TL;DR. PMs read the action items and blockers. Engineers read the progress table to see who's working on what overlapping piece. Putting decisions in their own section prevents them from getting lost as bullet points in someone's update, which is the most common failure mode of raw standup notes.

## Example

**Input** (excerpt from `10-meetings/daily-standup-20-03-2026.md`):
> "Remi: Training run kicks off after lunch... ran a quick sanity check on 100 examples and it's catching ~78% which is up from 61%. Worried about one thing - the conditional actions corpus Yuki pulled, some of it looks noisy, like maybe 15% mislabeled."

**Output row:**
| Remi | Implicit commitments tweaks done, sanity check 78% (up from 61%) | Kick off training run after lunch, spot check corpus for mislabels | Corpus noise risk (~15% mislabeled) |

And in Blockers and risks:
- Conditional actions corpus may be ~15% mislabeled, owner: Remi, needs: spot check before training run

## Edge cases

- **PM is the user**: the PM's own update often contains strategic context (rollout plans, scope cuts) that doesn't fit cleanly in "yesterday/today". Pull these into Decisions, Risks, or Callouts as appropriate, and keep the PM's table row focused on concrete work.
- **No explicit decisions/followups section**: scan the full notes for phrases like "let's decide", "going with", "deferred to", "owner:", "by EOD", "by Tuesday". These are signals.
- **Cross-references to other dates**: if someone mentions "by Tuesday 24-03" preserve the date. If they say "by Tuesday" without a date, leave it as stated, don't guess.
- **Late joiners or absences**: note in Attendees line.
