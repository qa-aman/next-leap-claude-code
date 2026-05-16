---
paths:
  - "outputs/*prompt*.md"
  - "outputs/**/prompt*.md"
  - "prompts/**"
---

# Prompt-Writing Rules

Apply whenever the user asks to "create a prompt", "write a prompt", "draft a prompt", "review a prompt", or generate instructions for a fresh Claude / Claude Code session to execute. Task type does not matter: code, data, research, automation, evaluation, content, debugging, agent orchestration.

Target quality: **>95/100** against the rubric below. Self-score before delivering. Iterate silently until the score clears 95. Do not dispatch a subagent for review. This rule replaces that step.

---

## The Rubric (100 points)

| # | Dimension | Weight | What "good" looks like |
|---|---|---|---|
| 1 | Goal clarity | 12 | The done condition is one verifiable sentence. The executor knows when to stop. No ambiguity on what success means. |
| 2 | Context sufficiency | 10 | Background the executor lacks is supplied inline or via absolute paths. Assumptions stated. No implicit knowledge. |
| 3 | Inputs and outputs | 10 | Inputs: types, paths, formats, size. Outputs: location, filename or return shape, schema, expected size/count, side effects. |
| 4 | Constraints | 10 | Every hard rule from `~/.claude/CLAUDE.md` and project `CLAUDE.md` that applies is restated. Each constraint has a verifiable check where possible (grep, count, lint, test, schema validate). |
| 5 | Tool / skill / model selection | 8 | Exact tool names, skill slugs, library names, model tier guidance. Says which to use when. Forbids rewriting what exists. |
| 6 | Anti-hallucination guards | 10 | "Omit, do not fabricate." Verify-before-claim mandate. External facts cite source URL + DD-MM-YYYY fetch date. No guessing APIs, paths, or schemas. |
| 7 | Process discipline | 8 | Steps numbered when order matters. Approval gates marked with `### AWAITING APPROVAL`. Parallel-vs-sequential rules explicit. Stop conditions defined. |
| 8 | Failure modes | 8 | 5+ realistic failure modes for this task type, each with a defense. Pre-delivery self-audit instruction. |
| 9 | Reference fidelity | 6 | If references exist, exact paths AND specific patterns/sections/properties to mirror are enumerated. Vague "match style" banned. Skip cleanly if no reference. |
| 10 | Audience calibration | 6 | Reader/consumer named: role, technical baseline, banned jargon, framing rule. Skip if executor-only output. |
| 11 | Self-contained-ness | 6 | Fresh session executes end-to-end. Absolute paths. Referenced files verified to exist. No back-and-forth needed. |
| 12 | Self-verification | 6 | Executor checks own work before delivery: grep, count, dry run, test run, schema validate, lint, manual diff. At least one check per major output. |

Total: 100.

---

## Mandatory checklist before delivering any prompt

- [ ] Goal stated as one verifiable done-condition.
- [ ] Inputs listed with paths/types/formats. Outputs listed with paths/schemas/sizes.
- [ ] All applicable hard rules from global + project CLAUDE.md restated inline. Do not assume executor loads them.
- [ ] At least one verifiable check per constraint (grep, count, file-exists, schema, test).
- [ ] Tools/skills/models named exactly. For skills, name what to read inside and which helpers to reuse verbatim.
- [ ] External sources listed as specific URLs (not "the docs"). Anti-hallucination clause: "if fetch/verify fails, omit."
- [ ] Process steps numbered where order matters, with `### AWAITING APPROVAL` markers at hand-off points.
- [ ] Failure-modes section (5-10 items) with "audit before delivering" instruction.
- [ ] Self-verification step: how the executor proves the output is correct before handing back.
- [ ] If reference artifacts exist: absolute paths AND enumerated patterns to mirror.
- [ ] If output has a human reader: role + technical baseline + banned jargon stated.
- [ ] Final line tells executor the exact first action.

---

## Required sections in every prompt

Use this skeleton. Skip a section only if genuinely not applicable to the task.

```
# <Title>

<one-paragraph: what gets produced, why, who consumes it>
<one-line discipline rule (karpathy-style: surgical, no scope creep, etc.)>

## Goal
- one verifiable done-condition sentence

## Inputs
- type, absolute path or source, format, size

## Outputs
- absolute path or return shape, schema, size/count target, side effects

## Context the executor needs
- absolute paths to relevant files, links, or short inline excerpts
- stated assumptions

## Tools / skills / models
- /skill-name, library, CLI, MCP tool, model tier
- what to read inside each skill, which helpers to reuse verbatim

## Reference (if applicable)
- absolute paths
- specific patterns/sections/properties to mirror
- "label each output with which pattern it follows"

## Constraints (non-negotiable)
- every applicable hard rule from CLAUDE.md
- verifiable check per constraint (grep, count, lint, test, schema)

## Process (numbered, strict order where it matters)
- numbered steps
- ### AWAITING APPROVAL markers at gates
- parallel vs sequential called out

## Verification (executor runs before delivery)
- specific checks: command to run, expected result
- self-audit against failure modes below

## Failure modes to defend against
- 5-10 items specific to this task type

## Audience (if output has a human reader)
- role, technical baseline, banned jargon, framing rule

---

Start by <exact first action>.
```

---

## Task-type adapters

How the generic rubric specializes. Pull in only what applies.

- **Content generation (docs, slides, posts, emails):** "Outputs" specifies filenames, sizes, structural format (headings, fields, speaker notes). "Verification" includes word count, banned-phrase grep, voice check.
- **Code generation / refactor:** "Outputs" specifies files touched, function signatures, tests added. "Verification" mandates run-the-tests, lint, type-check, manual diff review. "Anti-hallucination" forbids invented APIs, library names, file paths.
- **Research / synthesis:** "Outputs" specifies sources cited with URL + DD-MM-YYYY. "Verification" requires every claim traced to a source. "Anti-hallucination" forbids paraphrase from memory.
- **Automation / scripting / agent orchestration:** "Inputs" includes env, secrets handling, dry-run mode. "Verification" mandates dry-run output reviewed before live run. "Failure modes" includes idempotency, rate limits, partial state.
- **Evaluation / scoring / review:** "Goal" specifies the rubric and scoring scheme. "Outputs" includes per-dimension scores + evidence. "Verification" requires a sanity sample re-scored to confirm consistency.

---

## Anti-patterns (instant deductions)

- "Match the style of X" without enumerating what to match: -5
- "Use the docs" / "pull recent data" without specific URLs or sources: -5
- "Make it good" / "be friendly" / "PM-friendly" without concrete framing rules: -3
- "Cite sources" without specifying format and location: -3
- "Wait for approval" without a hard marker like `### AWAITING APPROVAL`: -3
- "Don't hallucinate" without the "omit if verify fails" rule: -5
- Stating a constraint without a verifiable check: -2 per constraint
- Naming a skill or tool without saying what to read inside or which helper to call: -3
- One-line per output (no schema, no size, no shape): -5
- No self-verification step before delivery: -6

---

## Self-scoring loop

1. Draft the prompt.
2. Score against the rubric. Write the scores in a comment block at the bottom for your own use.
3. If any dimension is below its full weight, fix that section.
4. Re-score. Repeat until total >= 95.
5. Strip the score comment. Deliver.

Do not show the user the rubric or scoring process. Deliver the >95 prompt with a short note on what's in it.

---

## When the user is iterating on an existing prompt

If the user says "improve this prompt" or "review this prompt":
- Score the current version against the rubric.
- Apply diffs to push the score above 95.
- Show: what changed, why, how each change improves output quality. Use a small table.
- Do not dispatch a subagent for review unless the user explicitly asks. This rule replaces that step.
