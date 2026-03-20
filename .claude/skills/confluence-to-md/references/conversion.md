# Confluence HTML to Markdown Conversion Reference

## Element mapping

| Confluence / HTML | Markdown output |
|---|---|
| `<h1>`, `<h2>`, `<h3>` | `#`, `##`, `###` |
| `<strong>`, `<b>` | `**text**` |
| `<em>`, `<i>` | `*text*` |
| `<ul><li>` | `- item` |
| `<ol><li>` | `1. item` |
| `<a href="url">text</a>` | `[text](url)` |
| `<code>` inline | `` `code` `` |
| `<pre>` / code block macro | ` ```lang\ncode\n``` ` |
| `<table>` | Markdown table |
| `<hr>` | `---` |
| `<br>` | blank line |
| `<p>` | blank line between paragraphs |

## Confluence macros - what to do

| Macro | Action |
|---|---|
| `{toc}` / Table of contents | Remove entirely |
| `{info}`, `{note}`, `{warning}` | Keep text content, remove macro wrapper. Add `> **Note:**` prefix |
| `{code}` | Convert to fenced code block with language tag |
| `{status}` | Replace with plain text label in brackets e.g. `[IN PROGRESS]` |
| `{jira}` issue link | Keep as plain text: `JIRA-123` |
| `{excerpt}` | Keep text, remove macro wrapper |
| `{expand}` | Keep text, add `> ` blockquote prefix |
| `{children}` / page tree | Remove entirely |
| `{recently-updated}` | Remove entirely |
| Image macros | Replace with `![alt](filename)` if image URL is available, otherwise `[image: filename]` |

## Strip entirely

- Page breadcrumb navigation
- "Created by X on date / Modified by Y on date" footers
- Confluence page labels/tags section
- "Liked by X people" sections
- Comment sections
- Page restriction notices
- HTML attributes (`class`, `id`, `data-*`, `style`)
- Confluence-specific HTML like `<ac:structured-macro>` wrappers (keep inner text)

## Tables

Convert HTML tables to Markdown pipe tables:
```markdown
| Column 1 | Column 2 | Column 3 |
|---|---|---|
| row 1    | data     | data     |
| row 2    | data     | data     |
```

For complex tables with merged cells: simplify to flat rows. Note "merged cells simplified" in a comment above the table.

## Code blocks

Confluence code macro format:
```html
<ac:structured-macro ac:name="code">
  <ac:parameter ac:name="language">javascript</ac:parameter>
  <ac:plain-text-body><![CDATA[const x = 1;]]></ac:plain-text-body>
</ac:structured-macro>
```

Converts to:
````markdown
```javascript
const x = 1;
```
````

If language is missing, use ` ``` ` without a language tag.

## File naming (slugify rules)

- Lowercase everything
- Replace spaces with hyphens
- Remove special characters except hyphens and underscores
- Trim leading/trailing hyphens
- Max 80 characters

Examples:
- `CRM Module - Product Specification` → `crm-module-product-specification`
- `API Gateway (v2.0)` → `api-gateway-v20`
- `Q&A / FAQ Page` → `qa-faq-page`
