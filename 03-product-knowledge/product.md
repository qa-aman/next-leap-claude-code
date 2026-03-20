# MeetFlow — Product Details

## Core Features

| Feature | Description | Status |
|---------|-------------|--------|
| Recording | Auto-join Zoom, Meet, Teams. Cloud recording with speaker labels | GA |
| Transcription | Real-time transcription, 92% accuracy (quiet environments) | GA |
| Smart Summaries | AI-generated meeting summaries with key decisions highlighted | GA |
| Action Items | Auto-extracted action items with assignee detection | GA |
| Integrations | Notion, Slack, Jira, Linear. Push summaries and action items | GA |
| Search | Full-text search across all meeting transcripts | GA |
| Meeting Pattern Insights | Weekly digest showing meeting load, talk-time ratios, recurring topics | Beta |

## AI Intelligence Pillar (Your Scope)

### Smart Summaries
AI-generated summaries that capture key decisions, discussion points, and context. Currently uses a fine-tuned model that produces summaries averaging 350 words per 30-minute meeting. User feedback says summaries are "too long" — the #2 complaint after action item accuracy.

### Action Item Confidence Scoring
Each extracted action item gets a confidence score (high/medium/low). The problem: 34% of action items are either wrong (assigned to the wrong person, misinterpreted as an action) or missing (real commitments that weren't captured). The confidence scoring model was trained on 50K labeled meetings but has accuracy gaps with:
- Implicit commitments ("I'll look into that")
- Multi-person action items
- Conditional actions ("If the data looks good, we'll ship it")

### Meeting Pattern Insights (Beta)
Weekly digest showing: total meeting hours, talk-time ratio per meeting, recurring agenda topics, suggested "meetings that could be emails." Currently in beta with 800 users. Engagement is moderate — 43% open rate on the weekly digest email.

## Current Sprint

**Action Item Confidence Scoring v2** — Research shows 34% of action items are wrong or missing. This sprint focuses on:
- Improving the extraction model for implicit commitments
- Adding "suggested action items" that users can confirm/dismiss
- Surfacing confidence scores more visibly in the UI (currently buried in a tooltip)

## Q2 2026 Roadmap

| Feature | Owner | Target |
|---------|-------|--------|
| Smart Follow-Up | You (AI Intelligence) | April 2026 |
| Salesforce Integration | Dana (Platform) | May 2026 |
| Enterprise Tier GA | Tomás (Enterprise) | June 2026 |
| Transcript Accuracy v2 | Aisha (Core) | June 2026 |

**Smart Follow-Up** — Draft follow-up emails after meetings using the summary and action items. Users review and edit before sending. Depends on Action Item Scoring v2 shipping first (garbage action items = garbage follow-ups).

## Tech Debt

- Transcript accuracy drops below 80% in noisy environments (coffee shops, open offices, poor mic quality)
- Speaker diarization fails for meetings with 8+ attendees — speakers get merged or misattributed
- Summary generation takes 45-90 seconds after meeting ends. Users expect near-instant
- Action item model retraining pipeline is manual. Takes 2 weeks to deploy a new model version
