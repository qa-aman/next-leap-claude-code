# Loop Engineering - teach-me session

**Captured:** 13-09-2026
**Purpose:** Running doc for a staged teach-me session. Items get ticked only when Aman has demonstrated them in his own words.

## Sources (all first-party Anthropic, every URL returned 200 on 13-09-2026, raw `.md` fetched where available)

1. https://code.claude.com/docs/en/best-practices - section "Give Claude a way to verify its work". Verbatim: *"Without a check it can run, 'looks done' is the only signal available, and you become the verification loop: every mistake waits for you to notice it. Give Claude something that produces a pass or fail, and the loop closes on its own."* Also the four gating levels: one prompt, `/goal`, Stop hook, second opinion.
2. https://code.claude.com/docs/en/hooks - exit code 2 semantics and the per-event table. Verbatim: *"Exit code 2 is the way a hook signals 'stop, don't do this.'"* and *"Stderr from a hook that exits 0 goes to the debug log only, never the transcript, and Claude never sees it."*
3. https://code.claude.com/docs/en/goal - `/goal` as a wrapper around a prompt-based Stop hook. Verbatim: *"completion is decided by a fresh model rather than the one doing the work."* and *"Not yet met: Claude keeps working and takes the reason as guidance for the next turn."*
4. https://code.claude.com/docs/en/memory - when a correction should become durable. Verbatim trigger: *"You type the same correction or clarification into chat that you typed last session."*
5. https://www.anthropic.com/engineering/building-effective-agents - the Evaluator-optimizer workflow: *"one LLM call generates a response while another provides evaluation and feedback in a loop."* and agents as *"LLMs using tools based on environmental feedback in a loop."*
6. In-house definition: `02-presentation/q&a.md` Q158. Live examples on this machine: `~/.claude/rules/feedback-driven-lessons.md` (the ledger) and the `auto-capture-corrections` Stop hook.

## Checklist

### Stage 1 - The problem
- [ ] 1.1 State the problem loop engineering solves: the same correction being made by a human, by hand, every run.
- [ ] 1.2 Explain why the problem exists at all: an agent's turn ends and nothing structural carries the correction into the next turn or the next session.
- [ ] 1.3 Name the three branches available and what each one costs: correct by hand each time, rewrite the prompt or rules by hand, or wire the correction back mechanically.

### Stage 2 - The solution
- [ ] 2.1 Describe the loop in one sentence: a harness stops the wrong path and returns the reason to the agent as input for the next iteration.
- [ ] 2.2 Explain the two halves and why both are needed: block (stop the bad action) and feed back (make the reason visible to the agent). Blocking alone is not a loop.
- [ ] 2.3 Explain the Claude Code mechanics from the hooks doc: exit code 2 blocks and its stderr is shown to Claude, `decision: "block"` + `reason`, and why exit code 1 does not do this.
- [ ] 2.4 Distinguish in-turn feedback (PreToolUse, PostToolUse, Stop) from durable feedback (memory, CLAUDE.md, rules, a lessons ledger), and say which one changes behaviour next week.
- [ ] 2.5 Name two edge cases: a hook that only blocks with no reason, and a hook that exits 0 with a warning on stderr (Claude never sees it).

### Stage 3 - The context
- [ ] 3.1 Explain the engineering version: PR review comments fed back into the agent that writes the code, so the agent improves rather than the individual developer.
- [ ] 3.2 Explain what changes downstream: a correction becomes a system property rather than a person's memory, and review load drops over time instead of staying flat.
- [ ] 3.3 Apply it to one workflow of your own and say where the block sits, where the feedback goes, and what makes it durable.

## Stage notes

(filled in as the session runs)

## Accuracy to-do

1. UNVERIFIED: "loop engineering" as an industry term. The Anthropic docs do not use the phrase. It is defined in-house in Q158. Confirm by finding a first-party source that uses it, or keep treating it as workshop vocabulary.
2. VERIFIED 13-09-2026 (raw hooks.md, line 824-828): exit code 2 is a blocking error, the blocking message is the JSON reason or stderr, `PreToolUse` blocks the tool call, `Stop` prevents Claude from stopping.
3. VERIFIED 13-09-2026 (raw hooks.md, line 864): exit code 1 without valid JSON is a non-blocking error and the action proceeds.
4. VERIFIED 13-09-2026 (raw hooks.md, line 822): stderr from a hook that exits 0 goes to the debug log only, Claude never sees it.
