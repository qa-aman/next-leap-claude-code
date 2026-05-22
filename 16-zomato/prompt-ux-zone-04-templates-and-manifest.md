# UX Zone 04, Page templates + AI-readable manifest

Add composed page templates (landing, listing, restaurant detail, checkout) and a single `UX-ZONE.md` contract to `/Users/amanparmar/Documents/AI-PM/Projects/next-leap-claude-code/16-zomato/ux-zone/`, so a prompt like "build a Zomato-style restaurant page" works zero-shot for a fresh Claude session.

Discipline rule: templates compose existing components only. No new component CSS. If a template needs something that does not exist, stop and surface it; do not silently invent.

## Goal

Done when `ux-zone/templates/` contains four runnable templates, `ux-zone/UX-ZONE.md` is the single manifest a future Claude session loads to use the kit, the gallery `index.html` links to each template, and VERIFICATION.md Phase 04 has all checks passing.

## Inputs

- Existing kit: `/Users/amanparmar/Documents/AI-PM/Projects/next-leap-claude-code/16-zomato/ux-zone/`
- All current components under `ux-zone/components/`
- Tokens: `ux-zone/tokens.json`, `ux-zone/tokens.css`
- Phase 02 components if present (restaurant-card, rating-chip, search-input, nav-pill, etc.). If phase 02 has not been run, build only templates that can compose from phase 01 components and document the limitation.

## Outputs (additions inside existing folder)

| Path | Format | What it contains |
|---|---|---|
| `ux-zone/templates/landing/index.html` | HTML | Full landing page composed from components |
| `ux-zone/templates/listing/index.html` | HTML | Restaurant listing with filters and cards (requires phase 02) |
| `ux-zone/templates/restaurant-detail/index.html` | HTML | Detail page with carousel, info, related (requires phase 02) |
| `ux-zone/templates/article/index.html` | HTML | Article page using only phase 01 components (header, hero, prose, footer) |
| `ux-zone/templates/<name>/README.md` | Markdown | Which components, props, where to swap content |
| `ux-zone/UX-ZONE.md` | Markdown | Single-file manifest: every component, every prop, composition rules, examples |
| `ux-zone/index.html` | edit | Add a "Templates" section linking each |
| `ux-zone/VERIFICATION.md` | edit | Append Phase 04 block |

## The manifest, `UX-ZONE.md`

This is the most important artifact. A fresh Claude session loads it and knows: which components exist, which props each takes, which CSS files to link, which images are safe to use, which patterns combine into a page, and what is forbidden.

Required sections:

1. **What this kit is.** One paragraph.
2. **Hard rules.** Bullet list, e.g., "Always link tokens.css first", "Never edit tokens.css per prototype", "Use uxz- prefixed classes".
3. **Token cheatsheet.** Table of the 12 most-used tokens with their CSS variable name + value + when to use.
4. **Component catalog.** Table: name, what it is, required props, optional props, CSS file path, source URL, source selector, available variants. One row per component.
5. **Composition rules.** How components nest, e.g., "tag-chip lives inside hero-article", "footer is always last child of body".
6. **Templates.** Four short paragraphs naming the four templates and when to use each.
7. **For a fresh Claude session.** A boilerplate prompt the user can paste: "You are building a prototype in folder X. Use the UX Zone at this path. Read `UX-ZONE.md` before anything else. Use only components listed there..." (write this verbatim).
8. **Forbidden.** Bullet list: do not hotlink, do not edit tokens, do not invent components, do not mix this kit with another design system on the same page.

## Constraints

| # | Constraint | Check |
|---|---|---|
| C1 | Templates use only existing components | `grep -oE 'class="uxz-[a-z-]+' ux-zone/templates/*/index.html` produces only classes that exist in `ux-zone/components/*/style.css` |
| C2 | No new component CSS in templates folder | `find ux-zone/templates -name '*.css'` returns empty; template HTML links to component CSS via relative paths |
| C3 | Every template HTML renders with zero console errors | Playwright at `http://localhost:8765/templates/<name>/index.html`, `browser_console_messages` empty |
| C4 | `UX-ZONE.md` covers every component folder | Script: list `ls ux-zone/components/`, assert every name appears in the component catalog table in `UX-ZONE.md` |
| C5 | `UX-ZONE.md` cites file paths that exist | grep for `ux-zone/...` paths in `UX-ZONE.md`, every path resolves |
| C6 | Boilerplate "fresh Claude session" prompt is copy-paste runnable | Manual: run it on a fresh session in a scratch folder; record output behavior in VERIFICATION.md |
| C7 | DD-MM-YYYY only | grep ISO date returns empty |
| C8 | No em dashes in md | `grep -r '—' ux-zone/templates ux-zone/UX-ZONE.md` empty |
| C9 | Templates work standalone (relative paths) | Open `templates/article/index.html` directly without a server, fonts may not load but layout must not break |

## Tools / skills / models

- `Read` + `Write` + `Edit` for files
- `Bash` to run `python3 -m http.server 8765` from `ux-zone/`
- Playwright MCP only for C3 console-error check
- No subagents needed; this is composition, not extraction

## Process

1. Read every component README under `ux-zone/components/` to build the catalog rows for `UX-ZONE.md`.
2. Identify which templates are buildable given the current component set. If phase 02 has not run, templates 2 and 3 are skipped, log this fact in VERIFICATION.md.
3. Draft `UX-ZONE.md`. Order matters: hard rules and the fresh-session prompt go near the top so a Claude session reading the file front-to-back gets them fast.

### AWAITING APPROVAL

Show the user: (a) the full `UX-ZONE.md` draft (or a 200-line preview if larger), (b) the list of templates you will build given the current component set, (c) for each template, the component composition tree. Wait for explicit "go".

4. Build each template as a single `index.html` that links the relevant component CSS files. Use only the markup snippets from each component's README, edit only the text content to fit the page.
5. Write `<name>/README.md` per template: which components it uses, where to swap text, where to swap images, responsive behavior.
6. Edit `ux-zone/index.html` gallery to add a "Templates" section that links each template.
7. Edit `ux-zone/README.md` to add a "Templates and manifest" section pointing to `UX-ZONE.md`.
8. Append Phase 04 to `VERIFICATION.md`.

## Verification

- C1 class-list script: every class in template HTML resolves to a definition in a component CSS file
- C3 Playwright: console errors empty for every template
- C4 script: every component folder appears in `UX-ZONE.md` catalog table
- C5 paths: every cited path exists on disk
- C6 fresh-session smoke: paste the boilerplate prompt into a new conversation, ask it to build a simple landing page, record whether it produced a valid HTML file that links tokens.css and at least one component CSS

## Failure modes

1. A template silently invents a class because the executor wrote markup from memory instead of from the component README. Defense: C1 class-list script catches it; also, every template README must list the components it pulls from, with file path.
2. `UX-ZONE.md` becomes a 1000-line dump that no model actually reads. Defense: cap at 400 lines, lead with hard rules + fresh-session prompt, push deep details into per-component READMEs.
3. The fresh-session boilerplate prompt works for the author but not for someone else because it relies on this conversation's context. Defense: write it standalone, no "we" or "this session"; only absolute paths and explicit instructions.
4. Templates look correct on desktop but break on mobile because component responsive rules conflict at the composition level. Defense: test each template at 360/768/1280 via Playwright resize, screenshot to `templates/<name>/reference-<width>.png`.
5. The manifest names props that no component actually accepts. Defense: source of truth for props is each component's README; the catalog table cites the README line.
6. Phase 04 builds templates that depend on phase 02 components that have not been built yet. Defense: detect this in step 2 and skip those templates; log in VERIFICATION.md as "Skipped: requires phase 02".

## Audience

`UX-ZONE.md` is read by both humans (PMs, designers, frontend engineers) and future Claude sessions. Banned jargon for the human audience: "ontology", "schema-driven", "DSL". Framing rule: every section answers a question a builder would ask, "What do I do? What can I use? What is forbidden?".

---

Start by reading every `README.md` under `ux-zone/components/` and listing the components + their available variants/props, so the `UX-ZONE.md` catalog is grounded in real component contracts before drafting begins.
