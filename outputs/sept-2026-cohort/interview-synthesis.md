# Interview Synthesis Brief

## TL;DR
- Across all 4 interviews (Sarah Chen, Marcus Okafor, Priya Nair, James Whitfield in `07-user-interviews/`), 19 distinct pains cluster into 4 themes. AI output trust (action items and summaries) is the most corroborated theme, raised by 3 of 4 users, and is already the active engineering sprint, not an open decision.
- Two concrete deadlines are live right now: James Whitfield's Fireflies pilot decision (end of Q1 2026, 22 seats, $12,936/year) and Sarah Chen's held 8-seat Team upgrade ($4,700/year), both blocked on trust rather than a missing feature.
- Marcus Okafor's privacy and data-control concerns surfaced in only 1 of 4 interviews but carry workflow-breaker severity and put a 120-seat renewal at risk; this belongs to the Enterprise tier workstream, not AI Intelligence.

## Top 3 Themes

### 1. AI output requires manual correction and erodes trust
Mentioned in 3 of 4 interviews (Sarah Chen, James Whitfield, Priya Nair). Severity: workflow-breaker, because it forces users to redo the work MeetFlow is meant to save and blocks revenue Sarah has already pitched internally.
> "I double-check the action items manually. Which defeats the purpose. If I'm going to review every item anyway, why not just take notes myself?" (interview-01-sarah-chen.md)

Supporting evidence: Sarah's confidence score marks wrong items "high" and misses implicit commitments ("When someone says 'I'll circle back on that,' that's a commitment. MeetFlow doesn't catch it," interview-01-sarah-chen.md); this same distrust stops her from turning on Meeting Pattern Insights and from moving her 8-seat Team upgrade forward. James reports "1 in 3 calls has an action item that's wrong enough to matter," and a wrong next step means "My rep looks unprofessional" (interview-04-james-whitfield.md). Priya's version of the same root problem is summary length: "The summaries are, like, 6 paragraphs? I skim them... I want 3-4 bullet points" (interview-03-priya-nair.md).

### 2. Missing native integrations push users toward competitors
Mentioned in 2 of 4 interviews (James Whitfield, Priya Nair). Severity: workflow-breaker, because James has a live competitive pilot on a fixed deadline and a documented 10+ hours/day of manual admin work across his team.
> "I don't want to switch. MeetFlow's summaries are better than Fireflies. But 'better summaries' doesn't beat 'summaries that are actually in Salesforce.' Integration wins over quality when quality isn't in my workflow." (interview-04-james-whitfield.md)

Supporting evidence: James's team manually copies summaries into Salesforce, "10-15 minutes per call... 10+ hours of daily admin work across the team" (interview-04-james-whitfield.md), and he has given his team until end of Q1 2026 before starting a Fireflies pilot. Priya names the same structural risk from her tool of record: "If Notion added meeting summaries that auto-posted into our meeting notes pages... honestly, I'd switch" (interview-03-priya-nair.md).

### 3. Narrow perceived value and price sensitivity expose churn and bundling risk
Mentioned in 2 of 4 interviews (Priya Nair, Marcus Okafor). Severity: annoyance, because both users currently tolerate it ("I keep it because the Slack thing is so convenient") rather than actively churning today.
> "Fifteen dollars a month for something I use twice a week... I keep it because the Slack thing is so convenient, but it feels like a lot. If it were $8, I wouldn't think about it." (interview-03-priya-nair.md)

Supporting evidence: Priya's entire experience runs through one integration ("If the Slack integration broke, I'd probably cancel within a week," interview-03-priya-nair.md), and the $49/seat Team plan is "a non-starter" for her 45-person company. Marcus describes near-zero active use org-wide: "Nobody reads the summaries. We have our own Google Docs process for sprint reviews and retros" (interview-02-marcus-okafor.md), says the tool mostly runs unnoticed in the background, and doubts AI adds value to meetings at all.

Note: a fourth theme, privacy and data control (Marcus Okafor, interview-02-marcus-okafor.md), cleared the clustering gate with 4 supporting pains but ranks below the three above on interview count. It carries workflow-breaker severity in its own right, tied to a 120-seat renewal decision, and is addressed in the recommendations below.

## Recommendations
- Theme 1 (accuracy/trust) is already the active sprint (Action Item Confidence Scoring v2, 17-03-2026 to 28-03-2026, per project roadmap): do not treat this as an open prioritization call. Confirm the shipped scope explicitly covers implicit commitments ("I'll circle back," soft phrasing) and sequencing errors like James's case, since both are named failure modes in the transcripts, and measure success post-launch against Sarah's 8-seat upgrade and James's Fireflies decision, not just the 66% accuracy baseline.
- Theme 2 (integrations): Salesforce is scheduled for May 2026, after James's end-of-Q1-2026 deadline. This is the one open decision in this brief: give James a firm interim commitment (a timeline or a manual-workaround SLA) before his team starts the Fireflies pilot, since losing a 22-seat account validates the exact gap Fireflies is selling against.
- Theme 3 (value/price): not urgent today, but monitor for Notion's bundled meeting-summary launch; if it ships, re-survey Priya-profile users (light usage, single-integration-dependent, Pro tier) before assuming Theme 1's fixes will retain them.
- Privacy/data control (Marcus, not in the top 3 by interview count but workflow-breaker severity): this maps to the Enterprise tier workstream (SSO, admin controls, audit logs, on-prem storage, GA June 2026), already roadmapped and not an AI Intelligence decision. Confirm the timeline lands ahead of the 120-seat contract renewal date, since Marcus has stated he will recommend against renewal on adoption grounds tied to unresolved security trust.
