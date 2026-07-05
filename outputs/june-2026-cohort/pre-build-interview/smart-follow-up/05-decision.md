# Decision: [BUILD / ITERATE / KILL] - Smart Follow-Up

**Date:** [DD-MM-YYYY - complete after interviews]
**Interviewees:** [N completed of 10 target]
**Segment:** Pro users running 5+ recurring meetings/week
**Decision owner:** AI Intelligence PM

> This file is a template populated after interviews complete. The verdict goes on line 1. Stakeholders rarely read past the first paragraph - structure accordingly.

---

## Verdict

[2 to 3 sentences. State the decision, the single strongest reason, and the next concrete step.]

Example BUILD: *"Build Smart Follow-Up as scoped. 8 of 10 interviewees described the action-item rewrite workflow unprompted and rated it the worst part of their day. The Action Item Scoring v2 dependency remains the gating risk. Next step: lock the beta cohort and confirm the v2 ML model accuracy gate by 31-03-2026."*

Example ITERATE: *"Iterate before building. Problem is real (9 of 10 confirmed) but anxiety about AI-drafted emails sent to customers is the dominant blocker. Reshape the feature to draft-into-clipboard-only for the first 30 days post-launch, then add direct send. Re-interview 5 users on the revised flow by 04-04-2026."*

Example KILL: *"Kill Smart Follow-Up as scoped. Users handle follow-ups themselves and consider the current 5-minute manual rewrite acceptable. Push exists but habit dominates. Recommend redirecting engineering capacity to Salesforce integration (which 6 of 10 mentioned unprompted as a bigger pain) and revisiting the Smart Follow-Up trust mechanism in Q3."*

---

## Evidence against thresholds

| Signal | Target | Actual | Pass / Fail |
|---|---|---|---|
| Problem described unprompted in first 10 min | 7 / 10 | [N] | [pass / fail] |
| Active workaround described | 8 / 10 | [N] | [pass / fail] |
| Workaround described as painful (strong words) | 6 / 10 | [N] | [pass / fail] |
| Showed workaround on screen (commitment rung 2) | 5 / 10 | [N] | [pass / fail] |
| Push + Pull > Anxiety + Habit | 6 / 10 | [N] | [pass / fail] |

**Overall:** [X of 5 thresholds cleared]

---

## Forces of Progress summary

Aggregate across all interviewees. See `references/jtbd-forces.md`.

| Force | Strength across sample | Top evidence |
|---|---|---|
| Push (status quo pain) | [Strong / Medium / Weak] | [1-2 representative quotes] |
| Pull (attraction of new) | [Strong / Medium / Weak] | [1-2 representative quotes] |
| Anxiety (switching fears) | [Strong / Medium / Weak] | [1-2 representative quotes] |
| Habit (inertia) | [Strong / Medium / Weak] | [1-2 representative quotes] |

**Force balance:** [interpretation - which side dominates and what that implies for adoption]

Per-interviewee force table:

| ID | Push | Pull | Anxiety | Habit | Net |
|---|---|---|---|---|---|
| I-01 |  |  |  |  | Switch / Stay |
| I-02 |  |  |  |  | Switch / Stay |
| ... |  |  |  |  | |

---

## Opportunity Solution Tree

```
OUTCOME: Reduce Pro monthly churn from 4.1% to under 3% by 31-12-2026
         (and improve action item accuracy from 66% to 80% by end of Q2 2026)

  OPPORTUNITY 1: "[Top opportunity in user words]"
    cited by: [list of interview IDs] (N of 10)
    solutions:
      - Smart Follow-Up (as scoped) <- the validated feature
      - [alternative considered]
      - [alternative considered]
    key assumptions:
      [v / x / ?] users will trust confidence scores enough to skip review
      [v / x / ?] 2-minute review target is achievable at 8-10 meetings/day
      [v / x / ?] multi-channel export (Slack + Notion + Jira) is essential, not nice-to-have
      [v / x / ?] users want to send themselves vs. delegate

  OPPORTUNITY 2: "[Second opportunity in user words]"
    cited by: [list] (N of 10)
    solutions:
      - [solution]
      - [solution]
```

Legend: `[v]` validated by interviews, `[x]` invalidated, `[?]` open and needs further test.

---

## What this means for the roadmap

[1 to 2 sentences linking back to Q2 2026 OKRs in `04-strategy/okrs-q2-2026.md`. Be specific about what changes - sprint scope, beta cohort, dependency timing, or kill/replan.]

---

## What we will NOT do based on this research

[Explicit list of things stakeholders might push for but the evidence does not support. Prevents scope creep and relitigation in 3 months.]

---

## Appendix - method

- Sample size: [N] of 10 target
- Recruit source breakdown: [from recruit plan]
- Interview window: [dates]
- Known biases in the sample: [from recruit plan risks section]
- Confidence in the decision: [High / Medium / Low] - [one sentence justification]
