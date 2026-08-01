"""
Compute every number the report shows, and build the page.

Nothing is calculated inside the HTML, and the whole ticket set is embedded in the
page so every filter recomputes from the raw rows. That is what stops a filter
changing a heading but not the panel below it, which is the most common bug in a
dashboard like this.

The automation shortlist rule is stated in the open, at SHORTLIST below. It is not a
score and there is no hidden weighting. It is three thresholds a subcategory has to
clear, and the report shows the actual value beside each check so anyone can disagree
with a threshold and re-rank it themselves.

Usage:
  python3 analyze.py --input categorized.xlsx --work-dir work/ --out report.html
"""

import argparse
import json
from pathlib import Path

import pandas as pd

SHORTLIST = {
    "min_tickets_latest_month": 12,   # below this, automation costs more than it saves
    "max_spread_hours": 3.0,          # P90 minus P10. Tight spread = same fix every time
    "max_p1p2_share_pct": 25.0,       # routine work, not incident firefighting
}
SMALL_SAMPLE = 10                     # fewer resolved tickets than this and a median is noise

L1, L2, L3 = "Category (L1)", "Subcategory (L2)", "Issue Type (L3)"
MONTH_NAMES = ["Jan", "Feb", "Mar", "Apr", "May", "Jun",
               "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]


def label_month(m):
    s = str(m)
    try:
        return f"{MONTH_NAMES[int(s[5:7]) - 1]} {s[:4]}"
    except (ValueError, IndexError):
        return s


def main():
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--input", required=True, help="the categorized workbook")
    ap.add_argument("--work-dir", required=True)
    ap.add_argument("--out", required=True, help="output .html")
    ap.add_argument("--sheet", default="Tickets")
    ap.add_argument("--title", default="Service desk ticket analysis")
    ap.add_argument("--template", default=None)
    ap.add_argument("--min-tickets", type=int, default=SHORTLIST["min_tickets_latest_month"])
    ap.add_argument("--max-spread", type=float, default=SHORTLIST["max_spread_hours"])
    ap.add_argument("--max-p1p2", type=float, default=SHORTLIST["max_p1p2_share_pct"])
    a = ap.parse_args()

    rule = {"min_tickets_latest_month": a.min_tickets, "max_spread_hours": a.max_spread,
            "max_p1p2_share_pct": a.max_p1p2}
    work = Path(a.work_dir)
    df = pd.read_excel(a.input, sheet_name=a.sheet)
    for c in (L1, L2, L3):
        if c not in df.columns:
            raise SystemExit(f"'{c}' is missing. Run apply_classification.py first.")

    months = sorted(df["Month"].astype(str).unique())
    df["Month"] = df["Month"].astype(str)
    if len(months) < 2:
        print(f"Only {len(months)} month present. Month-on-month sections will be thin.")

    # Optional columns degrade the report rather than crashing it.
    for col, default in [("Resolution Hours", None), ("Priority", "P3 - Moderate"),
                         ("SLA Met", ""), ("Reopened", "No"), ("Channel", "Unknown"),
                         ("Department", "Unknown"), ("Assignment Group", "Service Desk"),
                         ("Short Description", ""), ("Confidence", "High"), ("Reason", "")]:
        if col not in df.columns:
            df[col] = default
    df["Resolution Hours"] = pd.to_numeric(df["Resolution Hours"], errors="coerce")

    priorities = sorted(df["Priority"].dropna().astype(str).unique())
    channels = sorted(df["Channel"].dropna().astype(str).unique())
    l1_order = df[L1].value_counts().index.tolist()[:8]
    df[L1] = df[L1].where(df[L1].isin(l1_order), "Other")
    if "Other" in df[L1].values and "Other" not in l1_order:
        l1_order.append("Other")

    rows = []
    for _, r in df.iterrows():
        hrs = None if pd.isna(r["Resolution Hours"]) else round(float(r["Resolution Hours"]), 2)
        sla = None if str(r["SLA Met"]) not in ("Yes", "No") else (r["SLA Met"] == "Yes")
        rows.append([
            str(r["Ticket ID"]), months.index(r["Month"]), l1_order.index(r[L1]),
            str(r[L2]), str(r[L3]), priorities.index(str(r["Priority"])), hrs, sla,
            str(r["Reopened"]) == "Yes", channels.index(str(r["Channel"])),
            str(r["Department"]), str(r["Description"]), str(r["Confidence"]),
            str(r["Reason"]), str(r["Assignment Group"]),
        ])

    acc_path = work / "accuracy.json"
    accuracy = json.loads(acc_path.read_text()) if acc_path.exists() else {"scored": False}

    # Positional assumptions ("index 0 is the portal", "index <=1 is P1 or P2") break the
    # moment an export has no P1 tickets or names its channels differently. Resolve the
    # meaning here, once, and hand the page explicit indices.
    high_idx = [i for i, p in enumerate(priorities) if p.upper().startswith(("P1", "P2"))]
    portal_idx = [i for i, c in enumerate(channels)
                  if "portal" in c.lower() or "self" in c.lower()]

    payload = {
        "title": a.title,
        # The footer and the drill-panel line state where the page came from. Derive them
        # from the actual inputs, never hardcode them in the template: a stale filename or
        # ticket count in a caption is a claim with the same authority as the numbers
        # beside it, and it survives every later run unnoticed.
        "source_file": Path(a.input).name,
        "ticket_count": int(len(df)),
        "high_priority_idx": high_idx,
        "portal_channel_idx": portal_idx,
        "period": f"{label_month(months[0])} to {label_month(months[-1])}",
        "months": [label_month(m) for m in months],
        "priorities": [p.split(" - ")[0] for p in priorities],
        "channels": channels,
        "l1_order": l1_order,
        "rows": rows,
        "shortlist_rule": rule,
        "small_sample": SMALL_SAMPLE,
        "accuracy": accuracy,
    }

    tpl = Path(a.template) if a.template else Path(__file__).resolve().parent.parent / \
        "assets" / "dashboard_template.html"
    html = tpl.read_text().replace("/*__PAYLOAD__*/null",
                                   json.dumps(payload, separators=(",", ":")))
    out = Path(a.out)
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(html)

    # A console summary, so the findings are visible without opening a browser.
    res = df[df["Resolution Hours"].notna()]
    per_month = df.groupby("Month").size()
    print(f"{len(df)} tickets | " + " ".join(f"{label_month(m)}={per_month[m]}" for m in months))
    if len(months) >= 2:
        d = per_month[months[-1]] - per_month[months[-2]]
        print(f"Latest month vs previous: {d:+} ({100 * d / max(1, per_month[months[-2]]):+.1f}%)")
    if len(res):
        print(f"SLA met {100 * (res['SLA Met'] == 'Yes').mean():.1f}% | "
              f"reopened {100 * (res['Reopened'] == 'Yes').mean():.1f}% | "
              f"{res['Resolution Hours'].sum():.0f} agent-hours")

    print(f"\nShortlist rule: latest month >= {rule['min_tickets_latest_month']} tickets, "
          f"spread <= {rule['max_spread_hours']}h, P1+P2 <= {rule['max_p1p2_share_pct']}%")
    stats = []
    for (c1, c2), g in df.groupby([L1, L2]):
        rg = g[g["Resolution Hours"].notna()]
        h = rg["Resolution Hours"]
        spread = float(h.quantile(.9) - h.quantile(.1)) if len(rg) else 0.0
        latest = int((g["Month"] == months[-1]).sum())
        p12 = 100 * g["Priority"].astype(str).str.startswith(("P1", "P2")).mean()
        checks = {"volume": latest >= rule["min_tickets_latest_month"],
                  "spread": spread <= rule["max_spread_hours"],
                  "routine": p12 <= rule["max_p1p2_share_pct"]}
        stats.append({"l1": c1, "l2": c2, "n": len(g), "latest": latest,
                      "spread": round(spread, 2), "p12": round(p12, 1),
                      "hpm": round(float(h.sum()) / len(months), 1) if len(rg) else 0.0,
                      "resolved": len(rg), "passed": sum(checks.values()), "checks": checks})

    passed = sorted([s for s in stats if s["passed"] == 3], key=lambda s: -s["hpm"])
    near = sorted([s for s in stats if s["passed"] == 2], key=lambda s: -s["hpm"])[:4]
    print("\nAUTOMATION SHORTLIST")
    if passed:
        for s in passed:
            print(f"  {s['l1']} > {s['l2']:24} latest={s['latest']:3} "
                  f"spread={s['spread']:6.2f}h P1P2={s['p12']:5.1f}% "
                  f"{s['hpm']:7.1f} agent-hrs/mo")
    else:
        print("  Nothing clears all three checks.")
    if near:
        print("\nNEAR MISS (two of three)")
        for s in near:
            fail = ", ".join(k for k, v in s["checks"].items() if not v)
            print(f"  {s['l1']} > {s['l2']:24} fails: {fail:10} {s['hpm']:7.1f} agent-hrs/mo")

    print("\nWHERE THE HOURS GO (a different question from volume)")
    for s in sorted(stats, key=lambda s: -s["hpm"])[:5]:
        flag = "  << small sample" if s["resolved"] < SMALL_SAMPLE else ""
        print(f"  {s['l1']} > {s['l2']:24} {s['hpm']:7.1f} agent-hrs/mo "
              f"({s['resolved']} resolved){flag}")

    if not accuracy.get("scored"):
        print("\nThe report will show that categorization accuracy was NOT measured, because")
        print("there is no answer key. That is honest and it is the right thing to publish.")
    print(f"\nWrote {out}  ({out.stat().st_size / 1024:.0f} KB, {len(rows)} tickets embedded)")


if __name__ == "__main__":
    main()
