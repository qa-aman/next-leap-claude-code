---
name: pre-build-interview
description: Run pre-build user interviews to validate whether a planned feature actually solves a real problem before engineering invests. Use when the user says "validate this feature", "should we build this", "interview users about [feature]", "test this feature idea", "pre-build validation", "is this feature worth building", "talk to users first", or has a feature idea and wants to pressure-test it with real users before writing a PRD or kicking off engineering. Also trigger when the user wants to avoid building something users will not adopt, when they say "what would users actually think of this", or when they have a hypothesis and need a structured interview plan. Combines Mom Test question discipline, Lean Customer Development hypothesis structure, JTBD Forces of Progress, and Opportunity Solution Tree synthesis into one workflow that ends with a clear build / iterate / kill recommendation.
---

# Pre-Build Interview

A structured workflow for validating a feature idea with real users before engineering invests. The skill ends with a build / iterate / kill recommendation grounded in evidence, not vibes.

## Why this exists

Most pre-build interviews fail for one of four reasons:

1. The interviewer pitches the feature and users politely confirm it.
2. There is no written hypothesis, so no signal threshold to fail against.
3. Users say "yes this is a problem" but never actually switch behavior, so the feature ships and dies.
4. Transcripts pile up with no decision framework to convert insight into a build call.

This skill addresses each one with a dedicated framework: Mom Test for question quality, Lean Customer Development for hypothesis structure, JTBD Forces of Progress for switching pressure, and Opportunity Solution Tree for synthesis.

## When to use this skill

Use this BEFORE writing a PRD or feature spec. If a spec already exists and is in engineering review, use `technical-review` or `spec-reviewer` instead.

Do not use this for ongoing discovery (use the broader `product-discovery` skill) or for post-launch validation (run a survey or analytics review instead).

## The Five Phases

| Phase | Output | Framework |
|---|---|---|
| 1. Define the hypothesis | One-page hypothesis doc | Alvarez (Lean Customer Development) |
| 2. Design the guide | Interview script with 8 to 12 questions | Mom Test |
| 3. Recruit | Recruit plan with target N and criteria | Alvarez |
| 4. Conduct | Transcript or notes per interview | Mom Test live discipline |
| 5. Synthesize and decide | Build / iterate / kill recommendation | JTBD Forces + Opportunity Solution Tree |

Work through them in order. Do not skip Phase 1. A skipped hypothesis means there is nothing to falsify, which means the interviews will confirm whatever the user already believes.

---

## Phase 1: Define the hypothesis

Read `references/alvarez-validation.md` for the full structure.

Produce a one-page hypothesis with these fields, filled in by the user:

- **Feature in one sentence** (no jargon)
- **Target user segment** (concrete, not "everyone")
- **Problem we believe they have** (one sentence)
- **Current workaround** they use today
- **Why the workaround is painful** (frequency, severity, cost)
- **What we would build if confirmed**
- **Signal thresholds**: how many out of N interviewees must (a) describe the problem unprompted, (b) describe a current workaround, (c) describe the workaround as painful, for us to proceed. Defaults: 60% / 70% / 50% across 8 to 12 interviews.
- **Kill criteria**: what we would have to hear to walk away

If the user has not picked a target segment, force the choice before moving on. Vague segments produce vague interviews.

## Phase 2: Design the interview guide

Read `references/mom-test.md` for the rewriting rules.

Build an interview script with this structure:

1. **Warmup** (2 questions): job, daily workflow context
2. **Past behavior** (3 questions): last time they hit the problem, what they did, what it cost them
3. **Current workaround** (2 questions): how they handle it today, what they have tried before
4. **Forces of progress** (2 to 3 questions): see `references/jtbd-forces.md`. Probe push, pull, anxiety, habit.
5. **Closing** (1 question): who else they know who deals with this

Every question gets checked against the Mom Test rules. The skill must rewrite any question that:
- Pitches the feature ("would you use a tool that...")
- Asks about the future ("would you pay for...")
- Asks for opinions on hypotheticals ("do you think...")
- Is leading ("how frustrating is it when...")

Reveal the feature concept ONLY in the final 5 minutes, after all behavioral data is captured. Even then, ask "what would have to be true for this to be useful" rather than "would you use this".

## Phase 3: Recruit

Target 8 to 12 interviews from the segment defined in Phase 1. Below 8, you are pattern-matching on noise. Above 12, you are usually wasting time once the pattern is clear.

Recruit plan must specify:
- Source (existing users, cold outreach, intercept, panel)
- Screener questions (3 max, behavioral, not "are you interested in X")
- Incentive (if any)
- Timeline

If the user has a list of existing users (for example, from `06-user-feedback/` or `07-user-interviews/` in this repo), prefer those. Use the feedback files to identify users who have already mentioned the relevant problem area.

## Phase 4: Conduct interviews

Hand the user a one-page interviewer checklist:

- Ask the question, then shut up. Silence pulls out the real answer.
- Anchor every claim in a specific past incident. "Tell me about the last time..."
- When they say "always" or "never", ask for the most recent example.
- Note emotional signals (frustration, resignation, workaround pride). These are stronger than stated opinions.
- Do not pitch. Do not defend the current product. Do not explain the feature.

Capture notes against a fixed template per interview:

```
## Interview [N] - [Date DD-MM-YYYY] - [Segment]

### Problem evidence
- Unprompted mention of problem: yes / no
- Specific incident described: [1-2 lines]
- Frequency: [how often]
- Severity (their words): [quote]

### Current workaround
- What they do today: [1-2 lines]
- Pain level (their words): [quote]
- Time or money cost: [if mentioned]

### Forces (from JTBD)
- Push (what is wrong with status quo):
- Pull (what they wish existed):
- Anxiety (what would block them switching):
- Habit (what keeps them on current solution):

### Feature reaction (only if revealed)
- First reaction:
- Conditions for usefulness:
- Red flags raised:
```

## Phase 5: Synthesize and decide

Read `references/jtbd-forces.md` and `references/opportunity-solution-tree.md`.

Aggregate across all interviews:

1. **Score against the Phase 1 thresholds**. For each threshold, report the actual number and whether it cleared.
2. **Map Forces of Progress**. For each interviewee, classify push, pull, anxiety, habit. A feature ships when push + pull clearly exceeds anxiety + habit across the sample. If anxiety or habit dominates, the feature will be ignored even if the problem is real.
3. **Build a mini Opportunity Solution Tree**. Outcome at the top, the 2 to 4 opportunities (user needs) you actually heard, the proposed feature as one possible solution under the most relevant opportunity, and the open assumptions that still need testing.

Then produce the recommendation. Use exactly one of three verdicts:

- **BUILD**: thresholds cleared, forces favor switching, opportunity tree shows the feature addresses a real and prioritized need. Note what to build first and what to defer.
- **ITERATE**: problem is real but the proposed solution is wrong, or forces show anxiety dominates. Reshape the feature and run a second round of 4 to 6 interviews on the revised concept.
- **KILL**: thresholds missed, or forces show habit dominates (users tolerate the problem). Document what was learned so the team does not relitigate this idea in 3 months.

## Output format

Save all artifacts to `outputs/pre-build-interview/[feature-slug]/`:

```
outputs/pre-build-interview/[feature-slug]/
├── 01-hypothesis.md
├── 02-interview-guide.md
├── 03-recruit-plan.md
├── 04-interviews/
│   ├── interview-01.md
│   ├── interview-02.md
│   └── ...
└── 05-decision.md
```

The final `05-decision.md` must lead with the verdict in the first line. Stakeholders will not read past the first paragraph. Structure:

```
# Decision: [BUILD / ITERATE / KILL] - [Feature name]

**Date:** DD-MM-YYYY
**Interviewees:** N
**Segment:** [segment]

## Verdict
[2-3 sentences: what we are doing and why]

## Evidence against thresholds
[Table: threshold | target | actual | pass/fail]

## Forces of Progress summary
[Push, Pull, Anxiety, Habit, with strength rating]

## Opportunity Solution Tree
[Outcome, 2-4 opportunities, proposed solution, open assumptions]

## What this means for the roadmap
[1-2 sentences tying back to product OKRs]
```

## Anti-patterns to refuse

- Skipping Phase 1 ("just write me the questions"). Refuse. Without a hypothesis, the interviews are theater.
- Asking the user to validate the feature concept itself in interview questions. Rewrite the question.
- Fewer than 6 interviews. Push back and recommend 8 minimum.
- Pitching the feature in the first 30 minutes. The whole point is to capture unprompted behavior.
- A decision doc that says "users like it" without naming threshold numbers.

## Frameworks reference

| File | When to read |
|---|---|
| `references/mom-test.md` | Phase 2 question design and Phase 4 live discipline |
| `references/alvarez-validation.md` | Phase 1 hypothesis and Phase 3 recruit plan |
| `references/jtbd-forces.md` | Phase 4 capture and Phase 5 force mapping |
| `references/opportunity-solution-tree.md` | Phase 5 synthesis and decision |

Read each one when you reach the relevant phase. Do not preload all four.
