"""The skill's memory: one row per monthly run.

Next month starts here. It tells the run which artifact URL to republish to, so the management
team keeps one link, and shows whether categorization accuracy is holding.

    python3 history.py show
    python3 history.py add --period "Jan 2026 to Mar 2026" --export x.xlsx --tickets 450 \
        --accuracy-l2 98.7 --page path/page.html --url https://claude.ai/artifact/...
    python3 history.py set-review --period "Apr 2026 to Jun 2026" --page path/review.html \
        --url https://claude.ai/artifact/...
"""
import argparse
import datetime as dt
import json
from pathlib import Path

FILE = Path(__file__).resolve().parents[1] / "state" / "history.json"


def load():
    return json.loads(FILE.read_text()) if FILE.exists() else []


def main():
    ap = argparse.ArgumentParser()
    sub = ap.add_subparsers(dest="cmd", required=True)
    sub.add_parser("show")
    ad = sub.add_parser("add")
    for f in ("period", "export", "page", "url"):
        ad.add_argument(f"--{f}", required=True)
    ad.add_argument("--tickets", type=int, required=True)
    ad.add_argument("--accuracy-l2", default="not measured")
    ad.add_argument("--note", default="")
    ad.add_argument("--test", action="store_true",
                    help="a trial run on its own link; never the link to republish to")
    sr = sub.add_parser("set-review", help="attach the review page and its link to a run")
    for f in ("period", "page", "url"):
        sr.add_argument(f"--{f}", required=True)
    a = ap.parse_args()

    rows = load()
    if a.cmd == "set-review":
        match = [r for r in rows if r["period"] == a.period]
        if not match:
            raise SystemExit(f"No run for '{a.period}'. Record the run with 'add' first.")
        match[-1]["review_page"], match[-1]["review_url"] = a.page, a.url
        FILE.write_text(json.dumps(rows, indent=2))
        print(f"Review recorded for {a.period} -> {a.url}")
        return
    if a.cmd == "show":
        if not rows:
            print("No previous runs. This is the first: publish a new artifact and record its URL.")
            return
        for r in rows:
            print(f"{r['run_date']} | {r['period']} | {r['tickets']} tickets | "
                  f"L2 accuracy {r['accuracy_l2']} | {r['url']}" + (" | TEST" if r.get("test") else "")
                  + (f" | review {r['review_url']}" if r.get("review_url") else ""))
            print(f"    categorized workbook: {Path(r['page']).parent / 'servicenow-tickets-categorized.xlsx'}")
        live = [r for r in rows if not r.get("test")]
        reviews = [r for r in live if r.get("review_url")]
        if reviews:
            print(f"Publish this period's review to: {reviews[-1]['review_url']}")
        print(f"\nPublish this month to: {live[-1]['url']}" if live else
              "\nOnly test runs so far. Publish a new artifact for the first live run.")
        return

    rows.append({"run_date": dt.date.today().strftime("%d-%m-%Y"), "period": a.period,
                 "export": a.export, "tickets": a.tickets, "accuracy_l2": a.accuracy_l2,
                 "page": a.page, "url": a.url, "note": a.note, "test": a.test})
    FILE.parent.mkdir(parents=True, exist_ok=True)
    FILE.write_text(json.dumps(rows, indent=2))
    print(f"Recorded run {len(rows)} -> {FILE}")


if __name__ == "__main__":
    main()
