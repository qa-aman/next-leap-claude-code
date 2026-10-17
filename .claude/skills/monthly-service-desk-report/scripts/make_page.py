"""Turn the dashboard into the page that gets published, then gate it.

The Artifact host wraps the page in its own <html><head><body> skeleton, so the document
wrapper is stripped and the title set. Then the page is checked for the defects that have
reached leadership before: em dashes, non DD-MM-YYYY dates, a sample-data footer on real data,
a missing executive summary, and any external host the viewer would block.

    python3 make_page.py --dashboard ticket-dashboard.html --out page.html \
        --title "Service Desk Ticket Report" [--sample-data]

Exit 0 = ship. Exit 1 = fix the listed defects first.
"""
import argparse
import json
import re
import sys
from pathlib import Path


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--dashboard", required=True)
    ap.add_argument("--out", required=True)
    ap.add_argument("--title", required=True)
    ap.add_argument("--sample-data", action="store_true",
                    help="the run used generated sample data; the footer must say so")
    a = ap.parse_args()

    s = Path(a.dashboard).read_text()
    s = re.sub(r'^<!doctype html>\s*<html[^>]*>\s*<head>\s*<meta charset="utf-8">\s*'
               r'<meta name="viewport"[^>]*>\s*', "", s, flags=re.I)
    s = re.sub(r"<title[^>]*>.*?</title>", f'<title id="doctitle">{a.title}</title>', s,
               count=1, flags=re.S)
    s = re.sub(r"</head>\s*<body[^>]*>", "", s, count=1, flags=re.I)
    s = re.sub(r"</body>\s*</html>\s*$", "", s, flags=re.I)
    Path(a.out).write_text(s)

    problems = []
    m = re.search(r"const D = (\{.*?\});\n", s, flags=re.S)
    payload = json.loads(m.group(1)) if m else {}
    markup = s.replace(m.group(1), "") if m else s
    if "—" in markup:
        problems.append(f"{markup.count(chr(0x2014))} em dash(es) in page text; use a comma, colon or hyphen")
    bad_dates = re.findall(r"\b\d{4}-\d{2}-\d{2}\b|\b\d{1,2}/\d{1,2}/\d{4}\b", markup)
    if bad_dates:
        problems.append(f"non DD-MM-YYYY dates: {sorted(set(bad_dates))[:5]}")
    if 'id="execpoints"' not in s:
        problems.append("executive summary block missing; the template is out of date")
    if payload.get("sample_data", False) != a.sample_data:
        problems.append("sample-data footer does not match this run: rebuild analyze.py "
                        + ("with" if a.sample_data else "without") + " --sample-data")
    hosts = set(re.findall(r'(?:src|href)="https?://([^/"]+)', markup))
    if hosts:
        problems.append(f"external hosts the viewer may block: {sorted(hosts)}")
    size = len(s.encode()) / 1e6
    if size > 15:
        problems.append(f"page is {size:.1f} MB, limit is 16 MB")

    print(f"Wrote {a.out} ({size*1000:.0f} KB, {payload.get('ticket_count','?')} tickets, "
          f"title '{a.title}')")
    if problems:
        print("NOT READY:")
        for p in problems:
            print("  -", p)
        sys.exit(1)
    print("Page gate passed.")


if __name__ == "__main__":
    main()
