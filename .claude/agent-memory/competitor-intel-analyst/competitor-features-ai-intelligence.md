---
name: competitor-features-ai-intelligence
description: Competitor feature state as of 13-06-2026 for AI Intelligence area: action items, summaries, pre-meeting briefs, AI chat, templates, conversation intelligence
metadata:
  type: project
---

Research date: 13-06-2026. All features from official sources only.

## Action Items

- **Notion AI**: Extracts action items with owner, priority, and due date fields. Pushes to Notion Agent tasks and existing Notion databases automatically. No confidence score or correction loop documented.
- **Granola**: Extracts action items from transcript. No structured fields (due date, priority) documented on official site.
- **Fireflies**: Pushes action items as Salesforce Tasks (via Salesforce integration). AI Skills can generate BANT, MEDDIC, and objection extraction reports.
- **Otter**: "Detect commitments made during calls and suggests next steps." Assigns action items per meeting.
- **Fathom**: AI-generated action items on Premium+ ($16/seat/month annual).
- **MeetFlow gap**: No due date or priority fields. No user correction feedback loop. 66% accuracy (top churn driver). Model retraining pipeline is manual and takes 2 weeks (per product.md).

## Summary Quality

- **Notion AI**: Meeting-type-aware summaries (7 types: 1:1, team sync, client call, interview, brainstorm, etc.). Instant generation post-meeting. 19 language support.
- **Granola**: User can ask AI to adjust tone, length, and precision post-generation via chat. 10 language support.
- **Fireflies**: AI Skills with 50+ pre-built and custom prompt templates. Scheduled execution per-meeting or recurring.
- **Fathom**: 15+ expert meeting templates including BANT and Sandler. 28-language summary translation.
- **MeetFlow gap**: Single 350-word average summary regardless of meeting type. "Too long" is top 2 complaint (per product.md). No template system.

## Pre-Meeting Briefing

- **Granola**: "Briefs" feature (shipped 20-05-2025): who you are meeting, what was discussed last time, open items. Available Mac and Windows.
- **Otter**: Pre-call briefing for Sales Agent: deal value, key decision makers, last interaction summary, AI talking points.
- **Notion AI, Fireflies, Fathom**: None documented.
- **MeetFlow gap**: No pre-meeting capability. Meeting Pattern Insights data (past transcripts, action items) already exists in beta - raw material for briefs is available.

## Cross-Meeting AI Chat

- **Granola**: Agentic Chat (rebuilt April 2025): faster cross-meeting queries, inline citations, Recipes (expert-written prompts). Spans Team Spaces.
- **Fireflies**: AskFred per-meeting and cross-meeting. AI credits metered.
- **Otter**: AI Chat across full meeting history. Business+ plan.
- **Fathom**: Ask Fathom per-call (Free, limited) and account-wide all calls (Premium+, unlimited).
- **Notion AI**: Enterprise Search across workspace + all meetings (Business plan).
- **MeetFlow gap**: Full-text search only. No conversational interface over meeting history.

## Conversation Intelligence / Meeting Analytics

- **Fireflies**: Full suite - sentiment analysis (positive/negative/neutral per meeting), topic frequency tracking, talk-time analytics, filler word detection, questions asked per speaker, longest monologue. Team coaching dashboard with rep performance over time.
- **Otter**: Real-time coaching during live calls (Sales Agent, Enterprise). Not available on standard plans.
- **MeetFlow**: Meeting Pattern Insights beta (800 users, 43% open rate): meeting load, talk-time ratios, recurring topics. No sentiment. No cross-team coaching dashboard.
- **Granola, Notion AI, Fathom**: None documented for conversation intelligence.

## MCP / Extensibility

- **Granola**: MCP integration shipping Feb 2025. Connects meeting notes to Claude, ChatGPT, Cursor. Also personal and enterprise API (Business tier).
- **Otter**: MCP server integration (recently shipped).
- **Fathom**: MCP integration, public API on all paid tiers.
- **Fireflies**: API on Business and Enterprise ($19+/seat/month).
- **MeetFlow gap**: No MCP, no public API documented in product files.
