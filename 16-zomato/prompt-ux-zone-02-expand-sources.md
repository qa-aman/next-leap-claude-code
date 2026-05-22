# UX Zone 02, Expand the source surface

Extend the existing Zomato UX Zone at `/Users/amanparmar/Documents/AI-PM/Projects/next-leap-claude-code/16-zomato/ux-zone/` from one blog page to four production pages, so the component library covers real Zomato UI (buttons, cards, search, filters, forms, modals, ratings, price tags, image carousels) instead of just article chrome.

Discipline rule: extend, do not rewrite. Reuse existing tokens and components. Only add what the new pages actually show. No invented components.

## Goal

Done when: the existing `ux-zone/` folder contains 8 new components extracted from 3 new source pages, each with `index.html` + `style.css` + `README.md`, tokens.json grows to cover any new values, the gallery `index.html` shows all components in one view, and `VERIFICATION.md` is updated with pass/fail per new check.

## Inputs

- Existing kit (do not delete or replace): `/Users/amanparmar/Documents/AI-PM/Projects/next-leap-claude-code/16-zomato/ux-zone/`
- Existing executor prompt for reference: `/Users/amanparmar/Documents/AI-PM/Projects/next-leap-claude-code/16-zomato/prompt-ux-zone.md`
- New source pages (Playwright fetch, record date in DD-MM-YYYY in VERIFICATION.md):
  1. https://www.zomato.com/ (home)
  2. https://www.zomato.com/ncr/restaurants (or whichever listing page renders without login)
  3. https://www.zomato.com/ncr/cafe-delhi-heights-1-connaught-place-new-delhi (a stable restaurant detail page; if 404, pick any open detail page and record the URL)
- Existing tokens: read `ux-zone/tokens.json` and `ux-zone/tokens.css` before adding any new value.

## Outputs (all within existing ux-zone/ folder)

| Path | Action |
|---|---|
| `ux-zone/components/<new-name>/index.html` | create, one per new component |
| `ux-zone/components/<new-name>/style.css` | create, uses tokens |
| `ux-zone/components/<new-name>/README.md` | create, with source URL + selector + verbatim quote |
| `ux-zone/components/<new-name>/reference.png` | create, 1280px screenshot |
| `ux-zone/tokens.json` | edit, append only when a value cannot be expressed with existing tokens |
| `ux-zone/tokens.css` | edit, mirror new tokens.json entries |
| `ux-zone/assets/images/` | add new images, preserve original filenames |
| `ux-zone/assets/icons/` | add new SVG icons |
| `ux-zone/index.html` | edit, add a new `<section>` per new component |
| `ux-zone/README.md` | edit, append new components to the component-list table |
| `ux-zone/VERIFICATION.md` | edit, append a "Phase 02" section with each check |

## New components to extract (only if present on the listed pages)

Target list, drop any that are genuinely absent:
- `cta-button` (primary, secondary, ghost; sizes sm/md/lg; states default/hover/focus/active/disabled)
- `search-input` (the header search field with the location + query split)
- `nav-pill` (the filter pills above listings: cuisines, ratings, cost)
- `restaurant-card` (image, name, cuisines, rating chip, cost-for-two, delivery time)
- `rating-chip` (the colored rating box, e.g. 4.2 green, 3.5 yellow, 2.5 red)
- `price-tag` (cost-for-two, discount/offer pill)
- `image-carousel` (restaurant detail photo gallery; left/right controls, dot indicators)
- `breadcrumb` (City > Locality > Restaurant)
- `modal-dialog` (any login / address modal that appears on interaction)

For each, include source URL + source selector + verbatim source text in README.

## Constraints (each has a verifiable check)

| # | Constraint | Check |
|---|---|---|
| C1 | All new files live inside `ux-zone/` | `find ux-zone -newer prompt-ux-zone.md -type f \| grep -v ux-zone` returns empty |
| C2 | Reuse existing tokens first; only add new ones when no existing token fits | Diff `tokens.json` before/after; every new entry has a `source:` field that says why it could not reuse an existing token |
| C3 | No hardcoded hex in any component CSS | `grep -rE '#[0-9a-fA-F]{3,8}' ux-zone/components/*/style.css` empty |
| C4 | No hotlinks in HTML/CSS | `grep -rE 'https?://[^ "]+\.(png\|jpg\|webp\|svg\|woff2?\|ttf)' ux-zone/components ux-zone/index.html` empty |
| C5 | Every new component has a `reference.png` next to it | `find ux-zone/components -type d -mindepth 1 \| while read d; do test -f "$d/reference.png" \|\| echo MISSING $d; done` empty |
| C6 | tokens.json valid | `python3 -m json.tool ux-zone/tokens.json` exit 0 |
| C7 | Every new component README cites source URL + selector + verbatim quote | grep for "Source URL", "Source selector", "Source quote" in each new README |
| C8 | DD-MM-YYYY only | `grep -rE '\b[0-9]{4}-[0-9]{2}-[0-9]{2}\b' ux-zone` returns only token-source values intentionally formatted otherwise |
| C9 | No em dashes in md | `grep -r '—' ux-zone --include='*.md'` empty |
| C10 | Class prefix `uxz-<component-name>__` preserved | `grep -rE 'class="[^"]+"' ux-zone/components/<new>/index.html`; manual confirm all classes match prefix |
| C11 | Gallery renders new sections, zero console errors | Open `ux-zone/index.html` via local http server in Playwright; assert `browser_console_messages` empty |

## Tools / skills / models

- Playwright MCP (`mcp__plugin_playwright_playwright__*`) for navigation, snapshot, evaluate, screenshot. WebFetch will likely fail again (zomato.com is client-rendered) so do not waste a call on it.
- `browser_evaluate` to pull `getComputedStyle` for each new component and compare against existing tokens before adding new ones.
- `Bash` + `curl -L -o` to self-host new images and icons.
- Reuse the local server pattern from phase 01: `cd ux-zone && python3 -m http.server 8765`. Navigate Playwright to `http://localhost:8765/`.
- Do not use frameworks. Plain HTML + CSS + JSON.

## Process (strict order)

1. Read existing `tokens.json`, `tokens.css`, `README.md`, `VERIFICATION.md` so you know what already exists.
2. Open each new source URL via Playwright at 1280px. Take a full-page screenshot to `ux-zone/assets/reference/<page>-1280.png`.
3. For each candidate component, locate its selector on the live page. If absent across all three pages, drop it from the inventory.

### AWAITING APPROVAL

Show the user: (a) the final component inventory you will build (with source page next to each), (b) any new tokens you plan to add (with the existing token you considered and why it did not fit), (c) the asset count delta. Wait for explicit "go".

4. For each approved component: extract HTML structure, computed CSS, all interactive states. Write `index.html` + `style.css` + `README.md` + `reference.png`. Use existing tokens; only mint a new token when no existing one fits.
5. Append new tokens to `tokens.json` and mirror in `tokens.css`.
6. Append new gallery sections to `ux-zone/index.html` (one per new component).
7. Append new entries to `ux-zone/README.md` component-list table.
8. Run the full Verification section. Append a "Phase 02" block to `VERIFICATION.md` with command + result per check.

## Verification (executor runs before declaring done)

- `python3 -m json.tool ux-zone/tokens.json` exits 0
- `grep -rE '#[0-9a-fA-F]{3,8}' ux-zone/components/*/style.css` empty
- `grep -rE 'https?://[^ "]+\.(png|jpg|woff2|svg|ttf)' ux-zone/components ux-zone/index.html ux-zone/tokens.css` empty
- Asset resolver script from phase 01 (reproduced in VERIFICATION.md) reports 0 missing
- Playwright at `http://localhost:8765/`: 0 console errors
- Visual diff per new component: open `index.html` next to `reference.png`, subjective fidelity score in VERIFICATION.md, must be >= 8

## Failure modes

1. Listing/detail page requires login or location, blocking extraction. Defense: log the URL and HTTP status in VERIFICATION.md; pick the closest open alternative; do not fake a screenshot.
2. New tokens are added that duplicate existing ones (e.g., two grays close in value). Defense: before adding, grep `tokens.json` for any value within delta-E 5 of the candidate; if found, reuse and document the decision.
3. A component looks correct at 1280px but breaks at 768px. Defense: take screenshots at 360/768/1280 and add `@media` rules where layout shifts.
4. Class collisions with phase-01 components when both are rendered together in a prototype. Defense: keep the `uxz-<name>__element` BEM prefix; load phase-01 + new components on a single test page and visually confirm no styles bleed.
5. State variants (hover/focus/disabled) are skipped because they need interaction. Defense: capture them via `:hover` + `:focus` + `[disabled]` selectors and screenshot with Playwright `evaluate` toggling classes.
6. Rating-chip color logic invented. Defense: extract the threshold-to-color mapping from the live page DOM (data attributes or class names), not from intuition; if not present in DOM, document as "derived from observed values: 4.0+ green, 3.0-3.9 orange, <3.0 red" with the live samples cited.
7. Verification skipped. Defense: VERIFICATION.md Phase 02 block is a done-condition; without it, task is incomplete.

## Audience

`VERIFICATION.md` reads as a pure checklist (next Claude session + Aman). Component READMEs are read by PMs and teammates; banned jargon: "atoms/molecules/organisms" without a one-line definition. Framing rule for READMEs: action first, "use this when you need X."

---

Start by reading `ux-zone/tokens.json`, `ux-zone/README.md`, and `ux-zone/VERIFICATION.md`, then navigating Playwright to https://www.zomato.com/ at 1280px and taking a full-page screenshot to `ux-zone/assets/reference/home-1280.png`.
