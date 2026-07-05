---
name: pr-faq
description: Run Amazon's Working Backwards PR/FAQ process as a guided interview, then produce a full PR/FAQ document plus an explicit Go / No-Go / Not-Yet build decision. Use this skill when the user says "PR FAQ", "PRFAQ", "press release FAQ", "working backwards", "should we build this", "is this feature worth building", "help me decide whether to build X", "pressure-test this idea", "write a PR/FAQ for [feature]", or wants to validate a feature idea before committing engineering time. Also trigger when the user has a feature idea and wants a customer-first go/no-go decision, even if they never say "PR/FAQ".
---

# PR/FAQ — Working Backwards Decision Tool

Amazon's PR/FAQ is a forcing function. You write the launch announcement *before* you build anything, so the idea has to earn its customer before it earns a single sprint. This skill runs that process as an interactive interview, stores every answer, then writes the full PR/FAQ document and ends with an explicit build verdict.

The point is not to produce a nice document. The point is to expose whether the idea is worth building. A weak idea should feel weak by the time the verdict lands. Stay truth-seeking, not selling (see `references/working-backwards-guide.md`).

## What this produces

1. A **working answers file** that captures the interview as it happens (so nothing is lost across turns and the interview is resumable).
2. A **full PR/FAQ document**: one-page mock press release + external (customer) FAQ + internal (leadership) FAQ.
3. A **verdict**: `GO` / `NO-GO` / `NOT-YET`, with reasoning, feasibility risk flags, and the conditions that would flip a No.

## Step 1: Set up and detect context

Get the feature name from the user (ask if not given). Then check whether product context exists in the repo and read what's relevant:

- Product / company context (e.g. `03-product-knowledge/*`, `04-strategy/*`)
- Personas (e.g. `05-user-personas/*`)
- Feedback and interviews (e.g. `06-user-feedback/*`, `07-user-interviews/*`)
- Competitive landscape (e.g. `03-product-knowledge/competitive.md`)

This skill is generic — it works for any product. If no such context exists, just interview the user cold. If it does exist, use it to inform sharper questions and to pre-fill draft answers the user can confirm or correct. **Cite the source file for every number or quote you pull from the repo. Never invent a metric or a user quote.**

Tell the user in one line what you found (or that you found nothing and will interview cold).

Create the working answers file now:
`outputs/pr-faq-<feature-slug>-answers-<DD-MM-YYYY>.md` with a heading and an empty section per question. If it already exists, read it and resume from the first unanswered question.

## Step 2: Interview — one question at a time

Ask **one question per message**. This is deliberate: the discipline of answering each dimension in isolation is where the thinking happens. Do not batch. After the user answers, **append their answer to the working file immediately**, then ask the next question.

Adapt to the answers. If context files already answer a question, propose a draft answer and ask the user to confirm or correct it rather than asking cold. Ask a targeted follow-up only when an answer is too thin to write a credible PR/FAQ section from — do not follow up for its own sake.

Ask these nine, in order. The reasoning in italics is for you, not to be read aloud verbatim.

1. **Customer** — Who exactly is this for? One specific segment, not "everyone." *A fuzzy customer is the most common reason a PR/FAQ collapses at the verdict.*
2. **Problem** — What is their single biggest problem here, in their words? How painful is it today, and how do you know? *Rank to one problem. Push for evidence, not assertion.*
3. **Today's alternatives** — What do they use to solve it now, and where does that fall short? *This becomes the "today customers use X, it falls short because Y" line and feeds differentiation.*
4. **Solution** — What is the product/feature, in one or two plain sentences? What does it do for them? *No jargon, no internal acronyms.*
5. **How it works** — What is the customer's first experience, start to value? *Concrete steps, not a feature list.*
6. **Differentiation** — Why is this remarkable versus the alternatives and named competitors? What can you do that they structurally can't or won't? *If the honest answer is "nothing much," the verdict must say so.*
7. **Strategic fit** — How does this serve the product vision and current goals/OKRs? What does it trade off against? *Cite the vision/OKR file if present.*
8. **Size** — How many customers have this problem, and how much is solving it worth to them? Rough is fine; state the basis. *Substantial addressable problem, or niche?*
9. **Top risks** — What are the three things most likely to make this fail? Include feasibility, data/model, and adoption risks. *These become internal FAQ answers and verdict risk flags.*

When all nine are answered (and any follow-ups resolved), confirm with the user: "Ready to write the PR/FAQ and verdict?" Then proceed.

## Step 3: Write the PR/FAQ + verdict

Read `references/prfaq-template.md` for the exact document skeleton and `references/working-backwards-guide.md` for the writing rules and the verdict rubric. Write the final document to `outputs/pr-faq-<feature-slug>-<DD-MM-YYYY>.md`.

Build it strictly from the stored answers and cited context. Do not smuggle in invented metrics, quotes, or capabilities. The interview implicitly authorizes a long document, so write it in full without asking permission for length.

Two non-negotiable checks before you finish:

- **Press-release litmus test**: reread the press release as a customer. If it would not make that customer want the product, the idea is not ready — say so plainly in the verdict rather than dressing it up.
- **Verdict honesty**: the verdict follows from the answers, not from politeness. A great idea nobody can differentiate is a `NO-GO`. A strong idea with an unresolved blocking risk is a `NOT-YET` with the blocker named. Always end with "what would have to be true to flip this."

## Writing rules

- Dates in `DD-MM-YYYY`. No em dashes (use commas or hyphens). No emojis.
- Every repo-sourced number or quote carries its source file. No invented data.
- Validate any URL before it goes in the document (`curl -s -o /dev/null -w "%{http_code}" -L --max-time 10 <url>`); keep only 2xx (or 999 for anti-bot sites).
- Plain, customer-facing language in the press release. Save the hard internal questions for the internal FAQ.
