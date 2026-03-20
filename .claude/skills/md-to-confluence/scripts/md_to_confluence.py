#!/usr/bin/env python3
"""
md_to_confluence.py - Push local Markdown files to Confluence (upsert).

Creates the page if it doesn't exist, updates it if it does.
The page title is taken from the first # heading in the file.

Usage:
  # Single file
  python md_to_confluence.py --file spec.md --space BS --parent "Product Specs"

  # Single file with explicit parent page ID
  python md_to_confluence.py --file spec.md --space BS --parent-id 987654321

  # Bulk push (multiple files)
  python md_to_confluence.py --files "*.md" --space BS --parent "Product Specs"

  # Dry run (show what would happen without making changes)
  python md_to_confluence.py --file spec.md --space BS --parent "Product Specs" --dry-run

Credentials (in order of precedence):
  1. CLI flags: --confluence-url, --username, --token
  2. Environment variables: CONFLUENCE_URL, CONFLUENCE_USERNAME, CONFLUENCE_API_TOKEN
  3. .env file in current directory

Dependencies:
  pip install requests markdown python-dotenv
"""

import os
import re
import sys
import argparse
import requests
from pathlib import Path

# Load .env if present
try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    pass

try:
    import markdown as md_lib
    HAS_MARKDOWN = True
except ImportError:
    HAS_MARKDOWN = False


# ---------------------------------------------------------------------------
# Confluence REST API client
# ---------------------------------------------------------------------------

class ConfluenceClient:
    def __init__(self, base_url: str, username: str, token: str):
        self.base_url = base_url.rstrip("/")
        self.session = requests.Session()
        self.session.auth = (username, token)
        self.session.headers.update({
            "Accept": "application/json",
            "Content-Type": "application/json",
        })

    def find_page(self, title: str, space_key: str) -> dict | None:
        """Return page metadata if a page with this exact title exists, else None."""
        url = f"{self.base_url}/wiki/rest/api/content/search"
        escaped = title.replace('"', '\\"')
        cql = f'title = "{escaped}" AND space = "{space_key}" AND type = page'
        resp = self.session.get(url, params={"cql": cql, "expand": "version"})
        resp.raise_for_status()
        results = resp.json().get("results", [])
        return results[0] if results else None

    def find_page_by_title(self, title: str, space_key: str) -> dict | None:
        """Find a page by title to use as parent. Returns page metadata."""
        return self.find_page(title, space_key)

    def create_page(self, space_key: str, title: str, body_html: str,
                    parent_id: str | None = None) -> dict:
        url = f"{self.base_url}/wiki/rest/api/content"
        payload = {
            "type": "page",
            "title": title,
            "space": {"key": space_key},
            "body": {
                "storage": {
                    "value": body_html,
                    "representation": "storage",
                }
            },
        }
        if parent_id:
            payload["ancestors"] = [{"id": parent_id}]

        resp = self.session.post(url, json=payload)
        resp.raise_for_status()
        return resp.json()

    def update_page(self, page_id: str, title: str, body_html: str,
                    current_version: int) -> dict:
        url = f"{self.base_url}/wiki/rest/api/content/{page_id}"
        payload = {
            "type": "page",
            "title": title,
            "version": {"number": current_version + 1},
            "body": {
                "storage": {
                    "value": body_html,
                    "representation": "storage",
                }
            },
        }
        resp = self.session.put(url, json=payload)
        resp.raise_for_status()
        return resp.json()

    def page_url(self, page_data: dict) -> str:
        return self.base_url + page_data.get("_links", {}).get("webui", "")


# ---------------------------------------------------------------------------
# Markdown → Confluence HTML converter
# ---------------------------------------------------------------------------

def extract_title(content: str) -> tuple[str, str]:
    """Extract title from first # heading. Returns (title, body_without_title)."""
    lines = content.splitlines()
    title = ""
    body_lines = []
    title_found = False

    for line in lines:
        if not title_found and line.startswith("# "):
            title = line[2:].strip()
            title_found = True
        else:
            body_lines.append(line)

    body = "\n".join(body_lines).strip()
    return title, body


def strip_frontmatter(content: str) -> str:
    """Remove YAML frontmatter (--- ... ---) from the top of the file."""
    if content.startswith("---"):
        end = content.find("\n---", 3)
        if end != -1:
            return content[end + 4:].strip()
    return content


def convert_markdown_to_confluence_html(markdown_text: str) -> str:
    """Convert Markdown to Confluence storage format HTML."""
    if HAS_MARKDOWN:
        html = md_lib.markdown(
            markdown_text,
            extensions=["tables", "fenced_code", "nl2br", "sane_lists"],
        )
    else:
        html = _basic_md_to_html(markdown_text)

    html = _post_process_html(html)
    return html


def _post_process_html(html: str) -> str:
    """Convert standard HTML code blocks to Confluence code macros."""
    # Convert <pre><code class="language-xxx"> to Confluence code macro
    def replace_code_block(match):
        lang_match = re.search(r'class="language-(\w+)"', match.group(1))
        lang = lang_match.group(1) if lang_match else ""
        code = match.group(2)
        # Unescape HTML entities in code
        code = code.replace("&lt;", "<").replace("&gt;", ">").replace("&amp;", "&")
        lang_param = f'<ac:parameter ac:name="language">{lang}</ac:parameter>' if lang else ""
        return (
            f'<ac:structured-macro ac:name="code">'
            f'{lang_param}'
            f'<ac:plain-text-body><![CDATA[{code}]]></ac:plain-text-body>'
            f'</ac:structured-macro>'
        )

    html = re.sub(
        r"<pre>(<code[^>]*>)(.*?)</code></pre>",
        replace_code_block,
        html,
        flags=re.DOTALL,
    )

    # Convert > **NOTE:** ... blockquotes to Confluence info macros
    def replace_blockquote(match):
        content = match.group(1).strip()
        macro_name = "info"
        if re.match(r"<strong>warning", content, re.IGNORECASE):
            macro_name = "warning"
        elif re.match(r"<strong>note", content, re.IGNORECASE):
            macro_name = "note"
        elif re.match(r"<strong>tip", content, re.IGNORECASE):
            macro_name = "tip"
        return (
            f'<ac:structured-macro ac:name="{macro_name}">'
            f'<ac:rich-text-body><p>{content}</p></ac:rich-text-body>'
            f'</ac:structured-macro>'
        )

    html = re.sub(r"<blockquote>\s*<p>(.*?)</p>\s*</blockquote>",
                  replace_blockquote, html, flags=re.DOTALL)

    return html


def _basic_md_to_html(text: str) -> str:
    """Minimal fallback HTML converter when markdown library is not installed."""
    # Fenced code blocks
    text = re.sub(
        r"```(\w*)\n(.*?)```",
        lambda m: (
            f'<ac:structured-macro ac:name="code">'
            f'<ac:parameter ac:name="language">{m.group(1)}</ac:parameter>'
            f'<ac:plain-text-body><![CDATA[{m.group(2)}]]></ac:plain-text-body>'
            f'</ac:structured-macro>'
        ),
        text,
        flags=re.DOTALL,
    )
    # Headings
    for i in range(6, 0, -1):
        text = re.sub(rf"^{'#' * i} (.+)$", rf"<h{i}>\1</h{i}>", text, flags=re.MULTILINE)
    # Bold / italic
    text = re.sub(r"\*\*(.+?)\*\*", r"<strong>\1</strong>", text)
    text = re.sub(r"\*(.+?)\*", r"<em>\1</em>", text)
    # Inline code
    text = re.sub(r"`([^`]+)`", r"<code>\1</code>", text)
    # Links
    text = re.sub(r"\[(.+?)\]\((.+?)\)", r'<a href="\2">\1</a>', text)
    # Unordered list items
    text = re.sub(r"^- (.+)$", r"<li>\1</li>", text, flags=re.MULTILINE)
    text = re.sub(r"(<li>.*</li>)", r"<ul>\1</ul>", text, flags=re.DOTALL)
    # Ordered list items
    text = re.sub(r"^\d+\. (.+)$", r"<li>\1</li>", text, flags=re.MULTILINE)
    # Paragraphs
    text = re.sub(r"\n\n(.+?)\n\n", r"<p>\1</p>", text, flags=re.DOTALL)
    # HR
    text = re.sub(r"^---$", "<hr/>", text, flags=re.MULTILINE)
    return text


# ---------------------------------------------------------------------------
# Upsert logic
# ---------------------------------------------------------------------------

def upsert_page(client: ConfluenceClient, title: str, body_html: str,
                space_key: str, parent_id: str | None,
                dry_run: bool = False) -> dict:
    existing = client.find_page(title, space_key)

    if existing:
        page_id = existing["id"]
        version = existing["version"]["number"]
        last_modified = existing.get("version", {}).get("when", "unknown")
        print(f"  Page exists (last updated: {last_modified}). Updating...")
        if dry_run:
            print(f"  [DRY RUN] Would update page ID {page_id}, version {version} → {version + 1}")
            return existing
        result = client.update_page(page_id, title, body_html, version)
        print(f"  Updated: {client.page_url(result)}")
        return result
    else:
        print(f"  Page not found. Creating under parent ID {parent_id or 'root'}...")
        if dry_run:
            print(f"  [DRY RUN] Would create page '{title}' in space {space_key}")
            return {}
        result = client.create_page(space_key, title, body_html, parent_id)
        print(f"  Created: {client.page_url(result)}")
        return result


def resolve_parent_id(client: ConfluenceClient, parent: str | None,
                      parent_id: str | None, space_key: str) -> str | None:
    if parent_id:
        return parent_id
    if parent:
        page = client.find_page_by_title(parent, space_key)
        if not page:
            print(f"Warning: Parent page '{parent}' not found in space {space_key}. "
                  "Page will be created at space root.", file=sys.stderr)
            return None
        return page["id"]
    return None


def process_file(client: ConfluenceClient, filepath: Path, space_key: str,
                 parent_id: str | None, dry_run: bool) -> bool:
    print(f"\nProcessing: {filepath.name}")
    content = filepath.read_text(encoding="utf-8")
    content = strip_frontmatter(content)
    title, body = extract_title(content)

    if not title:
        title = filepath.stem
        print(f"  No # heading found. Using filename as title: '{title}'")

    body_html = convert_markdown_to_confluence_html(body)

    try:
        upsert_page(client, title, body_html, space_key, parent_id, dry_run)
        return True
    except requests.HTTPError as e:
        print(f"  FAILED: {e.response.status_code} {e.response.text}", file=sys.stderr)
        return False


# ---------------------------------------------------------------------------
# Entrypoint
# ---------------------------------------------------------------------------

def main():
    parser = argparse.ArgumentParser(description="Push Markdown files to Confluence.")
    parser.add_argument("--file", help="Single .md file to push")
    parser.add_argument("--files", help="Glob pattern for multiple files (e.g. '*.md')")
    parser.add_argument("--space", required=True, help="Confluence space key (e.g. BS)")
    parser.add_argument("--parent", help="Parent page title")
    parser.add_argument("--parent-id", help="Parent page ID (overrides --parent)")
    parser.add_argument("--dry-run", action="store_true",
                        help="Show what would happen without making changes")
    parser.add_argument("--confluence-url", default=os.getenv("CONFLUENCE_URL"))
    parser.add_argument("--username", default=os.getenv("CONFLUENCE_USERNAME"))
    parser.add_argument("--token", default=os.getenv("CONFLUENCE_API_TOKEN"))
    args = parser.parse_args()

    if not all([args.confluence_url, args.username, args.token]):
        print("Error: Credentials required. Set CONFLUENCE_URL, CONFLUENCE_USERNAME, "
              "CONFLUENCE_API_TOKEN or use --confluence-url, --username, --token.",
              file=sys.stderr)
        sys.exit(1)

    if not args.file and not args.files:
        print("Error: --file or --files required.", file=sys.stderr)
        sys.exit(1)

    if not HAS_MARKDOWN:
        print("Warning: markdown library not installed. Using basic converter.\n"
              "Install with: pip install markdown", file=sys.stderr)

    if args.dry_run:
        print("DRY RUN mode — no changes will be made.\n")

    client = ConfluenceClient(args.confluence_url, args.username, args.token)
    parent_id = resolve_parent_id(client, args.parent, args.parent_id, args.space)

    # Collect files
    if args.file:
        files = [Path(args.file)]
    else:
        import glob
        files = [Path(f) for f in glob.glob(args.files)]
        if not files:
            print(f"No files matched: {args.files}", file=sys.stderr)
            sys.exit(1)
        print(f"Found {len(files)} files to push.")

    success, failed = 0, 0
    for filepath in files:
        if not filepath.exists():
            print(f"File not found: {filepath}", file=sys.stderr)
            failed += 1
            continue
        if process_file(client, filepath, args.space, parent_id, args.dry_run):
            success += 1
        else:
            failed += 1

    print(f"\nDone. {success} pushed, {failed} failed.")
    sys.exit(0 if failed == 0 else 1)


if __name__ == "__main__":
    main()
