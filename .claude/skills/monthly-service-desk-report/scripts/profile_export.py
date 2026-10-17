"""Profile a service desk export before anything else touches it.

Answers the questions that decide how the run goes: which sheets exist, how many tickets per
month, which columns are blank, whether categories are already filled (and so must be ignored),
whether an answer key exists to score against, and whether a Taxonomy sheet in the export agrees
with the taxonomy JSON the classifier will use.

    python3 profile_export.py --input export.xlsx --taxonomy tax.json [--json out.json]
"""
import argparse
import json
import sys
from pathlib import Path

import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "ticket-category-analysis" / "scripts"))
import taxonomy_io  # noqa: E402

CAT_COLS = ["Category (L1)", "Subcategory (L2)", "Issue Type (L3)"]
REQUIRED = ["Ticket ID", "Month", "Description"]
OPTIONAL = ["Short Description", "Priority", "Assignment Group", "Resolution Hours", "SLA Met",
            "Reopened", "Department", "Channel"]


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--input", required=True)
    ap.add_argument("--taxonomy", required=True)
    ap.add_argument("--sheet", default="Tickets")
    ap.add_argument("--json", default=None, help="also write the profile here")
    a = ap.parse_args()

    xl = pd.ExcelFile(a.input)
    out = {"file": Path(a.input).name, "sheets": {}}
    for s in xl.sheet_names:
        out["sheets"][s] = int(len(pd.read_excel(xl, s)))
    if a.sheet not in xl.sheet_names:
        raise SystemExit(f"No '{a.sheet}' sheet. Sheets: {xl.sheet_names}. Pass --sheet.")

    t = pd.read_excel(xl, a.sheet)
    t["Month"] = t["Month"].astype(str)
    out["tickets"] = int(len(t))
    out["months"] = t["Month"].value_counts().sort_index().to_dict()
    out["missing_required"] = [c for c in REQUIRED if c not in t.columns]
    out["missing_optional"] = [c for c in OPTIONAL if c not in t.columns]
    out["blank_counts"] = {c: int(n) for c, n in t.isna().sum().items() if n}
    present = [c for c in CAT_COLS if c in t.columns]
    out["categories_prefilled"] = bool(present) and int(t[present].notna().any(axis=1).sum()) > 0
    out["answer_key"] = "Answer Key" in xl.sheet_names

    tax = taxonomy_io.load(a.taxonomy)
    json_paths = set(taxonomy_io.allowed_paths(tax))
    out["taxonomy_json_paths"] = len(json_paths)
    if "Taxonomy" in xl.sheet_names:
        x = pd.read_excel(xl, "Taxonomy")
        sheet_paths = {" > ".join(str(r[c]).strip() for c in CAT_COLS) for _, r in x.iterrows()
                       if all(pd.notna(r.get(c)) for c in CAT_COLS)}
        out["taxonomy_sheet_paths"] = len(sheet_paths)
        out["taxonomy_only_in_sheet"] = sorted(sheet_paths - json_paths)
        out["taxonomy_only_in_json"] = sorted(json_paths - sheet_paths)

    print(f"File      : {out['file']}")
    print(f"Sheets    : " + ", ".join(f"{k} ({v} rows)" for k, v in out["sheets"].items()))
    print(f"Tickets   : {out['tickets']}  | by month: {out['months']}")
    if out["missing_required"]:
        print(f"STOP      : required columns missing: {out['missing_required']}. Use --column-map.")
    if out["missing_optional"]:
        print(f"Degraded  : no {out['missing_optional']}, those report sections shrink")
    print(f"Blanks    : {out['blank_counts'] or 'none'}")
    print(f"Prefilled : {'YES, categories already filled. Exclude them from classification and say so.' if out['categories_prefilled'] else 'no, categories are blank, classify all'}")
    print(f"Answer key: {'yes, accuracy will be measured' if out['answer_key'] else 'NO, accuracy will print as not measured'}")
    if "taxonomy_sheet_paths" in out:
        same = not out["taxonomy_only_in_sheet"] and not out["taxonomy_only_in_json"]
        print(f"Taxonomy  : sheet {out['taxonomy_sheet_paths']} paths vs JSON {len(json_paths)}: "
              + ("identical" if same else "DIFFERENT, reconcile before classifying"))
        for p in out["taxonomy_only_in_sheet"][:10]:
            print(f"   only in sheet: {p}")
        for p in out["taxonomy_only_in_json"][:10]:
            print(f"   only in JSON : {p}")
    if a.json:
        Path(a.json).write_text(json.dumps(out, indent=2))


if __name__ == "__main__":
    main()
