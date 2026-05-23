# Smart Follow-Up PRD - Pressure Test

**Date:** 23-05-2026
**PRD reviewed:** `08-product-features/01-smart-follow-up/prd-smart-follow-ups.md`
**Format:** Three-role debate (Engineering Lead, Design, Sales/GTM), two rounds, then lead synthesis.

---

## Round 1

### Engineering Lead

1. **The April timeline is a fiction.** Scoring v2 ships March, beta early April, GA April. But the PRD lists labeling for implicit/multi-person/conditional items as "must be confirmed" before Scoring v2 development starts. If labeling hasn't started, we haven't started Scoring v2.
2. **Four integrations in one release is reckless.** Slack, Notion, Jira, Linear means four API contracts, four auth flows, four rate limits, four breakage surfaces. The PRD treats this as a bullet, not a project.
3. **p95 <120s latency has no infra backing.** No compute budget, no worker pool sizing, no plan for end-of-business burst when half the company's meetings end simultaneously.
4. **The monthly 200-meeting labeled audit is uncosted.** It's the "source of truth" for the 80% accuracy target with zero ownership or tooling discussion. The ML team is also building Scoring v2.
5. **Phase gates have no escalation path.** Rollback triggers are defined; "slow lane" is not. Phase 2 could stall indefinitely with no decision framework.
6. **Regression detection is too noisy.** 48h v1-baseline drop fires on normal user-preference variance. We won't be able to tell a real model regression from Sarah dismissing more aggressively.
7. **Privacy review with Tomas is unblocked.** Flagged as a to-do with no date, no escalation, no fallback if he restricts Team-tier logging.

**One-line take:** This PRD describes a Q3 feature dressed up as an April launch, built on a dependency that isn't started yet, with four integrations and a permanent ops commitment that nobody has been assigned.

### Design

1. **Hidden high-confidence items are a trust bomb.** Sarah's persona explicitly says "confidence scores say high but critical items still get missed." Hiding those from her review screen guarantees she'll send a wrong item and blame MeetFlow.
2. **The 2-minute review target is a number, not a designed flow.** No interaction model, no count of taps per item, no definition of what "approve all" covers.
3. **Three confidence UI models, zero consistency.** "85%" in review, colored dot in Slack, "Suggested/Confirmed" in Jira/Linear. A user across all three channels builds three mental models.
4. **Color-only confidence fails WCAG 1.4.1 Level A.** 8% of men have CVD. Screen readers can't read a colored dot. Zero accessibility content in the PRD.
5. **Zero-state and full-collapse cases unspecified.** Zero items? All items low-confidence? User dismisses everything? Meeting they didn't actually attend? No designed states.
6. **Marcus has no pre-send visibility.** For a privacy-focused engineer at a fintech, "what data leaves and where to" is table stakes, not Enterprise-tier polish.
7. **"Suggested" in Jira/Linear confuses assignees.** A status label exported into a system MeetFlow doesn't own - the downstream assignee has no context for what it means.

**One-line take:** This PRD solves the accuracy problem for the model, but not the trust problem for the user - and those are different things.

### Sales / GTM

1. **Value prop is invisible in a 20-min demo.** "AI-drafted follow-ups" is what Fireflies, Otter, and Granola already say. No crisp differentiated one-liner.
2. **The Free-to-Pro wedge is a confidence score nobody asked for.** A technical artifact behind a paywall isn't a tested conversion driver.
3. **Three enterprise pilots will demand an audit trail.** PRD defers audit logging to June. We're shipping AI-drafted business comms with no enterprise logging six weeks before Enterprise GA.
4. **Notion AI undercuts top-of-funnel.** Casual users like Priya can compare free Notion AI to a $15/mo paywall with a draft cap.
5. **Salesforce exclusion closes deals.** Per `competitive.md`, Fireflies' Salesforce integration is the #1 reason prospects consider switching away from us.
6. **Accuracy dependency is unsellable.** I can't build a sales motion around a feature whose ML dependency has no locked timeline.
7. **Metrics don't connect to the business case.** Adoption and draft-acceptance targets, no conversion/churn/ARR commitment. Company.md says churn is 4.1% monthly and conversion is 6.2%. PRD doesn't claim it'll move either.

**One-line take:** I can't sell a feature whose differentiation lives inside a confidence score, ships without audit logs for the buyers we're trying to close, and explicitly excludes the integration that costs us the most deals.

---

## Round 2 (cross-reactions)

### Engineering Lead - reacting

- **Design is right on three confidence UIs - and it's worse than they think.** Format inconsistency makes my regression-detection signal garbage. We can't separate "model got worse" from "user got confused by the format." Ship one representation, even a mediocre one.
- **Sales is right about the enterprise audit trail - and they buried the real risk.** If those three pilots run on April code without audit, we're accumulating compliance liability across Slack/Notion/Jira/Linear, not revenue. Audit trail is a hard dependency for any enterprise account, not a June enhancement.
- **Design's zero-state isn't engineering's problem to absorb.** Early models on new meeting types will produce zero-confidence outputs regularly. A blank screen or silent suppression IS the trust collapse Design called out in Sarah's persona. Needs designed paths.
- **New eng risk: four OAuth flows under one release.** One auth regression blocks every integration. No circuit-breaker design in the PRD.
- **New eng risk: Marcus privacy gap is now a compliance gap.** Pushing action items to third-party tools without informing attendees may violate their employers' DPAs. Legal review, not a settings toggle.

**Where I net out:** No eng walkthrough until (a) the confidence UI is collapsed to one representation, (b) enterprise audit trail moves into April scope OR pilot accounts are explicitly scoped out, and (c) legal signs off on the multi-party data push model.

### Design - reacting

- **Eng's four-integration concern detonates my confidence-UI problem.** If Salesforce gets pulled in under sales pressure, we'll have four different visual languages for the same concept. Power users live across all four channels - that's confusion baked into the architecture.
- **Sales' demo story is the same wound as my pre-send visibility gap.** The review screen is doing two jobs - trust-building for Marcus and "wow" moment for sales demos - and is designed as neither.
- **Eng's regression-noise problem traps design too.** If confirm/dismiss is unreliable as an accuracy signal, the UI gives users no way to tell when the model degraded vs. their meetings got messier. Trust collapse waiting for a trigger.
- **New design objection: batch "approve all" is the real danger.** Sarah rubber-stamps drafts that hide high-confidence items. When one is wrong, she won't remember approving it. Optimizing speed at the cost of perceived accountability.
- **New design objection: Free zero-confidence-score state is a conversion anti-pattern.** Free users get drafts with no signal to check items. They edit, get frustrated, churn. That's Sales' wedge problem expressed as a UX failure - hiding the value signal from the users we're trying to convert.

**Where I net out:** One confidence vocabulary, decided before any integration is scoped. The review screen needs a defined primary job - trust OR conversion, not both. Approve-all needs a confirm step or post-send undo window before I sign off.

### Sales - reacting

- **Eng's "Scoring v2 hasn't started" point makes April a lie I'm currently telling prospects.** Three pilots are anchored to Q2. If we slip, I don't just lose timing - I lose credibility. These buyers talk.
- **Eng's four-integration risk is a live demo failure mode.** A prospect demos this to their exec, the Jira export fails, and I have no answer. Day-one stability across four channels is non-negotiable.
- **Design's "Suggested in Jira" is the one that keeps me up.** A buyer's engineering team files it as a MeetFlow bug. I re-explain the confidence model in a support ticket instead of having a renewal conversation. Must resolve before any Jira-facing release.
- **WCAG failure is a procurement blocker, not a nice-to-have.** Any enterprise buyer with a procurement accessibility checklist kills this quietly.
- **New commercial risk: the "launch floor" problem.** If Scoring v2 isn't ready, the confidence UI ships without the underlying model improvement. I'm demoing something that looks more accurate without being more accurate. That's a trust cliff, not a slow burn.
- **New commercial risk: Marcus visibility gap = silent enterprise deal-killer.** Enterprise procurement will ask what data leaves their environment via Jira/Slack export. If we can't answer, deal dies quietly.
- **Push back on perfectionism:** Don't gate launch on every edge-case state. Ship the 80% case, document the rest as v1.1. Don't let rollout-escalation discipline gate the commercial release.

**Where I net out:** Confirmed Scoring v2 ship date before any April promise to a pilot. Resolve the Jira "Suggested" label and the Marcus data-visibility gap before any enterprise demo. Everything else I can manage with staged rollout and honest expectation-setting - those three are hard stops.

---

## Lead Synthesis

### Top 5 issues to fix before the eng walkthrough

1. **Collapse the confidence UI to ONE vocabulary across channels.** Three representations (percentage in review, color dots in Slack, "Suggested/Confirmed" in Jira/Linear) creates four downstream problems at once - user confusion, regression-signal noise, accessibility failure, and assignee confusion in Jira. Decide one model, then express it consistently per channel. This is the single change that unlocks the most other risks.
2. **Lock the Scoring v2 critical path before committing to April.** Confirm labeling scope/volume/timeline for implicit, multi-person, and conditional items. If labeling isn't started, April GA is not real - get a defensible date before the walkthrough so eng isn't sandbagged on commitments built on a guess.
3. **Address the enterprise audit trail decision now, not in June.** Either (a) pull audit logging into April scope or (b) explicitly scope enterprise pilot accounts OUT of the April rollout. The current PRD shipping AI-drafted business comms to three pilots without audit trails is a compliance and sales-credibility problem masquerading as a scope deferral.
4. **Spec the review screen as a designed flow, not a 2-minute target.** Define what "approve all" covers, what's shown vs. hidden, what the user sees when zero items reach threshold, what Marcus sees about outbound data before sending. The review screen is the trust moment AND the demo moment; right now it's designed as neither.
5. **Cut integration scope from four to two for launch.** Slack + Notion OR Slack + Jira. Pick the two that map to the highest-leverage user segments and ship those well. Adding the others as fast-followers protects launch quality and gives sales a clean second beat instead of a hedge.

### Three questions I need answered before the meeting

1. **What is the confirmed start and end date for Scoring v2 labeling work, and which ML resource owns the monthly 200-meeting audit?** Without these two answers, the rest of the roadmap is fiction.
2. **What is Tomás's actual position on (a) enterprise pilots in the April rollout and (b) Team-tier training data logging?** If either is restricted, the rollout plan changes materially - we need to know before the walkthrough, not after.
3. **What's the sales-tested one-liner that differentiates Smart Follow-Up from Fireflies/Otter/Granola/Notion AI?** If we can't say it in one sentence, we don't have a value prop - we have a feature. This should come from a real conversation with the sales team and 2-3 prospects, not from PM intuition.

### One thing in the PRD that's strong and should stay

**The dual-track accuracy measurement** (confirm/dismiss ratio as a real-time proxy, plus a monthly labeled audit of 200 meetings as the source of truth). This is the right instinct - separating a fast lossy signal from a slow trustworthy one. Even though eng is right that the audit work needs an owner and the confirm/dismiss baseline needs sharpening, the structure itself is correct and should survive every other revision.