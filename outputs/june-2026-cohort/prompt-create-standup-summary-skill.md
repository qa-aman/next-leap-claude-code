# Create a "standup-digest" Skill (MeetFlow Workshop)

You will create a new Claude Code skill that turns raw daily standup notes into a structured, stakeholder-ready markdown digest. The skill lives in this repo and will be invoked by a PM via the `Skill` tool. Be surgical: scaffold one skill, no scope creep, no extra files, no README.

## Goal

Produce a working skill at `/Users/amanparmar/Documents/AI-PM/Projects/next-leap-claude-code/.claude/skills/standup-digest/SKILL.md` that, when invoked on a `daily-standup-DD-MM-YYYY.md` file, writes a digest to `outputs/standup-digest-DD-MM-YYYY.md` matching the schema in the "Output schema" section below. **Done condition:** running the skill on `/Users/amanparmar/Documents/AI-PM/Projects/next-leap-claude-code/10-meetings/daily-standup-20-03-2026.md` produces a digest file at `outputs/standup-digest-20-03-2026.md` that passes every check in the "Verification" section.

## Inputs

- **Reference skill (already in repo, do not overwrite):** `/Users/amanparmar/Documents/AI-PM/Projects/next-leap-claude-code/.claude/skills/standup-summary/SKILL.md` — read it end-to-end. Mirror its YAML frontmatter shape, workflow numbering style, and owner+date discipline. Do **not** copy its slug or title.
- **Sample standup source:** `/Users/amanparmar/Documents/AI-PM/Projects/next-leap-claude-code/10-meetings/daily-standup-20-03-2026.md` — use only for verification; do not hardcode its contents into the skill.
- **Skill creation standard:** Anthropic Skill Creator pattern — YAML frontmatter (`name`, `description`) + markdown body, body under 500 lines, no README, no extra docs. See `~/.claude/CLAUDE.md` "Skill Creation Standard" section.
- **Project conventions:** `/Users/amanparmar/Documents/AI-PM/Projects/next-leap-claude-code/CLAUDE.md` (workshop date is 17-03-2026, dates DD-MM-YYYY, write outputs to `outputs/`).

## Outputs

Exactly one file, created (not overwritten):

- **Path:** `/Users/amanparmar/Documents/AI-PM/Projects/next-leap-claude-code/.claude/skills/standup-digest/SKILL.md`
- **Format:** YAML frontmatter + markdown body.
- **Size:** 120-300 lines total. If over 300, trim — do not split into subfiles.
- **Frontmatter fields (exact):**
  - `name: standup-digest`
  - `description:` one paragraph, 80-150 words, packed with trigger phrases ("digest the standup", "standup recap", "summarize daily sync", "blockers from standup", "action items from standup notes", "what happened in standup"). Description is the trigger surface; load it with intent phrases, not features.
- **Body must contain these H2 sections, in order:** `## When to use`, `## Inputs`, `## Workflow` (numbered steps), `## Output schema`, `## Output template`, `## Rules`, `## Failure modes`.

## Output schema (the digest the skill produces)

The skill, when run, must write `outputs/standup-digest-DD-MM-YYYY.md` containing:

1. `# Standup Digest - DD-MM-YYYY` (date from the source filename, not today)
2. `## TL;DR` — 3 bullets max, each ≤ 20 words, stakeholder-readable
3. `## Per-person updates` — one subsection per attendee with `Yesterday / Today / Blockers` bullets
4. `## Decisions` — bulleted list, empty section allowed but heading must be present
5. `## Risks` — bulleted list, empty allowed
6. `## Action items` — table with columns `Action | Owner | Due (DD-MM-YYYY) | Source`. Every row must have an owner (use `unassigned` if missing) and a due date (use `not stated` if missing). Never invent.
7. `## Source` — single line: `Source: <absolute path to standup file>`

## Constraints (non-negotiable, verifiable)

- **Dates DD-MM-YYYY everywhere.** Verify with: `grep -E '[0-9]{4}-[0-9]{2}-[0-9]{2}' .claude/skills/standup-digest/SKILL.md` returns no matches except ISO examples explicitly inside code fences labeled "wrong format" (none expected).
- **No emojis.** Verify: `grep -P '[\x{1F300}-\x{1FAFF}\x{2600}-\x{27BF}]' .claude/skills/standup-digest/SKILL.md` returns nothing.
- **No em dashes.** Verify: `grep '—' .claude/skills/standup-digest/SKILL.md` returns nothing. Use commas or hyphens.
- **No README, no auxiliary files.** Verify: `ls .claude/skills/standup-digest/` returns exactly `SKILL.md`.
- **Slug must be `standup-digest`** (different from existing `standup-summary`). Verify: `grep '^name: standup-digest' .claude/skills/standup-digest/SKILL.md` returns one line.
- **Frontmatter description is one paragraph, not a list.** Verify: between `description:` and the closing `---`, no `\n-` or numbered list lines.
- **Body ≤ 300 lines.** Verify: `wc -l .claude/skills/standup-digest/SKILL.md` shows ≤ 300.
- **Owner + due date mandatory in action-item rules.** Verify: the strings `owner` and `due` (or `Due`) both appear in the `## Rules` or `## Workflow` sections.
- **Outputs always to `outputs/standup-digest-DD-MM-YYYY.md`.** Verify: this exact filename pattern appears in `## Output schema` or `## Workflow`.
- **No invented metrics, no fabricated quotes.** The skill body must include an explicit "omit if not in source, do not fabricate" line.

## Tools / skills / models

- Use `Read` to load the reference skill and sample standup. Use `Write` to create `SKILL.md`. Use `Bash` only for the verification grep/wc commands at the end.
- Do **not** invoke the `skill-creator` skill, the `init_skill.py` script, or any subagent. Write `SKILL.md` directly.
- Do **not** read or modify `.claude/skills/standup-summary/` beyond the one initial read.
- Do **not** create `references/`, `scripts/`, or `assets/` subdirectories.

## Reference patterns to mirror from `standup-summary/SKILL.md`

Enumerated, not vague:

1. Frontmatter shape: `name:` then `description: |` block, closed with `---`.
2. The workflow's discipline around tagging every action item with both owner and resolved DD-MM-YYYY due date (including "by EOD" → resolve against source-file date).
3. The pattern of taking the digest date from the source filename, not today.
4. The closing instruction: "print a one-line confirmation with the output path, do not restate the summary in chat."

Do **not** mirror: the title, the slug, the exact section headings (this skill uses a different output schema with TL;DR + Risks sections that the reference does not have).

## Process (strict order)

1. Read the reference skill in full.
2. Read the sample standup in full (for mental model only, do not quote it inside the skill).
3. Draft `SKILL.md` in memory, applying every rule in "Constraints" and the schema in "Output schema".
4. Run the self-audit in "Verification" against your draft before writing.
5. Write the file with `Write` to the exact path above.
6. Run the verification commands listed below. If any fails, fix and re-write. Do not deliver a failing skill.
7. Print one line: `Created: .claude/skills/standup-digest/SKILL.md (N lines)`.

### AWAITING APPROVAL

Stop after step 7. Do **not** run the skill on the sample standup. Do **not** generate a digest file. Do **not** edit `MEMORY.md`, `CLAUDE.md`, or anything outside `.claude/skills/standup-digest/`.

## Verification (run before delivering)

Run each command from the repo root `/Users/amanparmar/Documents/AI-PM/Projects/next-leap-claude-code`. Every command must return the expected result.

| # | Command | Expected |
|---|---------|----------|
| 1 | `ls .claude/skills/standup-digest/` | exactly `SKILL.md` |
| 2 | `wc -l .claude/skills/standup-digest/SKILL.md` | between 120 and 300 |
| 3 | `grep -c '^name: standup-digest$' .claude/skills/standup-digest/SKILL.md` | `1` |
| 4 | `grep -c '^description:' .claude/skills/standup-digest/SKILL.md` | `1` |
| 5 | `grep -E '[0-9]{4}-[0-9]{2}-[0-9]{2}' .claude/skills/standup-digest/SKILL.md` | no matches |
| 6 | `grep '—' .claude/skills/standup-digest/SKILL.md` | no matches |
| 7 | `grep -c '## When to use\|## Inputs\|## Workflow\|## Output schema\|## Output template\|## Rules\|## Failure modes' .claude/skills/standup-digest/SKILL.md` | `7` |
| 8 | `grep -c 'standup-digest-DD-MM-YYYY.md\|outputs/standup-digest-' .claude/skills/standup-digest/SKILL.md` | at least `1` |
| 9 | `grep -ci 'owner' .claude/skills/standup-digest/SKILL.md` | at least `2` |
| 10 | `grep -ci 'do not fabricate\|omit' .claude/skills/standup-digest/SKILL.md` | at least `1` |

If any row fails, fix the file and re-run all ten before delivery.

## Failure modes to defend against

1. Copying the `standup-summary` slug or title and silently overwriting the existing skill. Defense: explicit `ls` check before `Write`; the path must not exist before step 5.
2. Putting trigger phrases in the body instead of the `description` frontmatter. Defense: description carries all trigger phrases; body documents behavior.
3. Using today's real date instead of the source-file date in examples. Defense: every example date in the skill body must be `DD-MM-YYYY` referenced from a hypothetical source filename, not the system clock.
4. Inventing attendee names, action items, or quotes inside the skill examples. Defense: examples use placeholder names like `<PM>`, `<Engineer 1>`, never real names from the sample standup.
5. Bloating with `references/` or `scripts/` directories the rubric explicitly forbids. Defense: verification row 1 enforces single-file skill.
6. Leaking em dashes, emojis, or ISO dates from training-data instincts. Defense: verification rows 5 and 6.
7. Describing what the skill does in the body without telling the executor *what to write to disk*. Defense: `## Output schema` and `## Output template` are both mandatory and distinct.
8. Drifting past 300 lines because the description got verbose. Defense: cap description at 150 words; verification row 2.
9. Forgetting the one-line confirmation rule, so future runs spam chat with the full digest. Defense: include the confirmation line in `## Workflow`.
10. Action-item tables without dates, the exact failure mode the reference skill was built to prevent. Defense: schema requires `Due` column with `not stated` fallback; verification row 9.

## Audience

The eventual consumer of the digest (not this skill file) is a busy stakeholder, typically an EM or skip-level. They scan in 60 seconds. Banned in digest output: hype words, hedging ("seems like", "kind of"), and any sentence over 25 words. The `SKILL.md` file itself is consumed by Claude, not a human reader, so keep its prose terse and instructional.

---

Start by reading `/Users/amanparmar/Documents/AI-PM/Projects/next-leap-claude-code/.claude/skills/standup-summary/SKILL.md` in full.
