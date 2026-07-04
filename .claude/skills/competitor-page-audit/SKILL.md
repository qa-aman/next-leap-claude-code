---
name: competitor-page-audit
description: >
  Audit your product page against a competitor's page and produce a visual scorecard
  where every gap comes with an exact, reasoned fix. Use whenever the user wants to
  compare their page to a competitor, says "teardown this page vs theirs", "why is my
  page losing to X", "audit my landing page against [competitor]", "compare my product
  page to the competition", "where is my page worse than theirs", or gets vague
  page-improvement suggestions from another tool and wants specifics. Also trigger when
  the user has two page URLs or screenshots and wants to know what to change, what's
  missing, or where users get stuck - even if they don't say "audit".
---

## What this skill does

It compares one product page (yours) against one competitor page across four lenses, walks both as a real user persona, and produces a shareable visual scorecard. Its whole reason to exist is to never return a vague suggestion. Tools like an N8N workflow say "modify your search bar" and leave you with nothing to do. This skill forces every finding to name the exact element, what the competitor does, what you do, why the gap matters, and the precise change - so you can act on it the same day.

Read `references/scoring-rubric.md` before scoring (it defines each 1-5 value per lens), `references/sales-benchmarks.md` before citing any conversion stat (it is the only source you may quote from without fresh validation), and use `references/scorecard-template.html` as the artifact skeleton.

The output is built to be executed, not just read. A diagnosis does not move revenue; ship-ready action items, a sales-impact frame, a sequenced roadmap, and a way to prove the lift do. Every run produces all four (see Step 5).

## The 5-part finding rule (non-negotiable)

This is the point of the skill. Every gap you report carries all five parts. A finding missing any part is not actionable and does not ship - drop it or complete it.

1. **Element** - the exact thing. "The search bar's placeholder text", not "the search bar".
2. **Competitor's treatment** - what they concretely do. "Placeholder shows a sample query: Try 'action items from Monday'".
3. **Your treatment** - what yours does now. "Placeholder says 'Search'".
4. **The gap** - why the difference matters, tied to a user goal or heuristic. "Theirs teaches the feature in the empty state; yours teaches nothing (violates recognition over recall)".
5. **Exact fix + why** - the specific change and the reason. "Change placeholder to a sample query. Cuts the blank-slate problem for first-time users".

If you catch yourself writing a finding as generic as "improve the hero section", stop. That is the exact failure this skill exists to prevent. Push until you can name the element and the change.

## Workflow

### Step 1 - Detect input type per page

The user gives you two pages: theirs and a competitor's. Each arrives as either a live URL or a screenshot. Classify each independently and tell the user what you can do with it:

- **Live URL** - load it in a real browser. Prefer the Chrome DevTools MCP tools; fall back to Playwright MCP if Chrome DevTools is unavailable. You can navigate, scroll, click, and inspect actual elements. All four lenses are fully available.
- **Screenshot** - you can read what is visible but cannot click, scroll, or test a flow. The usability/flow lens is downgraded (you score only what a static frame reveals). Say so; never fake a flow score from an image.

State up front, in one line, what each page is and which lenses are at full vs reduced fidelity. Honesty here is what keeps the scorecard trustworthy.

### Step 2 - Pick the persona and goal (interactive, blocking)

The walkthrough is only as sharp as the persona driving it. "A user" surfaces nothing; "a new Pro user trying to export last week's action items to Slack before a standup" surfaces real friction. So never guess silently.

Read the user's page, infer 2-3 plausible named personas, each with a specific job-to-be-done, and present them as a pick-list using the AskUserQuestion tool. Always include an "Other - type your own" path so the user can supply a persona and goal you did not infer. Do not run any analysis until the user picks one.

Each candidate persona is one line: a name/role + the concrete goal they came to the page to accomplish. Make the goal specific enough to walk (a task with a success state), not a vague mode ("browsing").

### Step 3 - Run the four lenses

Run each as its own focused pass. For every gap, apply the 5-part rule.

| Lens | What to do |
|---|---|
| **Usability / UX flow** | Cognitive walkthrough as the chosen persona, plus Nielsen's 10 heuristics as a checklist. Attempt the persona's goal step by step on each page. Record every point where the persona stalls, backtracks, hesitates, or cannot find the next action. This is the "mimic a user" core. Live-URL only for the flow portion. |
| **Feature / attribute parity** | Build a side-by-side matrix of elements and capabilities. What does the competitor's page have that yours does not (and vice versa)? Search bars, filters, social proof, pricing clarity, demo access, onboarding cues, trust badges, comparison tables. |
| **Messaging & copy** | Headline, value proposition, CTA wording, microcopy, social proof. Does the page communicate the value in the first screen, in the user's language? |
| **Visual & conversion design** | Visual hierarchy, CTA prominence, whitespace, trust signals, above-the-fold content. What pulls the eye and drives the click? |

Nielsen's 10 heuristics for the usability lens: visibility of system status; match between system and real world; user control and freedom; consistency and standards; error prevention; recognition over recall; flexibility and efficiency; aesthetic and minimalist design; help users recover from errors; help and documentation.

### Step 4 - Score each lens 1-5

Score both pages on every lens: 1-5 for the user's page, 1-5 for the competitor, against the rubric in `references/scoring-rubric.md`. The rubric gives each value a written definition per lens so two runs of the same pages land on similar scores instead of drifting on vibes. Read it before scoring.

Gap = competitor score minus your score. A positive gap means you trail. For any lens you had to downgrade (screenshot-only flow), score only what is visible and mark it downgraded rather than inventing a number.

### Step 5 - Render the visual scorecard

Produce a self-contained, theme-aware HTML artifact via the Artifact tool, using `references/scorecard-template.html` as the skeleton. It contains:

- **Header** - the persona and goal the run used, and overall You vs Competitor scores.
- **Lens heatmap** - four lenses, rows for You / Competitor / Gap, colored: green where you lead, grey for a tie, red where you trail (larger deltas darker).
- **Per lens** - the score, a short reasoning line, and the 5-part findings as cards. Tag each finding with the one **conversion lever** it pulls (decision confidence, friction, trust/risk reversal, findability, relevance/basket size, first-screen commitment) so the reader sees why it matters for sales, not just usability.
- **Friction log** - the walkthrough narrated step by step, marking where the persona stalled. Live-URL runs only; for screenshot runs, show a short note that the flow could not be walked.

Then the four things that make it a sales tool, not just a diagnosis:

- **Sales impact (validated benchmarks)** - for the highest-leverage gaps, one card each linking the gap to a documented conversion lever, with the figure and a validated source link. Cite only from `references/sales-benchmarks.md`, or a source you validated the same way this run. Frame as industry benchmarks, not the client's numbers, and never assert a precise revenue figure.
- **Ship-ready action items** - a numbered ticket per fix (A1, A2, ...) with: the **literal copy to paste** (write the real corrected description, placeholder, assembly block, trust strip - not a description of it), exact placement, acceptance criteria ("done when"), effort (S/M/L), and owner (content / eng / merch / creative). Any value you cannot verify from the page (warranty period, return window, assembly time) is a bracketed `[confirm]` placeholder with a note never to ship a guessed number - this respects the no-invented-metrics rule.
- **ROI-sequenced roadmap** - three buckets, This week / This sprint / This quarter, sequenced by sales impact against effort. Put low-effort trust fixes first; end the quarter bucket with the template-level move (roll the fixes into the PDP template so every SKU inherits them) - that is usually the real revenue prize, not the single page.
- **Experiment plan for the top 2 bets** - for the two highest-impact fixes, a short block: hypothesis, primary/secondary/guardrail metric, A/B or pre-post design, and a minimum detectable effect. This is how a benchmark becomes the client's own defensible number.

Set a clear `<title>`, pass a one-line `description`, and a favicon emoji. Keep the favicon stable if the user asks for a re-run of the same audit.

The action items are the heart of the upgrade. "Add reviews" is a suggestion; a ticket with the seed copy, the placement, and the acceptance criteria is something a team ships on Monday. Always push to the second form.

## Two limits to state in the output

Put both of these in the scorecard so it is not oversold:

- The walkthrough is a fast first pass, not real user research. It catches the obvious breaks you are blind to from seeing the page daily. It does not measure emotional reaction or edge-case confusion. Use it to decide where to point real research, not as a substitute for it.
- Screenshot-only runs cannot properly score the flow lens. Downgraded lenses are flagged, not faked.

## Guardrails

- No invented capabilities. Only report what you actually observed on each page. If you could not verify something (a flow behind a login, a paywalled feature), say so rather than assume.
- Every URL you cite in the output must be one you actually loaded. Do not write links from memory.
- Keep the persona consistent across both pages within a run - you are comparing how each page serves the same person with the same goal.
