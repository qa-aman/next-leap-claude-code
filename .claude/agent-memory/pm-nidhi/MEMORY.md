# PM-Nidhi memory

Heuristics learned across runs. Keep entries generalizable, one line each.

## Source files that answer common questions
- Company baseline numbers (ARR, users, churn, accuracy): `03-product-knowledge/company.md`
- Competitor landscape: `03-product-knowledge/competitive.md`
- Personas: `05-user-personas/`
- PRD template used by the `prd` skill: `.claude/skills/prd/assets/template-prd.md` (not `14-templates/`, that one is generic/unused by the skill)
- To find "the feature we are building right now": check `11-sprint/sprint-backlog-*.md` + `10-meetings/sprint-planning-*.md` for the active sprint goal, and `03-product-knowledge/product.md` "Current Sprint" section - they should agree.
- Before writing a PRD, glob `08-product-features/**` fully (it has subfolders like `01-smart-follow-up/`) to check if one already exists for the feature; don't assume from a flat glob of the top level only.

## Skill gotchas
- The `prd` skill's example PRD (`references/example-prd.md`, Smart Follow-Up) adds sections beyond the 8 required (Plan Availability, Rollout Strategy, Observability) when the feature needs them - fine to do the same, keep template order intact.

## Stakeholder preferences
- (none yet)

## Persona status
- [Persona status](persona_status.md) - Sarah Chen no longer available/using MeetFlow (16-09-2026); don't use as live reference persona.
