# Design Method - the six layers

Fifteen good books exist on this. Trying to apply all of them at once produces mush, so this method assigns **one owner per layer**. When two frameworks could both answer a question, the owner of that layer decides. That is the whole reason the table exists.

| Layer | Owner | Source |
|---|---|---|
| 1. Order of work | Five Planes | Jesse James Garrett, [The Elements of User Experience](http://www.jjg.net/elements/) |
| 2. User and goal | Goal-Directed Design, excise, posture | Alan Cooper, [About Face](https://www.wiley.com/en-us/About+Face%3A+The+Essentials+of+Interaction+Design%2C+4th+Edition-p-9781118766576) |
| 3. Diagnosis | Affordances, signifiers, the two Gulfs | Don Norman, [The Design of Everyday Things](https://jnd.org/books/) |
| 4. Visual craft | Hierarchy, scales, palette, depth | [Refactoring UI](https://www.refactoringui.com/) + [Laws of UX](https://lawsofux.com/) |
| 5. Build structure | Atoms to pages, pattern types | [Atomic Design](https://atomicdesign.bradfrost.com/) + [Design Systems](https://www.smashingmagazine.com/printed-books/design-systems/) |
| 6. Gate | 10 heuristics, trunk test, WCAG | [NN/g](https://www.nngroup.com/articles/ten-usability-heuristics/) + [Krug](https://sensible.com/dont-make-me-think/) + [W3C](https://www.w3.org/WAI/WCAG22/quickref/) |

Layer 4 lives in `visual-system.md`. Layer 6 lives in `review-gate.md`. This file covers 1, 2, 3, and 5.

---

## Layer 1 - Five Planes: the order of work

Garrett's insight is that UX decisions stack, and each plane constrains the one above it. Work bottom-up. Jumping to Surface first is the most common failure in AI-generated UI, and it is why so much of it looks polished and means nothing.

| Plane | The question it answers | What you produce |
|---|---|---|
| **Strategy** | What does the user want, and what does the business want | One sentence each. If they conflict, say so. |
| **Scope** | What features and content serve that | An in-list and an explicit out-list |
| **Structure** | How is it organised and how does the user move through it | Flow diagram, information architecture |
| **Skeleton** | Where does everything sit on the screen | Layout, hierarchy order, component inventory |
| **Surface** | What does it look and feel like | Tokens, type, colour, depth, motion |

**The check:** you may not name a colour until Strategy and Scope are written down. If you cannot state the user's goal in one sentence, you are not ready to design, you are ready to decorate.

The out-list on the Scope plane is doing more work than it looks. Naming what a screen is *not* for is the cheapest way to stop it becoming a dashboard of everything.

---

## Layer 2 - Goal-Directed Design: user, excise, posture

### Goals are not tasks

A task is "filter the list by owner". A goal is "know what I have to do today without reading everything". Tasks change with technology. Goals do not. Design for the goal and the tasks fall out of it, usually fewer than you started with.

Write, before designing:

1. **Persona.** A real one from `05-user-personas/` if one fits. If not, name the segment and its constraint.
2. **Goal.** One sentence, in the user's words, not the product's.
3. **The decision this screen serves.** If the screen serves more than one decision, it is probably two screens.
4. **Context of use.** Rushed, focused, on a phone between meetings, on a second monitor all day. This changes everything downstream.

### Excise - the thing to hunt

Excise is work the interface makes the user do that produces nothing for them. Extra confirmations, navigating to find a thing the system already knew, re-entering data the system holds, a settings page for a decision the system could make itself.

**Always publish an excise cut list.** Three to five lines, each saying what a user would have had to do and does not have to any more. This is the difference between a design and a drawing, and it is the fastest way for a reviewer to see whether you actually thought.

### Posture sets density

Cooper's postures answer "how much should be on this screen", which is otherwise decided by feel.

| Posture | Meaning | Density implication |
|---|---|---|
| **Sovereign** | Used for long stretches, full screen, by a user who becomes expert | Dense is correct. Optimise for the fifth hour, not the first minute. Muted palette, small controls, keyboard paths, information-rich. |
| **Transient** | Opened briefly to do one thing, then closed | Sparse and obvious. Large controls, generous spacing, no learning curve, no hidden state. |
| **Daemonic** | Runs invisibly, surfaces only to report or ask | Minimal. Show only what needs a decision. |

Getting this wrong is the usual cause of "it feels cluttered" (transient screen designed sovereign) or "it feels empty and slow to use" (sovereign screen designed transient).

---

## Layer 3 - Norman: diagnosing why a screen confuses people

Norman gives the vocabulary for *why* something is confusing, which matters because "it feels off" is not actionable and "the signifier is missing" is.

### The five concepts

1. **Affordance** - what an element makes possible. A button affords clicking.
2. **Signifier** - the perceivable signal that the affordance exists. The thing that *looks* like a button. Affordances without signifiers are invisible features. This is exactly why a borderless ghost button fails.
3. **Mapping** - the relationship between a control and its effect. Controls should sit near, and be arranged like, what they change.
4. **Feedback** - the system telling the user what just happened, immediately. Under 100ms feels instant. Above 400ms needs a visible response, even a skeleton.
5. **Constraint** - making the wrong action impossible rather than warning about it after the fact. Prefer a disabled state with a reason over an error message.

### The two Gulfs - the review question set

Walk every step of every flow and answer three questions. This is the highest-yield thing in this file.

1. **Gulf of Execution - "what can I do here?"** Does the user know what actions are available, without hovering, without documentation, without prior training?
2. **Gulf of Execution - "how do I do it?"** Is the path to the intended action obvious, or does it require a guess?
3. **Gulf of Evaluation - "did it work?"** After acting, does the user know what happened, what state they are now in, and what to do next?

Any step where an answer is "not really" is a defect with a name, a location, and a fix. Write it down that way.

---

## Layer 5 - Structure: atoms to pages, and keeping it coherent

### Atomic Design

Break the interface into five levels. The point is not tidiness, it is that this maps one-to-one onto a React component tree, so the mockup and the eventual build share a shape and the handover stops being a translation exercise.

| Level | What it is | Example |
|---|---|---|
| **Atoms** | Cannot be broken down further | Button, input, label, badge, icon |
| **Molecules** | A few atoms doing one job | Search field = label + input + button |
| **Organisms** | A distinct section of interface | Meeting row, nav bar, action-item card |
| **Templates** | Page-level layout with placeholder content | The dashboard grid |
| **Pages** | A template filled with real, specific content | The dashboard for a user with 3 meetings and 0 action items |

Always produce **pages, not templates**, for review, and always with realistic content. Lorem ipsum and "User Name" hide every layout bug that real content exposes: the long name, the empty list, the 47-character meeting title.

### Functional vs perceptual patterns

Kholmatova's split is what keeps a system coherent as it grows.

1. **Functional patterns** are behaviour: what a card is, what a confirmation flow does, how a filter works. These are decided by the product's domain.
2. **Perceptual patterns** are the feel: colour, spacing rhythm, type, shadow, motion, tone of voice. These are decided by the brand.

Keep them separate. A change to how something looks should never require changing what it does. When both are tangled in one component, every visual tweak becomes a behaviour risk.

### Strict or loose

Decide, and say which you chose. A **strict** system has few components with tight rules and is right when consistency matters more than expressiveness, which covers most product UI. A **loose** system allows local variation and is right for marketing pages and one-off campaigns. Trouble comes from being loose by accident, one exception at a time, until nothing matches.

---

## The two-minute output

Whatever you design, end with this. It is what makes a review fast rather than archaeological.

```
## Why this design

1. Who and goal: <persona>, trying to <goal>, in <context>
2. Posture: <sovereign / transient / daemonic>, so <density decision>
3. Hierarchy: first <x>, then <y>, last <z>
4. Excise removed: <3-5 lines>
5. Conventions borrowed: <pattern> from <product>, because Jakob's Law
6. States shipped: default, empty, loading, error, <first-run>
7. Assumptions I made: <list>
8. Open questions for you: <list, or "none">
```

Point 7 matters more than it looks. Stating an assumption lets a reviewer correct it in one line. Hiding it means it gets discovered after the build.
