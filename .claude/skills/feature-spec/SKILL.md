---
name: feature-spec
description: Write a concise feature spec (one-pager) for engineering handoff. Use when user says "write a spec", "one-pager", "feature spec", "spec this out", "spec for [feature name]", or wants a structured feature brief grounded in product context and user research.
---

# Feature Spec Generator

Write concise, research-grounded feature specs for MeetFlow. Every spec is rooted in real product context and user data - no invented metrics, no generic templates.

## When to Activate

- User asks to "write a spec", "one-pager", or "feature spec"
- User wants to document a feature idea for engineering handoff
- User says "spec this out" or "spec for [feature name]"

## How It Works

### Step 1: Gather context
Read the following files before writing anything:
- `03-product-knowledge/product.md` - current features, roadmap, tech debt
- `03-product-knowledge/competitive.md` - how competitors handle this
- `03-product-knowledge/company.md` - business snapshot, team, priorities
- `04-strategy/okrs-q2-2026.md` - current quarter goals
- `05-user-personas/` - individual persona files (sarah-chen.md, marcus-okafor.md, priya-nair.md)
- `06-user-feedback/feedback-q1-2026.md` - survey data and complaints
- `07-user-interviews/` - all interview transcripts

### Step 2: Write the spec
Use this exact output format:

```
# [Feature Name] - Feature Spec

**Author:** [PM name]
**Date:** [today]
**Status:** Draft

---

## Problem
What user problem does this solve? Cite specific data from research files.
2-3 sentences max.

## Users Affected
Which personas are impacted? Reference files in `05-user-personas/`.
Include estimated user count or segment size from `03-product-knowledge/company.md`.

## Proposed Solution
What are we building? Be specific about the user experience.
3-5 sentences describing the feature behavior.

## Success Metrics
How will we measure if this worked? 2-4 metrics.
Use real baseline numbers from the files (NPS, error rates, usage stats).
Connect to OKRs in `04-strategy/okrs-q2-2026.md`.

## Out of Scope
What are we explicitly NOT doing in v1? 2-4 items.
This prevents scope creep and sets expectations.

## Open Questions
What do we still need to figure out? 2-4 questions.
Include technical dependencies, research gaps, or stakeholder decisions needed.
```

### Step 3: Apply rules
- No invented metrics. Every number must come from a file in this repo.
- Cite sources: "(Source: 06-user-feedback/feedback-q1-2026.md)" or "(Source: 03-product-knowledge/product.md)"
- Keep the total spec under 600 words.
- Flag dependencies on other features or teams.
- If the feature connects to a known user pain point, lead with that data.

### Step 4: Save output
Write the spec to `outputs/[feature-name]-spec.md` unless the user specifies a different location.

## Quality Checklist

Before delivering, verify:
- [ ] Problem section cites specific research data
- [ ] Users Affected references actual personas by name with file paths
- [ ] Success Metrics use real baseline numbers from the files
- [ ] Success Metrics connect to Q2 OKRs
- [ ] Out of Scope is specific, not vague
- [ ] Total word count is under 600
- [ ] All numbers are traceable to source files
- [ ] Dependencies are flagged

## Worked Example

Here's what a good spec looks like for the Smart Follow-Up feature:

---

# Smart Follow-Up - Feature Spec

**Author:** Aman Parmar
**Date:** 2026-03-16
**Status:** Draft

---

## Problem
After meetings, participants spend 10-15 minutes drafting follow-up emails summarizing decisions and next steps. For sales teams, this is 10+ hours of daily admin across a 15-person team (Source: 07-user-interviews/interview-04-james-whitfield.md). MeetFlow already captures summaries and action items - but doesn't help users act on them.

## Users Affected
- **Sarah Chen (Power User)** - 8-10 meetings/day, would use follow-ups for every external meeting (see `05-user-personas/sarah-chen.md`)
- **James Whitfield (Sales Director)** - 15-person sales team, 4-5 prospect calls/day each. Highest time savings potential (see `07-user-interviews/interview-04-james-whitfield.md`)
- Estimated impact: 2,800 Pro users + 200 Team accounts (Source: 03-product-knowledge/company.md)

## Proposed Solution
After a meeting ends and the summary generates, MeetFlow drafts a follow-up email using the meeting summary and action items. The draft appears in a "Follow-Up" tab within the meeting detail page. Users review, edit, and send directly from MeetFlow or copy to their email client. The email includes: greeting, key decisions recap, action items with owners and deadlines, and a closing.

## Success Metrics
- Follow-up draft usage rate: target 40% of meetings (baseline: 0%, new feature)
- Time-to-follow-up: reduce from estimated 10-15 min to under 2 min
- Action item accuracy in follow-ups: must match Action Item Scoring v2 targets (reduce 34% error rate to under 15%) (Source: 03-product-knowledge/product.md)
- NPS impact: target 5-point lift in Pro segment (baseline: 29, Source: 06-user-feedback/feedback-q1-2026.md)

## Out of Scope
- Direct email sending (v1 is draft + copy only, no SMTP integration)
- Calendar integration for scheduling follow-up meetings
- Multi-language follow-ups (English only in v1)
- Automated follow-up sequences (no drip campaigns)

## Open Questions
- Dependency: Does Action Item Scoring v2 need to ship first? If follow-ups are built on inaccurate action items, the feature amplifies errors rather than saving time (Source: 07-user-interviews/interview-01-sarah-chen.md - "confidence score says 'high' but misses the most important item")
- Should follow-ups be available on Free tier or Pro+ only?
- What's the right default tone? Professional, casual, or configurable?
- Does James's team need CRM integration for follow-ups, or is copy-to-clipboard sufficient for v1?

---

## Anti-Patterns

Do NOT:
- Invent user quotes or metrics that aren't in the research files
- Write vague success metrics like "improve user satisfaction"
- Include implementation details or technical architecture
- Exceed 600 words - if you need more space, the scope is too broad
- Skip the Out of Scope section - this is where scope creep starts
