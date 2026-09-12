---
name: code-improvement-frameworks
description: "Named, first-party frameworks for judging and improving code quality - Martin Fowler's refactoring catalog and code smells, Google's engineering-practices code review standard, and the official React, Next.js and TypeScript guidance. Use this skill whenever you are reviewing, improving, refactoring, polishing, or critiquing code, or deciding whether a piece of code is good enough: it turns a vague 'this feels messy' into a named smell, a named refactoring, and a citable source. Load it before writing any code-quality finding, including inline review comments, PR reviews, refactor plans, and improvement reports, and even when the request sounds like a quick once-over. Preload it into review subagents through the `skills:` frontmatter field rather than restating its content in the agent body."
---

# Code Improvement Frameworks

## Why this exists

An improvement suggestion is only actionable if the reader can look it up. "This function is doing too much" is an opinion. "This is a Long Function, apply Extract Function (Fowler)" is a named diagnosis with a documented mechanical fix, and the author can decide for themselves whether they agree.

Naming the framework also stops you inventing standards. If a finding cannot be traced to one of the sources below or to the repo's own rules, it is probably a personal preference, and personal preference is the weakest thing to put in a review.

## The three lenses and which framework owns each

| Lens | Framework | Reference file |
|---|---|---|
| Readability and structure | Fowler's code smells plus the refactoring catalog | `references/refactoring-catalog.md` |
| Best practices and review judgement | Google engineering practices, "What to look for in a code review" | `references/google-code-review.md` |
| Performance and framework correctness | Official React, Next.js and TypeScript guidance | `references/react-nextjs-typescript.md` |

Read the reference file for a lens before writing findings under that lens. Each file is short and has its own table of contents. Do not paraphrase them from memory, because the value here is that the names are exact.

## How to use this in a review

1. **Read the code first, framework second.** Form the observation on your own, then reach for the name. Going the other way round produces findings that fit the catalog rather than the code.
2. **Name the smell, then the refactoring.** The smell is the diagnosis, the refactoring is the prescription. `references/refactoring-catalog.md` carries the lookup table from one to the other.
3. **Cite the source in the finding.** One short attribution, for example `Fowler, Long Function -> Extract Function` or `Google: Complexity`. The reader can then go and read the same page you did.
4. **Apply Google's standard to decide whether it is worth saying at all.** Their bar is code health, not perfection: "Reviewers should not require the author to polish every tiny piece of a CL before granting approval." A finding that would not improve the health of the codebase is noise.
5. **Mark preference explicitly.** Google's convention is the `Nit:` prefix for anything non-blocking and stylistic. Use it. A review where everything reads as equally urgent teaches the author to ignore all of it.
6. **Respect the repo's own rules over any general framework.** Read `./CLAUDE.md` and `./.claude/rules/*.md` first. Where a project rule and a general principle disagree, the project rule wins, and a general principle is never a reason to violate one.

## Severity, and why it is bounded

Rank findings by their effect on code health, using Google's framing:

1. **Major** - a design problem, a correctness or complexity issue, a missing test for real logic, or a violation of a repo rule. Worth blocking on.
2. **Minor** - a real improvement the author should make but that does not need to gate the change.
3. **Nit** - preference. Prefix with `Nit:` and never argue about it.

Google's counterweight is worth holding on to: "Instead of seeking perfection, what a reviewer should seek is continuous improvement." If every finding you produce is Major, the severity scale has stopped carrying information.

## What this skill deliberately does not cover

1. **Security and correctness bug hunting.** That is a different job with different sources (OWASP, the language's own security guidance). Flag a bug if you trip over it, then hand it to a security or correctness review rather than half-doing it here.
2. **Visual and UX quality.** In this repo that lives in `.claude/rules/ui-design-quality.md` and it is binding on prototype `.tsx`.
3. **Speculative performance work.** Fowler and Google agree on this one. Do not restructure code for speed without a measurement showing it is hot. An unmeasured performance finding is a guess wearing a suit.

## Applying it to this repo

The only runnable code lives in `15-prototype/` and `16-zomato/` (Next.js 14 App Router, React 18, TypeScript, Tailwind). So in practice:

1. The React and Next.js reference does the heaviest lifting, because most real findings here are Client and Server Component boundaries, unnecessary Effects, and re-render cost.
2. `npm run typecheck` inside `15-prototype/` is the fastest correctness gate and the only one wired up. There is no test runner, so Google's "Tests" criterion mostly converts into "is this logic verifiable at all", not "where are the unit tests".
3. Everything outside those two folders is Markdown and PPTX. There is no code to improve there, and saying so in one line is a better outcome than manufacturing findings.

## Finding format

Each finding should carry enough for the author to act without asking you a follow-up question.

```
### <one-line title>  [Readability | Performance | Best practices]  [Major | Minor | Nit]
**Where:** `path/to/file.ts:42`
**Framework:** <named smell or criterion, and the source>
**Current:**
```<lang>
<the code exactly as it is>
```
**Suggested:**
```<lang>
<the improved version>
```
**Why:** <one or two lines. What it costs now, what the fix unlocks.>
```

The `Framework` line is the part that makes this skill worth loading. If you cannot fill it in from one of the reference files or from a repo rule, that is a strong signal the finding is preference, so either downgrade it to `Nit:` or drop it.

## Sources

All first-party, all validated on 02-08-2026.

1. Refactoring catalog - https://refactoring.com/catalog/
2. Code Smell (Fowler) - https://martinfowler.com/bliki/CodeSmell.html
3. What to look for in a code review (Google) - https://google.github.io/eng-practices/review/reviewer/looking-for.html
4. The standard of code review (Google) - https://google.github.io/eng-practices/review/reviewer/standard.html
5. You Might Not Need an Effect (React) - https://react.dev/learn/you-might-not-need-an-effect
6. Server and Client Components (Next.js) - https://nextjs.org/docs/app/getting-started/server-and-client-components
7. TypeScript do's and don'ts - https://www.typescriptlang.org/docs/handbook/declaration-files/do-s-and-don-ts.html
8. Web Vitals - https://web.dev/articles/vitals
