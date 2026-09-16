# Teach Me: Agentic Software Development

**Sources (captured 15-09-2026):**
1. https://www.anthropic.com/engineering/building-effective-agents (definitions, workflow patterns, coding agents)
2. https://code.claude.com/docs/en/best-practices (the working practices, quoted from the raw `.md`)

**Purpose:** running session doc. Items get ticked only when Aman has demonstrated them in his own words or by a correct quiz answer with reasoning.

---

## Checklist

### Stage 1 - The problem
- [ ] 1.1 What "agentic" means versus a chatbot or autocomplete, in one sentence
- [ ] 1.2 The difference between a workflow and an agent (source 1 definitions)
- [ ] 1.3 Why a coding task is unusually well suited to agents (what makes it verifiable)
- [ ] 1.4 The one constraint most practices come from: context fills and performance degrades
- [ ] 1.5 The branches that were available: keep humans writing code with AI review, fixed workflows, or autonomous agents, and the trade-off of each

### Stage 2 - The solution (how you actually work agentically)
- [ ] 2.1 Give the agent a check it can run, and why "looks done" is the only signal otherwise
- [ ] 2.2 Explore, then plan, then code: why separating them avoids solving the wrong problem
- [ ] 2.3 The four ways to gate the stop (prompt, /goal, Stop hook, second-opinion subagent) and what each trades
- [ ] 2.4 Course-correct early, and the two-corrections rule (after two failed fixes, /clear and re-prompt)
- [ ] 2.5 Adversarial review in a fresh context, and why the reviewer must not see the reasoning
- [ ] 2.6 The five common failure patterns and their fixes

### Stage 3 - The context (why it matters beyond one session)
- [ ] 3.1 What changes for the human role: from writer to verifier and specifier
- [ ] 3.2 Why "simplest solution possible" applies to how much autonomy you hand over
- [ ] 3.3 What this changes for a PM specifically: acceptance criteria become the agent's test
- [ ] 3.4 Where human review still stays mandatory (source 1: "human review remains crucial")

---

## Stage 1 - The problem

(filled in as the session runs)

## Stage 2 - The solution

(filled in as the session runs)

## Stage 3 - The context

(filled in as the session runs)

---

## Verified quotes (grepped against raw source, 15-09-2026)

1. "Workflows are systems where LLMs and tools are orchestrated through predefined code paths." (source 1)
2. "Agents, on the other hand, are systems where LLMs dynamically direct their own processes and tool usage, maintaining control over how they accomplish tasks." (source 1)
3. "We recommend finding the simplest solution possible, and only increasing complexity when needed." (source 1)
4. "code solutions are verifiable through automated tests" and "human review remains crucial" (source 1)
5. "Most best practices are based on one constraint: Claude's context window fills up fast, and performance degrades as it fills." (source 2)
6. "Claude stops when the work looks done. Without a check it can run, 'looks done' is the only signal available, and you become the verification loop." (source 2)
7. "If you can't verify it, don't ship it." (source 2)

## Accuracy to-do (unverified)

1. Source 1 lists five workflow patterns (prompt chaining, routing, parallelization, orchestrator-workers, evaluator-optimizer). The list came via a summarising fetch. Names are consistent with the page headings but the exact list was not grepped. Verify before quoting.
