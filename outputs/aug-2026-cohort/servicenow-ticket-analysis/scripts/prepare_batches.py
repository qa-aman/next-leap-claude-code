"""
Step 2a of the workflow: prepare the tickets for classification.

Two things happen here, and the second one is what keeps the cost down.

1. Normalise the description - lowercase it, strip the greeting and sign-off filler,
   strip punctuation, collapse whitespace. None of that filler carries any signal
   about which bucket the ticket belongs to.
2. Deduplicate. A service desk gets the same complaint worded the same way many times
   over. After normalising, identical descriptions collapse into one CASE. We classify
   the case once and fan the answer back out to every ticket that shares it.

IMPORTANT - what we deliberately do NOT feed the classifier:
   Assignment Group is excluded. In this dataset each group maps one-to-one onto an
   L1 category, so including it would hand the classifier the answer and the accuracy
   number would mean nothing. We classify from what the user actually wrote.

Output: data/batches/batch-NN.md, ready to hand to Claude.
Run: python3 prepare_batches.py
"""

import json
import re
from pathlib import Path

import pandas as pd

from taxonomy import allowed_paths

ROOT = Path(__file__).resolve().parent.parent
DATA = ROOT / "data"
BATCHES = DATA / "batches"
BATCH_SIZE = 40

FILLER_PREFIX = re.compile(
    r"^(hi team|hello|hi|team|good morning|raising this again|second time reporting this)\b[,\s]*",
    re.I)
FILLER_SUFFIX = re.compile(
    r"\b(please help|kindly look into it urgently|need this today|"
    r"this is blocking my work|thanks in advance|"
    r"let me know if you need anything from my side|appreciate a quick fix)\s*$", re.I)
TYPO_FIX = {"teh": "the", "adn": "and", "plz": "please", "cannt": "cannot",
            "workign": "working", "sytem": "system", "nto": "not",
            "mornign": "morning", "acces": "access", "agian": "again"}


def normalise(text):
    t = str(text).lower().strip()
    for _ in range(2):
        t = FILLER_PREFIX.sub("", t).strip()
        t = FILLER_SUFFIX.sub("", t).strip()
    t = re.sub(r"[^\w\s]", " ", t)
    t = " ".join(TYPO_FIX.get(w, w) for w in t.split())
    return t


def main():
    src = DATA / "servicenow-tickets-jan-mar-2026.xlsx"
    tickets = pd.read_excel(src, sheet_name="Tickets")
    tickets["_norm"] = tickets["Description"].map(normalise)

    cases = (tickets.groupby("_norm")
             .agg(tickets_in_case=("Ticket ID", "count"),
                  sample_short=("Short Description", "first"),
                  sample_desc=("Description", "first"),
                  departments=("Department", lambda s: ", ".join(sorted(set(s))[:4])),
                  channels=("Channel", lambda s: ", ".join(sorted(set(s)))))
             .reset_index()
             .sort_values("tickets_in_case", ascending=False)
             .reset_index(drop=True))
    cases.insert(0, "case_id", [f"C{i + 1:03d}" for i in range(len(cases))])

    BATCHES.mkdir(parents=True, exist_ok=True)
    for f in BATCHES.glob("*.md"):
        f.unlink()

    paths = allowed_paths()
    n_batches = (len(cases) + BATCH_SIZE - 1) // BATCH_SIZE

    for b in range(n_batches):
        chunk = cases.iloc[b * BATCH_SIZE:(b + 1) * BATCH_SIZE]
        lines = [
            f"# Classification batch {b + 1} of {n_batches}",
            "",
            "Assign every case below to exactly one path from the allowed list.",
            "Return one JSON object per line: "
            '{"case_id":"C001","path":"L1 > L2 > L3","confidence":"High|Medium|Low",'
            '"reason":"one short line"}',
            "",
            "Rules:",
            "1. The path must match the allowed list character for character.",
            "2. If no path fits, use path `UNCATEGORIZED` and confidence `Low`.",
            "3. Confidence Low means a human must review it. Do not force a fit.",
            "4. Judge only from what the user wrote. Do not assume a team or a system "
            "that is not mentioned.",
            "",
            "## Allowed paths",
            "",
        ]
        lines += [f"- {p}" for p in paths]
        lines += ["", "## Cases", ""]
        for _, r in chunk.iterrows():
            lines += [
                f"### {r.case_id}  (covers {r.tickets_in_case} ticket"
                f"{'s' if r.tickets_in_case != 1 else ''})",
                f"- Short description: {r.sample_short}",
                f"- Description: {r.sample_desc}",
                f"- Departments: {r.departments}",
                f"- Channels: {r.channels}",
                "",
            ]
        (BATCHES / f"batch-{b + 1:02d}.md").write_text("\n".join(lines))

    cases.to_json(DATA / "cases.json", orient="records", indent=2)
    tickets[["Ticket ID", "_norm"]].to_json(DATA / "ticket_case_map.json",
                                            orient="records")

    print(f"Tickets           : {len(tickets)}")
    print(f"Unique cases      : {len(cases)}")
    print(f"Classification calls saved: {len(tickets) - len(cases)} "
          f"({100 * (1 - len(cases) / len(tickets)):.1f}% fewer)")
    print(f"Batches written   : {n_batches} x up to {BATCH_SIZE} cases -> {BATCHES}")


if __name__ == "__main__":
    main()
