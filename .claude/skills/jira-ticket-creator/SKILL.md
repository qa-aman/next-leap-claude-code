---
name: jira-ticket-creator
description: |
  Create Jira tickets from meeting notes, user stories, or quick lists. Use this skill when:
  - User says "create tickets", "make Jira tickets from", "push to Jira"
  - User has meeting action items to convert to tickets
  - User has user stories from a spec to push to the backlog
  - User wants to batch-create tasks, stories, or bugs
---

# Jira Ticket Creator

Parse any input into structured Jira tickets. Works with meeting action items, user stories from specs, or free-text lists.

## Input Sources

- Meeting action items
- User stories from spec files
- Free-text lists ("Create tickets for: X, Y, Z")
- Sprint planning output

## Field Mapping

| Field | Source | Default |
|-------|--------|---------|
| Summary | First line or action item text | Required |
| Description | Context, acceptance criteria if available | Empty |
| Type | Infer from content | Story |
| Priority | From context | Medium |
| Story Points | Estimate from complexity | Blank |
| Assignee | Match name to team directory | Unassigned |
| Epic | Link if specified in input | None |
| Sprint | Specified or current sprint | Current |

**Type inference:**
- Contains "bug", "fix", "broken", "error" -> Bug
- Contains "investigate", "research", "spike" -> Task
- Everything else -> Story

## User Story Format

When the ticket is a **Story** (or the user asks to "create a user story"), the description MUST follow this exact structure. Do not use bare "As a user..." one-liners for stories.

**Title** (the ticket summary):
`As a [role], I want [capability] so that [benefit]`

**Description body** (three labeled sections, in this order):

1. **Problem Statement** — the current state and why it is a problem. Name the specific gap, the affected surface, and the business or UX cost (missed monetization, fragmented experience, lost conversions). Ground it in real context, no filler.
2. **Objective** — what will be implemented and the intended outcome. One tight paragraph: the change, the mechanism (e.g. backend mappings, entity type), and the result it drives (consistency, engagement, conversions).

Acceptance criteria are optional but, when present, go under a third **Acceptance Criteria** bullet list after Objective.

### Reference example

> **Title:** As a user, I want to see relevant sticky CTA ads on news detail pages so that I can easily take action based on the content I am consuming
>
> **Problem Statement**
> Currently, predefined ad types such as sticky strip ads are not being shown on news detail pages, despite these pages being one of the highest traffic drivers on the website. This leads to missed monetization and conversion opportunities. Additionally, inconsistent CTA behavior across different entities (exam, college, others) results in a fragmented user experience.
>
> **Objective**
> To implement sticky strip ads on news detail pages with dynamic CTA behavior based on backend mappings and entity type, ensuring consistency, improved engagement, and maximized conversions.

## Workflow

1. **Parse** — extract individual ticket items from input
2. **Enrich** — add type, priority, assignee, epic from context
3. **Present** — show ticket table to user for confirmation
4. **Confirm** — user reviews, edits, approves
5. **Create** — create tickets via Jira REST API
6. **Log** — report created tickets with keys

## Confirmation Format

```
| # | Summary | Type | Priority | Assignee | Points | Epic |
|---|---------|------|----------|----------|--------|------|
| 1 | Implement feature X | Story | High | [name] | 5 | [Epic] |
| 2 | Fix login bug | Bug | Medium | [name] | 1 | [Epic] |

Total: 2 tickets, 6 story points
Proceed? (y/n/edit)
```

## Rules

- Maximum 15 tickets per batch (split larger lists)
- Always confirm before creating
- Show total story points in confirmation

## Anti-Patterns

- Don't create tickets without user confirmation
- Don't guess assignees — ask if unclear
- Don't create more than 15 tickets at once

## Quality Checklist

- [ ] Every ticket has a clear summary
- [ ] Type correctly inferred or specified
- [ ] Stories use the User Story Format: "As a [role]... so that [benefit]" title + Problem Statement + Objective
- [ ] User confirmed before creation
- [ ] Total story points shown
