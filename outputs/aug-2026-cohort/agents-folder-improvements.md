# `.claude/agents/` - Improvement Report

**Date:** 02-08-2026
**Scope:** all 12 agent definitions in `.claude/agents/` (1,176 lines total)
**Method:** read every file's frontmatter and body, compared the declared `tools:` list against the tool list the runtime actually reports for each agent, and checked each agent's output path against the project's cohort-folder convention.
**Nothing was modified.** This report is suggestions only.

---

## Scope

| File | Lines | Model | Memory |
|---|---|---|---|
| `aman.md` | 88 | sonnet | none |
| `churn-diagnoser.md` | 65 | sonnet | none |
| `churn-pattern-analyst.md` | 200 | sonnet | project |
| `code-improver-recent.md` | 81 | sonnet | none |
| `code-improver.md` | 75 | sonnet | none |
| `competitor-intel-analyst.md` | 212 | sonnet | project |
| `competitor-snapshot.md` | 45 | sonnet | none |
| `feedback-triangulator.md` | 64 | sonnet | none |
| `interview-insight-synthesizer.md` | 76 | sonnet | none |
| `pm-request-router.md` | 40 | sonnet | none |
| `prd-drafter.md` | 65 | sonnet | none |
| `senior-code-reviewer.md` | 165 | sonnet | project |

---

## Summary

The folder is in good shape on the things that are hardest to get right: every agent has a real `description` with worked `<example>` blocks, every one cites sources, and the PM agents are grounded in actual repo files. The problems are in the wiring, not the writing.

Three findings are worth acting on before the next cohort. First, nine agents write into `outputs/` root, which contradicts the cohort-folder convention this repo follows, so every generated artifact lands in the wrong place. Second, two agents declare themselves read-only but silently receive `Write` and `Edit` at runtime because `memory: project` auto-enables them, so the guarantee in their description is not real. Third, there are two pairs of agents whose trigger phrases overlap enough that dispatch becomes a coin flip.

The single highest-value fix is the output path, because it affects every artifact these agents produce.

---

## Suggestions

### 1. Nine agents write to `outputs/` root, not the cohort folder [Best practices] [Major]

**Where:**
1. `churn-diagnoser.md:27` - `outputs/churn-diagnosis.md`
2. `competitor-snapshot.md:17` - `outputs/competitor-snapshot-{name}.md`
3. `feedback-triangulator.md:16,37` - `outputs/triangulated-feedback.md`
4. `interview-insight-synthesizer.md:13,44` - `outputs/interview-synthesis.md`
5. `prd-drafter.md:25` - `outputs/prd-{feature-name}.md`
6. `code-improver.md:19,39` - `./outputs/code-improvements-<slug>.md`
7. `senior-code-reviewer.md:28,42` - `./outputs/code-review-<slug>.md`
8. `competitor-intel-analyst.md:51` - "Write all generated artifacts to `outputs/`"
9. `aman.md:15,81` - "Save generated artifacts to `outputs/`"

**Current** (`prd-drafter.md:25`):

```
Save to `outputs/prd-{feature-name}.md` (kebab-case the feature name, no date in the filename).
```

**Suggested:**

```
Save to `outputs/<current-month>-cohort/prd-{feature-name}.md` (kebab-case the feature
name, no date in the filename). Never write directly into `outputs/` root. If you cannot
determine the current cohort folder, list `outputs/` and use the most recent one.
```

**Why:** The established convention for this repo is that generated files go under the current month's cohort folder, for example `outputs/aug-2026-cohort/`. Right now every one of these agents drops its artifact one level too high, so cohort folders stay empty while `outputs/` root fills up. One line in each agent fixes it permanently.

---

### 2. Two "read-only" agents silently get `Write` and `Edit` [Best practices] [Major]

**Where:** `churn-pattern-analyst.md:4,14` and `competitor-intel-analyst.md:4`

**Current** (`churn-pattern-analyst.md`):

```yaml
tools: ListMcpResourcesTool, Read, ReadMcpResourceTool, TaskCreate, TaskGet, TaskList, TaskStop, TaskUpdate, WebFetch, WebSearch
memory: project
```

and at line 14 of the body:

```
- You are STRICTLY READ-ONLY. Never edit, create, move, or delete any file in the feedback source.
```

**Suggested:**

```yaml
tools: Read, Glob, Grep, Write
disallowedTools: Edit, NotebookEdit
memory: project
```

and reword line 14 to say the agent may write only to its report path and its own memory directory, never to a source file.

**Why:** `memory: project` auto-enables `Read`, `Write`, and `Edit` on top of whatever `tools:` declares. The runtime tool list for `churn-pattern-analyst` is in fact `... WebFetch, WebSearch, Write, Edit`, so the "STRICTLY READ-ONLY" line in its own body is not enforced by anything. Either drop the claim or add `disallowedTools: Edit` so the promise matches the wiring. `competitor-intel-analyst` has the same gap. This is the same class of problem as a checklist item that nothing verifies.

---

### 3. Two pairs of agents have colliding triggers [Best practices] [Major]

**Where:** `code-improver.md:3` against `code-improver-recent.md:3`, and `churn-diagnoser.md:3` against `churn-pattern-analyst.md:3`

**Current:** `code-improver` triggers on "improve this code / suggest improvements / best practices for this file". `code-improver-recent` triggers on "improve my recent changes / scan my latest work". A user who says "suggest improvements on what I changed" matches both. Separately, `churn-diagnoser` triggers on "why are users leaving / how do we improve stickiness" and `churn-pattern-analyst` triggers on "why users are leaving / what is driving churn". Those are the same sentence.

**Suggested:** Make the discriminator the first clause of each description, not a note buried at the end.

```
code-improver:        "...when the user names A SPECIFIC FILE OR DIRECTORY and wants a
                       written report file."
code-improver-recent: "...when the user points at RECENT CHANGES (the diff or last few
                       commits) and wants the answer inline, no file written."

churn-diagnoser:      "...when the user wants a SHORT DIAGNOSIS: top 3 drivers plus quick
                       wins and structural fixes."
churn-pattern-analyst:"...when the user wants an EXHAUSTIVE RANKED EXTRACT: every driver
                       with verbatim quotes, frequency counts, and severity."
```

**Why:** When two descriptions cover the same trigger phrase, the router picks one at random and the user gets a different shape of answer each time they ask the same question. Naming the discriminator up front (scope and output shape, not topic) makes the choice deterministic. The alternative, and it is a fair call, is to merge each pair into one agent with a scope parameter.

---

### 4. Roughly 130 lines of generic memory boilerplate is copy-pasted into 2 agents [Readability] [Major]

**Where:** `churn-pattern-analyst.md:66-194` and `competitor-intel-analyst.md:66-183`

**Current:** `churn-pattern-analyst.md` is 200 lines, of which lines 66 to 194 are a generic explanation of the memory system: what a `project` memory type is, how `MEMORY.md` is an index and not a memory, when to use tasks instead of memory. `competitor-intel-analyst.md` carries the same block. Neither block says anything specific to churn analysis or competitor research.

**Suggested:** Replace the block in each file with the 5 to 8 lines that are actually agent-specific, for example:

```
## Memory

Before starting, read your memory. After finishing, record only generalizable
heuristics, never one-off facts: which feedback phrasings reliably signal churn
intent, which severity calls you got wrong, which source files are the richest.
One fact per file, plus a one-line pointer in MEMORY.md.
```

**Why:** Two thirds of these two files is boilerplate the agent already receives from the harness when `memory:` is set. It buries the 60 lines that carry the actual job, it costs tokens on every dispatch, and when the memory spec changes there are now three copies to update. Keep only what is specific to this agent's learning.

---

### 5. `churn-pattern-analyst` cannot scan a directory [Best practices] [Major]

**Where:** `churn-pattern-analyst.md:4`

**Current:**

```yaml
tools: ListMcpResourcesTool, Read, ReadMcpResourceTool, TaskCreate, TaskGet, TaskList, TaskStop, TaskUpdate, WebFetch, WebSearch
```

**Suggested:**

```yaml
tools: Read, Glob, Grep, Write
```

**Why:** Its own description says to point it at "a feedback file **or directory**", and its first worked example is `"Read 06-user-feedback/ and tell me the top reasons Pro users are churning"`. With no `Glob` and no `Grep` it cannot enumerate a directory, so it can only work if the caller names each file. Meanwhile it carries five `Task*` tools, two MCP resource tools, and web search that its job never uses. `competitor-intel-analyst.md:4` has the same `Task*` block and also no `Glob`. These read like scaffolding left in from generation rather than deliberate choices.

---

### 6. Every agent is pinned to `sonnet`, including the pure switchboard [Performance] [Minor]

**Where:** all 12 files, `model: sonnet`

**Suggested:** Move the cheap, mechanical agents to `haiku`:

```yaml
# pm-request-router.md, competitor-snapshot.md
model: haiku
```

**Why:** `pm-request-router` does one thing: read a sentence, pick one of four labels, dispatch. `competitor-snapshot` is a 45-line agent that reads one doc and fills a fixed template. Neither needs Sonnet-level reasoning, and routing them to Haiku cuts the cost of the most frequently dispatched agent in the folder. Keep Sonnet for the analysts and reviewers, where the judgement is real.

---

### 7. No agent sets `maxTurns`, including the ones with `Bash` [Best practices] [Minor]

**Where:** `code-improver.md:4`, `code-improver-recent.md:4`, `senior-code-reviewer.md:4`, `aman.md:4`

**Suggested:** Add a ceiling to the agents that can loop on shell commands:

```yaml
maxTurns: 40
```

**Why:** These four hold `Bash` and scan an open-ended file set. A bounded turn count stops a runaway scan from burning a long tail of tokens on a repo that turns out to be larger than expected. It is a cheap backstop, not a constraint you will hit in normal use.

---

### 8. Frontmatter style drifts across the folder [Readability] [Minor]

**Where:** `name:` is quoted in 10 files (for example `churn-diagnoser.md:2`) and unquoted in 2 (`aman.md:2`, `code-improver-recent.md:2`). Colours collide: blue appears 3 times, green 3 times, yellow 2 times, and `aman.md` has no colour at all.

**Suggested:** Pick one, quoted or unquoted, and apply it to all 12. Give each agent a distinct colour, or drop `color` from every file rather than having some with and some without.

**Why:** Cosmetic, but this folder is a teaching artifact for the cohort. Twelve files that look like they came from one hand read better than twelve that look assembled. Colour collisions also make the task list harder to scan when several agents run at once.

---

### 9. `aman.md` overlaps `pm-request-router` [Best practices] [Minor]

**Where:** `aman.md:9-15` against `pm-request-router.md:10-19`

**Current:** `aman.md` reads the request, picks the best matching PM skill from a routing table, then produces the artifact end to end. `pm-request-router` classifies the request into one of four labels and dispatches a specialist, never answering itself.

**Suggested:** Say in each description which one owns which case. The natural split: `pm-request-router` handles a vague request where the deliverable is unknown, `aman` handles a named deliverable where the skill is obvious. Add one line to `aman.md` telling it to hand off to `pm-request-router` when it cannot pick a skill with confidence.

**Why:** Both are entry points for "help me with this PM thing", and `aman` has the broader tool set so it will usually win. That is probably the right outcome, but it should be a stated decision rather than an accident of which description matched first.

---

## Not flagged

1. The `<example>` blocks in every description. They are well written and are the main reason dispatch works at all, so leave them.
2. The citation discipline across the PM agents (cite the source file for every number and quote). It is consistent and correct.
3. `feedback-triangulator` holding the `Agent` tool. It fans out three workers deliberately, so that is the right wiring.
4. The "no date in the filename, overwrite if it exists" convention. It is applied consistently and matches how this repo works.
5. `senior-code-reviewer` at 165 lines. It is long, but unlike the two flagged above the length is job-specific content, not boilerplate.

---

## Suggested order of work

1. Finding 1 (output paths) - touches 9 files, one line each, biggest practical payoff.
2. Finding 2 (read-only claims) - 2 files, closes a promise that is not currently enforced.
3. Finding 3 (trigger collisions) - 4 descriptions, makes dispatch deterministic.
4. Findings 4 and 5 (boilerplate and missing `Glob`) - 2 files, can be done in the same pass.
5. Findings 6 to 9 - cleanup, do when convenient.
