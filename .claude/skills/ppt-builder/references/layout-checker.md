# Layout Checker — Details

Run after every build:

```bash
python3 scripts/check_layout.py <path-to-pptx>
```

Exit code is `0` if clean, `1` if any issue is found. **Do not hand the deck to the user until the check passes.**

## What it catches

1. **Out-of-bounds shapes** — content positioned past the 13.33 x 7.5 inch canvas.
2. **Overlapping text shapes** — footers sitting on top of the last row, labels colliding with badges, two textboxes inside the same row stepping on each other.

## Fix loop

- Read the slide number and overlapping text fragments reported.
- Fix the position or size of the offending shape in the build script.
- Re-run the build script, then re-run the checker.
- Repeat until exit code `0`.

## What is excluded

The checker excludes the orange accent bar at the top of every slide and the full-slide background rectangle by heuristic, so it will not false-flag those. For new decorative shapes that span the full width with negligible height (e.g. additional dividers), the heuristic catches them automatically.

## Common collision: right-side panel + bottom callout

If a slide has a right-side panel and a bottom accent callout at top=6.5in, cap the panel height at 4.4in (top=1.85in + height=4.4in = ends at 6.25in). Otherwise the panel and the callout will overlap.

## live_badge

If a layout truly needs a wide section_tag plus a small chip in the same row, use `live_badge(s)` (provided in the design system) — its dimensions are tuned so the bundled `section_tag` width never collides with it.
