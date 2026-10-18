---
name: vague-efficacy-request-defaults
description: How to resolve a vague "recent feature to improve efficacy" PRD ask, plus cohort-folder and overwrite handling seen 18-10-2026
metadata:
  type: project
---

A vague ask like "PRD for the recent feature to improve efficacy" resolves to Action Item Confidence Scoring v2 (accuracy work in flight, see MEMORY.md roadmap status). Subagents cannot ask the user, so state this assumption in the report.

**Why:** Run on 18-10-2026. Only accuracy is the in-flight efficacy bet; 04-strategy/product-vision.md and the sprint note back it.

**How to apply:**
- A full PRD for this feature already exists at `outputs/sept-2026-cohort/prd-action-item-confidence-scoring-v2.md` (different, longer format). Do not overwrite it. The one-pager was saved as `...-v2-one-page.md`.
- No `oct-2026-cohort` folder existed on 18-10-2026. The most recent folder was `sept-2026-cohort`, used as the fallback. Flag this to the caller.
- Gap still open: no file sets a date or owner for post-launch accuracy re-measurement.
