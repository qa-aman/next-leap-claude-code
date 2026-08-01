"""
Step 4 of the workflow: build the interactive dashboard.

The whole ticket set is embedded in the page, so every filter recomputes from the
raw rows rather than from a pre-baked summary. That matters: a filter that changes
the heading but not the panel below it is the single most common bug in a dashboard
like this, and computing from source is what prevents it.

Output: report/ticket-analysis-dashboard.html - self-contained, no network calls.
Run: python3 build_dashboard.py
"""

import json
from pathlib import Path

import pandas as pd

ROOT = Path(__file__).resolve().parent.parent
DATA = ROOT / "data"
REPORT = ROOT / "report"

MONTHS = ["2026-01", "2026-02", "2026-03"]
MONTH_LABEL = ["Jan 2026", "Feb 2026", "Mar 2026"]
PRIORITIES = ["P1 - Critical", "P2 - High", "P3 - Moderate", "P4 - Low"]
CHANNELS = ["Self-Service Portal", "Email", "Phone", "Chat"]

TEMPLATE = (Path(__file__).resolve().parent / "dashboard_template.html")


def main():
    df = pd.read_excel(DATA / "categorized-tickets.xlsx", sheet_name="Tickets")
    metrics = json.loads((DATA / "metrics.json").read_text())

    # Fixed colour order, assigned once by total volume and then frozen.
    # A filter must never repaint a category, so this list is the only source of hue.
    l1_order = [r["name"] for r in metrics["l1"]]

    rows = []
    for _, r in df.iterrows():
        hours = None if pd.isna(r["Resolution Hours"]) else round(float(r["Resolution Hours"]), 2)
        sla = None if r["SLA Met"] not in ("Yes", "No") else (r["SLA Met"] == "Yes")
        rows.append([
            r["Ticket ID"],
            MONTHS.index(r["Month"]),
            l1_order.index(r["Category (L1)"]),
            r["Subcategory (L2)"],
            r["Issue Type (L3)"],
            PRIORITIES.index(r["Priority"]),
            hours,
            sla,
            r["Reopened"] == "Yes",
            CHANNELS.index(r["Channel"]),
            r["Department"],
            r["Description"],
            r["Confidence"],
            r["Reason"],
            r["Assignment Group"],
        ])

    payload = {
        "months": MONTH_LABEL,
        "priorities": ["P1", "P2", "P3", "P4"],
        "channels": CHANNELS,
        "l1_order": l1_order,
        "rows": rows,
        "shortlist_rule": metrics["shortlist_rule"],
        "accuracy": metrics["accuracy"],
        "period": metrics["generated_for"],
    }

    html = TEMPLATE.read_text().replace(
        "/*__PAYLOAD__*/null", json.dumps(payload, separators=(",", ":")))
    REPORT.mkdir(parents=True, exist_ok=True)
    out = REPORT / "ticket-analysis-dashboard.html"
    out.write_text(html)
    print(f"Wrote {out}  ({out.stat().st_size / 1024:.0f} KB, {len(rows)} tickets embedded)")


if __name__ == "__main__":
    main()
