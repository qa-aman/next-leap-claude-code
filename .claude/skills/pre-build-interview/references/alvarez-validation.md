# Lean Customer Development - Hypothesis and Signal Thresholds

Source: Cindy Alvarez, *Lean Customer Development*.

The core insight: problem validation is a falsifiable experiment. Without a written hypothesis and a threshold for failure, every interview "confirms" the idea because you cannot distinguish signal from politeness.

## The hypothesis template

Use this exact structure. Fill every field. Vague fields produce vague interviews.

```
We believe that [specific user segment]
experiences [specific problem]
when [specific trigger / context]
and currently handles it by [current workaround]
which is painful because [frequency + severity + cost].

We will know we are right if, across 8 to 12 interviews:
- At least [N1] describe the problem without being prompted
- At least [N2] describe a workaround they actively use today
- At least [N3] describe the workaround as painful (their words, not ours)

We will walk away if:
- Fewer than [N1] describe the problem unprompted, OR
- Most describe the workaround as "fine" or "good enough"
```

## Default thresholds

Use these unless the user has reason to deviate:

| Signal | Default threshold (out of 10) |
|---|---|
| Describe problem unprompted | 6 |
| Describe an active workaround | 7 |
| Describe workaround as painful | 5 |
| Climb to commitment ladder rung 2+ (show workaround on call) | 4 |

Lower thresholds for very new spaces (you may be the first to ask). Raise for crowded spaces (many tools exist already and users have strong opinions).

## Segment specificity

A segment is specific enough when you can name it in one sentence and the user can recruit against it. Examples:

**Too vague:**
- "Knowledge workers"
- "MeetFlow users"
- "Managers"

**Specific enough:**
- "MeetFlow Pro users who run 10+ recurring meetings per week"
- "Engineering managers at Series B SaaS companies who run weekly 1:1s with 5+ direct reports"
- "Customer success leads using MeetFlow who export action items to Salesforce or Notion"

Force the user to commit to a segment in Phase 1. Mixed segments produce mixed signals.

## Sample size

8 to 12 interviews is the right zone for problem validation.

- Below 6: you are reading noise, not pattern.
- 8 to 10: enough to see clear patterns if they exist.
- 12+: usually unnecessary unless the signal is mixed and you need more data to break the tie.

If after 8 interviews the answer is obvious in either direction, stop. Save the time for the next experiment.

## Recruit plan template

```
## Recruit Plan - [Feature name]

**Target N:** [8 to 12]
**Segment:** [from hypothesis]
**Source:** [existing users / cold outreach / panel / intercept]

**Screener questions** (3 max):
1. [Behavioral question - have you done X in the last 30 days]
2. [Context question - what tool do you use for Y]
3. [Frequency question - how often do you Z]

**Disqualifiers:** [who to exclude and why]

**Incentive:** [if any - $50 gift card is typical for 30 min]

**Timeline:** [calendar week target]
**Owner:** [who is recruiting]
```

## When validation is "good enough" to move forward

The threshold is not "users love the feature". It is "users have the problem painfully enough that they will switch behavior to solve it".

Walk away signals:
- Users describe the problem only when prompted, never first.
- Workarounds are described as "fine", "no big deal", "I just do X and move on".
- Users cannot recall a specific recent incident.
- The pain is real but they have already tried 3+ tools and given up.

Proceed signals:
- Users bring up the problem before you ask.
- They show you their workaround on the call (commitment rung 2).
- They use words like "hate", "waste", "kills me", "every single time".
- They introduce you to a colleague with the same problem (commitment rung 3).
