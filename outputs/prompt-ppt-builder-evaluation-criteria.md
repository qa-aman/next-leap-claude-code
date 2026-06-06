# Build and Wire an Evaluation Rubric into the ppt-builder Skill

This prompt produces a deck-grading evaluation rubric and bakes it into the `ppt-builder` skill so that every generated `.pptx` is scored against usability and UX criteria before it reaches the user. The rubric covers positive, negative, and edge content cases and complements (does not duplicate) the existing mechanical `check_layout.py`. The consumer is a future Claude Code session running `ppt-builder`, plus Aman reviewing the scored report. Make surgical changes only: add the rubric and one workflow step; do not rewrite existing helpers, design constants, or `check_layout.py`.

## Goal

Done when the `ppt-builder` skill contains a new `references/evaluation-criteria.md` rubric and a Step 7 in `SKILL.md` that together cause every built deck to be scored 0-100 across the defined usability/UX dimensions, with a hard pass gate (>= 90/100 and zero critical failures) enforced before handoff, and a sanity re-score of one deck confirms the rubric is applied consistently.

## Inputs

- Skill to modify: `/Users/amanparmar/Documents/AI-PM/Projects/next-leap-claude-code/.claude/skills/ppt-builder/` (SKILL.md ~87 lines, `scripts/build_ppt.py`, `scripts/check_layout.py`, `references/slide-patterns.md`, `references/layout-checker.md`).
- UX source for criteria: `/Users/amanparmar/Documents/AI-PM/Projects/next-leap-claude-code/.claude/rules/ui-design-quality.md`. Pull the audience/perception-relevant rules: Section 1 (contrast 4.5:1 body, 3:1 large), Section 4 (4px spacing rhythm), Section 5 (one primary focal point per scope, hierarchy without color alone), Section 9.1 (Cognitive Load, Miller's Law ~7±2, Hick's Law / Choice Overload, Chunking), 9.2 (Proximity, Common Region, Similarity, Prägnanz - squint test), 9.3 (Selective Attention, Von Restorff, Serial Position, Peak-End), 9.5 (Jakob's Law, Mental Model, Aesthetic-Usability), 9.6 (Pareto - polish demo slides first).
- Skill's own non-negotiables: SKILL.md "Design rules" block (BG_DARK #0D0D0D, ACCENT #D47A21, max 5 bullets/slide, titles state takeaway not topic, no emojis, no speaker-direction labels).

## Outputs

1. `/Users/amanparmar/Documents/AI-PM/Projects/next-leap-claude-code/.claude/skills/ppt-builder/references/evaluation-criteria.md` - the rubric. Schema: one `## ` section per scoring dimension (target 8-10 dimensions), each with **What it measures**, **Weight (pts)**, **What "good" looks like**, **How to check** (a concrete inspection: python-pptx property read, bullet count, character count, contrast pair, or squint-test instruction), and **Critical?** (yes = an automatic fail regardless of total). Weights sum to exactly 100. Followed by: a **Positive / Negative / Edge use-case matrix** table (>= 5 rows per category), a **Scored report template** (per-dimension score + evidence line + total + verdict), and a **Pass gate** definition. Target length under 300 lines.
2. Edit to `/Users/amanparmar/Documents/AI-PM/Projects/next-leap-claude-code/.claude/skills/ppt-builder/SKILL.md` - add **Step 7: Evaluate (mandatory)** after the existing Step 6 layout checker, instructing the builder to score the deck against `references/evaluation-criteria.md`, write the scored report, and refuse handoff below the gate. Add one bullet to "Bundled resources" pointing to the new file. Do not touch any other section.

## Context the executor needs

- `check_layout.py` already covers MECHANICAL faults only: out-of-bounds shapes and overlapping textboxes (`references/layout-checker.md`). The new rubric must NOT re-test those. It tests content and usability quality: hierarchy, cognitive load, contrast intent, chunking, takeaway titles, serial position, peak-end closing, convention adherence.
- The deck is dark-themed: body text is `LIGHT_GREY`/`WHITE` on `BG_DARK` (#0D0D0D). The contrast dimension should verify the deck stays within the approved palette (no low-contrast grey-on-grey was introduced), since the palette itself is pre-vetted - flag only deviations from SKILL.md constants.
- Assumption: the evaluator inspects a saved `.pptx` plus the source content doc. It reads slides via python-pptx (already a skill dependency). No new pip dependency may be introduced.

## Tools / skills / models

- Edit/Write tools for the two file changes. Read the five skill files and `ui-design-quality.md` in full before writing.
- Do not invoke the `skill-creator` to scaffold - this is an edit to an existing skill, not a new one. Preserve the existing SKILL.md YAML frontmatter (`name`, `description`) unchanged.
- python-pptx is the only inspection library the rubric's "How to check" steps may assume.
- Model: this is reasoning + authoring; run in the main session, no subagent needed.

## Reference (mirror these patterns)

- Rubric table shape: mirror `/Users/amanparmar/Documents/AI-PM/Projects/next-leap-claude-code/.claude/rules/prompt-writing.md` - its `| # | Dimension | Weight | What "good" looks like |` table and its `## Anti-patterns (instant deductions)` list. Build the evaluation-criteria rubric in that same column structure and add the per-dimension fields named in Outputs #1.
- "How to check" concreteness: mirror `ui-design-quality.md`'s **what / verification / source** triad - every dimension must have a verifiable check, never "make it look good."
- Label each dimension with the `ui-design-quality.md` law(s) it derives from (e.g. "Miller's Law, §9.1") so the lineage is traceable.

## Constraints (non-negotiable)

- No em dashes anywhere in the authored files; use commas or hyphens. Check: `grep -nP "\x{2014}" <each new/edited file>` returns nothing.
- No emojis in any authored content. Check: visual scan + the rubric must itself forbid emojis in graded decks (mirrors SKILL.md rule).
- Any date written uses DD-MM-YYYY. Check: `grep -nE "[0-9]{4}-[0-9]{2}-[0-9]{2}" <files>` returns nothing.
- No invented metrics or numbers presented as MeetFlow facts; the rubric thresholds (weights, >= 90 gate, 44px-equivalent reasoning) are evaluation design choices, label them as such. Check: every threshold has a one-line rationale.
- Skill hygiene (global standard): SKILL.md body stays under 500 lines, overflow lives in `references/`, no README added, frontmatter intact. Check: `wc -l SKILL.md` < 500 and `references/evaluation-criteria.md` exists.
- Do not modify `check_layout.py`, `build_ppt.py`, `slide-patterns.md`, or the design constants. Check: `git diff --name-only` lists only `SKILL.md` and the new `references/evaluation-criteria.md`.
- Weights in the rubric sum to exactly 100. Check: add them; assert == 100.
- If any URL is cited, validate it returns 2xx (999 acceptable for anti-bot) before including; otherwise omit. The `ui-design-quality.md` source URLs are already vetted in that file, so reuse them verbatim rather than re-deriving.

## Process (strict order)

1. Read all six source files in full (5 skill files + `ui-design-quality.md`).
2. Draft the 8-10 scoring dimensions. Each must map to at least one usability concern and cite its `ui-design-quality.md` lineage. Required coverage: (a) Title-as-takeaway, (b) Cognitive load / bullet density (<=5, Miller/Hick), (c) Chunking & grouping (proximity/squint test), (d) Visual hierarchy & one focal point per slide, (e) Contrast & palette fidelity, (f) Serial-position ordering (most important first/last), (g) Peak-End (strong closing slide), (h) Convention/Jakob's-Law pattern fit, (i) Aesthetic consistency (spacing rhythm, alignment), (j) Content integrity (no emojis, no speaker-direction tags, no em dashes leaking into slides).
3. Build the Positive / Negative / Edge use-case matrix: positives (clean structured doc, right slide count, takeaway titles); negatives (emoji-laden source, >5 bullets crammed, em dashes, speaker-direction labels, two primary focal points on one slide); edges (near-empty content / 1-2 slides, 50+ slide dump needing split, single-section doc, very long bullet that overflows, table with many rows, non-English text). >= 5 rows each. State the expected grader verdict per row.
4. Write the scored report template and the pass gate (>= 90/100 AND zero `Critical?: yes` failures = ship; otherwise list fixes and re-build).
5. Write `references/evaluation-criteria.md`.
6. Add Step 7 to SKILL.md and the bundled-resources bullet. Touch nothing else.
7. Run the Verification block.

### AWAITING APPROVAL
Before editing SKILL.md (Step 6), show Aman the dimension list with weights and the use-case matrix headers. Wait for explicit approval, then proceed.

## Verification (run before delivery)

- `grep -n "-" .claude/skills/ppt-builder/references/evaluation-criteria.md .claude/skills/ppt-builder/SKILL.md` - expect no output.
- `grep -nE "[0-9]{4}-[0-9]{2}-[0-9]{2}" <both files>` - expect no output.
- `git -C /Users/amanparmar/Documents/AI-PM/Projects/next-leap-claude-code diff --name-only` - expect exactly the two intended files.
- `wc -l .claude/skills/ppt-builder/SKILL.md` - expect < 500.
- Sum the dimension weights - expect exactly 100.
- Consistency sanity check: pick one existing or freshly built deck, score it twice against the rubric mentally/programmatically; the two totals must match within 2 points. If they diverge, a dimension's "How to check" is too subjective - tighten it.
- Self-audit against every failure mode below.

## Failure modes to defend against

1. **Duplicating the layout checker** - rubric re-tests overlap/out-of-bounds. Defense: rubric scores only content/usability; cite that mechanical faults are check_layout.py's job.
2. **Subjective dimensions** - "looks clean" with no check. Defense: every dimension needs a concrete inspection (count, property read, palette compare, squint instruction).
3. **Weights not summing to 100** - Defense: explicit sum assertion in verification.
4. **Scope creep into other skill files** - Defense: `git diff --name-only` gate; refuse changes to build_ppt.py / check_layout.py / slide-patterns.md.
5. **Gate too lax or too strict** - a 51/100 deck ships, or a perfect deck fails on one nitpick. Defense: tier failures into Critical (auto-fail) vs scored; set gate at >= 90 with rationale stated.
6. **Em dashes / emojis leaking into the authored rubric itself** while it forbids them in decks. Defense: grep before delivery.
7. **Rubric assumes a new dependency** (e.g. a contrast-checker pip package). Defense: restrict checks to python-pptx reads and palette-constant comparison.
8. **Edge cases under-specified** - "handles big decks" with no expected verdict. Defense: every matrix row states the expected grader verdict and the fix it should demand.
9. **SKILL.md Step 7 contradicts Step 6 ordering** - Defense: Step 7 runs after the layout checker passes, not instead of it.

## Audience (for the scored report the rubric produces)

Aman, Senior PM. Technically fluent, no python-pptx internals needed in the report. Banned: hype, corporate filler, vague praise. Framing: lead with the verdict (ship / fix), then the total, then the lowest-scoring dimensions with the specific slide numbers and the one fix each needs. Short lines, numbers over adjectives.

---

Start by reading all six source files in full: the five files under `.claude/skills/ppt-builder/` and `.claude/rules/ui-design-quality.md`. Do not write anything until you have read them.
