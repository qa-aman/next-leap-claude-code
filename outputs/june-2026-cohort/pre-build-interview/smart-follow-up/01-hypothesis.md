# Hypothesis - Smart Follow-Up

**Date:** 17-03-2026
**Owner:** AI Intelligence PM
**Sprint anchor:** Active sprint 17-03-2026 to 28-03-2026, beta target early April 2026

---

## Feature in one sentence

After every meeting, MeetFlow drafts a follow-up email with confidence-scored action items that the user reviews in under 2 minutes and sends via email, Slack, Notion, or Jira/Linear.

## Target user segment

**MeetFlow Pro users who run 5+ recurring meetings per week and currently rely on MeetFlow's auto-extracted action items as their primary task list.**

This is the Sarah Chen segment (`05-user-personas/sarah-chen.md`). Roughly 280 of 2,800 Pro users (top 10% by meeting volume), per the rollout plan in the PRD. They are the population most burned by the 34% action item error rate and the ones who would benefit most from a draft-and-send loop.

Out of scope for this validation: Free users (will get a stripped version), Team admins (different buyer, validated separately by Tomas), and Priya Nair's "casual digest forwarder" segment (low pain, low signal).

## Problem we believe they have

After a meeting, they spend significant time manually rewriting MeetFlow's action items into emails, Notion pages, and Jira tickets before sending follow-ups, because they cannot trust what MeetFlow extracted.

## Current workaround

They open the MeetFlow summary, read it line by line, cross-reference their own scratch notes from the meeting, rewrite the action items into a new draft (email or Notion), and only then send it.

Source: Q1 2026 feedback - "I still have to go back and check every single one" (`06-user-feedback/feedback-q1-2026.md`, 19 of 19 NPS-detractor mentions cited action item accuracy).

## Why the workaround is painful

- **Frequency:** every meeting, multiple times per day.
- **Severity:** Sarah Chen persona describes 30 to 45 minutes per evening spent on manual correction (`05-user-personas/sarah-chen.md`).
- **Cost:** trust erosion. "The more this happens the less I trust the AI." Some users have stopped using auto-extracted items entirely and revert to manual notes, which deletes the product's core value.
- **Business cost:** Pro churn at 4.1% monthly (`03-product-knowledge/company.md`). Action item accuracy is the single largest factor in NPS detractor responses.

## What we would build if confirmed

The Smart Follow-Up feature as scoped in `08-product-features/01-smart-follow-up/prd-smart-follow-ups.md`: draft email + confidence-scored action items + review screen + multi-channel send. Plus the Action Item Scoring v2 dependency.

## Signal thresholds

Across 10 interviews (target):

| Signal | Threshold | Why this number |
|---|---|---|
| Describe the problem unprompted in first 10 min | 7 of 10 | Q1 2026 feedback already shows strong baseline pain. If we cannot replicate in interviews, the survey data is being misread. |
| Describe an active workaround they do today | 8 of 10 | If most do not have a workaround, they have stopped caring about the problem. KILL signal. |
| Describe the workaround as painful (their words: "waste", "kill", "hate", "every single one") | 6 of 10 | Strong emotional language is the leading indicator of switching. |
| Show their workaround on the call (commitment rung 2) | 5 of 10 | Behavioral proof beats stated opinion. |
| Probe reveals Push + Pull > Anxiety + Habit | 6 of 10 | The most important threshold. Predicts adoption, not just stated preference. |

## Kill criteria

We walk away from Smart Follow-Up as currently scoped if any of these are true after 10 interviews:

- Fewer than 7 describe the problem unprompted (the survey signal does not hold up to live probing).
- Most describe the current workaround as "fine" or "manageable" (habit dominates, feature will be ignored).
- Anxiety about AI accuracy is so high that users say they would not trust a draft regardless of confidence scoring (Action Item Scoring v2 is not enough on its own; we have a deeper trust problem).
- Push + Pull does not exceed Anxiety + Habit for at least 6 of 10 (forces predict non-adoption).

If kill criteria are hit, the recommendation will be ITERATE on the trust mechanism (different surfacing of confidence, manual-first mode, side-by-side compare) rather than abandon the problem.

## Open assumptions going in (to test in interviews)

1. Users want to send the follow-up email themselves vs. delegate to a colleague. (Sarah does it herself. Confirm.)
2. Users will trust a confidence score enough to skip manual review on high-confidence items. (Untested. This is the highest-risk assumption.)
3. The bottleneck is action item correctness, not summary quality or transcript accuracy.
4. Multi-channel export (Slack, Notion, Jira) is essential, not nice-to-have. (Sarah uses Notion. Validate for the rest.)
5. The 2-minute review-and-send target is achievable for users with 8-10 daily meetings.
