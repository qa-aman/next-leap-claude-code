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

- Drafts a follow-up email after each meeting using the summary and extracted action items.
- Shows you a review screen before anything is sent. You edit, delete, or approve.
- Assigns each action item a confidence score (example: "85% confident this is an action item") so you know what to double-check.
- Lets you send directly from MeetFlow or copy the draft to your email client.
- Integrates with Slack (send as a channel message), Notion (append to meeting page), and Jira/Linear (create tasks from action items).

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

---

## Success Metrics

- Follow-up draft acceptance rate (users send without major edits): target 60% within 90 days of launch.
- Action item accuracy in sent follow-ups: improve from 66% to 80% by end of Q2 2026.
- Feature adoption: 30% of active Pro and Team users generate at least one draft per week within 60 days.
- Support tickets about missing/wrong action items: reduce by 25% vs Q1 2026 baseline.

Cross-reference: `04-strategy/okrs-q2-2026.md` for how these tie to Q2 goals.

---

## What We're NOT Building

- Automatic sending. Every draft requires your explicit approval.
- Calendar integration. Scheduling follow-up calls is out of scope for this release.
- Salesforce sync. That integration is Q2. This launch targets Slack, Notion, Jira, Linear.
- Custom email templates beyond the default layout.
- Multi-language support. English only at launch.

---

## Dependencies

- **Action Item Scoring v2** must ship first. The confidence scoring model (trained on 50K labeled meetings) powers the flagging logic. Without it, follow-up drafts have no reliability signal.
- Action Item Scoring v2 gaps to resolve before launch: implicit commitments, multi-person items, and conditional actions (example: "if design approves, Marcus will kick off sprint").

---

## Timeline

| Milestone | Date |
|-----------|------|
| Action Item Scoring v2 ships | March 2026 |
| Smart Follow-Up beta (internal) | Early April 2026 |
| Smart Follow-Up GA (general availability) | April 2026 |
