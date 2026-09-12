# Review Gate - the evaluation layer

This is Layer 6. It runs in both modes: as the audit in Mode B, and as the gate before handover in Mode A. Same checks either way, because a design that has not been through the review is not finished, it is submitted.

**The standing rule:** the user must never be the person who finds a defect a check would have caught. If they find one, the gate did not run. So run it before showing anything, not after being asked.

---

## Part 1 - Mechanical checks (facts, not opinions)

Collect these first. They cost nothing, they are objective, and finding them by eye wastes a human's time.

### The script

```bash
python3 scripts/check_mockup.py <file.html>
```

Static analysis of the file. Checks contrast on every declared token pair, spacing values against the 4px scale, `:focus-visible` coverage, and one-primary-CTA-per-scope. Exits non-zero on failure. Fast, but it cannot see computed layout.

### The browser audit

Open the artifact in the Playwright or Chrome DevTools MCP browser and evaluate `assets/audit.js`. It returns JSON of failures from the real rendered page:

1. **Contrast** on every visible text node against its actual computed background, including inherited and layered backgrounds.
2. **Hit targets** below 44x44 CSS px.
3. **Gaps** below 8px between adjacent interactive elements.
4. **Focus rings** missing or below 3:1.
5. **Overflow and clipping**, including a child whose shadow escapes an `overflow: hidden` parent.
6. **Off-grid spacing** in computed styles.
7. **Images** without alt text, and form inputs without an associated label.

Static analysis cannot do these honestly, because real contrast depends on what actually rendered underneath. Do not skip the browser pass and then report contrast as verified. If no browser is available, say so and mark those checks unverified.

### WCAG 2.2 AA, the non-negotiable subset

Source: [W3C Quick Reference](https://www.w3.org/WAI/WCAG22/quickref/).

| Criterion | Requirement |
|---|---|
| 1.4.3 Contrast (Minimum) | 4.5:1 body text, 3:1 large text |
| 1.4.11 Non-text Contrast | 3:1 for interactive boundaries and meaningful graphics |
| 1.4.1 Use of Color | Never colour alone to convey meaning |
| 2.5.8 Target Size | 24x24 CSS px floor. This skill uses 44x44 as the working minimum, matching Apple HIG and NN/g touch research. |
| 2.4.7 Focus Visible | Every interactive element has a visible focus indicator |
| 2.4.11 Focus Not Obscured | The focused element is not hidden behind sticky headers or overlays |
| 1.3.1 Info and Relationships | Semantic markup, labelled inputs, real headings |
| 2.1.1 Keyboard | Everything reachable and operable by keyboard |

---

## Part 2 - The 10 heuristics

[Jakob Nielsen's 10 usability heuristics](https://www.nngroup.com/articles/ten-usability-heuristics/), the standard evaluation set since 1994. Walk each one against the artifact. The question in the right column is what to actually ask.

| # | Heuristic | Ask |
|---|---|---|
| 1 | **Visibility of system status** | Does the user always know what is happening? Is there feedback within 400ms of any action? |
| 2 | **Match between system and the real world** | Is the language the user's, not the database's? Do concepts follow real-world logic? |
| 3 | **User control and freedom** | Is there a clearly marked exit from every state? Can mistakes be undone? |
| 4 | **Consistency and standards** | Does the same thing look and behave the same everywhere? Does it follow platform convention? |
| 5 | **Error prevention** | Is the wrong action prevented rather than warned about after the fact? Are destructive actions confirmed? |
| 6 | **Recognition rather than recall** | Does the user have to remember something from a previous screen? |
| 7 | **Flexibility and efficiency of use** | Is there a fast path for the experienced user that does not get in the beginner's way? |
| 8 | **Aesthetic and minimalist design** | Does anything on screen not help the user's current decision? |
| 9 | **Help users recognise, diagnose, and recover from errors** | Does every error say what went wrong, in plain language, and what to do next? |
| 10 | **Help and documentation** | If help is needed, is it findable and task-focused? Better still, is it not needed? |

Heuristic 8 is the one most worth being strict about. It is the licence to delete, and deletion is usually the highest-value change available.

---

## Part 3 - Krug's trunk test

From [Don't Make Me Think](https://sensible.com/dont-make-me-think/). Drop a user onto any screen with no context, as if in the boot of a car, and check they can answer these in about five seconds:

1. What site or product is this?
2. What page am I on?
3. What are the major sections?
4. What can I do here?
5. Where am I in the bigger scheme?
6. How do I search or get to what I need?

Any unanswerable question is an orientation defect. This test is worth more than its simplicity suggests, because it is the closest cheap proxy for a real first-time user.

Krug's underlying rule, worth keeping in mind throughout: **users satisfice**. They do not read the page and pick the best option, they scan and click the first plausible thing. Design for scanning.

---

## Part 4 - The Norman flow walk

For each main flow, at each step, answer:

1. Can the user tell what actions are possible? (Gulf of Execution, availability)
2. Can the user tell how to perform the one they want? (Gulf of Execution, path)
3. After acting, can the user tell what happened and what state they are in? (Gulf of Evaluation)

Detail in `design-method.md`, Layer 3. This finds the defects that no automated check ever will, and it is where "why does this feel confusing" gets a real answer.

---

## Part 5 - Severity

Score every finding 0 to 4. Sort worst first. Do not present findings chronologically or by screen order, present them by severity, because that is the order they should be fixed in.

| Score | Meaning |
|---|---|
| **4 - Catastrophic** | Blocks the task, loses data, or fails accessibility outright. Fix before ship. |
| **3 - Major** | Users will get stuck or make errors. Fix before ship. |
| **2 - Minor** | Users are slowed or mildly confused. Fix in the next pass. |
| **1 - Cosmetic** | Noticeable but not costly. Fix if there is time. |
| **0 - Not a problem** | Recorded and dismissed, with the reason. |

Scoring is comparative, so calibrate against the worst thing you found rather than against an absolute idea of bad.

---

## Part 6 - The finding format

Every finding uses this shape. A finding that does not name a specific element and a specific fix is not a finding, it is an impression, and it wastes the reader's time.

```
### [severity] <one-line title>

Element:   <exact selector, component name, or screen region>
Now:       <what actually happens, observed, not assumed>
Breaks:    <heuristic number / law name / WCAG criterion>
Costs:     <what this costs the user or the team>
Fix:       <the specific change, with values where relevant>
Evidence:  <measured number, screenshot region, or script output>
```

Two things to be careful about, because both have caused real problems.

**Say what you observed, not what you think caused it.** If a number looks wrong, report the number and let the team that owns the logic decide why. "The count shows 12 while the filter says 3" is a finding. "The API is broken" is a guess wearing a finding's clothes.

**Never claim a check you did not run.** "Verified" is a claim about method, and it is the strongest claim in the sentence. If you eyeballed it, say you eyeballed it. Reserve "verified" for something re-runnable: a script output, a computed value, an enumeration you can paste.

---

## Part 7 - The handover verdict

Ship the verdict with the work, in this shape:

```
## Gate result

Static check:     PASS / FAIL (n findings)
Browser audit:    PASS / FAIL (n findings) / NOT RUN (reason)
Heuristic pass:   n findings, worst severity <n>
States shipped:   default, empty, loading, error <, first-run>
Viewed at:        1440px, 390px
Not verified:     <what you could not check, and why>
```

**Hard fails that block handover regardless of anything else:** any WCAG AA contrast failure, any interactive element not perceivable at rest, any hit target below 44px, any interactive element with no focus indicator, any flow with no exit, and a data-fetching screen shipped without its empty and error states.

Everything else is a scored finding. A high average never launders a hard fail.

**Under-claim.** "Implemented and audited by script, visual quality needs your eye" is honest and useful. "Done" over an unchecked artifact is worse than saying nothing.
