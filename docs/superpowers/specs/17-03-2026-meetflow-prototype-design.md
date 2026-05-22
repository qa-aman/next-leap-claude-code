# MeetFlow Prototype + UX Zone — Design Spec

**Date:** 17-03-2026
**Owner:** Aman Parmar (Senior PM, AI Intelligence pillar)
**Location:** `/15-prototype/`

---

## Goal

Ship a local Next.js prototype that demos the MeetFlow AI Intelligence pillar end-to-end (5 screens), backed by a curated UX Zone of competitor references and reusable components that can later be round-tripped into Figma via Figma MCP.

**Done condition:** `npm run dev` in `/15-prototype` renders 5 navigable routes (pre-meeting → live → post-summary → action-items → follow-up), and `/15-prototype/ux-zone/` contains screenshots + component files for every screen.

---

## Scope

### In scope
- 5-screen prototype mapped to MeetFlow roadmap bets
- UX Zone reference library (screenshots + component specs + React code)
- Master prompt (`PROMPT.md`) for building the prototype from the UX Zone
- Mobbin query list for populating screenshots
- README explaining the workflow

### Out of scope
- Real backend, auth, or persistence
- The actual Mobbin pull (user triggers when ready)
- Scaffolding the Next.js app (the prompt does this)
- Figma component generation (separate session, later)

---

## Screen Map

| # | Route | Screen | Roadmap anchor |
|---|---|---|---|
| 1 | `/` | Pre-meeting (upcoming meetings, join) | Core experience |
| 2 | `/live` | Live meeting (transcript + AI notes panel) | Core experience |
| 3 | `/summary` | Post-meeting summary | Smart Summaries (AI Intelligence pillar) |
| 4 | `/action-items` | Action items with confidence scoring v2 | Active sprint (17-03-2026 to 28-03-2026) |
| 5 | `/follow-up` | Smart follow-up composer | Smart Follow-Up (April 2026 launch) |

---

## Folder Structure

```
/15-prototype
  PROMPT.md                       # Master prompt to build the prototype
  MOBBIN-QUERIES.md               # Reproducible Mobbin search queries
  README.md                       # How to use this folder
  /ux-zone
    /pre-meeting
      /screenshots                # Mobbin PNGs + source.json
      /components
        /<ComponentName>
          spec.md                 # Anatomy, variants, states, sources
          tokens.json             # Colors, typography, spacing
          Component.tsx           # Working React component
      screen-notes.md             # Layout rationale + reference mapping
    /live-meeting/   (same structure)
    /post-summary/   (same structure)
    /action-items/   (same structure)
    /follow-up/      (same structure)
  /app                            # Next.js 14 App Router (5 routes)
  /components/ui                  # shadcn/ui primitives
  /lib
    mock-data.ts                  # 3 realistic MeetFlow meetings
    store.ts                      # Zustand store
```

---

## Tech Stack (confirmed)

- Next.js 14 (App Router)
- TypeScript
- Tailwind CSS
- shadcn/ui
- Zustand (state)
- Dark mode default, Linear/Granola-inspired aesthetic

---

## Workflow

1. **Populate UX Zone** — user runs Mobbin queries from `MOBBIN-QUERIES.md` and saves screenshots into `ux-zone/<screen>/screenshots/` with a `source.json` per file (app, url, fetch date)
2. **Annotate screens** — user (or Claude) fills in `screen-notes.md` per screen, picking which references to mirror
3. **Run the prompt** — user runs `PROMPT.md` in a fresh Claude Code session in `/15-prototype`; Claude scaffolds Next.js, builds each screen, saves components into `ux-zone/<screen>/components/`
4. **Iterate** — components live in UX Zone, are imported by `/app` routes
5. **Figma handoff (later)** — separate session uses Figma MCP `figma-code-connect` to map `Component.tsx` → Figma components

---

## Mobbin Strategy

- **Build-time, not runtime.** Mobbin populates the UX Zone once; the prompt reads local files only.
- **4 queries per screen** (20 total) — see `MOBBIN-QUERIES.md`
- **Target:** 5-10 saved screenshots per screen after curation
- **Each screenshot gets a `source.json`** with app name, source URL, fetch date (DD-MM-YYYY) for anti-hallucination

---

## Prompt Structure (XML-tagged)

`PROMPT.md` uses these sections:
- `<context>` — MeetFlow company snapshot, PM role, roadmap anchors
- `<references>` — UX Zone paths, what to read per screen
- `<requirements>` — Per-screen functional requirements + design principles
- `<tech_stack>` — Versions, libraries, conventions
- `<output>` — File-by-file build order, naming, locations
- `<constraints>` — Hard rules (DD-MM-YYYY, no invented metrics, etc.)
- `<verification>` — Self-checks before delivery
- `<acceptance>` — Done conditions

Scored against `.claude/rules/prompt-writing.md` rubric; target >95/100.

---

## Constraints

- All dates DD-MM-YYYY (filenames, content, frontmatter)
- No invented metrics — only numbers from `03-product-knowledge/` and `04-strategy/`
- No em dashes in user-facing copy (commas or hyphens)
- No emojis
- Workshop "today" is 17-03-2026
- Prototype runs offline (mock data, no live APIs)

---

## Acceptance Criteria

- [ ] `/15-prototype/PROMPT.md` exists and scores >95/100 on prompt-writing rubric
- [ ] `/15-prototype/MOBBIN-QUERIES.md` lists 4 queries per screen
- [ ] `/15-prototype/ux-zone/` has 5 screen folders, each with `screenshots/`, `components/`, `screen-notes.md`
- [ ] `/15-prototype/README.md` explains the 5-step workflow
- [ ] After user populates UX Zone and runs PROMPT.md, `npm run dev` shows 5 working routes

---

## Figma MCP Handoff (future, not this session)

Once UX Zone is populated:
- `figma-code-connect` maps each `Component.tsx` to a Figma component
- `figma-generate-design` builds frames from `spec.md`
- `tokens.json` becomes a Figma variable collection

No work required in this design — the folder structure enables it.
