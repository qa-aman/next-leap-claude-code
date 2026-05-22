# FilterChips

Segmented control for filtering the action items list. Three options: All / High confidence / Needs review. Each chip shows a count badge.

## Anatomy
- Outer container: rounded border, 1px gap between chips
- Active chip: filled bg-subtle + foreground text, accent-tinted count
- Inactive chip: muted text, hover state

## Mirrored from
- `screenshots/motion-05.png` - Priority dropdown filter (ASAP / High / Medium / Low with checkboxes). Adapted from dropdown to segmented control for higher visibility on /action-items.
- `screenshots/linear-04.png` - Filter + Display toolbar pattern above the list.

## Props
- `value: ActionFilter` - "all" | "high" | "needs-review"
- `onChange: (v: ActionFilter) => void`
- `counts: Record<ActionFilter, number>`
