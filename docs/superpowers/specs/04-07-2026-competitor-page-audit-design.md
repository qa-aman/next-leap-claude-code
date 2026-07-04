# Design: `competitor-page-audit` skill

Date: 04-07-2026
Status: Approved, ready for implementation

## Problem

Existing tools (e.g. an N8N workflow) return vague page-improvement suggestions like "modify your search bar" with no specifics: no target element, no reference to what the competitor does, no exact change, no reason. They are unactionable.

Separately, a PM who sees their own product page every day is blind to where real users stall. Real user research is slow and expensive. There is no fast, repeatable first pass that compares a product page against a competitor's and returns concrete, prioritized fixes.

## Goal

A skill that takes the user's product page and a competitor's page, walks both as a chosen user persona, scores them across four lenses, and produces a shareable visual scorecard where **every gap carries an exact, reasoned fix**.

## Non-goals

- Not a replacement for real user research. It surfaces obvious usability breaks; it does not measure emotional reaction or edge-case confusion. The output states this limit explicitly.
- Not a general strategy-level competitive analysis (the existing `competitive-analysis` skill covers that). This skill is a narrow two-page UX + conversion teardown.

## Inputs

The skill accepts, per page, either:
- **A live URL** - loaded in a real browser via Chrome DevTools MCP (fallback: Playwright MCP). Enables clicking, scrolling, element inspection, and the full cognitive walkthrough.
- **A screenshot** - heuristic read only. No interaction.

The skill detects the input type per page and degrades gracefully. If a page is screenshot-only, it flags which lenses it had to downgrade rather than fabricating a score.

## Flow

1. **Input detection** - classify each page as URL or screenshot; announce what capability is available for each.
2. **Persona selection (interactive, blocking)** - read the user's page, infer 2-3 named candidate personas, each with a specific job-to-be-done. Present as a pick-list using AskUserQuestion, always including an "Other - type your own" option so the user can supply a persona and goal the skill did not guess. Nothing runs until the user picks.
3. **Four-lens analysis** - run each as its own pass (see Lenses).
4. **Score** - 1-5 for You and 1-5 for Competitor per lens, against the fixed rubric. Gap = Competitor minus You.
5. **Render** - build the visual scorecard HTML artifact.

## Lenses

| Lens | Method |
|---|---|
| Usability / UX flow | Cognitive walkthrough as the chosen persona + Nielsen's 10 heuristics. Narrate where the persona stalls, backtracks, or hits a dead end. |
| Feature / attribute parity | Side-by-side matrix of elements and capabilities present on one page and not the other. |
| Messaging & copy | Headline, value proposition, CTA wording, microcopy, social proof. |
| Visual & conversion design | Visual hierarchy, CTA prominence, trust signals, above-the-fold content, whitespace. |

## Scoring model

- Each lens scored 1-5 for You and 1-5 for the Competitor, against a rubric baked into the skill so scores are repeatable, not vibes. Each score value (1 through 5) has a written definition per lens in the skill's reference file.
- Gap = Competitor score minus Your score.
- Heatmap colors the gap: green (you lead), grey (tie), red (you trail; larger deltas darker).

## The 5-part finding rule (core requirement)

Every gap the skill reports MUST carry all five parts. A finding missing any part does not ship.

1. **Element** - the exact thing (e.g. "the search bar's placeholder text", not "the search bar").
2. **Competitor's treatment** - what they concretely do.
3. **Your treatment** - what yours does now.
4. **The gap** - why the difference matters.
5. **Exact fix + why** - the specific change and the heuristic or user goal it serves.

## Output: visual scorecard (HTML artifact)

Self-contained, theme-aware HTML rendered via the Artifact tool.

- **Header** - persona + goal the run used; overall You vs Competitor scores.
- **Lens heatmap** - four lenses, rows for You / Competitor / Gap, colored.
- **Per lens** - the score, the reasoning, and the 5-part findings as cards.
- **Friction log** - the walkthrough narrated step by step, where the persona stalled. Live-URL runs only; omitted with a note for screenshot runs.
- **Prioritized fixes** - ranked list at the bottom by impact vs effort. The "do these first" list.

## Honest limits (written into the output)

- The walkthrough is a first pass, not real user research.
- Screenshot-only runs cannot score the flow lens properly; downgraded lenses are flagged, not faked.

## Build approach

Skill created via the Anthropic Skill Creator (`skill-creator`), per the user's global standard. Structure:
- `SKILL.md` - frontmatter (name + trigger-rich description) and the workflow body under 500 lines.
- `references/scoring-rubric.md` - the per-lens 1-5 definitions.
- `references/scorecard-template.html` - the artifact skeleton.
- Path: `.claude/skills/competitor-page-audit/`.
