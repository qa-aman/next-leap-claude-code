# Mobbin Queries — MeetFlow Prototype UX Zone

Run these in a Claude Code session with the Mobbin MCP connected. Each query returns screens you save into `ux-zone/<screen>/screenshots/` with a matching `source.json`.

**Target:** 5-10 curated screenshots per screen (so run the query, then keep only the strongest references).

**Date format for `source.json`:** DD-MM-YYYY.

---

## How to run

```
For each query below, call:
  mcp__mobbin__search_screens with the query string.

Then for each kept screenshot, save:
  ux-zone/<screen>/screenshots/<app-slug>-<short-label>-NN.png
  ux-zone/<screen>/screenshots/<same-filename>.source.json

source.json schema:
{
  "app": "Granola",
  "screen_title": "Meeting summary view",
  "url": "https://mobbin.com/...",
  "fetched_on": "17-03-2026",
  "why_kept": "Two-column layout with key moments + transcript, mirrors target for post-summary"
}
```

---

## Queries by Screen

### 1. Pre-meeting (`ux-zone/pre-meeting/`)

- `calendar meeting list`
- `upcoming meetings dashboard`
- `join video call`
- `meeting agenda prep`

**Reference apps to prioritize:** Granola, Fathom, Notion Calendar, Cron, Fellow

---

### 2. Live meeting (`ux-zone/live-meeting/`)

- `live transcription`
- `meeting recording interface`
- `real-time notes`
- `video call sidebar`

**Reference apps to prioritize:** Granola, Otter, Fireflies, Zoom AI Companion, Loom

---

### 3. Post-meeting summary (`ux-zone/post-summary/`)

- `meeting summary`
- `AI summary card`
- `transcript highlights`
- `meeting recap`

**Reference apps to prioritize:** Granola, Fathom, Otter, Notion AI, Read.ai

---

### 4. Action items (`ux-zone/action-items/`)

- `task list with confidence`
- `AI suggested tasks`
- `action items dashboard`
- `todo with assignee`

**Reference apps to prioritize:** Linear, Height, Motion, Asana AI, Granola action items

---

### 5. Smart follow-up (`ux-zone/follow-up/`)

- `email draft composer`
- `AI generated email`
- `follow up message`
- `send to recipients`

**Reference apps to prioritize:** Superhuman, HEY, Shortwave, Lavender, Granola follow-ups

---

## After running

1. Curate down to 5-10 screenshots per screen (delete the rest)
2. Fill in `screen-notes.md` for each screen — pick 2-3 references per UI region (header, content, sidebar) and note what to mirror
3. Run `PROMPT.md` to build the prototype
