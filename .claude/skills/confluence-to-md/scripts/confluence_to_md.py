#!/usr/bin/env python3
"""
confluence_to_md.py - Fetch Confluence pages and save as clean Markdown files.

Usage:
  # Single page by ID
  python confluence_to_md.py --mode single --page-id 123456789

  # Single page by URL
  python confluence_to_md.py --mode single --url "https://your-site.atlassian.net/wiki/spaces/BS/pages/123456789/Page+Title"

  # Full space
  python confluence_to_md.py --mode space --space-key BS

  # Keyword search
  python confluence_to_md.py --mode search --query "voice companion"

  # All modes support --output to set the save directory (default: current directory)
  python confluence_to_md.py --mode space --space-key BS --output ./confluence-export

Credentials (in order of precedence):
  1. CLI flags: --url, --username, --token
  2. Environment variables: CONFLUENCE_URL, CONFLUENCE_USERNAME, CONFLUENCE_API_TOKEN
  3. .env file in current directory

Dependencies:
  pip install requests beautifulsoup4 markdownify python-dotenv
"""

import os
import re
import sys
import json
import argparse
import requests
from pathlib import Path
from bs4 import BeautifulSoup

# Load .env if present
try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    pass

try:
    import markdownify as md_lib
    HAS_MARKDOWNIFY = True
except ImportError:
    HAS_MARKDOWNIFY = False


# ---------------------------------------------------------------------------
# Confluence REST API client
# ---------------------------------------------------------------------------

class ConfluenceClient:
    def __init__(self, base_url: str, username: str, token: str):
        self.base_url = base_url.rstrip("/")
        self.session = requests.Session()
        self.session.auth = (username, token)
        self.session.headers.update({"Accept": "application/json"})

    def get_page(self, page_id: str) -> dict:
        url = f"{self.base_url}/wiki/rest/api/content/{page_id}"
        params = {"expand": "body.storage,version,space,title"}
        resp = self.session.get(url, params=params)
        resp.raise_for_status()
        return resp.json()

    def search(self, cql: str, limit: int = 50) -> list[dict]:
        url = f"{self.base_url}/wiki/rest/api/content/search"
        results = []
        start = 0
        while True:
            params = {"cql": cql, "limit": min(limit, 50), "start": start,
                      "expand": "version,space,title"}
            resp = self.session.get(url, params=params)
            resp.raise_for_status()
            data = resp.json()
            results.extend(data.get("results", []))
            if len(results) >= limit:
                break
            if data.get("_links", {}).get("next") is None:
                break
            start += len(data["results"])
        return results[:limit]

    def get_page_body(self, page_id: str) -> tuple[str, str, str]:
        """Returns (title, space_key, html_body)."""
        page = self.get_page(page_id)
        title = page["title"]
        space_key = page["space"]["key"]
        html_body = page["body"]["storage"]["value"]
        return title, space_key, html_body


# ---------------------------------------------------------------------------
# Confluence Storage Format → Markdown converter
# ---------------------------------------------------------------------------

def slugify(text: str) -> str:
    text = text.lower()
    text = re.sub(r"[^\w\s-]", "", text)
    text = re.sub(r"[\s_]+", "-", text)
    text = text.strip("-")
    return text[:80]


def convert_confluence_to_markdown(html: str, title: str = "") -> str:
    """Convert Confluence storage format HTML to clean Markdown."""
    soup = BeautifulSoup(html, "html.parser")

    # --- Pre-process Confluence macros before general conversion ---

    # Code blocks: <ac:structured-macro ac:name="code">
    for macro in soup.find_all("ac:structured-macro", {"ac:name": "code"}):
        lang_param = macro.find("ac:parameter", {"ac:name": "language"})
        lang = lang_param.get_text(strip=True) if lang_param else ""
        body = macro.find("ac:plain-text-body")
        code = body.get_text() if body else ""
        fence = f"```{lang}\n{code}\n```"
        macro.replace_with(soup.new_string(f"\n{fence}\n"))

    # Info / note / warning macros → blockquote with label
    for name in ("info", "note", "warning", "tip"):
        for macro in soup.find_all("ac:structured-macro", {"ac:name": name}):
            body = macro.find("ac:rich-text-body")
            content = body.get_text(separator="\n", strip=True) if body else ""
            label = name.upper()
            macro.replace_with(soup.new_string(f"\n> **{label}:** {content}\n"))

    # Status macro → plain text label
    for macro in soup.find_all("ac:structured-macro", {"ac:name": "status"}):
        label = macro.find("ac:parameter", {"ac:name": "title"})
        text = label.get_text(strip=True) if label else "STATUS"
        macro.replace_with(soup.new_string(f"[{text}]"))

    # Expand macro → keep content
    for macro in soup.find_all("ac:structured-macro", {"ac:name": "expand"}):
        body = macro.find("ac:rich-text-body")
        content = body.decode_contents() if body else ""
        macro.replace_with(BeautifulSoup(content, "html.parser"))

    # Remove TOC, children, recently-updated, and other nav macros
    for name in ("toc", "children", "recently-updated", "page-tree",
                 "breadcrumbs", "excerpt-include"):
        for macro in soup.find_all("ac:structured-macro", {"ac:name": name}):
            macro.decompose()

    # Inline task list items
    for task in soup.find_all("ac:task"):
        status = task.find("ac:task-status")
        body = task.find("ac:task-body")
        checked = "x" if (status and status.get_text(strip=True) == "complete") else " "
        text = body.get_text(strip=True) if body else ""
        task.replace_with(soup.new_string(f"\n- [{checked}] {text}"))

    # Remove remaining ac: tags (keep their text)
    for tag in soup.find_all(re.compile(r"^ac:")):
        tag.unwrap()

    # Remove ri: tags entirely
    for tag in soup.find_all(re.compile(r"^ri:")):
        tag.decompose()

    # --- Convert HTML to Markdown ---
    if HAS_MARKDOWNIFY:
        markdown = md_lib.markdownify(
            str(soup),
            heading_style="ATX",
            bullets="-",
            strip=["script", "style"],
        )
    else:
        # Fallback: basic manual conversion
        markdown = _manual_html_to_md(soup)

    # --- Post-process cleanup ---
    markdown = _cleanup_markdown(markdown)

    # Prepend title as H1 if provided
    if title:
        markdown = f"# {title}\n\n{markdown}"

    return markdown


def _manual_html_to_md(soup: BeautifulSoup) -> str:
    """Minimal fallback converter when markdownify is not installed."""
    for tag in soup.find_all(["h1", "h2", "h3", "h4", "h5", "h6"]):
        level = int(tag.name[1])
        tag.replace_with(soup.new_string(f"\n{'#' * level} {tag.get_text(strip=True)}\n"))
    for tag in soup.find_all("strong"):
        tag.replace_with(soup.new_string(f"**{tag.get_text()}**"))
    for tag in soup.find_all("em"):
        tag.replace_with(soup.new_string(f"*{tag.get_text()}*"))
    for tag in soup.find_all("code"):
        tag.replace_with(soup.new_string(f"`{tag.get_text()}`"))
    for tag in soup.find_all("a"):
        href = tag.get("href", "")
        tag.replace_with(soup.new_string(f"[{tag.get_text()}]({href})"))
    for tag in soup.find_all("li"):
        tag.replace_with(soup.new_string(f"\n- {tag.get_text(strip=True)}"))
    for tag in soup.find_all(["ul", "ol", "p", "br"]):
        tag.replace_with(soup.new_string(f"\n{tag.get_text()}\n"))
    for tag in soup.find_all("hr"):
        tag.replace_with(soup.new_string("\n---\n"))
    return soup.get_text()


def _cleanup_markdown(text: str) -> str:
    """Remove noise, strip Confluence metadata footers, normalize whitespace."""
    lines = text.splitlines()
    cleaned = []
    skip_patterns = [
        re.compile(r"^Created by\s+.+\s+on\s+", re.IGNORECASE),
        re.compile(r"^Modified by\s+", re.IGNORECASE),
        re.compile(r"^Last updated", re.IGNORECASE),
        re.compile(r"^\d+ people liked this", re.IGNORECASE),
        re.compile(r"^Add Comment$", re.IGNORECASE),
    ]
    for line in lines:
        if any(p.match(line.strip()) for p in skip_patterns):
            continue
        cleaned.append(line)

    text = "\n".join(cleaned)
    # Collapse 3+ consecutive blank lines to 2
    text = re.sub(r"\n{3,}", "\n\n", text)
    return text.strip()


# ---------------------------------------------------------------------------
# File saving helpers
# ---------------------------------------------------------------------------

def save_markdown(content: str, output_dir: Path, filename: str) -> Path:
    output_dir.mkdir(parents=True, exist_ok=True)
    filepath = output_dir / filename
    filepath.write_text(content, encoding="utf-8")
    return filepath


def page_filename(space_key: str, title: str) -> str:
    return f"{space_key.lower()}-{slugify(title)}.md"


# ---------------------------------------------------------------------------
# Mode handlers
# ---------------------------------------------------------------------------

def handle_single(client: ConfluenceClient, page_id: str, output_dir: Path):
    print(f"Fetching page {page_id}...")
    title, space_key, html = client.get_page_body(page_id)
    markdown = convert_confluence_to_markdown(html, title)
    filename = page_filename(space_key, title)
    path = save_markdown(markdown, output_dir, filename)
    print(f"Saved: {path}")
    return 1, 0


def handle_space(client: ConfluenceClient, space_key: str, output_dir: Path,
                 batch_size: int = 5):
    cql = f'space = "{space_key}" AND type = page ORDER BY title ASC'
    print(f"Searching space {space_key}...")
    pages = client.search(cql, limit=200)
    print(f"Found {len(pages)} pages.")

    space_dir = output_dir / space_key.lower()
    success, failed = 0, 0

    for i, page_meta in enumerate(pages):
        page_id = page_meta["id"]
        title = page_meta["title"]
        if i > 0 and i % batch_size == 0:
            print(f"  [{i}/{len(pages)}] Batch complete. Continuing...")
        try:
            _, _, html = client.get_page_body(page_id)
            markdown = convert_confluence_to_markdown(html, title)
            filename = f"{slugify(title)}.md"
            path = save_markdown(markdown, space_dir, filename)
            print(f"  Saved: {path.name}")
            success += 1
        except Exception as e:
            print(f"  FAILED: {title} ({page_id}) — {e}", file=sys.stderr)
            failed += 1

    return success, failed


def handle_search(client: ConfluenceClient, query: str, output_dir: Path):
    cql = f'text ~ "{query}" AND type = page'
    print(f"Searching: {query}")
    pages = client.search(cql, limit=10)

    if not pages:
        print("No pages found.")
        return 0, 0

    print(f"\nFound {len(pages)} pages:")
    for i, p in enumerate(pages, 1):
        space = p.get("space", {}).get("key", "?")
        print(f"  {i}. [{space}] {p['title']}")

    selection = input("\nEnter numbers to download (e.g. 1,3,5 or 'all'): ").strip()
    if selection.lower() == "all":
        selected = pages
    else:
        try:
            indices = [int(x.strip()) - 1 for x in selection.split(",")]
            selected = [pages[i] for i in indices if 0 <= i < len(pages)]
        except ValueError:
            print("Invalid selection.", file=sys.stderr)
            return 0, 0

    export_dir = output_dir / "confluence-export"
    success, failed = 0, 0
    for page_meta in selected:
        page_id = page_meta["id"]
        title = page_meta["title"]
        space_key = page_meta.get("space", {}).get("key", "unknown")
        try:
            _, _, html = client.get_page_body(page_id)
            markdown = convert_confluence_to_markdown(html, title)
            filename = page_filename(space_key, title)
            path = save_markdown(markdown, export_dir, filename)
            print(f"  Saved: {path}")
            success += 1
        except Exception as e:
            print(f"  FAILED: {title} — {e}", file=sys.stderr)
            failed += 1

    return success, failed


# ---------------------------------------------------------------------------
# Entrypoint
# ---------------------------------------------------------------------------

def extract_page_id_from_url(url: str) -> str:
    match = re.search(r"/pages/(\d+)", url)
    if match:
        return match.group(1)
    raise ValueError(f"Could not extract page ID from URL: {url}")


def main():
    parser = argparse.ArgumentParser(description="Fetch Confluence pages as Markdown.")
    parser.add_argument("--mode", choices=["single", "space", "search"], required=True)
    parser.add_argument("--page-id", help="Page ID (single mode)")
    parser.add_argument("--url", help="Confluence page URL (single mode)")
    parser.add_argument("--space-key", help="Space key (space mode)")
    parser.add_argument("--query", help="Search query (search mode)")
    parser.add_argument("--output", default=".", help="Output directory")
    parser.add_argument("--confluence-url", default=os.getenv("CONFLUENCE_URL"))
    parser.add_argument("--username", default=os.getenv("CONFLUENCE_USERNAME"))
    parser.add_argument("--token", default=os.getenv("CONFLUENCE_API_TOKEN"))
    args = parser.parse_args()

    if not all([args.confluence_url, args.username, args.token]):
        print("Error: Confluence credentials required. Set CONFLUENCE_URL, "
              "CONFLUENCE_USERNAME, CONFLUENCE_API_TOKEN or use --confluence-url, "
              "--username, --token.", file=sys.stderr)
        sys.exit(1)

    if not HAS_MARKDOWNIFY:
        print("Warning: markdownify not installed. Using basic converter.\n"
              "Install with: pip install markdownify", file=sys.stderr)

    client = ConfluenceClient(args.confluence_url, args.username, args.token)
    output_dir = Path(args.output)

    if args.mode == "single":
        if args.url:
            page_id = extract_page_id_from_url(args.url)
        elif args.page_id:
            page_id = args.page_id
        else:
            print("Error: --page-id or --url required for single mode.", file=sys.stderr)
            sys.exit(1)
        success, failed = handle_single(client, page_id, output_dir)

    elif args.mode == "space":
        if not args.space_key:
            print("Error: --space-key required for space mode.", file=sys.stderr)
            sys.exit(1)
        success, failed = handle_space(client, args.space_key, output_dir)

    elif args.mode == "search":
        if not args.query:
            print("Error: --query required for search mode.", file=sys.stderr)
            sys.exit(1)
        success, failed = handle_search(client, args.query, output_dir)

    print(f"\nDone. {success} saved, {failed} failed.")
    sys.exit(0 if failed == 0 else 1)


if __name__ == "__main__":
    main()
