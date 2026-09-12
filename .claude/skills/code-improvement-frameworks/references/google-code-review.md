# Google engineering practices: the code review standard

**Sources, both first-party Google:**
1. https://google.github.io/eng-practices/review/reviewer/looking-for.html
2. https://google.github.io/eng-practices/review/reviewer/standard.html

Google's guide is written for reviewing a CL (change list, their term for a change under review). It maps cleanly onto reviewing a diff, a PR, or a set of files.

## Contents

1. The standard, and why it bounds your findings
2. The twelve things to look for
3. The summary checklist, verbatim
4. Nit, and the severity discipline

---

## 1. The standard, and why it bounds your findings

This is the part that should shape a review more than any checklist, because it decides what is worth saying at all:

> "In general, reviewers should favor approving a CL once it is in a state where it definitely improves the overall code health of the system being worked on, even if the CL isn't perfect."

> "A key point here is that there is no such thing as 'perfect' code, there is only better code."

> "Instead of seeking perfection, what a reviewer should seek is continuous improvement."

> "A CL that, as a whole, improves the maintainability, readability, and understandability of the system shouldn't be delayed for days or weeks because it isn't 'perfect.'"

> "Rather, the reviewer should balance out the need to make forward progress compared to the importance of the changes they are suggesting."

The practical consequence for an improvement report: a finding earns its place only if acting on it makes the codebase healthier. Length is not thoroughness. Twenty findings where four matter is a worse review than the four on their own, because the author now has to do the sorting you were supposed to do.

---

## 2. The twelve things to look for

In Google's order, which is deliberate: design first, style last.

1. **Design.** "The most important thing to cover in a review is the overall design of the CL." Do the interactions between pieces make sense, and does this change belong in this codebase at all.
2. **Functionality.** "Does this CL do what the developer intended?" Think about edge cases and concurrency. For user-facing changes, look at the behaviour, not only the code.
3. **Complexity.** "Is the CL more complex than it should be?" Their test for complexity is whether a reader can understand it quickly, and whether a future developer is likely to introduce bugs when they touch it. This criterion explicitly covers over-engineering: solving the problem in front of you rather than a speculative future one.
4. **Tests.** Ask for unit, integration, or end-to-end tests as appropriate. Check the tests are valid and would actually fail if the code broke. A test that passes no matter what is worse than no test, because it buys false confidence.
5. **Naming.** "Did the developer pick good names for everything?" A good name communicates what the thing is or does without being so long that it is hard to read.
6. **Comments.** "Comments are useful when they explain why some code exists, and should not be explaining what." A comment explaining what the code does usually means the code should be clearer instead.
7. **Style.** Follow the applicable style guide. Non-mandatory style points get the `Nit:` prefix. Do not block on personal preference.
8. **Consistency.** The style guide wins. Where the guide is silent, stay consistent with the existing code. If the existing code is wrong and fixing it is out of scope, file it rather than expanding the change.
9. **Documentation.** If the change affects how the code is built, tested, interacted with, or released, the corresponding docs need updating in the same change.
10. **Every line.** "Look at every line of code that you have been assigned to review." If you cannot understand a piece, say so and ask, because if you cannot follow it neither can the next person.
11. **Context.** Look at the surrounding code and the system, not only the diff. A change can look fine line by line and still be making a file steadily worse.
12. **Good things.** Say when something is done well. A review that is only defects trains the author to dread reviews, and it also throws away the cheapest way to reinforce a pattern you want repeated.

---

## 3. The summary checklist, verbatim

Google's own closing list. Use it as the final sweep before publishing a review.

> - The code is well-designed.
> - The functionality is good for the users of the code.
> - Any UI changes are sensible and look good.
> - Any parallel programming is done safely.
> - The code isn't more complex than it needs to be.
> - The developer isn't implementing things they might need in the future.
> - Code has appropriate unit tests.
> - Tests are well-designed.
> - The developer used clear names for everything.
> - Comments are clear and useful, and mostly explain why instead of what.
> - Code is appropriately documented.
> - The code conforms to our style guides.

---

## 4. Nit, and the severity discipline

> "Reviewers should always feel free to leave comments expressing that something could be better, but if it's not very important, prefix it with something like 'Nit: ' to let the author know that it's just a point of polish that they could choose to ignore."

Use it. The `Nit:` prefix is what makes the rest of the review credible: when everything is stated at the same volume, the author cannot tell what actually matters and defensively argues with all of it.

Mapping to the severity scale used in improvement reports:

| Google criterion | Usual severity |
|---|---|
| Design, Functionality, Complexity | Major |
| Tests (missing coverage of real logic) | Major |
| Naming, Comments, Consistency, Documentation | Minor |
| Style, formatting, personal preference | Nit |

One caveat specific to this repo. There is no test runner wired up, so the Tests criterion rarely converts into "add a unit test". Convert it instead into "is this logic verifiable at all", and note where a pure function extracted out of a component would make it testable later. `npm run typecheck` inside `15-prototype/` is the only automated gate available.
