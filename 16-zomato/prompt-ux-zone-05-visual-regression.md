# UX Zone 05, Visual regression check

Add an automated visual-diff harness to `/Users/amanparmar/Documents/AI-PM/Projects/next-leap-claude-code/16-zomato/ux-zone/` so any future change to tokens, components, or templates is caught before it ships. Without this, the kit silently rots the first time someone tweaks a value.

Discipline rule: this is tooling, not design. Do not change any component CSS to "improve diffs". If a diff fails because the source page changed, that is signal, log it and ask. If it fails because a token was edited, that is a real regression.

## Goal

Done when `ux-zone/.regression/` contains a Node + Playwright harness with a single `npm run check` entrypoint, baseline screenshots exist for every component and template at three widths, the harness produces a HTML report with per-component pass/fail + side-by-side diff images, and CI-runnable (exit code 1 on any failure). VERIFICATION.md Phase 05 covers all checks.

## Inputs

- Existing kit: `/Users/amanparmar/Documents/AI-PM/Projects/next-leap-claude-code/16-zomato/ux-zone/`
- Every component folder under `ux-zone/components/` (with `index.html`)
- Every template under `ux-zone/templates/` (if phase 04 ran)
- Existing reference screenshots under `ux-zone/assets/reference/` and `ux-zone/components/<name>/reference.png` (from phase 01 and 02)

## Outputs (additions inside existing folder)

| Path | Format | What it contains |
|---|---|---|
| `ux-zone/.regression/package.json` | JSON | deps: `playwright`, `pixelmatch`, `pngjs`. Scripts: `baseline`, `check`, `report` |
| `ux-zone/.regression/baseline.mjs` | JS | Captures fresh baselines for every component + template at 360/768/1280, writes to `.regression/baseline/<artifact>-<width>.png` |
| `ux-zone/.regression/check.mjs` | JS | Re-renders, compares against baseline with pixelmatch, writes diff PNGs to `.regression/diff/`, prints summary, exits 1 on any failure above threshold |
| `ux-zone/.regression/report.mjs` | JS | Builds `ux-zone/.regression/report.html`: per-artifact row with baseline / current / diff thumbnails + pass/fail badge |
| `ux-zone/.regression/config.json` | JSON | thresholds (default `pixelRatio: 0.005`, `viewports: [360,768,1280]`), per-artifact overrides allowed |
| `ux-zone/.regression/.gitignore` | text | ignore `diff/`, `current/`, `report.html`; track `baseline/` and config |
| `ux-zone/.regression/README.md` | Markdown | how to run, how to update baselines, when to update |
| `ux-zone/VERIFICATION.md` | edit | append Phase 05 |

## Constraints

| # | Constraint | Check |
|---|---|---|
| C1 | All files inside `ux-zone/.regression/` | `find ux-zone/.regression -type f \| head` returns only that subtree |
| C2 | Harness runs end-to-end with one command | `cd ux-zone/.regression && npm install && npm run check` exits with status reflecting real diff results |
| C3 | Baseline exists for every artifact at every width | Node script: count component folders + template folders; assert baseline count = artifacts * widths |
| C4 | Diff threshold configurable per artifact | `config.json` supports `overrides: { "components/hero-article": { pixelRatio: 0.01 } }`, harness reads it |
| C5 | Report is openable and shows side-by-side images | Manual: open `report.html` in browser, every row has 3 visible thumbnails |
| C6 | Exit code semantics | `npm run check` exits 0 when all pass, 1 when any fail; verified with `&& echo PASS \|\| echo FAIL` |
| C7 | No network calls during `check` (after install) | Wrap Playwright in a local-only context; the harness must work offline once deps are installed |
| C8 | No em dashes in md | `grep -r '—' ux-zone/.regression --include='*.md'` empty |
| C9 | DD-MM-YYYY only in any timestamps written to report | grep ISO returns empty |

## Tools / skills / models

- Use Node.js LTS. Use `playwright` Node package, NOT the MCP browser. The harness must work in CI where there is no Claude session.
- `pixelmatch` for pixel diff. `pngjs` for PNG read/write.
- Do NOT use a headless browser MCP tool inside the harness; the harness is its own process.
- During development you may use the Playwright MCP to verify behavior, but the deliverable is standalone Node code.

## Process

1. Inventory every artifact to test: every `components/<name>/index.html` and every `templates/<name>/index.html`.
2. Decide viewport list (default 360/768/1280) and per-artifact diff threshold (default `pixelRatio: 0.005`).

### AWAITING APPROVAL

Show the user: (a) the artifact inventory (count per type), (b) default thresholds and which artifacts you propose to override (e.g., carousel components often have animation jitter, suggest `0.02`), (c) the dependency footprint (3 npm packages). Wait for explicit "go".

3. Write `package.json` with pinned versions. Pin to avoid silent breakage: e.g., `playwright@^1.45`, `pixelmatch@^5.3`, `pngjs@^7.0`.
4. Write `baseline.mjs`. It walks the artifact list, launches Chromium, for each artifact navigates to `file://...` or `http://localhost:8765/...`, sets viewport, screenshots, saves PNG to `baseline/<artifact-id>-<width>.png`. Run it once to seed baselines.
5. Write `check.mjs`. Same render loop, but writes to `current/`, then loads matching baseline, runs pixelmatch with threshold from config, writes diff PNG, tallies pass/fail, prints a one-line summary, exits 1 on any failure.
6. Write `report.mjs`. Generates `report.html` from the latest `current/` + `baseline/` + `diff/` triples. Plain HTML + inline CSS, one row per artifact, pass/fail badge, three thumbnails (lazy-loaded).
7. Write `config.json` with sensible defaults and a commented example override block.
8. Write `.regression/README.md`: how to run, how to update a baseline ("when a token is intentionally changed: run `npm run baseline`, review the diff in the report, commit only the baselines that look right").
9. Run `npm install && npm run baseline && npm run check` once. Confirm exit 0. Open `report.html` to confirm rendering.
10. Append Phase 05 to `VERIFICATION.md` with all check commands + results.

## Verification

- `npm run check` exits 0 (no regression at baseline)
- Touch a token (e.g., change `--uxz-color-link` to red), run `npm run check`, confirm exit 1 and the affected artifact rows show failure with diff thumbnails. Revert the change. Record this synthetic-failure test in VERIFICATION.md as proof the harness actually catches regressions.
- Run `npm run check` again post-revert, confirm exit 0.
- Run on a fresh clone (simulated by `rm -rf node_modules && npm install && npm run check`) to confirm reproducibility.

## Failure modes

1. Fonts load asynchronously, causing flaky diffs at the moment of screenshot. Defense: wait for `document.fonts.ready` before each screenshot.
2. Animation or transitions cause sub-pixel jitter. Defense: inject a CSS override `*, *::before, *::after { animation: none !important; transition: none !important; }` into every page before screenshot.
3. Baselines committed for the wrong commit, locking in a bug. Defense: README explicitly tells the user "review the diff report in `report.html` before committing new baselines"; consider a wrapper script that opens the report.
4. Threshold too tight, every run fails on antialiasing noise. Defense: default `pixelRatio: 0.005` (0.5% of pixels can differ); README explains how to tune per artifact.
5. The harness depends on the local `http.server` being up. Defense: harness spins up an internal Node static server on a random port, does not rely on an external process.
6. CI fails because Chromium binary is not downloaded. Defense: `postinstall` script runs `npx playwright install chromium`; document this in README.
7. Cross-platform PNG bytes differ (macOS vs Linux). Defense: harness compares by pixel diff, not byte diff; document that baselines should be regenerated when changing the OS the CI runs on.

## Audience

`.regression/README.md` is read by frontend engineers and the next maintainer of the kit. Banned jargon: "snapshot testing" without explaining what is being snapshotted. Framing rule: lead with "When a check fails, here is what to do."

---

Start by listing every artifact to test (every `components/<name>/index.html` and every `templates/<name>/index.html` under `ux-zone/`) and writing `ux-zone/.regression/package.json` with pinned Playwright + pixelmatch + pngjs versions.
