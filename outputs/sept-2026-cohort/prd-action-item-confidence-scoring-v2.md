# PRD - Action Item Confidence Scoring v2

**Pillar:** AI Intelligence
**Owner:** Senior PM, AI Intelligence
**Target:** March 2026
**Status:** In Progress (sprint 17-03-2026 to 28-03-2026 already committed and in flight, `11-sprint/sprint-backlog-2026-03-17.md`)

---

## Problem

34% of MeetFlow's extracted action items are wrong or missing (`03-product-knowledge/company.md`; `03-product-knowledge/product.md`). This is the #1 complaint in the Q1 2026 NPS survey, 19 of 47 respondents (`06-user-feedback/feedback-q1-2026.md`): "I can't trust the action items. I still have to go back and check every single one." The survey's key finding states the gap between promoters and detractors is explained almost entirely by action item accuracy, and fixing it converts detractors into promoters because the core time-savings value is already proven (`06-user-feedback/feedback-q1-2026.md`). The current confidence model, trained on 50K labeled meetings, has three specific gaps: implicit commitments ("I'll look into that"), multi-person action items, and conditional actions ("if X, then Y") (`10-meetings/sprint-planning-2026-03-17.md`). Confidence scores also sit buried in a tooltip today, so even correct scores go unseen (`03-product-knowledge/product.md`).

Cross-reference: `03-product-knowledge/product.md` for full feature context.

---

## Who It's For

- **Sarah Chen - "The Power User"** - Head of Product, runs 8-10 meetings daily and uses AI action items as her primary task list. Confidence scores currently say "high" but critical items still get missed, so she double-checks every item manually, which defeats the purpose. She needs confidence scores she can actually trust, not just visible. See `05-user-personas/sarah-chen.md`.
- **Marcus Okafor - "The Skeptic"** - Engineering Manager at an Enterprise fintech. His team ignores MeetFlow's AI summaries and works around the tool in Google Docs. Multi-person and conditional action items are common in his sprint reviews and standups; improving extraction on exactly those two gaps is one of the few AI-quality levers that could move his team toward engaging with MeetFlow's output at all, though privacy remains his primary blocker and this PRD does not claim to resolve it. See `05-user-personas/marcus-okafor.md`.
- **Priya Nair - "The Casual"** - Chief of Staff, does not review transcripts or action items in detail today; her CEO reads the auto-pushed Slack digest instead. She is included here because Smart Follow-Up (`08-product-features/01-smart-follow-up/prd-smart-follow-ups.md`) will surface action items to her CEO more directly once it ships, so scoring accuracy in this sprint indirectly protects a digest she is not actively auditing herself. See `05-user-personas/priya-nair.md`.

---

## What It Does

- Improves the extraction model to catch implicit commitments ("I'll look into that") as tracked action items.
- Improves extraction for multi-person action items (an item owned or shared by more than one attendee).
- Improves extraction for conditional actions ("if X, then Y") phrasing.
- Moves confidence scores out of the tooltip and into the action item card itself, shown as High/Medium/Low text labels, not percentages (`11-sprint/sprint-backlog-2026-03-17.md`).
- Surfaces suggested action items that users can confirm or dismiss, with low-confidence items visually flagged (yellow highlight) so the user knows what to check first (`11-sprint/sprint-backlog-2026-03-17.md`).

---

## How It Works

1. A meeting ends and MeetFlow's transcription and extraction pipeline runs as it does today.
2. The v2 model scores each candidate action item, including the three previously weak categories (implicit, multi-person, conditional).
3. Each item is labeled High, Medium, or Low confidence and rendered directly on the action item card, not hidden in a tooltip.
4. Low-confidence items are highlighted in yellow so the user's eye goes there first.
5. The user reviews the list and confirms or dismisses each suggested item; free-text editing of suggested items is explicitly out of scope for this sprint (`11-sprint/sprint-backlog-2026-03-17.md`).
6. Confirmed items flow into the meeting's action item list as they do today; dismissed items are dropped.

---

## Success Metrics

- Action item accuracy (correct and complete): improve from 66% to the 80% Q2 2026 target (`04-strategy/okrs-q2-2026.md`, Objective 1). This sprint targets the three largest known gap categories toward that target; it is not expected to close the full 14-point gap alone.
- NPS: contribute to the move from 34 to the 45 target (`04-strategy/okrs-q2-2026.md`, Objective 3), since action item accuracy is the survey's stated explanation for the promoter/detractor gap (`06-user-feedback/feedback-q1-2026.md`).
- Pro monthly churn: contribute to the reduction from 4.1% to the 2.5% target (`04-strategy/okrs-q2-2026.md`, Objective 3).
- Smart Follow-Up adoption rate: this sprint is a named hard dependency for the 40% Pro adoption target (`04-strategy/okrs-q2-2026.md`, Objective 1; `03-product-knowledge/product.md` - "Depends on Action Item Scoring v2 shipping first").

Cross-reference: `04-strategy/okrs-q2-2026.md` for how these tie to quarterly goals.

---

## What We're NOT Building

- Free-text editing of suggested action items. Confirm/dismiss only in this sprint; editing is scoped to v2.1 (`10-meetings/sprint-planning-2026-03-17.md`).
- Percentage-based confidence display. Decided against in sprint planning because percentages test poorly with non-technical users; High/Medium/Low text labels only (`10-meetings/sprint-planning-2026-03-17.md`).
- Automating the model retraining pipeline. This sprint only documents the current manual steps (2 weeks per cycle); automation is scoped as a Q3 input, not a launch dependency (`11-sprint/sprint-backlog-2026-03-17.md`).
- Reprocessing historical meetings. Scope is new meetings only, matching how the dependent Smart Follow-Up PRD treats this same model (`08-product-features/01-smart-follow-up/prd-smart-follow-ups.md`).
- Transcript accuracy improvements. Transcript Accuracy v2 is a separate feature owned by Aisha, targeted June 2026 (`03-product-knowledge/product.md`).

---

## Dependencies

- **Labeled training data for conditional actions.** Fewer than 500 examples exist today; Yuki is pulling additional examples from the unlabeled corpus (`10-meetings/sprint-planning-2026-03-17.md`). Model quality on this category is capped until this is resolved.
- **Finalized API contract.** Frontend work (suggested items UI, confidence card redesign) depends on Kai finalizing the API contract (`10-meetings/sprint-planning-2026-03-17.md`).
- **Transcript quality ceiling.** The model consumes transcription output, which drops below 80% accuracy in noisy environments (`03-product-knowledge/product.md`, Tech Debt). Scoring improvements cannot exceed this ceiling until Transcript Accuracy v2 ships in June 2026.
- **Downstream: Smart Follow-Up.** Smart Follow-Up (April 2026 target) depends on this sprint shipping clean; garbage suggested action items produce garbage follow-up drafts (`03-product-knowledge/product.md`; `08-product-features/01-smart-follow-up/prd-smart-follow-ups.md`).

---

## Timeline

| Milestone | Date |
|-----------|------|
| API contract finalized | 19-03-2026 |
| Sprint start (model retraining, UI redesign begin) | 17-03-2026 |
| Sprint end - Action Item Confidence Scoring v2 ships | 28-03-2026 |
| Smart Follow-Up beta (dependent feature, hard-gated on this ship) | Early April 2026 |

Open question: no committed date exists in the repo for a post-launch accuracy re-measurement against the 80% Q2 target; recommend confirming an owner and cadence with the ML team (Remi/Yuki) before sprint close.
