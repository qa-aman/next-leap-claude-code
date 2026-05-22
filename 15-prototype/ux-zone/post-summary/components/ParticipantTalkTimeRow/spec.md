# ParticipantTalkTimeRow

Per-participant talk-time row with avatar + name + WPM + percentage + horizontal bar.

## Anatomy
- Avatar (28px) on the left
- Name (left, fills) + WPM + percentage (right) on top row
- Horizontal progress bar (accent-filled) below

## Mirrored from
- `screenshots/fireflies-05.png` - Speaker Talktime panel with avatar + name + WPM + donut + percentage. CANONICAL reference (donut adapted to horizontal bar for layout density).
- `screenshots/grain-04.png` - Mike/Rachel timeline bars with percentage badges (alternate horizontal format).

## Props
- `participant: Participant` - see `lib/mock-data.ts`
