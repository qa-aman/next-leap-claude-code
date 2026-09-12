# Interview Synthesis Brief

## TL;DR
- Action item accuracy is the top pain for power users and sales-driven teams. Sarah Chen manually double-checks every item, and James Whitfield says roughly 1 in 3 sales calls has an action item wrong enough to matter.
- Missing native integrations (Salesforce for James, Notion-style consolidation for Priya) are creating manual busywork and active churn risk. James's team has a Q1 2026 deadline before piloting Fireflies.
- Distrust in the AI's output is blocking expansion revenue, not just daily workflow. Sarah has withheld an 8-seat Team plan upgrade and won't enable Meeting Pattern Insights until accuracy improves.

## Top 3 Themes

### 1. Action Item Accuracy Undermines Trust in Core Output
Mentioned in 2 of 4 interviews (Sarah Chen, James Whitfield). Severity: workflow-breaker, both users describe wrong action items as directly breaking their workflow or their client relationships.
> "I double-check the action items manually. Which defeats the purpose. If I'm going to review every item anyway, why not just take notes myself?" (interview-01-sarah-chen.md)

> "The accuracy thing is real. Maybe 1 in 3 calls has an action item that's wrong enough to matter. For sales, wrong follow-up is worse than no follow-up." (interview-04-james-whitfield.md)

### 2. Missing Native Integrations Push Users Toward Competitors
Mentioned in 2 of 4 interviews (James Whitfield, Priya Nair). Severity: workflow-breaker, James has a concrete end-of-Q1-2026 deadline before piloting Fireflies, and his team currently loses 10+ hours a day copying summaries into Salesforce by hand.
> "I need this in Salesforce. That's where my pipeline lives. When my rep has a call with a prospect, I need the summary and action items in the opportunity record. Not in Slack, not in Notion — in Salesforce." (interview-04-james-whitfield.md)

### 3. Distrust in the AI Blocks Expansion Revenue and Feature Adoption
Mentioned in 2 of 4 interviews (Sarah Chen, Marcus Okafor). Severity: workflow-breaker, in both cases the user is explicit that distrust is blocking a purchasing or renewal decision, not just causing friction.
> "Fix accuracy, I'll move my whole team to Team plan. That's 8 seats. I've already pitched it to my CEO, but I told him we need to wait until the action items are reliable." (interview-01-sarah-chen.md)

## Full Ranked Table (Stage 3)

| Rank | Theme | Interviews mentioning | Severity | Justification (in the user's language) |
|---|---|---|---|---|
| 1 | Action Item Accuracy Undermines Trust in Core Output | 2 of 4 (Sarah, James) | workflow-breaker | Sarah: "defeats the purpose" of using the tool. James: "wrong follow-up is worse than no follow-up." |
| 2 | Missing Native Integrations Push Users Toward Competitors | 2 of 4 (James, Priya) | workflow-breaker | James: concrete Fireflies pilot deadline, "10+ hours of daily admin work." Priya: "I'd switch" if Notion added the feature. |
| 3 | Distrust in the AI Blocks Expansion Revenue and Feature Adoption | 2 of 4 (Sarah, Marcus) | workflow-breaker | Sarah withholds an 8-seat upgrade; Marcus: "we're paying for a tool most of my team ignores... adoption won't happen until I trust the security story." |
| 4 | Weak Perceived Value Drives Price Sensitivity and Passive Use | 2 of 4 (Marcus, Priya) | annoyance | Priya: "it feels like a lot" but keeps paying for the Slack digest. Marcus: "Nobody reads the summaries," tolerated rather than escalated. |
| 5 | Privacy and Data Control Concerns Block Enterprise Confidence | 1 of 4 (Marcus) | workflow-breaker | Marcus: "I don't trust any system that records my engineering reviews... Where does that data go?" A stated dealbreaker, but raised in only one interview. |

Note on theme 5: only one of the four interviews (Marcus Okafor) raised privacy and data retention as a pain, so by the ranking rule (interview count first) it sits last despite the severity tag. Its content still supports the existing Enterprise tier roadmap (SOC 2, on-prem storage, admin controls) referenced in that transcript's researcher notes.

## Recommendations
- Prioritize implicit-commitment detection and confidence-score reliability in Action Item Confidence Scoring v2, since this is the direct cause of theme 1 and is already the current sprint's focus.
- Give the Salesforce integration a committed public timeline before end of Q1 2026 to address theme 2 and retain James Whitfield's 22-seat account before his Fireflies pilot starts.
- Treat action item accuracy as a revenue-unlock, not just a satisfaction metric, when prioritizing against theme 3: Sarah's 8-seat expansion is explicitly gated on it.
- Revisit summary length and pricing perception for lower-usage Pro users to address theme 4, since it is currently tolerated but could tip into churn under competitive pressure (Notion).
- Treat theme 5 as validated input for the existing Enterprise tier workstream (SOC 2, on-prem storage, configurable retention, per-meeting exclusion) rather than a new AI Intelligence initiative, since Marcus's objections are structural, not accuracy-related.
