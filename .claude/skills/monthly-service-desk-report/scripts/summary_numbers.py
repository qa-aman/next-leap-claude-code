"""Recompute the executive summary's numbers in pandas, independently of the page.

The page computes its summary in the browser. This script computes the same four pointers from
the categorized workbook with different code, so a mismatch between the two exposes a bug in
either. Compare its output line by line with the summary text read back from the page.

    python3 summary_numbers.py --input categorized.xlsx
"""
import argparse

import pandas as pd


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--input", required=True)
    ap.add_argument("--sheet", default="Tickets")
    a = ap.parse_args()
    t = pd.read_excel(a.input, sheet_name=a.sheet)
    t["Month"] = t["Month"].astype(str)
    months = sorted(t["Month"].unique())
    first, prev, last = months[0], months[-2] if len(months) > 1 else months[0], months[-1]
    res = t[t["Resolution Hours"].notna()]
    sla = lambda d: (d["SLA Met"] == "Yes").sum(), lambda d: d["SLA Met"].notna().sum()
    ok, n = sla[0](res), sla[1](res)

    pm = t.groupby("Month").size()
    print(f"Demand   : {pm[first]} -> {pm[last]} ({(pm[last]-pm[first])/pm[first]*100:+.1f}%)")
    c = t.groupby(["Category (L1)", "Month"]).size().unstack(fill_value=0)
    d = (c[last] - c[prev]).sort_values(ascending=False)
    print(f"           top mover {d.index[0]} {d.iloc[0]:+d} in {last} vs {prev}")

    g = res.groupby("Subcategory (L2)").agg(n=("Ticket ID", "size"), hrs=("Resolution Hours", "sum"))
    top = g[g.n >= 10].sort_values("hrs", ascending=False).head(2)

    p1 = res[res["Priority"].astype(str).str.startswith("P1")]
    p1pct = sla[0](p1) / max(1, sla[1](p1)) * 100
    if len(p1) and p1pct < ok / n * 100:
        print(f"Risk     : P1 met SLA {sla[0](p1)} of {sla[1](p1)} ({p1pct:.1f}%) vs overall {ok/n*100:.1f}%")
    else:
        rest = res[res["Subcategory (L2)"].isin(g[(g.n >= 10) & ~g.index.isin(top.index)].index)]
        w = rest.groupby("Subcategory (L2)")["SLA Met"].apply(lambda x: (x == "Yes").mean() * 100).sort_values()
        wn = rest[rest["Subcategory (L2)"] == w.index[0]]
        print(f"Risk     : P1 on track {sla[0](p1)} of {sla[1](p1)} ({p1pct:.1f}%); worst SLA {w.index[0]} "
              f"{sla[0](wn)} of {sla[1](wn)} ({w.iloc[0]:.1f}%) vs overall {ok/n*100:.1f}%")
    rows = t[t["Subcategory (L2)"].isin(top.index)]
    r2 = res[res["Subcategory (L2)"].isin(top.index)]
    print(f"Effort   : {', '.join(top.index)} = {top.hrs.sum()/res['Resolution Hours'].sum()*100:.1f}% of hours, "
          f"SLA {sla[0](r2)/max(1,sla[1](r2))*100:.1f}%, {len(rows)/len(t)*100:.1f}% of volume")

    sub = t.groupby("Subcategory (L2)").size().sort_values(ascending=False)
    print(f"Decision : largest subcategory {sub.index[0]} = {sub.iloc[0]} of {len(t)} "
          f"(1 in {round(len(t)/sub.iloc[0])}); check it matches the page's shortlist pick")


if __name__ == "__main__":
    main()
