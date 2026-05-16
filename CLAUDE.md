# MeetFlow — Claude Code Workshop

## Project Identity

**MeetFlow** is an AI-powered meeting assistant SaaS. Series B ($18M from Benchmark, April 2025), $3M ARR, 15,000 active users.

You are a **Senior Product Manager** owning the **AI Intelligence pillar** - Smart Summaries, Action Item Confidence Scoring, and Meeting Pattern Insights.

## What This Repo Is

Workshop workspace for the "Claude Code for PMs" course. It contains realistic product context, user research, and competitive intelligence for MeetFlow. Use it to practice Claude Code workflows.

## Key Context (Always Loaded)

@03-product-knowledge/company.md
@04-strategy/product-vision.md

## File Map

| Directory | What's inside |
|-----------|--------------|
| `01-setup/` | Claude Code installation guides for Mac and Windows |
| `02-presentation/` | Session slides (PPTX) |
| `03-product-knowledge/` | Product context - company overview, product details, competitive landscape |
| `04-strategy/` | Product vision, OKRs, and roadmap priorities |
| `05-user-personas/` | Individual persona deep dives (Sarah Chen, Marcus Okafor, Priya Nair) |
| `06-user-feedback/` | Aggregated Q1 2026 feedback survey |
| `07-user-interviews/` | User interviews (4 transcripts) |
| `08-product-features/` | PRDs, feature specs, and user stories |
| `09-release-notes/` | Release notes for shipped features |
| `10-meetings/` | Meeting notes - sprint planning, stakeholder syncs |
| `11-sprint/` | Sprint backlog and retrospectives |
| `12-project-tracking/` | Weekly status reports and project tracking |
| `13-teams/` | Team structure and RACI for key features |
| `14-templates/` | Reusable PM artifact templates (PRDs, OKRs, retros, status reports, etc.) |
| `outputs/` | Write all generated content here |

## Rules

- No invented metrics. Use only numbers that appear in the files.
- Cite which file a number or quote came from.
- Ask before writing more than 500 words.
- Path-specific rules live in `.claude/rules/` and load automatically when working with matching files.
- When the user asks to "create a prompt", "write a prompt", "draft a prompt", or "review a prompt", read `.claude/rules/prompt-writing.md` first and apply its rubric. Self-score to >95/100 before delivering. Do not dispatch a subagent for review.

## Time Convention

This workshop is set in a fictional "now" of **17-03-2026**.

- All dates across the repo (sprint dates, launch dates, OKR quarters, feedback timestamps, meeting notes) are anchored to this fictional today.
- When reasoning about "current", "today", "upcoming", "this sprint", or "next quarter", use **17-03-2026** as today, not the real system date or any date from memory.
- Concrete anchors that follow from this:
  - Active sprint: 17-03-2026 to 28-03-2026 (Action Item Confidence Scoring v2)
  - Smart Follow-Up launch: April 2026 (~3 weeks out)
  - Salesforce integration: May 2026 (~7 weeks out)
  - Enterprise Tier GA + Transcript Accuracy v2: June 2026 (~12 weeks out)
  - Q1 2026 feedback survey is a historical artifact, not "recent" beyond the anchor.
- **Refresh recipe for future cohorts:** to make the repo feel fresh for a new session, change only the anchor date above and update the four concrete anchors above proportionally. Do not rewrite individual docs - the relative framing handles it.
- Date format everywhere is DD-MM-YYYY.

## Quick Tasks

Try these prompts to explore the workspace:

1. **Orientation:** "What project is this and what's my role?"
2. **Competitive analysis:** "Read 03-product-knowledge/competitive.md and tell me where MeetFlow is most at risk"
3. **Research synthesis:** "Read all files in 07-user-interviews/ and identify the top 3 user frustrations"
4. **Feature spec:** "Write a one-pager spec for the Smart Follow-Up feature"
