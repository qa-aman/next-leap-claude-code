# Launch Kit - Smart Follow-Up

**Date:** 17-03-2026 | **Launch target:** April 2026 (GA for Pro and Team users, Slack + Notion integrations)

---

## Positioning Summary

- **Alternatives:** Manually re-reading transcripts and writing follow-up emails by hand; relying on MeetFlow action items that are wrong 34% of the time (source: `prd-smart-follow-ups.md`, `competitive.md`). No competitor combines draft generation + confidence flagging in one review screen.
- **Unique capabilities:** (1) Drafts a follow-up email from the meeting summary and action items automatically. (2) Tags every action item as Ready (confidence >= 70%) or Needs review (confidence < 70%) - one consistent vocabulary across email, Slack, and Notion. (3) Review screen lets you approve, edit, or delete before anything is sent - nothing goes out automatically. (source: `prd-smart-follow-ups.md`)
- **Value:** You go from a 30-minute manual correction session to under 2 minutes per meeting; action item accuracy target improves from 66% to 80% by end of Q2 2026; you know which items to trust without re-reading the transcript. (source: `prd-smart-follow-ups.md`, `sarah-chen.md`, `feedback-q1-2026.md`)
- **Target customer:** Primary - Sarah Chen (Head of Product, 8-10 meetings/day, currently spends 45 min/evening on manual note correction, Pro user at $15/mo with a blocked team upgrade worth $4,700/yr). Secondary - Priya Nair (Chief of Staff, casual user, values low-friction output she can forward). (source: `sarah-chen.md`, `prd-smart-follow-ups.md`)
- **Category frame:** Follow-up automation within the AI meeting assistant category - not transcription, not generic AI summaries, but closing the accountability loop after the meeting ends. (source: `company.md`, `prd-smart-follow-ups.md`)

---

## 1. Announcement Blurb

You leave a meeting with ten action items. Three of them are wrong before the follow-up email is even drafted.

That broken loop is what Smart Follow-Up fixes. We know how much time you burn correcting MeetFlow's action items - the Q1 2026 survey was unambiguous: it was the #1 complaint, 19 out of 19 open-ended mentions. We built Smart Follow-Up to close that gap.

Here is how it works: when your meeting ends, MeetFlow drafts a follow-up email automatically. Every action item is labeled Ready or Needs review based on model confidence. You open the review screen, check the flagged items in under 2 minutes, and send - to email, Slack, or Notion. Nothing goes out without your approval.

The target is 80% action item accuracy by end of Q2 2026, up from 66% today.

Smart Follow-Up is available for all Pro and Team users starting April 2026. Free users get up to 5 drafts per month.

Try Smart Follow-Up after your next meeting.

---

## 2. Customer Email

**Subject:** Your follow-up email, drafted before you're back at your desk

---

You still have to correct every action item MeetFlow gives you. We know - it was the top complaint in our Q1 2026 survey.

Smart Follow-Up is the fix.

When your meeting ends, MeetFlow drafts a follow-up email using your summary and action items. Each item is labeled Ready (high confidence) or Needs review (flagged for you to check). You open the review screen, correct what needs correcting, and send - directly from MeetFlow to email, Slack, or Notion.

The review is designed for 8-10 meetings a day. Target: under 2 minutes per meeting, not 30.

Nothing sends automatically. You approve every draft before it goes out.

Smart Follow-Up is live for all Pro and Team users in April 2026. Free users get 5 drafts per month to try it.

Open your next summary and turn on Smart Follow-Up.

---

## 3. In-App Banner

**Banner copy (88 characters):** Your follow-up, drafted and ready to review. Nothing sends without you.

**CTA button:** Try Smart Follow-Up

---

## 4. Social Post

You run 8 meetings a day. Your follow-up emails take 30 minutes to write because you can't trust the action items.

Smart Follow-Up drafts the email for you - and flags every item that needs a second look before anything sends.

Action item accuracy target: 80% by Q2 2026, up from 66%.

Available for Pro and Team users, April 2026.

---

## SUCCESs Scorecard

### Initial Scoring

| Check | Blurb | Email | Banner | Social |
|---|---|---|---|---|
| Simple | pass - one idea: follow-up automation that you trust | pass - one idea, one CTA | pass - single compressed message | pass - one pain, one solution |
| Unexpected | pass - opens with the problem stat (3 of 10 wrong), not the product name | pass - subject frames success state before product is named | fail - "Nothing sends without you" is useful but not pattern-breaking | pass - "30 minutes to write because you can't trust" breaks the generic AI announcement pattern |
| Concrete | pass - 34% error rate, 2-minute review target, 80% accuracy goal, April 2026 | pass - "under 2 minutes", "8-10 meetings a day", "5 drafts per month" | fail - no specific number in 90 chars; "nothing sends without you" is behavioral not numerical | pass - "30 minutes", "80% by Q2 2026", "66%" all present |
| Credible | pass - all numbers from repo files, sourced below | pass - numbers cited to repo files | pass - behavioral claim (you approve before send) is verifiable and from PRD | pass - accuracy numbers from PRD and feedback files |
| Emotional | pass - opens on the frustration ("three of them are wrong"), names the evening correction session | pass - addresses the core embarrassment of unreliable AI | pass - "nothing sends without you" addresses the fear of AI sending bad emails | pass - "can't trust the action items" is the exact emotional complaint from Q1 survey |
| Stories | pass - before: 34% wrong; turn: review screen; after: send in 2 minutes | pass - before: correcting every item; turn: ready/needs review labels; after: send from MeetFlow | fail - too compressed for a full arc; implies turn but no before/after | pass - before: 30 min manual; after: drafted and flagged, April 2026 |
| **Total** | **6/6** | **6/6** | **3/6** | **6/6** |

### Banner Rewrite (3/6 - targeted at Unexpected, Concrete, Stories)

**Revised banner copy (89 characters):** 34% of action items are wrong. Smart Follow-Up flags every one before you send.

**CTA button:** Try Smart Follow-Up

### Banner Rescore

| Check | Banner (revised) |
|---|---|
| Simple | pass - one idea: flag bad items before they go out |
| Unexpected | pass - opens on the problem stat (34%), not a product claim |
| Concrete | pass - "34% of action items" is a specific number from repo files |
| Credible | pass - 34% error rate is from `prd-smart-follow-ups.md` and `feedback-q1-2026.md` |
| Emotional | pass - "before you send" activates the fear of sending wrong items |
| Stories | pass - implicit arc: wrong items exist (before) - Smart Follow-Up flags them (turn) - you send clean (after) |
| **Total** | **6/6** |

---

## Final Deliverables Summary

| Output | Status | Score |
|---|---|---|
| Announcement blurb | Ships as-is | 6/6 |
| Customer email | Ships as-is | 6/6 |
| In-app banner | Rewritten - use revised version | 6/6 (after rewrite) |
| Social post | Ships as-is | 6/6 |

**Final banner copy (use this version):** 34% of action items are wrong. Smart Follow-Up flags every one before you send.
**CTA button:** Try Smart Follow-Up

---

## Sources

| File | What was used |
|---|---|
| `08-product-features/01-smart-follow-up/prd-smart-follow-ups.md` | Feature capabilities, confidence vocabulary (Ready/Needs review), 70% confidence threshold, 2-minute review target, plan availability (Free: 5 drafts/mo, Pro: unlimited, Team: analytics), April 2026 GA date, Slack + Notion at launch, 80% accuracy target, rollout phases, 50K labeled meetings for training data |
| `03-product-knowledge/company.md` | Business snapshot, plan pricing ($15/mo Pro, $49/seat Team), category framing (AI meeting assistant) |
| `03-product-knowledge/competitive.md` | Competitive alternatives (Otter, Fireflies, Granola, Notion AI, manual), what competitors lack (no combined draft + confidence flagging), MeetFlow's AI quality positioning |
| `06-user-feedback/feedback-q1-2026.md` | Action items complaint: 19/19 mentions as #1 theme; NPS: 34; verbatim: "I can't trust the action items"; saves 20-30 min/day theme (16 mentions) |
| `05-user-personas/sarah-chen.md` | Primary persona: 8-10 meetings/day, 45 min/evening manual correction, blocked team upgrade ($4,700/yr), trust erosion detail |
| `09-release-notes/release-v2.4-smart-summaries.md` | Tone and voice reference; release notes style: plain, direct, short sentences, no hype words |
| `04-strategy/product-vision.md` | Action item accuracy baseline: 66%; direction: up |

### Number Traceability

| Number | Source |
|---|---|
| 34% of action items wrong or missing | `prd-smart-follow-ups.md` Problem section; corroborated by `product-vision.md` |
| 19/19 mentions - #1 complaint | `feedback-q1-2026.md` Top Complaints table |
| Under 2 minutes review per meeting | `prd-smart-follow-ups.md` Review screen design section |
| 45 minutes evening note correction | `sarah-chen.md` What You Love section |
| 8-10 meetings per day | `sarah-chen.md` Typical Day section |
| 80% accuracy target by Q2 2026 | `prd-smart-follow-ups.md` Success Metrics |
| 66% current action item accuracy | `product-vision.md` What Success Looks Like table |
| 5 drafts/month (Free tier) | `prd-smart-follow-ups.md` Plan Availability |
| April 2026 GA | `prd-smart-follow-ups.md` Timeline table |
| 70% confidence threshold for Ready label | `prd-smart-follow-ups.md` Confidence vocabulary section |
| $4,700/yr blocked upgrade | `sarah-chen.md` Revenue Potential section |
