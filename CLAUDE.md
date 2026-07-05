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
| `15-prototype/` | Runnable Next.js 14 prototype of the MeetFlow UI (the "ux-zone"). The only executable code in the repo. |
| `16-zomato/` | A second `ux-zone` prototype variant plus its build-prompt chain. |
| `outputs/` | Write all generated content here |

## Prototype (the only runnable code)

`15-prototype/` is a Next.js 14 App Router app (React 18, Tailwind 3, TypeScript). Everything else in the repo is Markdown/PPTX content. Run commands from inside `15-prototype/`:

- `npm run dev` - local dev server
- `npm run build` - production build
- `npm run typecheck` - `tsc --noEmit`, the fastest correctness gate; run this after editing any `.tsx`
- `npm run start` - serve the production build

There is no test runner or linter wired up; `typecheck` is the check to run before considering a UI change done. When touching prototype UI, the `.claude/rules/ui-design-quality.md` rules auto-load and are binding (they encode real bugs that shipped - invisible ghost buttons, buttons overflowing card borders).

## Claude Code Infrastructure (`.claude/`)

This repo is also a live Claude Code toolkit. Before hand-rolling a PM artifact, check whether a skill or agent already does it.

- **`.claude/skills/`** (40+ skills) - PM deliverable generators: `write-prd`, `feature-spec`, `okr-writer`, `prioritization`, `write-user-stories`, `stakeholder-update`, `jira-ticket-creator`, `mom` (Smart Brevity meeting minutes), plus publishing skills (`md-to-confluence`, `ppt-builder`) and writing skills. Invoke with `/<skill-name>`.
- **`.claude/agents/`** - specialized subagents: `pm-request-router` (triages vague requests), `prd-drafter` / `prd-quality-loop` / `prd-critic` (PRD pipeline), `churn-diagnoser`, `interview-insight-synthesizer`, `competitor-snapshot`, `feedback-triangulator`, `senior-code-reviewer`. Prefer these over ad-hoc work for their domains.
- **`.claude/rules/`** - path-triggered rules that auto-load when you touch matching files. Know these fire without being asked:
  - `08-product-features/**` -> PRDs must cite a persona, use real baselines, include a "What we're NOT building" section, link to Q2 OKRs.
  - `03-product-knowledge/**`, `05/06/07-*` -> cite source file/line for every metric and quote; never invent numbers or user quotes.
  - `outputs/**` -> short sentences, no unexplained jargon, cross-reference source files.
  - `15-prototype/**` (and any `ux-zone`/`prototype` `.tsx`) -> the UI design-quality rules above.
  - `outputs/*prompt*.md`, `prompts/**` -> the prompt-writing rubric (self-score >95 before delivering).

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
