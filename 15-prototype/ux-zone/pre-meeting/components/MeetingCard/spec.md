# MeetingCard

A row representing one upcoming meeting in the pre-meeting list. Click expands the agenda preview inline; the Join button is the primary CTA.

## Anatomy
- Time block (left): start time + duration, monospace, subtle border
- Title + meta (center): title + "Recording on" badge if applicable; date + participant avatars + count below
- Join button (right): primary CTA, stops propagation so it doesn't toggle the expansion

## Variants
- `expanded: false` - collapsed row, default state
- `expanded: true` - accent border, agenda panel shown below (rendered by parent)
- `recordingOn: true` - accent dot badge visible

## States
- Default, hover (row), expanded, focus-visible (keyboard)

## Mirrored from
- `screenshots/grain-02.png` - grouping by Now / Today / Tomorrow + per-meeting Record toggle pattern. The time block left + meta center + action right composition follows this card.
- `screenshots/apollo-01.png` - table-row composition (title + date + time + record toggle + action button on the right).
- `screenshots/otterai-03.png` - Today card with prominent Join button.

## Props
- `meeting: Meeting` - see `lib/mock-data.ts`
- `expanded: boolean`
- `onToggle: () => void`
- `onJoin: () => void`
