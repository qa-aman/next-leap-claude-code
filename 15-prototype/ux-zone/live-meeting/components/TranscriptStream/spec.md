# TranscriptStream

Scrollable transcript pane that auto-reveals mock lines on a timer to simulate the live experience. Each line: avatar + speaker name + timestamp + paragraph.

## Anatomy
- Scrollable container (520px fixed height)
- Per-line: 28px avatar (left), speaker block (right)
- Speaker block: name + timestamp on the baseline; paragraph below
- Listening indicator at the bottom (3-dot pulse + "Listening")

## Behavior
- Starts with 2 lines revealed; reveals one more every 2.2s until exhausted
- Auto-scrolls to bottom on each reveal (smooth)

## Mirrored from
- `screenshots/dialpad-01.png` - left-rail Transcripts/Notes tabs + Turn off AI toggle + Listening indicator + Add action item bottom anchor.
- `screenshots/otterai-03.png` - timestamped speaker blocks.
- `screenshots/fireflies-04.png` - speaker + timestamp baseline pattern.

## Props
- `lines: TranscriptLine[]`
