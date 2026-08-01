"""
Generate a realistic sample ticket export from any taxonomy.

Use this when there is no real export yet and you need to put a working report in
front of a stakeholder before the data exists. The output has the same shape as a
real export, so every downstream step is identical either way.

Three sheets:
  Tickets    - the export, with the three category columns deliberately BLANK
  Answer Key - the true path per ticket, held back so accuracy can be measured
  Taxonomy   - the reference

The descriptions are written the way people actually type into a portal: lowercase,
typos, filler, and no mention of the category name. A description that says
"password reset needed" is trivial to classify. "cant get in since morning" is the
real job, and a sample set that skips that teaches you nothing.

Usage:
  python3 generate_sample.py --taxonomy it-service-desk.json --out tickets.xlsx
  python3 generate_sample.py --taxonomy hr.json --months 2026-01 2026-02 2026-03 \
      --per-month 140 150 160 --out tickets.xlsx
"""

import argparse
import random
from datetime import datetime, timedelta
from pathlib import Path

import pandas as pd

import taxonomy_io
from ticket_columns import CHANNELS, PRIORITIES, SLA_TARGET, style_workbook

DEFAULT_MONTHS = ["2026-01", "2026-02", "2026-03"]
DEFAULT_PER_MONTH = [140, 150, 160]

DEPARTMENTS = ["Sales", "Finance", "Human Resources", "Operations", "Engineering",
               "Customer Success", "Marketing", "Legal", "Procurement", "Manufacturing"]
FIRST = ["Priya", "Rahul", "Anita", "Vikram", "Sneha", "Arjun", "Meera", "Karan", "Divya",
         "Rohit", "Fatima", "Daniel", "Grace", "Miguel", "Chloe", "Tobias", "Ayesha",
         "Nikhil", "Laura", "Omar", "Ingrid", "Samuel", "Nadia", "Peter"]
LAST = ["Sharma", "Iyer", "Nair", "Bose", "Kapoor", "Menon", "Reddy", "Joshi", "Okafor",
        "Silva", "Novak", "Fischer", "Dubois", "Rossi", "Andersen", "Haddad", "Kowalski",
        "Tanaka", "Mensah", "Ferreira"]

PREFIX = ["", "", "", "hi team, ", "hello, ", "hi, ", "team, ", "good morning, ",
          "raising this again, ", "second time reporting this, "]
SUFFIX = ["", "", "", "", " please help", " kindly look into it urgently", " need this today",
          " this is blocking my work", " thanks in advance",
          " let me know if you need anything from my side", " appreciate a quick fix"]
VAGUE_SHORT = ["Issue", "Not working", "Urgent help needed", "Please assist", "Request",
               "System problem", "Need support", "IT issue"]
TYPO_MAP = {"the": "teh", "and": "adn", "please": "plz", "cannot": "cannt",
            "working": "workign", "system": "sytem", "not": "nto", "morning": "mornign",
            "access": "acces", "again": "agian"}

CHANNEL_MIX = ["Self-Service Portal"] * 46 + ["Email"] * 27 + ["Phone"] * 18 + ["Chat"] * 9
DEFAULTS = {"weight": 4.0, "median_hours": 6.0, "sigma": 0.8,
            "priority_mix": [1, 18, 55, 26], "reopen_rate": 0.04}


def add_noise(text, rng):
    out = rng.choice(PREFIX) + text + rng.choice(SUFFIX)
    if rng.random() < 0.35:
        words = out.split()
        for i, w in enumerate(words):
            if w in TYPO_MAP and rng.random() < 0.5:
                words[i] = TYPO_MAP[w]
        out = " ".join(words)
    if rng.random() < 0.12:
        out = out.upper()
    return out


def short_desc(text, rng):
    if rng.random() < 0.32:
        return rng.choice(VAGUE_SHORT)
    return " ".join(text.split()[:6]).rstrip(",.").capitalize()


def month_multiplier(sim, month, months):
    """A trend multiplier can be keyed by month ("2026-01") or by position in the
    window ("1", "2", "3").

    Position keys are what make a taxonomy reusable. A taxonomy whose multipliers are
    written as absolute months only produces a trend for the one quarter someone had in
    mind when they wrote it, and every later window silently comes out flat. Flat is not
    obviously wrong when you look at it, which is what makes it worth preventing here.
    """
    mm = sim.get("monthly_multiplier") or {}
    if month in mm:
        return mm[month]
    return mm.get(str(months.index(month) + 1), 1.0)


def business_datetime(month, rng):
    y, m = int(month[:4]), int(month[5:7])
    last = [31, 29 if y % 4 == 0 and (y % 100 or y % 400 == 0) else 28, 31, 30, 31, 30,
            31, 31, 30, 31, 30, 31][m - 1]
    while True:
        dt = datetime(y, m, rng.randint(1, last))
        if dt.weekday() < 5:
            break
    hour = rng.choices(range(8, 19), weights=[6, 12, 14, 11, 9, 7, 9, 10, 8, 5, 3])[0]
    return dt.replace(hour=hour, minute=rng.randint(0, 59))


def build(tax, months, per_month, seed, open_rate=0.09):
    rng = random.Random(seed)
    by_l2, missing = {}, []
    for l1, l2, l3, ph, group, sim in taxonomy_io.leaves(tax):
        key = (l1, l2)
        by_l2.setdefault(key, {"group": group, "sim": sim, "issues": []})
        if not ph:
            missing.append(f"{l1} > {l2} > {l3}")
        by_l2[key]["issues"].append((l3, ph))
    if missing:
        raise SystemExit(
            f"{len(missing)} issue types have no example phrasings, so a sample cannot be "
            f"generated from this taxonomy. Add at least one phrasing to each, for example:\n  "
            + "\n  ".join(missing[:8]))

    rows, key_rows, counter = [], [], 1045200
    for month, target in zip(months, per_month):
        weighted = []
        for key, meta in by_l2.items():
            sim = meta["sim"]
            w = sim.get("weight", DEFAULTS["weight"])
            w *= month_multiplier(sim, month, months)
            weighted.append((key, w))
        total = sum(w for _, w in weighted)
        picks = rng.choices([k for k, _ in weighted],
                            weights=[w / total for _, w in weighted], k=target)

        for key in picks:
            (l1, l2), meta = key, by_l2[key]
            sim = meta["sim"]
            l3, phrasings = rng.choice(meta["issues"])
            raw = rng.choice(phrasings)

            counter += rng.randint(1, 4)
            tid = f"INC{counter:07d}"
            opened = business_datetime(month, rng)
            priority = rng.choices(PRIORITIES,
                                   weights=sim.get("priority_mix", DEFAULTS["priority_mix"]))[0]
            med = sim.get("median_hours", DEFAULTS["median_hours"])
            sig = sim.get("sigma", DEFAULTS["sigma"])
            hours = round(max(0.15, med * rng.lognormvariate(0, sig)), 2)

            still_open = month == months[-1] and rng.random() < open_rate
            if still_open:
                state = rng.choice(["In Progress", "On Hold", "New"])
                resolved, hours_out, sla_met = "", "", ""
            else:
                state = rng.choices(["Resolved", "Closed"], weights=[35, 65])[0]
                resolved = opened + timedelta(hours=hours)
                hours_out = hours
                sla_met = "Yes" if hours <= SLA_TARGET[priority] else "No"

            reopened = "Yes" if (not still_open and
                                 rng.random() < sim.get("reopen_rate",
                                                        DEFAULTS["reopen_rate"])) else "No"
            rows.append({
                "Ticket ID": tid,
                "Opened Date": opened.strftime("%d-%m-%Y %H:%M"),
                "Month": month,
                "Requester": f"{rng.choice(FIRST)} {rng.choice(LAST)}",
                "Department": rng.choice(DEPARTMENTS),
                "Channel": rng.choice(CHANNEL_MIX),
                "Short Description": short_desc(raw, rng),
                "Description": add_noise(raw, rng),
                "Priority": priority,
                "Assignment Group": meta["group"],
                "State": state,
                "Resolved Date": resolved.strftime("%d-%m-%Y %H:%M") if resolved else "",
                "Resolution Hours": hours_out,
                "SLA Target Hours": SLA_TARGET[priority],
                "SLA Met": sla_met,
                "Reopened": reopened,
                "Category (L1)": "", "Subcategory (L2)": "", "Issue Type (L3)": "",
            })
            key_rows.append({"Ticket ID": tid, "Month": month, "True Category (L1)": l1,
                             "True Subcategory (L2)": l2, "True Issue Type (L3)": l3})

    tickets = (pd.DataFrame(rows)
               .sort_values("Opened Date",
                            key=lambda s: pd.to_datetime(s, format="%d-%m-%Y %H:%M"))
               .reset_index(drop=True))
    key = (pd.DataFrame(key_rows).set_index("Ticket ID")
           .loc[tickets["Ticket ID"]].reset_index())
    tax_df = pd.DataFrame([
        {"Category (L1)": l1, "Subcategory (L2)": l2, "Issue Type (L3)": l3,
         "Assignment Group": g, "Example Phrasing": ph[0] if ph else ""}
        for l1, l2, l3, ph, g, _ in taxonomy_io.leaves(tax)])
    return tickets, key, tax_df


def main():
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--taxonomy", required=True)
    ap.add_argument("--out", required=True)
    ap.add_argument("--months", nargs="+", default=DEFAULT_MONTHS,
                    help="YYYY-MM, oldest first")
    ap.add_argument("--per-month", nargs="+", type=int, default=None)
    ap.add_argument("--seed", type=int, default=20260317,
                    help="fixed so re-running gives an identical file")
    a = ap.parse_args()

    per_month = a.per_month or (DEFAULT_PER_MONTH if a.months == DEFAULT_MONTHS
                                else [150] * len(a.months))
    if len(per_month) != len(a.months):
        raise SystemExit(f"--per-month needs {len(a.months)} numbers, one per month.")

    tax = taxonomy_io.load(a.taxonomy)
    tickets, key, tax_df = build(tax, a.months, per_month, a.seed)

    out = Path(a.out)
    out.parent.mkdir(parents=True, exist_ok=True)
    with pd.ExcelWriter(out, engine="openpyxl") as xl:
        tickets.to_excel(xl, sheet_name="Tickets", index=False)
        key.to_excel(xl, sheet_name="Answer Key", index=False)
        tax_df.to_excel(xl, sheet_name="Taxonomy", index=False)
        style_workbook(xl.book)

    print(f"Wrote {out}")
    print(f"  {len(tickets)} tickets across {len(a.months)} months: "
          + ", ".join(f"{m}={n}" for m, n in zip(a.months, per_month)))
    print("\nTrue category mix:")
    print(key["True Category (L1)"].value_counts().to_string())
    print("\nThe three category columns are blank on purpose. That is the problem to solve.")


if __name__ == "__main__":
    main()
