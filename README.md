# Claude Code for PMs - Workshop Repo

Practice workspace for the "Claude Code for PMs" course at NextLeap's Applied GenAI Bootcamp. Built around **MeetFlow**, a fictional AI meeting assistant ($3M ARR, 15,000 users, Series B).

You play the role of a Senior PM owning the AI Intelligence pillar - Smart Summaries, Action Item Confidence Scoring, and Meeting Pattern Insights.

## Prerequisites

- [Claude Code](https://code.claude.com/docs/en/quickstart) installed
- Anthropic account with API access
- See `01-setup/` for Mac and Windows installation guides

## Setup

```bash
git clone https://github.com/qa-aman/next-leap-claude-code.git
cd next-leap-claude-code
claude
```

Then try: "What project is this and what's my role?"

## What's Inside

The repo follows the PM lifecycle from research to shipping. Each folder is a stage.

| Folder | Stage | What's inside |
|--------|-------|---------------|
| `01-setup/` | Setup | Mac and Windows install guides, Atlassian integration setup, guided prompts |
| `02-presentation/` | Workshop | Session slides (PPTX) and live Q&A reference |
| `03-product-knowledge/` | Understand | Company overview, product details, competitive landscape, tech stack |
| `04-strategy/` | Plan | Product vision, Q2 2026 OKRs |
| `05-user-personas/` | Research | Sarah Chen, Marcus Okafor, Priya Nair - three persona deep dives |
| `06-user-feedback/` | Research | Q1 2026 NPS survey results |
| `07-user-interviews/` | Research | 4 user interview transcripts |
| `08-product-features/` | Build | Smart Follow-Up PRD, change log, and user stories |
| `09-release-notes/` | Ship | Release notes for Smart Summaries v2.4 |
| `10-meetings/` | Communicate | Sprint planning, stakeholder sync, daily standup, and standup summary |
| `11-sprint/` | Execute | Sprint backlog and retrospective |
| `12-project-tracking/` | Track | Weekly status report with traffic-light format |
| `13-teams/` | Organize | Team structure and RACI chart |
| `14-templates/` | Reuse | 14 blank templates for every artifact type above |
| `outputs/` | Generate | Claude writes generated content here |

## Workshop Sessions

**Session 1: Understanding the Product** (2 hours)
- Set up Claude Code and CLAUDE.md
- Competitive analysis using real product data
- Cross-document research synthesis (the "wow" moment)
- Strategy and OKR validation

**Session 2: Building and Shipping** (2 hours)
- PRD walkthrough with source tracing
- Sprint planning and retro connections
- Status report generation
- Claude Code skills for repeatable workflows

## Try These Prompts

Start Claude Code (`claude`) in this directory, then try:

1. "What project is this and what's my role?"
2. "Read 03-product-knowledge/competitive.md and tell me where MeetFlow is most at risk"
3. "Read all files in 07-user-interviews/ and identify the top 3 user frustrations"
4. "Write a one-pager spec for the Smart Follow-Up feature"
5. "/feature-spec" (triggers the built-in skill)

## Key Files

- **CLAUDE.md** - Project context Claude reads every session. Start here.
- **.claude/rules/** - Path-specific rules that load automatically: `feature-writing`, `outputs`, `product-knowledge`, `prompt-writing`, `user-research`.
- **.claude/skills/** - 35+ PM skills covering the full lifecycle: discovery (`product-discovery`, `discovery-interview-prep`, `opportunity-solution-tree`), strategy (`okr-writer`, `product-thinking`, `competitive-analysis`, `prioritization`), specs (`write-prd`, `feature-spec`, `write-user-stories`, `epic-breakdown`, `spec-reviewer`, `technical-review`, `compliance-auditor`), delivery (`jira-ticket-creator`, `standup-summary`, `retro-synthesizer`, `risk-register`, `stakeholder-update`, `release-notes-writer`, `go-to-market-checklist`), and content (`ppt-builder`, `pptx-editor`, `flowchart`, `email-drafter`, `md-to-confluence`, `confluence-to-md`, `youtube-transcript`).
- **14-templates/** - Blank templates for every PM artifact in this repo.
- **02-presentation/q&a.md** - Curated Q&A from live workshop sessions.

## Integrations

This repo is pre-configured to work with:
- **Atlassian (Jira + Confluence)** - See `01-setup/integrations.md` for setup

## License

Workshop materials for educational use.
