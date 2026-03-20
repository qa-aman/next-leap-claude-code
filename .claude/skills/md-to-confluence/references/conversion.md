# Markdown to Confluence HTML Conversion Reference

## Full element mapping

| Markdown | Confluence HTML |
|---|---|
| `# H1` | `<h1>H1</h1>` |
| `## H2` | `<h2>H2</h2>` |
| `### H3` | `<h3>H3</h3>` |
| `**bold**` | `<strong>bold</strong>` |
| `*italic*` | `<em>italic</em>` |
| `~~strikethrough~~` | `<del>strikethrough</del>` |
| `` `inline code` `` | `<code>inline code</code>` |
| `[text](url)` | `<a href="url">text</a>` |
| `![alt](url)` | `<ac:image><ri:url ri:value="url"/></ac:image>` |
| `---` | `<hr/>` |
| `> blockquote` | `<blockquote><p>blockquote</p></blockquote>` |
| blank line | `</p><p>` (paragraph break) |

## Lists

Unordered:
```html
<ul>
  <li>item one</li>
  <li>item two</li>
</ul>
```

Ordered:
```html
<ol>
  <li>first</li>
  <li>second</li>
</ol>
```

Nested lists: wrap inner `<ul>` or `<ol>` inside the parent `<li>`.

## Code blocks

````markdown
```javascript
const x = 1;
const y = 2;
```
````

Converts to Confluence code macro:
```html
<ac:structured-macro ac:name="code">
  <ac:parameter ac:name="language">javascript</ac:parameter>
  <ac:parameter ac:name="theme">Confluence</ac:parameter>
  <ac:plain-text-body><![CDATA[const x = 1;
const y = 2;]]></ac:plain-text-body>
</ac:structured-macro>
```

Supported language values: `javascript`, `typescript`, `python`, `java`, `sql`, `bash`, `json`, `yaml`, `html`, `css`, `go`, `rust`. For unknown languages, omit the language parameter.

## Tables

Markdown:
```markdown
| Name | Role | Status |
|---|---|---|
| Aman | CPO | Active |
```

Confluence HTML:
```html
<table>
  <thead>
    <tr>
      <th>Name</th>
      <th>Role</th>
      <th>Status</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td>Aman</td>
      <td>CPO</td>
      <td>Active</td>
    </tr>
  </tbody>
</table>
```

## Info panels (use for blockquotes with keywords)

If a blockquote starts with `**Note:**`, `**Warning:**`, or `**Info:**`, convert to Confluence info macros:

```html
<!-- Note -->
<ac:structured-macro ac:name="note">
  <ac:rich-text-body><p>Note text here</p></ac:rich-text-body>
</ac:structured-macro>

<!-- Warning -->
<ac:structured-macro ac:name="warning">
  <ac:rich-text-body><p>Warning text here</p></ac:rich-text-body>
</ac:structured-macro>

<!-- Info -->
<ac:structured-macro ac:name="info">
  <ac:rich-text-body><p>Info text here</p></ac:rich-text-body>
</ac:structured-macro>
```

## Page body wrapper

Wrap the entire converted content in:
```html
<ac:layout>
  <ac:layout-section ac:type="single">
    <ac:layout-cell>
      <!-- all converted content here -->
    </ac:layout-cell>
  </ac:layout-section>
</ac:layout>
```

Or simply pass the raw HTML body without a layout wrapper — Confluence accepts both. Use the wrapper only if the existing page uses it.

## What to exclude

- The first `#` heading — becomes page title, not body content
- HTML comments `<!-- -->` — strip them
- Frontmatter `---` YAML blocks — strip entirely
- Empty lines at the start and end of the file
