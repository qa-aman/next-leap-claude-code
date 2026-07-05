# Working Backwards — PR/FAQ Framework Guide

Source basis: Colin Bryar and Bill Carr, *Working Backwards* (the two Amazon executives who codified the process), and the authors' own template and instructions at workingbackwards.com. This guide distills the rules the skill enforces. It is background for you (the model), not user-facing.

## The core idea

Instead of starting with a technology or a feature and hunting for a market, you start with the customer's need and work backwards to the solution. You write the launch press release *first*, before building anything. If the announcement of the finished product would not make the target customer want it, the idea is not ready, and no amount of building fixes that.

This is a **forcing function for customer obsession**. The discipline lives in the writing: vague thinking produces a vague press release, and a vague press release is visibly weak.

## Truth-seeking, not selling

The PR/FAQ exists to find out whether an idea is good, not to convince anyone it is. When you write and when you render the verdict, default to honesty over persuasion. The internal FAQ specifically exists to surface the hardest objections, the biggest risks, and the weakest assumptions. A PR/FAQ that hides its risks has failed at its only job.

This is why the verdict must be willing to say NO-GO. A tool that always concludes "build it" is worthless as a decision aid.

## The document, in two parts

### Part 1 — Press release (about one page)

Written from a future date, announcing the product as if it already shipped. Plain, customer-facing language. No jargon, no internal acronyms, no roadmap-speak. It answers three questions: who is the customer, what problem does this solve, and why is the solution remarkable.

Standard sections:
- **Heading** — the product in one sentence.
- **Subheading** — target customer and the benefit, one sentence.
- **Summary paragraph** — launch date/location and a plain overview.
- **Problem paragraph** — the customer's top pain, from their perspective, ranked. Must establish a substantial addressable problem.
- **Solution paragraph(s)** — how it solves the problem. The canonical shape: "Today, customers use X, Y, or Z. Those fall short because [gap]. [Product] addresses these unmet needs by [how]."
- **Spokesperson quote** — one, from a company leader: why tackle this now.
- **Customer quote** — one, imaginary but realistic: the value in the customer's voice.
- **Getting started** — one sentence with the call to action / link.

### Part 2 — FAQ

Freeform in spirit (there are no mandatory questions), but split into two audiences:

- **External / customer FAQ** — what customers and the press will ask: price, how it works, who it's for, support, availability. Short and direct.
- **Internal FAQ** — longer and harder. The questions leadership and the team will raise: addressable market size (TAM), competitive differentiation, capabilities required, economics and per-unit economics, upfront investment, time to profitability/ship, load-bearing assumptions, and the top three risks that would make it fail. Regulatory or trust issues go here too when relevant.

## Process norms (from the authors)

- **First draft in hours, not days.** The value is in the thinking, not the polish.
- **Review by silent reading** (15-20 min) then discussion (~40 min). Reviewers evaluate: customer clarity, problem definition, whether the solution actually addresses the problem, the expected change in customer behavior, competitive differentiation, whether the TAM is big enough, and the constraints/risks.
- **PR/FAQ is for planning, not execution.** Once it clears the bar, normal delivery (Agile, etc.) takes over. The PR/FAQ is not the spec; it is the decision to invest in the spec.

## The verdict rubric (this skill's decision layer)

The user chose a **desirability-first** verdict: judge whether the idea is *worth* building. Feasibility is a risk flag that can gate a Go, not the primary axis.

Judge four dimensions qualitatively and opinionatedly. Resist scoring theatre and false precision — a number out of five hides the reasoning. State each as strong/weak with one line of why:

1. **Customer clarity** — is the customer one specific, real segment? Fuzzy customer = weak.
2. **Problem size** — is the problem painful and widespread enough to be worth solving? Niche or nice-to-have = weak.
3. **Differentiation** — can this do something the alternatives and named competitors structurally can't or won't? "Us too" = weak.
4. **Strategic fit** — does it serve the stated vision and current goals, and is the tradeoff worth it?

Then map to a verdict:

- **GO** — customer clear, problem substantial, differentiation defensible, strategically aligned, and no unresolved blocking risk. State the one thing to get right first.
- **NOT-YET** — the idea is fundamentally sound but a specific blocking item is unresolved (a key assumption untested, a feasibility/data risk unmitigated, a dependency not ready). Name the blocker and how to resolve it. This is a "come back when X is true," not a rejection.
- **NO-GO** — a dimension fails in a way effort won't fix: no real customer, problem too small, or no differentiation. Name the fatal flaw plainly. Do not soften it into a NOT-YET.

Always close with **"what would have to be true to flip this to a GO."** This makes even a No actionable, and it is the honest form of the answer to "can I build this?"

The press-release litmus test overrides everything: if the release, read as a customer, would not make that customer want the product, the verdict cannot be GO regardless of the dimensions.
