# Build MeetFlow Prototype from UX Zone

You are building a local Next.js prototype of MeetFlow's AI Intelligence pillar across 5 navigable screens. The prototype is a demo asset for stakeholder reviews and a foundation for future Figma round-tripping via Figma MCP. Be surgical: build only what these requirements specify, no extra features, no speculative abstractions.

---

<context>

**Product:** MeetFlow — AI-powered meeting assistant. Series B ($18M, Benchmark, April 2025). $3M ARR, 15,000 users (12,000 Free, 2,800 Pro, 200 Team). Pro $15/mo, Team $49/seat/mo.

**Your role (the human you are building this for):** Senior PM owning the AI Intelligence pillar — Smart Summaries, Action Item Confidence Scoring, Meeting Pattern Insights.

**Workshop "today":** 17-03-2026. Date format DD-MM-YYYY everywhere.

**Roadmap anchors this prototype demos:**
- Smart Summaries (AI Intelligence pillar, ongoing)
- Action Item Confidence Scoring v2 (active sprint, 17-03-2026 to 28-03-2026)
- Smart Follow-Up (launches April 2026)

**Full product context (read before building):**
- `/Users/amanparmar/Documents/AI-PM/Projects/next-leap-claude-code/03-product-knowledge/company.md`
- `/Users/amanparmar/Documents/AI-PM/Projects/next-leap-claude-code/04-strategy/product-vision.md`

</context>

---

<references>

**UX Zone (your visual + structural source of truth):**
Absolute path: `/Users/amanparmar/Documents/AI-PM/Projects/next-leap-claude-code/15-prototype/ux-zone/`

For each of the 5 screens, the UX Zone contains:
- `<screen>/screenshots/` — Mobbin PNGs of competitor references, each with a `.source.json` sibling listing app, URL, fetch date, and why it was kept
- `<screen>/screen-notes.md` — the human's notes on which references to mirror per UI region (header, content, sidebar, etc.)
- `<screen>/components/` — where you save reusable components you build (one folder per component: `spec.md`, `tokens.json`, `Component.tsx`)

**Before building any screen, you MUST:**
1. Read `<screen>/screen-notes.md` end-to-end
2. List every file in `<screen>/screenshots/` so you know what references exist
3. For each reference cited in `screen-notes.md`, open its `.source.json` and confirm the file exists. If a cited reference is missing, ask the user before proceeding.

**Mirror discipline:** For every component you build, name in `spec.md` exactly which screenshot(s) it draws from (filename + which UI element). Vague "inspired by Granola" is forbidden — use "header pattern from `granola-summary-03.png` top bar; key-moments card grid from `fathom-recap-02.png` middle section."

</references>

---

<tech_stack>

- **Framework:** Next.js 14 (App Router) + TypeScript (strict mode)
- **Styling:** Tailwind CSS + shadcn/ui (init with `npx shadcn@latest init`)
- **State:** Zustand (one store in `lib/store.ts`)
- **Theme:** Dark mode default. Aesthetic: Linear-meets-Granola — dense, calm, monospace-accented, generous whitespace inside cards
- **Data:** Mock only. Seed 3 realistic meetings in `lib/mock-data.ts` (use plausible meeting titles like "Pro churn deep-dive", "Smart Follow-Up design review", "Q1 customer interview synthesis"; use DD-MM-YYYY dates centered on 17-03-2026)
- **No backend, no auth, no live APIs.** Everything in-memory.

</tech_stack>

---

<requirements>

Build 5 routes mapped to these screens. Each route lives in `/app/<route>/page.tsx`.

### 1. `/` — Pre-meeting
**Purpose:** Show upcoming meetings, let user "join with MeetFlow"
**Must include:**
- Header with MeetFlow wordmark, user avatar (placeholder), nav to other 4 screens
- List of 3 upcoming meetings (title, time, participants, "Join" button)
- Agenda preview drawer/panel that opens when a meeting is clicked
- Empty state visible if list is filtered to zero

### 2. `/live` — Live meeting
**Purpose:** Simulate the in-meeting experience
**Must include:**
- Left: live transcript area (use static mock transcript that auto-scrolls a fixed snippet on mount; do not implement real audio)
- Right: AI Notes panel (3-4 bullet "AI-captured" notes)
- Top: recording controls (mute, stop, time elapsed)
- Bottom: speaker chips showing who's talking

### 3. `/summary` — Post-meeting summary
**Purpose:** Show the Smart Summary output
**Must include:**
- TL;DR card at top (3-4 sentences)
- Key moments section (timestamped highlights, clickable)
- Decisions made section
- Participant list with talk-time bars

### 4. `/action-items` — Action items with confidence v2
**Purpose:** Demo Action Item Confidence Scoring v2 (active sprint feature)
**Must include:**
- List of 6-8 action items, each with: title, assignee, due date (DD-MM-YYYY), confidence badge (High/Medium/Low with a numeric % shown on hover/inline)
- Confidence badge visually distinct (color + icon)
- Filter chips: All / High / Needs review (Low + Medium)
- Per-item action: Edit, Confirm, Reject
- Empty state for "Needs review" filter when none

### 5. `/follow-up` — Smart follow-up composer
**Purpose:** Demo Smart Follow-Up (April 2026 launch)
**Must include:**
- Recipient picker (multi-select chips, prefilled with meeting participants)
- AI-drafted email body (editable textarea, prefilled with a realistic draft tying back to action items)
- "Tone" selector: Concise / Warm / Direct (changing tone swaps the prefilled draft)
- Subject line
- "Send" button (toast on click; no actual send)

---

### Design principles (apply to every screen)
- Dark mode default. One theme.
- Tailwind utility classes only. No inline styles. No CSS modules.
- shadcn primitives for Button, Card, Input, Badge, Dialog, Tabs, Toast — do not rebuild these from scratch
- One `<Header />` component shared across all 5 routes
- Keyboard navigable (focus rings visible)
- No emojis. No em dashes in any user-facing copy (use commas or hyphens)

</requirements>

---

<output>

**Build in this exact order. Stop after each numbered step long enough to verify it works before moving on.**

1. **Scaffold project** in `/Users/amanparmar/Documents/AI-PM/Projects/next-leap-claude-code/15-prototype/`:
   - Run `npx create-next-app@latest . --typescript --tailwind --app --src-dir=false --import-alias="@/*" --no-eslint` (use `.` so it scaffolds into the existing folder — confirm `app/`, `package.json`, `tailwind.config.ts` appear)
   - Run `npx shadcn@latest init` (defaults, dark mode, slate base)
   - Install Zustand: `npm install zustand`

2. **Create shared scaffolding:**
   - `lib/mock-data.ts` (3 meetings, action items, transcript snippets)
   - `lib/store.ts` (Zustand store: current meeting, action item filter, follow-up draft state)
   - `components/Header.tsx` (nav to all 5 routes, active state)
   - Apply dark mode in `app/layout.tsx`

3. **Build screens in this order — for each screen, follow the per-screen loop below:**
   - 3a. `/` (pre-meeting)
   - 3b. `/summary` (post-meeting summary)
   - 3c. `/action-items`
   - 3d. `/follow-up`
   - 3e. `/live`

   **Per-screen loop (repeat for each):**
   - i. Read `ux-zone/<screen>/screen-notes.md`
   - ii. List `ux-zone/<screen>/screenshots/` and read each `.source.json`
   - iii. Build `app/<route>/page.tsx`
   - iv. Extract each reusable component into `ux-zone/<screen>/components/<ComponentName>/Component.tsx`
   - v. For each component, write `spec.md` (anatomy, variants, states, exact reference filenames) and `tokens.json` (the Tailwind values you used: colors, spacing, radii, type)
   - vi. Import the component from its UX Zone location into `app/<route>/page.tsx`

4. **Wire navigation** in `Header.tsx` so all 5 routes link to each other with active-state styling.

5. **Run verification (see `<verification>` section).**

6. ### AWAITING APPROVAL
   Stop here. Report back with: list of files created, screenshot or text summary of each rendered route, and any references that were missing or unclear. Wait for human approval before any further work.

</output>

---

<constraints>

Every rule below is non-negotiable. Each has a verification check.

| Constraint | Verification |
|---|---|
| All dates in DD-MM-YYYY format (no ISO, no US) | `grep -rE "[0-9]{4}-[0-9]{2}-[0-9]{2}\|[0-9]{2}/[0-9]{2}/[0-9]{4}" 15-prototype/app 15-prototype/lib` returns nothing |
| No em dashes in user-facing copy | `grep -rn "—" 15-prototype/app 15-prototype/components 15-prototype/lib` returns nothing |
| No emojis anywhere | `grep -rPn "[\x{1F300}-\x{1FAFF}\x{2600}-\x{27BF}]" 15-prototype/app 15-prototype/components 15-prototype/lib` returns nothing |
| No invented business metrics | Any number cited as a MeetFlow stat must come from `03-product-knowledge/company.md` or `04-strategy/product-vision.md`. If a screen needs a number not in those files, use a clearly-mock value labeled in mock-data.ts |
| Every component in UX Zone has spec.md + tokens.json + Component.tsx | `find 15-prototype/ux-zone -type d -name "components" -exec ls {} \;` — every component folder has all 3 files |
| Mirror discipline: every component spec.md names specific screenshot filenames | `grep -L "\.png" 15-prototype/ux-zone/*/components/*/spec.md` returns nothing |
| 5 routes exist | `ls 15-prototype/app` shows `page.tsx`, `live/`, `summary/`, `action-items/`, `follow-up/` |
| `npm run dev` starts without errors | Run it; check terminal output |
| TypeScript strict mode passes | `npx tsc --noEmit` exits 0 |
| No new top-level files outside the folders listed in `<output>` | `ls 15-prototype` matches the documented structure |
| No backend / no API routes | `find 15-prototype/app -name "route.ts"` returns nothing |
| No additions to package.json beyond Next, React, Tailwind, shadcn deps, Zustand | Read `package.json` and confirm |

</constraints>

---

<anti_hallucination>

- **Verify before claim.** If you reference a Mobbin screenshot, the file must exist on disk. If a `screen-notes.md` cites a reference that is missing, stop and ask the human — do not invent.
- **Omit, do not fabricate.** If a screen-notes.md is empty or sparse, build only what the requirements specify and flag the gap. Do not invent design decisions.
- **No invented APIs or libraries.** Use only what is listed in `<tech_stack>`. If you think you need an extra library, stop and ask.
- **No invented MeetFlow numbers.** ARR, user counts, churn, NPS, accuracy figures must come verbatim from `03-product-knowledge/company.md` or `04-strategy/product-vision.md`. Cite the source file in a comment when you use one.
- **Date discipline.** "Today" is 17-03-2026 for any due dates, timestamps, or "last updated" labels.

</anti_hallucination>

---

<verification>

Before reporting done, run every check below. Paste the output (or "PASS") next to each item in your report.

1. **Dev server boots:** `cd 15-prototype && npm run dev` — confirm no errors in first 10 seconds; kill the process.
2. **Type check:** `cd 15-prototype && npx tsc --noEmit` — exit 0.
3. **Date format:** `grep -rEn "[0-9]{4}-[0-9]{2}-[0-9]{2}|[0-9]{2}/[0-9]{2}/[0-9]{4}" 15-prototype/app 15-prototype/lib 15-prototype/components` — empty.
4. **No em dashes:** `grep -rn "—" 15-prototype/app 15-prototype/components 15-prototype/lib` — empty.
5. **No emojis:** `grep -rPn "[\x{1F300}-\x{1FAFF}\x{2600}-\x{27BF}]" 15-prototype/app 15-prototype/components 15-prototype/lib` — empty.
6. **All 5 routes exist:** `ls 15-prototype/app/{live,summary,action-items,follow-up}/page.tsx 15-prototype/app/page.tsx` — every file resolves.
7. **UX Zone completeness:** for each of 5 screens, every folder in `ux-zone/<screen>/components/` has all 3 files (`spec.md`, `tokens.json`, `Component.tsx`).
8. **Reference fidelity:** every `spec.md` in `ux-zone/*/components/*/` contains at least one `.png` filename citation.
9. **Self-audit against failure modes** (next section).

</verification>

---

<failure_modes>

Before delivering, check yourself against each of these. Fix any that apply.

1. **Built screens before reading `screen-notes.md`** — re-read; rebuild any screen where references were ignored.
2. **Components live in `/components/` instead of `/ux-zone/<screen>/components/`** — move them; the UX Zone is the canonical home.
3. **`spec.md` files say "inspired by Granola"** without naming specific screenshots — rewrite with explicit filename + region citations.
4. **Used `Date.now()` or system date** — every date must trace to 17-03-2026 (workshop today) or DD-MM-YYYY mock data.
5. **Added a backend route, auth, or live API call** — delete it; the prototype is offline-only.
6. **Invented a MeetFlow number** (ARR, churn, accuracy %, user count) — replace with the verbatim value from `03-product-knowledge/company.md`, or remove the claim.
7. **Built more than the 5 specified screens, or extra "nice to have" routes** — delete them.
8. **Used a UI library other than shadcn/ui** (e.g., Radix directly, Mantine, Chakra) — replace with shadcn primitives.
9. **Implemented real audio capture, real recording, or websocket transcript streaming** — replace with the static mock-transcript pattern; this is a visual prototype.
10. **Skipped the per-component `tokens.json`** — every component folder needs it for Figma round-trip later.

</failure_modes>

---

<acceptance>

You are done when:
- All 12 items in `<constraints>` pass their verification check
- All 9 items in `<verification>` pass
- All 10 items in `<failure_modes>` have been audited and none apply
- Final report posted with: file tree of `/15-prototype/app`, file tree of `/15-prototype/ux-zone`, list of any missing references flagged to the human, and the `### AWAITING APPROVAL` marker

</acceptance>

---

Start by reading `03-product-knowledge/company.md`, `04-strategy/product-vision.md`, then `ls 15-prototype/ux-zone/` and `cat 15-prototype/ux-zone/*/screen-notes.md`. Report what you find before running any `create-next-app` or write commands.
