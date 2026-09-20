# [FEATURE NAME] - Agent Spec

<!--
WHAT THIS IS
A spec written for an AI coding agent to build from and prove against. It is technology-free:
it says WHAT the system does and HOW WE KNOW it is done, never how to implement it. The
builder derives its own plan and tasks.

SHAPE (benchmarked 19-09-2026 against GitHub Spec Kit spec-template.md, AWS Kiro
requirements.md, and the Claude Code best-practices rule "give the agent a way to verify"):
  1-3   Why and who         (MeetFlow evidence discipline: every number cited to a repo file)
  4     User stories        (Spec Kit: prioritized, each independently shippable, Given/When/Then)
  5     Requirements        (Kiro EARS: WHEN ... THE SYSTEM SHALL ..., plus a Verify line per FR)
  6     Unchanged behaviour (Kiro: SHALL CONTINUE TO, the regression contract)
  7-10  Edge cases, success criteria, out of scope, assumptions
  11    Clarifications      (the interview record, so the reasoning survives the run)

RULES
- No implementation detail anywhere: no file names, components, libraries, endpoints, schemas.
- No invented numbers. Every metric cites its source file.
- Every FR has a Verify line stated as an observable outcome, never as a test name.
- Budget: under 900 words excluding tables. If it needs more, it is two specs.
- Dates DD-MM-YYYY. No em dashes.
-->

**Author:** [PM NAME]
**Date:** [DD-MM-YYYY]
**Status:** [Draft / In Review / Approved]
**Problem statement (verbatim, as received):** "[PASTE THE EXACT ASK. Do not paraphrase. The spec is traced back to this.]"

---

## 1. Problem

<!-- 2-3 sentences. Lead with the number or quote that makes the pain real. Cite the file. -->
[WHAT IS BROKEN OR MISSING FOR THE USER, WITH A CITED NUMBER OR VERBATIM QUOTE.] (Source: `[FILE PATH]`)

---

## 2. Users Affected

<!-- Personas by name with file link. Segment size from company.md. -->
- **[PERSONA NAME] ([ROLE])** - [WHY THIS PERSONA HITS THE PROBLEM]. See `05-user-personas/[file].md`.
- **[PERSONA NAME] ([ROLE])** - [WHY]. See `05-user-personas/[file].md`.
- Segment size: [COUNT OR SEGMENT] (Source: `03-product-knowledge/company.md`)

---

## 3. Outcome

<!-- One sentence. What is true for the user after this ships that is not true today. -->
[AFTER THIS SHIPS, THE USER CAN ...]

---

## 4. User Stories

<!--
Order by priority. P1 alone must be a shippable slice that delivers value on its own.
Each story is independently buildable, testable and demonstrable.
Every story needs the happy path plus at least one non-happy scenario (empty, error, or edge).
-->

### US-1 - [SHORT TITLE] (P1)

As a [PERSONA], I want [ACTION] so that [OUTCOME].

**Why P1:** [WHAT BREAKS FOR THE USER IF ONLY THIS SHIPS AND NOTHING ELSE. IT SHOULD STILL BE WORTH SHIPPING.]

**Independent test:** [HOW A REVIEWER PROVES THIS STORY ALONE, IN ONE SENTENCE.]

| # | Given | When | Then |
|---|---|---|---|
| 1 | [INITIAL STATE] | [USER ACTION] | [OBSERVABLE RESULT] |
| 2 | [EMPTY OR ERROR STATE] | [SAME ACTION] | [WHAT THE USER SEES INSTEAD] |

### US-2 - [SHORT TITLE] (P2)

As a [PERSONA], I want [ACTION] so that [OUTCOME].

**Why P2:** [VALUE, AND WHY IT CAN WAIT FOR US-1.]

**Independent test:** [ONE SENTENCE.]

| # | Given | When | Then |
|---|---|---|---|
| 1 | [INITIAL STATE] | [USER ACTION] | [OBSERVABLE RESULT] |
| 2 | [NON-HAPPY STATE] | [ACTION] | [RESULT] |

<!-- Add US-3 (P3) and beyond only if each is still independently shippable. -->

---

## 5. Functional Requirements

<!--
EARS notation. One behaviour per line. "SHALL" is binding, "SHOULD" is not allowed here
(move it to Assumptions or Out of Scope).
Verify: an outcome a person or agent can observe and call pass or fail. No test names, no
tooling. The builder decides whether that becomes a unit test, a browser step, or a screenshot.
Trace: which story this serves.
-->

- **FR-001** WHEN [CONDITION OR EVENT] THE SYSTEM SHALL [BEHAVIOUR].
  **Verify:** [OBSERVABLE OUTCOME, e.g. "open the summary for a meeting with 3 action items, each item shows a confidence label of High, Medium or Low"].
  **Trace:** US-1
- **FR-002** WHEN [CONDITION] THE SYSTEM SHALL [BEHAVIOUR].
  **Verify:** [OBSERVABLE OUTCOME].
  **Trace:** US-1
- **FR-003** IF [ERROR OR MISSING INPUT] THEN THE SYSTEM SHALL [FALLBACK BEHAVIOUR].
  **Verify:** [OBSERVABLE OUTCOME].
  **Trace:** US-2

---

## 6. Unchanged Behaviour

<!--
The regression contract. Everything adjacent that must keep working exactly as today.
Written so the builder can check it after the change, not just promise it.
-->

- **UB-001** THE SYSTEM SHALL CONTINUE TO [EXISTING BEHAVIOUR, e.g. "show the full summary for meetings with zero action items"].
  **Verify:** [OBSERVABLE OUTCOME].
- **UB-002** THE SYSTEM SHALL CONTINUE TO [EXISTING BEHAVIOUR].
  **Verify:** [OBSERVABLE OUTCOME].

---

## 7. Edge Cases and Error States

<!-- Each row is a question the builder would otherwise answer alone. Give the answer. -->

| Case | Expected behaviour |
|---|---|
| [EMPTY STATE, e.g. "meeting has no transcript"] | [WHAT THE USER SEES] |
| [BOUNDARY, e.g. "50+ action items in one meeting"] | [WHAT HAPPENS] |
| [FAILURE, e.g. "confidence cannot be computed"] | [FALLBACK, AND WHAT THE USER IS TOLD] |
| [CONCURRENCY OR TIMING, if relevant] | [BEHAVIOUR] |

---

## 8. Success Criteria

<!--
Measurable, technology-agnostic, with a cited baseline. Tie to the quarter's OKRs.
These are outcome measures after launch, not build checks (those live in FR Verify lines).
-->

- **SC-001** [METRIC] moves from [BASELINE] to [TARGET] within [TIMEFRAME]. (Baseline source: `[FILE PATH]`)
- **SC-002** [METRIC] target [VALUE] by [DD-MM-YYYY]. (Baseline source: `[FILE PATH]`)
- **SC-003** [USER-LEVEL MEASURE, e.g. "9 of 10 users complete the primary task on first attempt"].

Cross-reference: `04-strategy/okrs-q2-2026.md`.

---

## 9. Out of Scope

<!-- Name it now or argue about it later. One line each, with the reason where it is not obvious. -->
- [EXCLUDED ITEM 1 - e.g. "Sending the follow-up email. v1 is draft and copy only."]
- [EXCLUDED ITEM 2]
- [EXCLUDED ITEM 3]

---

## 10. Assumptions

<!-- Defaults the PM chose where the ask was silent. Listed so a reader can veto before build. -->
- [ASSUMPTION 1 - e.g. "English only in v1."]
- [ASSUMPTION 2 - e.g. "Available on Pro and Team plans, not Free."]
- [DEPENDENCY - e.g. "Relies on the existing action item extraction, no changes to it."]

---

## 11. Clarifications Resolved

<!--
The interview record. Every question the agent asked and the answer it received, in order.
A finished spec has zero open items here. "[NEEDS CLARIFICATION]" appears only if the interview
was ended early, and each one must name the FR or story it blocks.
-->

| # | Question | Answer | Affects |
|---|---|---|---|
| 1 | [QUESTION ASKED] | [ANSWER GIVEN] | FR-00X / US-X |
| 2 | [QUESTION ASKED] | [ANSWER GIVEN] | [SECTION] |

Open: none.
