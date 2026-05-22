# AiNotesPanel

Right-rail panel during the live meeting. Auto-reveals AI-captured notes on a timer; user can add notes manually.

## Anatomy
- Header: sparkle icon + "AI Notes" label + Live counter (mono, uppercase)
- Body: scrollable list of note cards
- Footer: "+ Add note manually" affordance with ⌘N hint

## Behavior
- Starts with 1 note revealed; reveals one more every 3.5s
- Placeholder dashed-border card while waiting

## Mirrored from
- `screenshots/dialpad-02.png` - Notes tab pattern with inline composer. The "Add note manually" anchor is adapted from Dialpad's "Add action item" bottom.
- `screenshots/zoom-05.png` - AI Companion welcome state pattern.

## Props
- `notes: string[]`
