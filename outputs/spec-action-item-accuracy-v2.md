# Action Item Confidence Scoring v2 - Feature Spec

**Author:** Aman Parmar (PM, AI Intelligence)
**Date:** 2026-03-21
**Status:** Draft

---

## Problem

MeetFlow's action item extraction is wrong or missing 34% of the time (Source: `03-product-knowledge/product.md`). This is the #1 complaint in the Q1 2026 NPS survey with 19 mentions out of 47 respondents (Source: `06-user-feedback/feedback-q1-2026.md`). Power users who rely on action items as their task system - the highest-value segment - are losing trust in the product. This accuracy gap blocks Team plan upsells, drives Pro churn at 4.1% monthly, and undermines every downstream feature (Smart Follow-Up, integrations) that depends on reliable action items.

---

## Users Affected

- **Sarah Chen (Head of Product)** - Runs 8-10 meetings/day, uses action items as her primary task list. Catches 2-3 errors daily, spends 30 min correcting on heavy days. Has 8 Team seats ($4,700/yr) ready to buy but blocked by accuracy. See `05-user-personas/sarah-chen.md`.
- **James Whitfield (Sales Director)** - Uses action items as follow-up prompts after prospect calls. Wrong action items make his reps look unprofessional. Reports 1 in 3 calls has a meaningful error. 22-seat Team account ($12,936/yr) evaluating Fireflies. See `07-user-interviews/interview-04-james-whitfield.md`.
- **Priya Nair (Chief of Staff)** - Casual user who skims action items in Slack digests. Lower direct impact, but accuracy improvements increase the value of the digest she already loves. See `05-user-personas/priya-nair.md`.
- Estimated impact: All 2,800 Pro users and 200 Team seats. Power users (estimated top 20%) feel this most acutely. (Source: `03-product-knowledge/company.md`)

---

## Proposed Solution

Upgrade the action item extraction model and confidence scoring system so users can trust what MeetFlow captures without manual review.

**Key interactions:**
- After a meeting ends, MeetFlow extracts action items and assigns each a visible confidence score (percentage, not just high/medium/low).
- Items below a configurable confidence threshold are flagged as "Suggested" - shown visually distinct so users know to review them.
- Users confirm, edit, or dismiss suggested items with one click. This feedback feeds back into the model.
- Implicit commitments ("I'll circle back on that"), multi-person items, and conditional actions ("if design approves, we'll ship it") are now captured as action items with appropriate confidence levels.
- Confidence scores surface prominently in the summary view, Slack digest, and integration exports - not buried in a tooltip.

**Boundaries:**
- This is an extraction and scoring improvement. No changes to the summary generation system, transcription pipeline, or integration layer.
- The user-facing experience stays within existing UI surfaces (summary view, Slack digest, Notion/Jira export). No new pages or navigation.
- User feedback (confirm/dismiss) is the retraining signal. No separate annotation workflow.

**Rabbit holes to avoid:**
- Don't rebuild the entire action item model from scratch. Fine-tune the existing model (trained on 50K labeled meetings) with targeted improvements for the three known gap areas.
- Don't attempt real-time confidence scoring during the meeting. Score after the meeting ends, same as today.
- Don't try to auto-assign action items to people outside the meeting. Assignee detection stays within meeting participants.
- Don't block on the manual model retraining pipeline fix (documented tech debt). Ship v2 with the current 2-week deployment cycle, address pipeline automation separately.

---

## Functional Requirements

**Happy path:**
1. Meeting ends. Transcription completes. Action item extraction runs with the v2 model.
2. Each action item shows: description, assignee (if detected), confidence score (0-100%), and source timestamp (link to transcript moment).
3. Items at or above the confidence threshold (default: 70%) appear as confirmed action items.
4. Items below threshold appear in a "Suggested Items" section, visually flagged for review.
5. User clicks confirm (promotes to confirmed), edit (opens inline editor), or dismiss (removes with a reason tag: "not an action item" / "duplicate" / "wrong assignee").
6. Confirmed and user-edited items flow to integrations (Slack, Notion, Jira, Linear) as they do today.
7. Dismiss/confirm actions are logged as training data for model improvement.

**Error states:**
8. If the extraction model fails or times out, show the raw transcript with a message: "Action items are taking longer than usual. We'll notify you when they're ready." Retry automatically once.
9. If no action items are detected in a meeting, show: "No action items detected. Review the transcript to add any manually."

**Edge cases:**
10. Meetings with 8+ attendees: speaker diarization issues may cause wrong assignee detection. Flag assignee confidence separately from item confidence. If speaker attribution is low-confidence, show "Assignee: unconfirmed" rather than guessing wrong.
11. Very short meetings (under 5 minutes): skip the "Suggested Items" section to avoid noise. Only show high-confidence items.
12. Back-to-back meetings: ensure action items from meeting N are finalized before meeting N+1 starts processing. No cross-contamination.

---

## Non-Functional Requirements

- **Latency:** Action item extraction + scoring must complete within 90 seconds of meeting end (current baseline: 45-90 seconds for summary generation per `03-product-knowledge/product.md`). Scoring adds no more than 15 seconds.
- **Accuracy target:** 80% action item accuracy (correct and complete), up from 66% baseline (Source: `04-strategy/okrs-q2-2026.md`, Objective 1).
- **Feedback loop:** User confirm/dismiss data must be available to the ML team within 24 hours for batch retraining analysis.

---

## Success Metrics

- Action item accuracy (correct and complete): target 80% (baseline: 66%, Source: `04-strategy/okrs-q2-2026.md`)
- Pro monthly churn rate: target 2.5% (baseline: 4.1%, Source: `04-strategy/okrs-q2-2026.md`)
- NPS: target 45 (baseline: 34, Source: `06-user-feedback/feedback-q1-2026.md`)
- Support tickets about missing/wrong action items: reduce by 25% vs Q1 2026 baseline (Source: `08-product-features/prd-smart-follow-ups.md`)

Cross-reference: `04-strategy/okrs-q2-2026.md` - this feature directly drives Objective 1 (Make AI output reliable enough to trust) and Objective 3 (Stop Pro users from leaving).

---

## Out of Scope

- Smart Follow-Up email drafting - ships separately in April 2026, depends on this feature
- Summary length optimization - separate initiative, different model
- Salesforce integration for action items - Dana's scope, Q2 2026
- Multi-language action item extraction - English only
- Real-time action item detection during live meetings
- Automated model retraining pipeline - tech debt item, tracked separately
- Custom confidence thresholds per user - v1 uses a fixed default (70%), user configurability deferred

---

## Open Questions

| # | Question | Owner | Due |
|---|----------|-------|-----|
| 1 | What confidence threshold (default 70%) maximizes the tradeoff between false negatives (missed items) and noise (too many suggestions)? Needs A/B testing or analysis of the 50K training set. | ML Lead | 2026-04-01 |
| 2 | Should suggested items be included in Slack digest and integration exports, or only confirmed items? Including them adds noise, excluding them loses the review prompt for users who only check Slack. | Aman Parmar | 2026-03-28 |
| 3 | How do we measure "accuracy" in production? The 66% baseline came from a labeled audit. Do we need a recurring audit cadence, or can user confirm/dismiss rates serve as a proxy? | ML Lead + Aman | 2026-04-01 |
| 4 | Does the 2-week model deployment cycle create an unacceptable delay for incorporating user feedback? If so, this may force pipeline automation to be a dependency rather than a separate track. | Eng Lead | 2026-03-28 |

---

## Assets

- Existing model documentation: `03-product-knowledge/product.md` (AI Intelligence Pillar section)
- Smart Follow-Up PRD (downstream dependency): `08-product-features/prd-smart-follow-ups.md`
- User interview evidence: `07-user-interviews/interview-01-sarah-chen.md`, `07-user-interviews/interview-04-james-whitfield.md`
- Q1 2026 NPS data: `06-user-feedback/feedback-q1-2026.md`
- Q2 OKR targets: `04-strategy/okrs-q2-2026.md`
