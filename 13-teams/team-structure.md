# AI Intelligence Pillar - Team Structure

**Pillar:** AI Intelligence
**PM:** You (Senior PM)
**Scope:** Smart Summaries, Action Item Confidence Scoring, Meeting Pattern Insights

Cross-reference: `03-product-knowledge/company.md` for full product team context.

---

## Team Members

| Name | Role | What They Own |
|------|------|--------------|
| You | Senior PM | Pillar strategy, roadmap, PRDs, stakeholder alignment |
| Kai | Engineering Lead | Technical architecture, API contracts, sprint facilitation |
| Remi | ML Engineer | Confidence scoring model, extraction model training |
| Yuki | ML Engineer | Data labeling, model evaluation, multi-person item detection |
| Priscilla | Backend Engineer | Data pipeline, model serving, infrastructure |
| Dev | Frontend Engineer | Action item UI, suggested items, confidence score display |
| Noor | Product Designer | Interaction design, prototypes, user-facing AI surfaces |

---

## RACI - Smart Follow-Up Feature

RACI is a responsibility model. Each letter stands for a role in a decision or task:
- **R - Responsible** (does the work)
- **A - Accountable** (makes the final call, owns the outcome)
- **C - Consulted** (gives input before the decision)
- **I - Informed** (told after the decision is made)

| Task | Accountable | Responsible | Consulted | Informed |
|------|-------------|-------------|-----------|---------|
| Feature strategy and scope | You | You | Dana Rivera, Aisha Patel | CEO, VP Eng |
| PRD sign-off | You | You | Kai, Noor | Full team |
| ML model work (Scoring v2) | Kai | Remi, Yuki | You | Dana, Tomás |
| Frontend implementation | Kai | Dev | Noor, You | - |
| Design and UX | You | Noor | Dev, Kai | - |
| API contract | Kai | Kai, Priscilla | Remi, Dev | You |
| Launch readiness | You | You, Kai | Dana, Aisha | VP Sales, CEO |

---

## Notes

- Smart Follow-Up depends on Action Item Scoring v2. Remi and Yuki are the critical path owners.
- Dana Rivera (Platform PM) is consulted on launch because Slack, Notion, Jira, and Linear integrations are in scope.
- Full PRD: `08-product-features/prd-smart-follow-ups.md`
