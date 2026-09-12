---
name: ux-designer
description: >
  Design and review UI/UX, and deliver it as a clickable self-contained HTML mockup (default)
  or as a Figma file, so it can be judged before any development starts. Use whenever the user
  wants to design a screen, flow, page, dashboard, form, onboarding, empty state, or app, wants
  to see what a feature would look like, or wants existing UI critiqued or improved. Trigger on
  "design this screen", "what should this look like", "make a mockup", "wireframe this", "build
  a prototype of", "UI for this feature", "design the UX", "improve this screen", "review this
  UI", "why does this page feel confusing", "make this look better", "audit this interface",
  "turn this PRD into screens", and on any request to visualise a feature before engineering
  builds it. Also use when someone pastes a URL, screenshot, or component file and asks what is
  wrong with it, or when a spec is written and the natural next question is "how does it look".
  Prefer this skill over hand-rolling UI, and use it even when the user does not say "UX".
---

# UX Designer

This skill produces UI you can judge before anyone writes production code. It runs in two modes and both end at the same place: a working artifact plus a short, reviewable statement of why each decision was made.

**Mode A - DESIGN.** A brief, PRD, feature idea, or user problem goes in. Screens come out.
**Mode B - REVIEW.** An existing URL, screenshot, or component file goes in. A ranked, fixable defect list comes out, and optionally a corrected mockup of the worst screen.

The reason both modes live in one skill is that they use the same rulebook. A review that cannot say what "good" looks like is just an opinion, and a design that was never audited is just a guess.

---

## Read these first

Load only what the job needs. All four are in this skill folder.

| File | Read it when |
|---|---|
| `references/design-method.md` | Mode A, always. The six-layer method (Five Planes, Goal-Directed Design, Norman's diagnosis, Atomic Design) and the order the work must happen in. |
| `references/visual-system.md` | Before writing any CSS. Type scale, spacing scale, colour ramps, elevation, and the default token set. This is the Refactoring UI layer, turned into numbers. |
| `references/review-gate.md` | Mode B, always. Also Mode A before handover. The 10 heuristics, the trunk test, severity scoring, and the evidence format every finding must carry. |
| `references/figma-output.md` | Only when the user asks for Figma output. |

**Also binding, and not duplicated here:** `.claude/rules/ui-design-quality.md` in this repo. It carries the contrast, hit-target, container-math, and Laws of UX rules, and it auto-loads when you touch prototype `.tsx`. It does not auto-load for a standalone `.html` mockup, so read it yourself when building one. Where that file and this skill disagree on a number, that file wins.

---

## Ask before designing, but ask once

Design work fails most often because the goal was never stated, not because the CSS was wrong. Before Mode A, you need four things. Pull whatever you can from the repo and the conversation first, then ask only for the genuine gaps, in a single question. Do not interview the user across five turns.

1. **Who** is on this screen. Name a real persona from `05-user-personas/` if one fits.
2. **What decision or action** the screen exists to serve. One sentence.
3. **What state** the screen is in. First use, loaded with data, empty, error, loading. Designing only the happy state is the most common way a mockup misleads.
4. **Where it lives.** Standalone mockup, or must it match `15-prototype/` tokens.

If the user has given you a PRD or spec, treat silence as agreement with what the doc says and proceed. State your assumptions in the output instead of blocking on them.

---

## Mode A - designing new UI

Work in this order. The order is the point: it stops you choosing colours before you know what the user is trying to do. Full detail in `references/design-method.md`.

**1. Frame it (Strategy + Scope).**
Write the brief before the pixels: user, goal, the one decision this screen serves, the success signal, and what is explicitly not on this screen. Cite the repo file and line for any number or quote you use. Two-thirds of a page, no more.

**2. Structure it (Flow, IA, posture).**
Map the steps the user takes. Pick the product posture, because it sets density: sovereign (used all day, dense, expert), transient (used briefly, sparse, obvious), or daemonic (mostly invisible). Then list the **excise** you are removing, meaning work the interface makes the user do that produces nothing for them. Naming what you cut is what separates design from decoration.

**3. Skeleton it (Layout and hierarchy).**
Decide the visual hierarchy before styling: what must be seen first, second, and last. Then inventory the components as atoms, molecules, and organisms, so the mockup structure and the eventual React structure are the same shape.

**4. Surface it (Tokens and craft).**
Apply `references/visual-system.md`. Pick from the scale, never invent a value. If the target is `15-prototype/`, use the tokens already in `15-prototype/tailwind.config.ts` instead of your own.

**5. Build the artifact.**
Start from `assets/mockup-shell.html`. Copy it, do not rewrite it. It ships the token layer, light and dark handling, the responsive frame, the state switcher, and the decision panel already wired.

**6. Run the gate, then fix, then re-run.**
Section "The gate" below. This is not optional and it is not something to run after the user complains.

**7. Hand over.**
The mockup, plus a short "why" section using the structure in `references/review-gate.md`, plus your open questions.

### Design every state, not just the good one

A mockup that only shows the loaded, happy, data-rich state is the single most expensive kind of misleading artifact, because engineering builds it and then discovers the gaps in QA. The shell has a built-in state switcher. Use it. At minimum ship **default, empty, loading, and error** for any screen that fetches data, and add **first-run** for anything a new user hits. Empty states matter most: they are the first thing a real new user sees and the last thing anyone designs.

---

## Mode B - reviewing existing UI

Sequence matters here too, because objective failures should be found by a machine before a human starts giving opinions.

**1. Get the artifact in front of you.**
A URL means drive it in a real browser with the Playwright or Chrome DevTools MCP, take the screenshot, and read the DOM. A screenshot means read it directly. Component files means read the code and, if it runs, render it. Never review a URL from memory or from its marketing copy.

**2. Run the mechanical audit first.**
`assets/audit.js` in the page returns real computed failures: contrast below threshold, hit targets under 44px, missing focus rings, overlapping interactive elements, off-grid spacing. These are facts, not opinions, and they cost nothing to collect.

**3. Then the heuristic pass.**
The 10 heuristics from `references/review-gate.md`, each finding scored 0 to 4 for severity.

**4. Then the diagnosis pass.**
For the two or three main flows, walk Norman's question set: at each step, can the user tell what they can do, how to do it, and whether it worked. This is where the real "why is this confusing" answers come from, and no automated check will find them.

**5. Drive every control.**
Any dropdown, tab, filter, toggle, or selector must be clicked and its dependent panel checked for an actual update. A selector whose linked content goes stale is a real defect and screenshots never catch it.

**6. Report.**
Ranked worst-first. Every finding carries: the exact element, what happens now, which heuristic or law it breaks, the specific fix, and severity. A finding without a named element and a concrete fix is not a finding, it is a mood. If the user wants it, rebuild the worst screen as a corrected mockup so the fix is visible rather than described.

---

## Output format

**Default is a self-contained HTML mockup.** One file, inline CSS and JS, no CDN, no build step. It opens by double-clicking and it can be emailed. Write it to the current cohort folder under `outputs/` (for example `outputs/aug-2026-cohort/`), never loose in `outputs/`.

Why HTML rather than static images: it is clickable, so the flow can be tested, it is responsive, so the mobile story is honest, and it is the closest thing to the eventual build without being the build.

**Figma on request.** When the user asks for Figma, read `references/figma-output.md`. Short version: design in HTML first, then push, because the HTML is what carries the audited token values.

**React into `15-prototype/`** only when the user explicitly asks for working prototype code. Then `.claude/rules/ui-design-quality.md` and `npm run typecheck` both apply.

---

## The gate

Run this before you show the user anything. If a defect reaches them, the gate did not run, and finding it is not their job.

**Step 1 - static check.** `python3 scripts/check_mockup.py <file.html>`. Reads the token manifest and CSS, and checks contrast pairs, spacing grid, focus-visible coverage, and one-primary-CTA-per-scope. Exits non-zero on failure.

**Step 2 - runtime check.** Open the file in the Playwright or Chrome DevTools MCP browser and evaluate `assets/audit.js`. It returns JSON of computed failures. This catches what static analysis cannot: real rendered contrast, real hit-target sizes, real overlap.

**Step 3 - look at it.** Screenshot the artifact at 1440px and at 390px and actually read the images. Screenshot the sections you changed, not just the top of the page. Then apply the standing bar from `~/.claude/CLAUDE.md`: if an Apple or Google designer reviewed this in 2026, would they ship it to end users. A gate pass certifies accessible and functional, never premium.

**Step 4 - drive it.** Click every interactive element, switch every state in the state switcher, and confirm the dependent content actually changes.

**Step 5 - report the verdict with the work.** State what passed, what you could not verify, and why. "Contrast verified by script, hit targets verified in browser, visual quality is my judgement and needs your eye" is an honest handover. "Done" is not.

If a step is genuinely blocked, for example no browser is available, say so plainly and mark those checks unverified. Under-claiming is always better than a green label over an unchecked artifact.

---

## Things that reliably go wrong

1. **Colour before goal.** If you are picking a palette and cannot state the user's goal in one sentence, go back to step 1.
2. **Only the happy state.** See above. Empty and error states are where products actually get judged.
3. **Inventing spacing.** `padding: 13px` means the scale was abandoned. Pick from the scale.
4. **Two primary CTAs in one scope.** That is zero primary CTAs.
5. **Ghost buttons with no border and no fill.** Text on a surface is not a button. This shipped as a real bug in this repo.
6. **Reviewing a screenshot of the top of a long page.** The bug is usually below the fold, in the part you just changed.
7. **Copying a competitor's layout without naming the pattern.** Jakob's Law says match convention, but say which convention and why, so the choice is reviewable.
8. **A findings list with no fixes.** Every defect ships with the exact change.
