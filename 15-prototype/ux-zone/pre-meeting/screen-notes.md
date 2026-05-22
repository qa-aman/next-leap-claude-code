# Pre-meeting — Screen Notes

**Route:** `/`
**Purpose:** Show upcoming meetings, let user join with MeetFlow.

---

## References to mirror

### Header
- Reference: `fireflies-05.png` — Mirror the top-bar pattern with brand wordmark left, search bar center, primary action button (Capture) + invite + notifications + avatar on the right. Use this as the canonical Header.tsx layout.
- Reference: `apollo-01.png` — Mirror the dense sidebar nav grouping (Home / Meetings / sections divided by labels) for the left rail if we add one.

### Meeting list
- Reference: `grain-02.png` — Mirror the **grouping pattern (Now / Today / Tomorrow / Wednesday Feb 12)** and the per-meeting card with title + time + Join Meeting button + Record toggle. This is the closest match to MeetFlow's pre-meeting flow.
- Reference: `apollo-01.png` — Mirror the **table-row composition**: title + date + time + location chip + record toggle + insights button. Use as alternate compact view.
- Reference: `zoom-04.png` — Mirror the **date-grouping headers** (Tomorrow / Tue, Apr 18 / Tue, Apr 25) and the minimal row composition (time range + title + meeting ID).
- Reference: `otterai-03.png` — Mirror the **Today card** style with prominent time + Join meeting button.

### Agenda preview panel
- Reference: `otterai-03.png` — Mirror the **right-side calendar mini-view + Today's items panel**. Use as the drawer that opens when a meeting is clicked.
- Reference: `grain-02.png` — Mirror the **expanded card pattern** (Workspace Access + Template selector + add tag) inline under the meeting row.

### Empty state
- Reference: `zoom-04.png` — Mirror the **clean centered empty area** style when a filter returns zero results.

---

## Layout rationale

Two-column landing: left rail nav (Header.tsx shared across all routes), main column shows a date-grouped list of meetings (Now → Today → Tomorrow → later). Clicking a meeting opens an inline expanded panel (Grain pattern) rather than navigating away — keeps the user oriented before they `/live`. Record toggle per row makes the recording opt-in obvious.

---

## Components to extract

- `Header` (canonical version, shared across all 5 screens) — driven by `fireflies-05.png` top bar
- `MeetingCard` — Grain-02 grouping card style
- `AgendaPreviewPanel` — Otter.ai-03 right-side mini-calendar pattern
- `EmptyState` — Zoom-04 minimal centered style
