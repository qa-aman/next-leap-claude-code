"""
The one place ticket numbers are computed.

The dashboard, the console summary and the PowerPoint deck all read from here. If
each surface computed its own totals they would drift, and the version management
sees would quietly stop matching the version the analyst is looking at. One function,
three consumers.

The dashboard also recomputes client-side so its filters work on the raw rows. That
JavaScript is checked against this module's output rather than trusted, because two
implementations of the same arithmetic is exactly how a report starts lying.
"""

import pandas as pd

L1, L2, L3 = "Category (L1)", "Subcategory (L2)", "Issue Type (L3)"
MONTH_NAMES = ["Jan", "Feb", "Mar", "Apr", "May", "Jun",
               "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]

SHORTLIST = {
    "min_tickets_latest_month": 12,   # below this, automation costs more than it saves
    "max_spread_hours": 3.0,          # P90 minus P10. Tight spread = same fix every time
    "max_p1p2_share_pct": 25.0,       # routine work, not incident firefighting
}
SMALL_SAMPLE = 10                     # fewer resolved tickets than this and a median is noise

OPTIONAL_DEFAULTS = [
    ("Resolution Hours", None), ("Priority", "P3 - Moderate"), ("SLA Met", ""),
    ("Reopened", "No"), ("Channel", "Unknown"), ("Department", "Unknown"),
    ("Assignment Group", "Service Desk"), ("Short Description", ""),
    ("Confidence", "High"), ("Reason", ""),
]


def label_month(m):
    s = str(m)
    try:
        return f"{MONTH_NAMES[int(s[5:7]) - 1]} {s[:4]}"
    except (ValueError, IndexError):
        return s


def pct(a, b):
    return round(100 * a / b, 1) if b else 0.0


def load(path, sheet="Tickets"):
    """Read the categorized workbook and fill in whatever the export did not carry,
    so a thin export produces a thinner report rather than a stack trace."""
    df = pd.read_excel(path, sheet_name=sheet)
    for c in (L1, L2, L3):
        if c not in df.columns:
            raise SystemExit(f"'{c}' is missing. Run apply_classification.py first.")
    for col, default in OPTIONAL_DEFAULTS:
        if col not in df.columns:
            df[col] = default
    df["Month"] = df["Month"].astype(str)
    df["Resolution Hours"] = pd.to_numeric(df["Resolution Hours"], errors="coerce")
    months = sorted(df["Month"].unique())
    return df, months


def compute(df, months, rule=None):
    rule = rule or dict(SHORTLIST)
    nm = len(months)
    res = df[df["Resolution Hours"].notna()]
    per_month = df.groupby("Month").size().reindex(months, fill_value=0)

    headline = {
        "months": [label_month(m) for m in months],
        "totals": [int(per_month[m]) for m in months],
        "total": int(len(df)),
        "resolved": int(len(res)),
        "open": int(df["Resolution Hours"].isna().sum()),
        "mom_change": int(per_month.iloc[-1] - per_month.iloc[-2]) if nm > 1 else 0,
        "mom_change_pct": pct(per_month.iloc[-1] - per_month.iloc[-2],
                              per_month.iloc[-2]) if nm > 1 else 0.0,
        "first_to_last_pct": pct(per_month.iloc[-1] - per_month.iloc[0],
                                 per_month.iloc[0]) if nm > 1 else 0.0,
        "sla_met_pct": pct((res["SLA Met"] == "Yes").sum(), len(res)),
        "reopen_pct": pct((res["Reopened"] == "Yes").sum(), len(res)),
        "agent_hours": round(float(res["Resolution Hours"].sum()), 1),
        "agent_hours_per_month": round(float(res["Resolution Hours"].sum()) / nm, 1),
    }

    def per_month_counts(g):
        return [int((g["Month"] == m).sum()) for m in months]

    l1 = []
    for cat, g in df.groupby(L1):
        rg = res[res[L1] == cat]
        c = per_month_counts(g)
        l1.append({
            "name": cat, "counts": c, "total": len(g), "share_pct": pct(len(g), len(df)),
            "mom_change": c[-1] - c[-2] if nm > 1 else 0,
            "first_to_last_pct": pct(c[-1] - c[0], c[0]) if nm > 1 and c[0] else 0.0,
            "sla_met_pct": pct((rg["SLA Met"] == "Yes").sum(), len(rg)),
            "agent_hours_per_month": round(float(rg["Resolution Hours"].sum()) / nm, 1),
        })
    l1.sort(key=lambda r: -r["total"])

    l2 = []
    for (cat, sub), g in df.groupby([L1, L2]):
        rg = res[(res[L1] == cat) & (res[L2] == sub)]
        h = rg["Resolution Hours"]
        c = per_month_counts(g)
        p10 = float(h.quantile(0.10)) if len(rg) else 0.0
        p90 = float(h.quantile(0.90)) if len(rg) else 0.0
        p12 = int(g["Priority"].astype(str).str.upper().str.startswith(("P1", "P2")).sum())
        portal = int(g["Channel"].astype(str).str.lower()
                     .str.contains("portal|self", regex=True, na=False).sum())
        row = {
            "parent": cat, "name": sub, "counts": c, "total": len(g),
            "latest": c[-1], "share_pct": pct(len(g), len(df)),
            "first_to_last_pct": pct(c[-1] - c[0], c[0]) if nm > 1 and c[0] else 0.0,
            "median_hours": round(float(h.median()), 2) if len(rg) else 0.0,
            "spread_hours": round(p90 - p10, 2),
            "agent_hours_per_month": round(float(h.sum()) / nm, 1) if len(rg) else 0.0,
            "sla_met_pct": pct((rg["SLA Met"] == "Yes").sum(), len(rg)),
            "reopen_pct": pct((rg["Reopened"] == "Yes").sum(), len(rg)),
            "p1p2_share_pct": pct(p12, len(g)),
            "portal_share_pct": pct(portal, len(g)),
            "resolved": len(rg),
            "small_sample": len(rg) < SMALL_SAMPLE,
            "group": g["Assignment Group"].mode().iat[0] if len(g) else "Service Desk",
        }
        row["checks"] = {
            "volume": bool(row["latest"] >= rule["min_tickets_latest_month"]),
            "spread": bool(row["spread_hours"] <= rule["max_spread_hours"]),
            "routine": bool(row["p1p2_share_pct"] <= rule["max_p1p2_share_pct"]),
        }
        row["checks_passed"] = sum(row["checks"].values())
        l2.append(row)
    l2.sort(key=lambda r: -r["total"])

    key = lambda r: (-r["agent_hours_per_month"], -r["resolved"], r["name"])
    shortlist = sorted([r for r in l2 if r["checks_passed"] == 3], key=key)
    near_miss = sorted([r for r in l2 if r["checks_passed"] == 2], key=key)
    effort = sorted(l2, key=key)[:8]
    sla = sorted([r for r in l2 if r["resolved"] >= SMALL_SAMPLE],
                 key=lambda r: (r["sla_met_pct"], -r["resolved"], r["name"]))[:8]

    return {"months": months, "month_labels": [label_month(m) for m in months],
            "headline": headline, "l1": l1, "l2": l2, "rule": rule,
            "shortlist": shortlist, "near_miss": near_miss,
            "effort": effort, "sla_pressure": sla, "small_sample": SMALL_SAMPLE}
