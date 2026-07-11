# Triangulated Feedback

Sources: user interviews (07-user-interviews/, 4 transcripts), Q1 2026 NPS survey (06-user-feedback/feedback-q1-2026.md, 47 respondents), and Pro churn context (03-product-knowledge/company.md, 04-strategy/product-vision.md).

## Triangulated Issues (2+ sources) - top priorities

### 1. Action item accuracy - 3 of 3 sources
- Interviews: Sarah Chen manually checks every action item and catches 2-3 errors per day; MeetFlow misses implicit commitments such as "I'll circle back on that" and read her CEO's "let's think about whether we should revisit pricing" as a discussion point rather than an action item (07-user-interviews/interview-01-sarah-chen.md). James Whitfield estimates roughly 1 in 3 sales calls has an action item wrong enough to matter, which makes his reps "look unprofessional" with prospects (07-user-interviews/interview-04-james-whitfield.md).
- Survey: "Action items wrong or missing" is the top complaint theme, 19 of 47 respondent mentions, verbatim "I can't trust the action items. I still have to go back and check every single one." (06-user-feedback/feedback-q1-2026.md)
- Churn: "Action item accuracy is the top complaint driving churn" and "Action item accuracy at 66% (34% wrong or missing) is eroding trust with the most valuable user segment - power users who rely on action items as their task system" (03-product-knowledge/company.md). Product vision lists it as the top current gap: "Action items are wrong 34% of the time. Users can't trust what MeetFlow captures." (04-strategy/product-vision.md)

### 2. Salesforce integration gap / Fireflies competitive threat - 2 of 3 sources
- Interviews: James Whitfield says "I need this in Salesforce... Not in Slack, not in Notion - in Salesforce." His team manually copies summaries into Salesforce, costing 10+ hours of admin work daily across his 15 reps. Fireflies "auto-logs the call summary, action items, even sentiment analysis right into the opportunity," and his 22-seat Team account ($12,936/year) is at risk with a self-imposed end-of-Q1-2026 deadline to see a Salesforce timeline (07-user-interviews/interview-04-james-whitfield.md).
- Survey: "Need Salesforce integration" theme, 11 of 47 respondent mentions, verbatim "We're a sales org. No Salesforce = no deal for Team plan." (06-user-feedback/feedback-q1-2026.md)
- Note: company.md names Salesforce integration as "most-requested integration" under Current Priorities and cites "direct competitive pressure from Fireflies," but does not tie it explicitly to the 4.1% Pro churn figure, so it is not counted as a churn-source citation here.

### 3. Summaries too long - 2 of 3 sources
- Interviews: Priya Nair: "The summaries are, like, 6 paragraphs? I skim them. My CEO skims them. I want 3-4 bullet points - the decisions that were made and who's doing what." (07-user-interviews/interview-03-priya-nair.md)
- Survey: "Summaries too long" theme, 14 of 47 respondent mentions, verbatim "I want bullet points, not an essay. Give me the 3 things that matter." (06-user-feedback/feedback-q1-2026.md)

### 4. Privacy and data retention concerns - 2 of 3 sources
- Interviews: Marcus Okafor wants SOC 2 Type II certification, on-prem transcript storage, configurable auto-delete (30/60/90 days), and the ability to exclude specific meetings from recording; he says "I asked IT about the data retention policy. They didn't have a clear answer. That's a problem." This blocks real adoption on his 120-seat Team account (07-user-interviews/interview-02-marcus-okafor.md).
- Survey: "Privacy/data concerns" theme, 8 of 47 respondent mentions, verbatim "Where are recordings stored? Can I auto-delete after 30 days?" (06-user-feedback/feedback-q1-2026.md)

### 5. Price sensitivity for light/casual use - 2 of 3 sources
- Interviews: Priya Nair: "Fifteen dollars a month for something I use twice a week... it feels like a lot. If it were $8, I wouldn't think about it." She also calls the $49/seat Team plan "a non-starter" for her 45-person company (07-user-interviews/interview-03-priya-nair.md).
- Survey: "Too expensive for light use" theme, 7 of 47 respondent mentions, verbatim "I use it twice a week. $15/month doesn't feel worth it." (06-user-feedback/feedback-q1-2026.md)

### 6. Notion bundling threat to casual/free users - 2 of 3 sources
- Interviews: Priya Nair: "We live in Notion. Everything - docs, projects, OKRs. If Notion added meeting summaries that auto-posted into our meeting notes pages... honestly, I'd switch." (07-user-interviews/interview-03-priya-nair.md)
- Churn: "Notion AI is bundling meeting summary features free for existing Notion users. This directly threatens MeetFlow's free tier and casual users." (03-product-knowledge/company.md, Key Risks)

## Source-Specific Issues (1 source) - needs more investigation

- Passive usage / low feature adoption on large Team accounts - only in interviews (07-user-interviews/interview-02-marcus-okafor.md): Marcus Okafor says "Nobody reads the summaries... MeetFlow runs in the background - I forget it's there most days," and warns he will recommend against renewal for his 120-seat org. Worth investigating further because it is a direct renewal-risk signal on a large account, even though neither the survey nor the churn baseline corroborates it.
- Granola gaining among prosumer power users - only in churn source (03-product-knowledge/company.md, Key Risks): "Granola is gaining fast among prosumer power users with a Mac-native, beautifully designed experience." Worth investigating because it targets the same high-ARPU power-user segment (e.g. Sarah Chen) that the accuracy issue is already eroding trust with.
- Transcription accuracy drops in noisy environments (92% quiet-room only) - only in churn source (04-strategy/product-vision.md, Current Gaps to Close). Worth investigating because it is a named baseline gap the company is explicitly building Transcript Accuracy v2 to close in June 2026, even though no interview or survey respondent raised it directly in the files reviewed.
