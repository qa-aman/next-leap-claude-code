# PR/FAQ Document Template

Fill this skeleton from the stored interview answers. Keep the press release to roughly one page. The whole document should read like a real launch announcement followed by an honest Q&A, not like an internal spec.

Replace every `[bracketed]` prompt. Delete guidance notes (the lines in _italics_) from the final output.

---

```markdown
# PR/FAQ: [Feature Name]

**For internal review — [DD-MM-YYYY]. Proposed launch: [Month YYYY].**

---

## Press Release

### [Heading — the product/feature in one plain sentence a customer would understand]
_No internal names or acronyms. This is what the world would read._

#### [Subheading — the target customer and the core benefit, one sentence]

**[Launch City], [Month YYYY]** — [Summary paragraph: 2-4 sentences. What is launching, for whom, and the single most important benefit. Written as if it already shipped.]

**The problem.** [The customer's top problem in their own terms, ranked to the one that hurts most. Name who has it and how painful it is. Cite evidence/source if from repo. Establish that the addressable problem is substantial, not niche.]

**The solution.** [How the product solves that problem. Use the shape: "Today, customers use [X, Y, or Z]. Those fall short because [gap]. [Product] addresses this by [how]." Keep it concrete and customer-facing.]

> "[Company spokesperson quote: why the team decided to tackle this problem now, and what it means for customers. One or two sentences.]"
> — [Name, Title]

> "[Customer quote: realistic and specific, showing the before/after value in the customer's voice. Imaginary but must sound like a real person, not marketing.]"
> — [Customer name, role, company type]

**Getting started.** [One sentence on how a customer starts using it, with a link or equivalent call to action.]

---

## External FAQ
_Questions a customer or the press would ask. Short, direct, customer-facing._

**How much does it cost?**
[Answer, or the pricing logic if not final.]

**How does it work?**
[Answer, in customer terms.]

**Who is it for / who is it not for?**
[Answer.]

**How do I get help or support?**
[Answer.]

**When and where can I get it?**
[Answer: availability, platforms, rollout.]

---

## Internal FAQ
_The hard questions leadership and the team will ask. This is where the idea is stress-tested. Be honest, not persuasive._

**How big is the problem / what is the addressable size?**
[Number of customers affected and value of solving it. State the basis. Cite source if from repo.]

**How is this differentiated from what customers use today and from competitors?**
[Name the alternatives and named competitors. State what this does that they structurally can't or won't. If differentiation is weak, say so.]

**What new capabilities do we need to build or acquire?**
[Tech, data, model, integrations, team.]

**What are the economics?**
[Cost to build and run, expected revenue or retention impact, rough per-unit economics if relevant.]

**What is the upfront investment and time to ship?**
[Effort, timeline, what it displaces on the roadmap.]

**What must be true for this to succeed? (key assumptions)**
[The load-bearing assumptions. What are we betting on.]

**What are the top three risks that would make this fail?**
1. [Risk — likelihood and what would trigger it]
2. [Risk]
3. [Risk]

---

## Verdict

**GO / NO-GO / NOT-YET** — [state one, up top, no hedging]

**Why:**
- **Customer clarity:** [strong / weak — is the customer specific and real?]
- **Problem size:** [substantial / niche — is it worth solving?]
- **Differentiation:** [defensible / thin — versus alternatives and competitors]
- **Strategic fit:** [aligned / off-strategy — versus vision and current goals]

**Feasibility risk flags:** [The feasibility/data/capacity concerns, flagged not scored. These inform the verdict but do not lead it.]

**What would have to be true to flip this to a GO:**
- [Condition 1]
- [Condition 2]

[If GO: one line on the single most important thing to get right first. If NOT-YET: name the blocking item and how to resolve it. If NO-GO: name the fatal flaw plainly.]
```

---

## Filling notes

- Pull the press release straight from the customer/problem/solution/how-it-works answers. It should need no new information beyond the interview.
- The problem paragraph must make the reader feel the pain. If it reads flat, the problem may be too small — that is a signal for the verdict.
- Keep external FAQ answers short. Route anything hard, uncertain, or internal to the internal FAQ.
- The verdict is not a summary. It is a decision. It must be answerable "yes I'd stake a sprint on this" or "no, here's why."
