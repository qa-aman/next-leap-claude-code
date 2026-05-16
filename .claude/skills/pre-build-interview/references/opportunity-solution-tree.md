# Opportunity Solution Tree - Synthesis to Decision

Source: Teresa Torres, *Continuous Discovery Habits*.

The core insight: interview transcripts on their own do not produce decisions. You need a structure that connects what you heard (opportunities) to what you might build (solutions) to what you still do not know (assumption tests), all anchored to a business outcome. Otherwise the team relitigates the decision every week.

## The tree structure

```
                    DESIRED OUTCOME
                    (business metric)
                          |
       +------------------+------------------+
       |                  |                  |
  OPPORTUNITY A    OPPORTUNITY B    OPPORTUNITY C
  (user need)      (user need)      (user need)
       |                  |
   +---+---+         +----+----+
   |       |         |         |
 SOL 1   SOL 2     SOL 3     SOL 4
                     |
                +----+----+
                |         |
            ASSUMPTION  ASSUMPTION
            TEST 1      TEST 2
```

## How to build it in Phase 5

### Step 1: Outcome at the top

The outcome must be a business metric the team is already accountable for. In MeetFlow context, examples:

- Reduce Pro monthly churn from 4.1% to under 3%
- Lift Free to Pro conversion from 6.2% to 8%
- Improve action item accuracy from 66% to over 85%

Do not write "delight users" or "improve product". Outcomes must be measurable.

### Step 2: Opportunities from the interviews

An opportunity is a user need, pain point, or desire you heard repeatedly across interviews. Not a feature. Phrased as the user would phrase it.

Rules:
- Each opportunity must be backed by 3+ interview citations.
- Each opportunity is distinct (no overlap with siblings).
- Phrased in the user's words, not yours.

Examples:

**Bad opportunity:** "Build a Smart Follow-Up feature."
**Good opportunity:** "I cannot tell which action items from yesterday's meeting are still open."

**Bad opportunity:** "Improve AI accuracy."
**Good opportunity:** "When the AI gets an action item wrong, I have to redo the whole follow-up manually, so I stopped trusting it."

Sort opportunities by how many interviewees mentioned them and by impact on the outcome. Pick the top 2 to 4 for the tree. Park the rest in a "later" list.

### Step 3: Solutions under each opportunity

For each opportunity, list 2 to 4 possible solutions. The proposed feature is one of them. The others exist to make it clear you considered alternatives.

This is where the feature being validated finally appears, under the opportunity it claims to address. If the proposed feature does not slot cleanly under any of the opportunities you actually heard, that is the answer: KILL.

### Step 4: Assumption tests

For the leading solution under each opportunity, list the assumptions that must be true for it to work. Categorize each as:

- **Desirability**: do users want it?
- **Viability**: does it fit the business?
- **Feasibility**: can engineering build it?
- **Usability**: can users figure it out?

Mark which assumptions the interviews already validated, which they invalidated, and which are still open. Open assumptions become the test plan for ITERATE or BUILD next steps.

## The decision rules

After the tree is built, apply these rules:

| Tree state | Verdict |
|---|---|
| Proposed feature sits under a top-ranked opportunity, key assumptions validated, forces favor switch | BUILD |
| Feature sits under a real opportunity but key assumptions still open or anxiety dominates | ITERATE - test open assumptions, refine feature |
| Feature does not slot under any heard opportunity, OR habit dominates | KILL |
| Tree reveals a bigger opportunity than the feature addresses | PIVOT - new feature scope under the same outcome |

## Mini-tree template for the decision doc

Keep it small. The whole tree should fit on one page.

```
OUTCOME: [metric + target]

  OPPORTUNITY 1: "[user quote / paraphrase]"
    cited by: I-01, I-03, I-05, I-08 (4 of 8)
    solutions:
      - [proposed feature] <- the one being validated
      - [alternative 1]
      - [alternative 2]
    key assumptions:
      [v] users will trust the output (validated by I-03, I-05)
      [x] users will check it less than 30 sec (invalidated by I-01)
      [?] enterprise admins will allow it (untested)

  OPPORTUNITY 2: "[user quote / paraphrase]"
    cited by: I-02, I-04, I-07 (3 of 8)
    ...
```

Legend: `[v]` validated, `[x]` invalidated, `[?]` open.

## Why this matters for the final recommendation

The tree forces the question: "Does the feature we want to build actually map to what users said matters?"

Most pre-build interviews skip this step. The team hears users say "yes the problem is real" and ships the feature they originally wanted. The tree exposes the gap between heard opportunities and proposed solutions, which is where most features die after launch.

Reference: there is also a separate `opportunity-solution-tree` skill in this repo. Use it for fuller-scale roadmap work. For pre-build interview synthesis, the mini-tree above is enough.
