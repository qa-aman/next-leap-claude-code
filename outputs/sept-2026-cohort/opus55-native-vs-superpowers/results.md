# Opus 5.5: native loop vs Superpowers (results, 26-09-2026)

**Verdict:** the native loop gave the better architecture and plan in all 4 blind head-to-head judgements. It won because its interview found the PM's constraints. Superpowers wrote more executable task lists, but for a product that missed privacy, budget and edit-history requirements.

## Setup

- Same app idea and the same simulated PM for both arms. See `brief.md`: 16 hidden requirements (R1-R16), revealed only when asked.
- Builder: Claude Code 2.1.283 on `claude-opus-5-5`, default effort. User settings skipped (no personal plugins, hooks or CLAUDE.md).
- **Native arm:** the official interview prompt from [best practices](https://code.claude.com/docs/en/best-practices), then phases and checks, then a fresh session writes PLAN.md.
- **Superpowers arm:** superpowers 6.4.1 only. "Use your superpowers skills to brainstorm this with me and then write the implementation plan."
- 2 runs per arm. Script: `run_experiment.py`. Transcripts and documents: `runs/`.
- Blind judge: Opus 5.5, high effort, with skill names redacted (`judge.py`).
  - 2 absolute scorings per run.
  - 4 pairwise comparisons, each pair in both orders.
  - Raw output: `judgements/`.

## Results

| | Native (avg of 2 runs) | Superpowers (avg of 2 runs) |
| --- | --- | --- |
| Requirements captured (of 16) | **15** | 9.25 |
| C2 Architecture fits constraints (1-5) | **4.0** | 2.5 |
| C3 Plan executability | 5.0 | 4.75 |
| C4 Verification | 5.0 | 5.0 |
| C5 Scope discipline | 3.5 | 3.5 |
| C6 Risk handling | **4.0** | 3.0 |
| C7 Readable by a non-technical PM | **3.5** | 2.5 |
| Pairwise wins | **4 of 4, "clear"** | 0 of 4 |
| Q&A rounds | 16-28 | 20-24 |
| Time | 16-19 min | 24 min to over 30 min |
| API-list cost per run | $37-67 | $105 (run 1; run 2 not fully logged) |

Both judge passes gave the same requirement count for every run. Three of the judge's verbatim quotes were checked against the documents with `grep`, and all three were found.

## Why native won: it asked about the hard parts

- The native prompt says "dig into the hard parts I might not have considered". Its first turn held about 10 questions, for example:
  - Who is "I" in "I'll send the deck"?
  - Should the meeting date be a field? "Notes are often pasted days later, and 'next Tuesday' then resolves to the wrong week."
- Superpowers asked one question at a time and moved to design approval after about 4 rounds. It never asked about privacy, budget, languages, note length or edit history.
- What both Superpowers runs missed:
  - **30-day note deletion (R7).** Notes were kept forever. One spec says "Nothing is hard-deleted".
  - **$20 budget (R12).** No cost estimate. One run defaulted to Opus for extraction and judging.
  - **Hinglish (R3).**
  - **Non-technical builder (R13).** One run is "host-agnostic" and needs Docker.
- Superpowers run 2 also capped notes at `MAX_NOTES_CHARS = 50_000`, about 8,000 words. The PM's transcripts run to 15,000 words.

## Where Superpowers was better

- **Task-level detail.** Each of its 16 tasks has test-first steps, exact commands, an expected FAIL then PASS, and a commit. The judge called one plan "fully written TDD code... very executable, but it builds the wrong product".
- **Accuracy design.** The LLM copies the owner text, and code matches it against the roster. Both arms landed on this idea.

## Weaknesses in native too

- Over-scoping. Native run 2 added draft locks, a stats page and a minimap, and the judge scored scope 3.
- Unchecked hosting limits. Cloudflare free-plan limits were not verified.
- Wrong model ID. Native run 2 used `claude-opus-5`, and so did both Superpowers runs. Only Opus 5.5 exists as `claude-opus-5-5`.

## Limits of this test

- n = 2 per arm, one app idea, and a simulated PM.
- Questions were asked in plain text, because AskUserQuestion is not available in non-interactive runs.
- This tested planning quality only, not the built app.
- Superpowers run 2 hit a 30-minute single-call timeout mid-plan. It was resumed once to finish.
- The judge is the same model family as the builders.

## Untested hypothesis

Use the native interview for the spec, then ask Superpowers `writing-plans` to turn it into tasks. This may combine native's requirement capture with Superpowers' task detail. It needs its own run before we recommend it.
