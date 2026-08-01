"""
Normalise, deduplicate, and write classification batches.

The deduplication is what keeps this affordable. A service desk gets the same
complaint worded the same way over and over, so after normalising, identical
descriptions collapse into one CASE. Classify the case once, fan the answer out to
every ticket that shares it.

Usage:
  python3 prepare_batches.py --taxonomy tax.json --input tickets.xlsx --work-dir work/
"""

import argparse
import re
from pathlib import Path

import pandas as pd

import taxonomy_io
from ticket_columns import apply_column_map, check_columns

FILLER_PREFIX = re.compile(
    r"^(hi team|hello|hi|team|good morning|good afternoon|dear team|greetings|"
    r"raising this again|second time reporting this|following up|fyi)\b[,\s]*", re.I)
FILLER_SUFFIX = re.compile(
    r"\b(please help|kindly look into it urgently|need this today|this is blocking my work|"
    r"thanks in advance|thanks|thank you|regards|let me know if you need anything from my side|"
    r"appreciate a quick fix|asap|urgent)\s*[.!]*\s*$", re.I)
TYPO_FIX = {"teh": "the", "adn": "and", "plz": "please", "cannt": "cannot",
            "workign": "working", "sytem": "system", "nto": "not", "mornign": "morning",
            "acces": "access", "agian": "again", "recieve": "receive", "occured": "occurred"}


def normalise(text):
    t = str(text).lower().strip()
    for _ in range(3):                       # greetings and sign-offs often stack
        t = FILLER_SUFFIX.sub("", FILLER_PREFIX.sub("", t).strip()).strip()
    t = re.sub(r"[^\w\s]", " ", t)
    return " ".join(TYPO_FIX.get(w, w) for w in t.split())


def main():
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--taxonomy", required=True)
    ap.add_argument("--input", required=True, help="the ticket export (.xlsx or .csv)")
    ap.add_argument("--work-dir", required=True)
    ap.add_argument("--sheet", default="Tickets")
    ap.add_argument("--batch-size", type=int, default=40)
    ap.add_argument("--column-map", default="", help="'Their Name=Our Name,...'")
    a = ap.parse_args()

    tax = taxonomy_io.load(a.taxonomy)
    src = Path(a.input)
    df = (pd.read_csv(src) if src.suffix.lower() == ".csv"
          else pd.read_excel(src, sheet_name=a.sheet))
    df = apply_column_map(df, a.column_map)
    degraded = check_columns(df)

    work = Path(a.work_dir)
    batches = work / "batches"
    batches.mkdir(parents=True, exist_ok=True)
    for f in batches.glob("*.md"):
        f.unlink()

    df["_norm"] = df["Description"].map(normalise)
    has = lambda c: c in df.columns
    agg = {"tickets_in_case": ("Ticket ID", "count"),
           "sample_desc": ("Description", "first")}
    if has("Short Description"):
        agg["sample_short"] = ("Short Description", "first")
    if has("Department"):
        agg["departments"] = ("Department", lambda s: ", ".join(sorted(set(s.astype(str)))[:4]))
    if has("Channel"):
        agg["channels"] = ("Channel", lambda s: ", ".join(sorted(set(s.astype(str)))[:4]))

    cases = (df.groupby("_norm").agg(**agg).reset_index()
             .sort_values("tickets_in_case", ascending=False).reset_index(drop=True))
    cases.insert(0, "case_id", [f"C{i + 1:03d}" for i in range(len(cases))])

    paths = taxonomy_io.allowed_paths(tax)
    n_batches = max(1, (len(cases) + a.batch_size - 1) // a.batch_size)

    for b in range(n_batches):
        chunk = cases.iloc[b * a.batch_size:(b + 1) * a.batch_size]
        lines = [
            f"# Classification batch {b + 1} of {n_batches}",
            "",
            f"Domain: {tax.get('domain', 'tickets')}.",
            "",
            "Assign every case below to exactly one path from the allowed list.",
            "Return one JSON object per line, nothing else:",
            '`{"case_id":"C001","path":"L1 > L2 > L3","confidence":"High|Medium|Low",'
            '"reason":"one short line"}`',
            "",
            "Rules, and the reason each one exists:",
            "1. The path must match the allowed list character for character. The next script "
            "rejects anything else rather than silently accepting an invented category.",
            "2. If nothing fits, return `UNCATEGORIZED` with confidence `Low`. A forced fit is "
            "worse than an honest gap, because it hides in the numbers where nobody sees it.",
            "3. `Low` confidence means a human must review it. You are allowed to not know.",
            "4. Judge only from what the user wrote. Do not assume a team, a system or a cause "
            "that is not in the text.",
            "5. `reason` is one short line a service desk manager could read and agree or "
            "disagree with. It is what makes the classification auditable.",
            "",
            "## Allowed paths",
            "",
        ]
        lines += [f"- {p}" for p in paths]
        lines += ["", "## Cases", ""]
        for _, r in chunk.iterrows():
            n = r.tickets_in_case
            lines.append(f"### {r.case_id}  (covers {n} ticket{'s' if n != 1 else ''})")
            if "sample_short" in cases.columns:
                lines.append(f"- Short description: {r.sample_short}")
            lines.append(f"- Description: {r.sample_desc}")
            if "departments" in cases.columns:
                lines.append(f"- Departments: {r.departments}")
            if "channels" in cases.columns:
                lines.append(f"- Channels: {r.channels}")
            lines.append("")
        (batches / f"batch-{b + 1:02d}.md").write_text("\n".join(lines))

    cases.to_json(work / "cases.json", orient="records", indent=2)
    df[["Ticket ID", "_norm"]].to_json(work / "ticket_case_map.json", orient="records")

    saved = len(df) - len(cases)
    print(f"Tickets            : {len(df)}")
    print(f"Unique cases       : {len(cases)}")
    print(f"Classification work: {saved} fewer calls "
          f"({100 * saved / max(1, len(df)):.1f}% saved by deduplicating)")
    print(f"Batches            : {n_batches} of up to {a.batch_size} -> {batches}")
    if degraded:
        print(f"\nNot present in the export, so those report sections will be skipped: "
              f"{', '.join(degraded)}")
    print(f"\nNext: read each file in {batches}, then write one JSON object per case to "
          f"{work / 'classified.jsonl'}")


if __name__ == "__main__":
    main()
