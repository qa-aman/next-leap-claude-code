"""
Step 3 of the workflow: turn the categorised tickets into the numbers management needs.

Everything the dashboard shows is computed here and written to data/metrics.json.
Nothing is computed inside the HTML, so any number on the dashboard can be traced
back to a line in this file.

The automation shortlist rule is stated in the open, at SHORTLIST below. It is not a
score. It is three thresholds a subcategory has to clear, and the report shows the
three values so anyone can disagree with the thresholds and re-rank it themselves.

Run: python3 analyze.py
"""

import json
from pathlib import Path

import pandas as pd

ROOT = Path(__file__).resolve().parent.parent
DATA = ROOT / "data"

MONTH_LABEL = {"2026-01": "Jan 2026", "2026-02": "Feb 2026", "2026-03": "Mar 2026"}

# The automation shortlist rule. Change these three numbers and the shortlist changes.
SHORTLIST = {
    "min_tickets_latest_month": 12,   # enough volume for automation to be worth building
    "max_spread_hours": 3.0,          # P90 minus P10. Tight spread = the same fix every time
    "max_p1p2_share_pct": 25.0,       # mostly routine, not incident firefighting
}


def pct(a, b):
    return round(100 * a / b, 1) if b else 0.0


def main():
    df = pd.read_excel(DATA / "categorized-tickets.xlsx", sheet_name="Tickets")
    acc = json.loads((DATA / "accuracy.json").read_text())
    months = sorted(df["Month"].unique())
    resolved = df[df["Resolution Hours"].notna()].copy()

    # ---------- headline ----------
    per_month = df.groupby("Month").size()
    headline = {
        "months": [MONTH_LABEL[m] for m in months],
        "month_keys": months,
        "totals": [int(per_month[m]) for m in months],
        "total_tickets": int(len(df)),
        "mom_change_pct": pct(int(per_month[months[-1]]) - int(per_month[months[-2]]),
                              int(per_month[months[-2]])),
        "open_tickets": int((df["Resolution Hours"].isna()).sum()),
        "sla_met_pct": pct((resolved["SLA Met"] == "Yes").sum(), len(resolved)),
        "reopen_pct": pct((resolved["Reopened"] == "Yes").sum(), len(resolved)),
        "total_agent_hours": round(resolved["Resolution Hours"].sum(), 1),
    }

    # ---------- L1 by month ----------
    l1 = []
    for cat, g in df.groupby("Category (L1)"):
        counts = [int((g["Month"] == m).sum()) for m in months]
        rg = resolved[resolved["Category (L1)"] == cat]
        l1.append({
            "name": cat,
            "counts": counts,
            "total": int(len(g)),
            "share_pct": pct(len(g), len(df)),
            "mom_change": counts[-1] - counts[-2],
            "mom_change_pct": pct(counts[-1] - counts[-2], counts[-2]),
            "first_to_last_pct": pct(counts[-1] - counts[0], counts[0]),
            "sla_met_pct": pct((rg["SLA Met"] == "Yes").sum(), len(rg)),
            "reopen_pct": pct((rg["Reopened"] == "Yes").sum(), len(rg)),
            "agent_hours": round(rg["Resolution Hours"].sum(), 1),
            "median_hours": round(rg["Resolution Hours"].median(), 2) if len(rg) else 0,
        })
    l1.sort(key=lambda r: -r["total"])

    # ---------- L2 by month ----------
    l2 = []
    for (cat, sub), g in df.groupby(["Category (L1)", "Subcategory (L2)"]):
        counts = [int((g["Month"] == m).sum()) for m in months]
        rg = resolved[(resolved["Category (L1)"] == cat) &
                      (resolved["Subcategory (L2)"] == sub)]
        hrs = rg["Resolution Hours"]
        p10 = float(hrs.quantile(0.10)) if len(rg) else 0.0
        p90 = float(hrs.quantile(0.90)) if len(rg) else 0.0
        p12 = g["Priority"].isin(["P1 - Critical", "P2 - High"]).sum()
        l2.append({
            "parent": cat,
            "name": sub,
            "counts": counts,
            "total": int(len(g)),
            "share_pct": pct(len(g), len(df)),
            "mom_change": counts[-1] - counts[-2],
            "mom_change_pct": pct(counts[-1] - counts[-2], counts[-2]),
            "first_to_last_pct": pct(counts[-1] - counts[0], counts[0]),
            "median_hours": round(float(hrs.median()), 2) if len(rg) else 0.0,
            "p10_hours": round(p10, 2),
            "p90_hours": round(p90, 2),
            "spread_hours": round(p90 - p10, 2),
            "agent_hours_total": round(float(hrs.sum()), 1) if len(rg) else 0.0,
            "agent_hours_per_month": round(float(hrs.sum()) / len(months), 1) if len(rg) else 0.0,
            "sla_met_pct": pct((rg["SLA Met"] == "Yes").sum(), len(rg)),
            "reopen_pct": pct((rg["Reopened"] == "Yes").sum(), len(rg)),
            "p1p2_share_pct": pct(p12, len(g)),
            "assignment_group": g["Assignment Group"].mode().iat[0],
            "self_service_pct": pct((g["Channel"] == "Self-Service Portal").sum(), len(g)),
        })
    l2.sort(key=lambda r: -r["total"])

    # ---------- L3, with real ticket examples for the drill-down ----------
    l3 = []
    for (cat, sub, iss), g in df.groupby(["Category (L1)", "Subcategory (L2)",
                                          "Issue Type (L3)"]):
        rg = resolved[resolved["Issue Type (L3)"] == iss]
        l3.append({
            "parent_l1": cat, "parent_l2": sub, "name": iss,
            "counts": [int((g["Month"] == m).sum()) for m in months],
            "total": int(len(g)),
            "median_hours": round(float(rg["Resolution Hours"].median()), 2) if len(rg) else 0.0,
            "examples": [
                {"id": r["Ticket ID"], "month": MONTH_LABEL[r["Month"]],
                 "desc": r["Description"], "priority": r["Priority"],
                 "confidence": r["Confidence"], "reason": r["Reason"],
                 "hours": None if pd.isna(r["Resolution Hours"]) else float(r["Resolution Hours"])}
                for _, r in g.head(4).iterrows()],
        })
    l3.sort(key=lambda r: -r["total"])

    # ---------- automation shortlist ----------
    shortlist, near_miss = [], []
    for r in l2:
        checks = {
            "volume": bool(r["counts"][-1] >= SHORTLIST["min_tickets_latest_month"]),
            "spread": bool(r["spread_hours"] <= SHORTLIST["max_spread_hours"]),
            "routine": bool(r["p1p2_share_pct"] <= SHORTLIST["max_p1p2_share_pct"]),
        }
        row = {**r, "checks": checks, "checks_passed": sum(checks.values())}
        if all(checks.values()):
            shortlist.append(row)
        elif sum(checks.values()) == 2:
            near_miss.append(row)
    shortlist.sort(key=lambda r: -r["agent_hours_per_month"])
    near_miss.sort(key=lambda r: -r["agent_hours_per_month"])

    # ---------- where the hours actually go (separate from the shortlist) ----------
    effort = sorted(l2, key=lambda r: -r["agent_hours_per_month"])[:8]

    # ---------- SLA pressure ----------
    sla = sorted([r for r in l2 if r["total"] >= 10], key=lambda r: r["sla_met_pct"])[:8]

    channels = df["Channel"].value_counts()
    metrics = {
        "generated_for": "Jan 2026 to Mar 2026",
        "headline": headline,
        "l1": l1, "l2": l2, "l3": l3,
        "shortlist_rule": SHORTLIST,
        "shortlist": shortlist,
        "near_miss": near_miss,
        "effort": effort,
        "sla_pressure": sla,
        "channels": [{"name": k, "count": int(v), "share_pct": pct(int(v), len(df))}
                     for k, v in channels.items()],
        "accuracy": acc,
    }
    (DATA / "metrics.json").write_text(json.dumps(metrics, indent=2))

    print(f"Tickets {headline['total_tickets']} | "
          f"{' '.join(f'{m}={c}' for m, c in zip(headline['months'], headline['totals']))} "
          f"| MoM {headline['mom_change_pct']:+}%")
    print(f"SLA met {headline['sla_met_pct']}% | reopened {headline['reopen_pct']}% | "
          f"{headline['total_agent_hours']} agent-hours over 3 months\n")

    print(f"Shortlist rule: latest month >= {SHORTLIST['min_tickets_latest_month']} tickets, "
          f"spread <= {SHORTLIST['max_spread_hours']}h, "
          f"P1+P2 <= {SHORTLIST['max_p1p2_share_pct']}%\n")
    print("AUTOMATION SHORTLIST")
    for r in shortlist:
        print(f"  {r['parent']} > {r['name']:22} Mar={r['counts'][-1]:3}  "
              f"spread={r['spread_hours']:6.2f}h  P1P2={r['p1p2_share_pct']:5.1f}%  "
              f"{r['agent_hours_per_month']:6.1f} agent-hrs/mo  "
              f"trend {r['first_to_last_pct']:+.0f}%")
    print("\nNEAR MISS (2 of 3 checks)")
    for r in near_miss[:5]:
        failed = [k for k, v in r["checks"].items() if not v]
        print(f"  {r['parent']} > {r['name']:22} fails: {', '.join(failed)}  "
              f"{r['agent_hours_per_month']:6.1f} agent-hrs/mo")
    print("\nWHERE THE HOURS GO (top 5, not the same question as automation)")
    for r in effort[:5]:
        print(f"  {r['parent']} > {r['name']:22} {r['agent_hours_per_month']:6.1f} "
              f"agent-hrs/mo  spread={r['spread_hours']:.1f}h")
    print(f"\nWrote {DATA / 'metrics.json'}")


if __name__ == "__main__":
    main()
