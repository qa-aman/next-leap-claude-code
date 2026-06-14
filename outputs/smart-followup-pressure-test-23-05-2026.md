# Smart Follow-Up PRD - Pressure Test

**Date:** 23-05-2026
**PRD under review:** `08-product-features/01-smart-follow-up/prd-smart-follow-ups.md`
**Method:** Three-role adversarial debate (Engineering Lead, Design, Sales/GTM), two rounds, lead synthesis.
**Reviewed by:** AI Intelligence PM (lead)

---

## Lead summary

The PRD is well-structured and already absorbed a prior pressure test - scope cuts, confidence vocabulary, rollout phasing, and dependency gates are all documented. The debate did not find weak thinking. It found a single missing thing that every role circled independently from a different direction:

**There is no defined send architecture.** No outbox, no cancel window, no recipient-resolution service, no partial-send idempotency. The PRD says "no auto-send, every draft requires approval" and treats that as the safety story. All three roles agree it is a slogan, not a safeguard. The moment an email leaves a user's account, none of the trust mechanisms in this PRD apply, and a wrong send is unrecoverable.

That gap is the spine of the five issues below.

---

## Top 5 issues to fix before the eng walkthrough

### 1. Define the send path: outbox + cancel window, not "no auto-send"
All three roles converged here. Eng: the 48h rollback is useless for external sends - bad emails are already gone. Design: there is no undo after send; real email recall is impossible once SMTP/Slack/Notion accept the payload. Sales: "every email reviewed, confirmed, recoverable" is a *differentiator* versus Fireflies' fire-and-forget, worth the friction.

The fix all three landed on independently: a hold-and-release outbox (queue the send, hold 30-60s, visible cancel, like Gmail Undo Send but longer). It is invisible until needed, so it satisfies Eng's safety and Sales' polish without the modal friction. Replace the "undo" fantasy with this. Medium eng cost, highest leverage item in the review.

### 2. Recipient resolution is an unscoped backend service, and it is a launch blocker
Design flagged it; Eng owned it as the biggest hole in the spec. The PRD shows "sent to: [recipients]" with zero detail on how recipients are determined, how a user fixes a wrong recipient, or what happens when 14 attendees should resolve to 3. This is identity mapping across Zoom/Meet/Teams attendee lists with inconsistent email fields - multiple eng weeks, not a screen. A wrong-recipient send is worse than any partial-send failure and it is currently undesigned and unsized.

### 3. "Ready" is a trust promise the model can't keep at GA
Sales and Design compound on the same point. GA is April; the 80% accuracy target is end of Q2; the model runs at ~66% today. "Ready" = confidence ≥70%, auto-included, and collapsed to a one-line preview - which Design argues trains approve-without-review. So the worst case is a flow that auto-collapses a confidently-wrong item and sends it from the customer's own account. Either hold the auto-include/collapse behaviour until accuracy catches up, apply asymmetric friction (frictionless for Priya's casual/Slack path, a real review gate on Ready items going to external email), or rename "Ready" to something the 66% system can honestly claim pre-Q2.

### 4. The review screen is built for one draft; the power user has an inbox
Eng and Design name the same wound. Sarah runs 8-10 meetings/day at 5-8 items each = 50-80 review actions, across 10 separate draft screens. The "under 2 min per meeting" target measures the wrong thing - the real problem is queue management, not per-draft speed. The fix is a consolidated, batched end-of-day review surface, not a faster single screen. This is also where the 30%-of-Pro-weekly adoption metric quietly dies: the power users most likely to evangelize churn the fastest if the flow doesn't scale to their volume.

### 5. Three unowned/unsized dependencies sit on the trust-critical path
- **Feedback-loop privacy review** has no owner, no date, no defined legal question - and "we train on your meeting content" with no audit trail is exactly the objection that loses the three enterprise pilots permanently (Marcus's persona objection is already in the room). Get an owner this week or scope the feedback loop out of Team beta.
- **Partial-send idempotency** (Slack succeeds, Notion 429s) is unspecified. A half-sent follow-up is worse than none.
- **The third vocabulary.** Poor-audio handling introduces "Suggested," contradicting the "one vocabulary everywhere" promise. Collapsing it into the existing two labels is near-free copy work; the sub-80% transcript-quality branch it rides on is real conditional logic in the draft pipeline that the timeline doesn't account for.

---

## 3 questions I need answered before the meeting

1. **What is the per-draft inference cost and the queue behaviour at peak?** Per-meeting LLM generation across 2,800 Pro users at 8-10 meetings/day is real COGS and a margin question, not just a latency one. If 500 users end a Friday standup in the same 10-minute window, does the 120s p95 hold? Until this is modelled, the 5/month Free cap reads as a cost-control band-aid rather than a funnel decision, and "unlimited drafts" as a Pro selling point may be unpriced.

2. **If Scoring v2 slips past the 25-03-2026 labeling gate, what is the fallback - degraded mode, or does April GA slip entirely?** There is no degraded-mode plan. The whole feature collapses without Scoring v2, and the new gap areas (implicit, multi-person, conditional items) are the hardest data to label. I need the decision rule in advance, not on 26-03.

3. **What is the April commercial story for the three enterprise pilots and for churning Pro customers?** The pilots are scoped out until June, accuracy is below target at GA, and there is no Salesforce sync. What do reps sell in April to keep the pilots warm for 10 weeks, and what do we tell a Pro customer churning on action-item accuracy *now*? (Sales' lean: sell governance and control - the send-pause, recipient confirm, and recoverability from issue #1 - as the differentiator, not raw drafting.)

---

## 1 thing that's strong and should stay

**The phased, feature-flagged rollout with gates and a defined rollback trigger.** Internal dogfood → top-10% Pro → all paid (excl. enterprise) → Free → enterprise, each with an explicit go/no-go gate, is exactly right for an ML change that touches every user's action items. No role argued against the structure. The only fix is the rollback *trigger* (issue #1): 48 hours is too slow for external sends, but the staged-gate framework around it is sound and should not be touched.

---

## Disagreement worth noting

Sales explicitly pushed back on Design's WCAG concern as an April priority: AA contrast, focus order, and keyboard nav matter for enterprise procurement later but won't lose an SMB/Pro deal in April, and shouldn't eat sprint capacity that belongs to the send-pause and recipient confirm. Lead call: fix the color-only "yellow" flag and screen-reader announcement now (cheap, and they ride the same components as issue #3), defer the broader AA audit to the enterprise track. Document it as a deliberate deferral, not an oversight.
