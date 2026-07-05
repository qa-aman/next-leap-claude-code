# User Interview Synthesis

**Date:** 17-03-2026
**Interviews:** 4 transcripts from `07-user-interviews/`
**Source files:** `interview-01-sarah-chen.md`, `interview-02-marcus-okafor.md`, `interview-03-priya-nair.md`, `interview-04-james-whitfield.md`

---

## TL;DR

- Action item accuracy is the most widespread pain: 3 of 4 users describe outputs they cannot trust, leading to manual re-work that erases the product's core value.
- The tool does not live where users work: 3 of 4 users need outputs in a specific system (Salesforce, Slack, Google Docs) and MeetFlow's failure to integrate there makes it a background nuisance or an active churn candidate.
- Trust failure compounds everything: once a user loses confidence in the AI, they stop engaging with new features and start evaluating exits -- two users are at that point now.

---

## Top 3 Themes

### 1. Action Item Accuracy and AI Output Quality

**Interview count:** 3 of 4 (interview-01-sarah-chen.md, interview-03-priya-nair.md, interview-04-james-whitfield.md)
**Severity:** workflow-breaker

Action items are wrong or missing often enough that users have built manual review into their workflow -- which defeats the product's purpose. Sarah catches 2-3 errors per day. James sees a wrong item on 1 in 3 sales calls, which damages client relationships. Priya finds summaries too long to skim, meaning the structured output never lands. The implicit-commitment gap (language like "I'll circle back on that" classified as discussion, not action) is the sharpest edge of this problem.

> "I double-check the action items manually. Which defeats the purpose. If I'm going to review every item anyway, why not just take notes myself?" (interview-01-sarah-chen.md)

---

### 2. Missing Workflow Integration

**Interview count:** 3 of 4 (interview-02-marcus-okafor.md, interview-03-priya-nair.md, interview-04-james-whitfield.md)
**Severity:** workflow-breaker

MeetFlow produces outputs in MeetFlow. The people who should use those outputs work in Salesforce, Slack, Notion, and Google Docs. When the output does not land in the user's actual tool, it either does not get read (Marcus's team, Priya outside of Slack) or gets manually copied at enormous cost (James's team: 10+ hours of admin per day across 15 reps). The tool is perceived as a standalone island, not a workflow layer.

> "Right now my team manually copies meeting summaries into Salesforce. That's 10-15 minutes per call. With 15 reps doing 4-5 calls a day, that's 10+ hours of daily admin work across the team." (interview-04-james-whitfield.md)

---

### 3. Trust in the System

**Interview count:** 2 of 4 (interview-01-sarah-chen.md, interview-02-marcus-okafor.md)
**Severity:** workflow-breaker

Two different users have lost trust in MeetFlow for two different reasons. Sarah's trust eroded through repeated AI accuracy failures -- she refuses to use Meeting Pattern Insights because she no longer believes the underlying AI is reliable. Marcus's trust is structural: he has no visibility into where recordings go, no SOC 2 certification to share with his CISO, and no on-prem option for sensitive engineering discussions. Both paths lead to the same outcome: the user stops engaging and starts planning exit.

> "I don't trust the AI enough to give me meeting analytics. If it can't get action items right, why would I trust it to tell me how I spend my time?" (interview-01-sarah-chen.md)

---

## Recommendations

1. **Ship implicit-commitment detection in Action Item Scoring v2.** Language patterns like "I'll circle back," "let's revisit," and "we should think about" are explicit training targets. This is the single fix with the highest user-facing impact for the AI Intelligence pillar.

2. **Accelerate Salesforce integration and validate James's account timeline.** His team's Q1 2026 deadline has passed. A concrete shipping commitment -- not a roadmap slide -- is the only thing that prevents a Fireflies pilot from starting. Dana's Q2 date may already be too late.

3. **Publish a data governance page users can share with their CISO.** SOC 2 Type II, on-prem storage timeline, and configurable auto-delete are the specific asks from Marcus. This is a prerequisite for enterprise renewal, not a nice-to-have.

4. **Add a "brief mode" summary option.** 3-4 structured bullets (decisions, owners, deadlines) as an opt-in output format. This addresses Priya's output format pain and raises the perceived value of summaries for exec-facing workflows.

---

*All quotes are verbatim from the source transcripts. No metrics were added beyond what appears in the interview files.*
