# Sprint Backlog - March 17-28, 2026

**Sprint goal:** Ship Action Item Confidence Scoring v2.
**Sprint dates:** March 17-28, 2026 (2 weeks)
**Team:** Kai (eng lead), Remi (ML), Yuki (ML), Priscilla (backend), Dev (frontend), Noor (designer)

Cross-reference: `10-meetings/sprint-planning-2026-03-17.md` for context and decisions.

---

## Backlog

| Task | Owner | Status | Story Points |
|------|-------|--------|-------------|
| Finalize API contract for scoring v2 | Kai | Done | 2 |
| Pull labeled data for conditional actions from unlabeled corpus | Yuki | Done | 3 |
| Retrain model - implicit commitments ("I'll look into that") | Remi, Yuki | In Progress | 8 |
| Retrain model - multi-person action items | Yuki | In Progress | 5 |
| Retrain model - conditional actions ("if X, then Y") | Remi | Not Started | 5 |
| Confidence score card redesign (move out of tooltip) | Dev, Noor | In Progress | 3 |
| Suggested action items UI - confirm/dismiss interaction | Dev, Noor | Not Started | 5 |
| Low-confidence item flagging (yellow highlight in UI) | Dev | Not Started | 3 |
| Document manual retraining pipeline steps | Priscilla | Not Started | 2 |

**Total:** 36 story points

---

## Notes

- Confidence scores will display as High/Medium/Low labels - not percentages. Decided in sprint planning.
- Free-text editing of suggested items is out of scope. Confirm/dismiss only.
- The retrain pipeline doc is not a launch dependency. It's a Q3 automation input.

---

## Dependency

Smart Follow-Up (April 2026) depends on this sprint shipping clean.
See PRD: `08-product-features/prd-smart-follow-ups.md`
