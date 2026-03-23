# Jira Attention - Skill Design Spec

## Overview

A Claude Code skill (`/jira-attention`) that surfaces all Jira tickets where the PM is tagged, mentioned, or needs to provide input. For each ticket, it gathers local project context, drafts a ready-to-post Jira comment, and posts approved comments via the Jira Cloud REST API.

## Trigger

On-demand via `/jira-attention`. No scheduled/automated runs.

## Authentication

Reuses existing Atlassian credentials from the Confluence skill setup:

| Variable | Purpose | Default |
|----------|---------|---------|
| `CONFLUENCE_API_TOKEN` | Atlassian API token (works for both Confluence and Jira) | Required |
| `CONFLUENCE_USERNAME` | Atlassian account email | Required |
| `JIRA_BASE_URL` | Jira Cloud instance URL | `https://createswithap.atlassian.net` (user-specific default) |

Fail fast with setup instructions if any are missing.

## Ticket Discovery

JQL query against Jira Cloud REST API (`/rest/api/3/search`):

```
(assignee = currentUser() OR mention = currentUser() OR watcher = currentUser())
AND status != Done
AND updated >= -7d
ORDER BY updated DESC
```

Catches three signals:
- Tickets assigned to you
- Tickets where someone mentioned you in a comment
- Tickets you're watching

**Constraints:**
- Max 15 tickets per run
- Only open/in-progress tickets updated in the last 7 days
- Fetches per ticket: key, summary, description, status, priority, last 5 comments, reporter, assignee, labels, linked issues

## Local Context Matching

For each ticket, extract 3-5 key terms from the summary, description, and latest comments. Search local project directories for matching files.

**Search targets (priority order):**

1. `08-product-features/` - PRDs, specs, user stories
2. `03-product-knowledge/` - company, product, competitive intel
3. `04-strategy/` - vision, OKRs, roadmap
4. `07-user-interviews/` - interview transcripts
5. `06-user-feedback/` - survey data
6. `10-meetings/` - meeting notes
7. `outputs/` - generated specs and reviews

**Matching logic:**
- Extract key terms from ticket content (feature names, product areas, user-facing concepts)
- Grep across target directories for matches
- Read top 3 matched files per ticket (capped to control token usage)
- If no local match found, draft comment using only Jira ticket context

## Comment Drafting

Each drafted comment follows this structure:

1. **Context acknowledgment** - brief reference to what was asked or why you were tagged
2. **PM input** - the actual response, grounded in data from matched local files (cites source file where possible)
3. **Next steps** - clear action items or decisions, with owners if identifiable

Tone: direct, specific, no filler. Matches the user's writing style preferences (no em dashes, no corporate speak, short paragraphs).

## Output Presentation

```
## Tickets Needing Your Input (N found)

### 1. MEET-234: Action item confidence threshold
Status: In Review | Tagged by: Dana Rivera | 2 days ago
Context: 08-product-features/action-item-scoring-prd.md
---
Draft comment:
> [the drafted comment]
---
[Post] [Skip] [Edit]

### 2. MEET-301: Salesforce field mapping
...
```

**Interaction per ticket:**
- **Post** - approve and post the comment as-is
- **Skip** - do not post, move to next ticket
- **Edit** - present the draft as editable text. User modifies inline and confirms. The modified text is what gets posted.

Nothing posts without explicit approval.

## Posting

Approved comments posted via `POST /rest/api/3/issue/{issueIdOrKey}/comment` (v3 endpoint) with Atlassian Document Format (ADF) body.

**Minimum ADF structure:**

```json
{
  "body": {
    "type": "doc",
    "version": 1,
    "content": [
      {
        "type": "paragraph",
        "content": [{ "type": "text", "text": "First paragraph" }]
      },
      {
        "type": "paragraph",
        "content": [{ "type": "text", "text": "Second paragraph" }]
      }
    ]
  }
}
```

Multi-paragraph comments use multiple `paragraph` nodes, not `\n` characters.

## End-to-End Flow

```
1. Validate auth (CONFLUENCE_API_TOKEN, CONFLUENCE_USERNAME, JIRA_BASE_URL)
       |
2. Run JQL query -> fetch up to 15 open tickets
       |
3. For each ticket:
   a. Extract keywords from summary + description + recent comments
   b. Grep local project dirs for matching files
   c. Read top 3 matched files
   d. Draft comment (context + PM input + next steps)
       |
4. Present all drafts with [Post] [Skip] [Edit] per ticket
       |
5. Post approved comments via Jira REST API
       |
6. Summary: "Posted X/Y comments. Skipped: [ticket keys]."
```

## Error Handling

| Scenario | Behavior |
|----------|----------|
| Auth env vars missing | Fail fast with setup instructions |
| API rate limit (429) | Read `Retry-After` response header, wait that duration, retry once. If retry also fails, report error and continue. |
| No tickets found | "No tickets needing your attention in the last 7 days." |
| No local context match | Draft from Jira context only, flag "no local context found" |
| Comment post fails | Report error per ticket, continue with remaining |

## Constraints

- Max 15 tickets per invocation
- Max 3 local files read per ticket
- 7-day lookback window
- No comments posted without explicit user approval
