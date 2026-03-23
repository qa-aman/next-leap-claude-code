---
name: technical-review
description: Review a feature spec for technical readiness before engineering walkthrough. Use when the user says "review this spec", "technical review", "is this spec ready for eng", "prepare for eng walkthrough", "check my spec", "what will engineers ask", "validate this spec", or wants to ensure a feature spec covers all technical dimensions before presenting to engineering. Also trigger when a spec has been written and the user mentions "walkthrough", "handoff", or "ready for review".
---

# Technical Review

Review a MeetFlow feature spec and produce a checklist of what needs improvement before presenting to engineering.

## Why this exists

PMs lose credibility in eng walkthroughs when specs have technical blind spots. Engineers ask about data model changes, latency budgets, rollback plans, and monitoring - things PMs often skip. This skill catches those gaps before the meeting, not during it.

## How to use

1. Read the spec file the user provides.
2. Read the MeetFlow product context (`03-product-knowledge/product.md` and `03-product-knowledge/company.md`) to ground the review in the actual system.
3. Run the spec through every checklist category below.
4. Output a single checklist with pass/fail per item and specific improvement notes for failures.

## Output format

```markdown
# Technical Review: [Spec Title]

**Reviewed:** [date]
**Verdict:** [Ready / Needs Work / Major Gaps]

## Checklist

### [Category Name]
- [x] Item that passes
- [ ] **Item that fails** - [specific note on what's missing and what to add]

### [Next Category]
...

## Top 5 Engineer Questions You'll Get
1. [Question] - **Suggested answer:** [based on spec content or flag as gap]

## Summary
[2-3 sentences: what's strong, what's the biggest gap, recommended next step]
```

Verdict logic:
- **Ready**: All items pass, or failures are minor and non-blocking
- **Needs Work**: 3+ failures across categories, but core architecture is addressed
- **Major Gaps**: Missing entire categories or fundamental technical decisions unaddressed

## Checklist categories

### 1. Spec Structure (basics)
- Problem statement exists and cites real data (numbers from MeetFlow files, not invented)
- Users affected are named personas with specific impact described
- Success metrics have baselines AND targets from existing files
- Out of scope section exists and is specific (not vague)
- Open questions have owners and due dates

### 2. MeetFlow Architecture Impact
Review against MeetFlow's known architecture (from `03-product-knowledge/product.md`):
- Does this touch the **transcription pipeline**? If yes, does the spec address the 92% accuracy baseline and noisy environment degradation?
- Does this touch the **action item extraction model** (trained on 50K labeled meetings)? If yes, does it specify fine-tuning vs retraining, and address the three known gaps (implicit commitments, multi-person items, conditional actions)?
- Does this touch **summary generation** (avg 350 words/30-min meeting, 45-90 sec generation time)? If yes, does it address latency impact?
- Does this touch **integrations** (Slack, Notion, Jira, Linear)? If yes, does it specify what data flows to each integration and any format changes?
- Does this touch **speaker diarization**? If yes, does it address the known 8+ attendee failure mode?
- Does this require **model retraining**? If yes, does it account for the current 2-week manual deployment cycle?

### 3. Data and ML Considerations
- Training data requirements specified (what data, how much, where it comes from)
- Model accuracy targets defined with measurement methodology
- Feedback loop described (how user actions improve the model over time)
- Data privacy implications addressed (especially for enterprise/Team plan users - Marcus Okafor's concerns from `07-user-interviews/interview-02-marcus-okafor.md`)
- A/B testing or rollout strategy mentioned (not just "ship it")

### 4. Performance and Scale
- Latency budget specified (with comparison to current baselines from product.md)
- Impact on meeting-end processing time addressed (users expect near-instant)
- Scale considerations for power users (Sarah Chen: 8-10 meetings/day)
- Back-to-back meeting handling addressed (no cross-contamination)
- Concurrent meeting processing if relevant

### 5. Error Handling and Edge Cases
- What happens when the feature fails? (graceful degradation, not just happy path)
- Empty states defined (no results, no data, first-time use)
- Edge cases for meeting types: short meetings (<5 min), large meetings (8+ attendees), poor audio quality
- Retry/timeout behavior specified
- Does the spec address what happens during the transition period (old behavior to new)?

### 6. Dependencies and Sequencing
- Upstream dependencies identified (what must ship first?)
- Downstream dependencies noted (what breaks or blocks if this is late?)
- Cross-pillar dependencies flagged:
  - Platform & Integrations (Dana Rivera)
  - Enterprise & Security (Tomas Herrera)
  - Core Experience (Aisha Patel)
- Timeline feasibility: does the spec acknowledge the Q2 2026 roadmap constraints?

### 7. Observability and Rollback
- How will engineering know if this is working in production? (metrics, dashboards, alerts)
- What signals indicate the feature should be rolled back?
- Can this be feature-flagged for gradual rollout?
- Logging requirements for debugging (especially for ML model outputs)

### 8. Tier and Access Control
- Which plans get this feature? (Free / Pro / Team / Enterprise)
- If tiered, how does the experience degrade for lower tiers?
- Any implications for the upcoming Enterprise tier GA (June 2026)?

## Engineer questions

After the checklist, generate the top 5 questions engineers are most likely to ask during the walkthrough. Focus on:

- Architecture decisions that aren't explained
- "Why not X?" alternatives the spec doesn't address
- Scale/performance concerns specific to MeetFlow's user patterns
- Data model changes that ripple through the system
- Timeline feasibility given known tech debt

For each question, provide a suggested answer if the spec contains enough information, or flag it as a gap the PM needs to resolve.

## Grounding rules

- Only cite numbers that appear in MeetFlow's files. Never invent metrics.
- Reference the specific file when flagging a gap (e.g., "product.md mentions X but your spec doesn't address it").
- Be direct. "This is missing" is better than "you might want to consider adding."
- Don't pad the checklist with trivial passes. If everything in a category passes, say so in one line and move on.
