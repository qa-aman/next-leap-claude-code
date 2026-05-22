# ActionItemRow

A single action item row. Two-column grid (content left, actions right). Content holds badges row + title + meta row.

## Anatomy
- Badge row: ConfidenceBadge + state badge (Confirmed / Needs review)
- Title: task text
- Meta row: avatar + assignee name, due date (mono), source meeting title
- Actions (right): Reject + Confirm for needs-review state; Edit for confirmed state

## Mirrored from
- `screenshots/sana-ai-01.png` - Task / Owner / Deadline / Notes table with source-meeting badges per cell. CANONICAL row model - closest match to MeetFlow's action items extracted from meetings.
- `screenshots/asana-03.png` - dual-pill pattern (ConfidenceBadge + state badge) at the top of the row.
- `screenshots/linear-04.png` - minimal density of identifying meta (assignee + due date on the right line).
- `screenshots/otterai-02.png` - inline action affordances (Confirm / Reject / Edit) on the right.

## Props
- `item: ActionItem`
- `onConfirm: (id: string) => void`
- `onReject: (id: string) => void`
