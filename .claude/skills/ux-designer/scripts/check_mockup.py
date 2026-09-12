#!/usr/bin/env python3
"""Static gate for a ux-designer HTML mockup.

Usage:
    python3 check_mockup.py <file.html> [--json]

Checks, in order of how often they catch something real:

  1. WCAG contrast for every pair in the #ux-manifest block, in BOTH light and dark.
     Dark mode is where contrast quietly breaks, because people invert a palette
     instead of rebuilding it.
  2. Spacing values off the 4px scale.
  3. :focus-visible coverage.
  4. One [data-primary] per [data-scope].
  5. Required states present.
  6. External resource references, which break the self-contained promise.

Exit code 0 = clean, 1 = failures, 2 = could not run.

Deliberately honest about its limits: this reads the file, it does not render it.
Computed contrast, hit-target size and overlap need the browser pass with
assets/audit.js. Do not report those as verified on the strength of this script.
"""

import json
import os
import re
import sys
from html.parser import HTMLParser

SCALE = {0, 1, 2, 4, 8, 12, 16, 20, 24, 32, 40, 48, 64, 80, 96, 128}
REQUIRED_STATES = ("default", "empty", "loading", "error")
VOID = {"area", "base", "br", "col", "embed", "hr", "img", "input",
        "link", "meta", "param", "source", "track", "wbr"}


class Node(object):
    __slots__ = ("tag", "attrs", "children", "parent")

    def __init__(self, tag, attrs, parent):
        self.tag = tag
        self.attrs = attrs
        self.children = []
        self.parent = parent

    def descendants(self):
        for child in self.children:
            yield child
            for sub in child.descendants():
                yield sub


class DomBuilder(HTMLParser):
    """Minimal nesting-aware parser. Stdlib only, so the gate has no dependencies.

    Regex cannot do this job: an attribute search over raw text bleeds past the
    closing tag, which made an earlier version count primary CTAs from every
    state section against a single scope.
    """

    def __init__(self):
        HTMLParser.__init__(self, convert_charrefs=True)
        self.root = Node("#document", {}, None)
        self.stack = [self.root]
        self.skip = None

    def handle_starttag(self, tag, attrs):
        if self.skip:
            return
        node = Node(tag, dict(attrs), self.stack[-1])
        self.stack[-1].children.append(node)
        if tag in ("script", "style"):
            self.skip = tag
        elif tag not in VOID:
            self.stack.append(node)

    def handle_startendtag(self, tag, attrs):
        if self.skip:
            return
        self.stack[-1].children.append(Node(tag, dict(attrs), self.stack[-1]))

    def handle_endtag(self, tag):
        if self.skip:
            if tag == self.skip:
                self.skip = None
            return
        for i in range(len(self.stack) - 1, 0, -1):
            if self.stack[i].tag == tag:
                del self.stack[i:]
                break


def build_dom(html):
    parser = DomBuilder()
    parser.feed(html)
    return parser.root


# --------------------------------------------------------------------------- colour

def parse_color(value):
    """Return (r, g, b) from #rgb, #rrggbb, rgb() or rgba(). None if not a colour."""
    v = value.strip().lower()
    m = re.match(r"^#([0-9a-f]{3}|[0-9a-f]{6})$", v)
    if m:
        h = m.group(1)
        if len(h) == 3:
            h = "".join(c * 2 for c in h)
        return tuple(int(h[i:i + 2], 16) for i in (0, 2, 4))
    m = re.match(r"^rgba?\(([^)]+)\)$", v)
    if m:
        parts = [p.strip() for p in re.split(r"[,\s/]+", m.group(1)) if p.strip()]
        if len(parts) >= 3:
            try:
                return tuple(min(255, max(0, int(round(float(p.rstrip("%")))))) for p in parts[:3])
            except ValueError:
                return None
    return None


def luminance(rgb):
    out = []
    for c in rgb:
        s = c / 255.0
        out.append(s / 12.92 if s <= 0.04045 else ((s + 0.055) / 1.055) ** 2.4)
    return 0.2126 * out[0] + 0.7152 * out[1] + 0.0722 * out[2]


def contrast(fg, bg):
    a, b = luminance(fg), luminance(bg)
    hi, lo = max(a, b), min(a, b)
    return (hi + 0.05) / (lo + 0.05)


# --------------------------------------------------------------------------- parsing

def strip_comments(css):
    return re.sub(r"/\*.*?\*/", "", css, flags=re.S)


def all_css(html):
    return strip_comments("\n".join(re.findall(r"<style[^>]*>(.*?)</style>", html, flags=re.S)))


def token_blocks(css):
    """Return (light, dark) dicts of custom properties.

    Light = the :root block. Dark = anything under a prefers-color-scheme: dark
    media query or an html[data-theme="dark"] selector, layered over light.
    """
    light, dark_raw = {}, {}

    for body in re.findall(r":root\s*\{([^}]*)\}", css):
        for name, val in re.findall(r"(--[\w-]+)\s*:\s*([^;]+);", body):
            light[name] = val.strip()

    dark_css = "\n".join(re.findall(r"@media[^{]*prefers-color-scheme\s*:\s*dark[^{]*\{(.*?)\n\s*\}\s*\n", css, flags=re.S))
    dark_css += "\n".join(re.findall(r"html\[data-theme=[\"']dark[\"']\]\s*\{([^}]*)\}", css))
    for name, val in re.findall(r"(--[\w-]+)\s*:\s*([^;]+);", dark_css):
        dark_raw[name] = val.strip()

    dark = dict(light)
    dark.update(dark_raw)
    return light, dark


def manifest_of(html):
    m = re.search(r'<script[^>]*id=["\']ux-manifest["\'][^>]*>(.*?)</script>', html, flags=re.S)
    if not m:
        return None, "no #ux-manifest block found - copy assets/mockup-shell.html rather than writing from scratch"
    try:
        return json.loads(m.group(1)), None
    except ValueError as exc:
        return None, "#ux-manifest is not valid JSON: %s" % exc


# --------------------------------------------------------------------------- checks

def check_contrast(manifest, light, dark):
    fails, notes = [], []
    pairs = manifest.get("contrast_pairs") or []
    if not pairs:
        notes.append("manifest declares no contrast_pairs, so nothing was checked")
    for theme_name, tokens in (("light", light), ("dark", dark)):
        for pair in pairs:
            fg_tok, bg_tok = pair.get("fg"), pair.get("bg")
            minimum = float(pair.get("min", 4.5))
            fg_raw, bg_raw = tokens.get(fg_tok), tokens.get(bg_tok)
            if fg_raw is None or bg_raw is None:
                notes.append("%s [%s]: token not defined (%s / %s)" % (pair.get("name"), theme_name, fg_tok, bg_tok))
                continue
            fg, bg = parse_color(fg_raw), parse_color(bg_raw)
            if not fg or not bg:
                notes.append("%s [%s]: value is not a plain colour, check it in the browser" % (pair.get("name"), theme_name))
                continue
            ratio = contrast(fg, bg)
            if ratio < minimum:
                fails.append("contrast %.2f:1 (needs %.1f) - %s [%s]  %s %s on %s %s"
                             % (ratio, minimum, pair.get("name"), theme_name, fg_tok, fg_raw, bg_tok, bg_raw))
    return fails, notes


def check_spacing(css):
    fails = []
    props = r"(?:margin|padding|gap|row-gap|column-gap|top|right|bottom|left|inset)[\w-]*"
    for prop, value in re.findall(r"(%s)\s*:\s*([^;{}]+)[;}]" % props, css):
        for num in re.findall(r"(?<![\w.-])(\d+(?:\.\d+)?)px", value):
            px = float(num)
            if px not in SCALE and px % 4 != 0:
                fails.append("off-grid spacing %spx in `%s: %s` - use var(--space-*)" % (num, prop, value.strip()))
    return sorted(set(fails))


def check_focus(css, html):
    fails = []
    if ":focus-visible" not in css:
        fails.append("no :focus-visible rule anywhere - keyboard users get no focus indicator (WCAG 2.4.7)")
    if re.search(r"outline\s*:\s*(none|0)", css) and ":focus-visible" not in css:
        fails.append("outline removed with no :focus-visible replacement")
    interactive = len(re.findall(r"<(?:button|a\s|input|select|textarea)", html, flags=re.I))
    if interactive and ":focus-visible" not in css:
        fails.append("%d interactive elements and no focus styling" % interactive)
    return fails


def check_primary(dom):
    fails = []
    for node in dom.descendants():
        if "data-scope" not in node.attrs:
            continue
        n = sum(1 for d in node.descendants() if "data-primary" in d.attrs)
        if "data-primary" in node.attrs:
            n += 1
        if n > 1:
            fails.append('scope "%s" has %d [data-primary] elements - two primaries means no primary'
                         % (node.attrs["data-scope"], n))
    return fails


def check_states(dom, manifest):
    fails = []
    sections = [n for n in dom.descendants() if "data-state" in n.attrs]
    present = set(n.attrs["data-state"] for n in sections)
    declared = manifest.get("states") or list(REQUIRED_STATES)
    for state in declared:
        if state not in present:
            fails.append('manifest declares state "%s" but no [data-state="%s"] section exists' % (state, state))
    for state in REQUIRED_STATES:
        if state not in present:
            fails.append('missing "%s" state - a screen shipped without it will surprise engineering' % state)
    active = [n for n in sections if "data-active" in n.attrs]
    if len(active) != 1:
        fails.append("%d state sections carry data-active, expected exactly 1" % len(active))
    return fails


def check_self_contained(html):
    fails = []
    for m in re.findall(r'<(?:script|link|img)[^>]*(?:src|href)=["\'](https?://[^"\']+)["\']', html, flags=re.I):
        fails.append("external resource %s - the mockup must open with no network" % m)
    return sorted(set(fails))


def check_placeholders(html):
    n = html.count("REPLACE")
    return ["%d REPLACE placeholders left in the file" % n] if n else []


# --------------------------------------------------------------------------- main

def run(path):
    with open(path, "r", encoding="utf-8") as fh:
        html = fh.read()

    css = all_css(html)
    light, dark = token_blocks(css)
    manifest, err = manifest_of(html)
    if err:
        return {"file": path, "sections": [("manifest", [err], [])], "notes": []}

    dom = build_dom(html)
    contrast_fails, contrast_notes = check_contrast(manifest, light, dark)

    sections = [
        ("contrast (light + dark)", contrast_fails, contrast_notes),
        ("spacing scale", check_spacing(css), []),
        ("focus visibility", check_focus(css, html), []),
        ("one primary per scope", check_primary(dom), []),
        ("states", check_states(dom, manifest), []),
        ("self-contained", check_self_contained(html), []),
        ("placeholders", check_placeholders(html), []),
    ]
    return {"file": path, "manifest": manifest, "sections": sections}


def main():
    args = [a for a in sys.argv[1:] if not a.startswith("--")]
    as_json = "--json" in sys.argv
    if not args:
        print(__doc__)
        return 2
    path = args[0]
    if not os.path.isfile(path):
        print("not a file: %s" % path)
        return 2

    result = run(path)
    sections = result["sections"]
    total = sum(len(f) for _, f, _ in sections)

    if as_json:
        print(json.dumps({
            "file": result["file"],
            "failures": total,
            "sections": [{"name": n, "failures": f, "notes": nt} for n, f, nt in sections],
        }, indent=2))
        return 1 if total else 0

    print("\nux-designer static gate  ->  %s\n" % result["file"])
    for name, fails, notes in sections:
        mark = "FAIL" if fails else "pass"
        print("[%s] %s" % (mark, name))
        for f in fails:
            print("       - %s" % f)
        for n in notes:
            print("       ? %s" % n)
    print("")
    if total:
        print("%d failure(s). Fix these before showing anyone.\n" % total)
    else:
        print("Static checks clean.")
        print("Still unverified by this script: computed contrast on rendered")
        print("backgrounds, hit-target sizes, overlap, and tab order. Run the")
        print("browser pass with assets/audit.js before calling anything verified.\n")
    return 1 if total else 0


if __name__ == "__main__":
    sys.exit(main())
