# UX Zone 03, Framework adapters (React + Tailwind + Figma)

Add React/JSX + Tailwind variants beside every existing component in `/Users/amanparmar/Documents/AI-PM/Projects/next-leap-claude-code/16-zomato/ux-zone/`, plus a Figma library spec, so the kit drops into v0, Claude artifacts, Next.js, or Figma without translation.

Discipline rule: variants are mirrors, not redesigns. Same DOM shape, same tokens, same class names where possible. If a Tailwind value cannot represent a token exactly, use an arbitrary value `[value]`, do not round.

## Goal

Done when every existing component folder under `ux-zone/components/` contains: the original `index.html` + `style.css` (unchanged), a `Component.jsx` (React + plain CSS), a `Component.tailwind.jsx` (React + Tailwind), and a `figma.md` spec; plus a top-level `ux-zone/adapters/tailwind.config.js` and `ux-zone/adapters/figma-library.md`; plus VERIFICATION.md Phase 03 with all checks passing.

## Inputs

- Existing kit: `/Users/amanparmar/Documents/AI-PM/Projects/next-leap-claude-code/16-zomato/ux-zone/`
- Existing tokens: `ux-zone/tokens.json` and `ux-zone/tokens.css`
- Existing components list: every folder under `ux-zone/components/`

## Outputs (additions inside existing folder)

| Path | Format | Notes |
|---|---|---|
| `ux-zone/adapters/tailwind.config.js` | JS | Theme extends generated 1-to-1 from `tokens.json` (colors, fontFamily, fontSize, spacing, borderRadius, boxShadow, screens) |
| `ux-zone/adapters/tokens.tailwind.css` | CSS | Tailwind `@layer base` that re-exports tokens for projects that prefer raw classes over config |
| `ux-zone/adapters/figma-library.md` | Markdown | Figma library spec: page list, frame list, component list with variants, color styles, text styles, effect styles, all mapped to token names |
| `ux-zone/components/<name>/Component.jsx` | JSX | React functional component, default export, named `<PascalName>`, props typed via JSDoc, plain CSS import |
| `ux-zone/components/<name>/Component.tailwind.jsx` | JSX | Same component, Tailwind-only styling, no CSS import |
| `ux-zone/components/<name>/figma.md` | Markdown | Figma frame spec: variants, properties, layout grid, auto-layout rules, constraints |

## Constraints

| # | Constraint | Check |
|---|---|---|
| C1 | Original `index.html` / `style.css` untouched | `git diff --stat ux-zone/components/*/index.html ux-zone/components/*/style.css` empty |
| C2 | `tailwind.config.js` theme values match `tokens.json` 1-to-1 | Node script that loads both and asserts equality on color, spacing, fontSize, radius, shadow, screen keys |
| C3 | Every component has all four artifacts | `for d in ux-zone/components/*/; do for f in Component.jsx Component.tailwind.jsx figma.md; do test -f "$d$f" \|\| echo MISSING; done; done` empty |
| C4 | React components compile (JSX syntax valid) | `npx --yes @babel/cli ux-zone/components/<name>/Component.jsx --presets=@babel/preset-react -o /dev/null` exit 0 (or `node --experimental-vm-modules` parse check) |
| C5 | Tailwind variants use only classes derivable from `tailwind.config.js` (no raw hex) | Regex over `*.tailwind.jsx`: no `#[0-9a-f]{3,8}` outside `[arbitrary]` brackets; document any arbitrary-value uses in figma.md |
| C6 | DD-MM-YYYY format only | grep ISO date pattern returns empty |
| C7 | No em dashes in markdown | `grep -r '—' ux-zone/adapters ux-zone/components/*/figma.md` empty |
| C8 | Class prefix preserved in JSX variants | every JSX uses `uxz-<component>` class roots, same as the original HTML |
| C9 | Figma spec lists every variant and prop | `figma.md` for each component has a "Variants", "Properties", "Auto-layout" section |

## Tools / skills / models

- No browser needed for this phase. This is pure file generation.
- Use `Read` + `Write` + `Edit` only.
- Do not run `npm install`. The check in C4 uses `npx --yes` which fetches on demand. If the user does not want network use, skip C4 and add a syntactic dry-run instead.
- Do not invoke the `frontend-design` skill (that designs new UIs; this task adapts an existing one).
- Reference for Tailwind config shape: https://tailwindcss.com/docs/configuration. Reference for Figma library structure: https://help.figma.com/hc/en-us/articles/360038662654.

## Reference

- Source of truth for every value: `ux-zone/tokens.json`. Anything not derivable from tokens is forbidden in the JSX variants. If a component currently uses a raw value in its CSS (it should not, per phase-01 C5), surface that and add it to tokens first.

## Process (strict order)

1. Read `ux-zone/tokens.json` end to end. Map each top-level key to its Tailwind config slot (e.g., `color` -> `theme.extend.colors`, `radius` -> `borderRadius`, `breakpoint` -> `screens`).
2. Generate `ux-zone/adapters/tailwind.config.js`. Keep the file readable, one section per token group, comments naming the token source line. Run the equality check (C2) before generating any JSX.
3. Generate `ux-zone/adapters/tokens.tailwind.css` for projects that prefer raw `@theme` style. This is a small file (~80 lines).
4. Walk every folder under `ux-zone/components/`. For each:
   a. Open the existing `index.html`, identify the root element, props that would parameterize it (e.g., hero-article takes `title`, `tag`, `author`, `date`, `readTime`, `heroSrc`), and any variant classes.
   b. Write `Component.jsx`: functional component, JSDoc-typed props, imports `../../tokens.css` and `./style.css`, default values match the existing static example.
   c. Write `Component.tailwind.jsx`: same props, same DOM, classes are Tailwind utilities backed by `tailwind.config.js`. For values not expressible directly, use `[arbitrary]` and note in figma.md.
   d. Write `figma.md`: list variants (e.g., tag-chip has default + brand), properties (boolean/text/instance), auto-layout direction + padding + gap, constraints, color style names, text style names, all mapped to token names.

### AWAITING APPROVAL

Show the user: (a) one fully built component (suggest `tag-chip`, the smallest) across all four artifacts, (b) the generated `tailwind.config.js`, (c) the C2 equality check result. Wait for explicit "go" before generating the remaining components.

5. After approval, generate the remaining components in parallel groups of 4 (cap from CLAUDE.md). Use Sonnet for the file-generation subagents; embed the relevant token excerpts in the prompt so each subagent does not re-read `tokens.json`.
6. Write `ux-zone/adapters/figma-library.md`: page structure (Cover, Tokens, Components, Templates), Figma color/text/effect styles named to match tokens (e.g., `color/text-body`, `text/body-md`).
7. Append a "Phase 03" block to `ux-zone/VERIFICATION.md` with command + result per check.
8. Update `ux-zone/README.md`: add a new "Framework adapters" section explaining how to use the JSX variants in v0, Claude artifacts, and Next.js, plus how to import the Figma library.

## Verification

- C2 equality script output: 0 mismatches
- C3 grep: 0 missing artifacts
- C4 babel parse: exit 0 for every JSX file (or syntactic dry-run if offline)
- C5 hex regex: empty outside `[arbitrary]`
- C8 class prefix grep: every JSX root uses `uxz-` prefix
- Manual smoke: copy `tag-chip/Component.tailwind.jsx` into a fresh `<div>` in a Next.js app with `tailwind.config.js` from `ux-zone/adapters/`, confirm it renders identically to `tag-chip/index.html`. Record result in VERIFICATION.md.

## Failure modes

1. Tailwind config drifts from tokens.json over time. Defense: the config is generated from tokens.json by a script kept in `ux-zone/adapters/build-tailwind.mjs` (write this script too); C2 equality check is the regression gate.
2. JSX variants invent new props that the HTML version never supported. Defense: prop list is derived strictly from text/attribute slots visible in the existing `index.html`; document each prop's HTML origin in JSDoc.
3. Arbitrary Tailwind values explode (`[20px]` everywhere) because token names are not in the config. Defense: extend the config until every token has a name; the arbitrary-value escape hatch is only for one-off overrides, not for normal use.
4. Figma spec is too vague to be implementable. Defense: every `figma.md` section names the exact Figma feature (e.g., "Component property of type Boolean named `isBrand`, default false; toggles instance to `tag-chip/brand`").
5. JSX components ship with React 18 hooks while a teammate uses React 17. Defense: components are stateless functional + props only; no hooks, no Suspense, no context. Note this in the adapters README.
6. Phase 03 silently breaks phase 01 examples by editing original files. Defense: C1 git-diff check is run last, before declaring done.

## Audience

`figma.md` files are read by designers; banned jargon: "atomic design" without a definition, "BEM" (designers do not use it). Framing rule: name the Figma feature directly. JSX files are read by frontend engineers; standard JSDoc.

---

Start by reading `ux-zone/tokens.json` end to end and then writing `ux-zone/adapters/tailwind.config.js` with a one-section-per-token-group layout. Run the C2 equality check before generating any JSX.
