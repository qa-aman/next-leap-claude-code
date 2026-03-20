---
name: confluence-to-md
description: Fetch content from Confluence and save it as clean Markdown files locally. Use this skill whenever the user wants to pull, download, export, or sync Confluence pages to local .md files. Trigger on any of these: "fetch from Confluence", "download Confluence page", "convert Confluence to markdown", "pull this Confluence space", "get Confluence docs", "sync Confluence to local", "export Confluence page". Also trigger when the user pastes a Confluence URL and wants it saved as a file. Don't wait for the user to say "use confluence-to-md skill" — if Confluence content needs to land locally as Markdown, this skill applies.
---

# Confluence to Markdown

Fetch Confluence pages and save them as clean `.md` files locally. Strips HTML noise, macros, and metadata so the output is readable Markdown.

## Three modes

Identify which mode from the user's request:

### 1. Single page (URL or page ID)

Extract the page ID from a Confluence URL — it's the number in the path:
```
https://your-site.atlassian.net/wiki/spaces/BS/pages/123456789/Page+Title
                                                              ^^^^^^^^^
                                                              page ID
```

MCP call:
```
confluence_get_page(page_id="123456789")
```

Save as: `<SPACE>-<page-title-slugified>.md`

### 2. Full space (space key)

```
confluence_search(cql='space = "BS" AND type = page ORDER BY title ASC', limit=50)
```

Then fetch each page individually. Batch in groups of 5 — confirm with user after each batch before continuing.

Save into folder: `<SPACE-KEY>/`

### 3. Keyword search

```
confluence_search(cql='text ~ "voice companion" AND type = page', limit=10)
```

Show the user a numbered list of matching titles before fetching. Ask which ones to download. Never auto-fetch all search results.

## CQL reference

Common queries:
```
# All pages in a space
space = "BS" AND type = page

# Pages updated in the last 7 days
space = "BS" AND type = page AND lastModified >= "2026-03-07"

# Pages by a specific author
space = "BS" AND type = page AND creator = "user@example.com"

# Search by title
title ~ "CRM" AND type = page

# Search by content
text ~ "voice companion" AND type = page
```

## Conversion: what to keep, what to strip

For full conversion rules, see `references/conversion.md`.

Quick rules:
- Keep: headings, body text, lists, tables, code blocks, links
- Strip: Confluence macros, breadcrumbs, "Created by / Modified by" footers, HTML attributes, status badges, table of contents macros

## Running the script directly

For bulk operations or automation, use the Python script instead of relying on MCP calls:

```bash
# Install dependencies first (one time)
pip install requests beautifulsoup4 markdownify python-dotenv

# Single page
python scripts/confluence_to_md.py --mode single --page-id 123456789

# Full space
python scripts/confluence_to_md.py --mode space --space-key BS --output ./confluence-export

# Keyword search (interactive)
python scripts/confluence_to_md.py --mode search --query "voice companion"
```

Credentials are read from environment variables or `.env` file automatically.
See `scripts/confluence_to_md.py` for full usage.

## Token efficiency

This is important. The goal is to write files, not summarize content in chat.

1. Fetch page → convert immediately → write `.md` to disk
2. Do not hold raw HTML in context after conversion
3. Do not re-read the file back to confirm
4. Report success by filename only, not by content

For spaces with 20+ pages: process in batches of 5, confirm before each batch.

## Output naming

| Mode | Output |
|---|---|
| Single page | `<SPACE>-<slugified-title>.md` in current directory |
| Full space | `<SPACE-KEY>/` folder, one file per page |
| Search results | `confluence-export/` folder, slugified filenames |

Default save location: current working directory. Tell the user the exact path after saving.

## After saving

Report:
- Number of pages fetched
- File paths saved
- Any failures with reason

Do not summarize page content in chat.
