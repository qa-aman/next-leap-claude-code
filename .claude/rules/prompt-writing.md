---
paths:
  - "outputs/*prompt*.md"
  - "outputs/**/prompt*.md"
  - "prompts/**"
---

# Prompt-Writing Rules

Apply whenever the user asks to "create a prompt", "write a prompt", "draft a prompt", "review a prompt", or generate instructions for a fresh Claude / Claude Code session to execute. Task type does not matter: code, data, research, automation, evaluation, content, debugging, agent orchestration.

**Delivery is chat-only. Output the finished prompt directly in the conversation, inside one fenced code block so it is copy-pasteable. Do not write a file. Do not create anything in `outputs/` or `prompts/`. No subagent for review. This rule replaces that step.**

**Always copy the finished prompt to the clipboard automatically as the last step, without being asked.** After printing the prompt in chat, pipe the exact same prompt text to `pbcopy` using a quoted heredoc so nothing needs escaping, then confirm in one line that it was copied. Use this pattern (the heredoc delimiter `'PROMPTEOF'` is quoted so `$`, backticks, and quotes inside the prompt are copied literally):

```
cat << 'PROMPTEOF' | pbcopy
<the exact prompt text, verbatim>
PROMPTEOF
echo "prompt copied to clipboard ($(pbpaste | wc -c | tr -d ' ') chars)"
```

The clipboard copy must be byte-identical to what you printed in chat. Do this on every prompt you deliver, including iterations, so the user never has to ask separately.

Target quality: **>95/100** against the rubric below. Self-score silently before delivering. Iterate until the score clears 95, then deliver the prompt in the chat with a 2-3 line note on what it contains. Do not show the user the rubric or the scoring process.

---

## Ground every prompt in Anthropic's prompting guidance

Source: Anthropic "Prompting best practices" (platform.claude.com), current Claude models (Opus 4.x, Sonnet 4.6, Fable 5). These are not optional extras. They map directly to rubric dimensions.

1. **Be clear and direct.** Write for "a brilliant new employee who lacks context on your norms." State the exact output, format, and constraints. If you want above-and-baseline effort, say so explicitly ("go beyond the basics", "include as many relevant features as possible"); the model will not infer it from a vague ask.
2. **Give the motivation, not just the rule.** Explain *why* a constraint exists. "Never use ellipses, because a text-to-speech engine reads this aloud and cannot pronounce them" outperforms "never use ellipses." The model generalizes correctly from the reason.
3. **Use 3-5 examples for any non-trivial format, tone, or structure.** Examples are the most reliable steering tool. Make them relevant (mirror the real case), diverse (cover edge cases so the model does not latch onto an accidental pattern), and structured (wrap each in `<example>` tags, the set in `<examples>`).
4. **Structure the prompt with XML tags.** Separate instructions, context, inputs, and examples with descriptive tags (`<instructions>`, `<context>`, `<input>`, `<example>`). Consistent tags reduce misinterpretation. Nest when content is hierarchical.
5. **Give the executor a role.** One role sentence at the top ("You are a senior PM owning the AI Intelligence pillar...") focuses tone and judgment for the whole prompt.
6. **Long inputs go at the top, the ask goes at the bottom.** For 20k+ token inputs, place documents/data first and the instruction last; this can lift quality up to ~30%. Wrap each doc in `<document>` with `<source>` and `<document_content>`. For long-doc tasks, instruct the executor to pull relevant quotes into `<quotes>` tags first, then act.
7. **Say what to do, not what not to do.** "Write in flowing prose paragraphs" beats "do not use markdown." Pair a positive instruction with an XML format indicator when format matters.
8. **Calibrate force. Do not over-prompt.** Current models follow instructions precisely and over-trigger on shouting. Use "Use this tool when X", not "CRITICAL: you MUST always use this tool." Reserve emphatic language for genuinely load-bearing rules. Over-prompting causes overeagerness, excessive thinking, and unwanted subagent spawning.
9. **Be explicit when you want action vs. recommendation.** "Change this function" makes the executor act; "can you suggest changes" makes it only advise. Match the verb to the intent.
10. **Steer thinking by goal, not by prescribed steps.** "Think thoroughly, then verify your answer against [criteria] before finishing" beats a hand-written step list; the model's own reasoning often exceeds a prescribed plan. When thinking is off, ask it to reason in `<thinking>` tags and answer in `<answer>` tags. Note: with thinking off, current Opus is sensitive to the word "think"; prefer "consider", "evaluate", "reason through".
11. **Demand investigation before claims (anti-hallucination).** "Never speculate about code or files you have not opened. Read the referenced file before answering." This is the single highest-leverage guard for code and research prompts.
12. **Constrain overengineering.** Add "only make changes directly requested or clearly necessary; do not add abstractions, defensive code, or files beyond the task" when the prompt touches code.
13. **Do not use prefill.** Prefilled assistant turns are unsupported on current models. For structured output, instruct the schema directly (or name Structured Outputs / tool enums), do not fake a prefix.
14. **For multi-window or long-horizon tasks,** tell the executor to track state in structured files (JSON for status, freeform for progress notes), use git for checkpoints, and keep incremental progress rather than attempting everything at once.

---

## The Rubric (100 points)

| # | Dimension | Weight | What "good" looks like |
|---|---|---|---|
| 1 | Goal clarity | 12 | The done condition is one verifiable sentence. The executor knows when to stop. Effort level stated explicitly if above baseline. |
| 2 | Context sufficiency | 10 | Background the executor lacks is supplied inline or via absolute paths, with the motivation behind key constraints. Assumptions stated. No implicit knowledge. |
| 3 | Inputs and outputs | 10 | Inputs: types, paths, formats, size. Outputs: return shape or chat format, schema, expected size/count, side effects. Long inputs placed at top, the ask at the bottom. |
| 4 | Constraints | 10 | Every hard rule from `~/.claude/CLAUDE.md` and project `CLAUDE.md` that applies is restated, phrased as what TO do. Each has a verifiable check where possible (grep, count, lint, test, schema validate). |
| 5 | Tool / skill / model selection | 8 | Exact tool names, skill slugs, library names, model tier. Says which to use when, calibrated ("use when X"), not shouted. Forbids rewriting what exists. |
| 6 | Anti-hallucination guards | 10 | "Investigate before claiming." "Omit, do not fabricate." External facts cite source URL + DD-MM-YYYY fetch date. No guessing APIs, paths, or schemas. |
| 7 | Process discipline | 8 | Steps numbered only where order matters. Approval gates marked `### AWAITING APPROVAL`. Parallel-vs-sequential rules explicit. Thinking steered by goal, not over-prescribed. Stop conditions defined. |
| 8 | Failure modes | 8 | 5+ realistic failure modes for this task type, each with a defense. Pre-delivery self-audit instruction. |
| 9 | Reference fidelity | 6 | If references exist, exact paths AND specific patterns/sections/properties to mirror, ideally as `<example>` blocks. Vague "match style" banned. Skip cleanly if no reference. |
| 10 | Audience calibration | 6 | Reader/consumer named: role, technical baseline, banned jargon, framing rule. Skip if executor-only output. |
| 11 | Structure and self-containment | 6 | XML tags separate instructions/context/input/examples. Role set at top. Fresh session executes end-to-end with absolute paths and verified-existing files. No back-and-forth. |
| 12 | Self-verification | 6 | Executor checks own work before delivery: grep, count, dry run, test run, schema validate, lint, manual diff. At least one check per major output. |

Total: 100.

---

## Mandatory checklist before delivering any prompt

- [ ] Role sentence at the top. Goal stated as one verifiable done-condition. Effort level explicit if above baseline.
- [ ] Instructions, context, inputs, and examples separated with XML tags.
- [ ] Inputs listed with paths/types/formats; long inputs placed before the ask. Outputs listed with shape/schema/size.
- [ ] All applicable hard rules from global + project CLAUDE.md restated inline, phrased as what TO do. Do not assume the executor loads them.
- [ ] At least one verifiable check per constraint (grep, count, file-exists, schema, test).
- [ ] Tools/skills/models named exactly and calibrated ("use when X", not "you MUST"). For skills, name what to read inside and which helpers to reuse verbatim.
- [ ] 3-5 `<example>` blocks for any non-trivial format, tone, or structure.
- [ ] External sources listed as specific URLs (not "the docs"). Anti-hallucination clause: "investigate before claiming; if fetch/verify fails, omit."
- [ ] Process steps numbered only where order matters, with `### AWAITING APPROVAL` markers at hand-off points. No over-prompting / shouting.
- [ ] Failure-modes section (5-10 items) with "audit before delivering" instruction.
- [ ] Self-verification step: how the executor proves the output is correct before handing back.
- [ ] If reference artifacts exist: absolute paths AND enumerated patterns to mirror.
- [ ] If output has a human reader: role + technical baseline + banned jargon stated.
- [ ] Final line tells the executor the exact first action.

---

## Required sections in every prompt

Use this skeleton. Skip a section only if genuinely not applicable. Wrap variable content in XML tags so the executor parses it unambiguously.

```
You are <role: who the executor is and what they own>.

<task>
one-paragraph: what gets produced, why, who consumes it.
one-line discipline rule (surgical, no scope creep, minimal solution).
</task>

## Goal
- one verifiable done-condition sentence
- effort level if above baseline ("go beyond the basics", etc.)

## Inputs
<inputs>
- type, absolute path or source, format, size
- (place any long document content here, at the top, wrapped in <document> tags)
</inputs>

## Outputs
- return shape or chat-output format, schema, size/count target, side effects

## Context the executor needs
<context>
- absolute paths to relevant files, links, or short inline excerpts
- the motivation behind the key constraints (the why, not just the what)
- stated assumptions
</context>

## Tools / skills / models
- /skill-name, library, CLI, MCP tool, model tier; "use X when ..." (calibrated, not shouted)
- what to read inside each skill, which helpers to reuse verbatim

## Reference (if applicable)
<examples>
  <example> absolute path + the specific pattern/section/property to mirror </example>
  (3-5 examples; "label each output with which pattern it follows")
</examples>

## Constraints (non-negotiable)
- every applicable hard rule from CLAUDE.md, phrased as what TO do
- verifiable check per constraint (grep, count, lint, test, schema)

## Process (numbered only where order matters)
- steps; ### AWAITING APPROVAL markers at gates
- parallel vs sequential called out
- "think thoroughly, then verify against [criteria]" rather than a rigid step list

## Verification (executor runs before delivery)
- specific checks: command to run, expected result
- self-audit against the failure modes below

## Failure modes to defend against
- 5-10 items specific to this task type

## Audience (if output has a human reader)
- role, technical baseline, banned jargon, framing rule

Start by <exact first action>.
```

---

## Task-type adapters

How the generic rubric specializes. Pull in only what applies.

- **Content generation (docs, slides, posts, emails):** "Outputs" specifies sizes and structural format (headings, fields, speaker notes). "Verification" includes word count, banned-phrase grep, voice check. Show 1-2 `<example>` blocks of the target voice.
- **Code generation / refactor:** "Outputs" specifies files touched, function signatures, tests added. "Verification" mandates run-the-tests, lint, type-check, manual diff. Add "investigate before claiming" and the overengineering constraint. "Anti-hallucination" forbids invented APIs, library names, file paths.
- **Research / synthesis:** Place source documents at the top, the question last. Instruct quote-extraction into `<quotes>` tags before synthesis. "Outputs" cites sources with URL + DD-MM-YYYY. "Verification" requires every claim traced to a source. Forbid paraphrase from memory.
- **Automation / scripting / agent orchestration:** "Inputs" includes env, secrets handling, dry-run mode. "Verification" mandates dry-run output reviewed before live run. Add subagent-scope guidance ("use subagents only for parallel/isolated workstreams"). "Failure modes" includes idempotency, rate limits, partial state.
- **Evaluation / scoring / review:** "Goal" specifies the rubric and scoring scheme. "Outputs" includes per-dimension scores + evidence. "Verification" requires a sanity sample re-scored to confirm consistency.

---

## Anti-patterns (instant deductions)

- "Match the style of X" without enumerating what to match: -5
- "Use the docs" / "pull recent data" without specific URLs or sources: -5
- Stating a constraint as "do not X" where "do Y" is clearer: -3
- "Make it good" / "be friendly" / "PM-friendly" without concrete framing rules: -3
- Over-prompting: "CRITICAL", "you MUST always", all-caps shouting on non-load-bearing rules: -4
- Recommending prefill / a forced assistant prefix (unsupported on current models): -5
- "Cite sources" without specifying format and location: -3
- "Wait for approval" without a hard marker like `### AWAITING APPROVAL`: -3
- "Don't hallucinate" without "investigate before claiming" and "omit if verify fails": -5
- No `<example>` blocks on a format/tone/structure task: -4
- No XML tags separating instructions from inputs on a mixed-content prompt: -3
- Stating a constraint without a verifiable check: -2 per constraint
- Naming a skill or tool without saying what to read inside or which helper to call: -3
- One-line per output (no schema, no size, no shape): -5
- No self-verification step before delivery: -6

---

## Self-scoring loop

1. Draft the prompt.
2. Score against the rubric silently.
3. If any dimension is below its full weight, fix that section.
4. Re-score. Repeat until total >= 95.
5. Deliver the prompt in the chat inside one fenced code block, copy-pasteable. No file written.
6. Copy the same prompt to the clipboard via `pbcopy` (quoted heredoc) and confirm in one line.

Deliver the >95 prompt with a short note (2-3 lines) on what is in it. Do not show the user the rubric or scoring process.

---

## When the user is iterating on an existing prompt

If the user says "improve this prompt" or "review this prompt":
- Score the current version against the rubric.
- Apply diffs to push the score above 95.
- Deliver the improved prompt in the chat, copy it to the clipboard via `pbcopy`, then show what changed and why in a small table. Use it to highlight which rubric dimension each change lifts.
- Do not write a file. Do not dispatch a subagent for review unless the user explicitly asks. This rule replaces that step.
