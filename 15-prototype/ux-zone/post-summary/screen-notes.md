# Post-meeting summary — Screen Notes

**Route:** `/summary`
**Purpose:** Show the Smart Summary output (TL;DR, key moments, decisions, participants).

---

## References to mirror

### TL;DR card
- Reference: `zoom-01.png` — Mirror the **"Quick recap" block** at the top: short heading + 3-4 sentence paragraph. This is the canonical TL;DR pattern.
- Reference: `manus-03.png` — Mirror the **structured doc card with Topic + Overview** as an alternate format if the TL;DR needs more structure.
- Reference: `apollo-02.png` — Mirror the **Outcome card** style with a single bold section title and 3-4 sentence body.

### Key moments (timestamped)
- Reference: `grain-04.png` — Mirror the **Chapters + Outcomes sections with right-aligned timestamps** (e.g., `0:18`, `1:04`, `1:16`). Each row is clickable. This is the BEST reference for the key-moments pattern.
- Reference: `fireflies-05.png` — Mirror the **bulleted General Summary list with bolded lead-in phrases** as an alternate dense format.

### Decisions made
- Reference: `apollo-02.png` — Mirror the **multi-section card grid** (Outcome / Next Steps / Pain Points / Objections — each a separate card with a speaker attribution and bullets). Adapt the "Pain Points" and "Objections" pattern for Decisions and Open Questions.
- Reference: `manus-03.png` — Mirror the **Key Points > Decisions > Action Items > Important Information** hierarchy as a compact decisions list.

### Participant list with talk-time bars
- Reference: `fireflies-05.png` — Mirror the **Speaker Talktime panel**: avatar + name + WPM + talk-time donut + percentage per speaker. CANONICAL talk-time pattern.
- Reference: `grain-04.png` — Mirror the **Mike/Rachel timeline bars on the right** with per-speaker segments + percentage badge as an alternate horizontal view.

---

## Layout rationale

Single-column page with progressive disclosure: TL;DR card at top (Zoom Quick recap pattern), then a section-card grid (Apollo Insights pattern) for Key moments / Decisions / Action items preview, then Participants with talk-time bars (Fireflies pattern) at the bottom. The Apollo "Auto-draft email" button at the top-right of the page links to `/follow-up` — natural bridge to the next screen.

---

## Components to extract

- `TldrCard` — Zoom-01 Quick recap pattern
- `KeyMomentRow` — Grain-04 timestamped chapter row
- `DecisionsList` — Apollo-02 multi-section card grid (one card per section)
- `ParticipantTalkTimeRow` — Fireflies-05 talktime panel pattern
