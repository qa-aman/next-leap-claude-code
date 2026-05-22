# Build the Zomato Blog "UX Zone" — Design System + Assets Package

Produce a self-contained UX Zone (design tokens, component library, asset pack, and usage guide) extracted from the live Zomato blog page at https://www.zomato.com/blog/sushi/. The package is the single source of truth that Aman and his teammates will reference when building prototypes, so every prototype built against this UX Zone looks visually and behaviourally identical to the source page and to each other.

Discipline rule: surgical extraction only. Mirror what the source page actually uses. Do not invent components, do not "improve" the design, do not add framework opinions beyond what is asked.

## Goal

Deliver a working UX Zone at `/Users/amanparmar/Documents/AI-PM/Projects/next-leap-claude-code/16-zomato/ux-zone/` that satisfies all six done-conditions:

1. `tokens.json` exists with colors, typography, spacing, radii, shadows extracted from the live page.
2. `components/` contains one `.html` + one `.css` file per component listed in the Components Inventory below, each rendering standalone in a browser.
3. `assets/` contains every referenced image, icon, font file, and logo from the page, downloaded locally (no hotlinks).
4. `index.html` renders a single-page "component gallery" showing every component with its name, variants, and tokens used.
5. `README.md` (max 250 lines) explains how to use the UX Zone in a new prototype in under 5 minutes, with a copy-paste starter snippet.
6. A verification report `VERIFICATION.md` is produced confirming each item in the Verification section passes.

Stop when all six done-conditions are met and `VERIFICATION.md` shows zero failing checks.

## Inputs

- Live source page: https://www.zomato.com/blog/sushi/ (fetch date must be recorded in `VERIFICATION.md` in DD-MM-YYYY format)
- Target output root (absolute): `/Users/amanparmar/Documents/AI-PM/Projects/next-leap-claude-code/16-zomato/ux-zone/`
- Project rules: `/Users/amanparmar/Documents/AI-PM/Projects/next-leap-claude-code/CLAUDE.md`
- Global rules: `/Users/amanparmar/.claude/CLAUDE.md`

## Outputs

All paths are absolute, rooted at `/Users/amanparmar/Documents/AI-PM/Projects/next-leap-claude-code/16-zomato/ux-zone/`.

| Path | Format | Schema / shape | Size target |
|---|---|---|---|
| `tokens.json` | JSON | Keys: `color`, `typography`, `spacing`, `radius`, `shadow`, `breakpoint`. Each leaf is `{ value, source: "css-variable|computed|inline" }` | 50-200 leaves |
| `tokens.css` | CSS | `:root { --color-...: ...; }` mirror of `tokens.json` | 1 file |
| `components/<name>/index.html` | HTML | Standalone, links `tokens.css` + own CSS | 1 per component |
| `components/<name>/style.css` | CSS | Uses tokens, no hard-coded hex/px where a token exists | 1 per component |
| `components/<name>/README.md` | Markdown | Variants, props, when-to-use, copy-paste snippet | <100 lines each |
| `assets/images/` | png/jpg/webp/svg | Original filenames preserved | All referenced images |
| `assets/fonts/` | woff2/woff | Self-hosted from source | All custom fonts |
| `assets/icons/` | svg | Inline icons extracted | All unique icons |
| `index.html` | HTML | Gallery rendering every component | 1 file |
| `README.md` | Markdown | Usage guide + starter snippet | ≤250 lines |
| `VERIFICATION.md` | Markdown | Checklist with pass/fail per item from Verification section | 1 file |

## Components Inventory (must extract all that exist on the source page)

Extract each as a separate component folder. If a listed component is genuinely absent from the page, omit it and note the omission in `VERIFICATION.md`. Do not add components not on the page.

- `header-nav` (top navigation bar, logo, search, account)
- `hero-article` (article hero: title, byline, date, hero image, category tag)
- `body-paragraph` (default prose styling)
- `body-heading` (h1, h2, h3 variants)
- `inline-image` (figure + caption)
- `pull-quote` (if present)
- `cta-button` (primary, secondary variants)
- `cta-banner` (in-article promo card if present)
- `related-articles-card` (article card with image, title, meta)
- `related-articles-grid` (layout container)
- `tag-chip` (category/tag pill)
- `social-share-bar` (share icons + counts)
- `author-bio` (author avatar, name, blurb)
- `comments-block` (if present)
- `footer` (links, social, legal)

For each component, capture: HTML structure, CSS classes used on the live page, all visual states present (default, hover, focus, active where applicable), responsive behaviour at 360px / 768px / 1280px.

## Context the executor needs

- The user is a Senior PM. He and teammates will paste components into prototypes (Claude artifacts, V0, plain HTML, Figma-to-code outputs). The UX Zone must work without a build step. No React, no Tailwind, no PostCSS. Plain HTML + CSS + JSON only.
- "UX Zone" in the user's words = a locked-down kit of components + assets + tokens, so two people building two different prototypes produce visually identical results.
- Output is consumed by humans (Aman + teammates) AND by future Claude sessions that will be told "build prototype X using the UX Zone at this path". Both consumers must be able to use it cold.

## Tools / skills / models

- Use `WebFetch` to retrieve the rendered HTML of https://www.zomato.com/blog/sushi/. If WebFetch returns server-rendered HTML only and the page relies on client-side hydration for key components, fall back to `mcp__plugin_playwright_playwright__browser_navigate` + `browser_snapshot` + `browser_evaluate` to read computed styles and the full DOM. Document which method was used in `VERIFICATION.md`.
- Use `mcp__plugin_playwright_playwright__browser_take_screenshot` once per component at 1280px width and store in `components/<name>/reference.png`. This is the visual ground truth the component must match.
- Use `Bash` with `curl -L -o` to download assets. Preserve original filenames; if collisions, suffix with `-1`, `-2`.
- Use `mcp__plugin_playwright_playwright__browser_evaluate` to pull computed CSS variables and `getComputedStyle` values for tokens. Prefer CSS custom properties from `:root` over computed values when both exist.
- Do not use a frontend framework. Do not use Tailwind. Do not invoke the `frontend-design` skill (that skill generates new designs; this task extracts an existing one).
- Model tier: this task is mechanical extraction. Use the current session model. Do not spawn subagents for the extraction itself; spawn at most 2 parallel agents only for downloading assets in batches if there are >20 assets.

## Reference (the source page is the only reference)

- URL: https://www.zomato.com/blog/sushi/
- Patterns to mirror exactly:
  - Color values (down to the hex)
  - Font family stack, weights, sizes, line-heights, letter-spacing
  - Spacing scale (extract the actual px/rem values used, do not normalize to an 8pt grid if the page uses something else)
  - Border radii, shadow values
  - Hover/focus states as they exist on the page
  - Responsive breakpoints where the layout actually changes
- For each component, in `components/<name>/README.md`, include a line: `Source selector: <CSS selector on the live page this maps to>`. This is the proof-of-fidelity link.

## Constraints (non-negotiable)

Every constraint has a verifiable check. Run the check; record pass/fail in `VERIFICATION.md`.

| # | Constraint | Verifiable check |
|---|---|---|
| C1 | All output paths under `/Users/amanparmar/Documents/AI-PM/Projects/next-leap-claude-code/16-zomato/ux-zone/` | `find <root>/ux-zone -type f | wc -l` > 0; no files outside |
| C2 | All dates use DD-MM-YYYY format | `grep -rE '[0-9]{4}-[0-9]{2}-[0-9]{2}' <root>/ux-zone` returns nothing |
| C3 | No invented metrics, no fabricated brand voice copy | All component example text comes verbatim from the source page; record source quote in each component README |
| C4 | No hotlinked assets in any HTML/CSS file | `grep -rE 'https?://' <root>/ux-zone/components <root>/ux-zone/index.html` returns only documentation references, not `src=` or `url(...)` |
| C5 | Every component CSS uses tokens for color, font-family, spacing >= 4px, radius, shadow | `grep -E '#[0-9a-fA-F]{3,8}' <root>/ux-zone/components/*/style.css` returns nothing |
| C6 | Every asset referenced in HTML/CSS exists on disk | Script: for each `src=` and `url(...)`, resolve path, assert file exists |
| C7 | `tokens.json` is valid JSON | `python -m json.tool tokens.json` exits 0 |
| C8 | `index.html` opens in a browser and renders every component without console errors | Open via Playwright, `browser_console_messages` returns no errors |
| C9 | README starter snippet copy-pasted into a blank HTML file renders a working hero + button | Manual test recorded in VERIFICATION.md |
| C10 | No emojis in any file unless they exist on the source page | `grep -P "[\x{1F300}-\x{1FAFF}]" -r <root>/ux-zone` returns nothing |
| C11 | No em dashes in any markdown file | `grep -r '—' <root>/ux-zone/**/*.md` returns nothing (use commas or hyphens) |
| C12 | Folder structure matches the Outputs table exactly | `tree -L 3 <root>/ux-zone` matches expected layout |

## Process (strict order)

1. Create the directory skeleton at `/Users/amanparmar/Documents/AI-PM/Projects/next-leap-claude-code/16-zomato/ux-zone/` per the Outputs table.
2. Fetch the live page. Record fetch method + DD-MM-YYYY date.
3. Extract tokens: navigate via Playwright, evaluate `getComputedStyle(document.documentElement)` and the body, pull CSS custom properties, sample 10 representative elements for font/spacing/color confirmation. Write `tokens.json` and mirror to `tokens.css`.
4. Take full-page reference screenshot at 1280px, 768px, 360px. Save to `assets/reference/full-page-<width>.png`.
5. Walk the Components Inventory in order. For each:
   a. Identify the source selector on the live page.
   b. Capture component screenshot at 1280px to `components/<name>/reference.png`.
   c. Extract HTML structure, write to `components/<name>/index.html` (linking `../../tokens.css` and `./style.css`).
   d. Extract CSS (computed + class-derived), write to `components/<name>/style.css` using tokens.
   e. Write `components/<name>/README.md` with variants, source selector, source-quote example text.
6. Download all referenced assets to `assets/` preserving filenames. Rewrite all `src` and `url()` references in HTML/CSS to relative paths.
7. Build `index.html` gallery: one section per component, `<iframe>` or inline include each, labelled with name + source selector.
8. Write `README.md` usage guide with a 20-line starter snippet that pulls in `tokens.css` and one component.

### AWAITING APPROVAL

Before step 9, pause and show the user: (a) the components inventory actually found on the page vs the requested list, (b) the token count and 5 sample tokens, (c) the asset count. Wait for explicit "go". Do not proceed to step 9 without it.

9. Run the full Verification section. Produce `VERIFICATION.md`.
10. Report back: total files, total assets, total tokens, any constraint failures, path to `index.html` for the user to open.

## Verification (executor runs all of these before declaring done)

Run each check. Record command + result + pass/fail in `VERIFICATION.md`.

1. `find <root>/ux-zone -type f | wc -l` returns expected count (>= component count × 3 + assets + 5 root files).
2. `python -m json.tool <root>/ux-zone/tokens.json` exits 0.
3. `grep -rE '#[0-9a-fA-F]{3,8}' <root>/ux-zone/components/*/style.css` returns empty.
4. `grep -rE 'https?://[^ "]+\.(png|jpg|jpeg|webp|svg|woff2?|ttf)' <root>/ux-zone/components <root>/ux-zone/index.html <root>/ux-zone/tokens.css` returns empty (no hotlinks).
5. Asset resolution script: parse every `src=`, `href=`, `url(...)` in HTML/CSS files; for each, assert file exists on disk. Zero missing.
6. `grep -rE '[0-9]{4}-[0-9]{2}-[0-9]{2}' <root>/ux-zone` returns empty.
7. `grep -r '—' <root>/ux-zone --include='*.md'` returns empty.
8. Open `<root>/ux-zone/index.html` via Playwright at 1280px. Capture `browser_console_messages`. Zero errors.
9. Visual diff sanity: open `components/header-nav/index.html` and compare side-by-side with `components/header-nav/reference.png`. Record subjective fidelity score (1-10) in `VERIFICATION.md`; if any component scores <8, fix before declaring done.
10. Copy the README starter snippet into `/tmp/uxzone-smoketest.html`, open in browser, confirm it renders a styled hero + button matching tokens.

If any check fails, fix and re-run. Do not mark done with failing checks.

## Failure modes to defend against

1. The page is client-rendered and `WebFetch` returns a near-empty shell. Defense: fall back to Playwright; verify the DOM contains >50 visible text nodes before proceeding.
2. Hotlinked CDN assets break later when the CDN URL rotates. Defense: download every asset, rewrite refs to relative paths, run check C4.
3. Tokens are extracted from a single element and over-fit. Defense: sample at least 10 elements per token category; if two values disagree, store both as variants (e.g., `--color-text-primary`, `--color-text-muted`).
4. Components silently drift from the source because no screenshot ground truth was saved. Defense: every component has `reference.png` captured before extraction.
5. CSS specificity collisions when two components are dropped into the same prototype. Defense: prefix every component class with `uxz-<component-name>__`.
6. Fonts render as fallback because the @font-face is missing. Defense: extract @font-face rules from the source, download woff/woff2, host under `assets/fonts/`, include @font-face in `tokens.css`.
7. Executor invents copy ("Lorem ipsum" or fabricated headlines). Defense: every example string in a component README cites the source quote verbatim, with the selector it came from. If a string cannot be sourced, omit it, do not fabricate.
8. Responsive behaviour is captured only at desktop. Defense: take screenshots at 360px / 768px / 1280px; if layout shifts, add a `@media` block to component CSS.
9. The user adds a 16th component later and has no way to extend. Defense: README includes a "how to add a new component" section with the same folder convention.
10. Verification is skipped because the executor is "almost done". Defense: VERIFICATION.md is itself a done-condition; without it, the task is not complete.

Audit against all 10 failure modes before declaring done. List each in `VERIFICATION.md` with "defended: yes/no + how".

## Audience

`README.md` is read by Senior PMs and their teammates (mixed technical baseline). Banned jargon: "design tokens" without a one-line definition, "atomic design", "design system" without explaining it means "the components in this folder". Framing rule: action-first. Tell the reader what to do in step 1, then explain.

`VERIFICATION.md` is read by the next Claude session and by Aman. Pure checklist format, no prose.

---

Start by creating the directory skeleton at `/Users/amanparmar/Documents/AI-PM/Projects/next-leap-claude-code/16-zomato/ux-zone/` and fetching https://www.zomato.com/blog/sushi/ via WebFetch. Record the fetch method and DD-MM-YYYY date as the first line of `VERIFICATION.md`.
