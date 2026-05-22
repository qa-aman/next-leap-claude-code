# Action items + confidence — Screen Notes

**Route:** `/action-items`
**Purpose:** Demo Action Item Confidence Scoring v2 (active sprint 17-03-2026 to 28-03-2026).

---

## References to mirror

### Filter chips (All / High / Needs review)
- Reference: `motion-05.png` — Mirror the **Priority dropdown filter (ASAP / High / Medium / Low with checkboxes)**. Adapt to All / High / Needs review with the same checkbox-in-dropdown pattern.
- Reference: `linear-04.png` — Mirror the **Filter + Display buttons in a top toolbar** for the filter affordances above the list.

### Action item row (with confidence badge)
- Reference: `sana-ai-01.png` — Mirror the **Task / Owner / Deadline / Notes table layout with source-meeting badges under each cell**. This is the CLOSEST match to MeetFlow action items extracted from meetings — use as the canonical row layout.
- Reference: `linear-04.png` — Mirror the **minimal row density**: status icon + ID + title + project badge + due date + assignee on the right. Adapt for compact view.
- Reference: `otterai-02.png` — Mirror the **simple checklist style** (checkbox + task title + Add action item) as an even more compact alternate.

### Confidence badge styling
- Reference: `asana-03.png` — **BEST reference for confidence badge.** Mirror the **dual-pill pattern**: colored Priority chip (Low/Medium/High) + colored Status chip (On track / At risk / Off track) side by side. Apply this exact pattern as confidence badge (High/Medium/Low) + state badge (Confirmed/Needs review).

### Per-item actions (Edit, Confirm, Reject)
- Reference: `otterai-02.png` — Mirror the **inline action affordances** (Assign this to yourself / Check off this action item style). Use for Edit / Confirm / Reject row actions.
- Reference: `linear-04.png` — Mirror the **right-side icons appearing on row hover** for the secondary actions.

### Empty state (no items in "Needs review")
- Reference: `linear-04.png` — Mirror the **minimal centered empty area** with a single icon + supporting copy.

---

## Layout rationale

Trust is the headline feeling on this screen because confidence is the v2 differentiator. The confidence badge must be unmissable — use the Asana dual-pill pattern (color + label) so it reads at a glance. Filter chips at the top let the user jump straight to "Needs review" (low + medium confidence) for triage. Sana-AI's Task/Owner/Deadline/Notes columns map almost 1:1 to MeetFlow's data model.

---

## Components to extract

- `FilterChips` — Motion-05 dropdown filter pattern
- `ActionItemRow` — Sana-AI-01 four-column table row
- `ConfidenceBadge` — Asana-03 colored pill (paired with a state pill)
- `ActionItemMenu` — Otter.ai-02 inline action affordances
- `EmptyState` — reuse from pre-meeting (Zoom-04 / Linear-04 minimal style)
