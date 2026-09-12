# PRD: Action Item Confidence Scoring v2

## Status

Already in development. This is the active sprint, 17-03-2026 to 28-03-2026. Smart Follow-Up, which depends on this work, ships April 2026 (`04-strategy/product-vision.md`). This PRD documents the sprint in flight, it is not a proposal to start it.

## 1. Problem

Action item accuracy is 66%, meaning 34% are wrong or missing, named as the top complaint driving churn (`03-product-knowledge/company.md`). Sarah Chen: "I double-check the action items manually. Which defeats the purpose." (`07-user-interviews/interview-01-sarah-chen.md`). James Whitfield: "Maybe 1 in 3 calls has an action item that's wrong enough to matter. For sales, wrong follow-up is worse than no follow-up." (`07-user-interviews/interview-04-james-whitfield.md`).

## 2. Target User

Sarah Chen, the power user persona (`05-user-personas/sarah-chen.md`). She uses AI-generated action items as her primary task list and has an 8-seat Team plan upgrade held pending accuracy. Marcus Okafor and Priya Nair are not the fit here, their pain points center on data control and pricing, not action item trust.

## 3. Solution

- Every action item ships with a confidence score, so users know at a glance which ones to trust and which to verify.
- Confidence scores are reliable, not just present. Sarah's core complaint is that scores already say "high" while critical items still get missed, so v2's job is to close that gap, not add a new label.
- Low-confidence items are flagged distinctly, so a user scanning at end of day can triage instead of re-reading every item.
- The scoring feeds directly into Smart Follow-Up (April 2026), which closes the action item loop by turning confirmed items into sendable follow-ups.
- Fewer false "high confidence" labels, which is the specific ask Sarah names as what would make her happy.

## 4. Success Metric

Action item accuracy (correct and complete). Baseline 66% (`03-product-knowledge/company.md`, `04-strategy/product-vision.md`). Target 80% (`04-strategy/okrs-q2-2026.md`, Objective 1, Q2 2026).

## 5. Risks

1. Trust is eroding, not just accuracy. Sarah's churn risk note says if accuracy doesn't improve she stops advocating internally and the team upgrade never happens (`05-user-personas/sarah-chen.md`). A better score that doesn't change actual reliability won't move this.
2. Smart Follow-Up ships April 2026 and depends on this scoring being trustworthy first. If v2 doesn't hold, Follow-Up launches on an unreliable base.
3. Granola is gaining fast among prosumer power users with a more polished native experience (`03-product-knowledge/company.md`). Sarah is exactly that segment, if accuracy stays weak she has a credible alternative.

## 6. Out of Scope

1. Smart Follow-Up itself, that is a separate feature shipping April 2026.
2. Transcription accuracy in noisy environments, that is Transcript Accuracy v2, shipping June 2026.
3. Salesforce integration and any CRM-linked follow-up routing, that is Dana Rivera's May 2026 scope.
