# RecipientPicker

Multi-select recipient chips for the follow-up composer. Chips are removable; "+ Add" opens a dropdown to add missing participants.

## Anatomy
- Label: "TO" (uppercase, subtle)
- Container: rounded border with internal chip flex-wrap
- Chip: avatar + name + × close
- Add button: ghost style; opens floating dropdown of unselected participants

## Mirrored from
- `screenshots/apollo-01.png` - To: field with email chips + dropdown.
- `screenshots/superhuman-05.png` - single-line To: with chip removal.

## Props
- `available: { name, initials }[]`
- `selected: string[]`
- `onToggle: (name: string) => void`
