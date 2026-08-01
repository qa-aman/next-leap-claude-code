"""
Fan the case answers back out to every ticket, validate them, and score them.

Three gates run here, and the third one is why this step exists at all. Without a
measured accuracy the report is a set of numbers with no idea whether the categories
underneath them are right, and every finding downstream is an assertion rather than
a measurement.

  1. Coverage - every case classified, exactly once
  2. Validity - every path exists in the taxonomy, character for character
  3. Accuracy - compared against an answer key, if one exists

Gate 3 is skipped with a loud warning when there is no answer key, which is the
normal situation on a first run against real data. Skipping it is fine. Pretending
it passed is not.

Usage:
  python3 apply_classification.py --taxonomy tax.json --input tickets.xlsx \
      --work-dir work/ --out categorized.xlsx
"""

import argparse
import json
from pathlib import Path

import pandas as pd

import taxonomy_io
from ticket_columns import apply_column_map, style_workbook

TRUE_COLS = {"L1": "True Category (L1)", "L2": "True Subcategory (L2)",
             "L3": "True Issue Type (L3)"}
PRED_COLS = {"L1": "Category (L1)", "L2": "Subcategory (L2)", "L3": "Issue Type (L3)"}


def read_answer_key(src, sheet="Answer Key"):
    try:
        key = pd.read_excel(src, sheet_name=sheet)
    except Exception:
        return None
    if "Ticket ID" not in key.columns or TRUE_COLS["L2"] not in key.columns:
        return None
    return key.drop(columns=[c for c in ["Month"] if c in key.columns])


def main():
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--taxonomy", required=True)
    ap.add_argument("--input", required=True)
    ap.add_argument("--work-dir", required=True)
    ap.add_argument("--out", required=True)
    ap.add_argument("--sheet", default="Tickets")
    ap.add_argument("--answer-key-sheet", default="Answer Key")
    ap.add_argument("--column-map", default="")
    a = ap.parse_args()

    tax = taxonomy_io.load(a.taxonomy)
    work, src = Path(a.work_dir), Path(a.input)
    cases = pd.read_json(work / "cases.json")
    tmap = pd.read_json(work / "ticket_case_map.json")
    df = (pd.read_csv(src) if src.suffix.lower() == ".csv"
          else pd.read_excel(src, sheet_name=a.sheet))
    df = apply_column_map(df, a.column_map)

    jsonl = work / "classified.jsonl"
    if not jsonl.exists():
        raise SystemExit(f"{jsonl} does not exist. Classify the batches in "
                         f"{work / 'batches'} first, one JSON object per line.")
    preds = []
    for i, line in enumerate(jsonl.read_text().splitlines(), 1):
        if not line.strip():
            continue
        try:
            preds.append(json.loads(line))
        except json.JSONDecodeError as e:
            raise SystemExit(f"{jsonl} line {i} is not valid JSON: {e}")
    preds = pd.DataFrame(preds)
    for col in ["case_id", "path", "confidence"]:
        if col not in preds.columns:
            raise SystemExit(f"classified.jsonl is missing the '{col}' field.")
    preds["reason"] = preds.get("reason", "")

    # ---- gate 1: coverage ----
    missing = sorted(set(cases.case_id) - set(preds.case_id))
    unknown = sorted(set(preds.case_id) - set(cases.case_id))
    if missing or unknown:
        raise SystemExit(f"Case mismatch.\n  Not classified: {missing[:12]}\n"
                         f"  Not in the case list: {unknown[:12]}")
    if preds.case_id.duplicated().any():
        dup = preds.case_id[preds.case_id.duplicated()].unique().tolist()
        raise SystemExit(f"Duplicate case_id in classified.jsonl: {dup[:12]}")

    # ---- gate 2: validity ----
    valid = set(taxonomy_io.allowed_paths(tax)) | {"UNCATEGORIZED"}
    bad = preds[~preds.path.isin(valid)]
    if len(bad):
        raise SystemExit("These paths are not in the taxonomy, character for character:\n" +
                         bad[["case_id", "path"]].to_string(index=False))

    parts = preds.path.str.split(taxonomy_io.SEP, expand=True)
    for i, (lvl, col) in enumerate(PRED_COLS.items()):
        preds[col] = parts[i].fillna("Uncategorized") if i in parts else "Uncategorized"

    out = (df.drop(columns=[c for c in PRED_COLS.values() if c in df.columns])
           .merge(tmap, on="Ticket ID")
           .merge(cases[["case_id", "_norm"]].merge(preds, on="case_id"), on="_norm", how="left")
           .drop(columns=["_norm"])
           .rename(columns={"confidence": "Confidence", "reason": "Reason",
                            "case_id": "Case ID"}))

    review = out[out.Confidence.isin(["Low", "Medium"])][
        [c for c in ["Ticket ID", "Month", "Short Description", "Description",
                     *PRED_COLS.values(), "Confidence", "Reason"] if c in out.columns]]

    accuracy = {
        "tickets": int(len(out)),
        "unique_cases": int(len(cases)),
        "dedup_saving_pct": round(100 * (1 - len(cases) / max(1, len(out))), 1),
        "uncategorized": int((out[PRED_COLS["L1"]] == "Uncategorized").sum()),
        "needs_review_tickets": int(len(review)),
        "scored": False,
    }

    # ---- gate 3: accuracy ----
    key = read_answer_key(src, a.answer_key_sheet)
    per_cat = by_conf = wrong = None
    if key is not None:
        truth = out.merge(key, on="Ticket ID")
        for lvl in PRED_COLS:
            truth[f"correct_{lvl}"] = truth[PRED_COLS[lvl]] == truth[TRUE_COLS[lvl]]
        n = len(truth)
        per_cat = (truth.groupby(TRUE_COLS["L1"])
                   .agg(tickets=("Ticket ID", "count"),
                        L1_correct_pct=("correct_L1", lambda s: round(100 * s.mean(), 1)),
                        L2_correct_pct=("correct_L2", lambda s: round(100 * s.mean(), 1)),
                        L3_correct_pct=("correct_L3", lambda s: round(100 * s.mean(), 1)))
                   .reset_index().rename(columns={TRUE_COLS["L1"]: PRED_COLS["L1"]}))
        by_conf = (truth.groupby("Confidence")
                   .agg(tickets=("Ticket ID", "count"),
                        L2_correct_pct=("correct_L2", lambda s: round(100 * s.mean(), 1)))
                   .reindex(["High", "Medium", "Low"]).dropna(how="all").reset_index())
        wrong = truth[~truth.correct_L2][
            ["Ticket ID", "Description", PRED_COLS["L2"], TRUE_COLS["L2"], "Confidence"]
        ].drop_duplicates(subset=["Description"])
        accuracy.update({
            "scored": True, "tickets_scored": int(n),
            "overall": {lvl: round(100 * truth[f"correct_{lvl}"].sum() / n, 1)
                        for lvl in PRED_COLS},
            "per_category": per_cat.to_dict(orient="records"),
            "by_confidence": by_conf.to_dict(orient="records"),
            "distinct_misclassified_cases": int(len(wrong)),
        })

    (work / "accuracy.json").write_text(json.dumps(accuracy, indent=2))
    dest = Path(a.out)
    dest.parent.mkdir(parents=True, exist_ok=True)
    with pd.ExcelWriter(dest, engine="openpyxl") as xl:
        out.to_excel(xl, sheet_name="Tickets", index=False)
        if per_cat is not None:
            per_cat.to_excel(xl, sheet_name="Accuracy", index=False)
        review.to_excel(xl, sheet_name="Needs Review", index=False)
        if wrong is not None:
            wrong.to_excel(xl, sheet_name="Misclassified", index=False)
        style_workbook(xl.book)

    print(f"Applied {len(preds)} case answers to {len(out)} tickets.")
    print(f"  Uncategorized : {accuracy['uncategorized']}")
    print(f"  Needs review  : {accuracy['needs_review_tickets']} "
          f"(Medium or Low confidence)")
    if accuracy["scored"]:
        o = accuracy["overall"]
        print(f"\nMeasured against the answer key:")
        print(f"  Category (L1)    : {o['L1']}%")
        print(f"  Subcategory (L2) : {o['L2']}%")
        print(f"  Issue type (L3)  : {o['L3']}%")
        print(f"\nBy confidence band (L2):\n{by_conf.to_string(index=False)}")
        if len(wrong):
            print(f"\n{len(wrong)} distinct descriptions landed in the wrong subcategory:")
            for _, r in wrong.head(12).iterrows():
                print(f"  [{r.Confidence:6}] {r[PRED_COLS['L2']]:24} should be "
                      f"{r[TRUE_COLS['L2']]:24} | {str(r.Description)[:56]}")
    else:
        print("\nNO ANSWER KEY FOUND, so accuracy was not measured.")
        print("That is normal on a first run against real data, and it is fine. What is not")
        print("fine is reporting the categories as reliable without ever checking them.")
        print("Hand-label 200 to 300 tickets, put them in an 'Answer Key' sheet with columns")
        print("Ticket ID / True Category (L1) / True Subcategory (L2) / True Issue Type (L3),")
        print("and rerun. The report will then carry a real number instead of a blank.")
    print(f"\nWrote {dest}")


if __name__ == "__main__":
    main()
