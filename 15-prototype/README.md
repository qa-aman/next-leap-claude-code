# MeetFlow Prototype

A local Next.js prototype demoing the MeetFlow AI Intelligence pillar across 5 screens, built from a curated UX Zone of competitor references.

**Workshop today:** 17-03-2026
**Owner:** Aman Parmar (Senior PM, AI Intelligence)

---

## What's in this folder

| Path | Purpose |
|---|---|
| `PROMPT.md` | Master prompt — feed to Claude Code to build the prototype |
| `MOBBIN-QUERIES.md` | Reproducible Mobbin search queries for the UX Zone |
| `ux-zone/` | Reference library: screenshots + component specs + React code per screen |
| `app/` | Next.js 14 App Router (created by running `PROMPT.md`) |
| `components/ui/` | shadcn/ui primitives (created by running `PROMPT.md`) |
| `lib/` | Mock data + Zustand store (created by running `PROMPT.md`) |

---

## The 5 Screens

| # | Route | Screen | Roadmap anchor |
|---|---|---|---|
| 1 | `/` | Pre-meeting | Core experience |
| 2 | `/live` | Live meeting | Core experience |
| 3 | `/summary` | Post-meeting summary | Smart Summaries |
| 4 | `/action-items` | Action items + confidence | Active sprint |
| 5 | `/follow-up` | Smart follow-up composer | April 2026 launch |

---

## Workflow (5 steps)

### Step 1 — Populate UX Zone with Mobbin
Open `MOBBIN-QUERIES.md`. Run each query via Mobbin MCP. Save 5-10 curated screenshots per screen into `ux-zone/<screen>/screenshots/` with a matching `source.json`.

### Step 2 — Write screen-notes
For each screen, fill in `ux-zone/<screen>/screen-notes.md`. Pick 2-3 references per UI region and note what to mirror.

### Step 3 — Run PROMPT.md
In a fresh Claude Code session inside `/15-prototype`, paste the contents of `PROMPT.md`. Claude will:
- Scaffold Next.js 14 + TS + Tailwind + shadcn/ui + Zustand
- Build each screen route
- Save reusable components into `ux-zone/<screen>/components/<Component>/` with `spec.md`, `tokens.json`, `Component.tsx`
- Wire navigation, seed mock data

### Step 4 — Run the prototype
```
cd 15-prototype
npm install
npm run dev
```
Open http://localhost:3000 and walk through the 5 screens.

### Step 5 — Figma handoff (later, separate session)
Use Figma MCP `figma-code-connect` to map each `Component.tsx` to a Figma component, and `figma-generate-design` to build frames from `spec.md`. The UX Zone structure is designed to support this.

---

## Tech Stack

- Next.js 14 (App Router)
- TypeScript
- Tailwind CSS
- shadcn/ui
- Zustand
- Dark mode default, Linear/Granola-inspired

---

## Rules (carried from project CLAUDE.md)

- Dates: DD-MM-YYYY everywhere
- No invented metrics — only numbers from `03-product-knowledge/` and `04-strategy/`
- No em dashes, no emojis
- Prototype runs offline (mock data, no live APIs)

---

## Spec

Full design spec: `../docs/superpowers/specs/17-03-2026-meetflow-prototype-design.md`
