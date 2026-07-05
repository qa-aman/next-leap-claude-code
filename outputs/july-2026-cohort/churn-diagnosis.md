# Churn Diagnosis: MeetFlow Pro

Baseline: Pro monthly churn 4.1% (03-product-knowledge/company.md)

## Top 3 Churn Drivers

### 1. Action item accuracy (34% error rate)
Evidence:
- "Action items wrong or missing" was the top complaint theme with 19 mentions: "I can't trust the action items. I still have to go back and check every single one." (06-user-feedback/feedback-q1-2026.md)
- "The gap between promoters and detractors is explained almost entirely by action item accuracy... Detractors rely on action items as their task management system and get burned by the 34% error rate." (06-user-feedback/feedback-q1-2026.md)
- "I double-check the action items manually. Which defeats the purpose. If I'm going to review every item anyway, why not just take notes myself?" (07-user-interviews/interview-01-sarah-chen.md)
- "Maybe 1 in 3 calls has an action item that's wrong enough to matter. For sales, wrong follow-up is worse than no follow-up." (07-user-interviews/interview-04-james-whitfield.md)

Why it drives churn: This is the strongest driver, both in volume (top complaint at 19/47 mentions) and in depth (two independent interviews, a power user and a sales director, describe it as the reason they discount or delay expansion/renewal). It directly maps to the 66% accuracy baseline in 03-product-knowledge/company.md and is named there as "the top complaint driving churn."

### 2. Missing Salesforce/CRM integration for revenue-critical workflows
Evidence:
- "Need Salesforce integration" was the third-highest complaint theme with 11 mentions: "We're a sales org. No Salesforce = no deal for Team plan." (06-user-feedback/feedback-q1-2026.md)
- "I need this in Salesforce. That's where my pipeline lives... Right now my team manually copies meeting summaries into Salesforce. That's 10-15 minutes per call." (07-user-interviews/interview-04-james-whitfield.md)
- "Fireflies does the Salesforce thing. Auto-logs the call summary, action items, even sentiment analysis right into the opportunity. We're considering switching." (07-user-interviews/interview-04-james-whitfield.md)

Why it drives churn: For sales-heavy Team accounts, integration absence is a concrete, dated churn trigger (James Whitfield's 22-seat account, $12,936/year, has an end-of-Q1-2026 deadline before piloting Fireflies). It converges in both the survey and an interview, though the interview evidence is currently limited to one account, so treat the urgency as real but the segment size as narrower than driver 1.

### 3. Summary length and lack of concise structure
Evidence:
- "Summaries too long" was the second-highest complaint theme with 14 mentions: "I want bullet points, not an essay. Give me the 3 things that matter." (06-user-feedback/feedback-q1-2026.md)
- "The summaries are, like, 6 paragraphs? I skim them. My CEO skims them. I want 3-4 bullet points." (07-user-interviews/interview-03-priya-nair.md)

Why it drives churn: This is a satisfaction drag on casual/light users like Priya, who are already price-sensitive ("$15/month for something I use twice a week... If it were $8, I wouldn't think about it," interview-03-priya-nair.md) and vulnerable to Notion bundling free meeting summaries. It appears in both the survey and an interview, but the interview evidence comes from a single casual-user persona rather than a power user, so this driver is more about accelerating an already-loose relationship than being a standalone cause.

## Secondary Drivers (single-source or thin evidence, not in top 3)

- Privacy/data retention concerns: 8 mentions in the survey (06-user-feedback/feedback-q1-2026.md) and echoed strongly by Marcus Okafor ("I don't trust any system that records my engineering reviews... Where does that data go?", interview-02-marcus-okafor.md). This does appear in two sources, but Marcus explicitly frames his issue as an "adoption issue," not an active cancellation driver for his account, and it maps to the Enterprise/security roadmap rather than the AI Intelligence pillar, so it is flagged as secondary rather than promoted to the top 3.
- Price sensitivity for light use: 7 mentions in the survey (06-user-feedback/feedback-q1-2026.md), echoed by Priya Nair, but this is best read as a symptom of low engagement (driven by summary length and passive Slack-only usage) rather than an independent driver.

## Quick Wins (shippable in under 2 sprints)

- Ship a "top 3 bullet" summary format toggle (decisions made, who owns what) as a default view instead of the current 6-paragraph format, addressing driver 3 directly for the 14 survey respondents who asked for it.
- Add a lightweight confidence-flag UI so users can see and quickly correct low-confidence action items inline, reducing manual double-checking time for driver 1 without waiting for a full model retrain.
- Publish a short, public data retention/auto-delete FAQ (even ahead of full SOC 2 work) to blunt the loudest privacy objections cheaply, since it was raised by 8 survey respondents and one interview.

## Structural Fixes (quarter-level work)

- Rebuild action item extraction to catch implicit commitments ("I'll circle back on that," "let's think about whether we should revisit X"), the specific gap Sarah Chen identifies as the core failure mode; this is the current Action Item Confidence Scoring v2 sprint and should stay the top investment given it is the only driver with survey-plus-multiple-interview convergence (driver 1).
- Ship the Salesforce integration on the committed May 2026 timeline (04-strategy/product-vision.md) and communicate a concrete date to at-risk Team accounts like James Whitfield's before the end of Q1 2026 deadline he has set internally (driver 2).
- Redesign the default summary structure and length as part of Smart Summaries work, informed by the 14-mention survey signal and Priya Nair's feedback, to reduce churn risk among casual/light-usage Pro users who are otherwise vulnerable to Notion bundling (driver 3).
