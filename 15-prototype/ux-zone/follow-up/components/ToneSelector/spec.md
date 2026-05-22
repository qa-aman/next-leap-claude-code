# ToneSelector

Three-up card grid for picking the AI draft tone: Concise / Warm / Direct. Selecting a tone triggers the body to swap to the matching prefilled draft.

## Anatomy
- Label: "TONE" (uppercase, subtle)
- 3-column grid of card-shaped buttons
- Each card: label (bold) + hint line below
- Active state: accent border + accent-tinted bg

## Mirrored from
- `screenshots/strut-02.png` - BEST reference for tone selector. AI Edit > Adjust tone > sub-menu (Neutral / Friendly / Professional / Casual). Adapted from dropdown to inline 3-card grid for higher visibility.
- `screenshots/pipedrive-03.png` - Email tone dropdown + Email length dropdown structured controls.
- `screenshots/honeybook-04.png` - inline tone chips below the draft.

## Props
- `value: Tone` - "concise" | "warm" | "direct"
- `onChange: (t: Tone) => void`
