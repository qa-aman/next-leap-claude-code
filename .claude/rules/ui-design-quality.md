---
paths:
  - "15-prototype/**/*.tsx"
  - "15-prototype/**/*.css"
  - "15-prototype/tailwind.config.ts"
  - "**/ux-zone/**/*.tsx"
  - "**/prototype/**/*.tsx"
---

# UI Design Quality Rules

Apply whenever writing or modifying UI code: components, pages, design tokens, or styles. These rules exist because real bugs shipped: a ghost button was invisible against the page background, and a button overflowed its container's border. They prevent recurrence.

Every rule below has a **what**, a **verification**, and a **source**. If a rule and a stylistic preference conflict, the rule wins. Don't ship code that fails the verification.

---

## 1. Contrast (the non-negotiables)

**1.1 Body text vs background: minimum 4.5:1**
WCAG 2.2 SC 1.4.3 (Minimum). Applies to all text below 18pt regular / 14pt bold.
Source: https://www.w3.org/WAI/WCAG22/quickref/?showtechniques=143%2C144%2C145%2C147%2C148#contrast-minimum

**1.2 Large text vs background: minimum 3:1**
WCAG 2.2 SC 1.4.3. Large = 18pt+ regular OR 14pt+ bold (24px / 19px CSS approx).

**1.3 UI component boundaries vs adjacent colors: minimum 3:1**
WCAG 2.2 SC 1.4.11 (Non-text Contrast). A button must be **perceivable as a button at rest** without hover or focus. That means at least one of {fill, border, icon, distinct shape} hits 3:1 against the surface it sits on.

**This is why ghost buttons fail.** A ghost button with no border and no background is text on a surface, not a button. Either:
- give it a visible border at rest (`border border-border` is fine if border has 3:1 contrast against the card surface), OR
- give it a subtle filled background at rest (e.g. `bg-bg-subtle`), OR
- restrict ghost variant to contexts where the parent already provides a button-shaped affordance (toolbar slot, dropdown row).
Source: https://www.w3.org/WAI/WCAG22/Understanding/non-text-contrast.html

**1.4 Verification**
For any new button or interactive element: open https://webaim.org/resources/contrastchecker/ and verify text vs background ratio. Or use the Chrome DevTools Accessibility panel (Inspect element -> Accessibility -> Contrast). Document the ratio in the component's `spec.md` under a `## Contrast` section.

---

## 2. Hit targets and spacing between interactive elements

**2.1 Minimum hit target: 44x44 CSS px**
Apple HIG and WCAG 2.2 SC 2.5.8 (Target Size, Minimum, 24x24 CSS px). NN/g recommends 1cm x 1cm physical, which on a 96dpi display is ~38px and on a typical phone is ~44-48px. Use **44x44 CSS px** as the universal minimum because it works for both pointer and touch.
Source: https://www.nngroup.com/articles/touch-target-size/ and https://www.w3.org/WAI/WCAG22/Understanding/target-size-minimum.html

If a visible button is smaller than 44x44 (e.g. an icon button at 28x28), expand its hit area with padding, `::before` pseudo, or a wrapper. Don't reduce the visible glyph to make it look "compact" without preserving the hit area.

**2.2 Minimum gap between adjacent interactive elements: 8px**
Smaller than this and Fitts' Law gets you slip-errors. 8px is the floor; 12px is the comfortable default for primary toolbars.
Source: NN/g (as above), Fitts' Law application.

**2.3 Buttons that sit at the edge of a container need at least 8px of breathing room**
A button must never visually kiss or cross its parent's border or rounded corner. Use `padding` on the parent or `margin` on the button to guarantee at least 8px clear space between the button's outer bound (including any glow / box-shadow visible at rest) and the container's stroke.

**This is why the Confirm button overflowed the card.** The card had `py-3.5` (14px) but the button had a hover glow of ~6-8px AND was vertically aligned with `items-start`, putting the top edge directly at the padding boundary. Fix: increase container padding, use `items-center` so buttons cannot drift to the top/bottom edge of the row, OR remove `overflow-hidden` from a card whose decorations need to bleed slightly.

---

## 3. Container math (preventing overlap and clipping)

**3.1 Rule: container padding >= max(child outer bound, child shadow / glow extent) + 4px**
"Outer bound" includes any visible decoration: box-shadow, ring, outline glow at rest. If a button has `shadow-[0_0_0_1px_rgba(...)]` (1px outline) and lives inside a card with `py-3`, you have only 12-1 = 11px of true clear space. If hover adds a 12px glow, hover state will clip with `overflow-hidden`.

**3.2 Never combine `overflow-hidden` with children that have outward-extending decorations at rest**
If a child needs `shadow-glow-*` or a soft outer glow, the parent must either:
- not use `overflow-hidden`, OR
- have padding >= glow radius + 4px so the glow renders inside the clipping bounds.

**3.3 Vertical alignment in mixed-height grid rows**
When a row contains a tall content column and a short action column, align actions with `items-center` (or `items-start` only if you also set explicit `mt-*` to push them off the top edge). `items-stretch` is rarely what you want for buttons.

**3.4 Verification**
Open the page in Chrome DevTools, inspect each card / list row, and confirm:
- Button outer bounding box does not cross the card's `border-radius` arc.
- Hover state: trigger hover, confirm no clipping.

---

## 4. Spacing scale (the 4px grid)

**4.1 Use a single spacing scale across the project**
This project's scale is 4px-based (Tailwind default): 4, 8, 12, 16, 20, 24, 32, 40, 48. Don't introduce arbitrary values (`px-[13px]`, `mt-[7px]`) unless mirroring an exact Mobbin reference and noting the deviation.

**4.2 Container padding minimums**
- Inline chip / pill: 8px horizontal, 2px vertical (small)
- Button: 12-14px horizontal, 8-10px vertical (sm), 14px / 10-12px (md)
- Card body: 16px on all sides minimum, 20-24px for hero cards
- Section gap on a page: 24px minimum, 32px between major sections

**4.3 Source**
IBM Carbon 2x grid (https://carbondesignsystem.com/elements/2x-grid/overview/) and Material Design 4dp baseline grid. Both projects standardize on 4px increments and call out that ad-hoc values fragment the visual rhythm.

---

## 5. Button variants and visual hierarchy

**5.1 Each variant must be visually distinct WITHOUT relying on color alone**
WCAG 2.2 SC 1.4.1 (Use of Color). Primary vs secondary vs ghost must differ in {fill, border, weight} — never only in hue.

| Variant | At-rest indicators |
|---|---|
| Primary | Solid fill + brand color + inset highlight + shadow |
| Secondary | Subtle fill + visible border (1px) |
| Ghost | Visible border OR subtle fill (NOT both naked) |
| Danger | Solid fill + danger color + inset highlight |

**5.2 Maximum one primary CTA per visual scope**
A scope = a card, a row, a modal, a section. Two primaries in one scope = no primary. If you need two emphasized actions, demote one to secondary or split them across scopes.

**5.3 Source**
Apple HIG, Material Design button anatomy, Refactoring UI Ch. "Hierarchy".

---

## 6. Color palette discipline

**6.1 Each semantic color needs 5-10 shades, not 1**
A single "danger" red can't serve as text, border, fill, and dimmed-background. Define a scale and use the right shade for the role.
Source: Refactoring UI, https://www.refactoringui.com/previews/building-your-color-palette - "5-10 shades per color... nine is a great number."

**6.2 Role -> shade convention (this project)**
- Text on tinted backgrounds: darkest shade (success-700, warning-700, danger-700 equivalents)
- Borders on tinted backgrounds: mid shade at 30-40% alpha
- Tinted backgrounds: lightest shade or base color at 8-12% alpha
- Solid fills (primary CTA): base shade
- Hover states: shift one step darker / lighter

**6.3 Avoid pure black backgrounds; avoid pure white text on tinted backgrounds**
Refactoring UI: "True black tends to look pretty unnatural; start with a really dark grey." This project's base is `#08080a`, not `#000000`.

---

## 7. Focus and hover states

**7.1 Every interactive element needs a visible focus indicator with 3:1 contrast**
WCAG 2.2 SC 2.4.11 (Focus Not Obscured) and SC 1.4.11. Use `focus-visible:` (not `focus:`) so it only shows on keyboard nav, not on every click.
Source: https://www.w3.org/WAI/WCAG22/Understanding/focus-appearance.html

**7.2 Hover state must be a perceivable change, not just opacity 0.9**
The change should communicate "this is clickable" - typically: background shift, border shift, subtle elevation, OR icon color shift. Pure opacity changes are easy to miss and feel like a disabled state.

**7.3 Don't rely on hover to make a button visible**
A button that's only visible on hover fails WCAG 1.4.11 because at-rest perceivability is required.

---

## 8. Pre-merge UI checklist

Before considering any UI change done, walk this list:

- [ ] Every text run hits 4.5:1 against its background (3:1 if large).
- [ ] Every button / interactive element is visually distinguishable at rest (3:1 boundary contrast). No invisible ghost buttons.
- [ ] No button or focusable element is smaller than 44x44 CSS px hit area.
- [ ] No interactive element kisses or crosses its container's border or border-radius arc.
- [ ] Hover state triggered: no clipping, no shadow escaping `overflow-hidden`.
- [ ] Focus state triggered (Tab through): visible 3:1-contrast ring on every interactive.
- [ ] At least 8px gap between adjacent interactive elements.
- [ ] Spacing values are on the 4px grid; arbitrary `[13px]` values are justified inline.
- [ ] Each scope has at most one primary CTA.
- [ ] No info conveyed by color alone (icon + text + color together).

---

## 9. Psychological laws of UX (Jon Yablonski)

Sections 1-8 govern execution. This section governs intent: which design moves to make in the first place. Sourced from *Laws of UX* by Jon Yablonski (https://lawsofux.com/, O'Reilly 2020 / 2024). The 30 laws are grouped by what cognitive system each one engages. Every law has a **principle**, a **MeetFlow application**, and where useful a **review question** to ask of any new screen.

If a law and a stylistic preference conflict, the law wins. If you skip a law on a specific screen, leave a one-line note in the screen's `screen-notes.md` saying why.

### 9.1 Cognitive load (the single most important theme)

The user has a finite amount of mental effort to spend on your interface. Every element competes for that budget.

| Law | Principle | MeetFlow application |
|---|---|---|
| **Cognitive Load** | Mental effort required to use an interface | Audit every screen against the question "what is the user trying to decide here?" Strip anything that doesn't help that decision. |
| **Miller's Law** | Working memory holds 7 ± 2 items | Cap list options, menus, and tabs at ~7 per group. Action items page already does this via filter chips and screen grouping. Don't ever show a flat list of 20+ tasks without chunking. |
| **Hick's Law** | Decision time scales with number + complexity of choices | Use progressive disclosure. Tone selector ships with 3 options (Concise / Warm / Direct), not 7. Action items show 3 filter chips, not 8 columns. |
| **Choice Overload** | Many options causes paralysis | When a feature could expose N controls, default to the 3 highest-leverage ones, hide the rest behind an "Advanced" affordance. |
| **Chunking** | Group information into meaningful units | Pre-meeting list groups meetings by Today / Tomorrow / Later, not as a 30-row flat list. Summary page groups output into Recap / Key moments / Decisions / Participants - 4 chunks, not 1 wall. |
| **Working Memory** | The system holding info briefly during a task | If a user must remember a value from screen A to use on screen B, you have a bug. Carry context forward (e.g., `/follow-up` references the source meeting and its action items inline). |
| **Occam's Razor** | Pick the simplest solution | Before adding a setting, a tab, a toggle, ask: can the system decide this on the user's behalf with a sensible default? |
| **Tesler's Law** | Some complexity is irreducible | Don't paper over it - shift it from user to system. Action item confidence is irreducibly fuzzy, so the system computes a confidence score and asks the user to confirm low-confidence ones, instead of forcing a binary decision on all. |

**Review question:** Open any screen and count the discrete things on it. If above 9, it probably needs chunking or progressive disclosure.

### 9.2 Perception and grouping (Gestalt)

How the brain decides what belongs together, before reading any text.

| Law | Principle | MeetFlow application |
|---|---|---|
| **Law of Proximity** | Things close together are perceived as a group | The badge row, title, and meta row inside ActionItemRow sit at 8px gap (one group). The Confirm + Reject buttons sit at 8px gap from each other but 16px from the content (a separate group). |
| **Law of Common Region** | A shared bounded region is read as a group | Cards work because the border + bg-elevated define a region. Don't nest cards inside cards without strong reason - it confuses the grouping. |
| **Law of Similarity** | Visually similar items are read as related | All ConfidenceBadges share the same shape and tone-coded color scheme. All primary CTAs share the same gradient + glow. Breaking this consistency breaks the grouping. |
| **Law of Uniform Connectedness** | Connected things (line, container) feel even more grouped than near things | The accent left rail on ActionItemRow is a uniform connector that says "this is one unit." The transcript timeline rail in TranscriptStream does the same. |
| **Law of Prägnanz** | Brains simplify complex visuals to the simplest form | If a layout is ambiguous, the brain picks one interpretation, often wrong. Strong corner radii, clear edges, consistent padding all push the brain toward the right reading. |

**Review question:** Squint at the screen until text blurs. Do the visual groups match the conceptual groups? If a header looks like it belongs to the card below it, your spacing is wrong.

### 9.3 Attention and memory

What the user actually notices and recalls.

| Law | Principle | MeetFlow application |
|---|---|---|
| **Selective Attention** | Users only see what they're looking for | The primary CTA must be unmistakable. One primary per scope (Section 5.2). Demote everything else. |
| **Von Restorff Effect** | The element that differs is the one remembered | ConfidenceBadge uses red for Low precisely because red is the visual outlier in a calm dark UI. Don't waste the outlier slot on decoration. |
| **Serial Position Effect** | First and last items are remembered best | First item in any list = most important or most recent. Last item = strong second slot. Bury the noise in the middle. The follow-up page's tone selector puts Concise first (the default) and Direct last (the strongest stance). |
| **Peak-End Rule** | Experiences are remembered by their peak moment and their ending | The Send confirmation on /follow-up is the "ending" of the demo flow. It must feel good - hence the success medallion + soft copy. Don't fade it out abruptly. |
| **Zeigarnik Effect** | Unfinished tasks stick in memory | "Needs review" badges on action items are a Zeigarnik prompt: the user feels the open loop. Don't show open loops you don't want the user to act on. |

**Review question:** What's the one thing on this screen the user will remember tomorrow? If you can't answer in one sentence, the hierarchy is muddy.

### 9.4 Interaction physics

What it actually feels like to use the thing.

| Law | Principle | MeetFlow application |
|---|---|---|
| **Fitts's Law** | Time to hit a target = function of size + distance | Larger primary CTAs, placed near where the user's eye already is. The Join button sits on the right of the meeting row, not buried in a kebab menu. (Section 2's 44x44 hit target rule is the Fitts's Law floor.) |
| **Doherty Threshold** | Productivity drops above ~400ms latency | All prototype interactions are local + instant. In a real product: any action taking longer than 400ms needs a skeleton, spinner, or optimistic update. |
| **Goal-Gradient Effect** | Motivation increases as the goal nears | The AI Notes panel header shows "Live · 3/4" - a visible progress signal toward "all notes captured." The Confidence Scoring filter shows counts per state. |
| **Flow** | Deep, uninterrupted engagement | Don't pop modals during /live. Don't ask for input the system could infer. The whole point of MeetFlow is "the AI watches so you can stay in the meeting." |

**Review question:** Run through the golden path. Count interruptions (modals, confirmations, unnecessary clicks). Target zero between starting a meeting and seeing its summary.

### 9.5 Convention and expectation

The user already has 20 years of UI muscle memory. Use it; don't fight it.

| Law | Principle | MeetFlow application |
|---|---|---|
| **Jakob's Law** | Users expect your product to work like the others | Meeting list looks like a calendar list. Transcript looks like a chat. Email composer looks like an email composer. The Mobbin references aren't a shortcut - they're the law in action. Mirror Granola / Fireflies / Linear patterns; don't reinvent. |
| **Mental Model** | Users come with a model of how the system works | The user thinks "AI extracts action items from what's said in the meeting." If the action items shown on /action-items don't trace back to a source meeting, the model breaks. The "from [meeting title]" line in each row exists for this reason. |
| **Aesthetic-Usability Effect** | Beautiful is perceived as more usable | The frontend polish work (Sec 4 of round 1) was not vanity - it changes how the prototype is judged. Investor and stakeholder demos rely on this effect. |
| **Paradox of the Active User** | Users don't read documentation, they start using the product | No instructional text on any screen. Every affordance must self-explain through label + position + style. Tooltips are the maximum acceptable documentation. |
| **Postel's Law** | Be liberal in what you accept, conservative in what you send | Forms should accept whatever the user types and clean it up server-side. Output should be tightly formatted and predictable. (Real-product rule; less relevant for this prototype but document it for the future.) |

**Review question:** A new user lands on this screen with zero prior context. Within 5 seconds, do they know what to do?

### 9.6 Pragmatism and prioritization

Where to spend design effort.

| Law | Principle | MeetFlow application |
|---|---|---|
| **Pareto Principle** | 80% of effects from 20% of causes | Polish the screens stakeholders actually demo. Don't gold-plate edge states no one will see in the walkthrough. |
| **Parkinson's Law** | Work expands to fill time available | Time-box design iterations. If you can't make a decision in 30 min, the choices are too close to matter - flip a coin and move on. |
| **Cognitive Bias** | Users (and designers) systematically err | Design defensively. Don't assume the user will read the warning, click the right button, or notice the badge. Make the right thing the path of least resistance. |

**Review question (for the project, not the screen):** Of all the design improvements I could make this week, which 20% will drive 80% of the perceived quality? Do those first.

### 9.7 The pre-merge Laws checklist (add to Section 8)

Walk this in addition to Section 8's mechanical checklist:

- [ ] Cognitive load: nothing on screen that doesn't help the user's current decision.
- [ ] Miller / Hick: no list, menu, or option set with more than ~9 items.
- [ ] Proximity / Common Region: visual groups match conceptual groups (squint test).
- [ ] Selective Attention: one unmistakable primary action per scope.
- [ ] Serial Position: most important content first or last in any sequence.
- [ ] Jakob's Law: pattern mirrors what users see in other meeting / productivity tools (cite the Mobbin reference).
- [ ] Mental Model: nothing on screen contradicts the user's understanding of what the system does.
- [ ] Goal-Gradient: long flows show progress.
- [ ] Peak-End: the closing moment of any flow feels good.

---

## 10. When in doubt

Open the official source. The five I trust most:
- WCAG 2.2: https://www.w3.org/WAI/WCAG22/quickref/
- Apple HIG: https://developer.apple.com/design/human-interface-guidelines/
- Material Design 3: https://m3.material.io/
- Refactoring UI book / blog: https://www.refactoringui.com/
- Laws of UX (Jon Yablonski): https://lawsofux.com/ and the O'Reilly book

For Figma-specific guidance (Auto Layout padding, component variants), Figma's help center: https://help.figma.com/hc/en-us/categories/360002051613-Design

If a rule here conflicts with one of the above on a specific value, the official source wins and the rule should be updated.
