# AgendaPreviewPanel

Inline expansion shown under a MeetingCard when it is clicked. Two columns: Agenda bullets (left) + Attendees list (right).

## Anatomy
- Border-top divider from the parent card body
- Two-column grid (1fr / 220px) - stacks on mobile
- Left: "Agenda" subtitle + bulleted items
- Right: "Attendees" subtitle + avatar + name rows

## Variants
- Single variant; data-driven

## Mirrored from
- `screenshots/otterai-03.png` - right-side calendar mini-view + Today's items panel pattern adapted into the inline two-column layout.
- `screenshots/grain-02.png` - expanded card pattern with extra details inline under the row.

## Props
- `meeting: Meeting`
