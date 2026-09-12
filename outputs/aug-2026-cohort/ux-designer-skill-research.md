# UX Designer Skill - Source Research

**Date:** 02-08-2026
**Purpose:** Decide which books and frameworks the `ux-designer` skill should be built on, before we write a single line of the skill.
**Status:** For Aman's review. Nothing is built yet.

---

## 1. How this list was built

1. Searched for the current best-selling and most-recommended UI/UX books (August 2026), then cross-checked the titles that appear on more than one independent list.
2. Kept only books that give a **named, reusable framework**, not just opinions. A skill needs procedures, not inspiration.
3. Every link below is a **first-party source**: the author's own site, the official book site, or the publisher. Each URL was checked and returns 200. No Amazon links, no blog summaries.

---

## 2. The books, their frameworks, and what each gives the skill

| # | Book | Author | The framework it gives us | Why it matters for this skill |
|---|---|---|---|---|
| 1 | [The Design of Everyday Things](https://jnd.org/books/) | Don Norman | Affordances, signifiers, mapping, feedback, constraints. Plus the Seven Stages of Action and the Gulf of Execution / Gulf of Evaluation | This is the diagnostic layer. It tells the skill **why** a screen confuses a user, not just that it looks wrong. Every "the user does not know what to do next" bug traces back to one of these five. |
| 2 | [Don't Make Me Think](https://sensible.com/dont-make-me-think/) | Steve Krug | Krug's laws of usability, the "trunk test" for orientation, satisficing behaviour, guerrilla usability testing | The cheapest quality gate we have. The trunk test is a 6-question check the skill can run on any screen it produces. Also gives us the rule that users scan and satisfice, they do not read. |
| 3 | [Refactoring UI](https://www.refactoringui.com/) | Adam Wathan, Steve Schoger | Visual hierarchy by weight and contrast, a fixed spacing and type scale, limited palette, depth through shadow, "design the content first" | The single highest-value book for our case, because we generate Tailwind or React UI. It converts taste into rules a model can actually follow. This is what stops output looking like a 2015 admin panel. |
| 4 | [Laws of UX](https://lawsofux.com/) ([book page](https://jonyablonski.com/work/laws-of-ux/)) | Jon Yablonski | 21 named laws across four groups: heuristics, Gestalt principles, cognitive biases, and principles. Fitts, Hick, Jakob, Miller, Von Restorff, Peak-End, Aesthetic-Usability | Gives the skill vocabulary to **justify** a decision. "Hick's Law, so we cut the menu from 11 to 5" is defensible. "It felt cleaner" is not. The site is free and structured, so it is easy to encode. |
| 5 | [The Elements of User Experience](http://www.jjg.net/elements/) | Jesse James Garrett | The Five Planes: Strategy, Scope, Structure, Skeleton, Surface | The spine of the whole skill. It forces the work in the right order, so we do not jump to colours before we know the user goal. Every other framework hangs off one of these five planes. |
| 6 | [About Face (4th ed.)](https://www.wiley.com/en-us/About+Face%3A+The+Essentials+of+Interaction+Design%2C+4th+Edition-p-9781118766576) | Alan Cooper et al. | Goal-Directed Design: personas, goals vs tasks, interaction frameworks, product postures, and "excise" (work the interface makes the user do for no benefit) | Excise is the concept I want most. It gives the skill a named target to cut. Postures (sovereign, transient, daemonic) tell us how dense a screen should be, which is a decision we currently make by feel. |
| 7 | [Atomic Design](https://atomicdesign.bradfrost.com/) | Brad Frost | Atoms, molecules, organisms, templates, pages | This is how the skill should structure the code it writes. It maps cleanly to React components, so the design method and the file structure become the same thing. Free to read online. |
| 8 | [Design Systems](https://www.smashingmagazine.com/printed-books/design-systems/) | Alla Kholmatova | Functional patterns vs perceptual patterns, loose vs strict systems, defining design principles before components | Atomic Design tells us how to break things down. This tells us how to keep them coherent, and when a system should be strict versus loose. Useful when the skill has to work inside an existing product. |
| 9 | [Universal Principles of Design](https://www.quarto.com/books/9781631597480/universal-principles-of-design-updated-and-expanded-third-edition) | William Lidwell et al. | 125 named design principles with examples, one per spread | A reference, not a method. Good as a lookup table the skill can cite, but too broad to be the backbone. |
| 10 | [100 Things Every Designer Needs to Know About People](https://www.peachpit.com/store/100-things-every-designer-needs-to-know-about-people-9780136746911) | Susan Weinschenk | 100 research-backed findings on perception, memory, attention, motivation, decision-making | Overlaps heavily with Laws of UX but goes deeper on the research. Treat it as the evidence base behind #4, not a separate framework. |
| 11 | [Hooked](https://www.nirandfar.com/hooked/) | Nir Eyal | The Hook Model: Trigger, Action, Variable Reward, Investment | Useful only for retention and habit features. Also carries an ethical risk, so if we include it, the skill must pair it with a "is this manipulative" check. |
| 12 | [Lean UX](https://jeffgothelf.com/books/) | Jeff Gothelf, Josh Seiden | Assumptions to hypotheses to MVP to learning. Outcomes over outputs | Connects design to evidence. Stops the skill producing a beautiful screen nobody validated. Overlaps with our existing `experiment-design` and `outcome-vs-output` skills. |
| 13 | [Sprint](https://www.thesprintbook.com/) | Jake Knapp et al. | The five-day design sprint: Map, Sketch, Decide, Prototype, Test | A process for a team in a room. Less useful for a Claude Code skill working solo, but the "Decide" and "Prototype" days give a good structure for generating and choosing between UI options. |
| 14 | [Articulating Design Decisions](https://www.tomgreever.com/book/) | Tom Greever | A structure for explaining and defending a design decision to stakeholders | This is the piece almost every UI skill misses. If the skill states **why** each choice was made, you can review it in two minutes instead of guessing. |
| 15 | [Inspired](https://www.svpg.com/books/inspired-how-to-create-tech-products-customers-love/) | Marty Cagan | Product discovery, opportunity assessment, four risks (value, usability, feasibility, business viability) | Already covered by your existing PM skills (`product-discovery`, `write-prd`). Listed for completeness, not proposed for inclusion. |

---

## 3. Non-book official resources worth encoding

These are free, first-party, and update more often than any book. For a skill, they are more valuable than half the list above.

| Resource | Owner | What it gives us |
|---|---|---|
| [10 Usability Heuristics for User Interface Design](https://www.nngroup.com/articles/ten-usability-heuristics/) | Nielsen Norman Group | The 10-point heuristic evaluation. This is the industry-standard review checklist and the natural quality gate for the skill. |
| [Material Design 3](https://m3.material.io/) | Google | A complete, current spec for component behaviour, spacing, motion, and states. Good default when we have no design system. |
| [Human Interface Guidelines](https://developer.apple.com/design/human-interface-guidelines/) | Apple | The platform rules for anything Apple-facing, and the best-written source on interaction patterns generally. |
| [WCAG 2.2 Quick Reference](https://www.w3.org/WAI/WCAG22/quickref/) | W3C / WAI | Accessibility as testable success criteria. This is the only part of the skill that can be checked mechanically, so it should be a hard gate, not advice. |
| [Laws of UX site](https://lawsofux.com/) | Jon Yablonski | The 21 laws in structured, free form. Easier to encode than the book. |

---

## 4. My recommendation: which frameworks actually go into the skill

Fifteen books cannot fit in one skill. My proposal is six layers, each owned by one primary framework, so there is no overlap and no argument about which rule wins.

| Layer | Primary framework | Source | What the skill does here |
|---|---|---|---|
| 1. Spine (order of work) | Five Planes | Garrett (#5) | Force Strategy and Scope before Surface. Refuse to pick colours before the user goal is written down. |
| 2. User and goal | Goal-Directed Design, excise | Cooper (#6) | Name the persona, the goal, and the excise being removed. Pick the product posture. |
| 3. Diagnosis | Affordances, signifiers, Gulfs of Execution and Evaluation | Norman (#1) | For every screen, state what the user can do, how they know, and how they know it worked. |
| 4. Visual craft | Hierarchy, spacing scale, type scale, palette, depth | Refactoring UI (#3) + Laws of UX (#4) | The concrete rules that make output look 2026, not 2015. |
| 5. Structure of the build | Atoms to pages | Atomic Design (#7) + Kholmatova (#8) | Component breakdown that maps 1:1 to the React file structure. |
| 6. Gate before handover | 10 heuristics + WCAG 2.2 AA + the trunk test | NN/g + W3C + Krug (#2) | A pass or fail check with evidence, run before anything is shown to you. |

**Cross-cutting:** every deliverable ends with a short "why" section in Greever's structure (#14), so a review takes two minutes.

**Left out on purpose:** Hooked (#11) unless we are explicitly designing for retention, Sprint (#13) because it is a team-in-a-room process, Inspired (#15) and Lean UX (#12) because your existing PM skills already cover discovery and validation. Universal Principles (#9) and 100 Things (#10) stay as a lookup reference, not as the method.

---

## 5. What I need from you before building

1. **Scope:** should this skill design **new** UI from a brief, **review and improve** existing UI, or both? Both is fine, it just means two entry paths inside one skill.
2. **Output format:** does it produce a design brief in Markdown, working React or Tailwind code in `15-prototype/`, or an HTML mockup? This changes the whole build.
3. **The six-layer stack above:** does it look right, or do you want a different framework owning any layer?
4. **Anything to add:** if there is a book or a system you already trust and it is not on this list, tell me and I will fold it in.

Just correct me if I have got any of this wrong. Once you confirm, I will build the skill using the Anthropic Skill Creator standard, with the layers above as the body and the gate in section 4 as a build-time check rather than something you have to ask for.
