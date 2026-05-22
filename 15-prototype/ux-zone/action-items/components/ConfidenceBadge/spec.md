# ConfidenceBadge

The headline indicator for Action Item Confidence Scoring v2. Color-coded pill with a leading dot, the confidence label, and an optional numeric percentage.

## Anatomy
- Leading dot (3px, color matches tone)
- Label: High / Medium / Low
- Percentage (monospace, slight opacity reduction) - optional

## Variants
- `confidence: high` - success (green)
- `confidence: medium` - warning (amber)
- `confidence: low` - danger (red)
- `showPct: false` - hides numeric value (for dense lists)

## Tooltip
- Native `title` attribute with full label + percentage for hover detail

## Mirrored from
- `screenshots/asana-03.png` - BEST reference. Mirrors the colored Priority chip side of Asana's dual-pill pattern (Low / Medium / High). The companion `state` chip (Confirmed / Needs review) is rendered separately in ActionItemRow.

## Props
- `confidence: "high" | "medium" | "low"`
- `pct: number` - 0-100
- `showPct?: boolean` - default true
