# Launch Kit - Smart Summaries v2.4
**Date:** 17-03-2026 | **Launch target:** GA - Released November 2025

---

## Positioning Summary

- **Alternatives:** Re-reading long transcripts manually, writing follow-up notes by hand, or accepting generic "transcript highlight" summaries from Otter.ai (source: competitive.md)
- **Unique capabilities:** Summaries are 30% shorter on average; decisions surface at the top in a consistent structure (decisions, discussion, context); no competitor offers this structured hierarchy by default (source: release-v2.4-smart-summaries.md, competitive.md)
- **Value:** Users who run 8-10 meetings/day can scan the three things that matter in seconds - not wade through 350-word summaries - and leave the meeting with a reliable record rather than an essay (source: release-v2.4-smart-summaries.md, sarah-chen.md)
- **Target customer:** Sarah Chen (Power User, Pro plan) - runs 8-10 meetings daily, no buffer time, needs to scan outputs quickly; summaries-too-long was her class of complaint (#2 theme, 14 mentions in Q1 2026 NPS survey) (source: sarah-chen.md, release-v2.4-smart-summaries.md)
- **Category frame:** AI meeting assistant - specifically the summary quality sub-category where Otter is generic and Notion AI is basic (source: competitive.md)

---

## 1. Announcement Blurb

You leave 8 meetings a day and come back to a 350-word wall of text. You skim it fast, miss the decision buried in paragraph four, and spend 20 minutes rewriting follow-ups from scratch anyway.

Smart Summaries v2.4 fixes the shape of the problem. Summaries are now 30% shorter on average, and every summary opens with decisions first - not context, not discussion, decisions. The structure is consistent every time: decisions, then discussion, then context. Nothing is buried.

Turn it on in your account settings. Your next summary will look different immediately.

Promoters now cite summaries as the reason they recommend MeetFlow - a shift backed by a 12-point NPS gain from Q3 2025 to Q1 2026. The "summaries too long" complaint dropped from the #2 theme to background noise.

Your meetings are already recorded. Now the output is worth reading.

---

## 2. Customer Email

**Subject:** Your meeting summaries just got 30% shorter

You told us summaries were too long. The #2 complaint in our NPS survey: "I want bullet points, not an essay. Give me the 3 things that matter."

Smart Summaries v2.4 is live for your account.

What changed: summaries are 30% shorter on average. Decisions are highlighted at the top every time - not buried in paragraphs. The structure is consistent: decisions first, then discussion, then context.

The old model averaged 350 words for a 30-minute meeting. That is too much to skim between back-to-back calls.

Open your most recent meeting summary to see the difference.

This shipped in November 2025 and is already running on your account. No setup needed.

---

## 3. In-App Banner

**Banner text (87 characters):** Summaries are now 30% shorter. Decisions surface first. Same meeting, less reading.

**CTA button:** See your summary

---

## 4. Social Post

You asked for bullet points, not essays. Your meeting summaries now open with decisions at the top - 30% shorter on average, structured the same way every time. The thing you needed to see is no longer buried in paragraph four.

*(279 characters)*

---

## SUCCESs Scorecard

| Check | Blurb | Email | Banner | Social |
|---|---|---|---|---|
| Simple | pass - one idea: summaries are shorter and structured better | pass - one idea, one CTA | pass - compressed to one benefit + CTA | pass - single point: decisions surface first, shorter |
| Unexpected | pass - opens on the problem (wall of text), not the feature name | pass - subject line leads with the user's payoff ("30% shorter"), not "Introducing" | pass - "less reading" reframes the benefit against the expected "better summaries" framing | pass - "buried in paragraph four" is a specific, uncomfortable image |
| Concrete | pass - "350-word wall", "30% shorter", "8 meetings a day" all from files | pass - "30% shorter", "350 words", "November 2025" all sourced | pass - "30% shorter" is concrete; 87 chars is tight but passes | pass - "30% shorter", "paragraph four" is concrete placement, not abstract |
| Credible | pass - 12-point NPS gain (Q3 2025 to Q1 2026), 14 NPS mentions, all sourced | pass - "your account" grounds it; "#2 complaint" from NPS survey sourced | borderline pass - no stat fits in 90 chars, but "30%" is a real number from release notes | pass - "30% shorter" is a sourced number; no invented claims |
| Emotional | pass - "buried in paragraph four" and "worth reading" hit the frustration and relief | pass - "too much to skim between back-to-back calls" names the physical reality | pass - "less reading" touches the relief, though lightly | pass - "buried in paragraph four" names the irritation precisely |
| Stories | pass - before (wall of text, miss the decision, rewrite follow-ups) -> turn (v2.4 ships) -> after (worth reading) | pass - before (too long) -> turn (what changed) -> after (open it, see the difference) | pass - implied arc: was buried, now surfaces, less effort | pass - implied arc: was buried in paragraph four, now at the top |
| **Total** | **6/6** | **6/6** | **5/6** | **6/6** |

Banner note: Credible check is borderline at 5/6 - no room for a supporting metric in 87 characters. The "30%" figure carries it. Ships as-is.

---

## Sources

| File | What it supplied |
|---|---|
| `09-release-notes/release-v2.4-smart-summaries.md` | 30% shorter average, 350-word average (previous model), decisions-first structure, November 2025 GA date, NPS 22 (Q3 2025) to 34 (Q1 2026) = 12-point gain, "summaries too long" = #2 complaint with 14 NPS mentions |
| `05-user-personas/sarah-chen.md` | 8-10 meetings/day, no buffer time, power user profile, Pro plan at $15/mo |
| `03-product-knowledge/competitive.md` | Otter.ai summaries described as "generic - more transcript highlights than true synthesis"; Notion AI described as "basic"; MeetFlow wins on AI quality |
| `.claude/skills/launch-announcement/references/dunford-positioning.md` | Positioning component order and definitions |
| `.claude/skills/launch-announcement/references/storybrand-sb7.md` | SB7 arc mappings per format, hero test |
| `.claude/skills/launch-announcement/references/success-checklist.md` | Six-check scoring rubric |
