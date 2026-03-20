# Sprint Planning - March 17, 2026

**Date:** March 17, 2026
**Facilitator:** You (AI Intelligence PM)
**Attendees:** You, Kai (eng lead), Remi (ML engineer), Yuki (ML engineer), Priscilla (backend), Dev (frontend), Noor (designer)
**Sprint duration:** March 17-28, 2026 (2 weeks)

---

## Sprint Goal

Ship Action Item Confidence Scoring v2.

The confidence model (trained on 50K labeled meetings) currently misses 34% of action items. This sprint addresses the three biggest gaps: implicit commitments, multi-person items, and conditional actions.

Smart Follow-Up depends on this. No scoring v2 = no reliable follow-up drafts in April.

---

## What We Committed To

1. **Improve extraction model for implicit commitments** - "I'll look into that" should register as an action item. Remi and Yuki own the model work.
2. **Add suggested action items UI** - Surface items users can confirm or dismiss. Low-confidence items shown in yellow. Dev owns front-end, Noor owns interaction design.
3. **Surface confidence scores visibly** - Right now they're buried in a tooltip. Move them into the action item card itself. Dev and Noor.
4. **Retrain pipeline smoke test** - The retraining pipeline is manual and takes 2 weeks. Priscilla will document the current steps so Kai can scope an automation sprint next quarter.

---

## Who's Doing What

| Task | Owner |
|------|-------|
| Model work - implicit commitments | Remi, Yuki |
| Model work - conditional actions | Remi |
| Model work - multi-person items | Yuki |
| Suggested action items UI | Dev, Noor |
| Confidence score card redesign | Dev, Noor |
| Retrain pipeline documentation | Priscilla |
| API contract for scoring v2 | Kai |

---

## Blockers

- Labeled data for conditional actions is thin. Remi flagged we have fewer than 500 examples. Yuki will pull additional examples from the unlabeled corpus by end of week.
- The frontend depends on a finalized API contract. Kai will have it ready by Wednesday, March 19.

---

## Decisions Made

- Confidence scores will show as text labels (High/Medium/Low), not percentages. Percentages test poorly with non-technical users.
- Suggested action items are confirm/dismiss only - no free-text editing in this sprint. That is scope for v2.1.
- We will not change the model retraining cadence this sprint. Document first, automate later.

---

## Cross-References

- Smart Follow-Up PRD: `08-product-features/prd-smart-follow-ups.md` - this sprint is a hard dependency for April launch.
- Sprint backlog: `11-sprint/sprint-backlog-2026-03-17.md`
