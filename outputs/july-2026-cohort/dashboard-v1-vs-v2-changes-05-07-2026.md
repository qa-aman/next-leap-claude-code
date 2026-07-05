# Dashboard v1 vs v2 - What Changed

**Date:** 05-07-2026
**Files compared:**
- v1: `outputs/salary-dashboard-05-07-2026.html`
- v2: `outputs/salary-dashboard-v2-05-07-2026.html` (rebuilt with the `/dataviz` design system)

The data did not change. Both files show the same 36 people. Verified KPIs are identical in both:
Headcount 36, Average $101,125, Highest $176,000, Lowest $44,000, Median $96,000.
v2 is a design and correctness upgrade, not a data change.

---

## Change summary

| Area | v1 | v2 | Why it matters |
|---|---|---|---|
| Bar chart colour | Blue-to-navy gradient on every bar | One flat blue hue per bar | A single measure gets one colour. A gradient double-encodes bar length as colour and adds no information. |
| Colour-blind safety | Chosen by eye | Donut palette run through the validator script for light and dark | Removes guesswork. The 3 categorical colours pass CVD separation in both modes. |
| Low-contrast colours | Not handled | Every donut slice carries a direct label and percentage | Two of the categorical colours fall below the 3:1 contrast line on white. Labels mean colour is never the only signal. |
| Donut segment edges | Segments touched | 2px surface gap between segments | Cleaner separation without drawing borders around marks. |
| Hover | None | Tooltips on bars and donut slices; hovering a slice dims the others | You can read exact values and link a slice to its legend row. |
| Dark mode | None | A real second theme with its own validated colours, plus a toggle button | Dark mode is built from dark-surface colours, not an automatic invert. |
| Table | Sortable and searchable | Same, kept as the accessible twin | Every value stays reachable without a tooltip. |
| Typography | Mixed weights | System sans throughout, proportional figures on big numbers, aligned figures only in table columns | Numbers read cleanly at large sizes and line up in the table. |
| Location chart | Vertical columns | Horizontal bars | Location names read straight, no rotated or clipped labels. |

---

## The method behind v2

The `/dataviz` skill follows a fixed order. Colour comes last, after the chart type is chosen.

1. **Pick the form by its job.** Department, location, and experience are magnitude, so they are bars. Gender and employment type are part-to-whole with 3 slices each, so they are donuts. KPIs are single numbers, so they are stat tiles.
2. **Assign colour by job.** Magnitude bars use one sequential blue. The donuts use a categorical palette where each colour means an identity, not a rank.
3. **Validate, do not eyeball.** The categorical palette was checked with the validator script:
   - Light mode: passes lightness, chroma, and colour-blind separation. Two colours flagged below 3:1 contrast, so labels are required (done).
   - Dark mode: passes all four checks.
4. **Mark specs.** Thin bars, rounded ends, 2px gaps, hairline separators, no borders around marks.
5. **Hover layer.** Tooltips on every mark.
6. **Accessibility pass.** Legends with labels, a table view, and a real dark mode.

---

## What did not change, on purpose

- Chart types that were already right stayed the same. Bars stayed bars, donuts stayed donuts.
- No chart was added just to look busy.
- v1 is left in place. v2 is a separate file so you can compare them side by side.

---

## Open options (not done yet)

- Split the two donuts into their own panels instead of side by side.
- Show experience with an ordered light-to-dark ramp to stress seniority.
- Add tenure (years since joining date), a salary-vs-experience scatter, or a top-10 earners panel.
- Generate the HTML data array straight from the Excel Data sheet so the two files stay in sync.
