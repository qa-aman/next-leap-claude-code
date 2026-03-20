---
name: md-to-confluence
description: Push local Markdown files to Confluence - create new pages or update existing ones. Use this skill whenever the user wants to publish, push, upload, sync, or create Confluence pages from .md files. Trigger on: "push to Confluence", "publish this spec to Confluence", "create Confluence page from this markdown", "update Confluence with this file", "sync md to Confluence", "upload spec to Confluence". Also trigger when the user says "create a page in Confluence" and there's a local file involved. Don't wait for an explicit skill request — if the intent is to get local Markdown content into Confluence, use this skill.
---

# Markdown to Confluence

Push a local `.md` file to Confluence. Creates the page if it doesn't exist, updates it if it does (upsert).

## Before starting - confirm 3 things

1. **Source file** - which `.md` file? (path)
2. **Target space** - which Confluence space key? (e.g. `BS`, `TECH`, `HR`)
3. **Parent page** - which page to nest under? (title or page ID)

If any are missing, ask before doing anything.

## Upsert logic

### Step 1 - determine the page title

The title is the first `#` heading in the file:
```markdown
# CRM Module - Product Specification   ← this becomes the page title
```

If no `#` heading exists, use the filename without `.md`.

### Step 2 - check if page exists

```
confluence_search(cql='title = "CRM Module - Product Specification" AND space = "BS" AND type = page')
```

- **Results found → update.** Show title + last modified date. Confirm: "Page exists (last updated: <date>). Update it?"
- **No results → create.** Notify: "Creating new page '<title>' under '<parent>' in space <KEY>."

### Step 3a - Update existing page

```
confluence_update_page(
  page_id="<id from search result>",
  title="<title>",
  body="<converted HTML>",
  version=<current_version + 1>
)
```

### Step 3b - Create new page

First get the parent page ID if only a title was given:
```
confluence_search(cql='title = "<parent title>" AND space = "BS" AND type = page')
```

Then:
```
confluence_create_page(
  space_key="BS",
  title="<title>",
  body="<converted HTML>",
  parent_id="<parent page id>"
)
```

## Markdown to Confluence HTML conversion

Confluence accepts HTML as the page body. See `references/conversion.md` for the full mapping.

Quick reference:

```
# Heading 1        →  <h1>Heading 1</h1>
## Heading 2       →  <h2>Heading 2</h2>
**bold**           →  <strong>bold</strong>
*italic*           →  <em>italic</em>
- item             →  <ul><li>item</li></ul>
1. item            →  <ol><li>item</li></ol>
`code`             →  <code>code</code>
[text](url)        →  <a href="url">text</a>
```

Code blocks:
````markdown
```javascript
const x = 1;
```
````
Becomes:
```html
<ac:structured-macro ac:name="code">
  <ac:parameter ac:name="language">javascript</ac:parameter>
  <ac:plain-text-body><![CDATA[const x = 1;]]></ac:plain-text-body>
</ac:structured-macro>
```

Tables: convert to `<table><tbody><tr><td>...</td></tr></tbody></table>`.

Strip the first `#` heading from the body - it becomes the page title, not content.

## Running the script directly

For bulk operations or automation, use the Python script instead of MCP calls:

```bash
# Install dependencies first (one time)
pip install requests markdown python-dotenv

# Single file
python scripts/md_to_confluence.py --file spec.md --space BS --parent "Product Specs"

# Bulk push
python scripts/md_to_confluence.py --files "foundation/**/*.md" --space BS --parent "Engineering Docs"

# Dry run (check what would happen without making changes)
python scripts/md_to_confluence.py --file spec.md --space BS --parent "Product Specs" --dry-run
```

Credentials are read from environment variables or `.env` file automatically.
See `scripts/md_to_confluence.py` for full usage.

## Token efficiency

Read the file once → convert → publish → done.

- Do not re-read the file after publishing
- Do not fetch the page back from Confluence to verify
- Trust the API response: HTTP 200/201 = success

## After publishing

Report:
- Page title
- Created or updated
- Direct Confluence URL (from API response)

Nothing else. Don't fetch or summarize content back.

## Bulk push

For multiple `.md` files:
- Confirm space and parent page applies to all, or ask per file
- Process one at a time, report status per file
- Don't stop on a single failure - complete all files, report failures at the end
