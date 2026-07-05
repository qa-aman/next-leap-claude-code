# Interview Synthesis Brief

## TL;DR
- Action item accuracy is the top workflow-breaker, raised by 2 of 4 interviewees (Sarah Chen, James Whitfield), and it directly blocks a power user's Team plan upgrade and a sales director's renewal decision.
- Missing integrations (Salesforce, Notion) put two Team-plan-relevant accounts at active churn risk: James Whitfield has an end-of-Q1-2026 deadline before piloting Fireflies, and Priya Nair says she'd switch if Notion bundled meeting summaries.
- Two interviewees engage with MeetFlow passively or superficially (Marcus Okafor's team ignores summaries entirely, Priya Nair only reads the Slack digest and skims), signaling weak product-workflow fit for a meaningful segment beyond the two power users.

## Top 3 Themes

### 1. Action Item Accuracy and Trust
Mentioned in 2 of 4 interviews (Sarah Chen, James Whitfield). Severity: workflow-breaker, because it blocks Sarah's willingness to upgrade her team and makes James's reps "look unprofessional" on client calls.
> "Confidence score says 'high' but misses the most important item. Every. Single. Time. Yesterday it caught 'send the invite' but missed 'we need to realign the roadmap before board review.' That's the one that matters." (interview-01-sarah-chen.md)

### 2. Missing Integrations / Standalone Product
Mentioned in 2 of 4 interviews (James Whitfield, Priya Nair). Severity: workflow-breaker, because James has set a concrete end-of-Q1-2026 deadline to pilot Fireflies if Salesforce integration isn't on a timeline.
> "I need this in Salesforce. That's where my pipeline lives. When my rep has a call with a prospect, I need the summary and action items in the opportunity record. Not in Slack, not in Notion — in Salesforce." (interview-04-james-whitfield.md)

### 3. Product Doesn't Fit Real Usage Patterns
Mentioned in 2 of 4 interviews (Marcus Okafor, Priya Nair). Severity: annoyance, because usage is shallow or single-feature-dependent but tolerated rather than actively blocking work.
> "My team uses it because IT deployed it. Nobody reads the summaries. We have our own Google Docs process for sprint reviews and retros. MeetFlow runs in the background — I forget it's there most days." (interview-02-marcus-okafor.md)

## Full Theme Ranking

| Rank | Theme | Interviews | Severity | Justification |
|---|---|---|---|---|
| 1 | Action Item Accuracy and Trust | 2/4 (Sarah, James) | workflow-breaker | Sarah "double-checks manually" every item; James says wrong follow-ups make reps "look unprofessional." |
| 2 | Missing Integrations / Standalone Product | 2/4 (James, Priya) | workflow-breaker | James has a concrete Q1 2026 deadline to pilot Fireflies; product is a "standalone island." |
| 3 | Product Doesn't Fit Real Usage Patterns | 2/4 (Marcus, Priya) | annoyance | Marcus's team ignores summaries but has a workaround; Priya skims but keeps paying. |
| 4 | Data Privacy and Retention Concerns | 1/4 (Marcus) | workflow-breaker | Marcus says "adoption won't happen until I trust the security story," tying directly to a 120-seat renewal. |
| 5 | Pricing Sensitivity | 1/4 (Priya) | annoyance | "$15/month... feels like a lot," but she keeps the plan for the Slack digest alone. |

Note: theme 4 (Data Privacy) carries workflow-breaker severity but ranks below theme 3 because only 1 of 4 interviews raised it; interview count is the primary sort key per the ranking methodology.

## Recommendations
- Prioritize implicit-commitment detection in Action Item Confidence Scoring v2, the specific gap Sarah names ("I'll circle back on that" / "let's think about whether we should revisit pricing" going uncaptured).
- Give Dana's Salesforce integration a committed public timeline before end of Q1 2026 to prevent James's 22-seat account from starting a Fireflies pilot.
- Investigate whether shorter, bulleted summary formats (Priya's request) would increase engagement among casual users who currently only skim or ignore output, without waiting on a full redesign.
- Flag Marcus's data retention and SOC 2 gaps to Tomás's Enterprise & Security roadmap; his 40-seat sub-account is a live renewal risk independent of AI Intelligence work.
