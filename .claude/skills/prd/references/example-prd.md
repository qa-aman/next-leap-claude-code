# PRD - Smart Follow-Up Emails

**Pillar:** AI Intelligence
**Owner:** AI Intelligence PM
**Target:** April 2026
**Status:** Draft

---

## Problem

34% of action items MeetFlow extracts are wrong or missing. That means nearly 1 in 3 tasks from a meeting is lost or incorrect before a follow-up email is even drafted. Users who depend on meeting summaries to drive accountability get burned. The top complaint in the Q1 2026 survey is action items (19 of 19 mentions). NPS is 34 - below industry average. Fixing follow-up accuracy is the clearest path to improving it.

Cross-reference: `03-product-knowledge/product.md` for full feature context.

---

## Who It's For

Three personas drive this feature. Each has different needs.

- **Sarah Chen** - Head of Product. Runs 8-10 meetings per day. Needs fast, accurate follow-ups she can send without re-reading full transcripts. See `05-user-personas/sarah-chen.md`.
- **Marcus Okafor** - Engineering Manager. Privacy-focused. He will not use features that send data outside his control without explicit review. See `05-user-personas/marcus-okafor.md`.
- **Priya Nair** - Chief of Staff. Casual MeetFlow user. Loves the Slack digest. Values low-friction output she can forward or copy. See `05-user-personas/priya-nair.md`.

---

## What It Does

- Drafts a follow-up email after each meeting. Uses the summary and extracted action items.
- Shows a review screen before anything is sent. You edit, delete, or approve.
- Tags each action item as **Ready** or **Needs review**. One label, used everywhere (see "Confidence vocabulary" below).
- Lets you send directly from MeetFlow or copy the draft to your email client.
- Integrates with Slack and Notion at launch. Jira and Linear ship as fast-followers in May 2026.

### Why integration scope was cut

Original draft included Slack, Notion, Jira, and Linear at launch. Four integrations in one release was flagged as a quality and demo-stability risk in the 23-05-2026 pressure test (`outputs/smart-followup-pressure-test-23-05-2026.md`). Slack and Notion cover the highest-volume export channels per Q1 2026 feedback. Jira and Linear move to a May 2026 fast-follow.

---

## Plan Availability

- **Free:** Follow-up drafts generated, no confidence scores. Max 5 drafts per month.
- **Pro:** Full feature. Confidence scores, unlimited drafts, all export channels.
- **Team:** Full feature plus team-wide follow-up analytics (sent rate, edit rate by team).

Source: Aligns with current tier structure in `03-product-knowledge/product.md`.

---

## How It Works

Step-by-step user flow:

1. Your meeting ends. MeetFlow generates a summary (avg 350 words for a 30-min meeting).
2. Action Item Scoring v2 runs. Each item gets a confidence score.
3. MeetFlow surfaces a "Draft Follow-Up" prompt in the dashboard or Slack digest.
4. You open the draft. You see the subject line, a short summary, and a bulleted action item list.
5. Low-confidence items are flagged (shown in yellow). You review and edit as needed.
6. You choose: send via email, post to Slack, or export to Notion/Jira/Linear.
7. Sent. A confirmation log is saved to your meeting record.

### Confidence vocabulary (one model, used everywhere)

The pressure test surfaced three different confidence representations in the original draft (percentage in review, color dots in Slack, "Suggested/Confirmed" in tasks). One vocabulary replaces all three.

- **Ready** = model confidence ≥ 70%. Auto-included in the draft.
- **Needs review** = model confidence < 70%. Flagged for the user to check.
- The raw percentage is available on hover or tap for users who want detail. It is never the primary signal.
- Every surface (review screen, Slack, Notion, future Jira/Linear) uses the same two labels. No new words per channel.

### Accessibility

- Labels are text plus an icon (checkmark for Ready, exclamation for Needs review). Never color alone.
- This meets WCAG 2.1 Level A (success criterion 1.4.1, "Use of Color").
- All confidence states are readable by screen readers.

### Integration export format

When follow-ups are sent via integrations, the same vocabulary applies:

- **Slack:** Action items posted as a channel message. Each item shows the **Ready** or **Needs review** label inline, with the matching icon.
- **Notion:** Action items appended to the meeting page. Same labels and icons.
- **Jira and Linear (May 2026):** Action items exported as tasks. The label maps to a task field. **Ready** items create a confirmed task. **Needs review** items create a draft task that the assignee must accept before it appears in their queue. This avoids the downstream confusion flagged in the pressure test.

### Poor audio quality handling

Transcript accuracy drops below 80% in noisy environments (`03-product-knowledge/product.md`). When transcript quality is low:

- The follow-up draft shows a banner: "Transcript quality was low for this meeting. Action items may be less accurate."
- All action items default to "Suggested" status regardless of model confidence.
- Users can still review, edit, and send.

---

## Success Metrics

- Follow-up draft acceptance rate (users send without major edits): target 60% within 90 days of launch.
- Action item accuracy in sent follow-ups: improve from 66% to 80% by end of Q2 2026.
- Feature adoption: 30% of active Pro and Team users generate at least one draft per week within 60 days.
- Support tickets about missing/wrong action items: reduce by 25% vs Q1 2026 baseline.

**How we measure accuracy in production:** Two methods running in parallel. (1) User confirm/dismiss ratio as a real-time proxy - tracked per rollout phase. (2) Monthly labeled audit of 200 randomly sampled meetings, scored by the ML team against ground truth. The audit is the source of truth for the 80% target. The confirm/dismiss ratio is the early warning system.

Cross-reference: `04-strategy/okrs-q2-2026.md` for how these tie to Q2 goals.

---

## Review screen design

Sarah Chen runs 8-10 meetings/day (`05-user-personas/sarah-chen.md`). At 5-8 items per meeting, that's 50-80 review actions daily. The screen is designed for that load.

**What the user sees by default:**

- A count at the top: "4 Ready, 2 Needs review."
- The full action item list. Ready items are collapsed but visible (one-line preview). Needs review items are expanded.
- An outbound data preview: "This draft will be sent from your account to: [recipients]. Action items will be posted to: Slack #product-eng, Notion meeting page." This addresses Marcus's privacy concern (`05-user-personas/marcus-okafor.md`) before send, not after.

**Approve all behavior (defined explicitly):**

- "Approve all Needs review" accepts every flagged item as-is. The user still sees a confirm step: "Approve 2 Needs review items?"
- "Approve all" does not bypass the outbound data preview.
- Ready items are already in the draft. They do not need approval, but they are visible and can be removed.

**Zero-state and edge cases:**

- Zero action items extracted: review screen shows "No action items detected." User can still send the summary or add items manually.
- All items are Needs review: no Ready count shown. The user must review each before sending.
- Low transcript quality: banner appears (see "Poor audio quality handling" below). All items default to Needs review.
- User did not attend the meeting (calendar invite only): draft is not auto-generated. User can request one manually.

**Target:** under 2 minutes review per meeting, compared to Sarah's current 30 minutes of manual correction. Measured by time from review-screen open to send.

---

## What We're NOT Building

- Automatic sending. Every draft requires your explicit approval.
- Calendar integration. Scheduling follow-up calls is out of scope for this release.
- Custom email templates beyond the default layout.
- Multi-language support. English only at launch.
- Re-processing historical meetings. Confidence scores and follow-up drafts apply to new meetings only. Old meetings retain v1 action items as-is.
- Audit log events for Enterprise tier. Structured audit logging of AI confidence decisions deferred to Enterprise GA (June 2026, Tomás's scope).
- **Enterprise pilots are scoped OUT of the April rollout.** The three active enterprise pilots will not get Smart Follow-Up in April. They are re-included after audit logging ships at Enterprise GA in June 2026. Reason: shipping AI-drafted business comms to enterprise accounts without audit trails creates compliance risk and unsellable demo moments. Surfaced in the 23-05-2026 pressure test.
- Jira and Linear export at launch. Both ship in May 2026 as fast-followers (see "Why integration scope was cut" above).
- Salesforce sync. Q2 2026 launch targets Slack and Notion only.

---

## Dependencies

- **Action Item Scoring v2** must ship first. The confidence scoring model (trained on 50K labeled meetings) powers the Ready / Needs review logic. Without it, drafts have no reliability signal.
- Scoring v2 gaps to resolve before launch: implicit commitments, multi-person items, and conditional actions (example: "if design approves, Marcus will kick off sprint").
- **Training data for new gap areas - hard gate on April GA.** The existing 50K dataset has the same blind spots the model has. ML team needs to label new data for implicit, multi-person, and conditional items. Labeling scope, volume, and named ML owner must be confirmed by 25-03-2026. If labeling has not started by that date, April GA slips. This was the top risk flagged in the 23-05-2026 pressure test.
- **Monthly labeled audit of 200 meetings needs an owner.** This is the source of truth for the 80% accuracy target. Confirm ML owner and tooling before beta. Not a future enhancement.
- **Transcript quality ceiling.** Scoring v2 consumes transcription output. Transcript Accuracy v2 (Aisha, June 2026) ships after this feature. Until then, noisy-environment transcripts (~80% accuracy per `03-product-knowledge/product.md`) cap action item quality regardless of model improvements. The poor audio handling above mitigates this.
- **Privacy review for feedback loop.** Scoring v2 logs user confirm/dismiss actions as training data. For Team users, confirm with Tomas whether this training data includes meeting content, whether it's aggregated or per-user, and whether it complies with data retention policies. Must resolve before beta.

---

## Rollout Strategy

This is an ML model change that affects every user's action items. Phased rollout, not big bang.

| Phase | Audience | Duration | Gate to proceed |
|-------|----------|----------|-----------------|
| 1. Internal dogfood | MeetFlow employees | 1 week | No regressions in confirm/dismiss ratio vs v1 |
| 2. Pro power users | Top 10% Pro users by meeting volume (Sarah Chen segment) | 2 weeks | Accuracy proxy (confirm rate) >= 75%, no P0 bugs |
| 3. All Pro + Team (excl. enterprise pilots) | All paid users except the three active enterprise pilots | 1 week | Confirm rate holds, support ticket volume stable |
| 4. Free tier | All users | Ongoing | No gate - expand after paid tiers are stable |
| 5. Enterprise pilots | Three active pilots | After June 2026 Enterprise GA | Audit logging shipped, Tomás sign-off |

Feature-flagged from day one. Rollback trigger: confirm/dismiss ratio drops below v1 baseline for 48 hours, or P0 bug in draft generation.

---

## Observability

| Signal | What to track | Alert threshold |
|--------|--------------|-----------------|
| Confirm/dismiss ratio | Real-time proxy for accuracy. Track per rollout phase. | Drops below v1 baseline for 48 hours |
| Average confidence score | Trending metric. Sudden drops indicate model or input degradation. | Mean drops >10% week-over-week |
| Draft acceptance rate | Users who send without major edits. Primary success metric. | Below 40% after 30 days |
| Follow-up generation latency | Time from meeting end to draft available. | >120 seconds p95 |
| Transcript quality flag rate | How often the "low quality" banner appears. | >20% of meetings (indicates upstream issue) |

Logging requirements: For every follow-up draft, log input transcript quality score, extracted items with confidence scores, user edit actions (confirm, dismiss, edit, add), and final sent state. Retain for 90 days. Access restricted to ML and engineering teams.

---

## Timeline

| Milestone | Date |
|-----------|------|
| Scoring v2 labeling started (hard gate for April GA) | 25-03-2026 |
| Action Item Scoring v2 ships | March 2026 |
| Smart Follow-Up beta (internal) | Early April 2026 |
| Smart Follow-Up GA (Slack + Notion, paid tiers excl. enterprise) | April 2026 |
| Jira + Linear export ships (fast-follow) | May 2026 |
| Enterprise pilots included | After June 2026 Enterprise GA |
