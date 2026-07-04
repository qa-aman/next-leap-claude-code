---
name: mom
description: |
  Turn a file of raw meeting notes, minutes, or a transcript into a ready-to-send Minutes of Meeting (MoM) written in Axios Smart Brevity style. Use this skill whenever the user wants to write, produce, format, share, or send meeting minutes or a MoM from a notes file, even if they don't say "Smart Brevity". Trigger on phrases like "send the MoM", "create minutes of meeting", "write up the MoM", "turn these meeting notes into minutes", "share the meeting summary", "MoM for this meeting", "minutes from the sync/standup/review", or when the user points at a meeting notes file and asks for minutes to circulate. Do NOT trigger for daily standup digests (use standup-summary) or for drafting an email (use email-drafter) unless the user explicitly wants meeting minutes.
---

# MoM — Minutes of Meeting (Smart Brevity)

Turn raw, messy meeting notes into a Minutes of Meeting that a busy non-attendee reads in 30 seconds and acts on. The reader wasn't fully present. They want the outcome, what it means for them, and what they now owe, without wading through the discussion.

## The frameworks this skill applies

**Smart Brevity** (Axios: VandeHei, Allen, Schwartz) is the backbone. Meeting minutes are a distribution artifact, not a persuasion essay, so the reader scans before they read. Smart Brevity is built for exactly this: lead with the single most important thing, say why it matters, then make everything scannable with bold lead-ins and short bullets. The goal is roughly 40% shorter than the raw notes while losing nothing that matters.

**One Minto move** (Barbara Minto, Pyramid Principle): answer first. Every decision and every action item leads with the outcome, not the discussion that produced it. Write "Ship confidence scoring behind a flag on 28-03" then the one line of why, never a paragraph of debate ending in the decision. The reader gets the conclusion in the first three words of the bullet.

## Input

The user provides a file path to meeting notes, minutes, or a transcript. If they didn't name one, ask which file. If they pasted raw text instead of a path, treat the pasted text as the source.

Read the whole file before writing anything. Skimming loses owners, dates, and the one decision that actually mattered.

## Hard rules

- **No invented content.** Use only what's in the source file. If a detail (owner, date, attendee) isn't there, mark the gap rather than fill it. This mirrors the rest of this repo: no invented metrics, cite the source.
- **Every action item needs an owner and a due date.** If the notes don't name an owner, write `owner: unassigned`. If no date is stated, write `due: not stated`. Never guess. A visible gap prompts follow-up; a guessed date creates a false commitment.
- **Dates are DD-MM-YYYY** everywhere, including the filename.
- **Keep sections even when empty.** If there were no decisions, write "None this meeting." so the reader knows nothing was dropped, rather than wondering if a section is missing.
- **Answer-first bullets.** The outcome is the first few words of every decision and action bullet. Context, if needed, comes after a dash on the same line.

## Date handling

Use the **meeting's date** (from the file's title, header, or filename), not today's date, for both the MoM heading and the filename. If the notes give only a relative date ("yesterday's sync"), resolve it against any absolute anchor in the file. If no meeting date can be found anywhere, ask the user for it rather than assuming.

For action-item due dates stated as relative ("by end of sprint", "next Friday"), resolve them against the meeting date and write the absolute `DD-MM-YYYY`. If a time qualifier matters, keep it in parentheses, e.g. `28-03-2026 (EOD)`.

## Output

Write to `outputs/mom-<meeting-slug>-DD-MM-YYYY.md`. The slug is a short kebab-case name of the meeting (e.g. `sprint-planning`, `stakeholder-sync`). Use this exact structure:

```markdown
# MoM: <Meeting Name> — DD-MM-YYYY

**The headline:** <one sentence — the single most consequential outcome of this meeting>

**Why it matters:** <1-2 lines — why someone who skipped this meeting should care>

## Decisions
- **<Decision, stated outcome-first>** — <one line of context, only if it isn't obvious>

## Action items
- **<Owner>** — <action, outcome-first> — due DD-MM-YYYY

## Discussion — go deeper
- **<Topic>** — <2-3 lines. What was debated and where it landed. Skip anything already captured above.>

## Open questions / parked
- <unresolved item, and who needs to resolve it if the notes say>

---
*Attendees: <names from the file, or "not listed"> | Source: <input file path>*
```

### Notes on each section

- **The headline** is the hardest and most important line. It is not "we had a meeting about X." It is the one thing that changed. If you can only keep one sentence, this is it.
- **Why it matters** connects the outcome to the reader's world: a deadline, a risk, a dependency, a number that moved. Lead with impact, not recap.
- **Decisions** and **Action items** carry the weight. Bold the lead so the eye catches it while scrolling.
- **Discussion — go deeper** is the optional layer for people who want the texture. Keep it tight; it is not a transcript. If everything important is already in Decisions and Actions, a one-line "Nothing beyond the decisions above." is fine.
- **Open questions / parked** surfaces what's unresolved so it doesn't silently vanish. This is where next meetings get their agenda.

## Length discipline

Target the MoM at roughly 40% the length of the source notes. If the notes are already short, don't pad to fill the template — shorter is the point. Cut hedging, throat-clearing, and any sentence that restates a bullet. Every line should earn its place by telling the reader something they'd act on.

## Finish

Print a **one-line confirmation** with the output file path. Do not restate the full MoM in chat — the file is the deliverable, and re-pasting it wastes the reader's attention, which is the whole thing this skill is fighting for.

If the user later says "send it to #channel" or "draft an email to X", that's a separate delivery step handled by the Slack or email tooling — this skill's job ends at the ready-to-send file.

## Example

**Source (raw notes excerpt):**
> Talked for a while about the confidence scoring rollout. Marcus worried about false positives at low confidence. Priya said support is drowning in tickets about wrong action items. Eventually agreed we'll gate v2 behind a feature flag and turn it on for 10% of Pro on the 28th. Sarah to write the rollback doc, needs it before we flip the flag. Someone should tell the CS team but we didn't decide who.

**MoM output (Decisions + Actions):**
```markdown
## Decisions
- **Confidence Scoring v2 ships behind a feature flag, 10% of Pro on 28-03-2026** — gated rollout to contain false-positive risk Marcus raised.

## Action items
- **Sarah** — write the rollback doc, required before the flag flips — due 27-03-2026
- **owner: unassigned** — brief the CS team on the rollout — due: not stated
```

Notice: the decision leads with the outcome, not Marcus's worry. The unassigned CS action is surfaced, not invented an owner for. The false-positive debate lives in "go deeper," not here.
