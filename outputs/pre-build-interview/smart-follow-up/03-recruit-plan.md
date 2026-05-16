# Recruit Plan - Smart Follow-Up

**Date:** 17-03-2026
**Target N:** 10 interviews
**Recruit window:** 18-03-2026 to 24-03-2026
**Interview window:** 25-03-2026 to 03-04-2026 (must complete before beta starts in early April)

---

## Segment

MeetFlow Pro users who run 5 or more recurring meetings per week and use MeetFlow's auto-extracted action items as their primary or backup task list.

Approximate population: 280 users (top 10% of 2,800 Pro accounts by meeting volume). Same population as Phase 2 of the rollout in the PRD, which means recruiting here doubles as priming the beta cohort.

## Source

**Primary (target 7 of 10):** existing Pro users sourced from the MeetFlow product database, filtered by:
- Pro tier
- 20+ meetings recorded in the last 30 days
- 5+ action items reviewed (any edit, dismiss, confirm) in the last 30 days
- Has NOT churned or downgraded in the last 90 days

**Secondary (target 2 of 10):** NPS detractors from the Q1 2026 feedback survey (`06-user-feedback/feedback-q1-2026.md`) who mentioned action items. These users have the strongest stated pain and are most likely to surface anxiety signals.

**Tertiary (target 1 of 10):** one user from outside the bullseye - a Pro user with low meeting volume (under 5 per week) - as a contrast case. If this user has the same pain, the segment may be wider than we think. If not, that confirms our targeting.

## Screener questions

Sent via email before scheduling. 3 questions max.

1. "In a typical week, roughly how many work meetings do you have?" (Disqualify under 5.)
2. "After your meetings, do you usually send any kind of follow-up - email, Slack message, or shared note - to attendees?" (Disqualify "rarely" or "never".)
3. "When you send a follow-up, where do action items usually come from?"
   a. I write them from memory or scratch notes
   b. I copy them from MeetFlow's auto-extracted list
   c. I use MeetFlow's list but rewrite or correct it first
   d. Other
   (Target: c. Acceptable: b. Disqualify: a or d only.)

## Disqualifiers

- MeetFlow employees (already saturated with internal opinions).
- Users who joined in the last 30 days (not enough behavioral history).
- Users in the active Action Item Scoring v2 internal dogfood group (different prompt set required, do separately).
- Free users (different segment, separate validation if needed).

## Incentive

$75 Amazon gift card per completed 45-minute interview. Higher than the typical $50 because Pro power users have high opportunity cost and we need a fast turnaround.

## Outreach template

Subject: *Quick research request - 45 min, $75 gift card*

Body keeps it short and behavior-focused, never mentions Smart Follow-Up or any specific feature. Frame: "we're talking to power users about how you handle your meetings end-to-end."

## Owner

AI Intelligence PM owns recruit. Coordinate with the Core Experience PM (Aisha) on the user database filter so we do not double-book users already in her Transcript Accuracy v2 research queue.

## Risks to the recruit

- **Survivor bias.** All 10 are current Pro users, so we miss the "tried MeetFlow, churned because of action items" segment. Mitigation: pull 2 of 10 from churned-then-returned users if possible, otherwise note this gap explicitly in the decision doc.
- **Selection bias toward complainers.** The 2 NPS detractor recruits may over-rotate the sample toward pain. Track this in synthesis - if push signal comes mostly from those 2, weight accordingly.
- **Timeline pressure.** Beta starts early April. If we hit fewer than 8 completed interviews by 03-04-2026, we present a partial-data decision doc with confidence interval explicitly stated, rather than delay the sprint.
