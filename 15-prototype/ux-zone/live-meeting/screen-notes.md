# Live meeting — Screen Notes

**Route:** `/live`
**Purpose:** Simulate the in-meeting experience: transcript + AI notes + recording controls.

---

## References to mirror

### Recording controls (bottom bar)
- Reference: `dialpad-01.png` — Mirror the **full bottom toolbar**: Details / Chat / Participants / AI tabs on left, Unmute / Start video / Share / Reactions / Settings / More in center, Stop / Host / End on right. Use as the canonical control layout.
- Reference: `otterai-03.png` — Mirror the **Stop Notetaker pill + REC timer + secondary icons** for the in-call recording state indicator.

### Live transcript (left column)
- Reference: `dialpad-01.png` — Mirror the **left-rail Transcripts/Notes tabs + Turn off AI toggle + Listening indicator + Add action item bottom anchor**. This is the canonical live-transcript pane.
- Reference: `otterai-03.png` — Mirror the **timestamped speaker blocks with inline embedded media** for the transcript stream.
- Reference: `fireflies-04.png` — Mirror the **AI Filters chips above transcript** (Tasks / Questions / Metrics / Date) for the optional filter rail.

### AI Notes panel (right column)
- Reference: `dialpad-02.png` — Mirror the **Notes tab empty state ("No meeting notes yet…") + inline "Add action item" composer with Assign to + Cancel/Add buttons**. Use this as the AI Notes panel default state.
- Reference: `zoom-05.png` — Mirror the **AI Companion welcome state with prompt chips** (Catch me up / Was my name mentioned / What are action items). Use for the panel's idle state.

### Speaker chips (bottom of video)
- Reference: `dialpad-01.png` — Mirror the **Sam Lee speaker chip with red muted-mic indicator + small participant badge** anchored to the video area bottom-left.
- Reference: `fireflies-04.png` — Mirror the **Speaker Talktime sidebar** (avatar + WPM + talk-time donut + %) for a richer participant view if we add one.

---

## Layout rationale

Three-zone in-meeting screen: left transcript (60% width), right AI Notes panel (40% width), bottom call controls full-width. Transcript auto-scrolls a mock snippet; AI Notes panel shows 3-4 prefilled AI bullets so the value prop is visible immediately. Speaker chips anchor to the video area so the user always knows who is talking.

---

## Components to extract

- `RecordingControls` — Dialpad-01 bottom toolbar pattern
- `TranscriptStream` — Dialpad-01 left rail + Otter.ai-03 speaker block style
- `AiNotesPanel` — Dialpad-02 Notes tab pattern with inline action-item composer
- `SpeakerChip` — Dialpad-01 chip style anchored to video corner
