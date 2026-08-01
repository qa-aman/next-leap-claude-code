# Monthly ticket category analysis, the workflow

**Status:** draft for review. Once the requesting team member agrees this is right, it becomes a
skill. Written 01-08-2026.

---

## The problem this solves

Every month the service desk receives a few hundred requests. Two jobs follow from that, and the
second one is the harder one.

1. **Report the inflow.** How many tickets came in per category, per subcategory, per issue type,
   month on month with three months of history, and what does management need to do about it.
2. **Categorize the tickets in the first place.** Tickets arrive with a free-text description and no
   category. Today a person reads each description and picks a bucket by hand. That is slow, it is
   inconsistent between people, and it is the reason report 1 is late.

This workflow does both, in one pass, and it measures how well step 2 worked instead of assuming it.

---

## The six steps

```
1. Fix the taxonomy      taxonomy.py            once, then only when it changes
2. Load the tickets      the monthly export     each month
3. Dedupe and batch      prepare_batches.py     each month
4. Classify              Claude, batch by batch each month
5. Apply and score       apply_classification.py each month
6. Analyse and report    analyze.py, build_dashboard.py   each month
```

### Step 1. Fix the taxonomy

Three tiers: **Category (L1) > Subcategory (L2) > Issue Type (L3)**. Currently 6, 25 and 46.
It lives in `scripts/taxonomy.py` and is rendered for humans in `taxonomy.md`.

The taxonomy is **fixed, not discovered**. That is a deliberate choice and it is the reason the
month-on-month numbers mean anything. If the buckets are regenerated from the data each month, the
categories shift underneath the trend and a rise in "Password" might just be a rename. Fix them
once, and change them on purpose.

When the taxonomy does change, say so in the report for that month. A category that appears in March
and not in February is not growth.

### Step 2. Load the tickets

The monthly ServiceNow export. Required columns:

1. `Ticket ID`, `Opened Date`, `Month`
2. `Short Description` and `Description`, which are what the classifier reads
3. `Priority`, `Assignment Group`, `State`
4. `Resolved Date`, `Resolution Hours`, `SLA Target Hours`, `SLA Met`, `Reopened`
5. `Department`, `Channel`
6. Three empty columns for `Category (L1)`, `Subcategory (L2)`, `Issue Type (L3)`

For this draft the export is simulated by `scripts/generate_tickets.py`, which writes 450 tickets
across three months plus a held-back **Answer Key** sheet. On real data the Answer Key is replaced by
a few hundred hand-labelled tickets, and everything else is unchanged.

### Step 3. Dedupe and batch

`prepare_batches.py` does two things.

1. **Normalise.** Lowercase the description, strip greetings and sign-offs, strip punctuation, fix
   the common typos. None of that filler tells you anything about the bucket.
2. **Deduplicate.** A service desk gets the same complaint worded the same way over and over. After
   normalising, identical descriptions collapse into one **case**. We classify the case once and fan
   the answer out to every ticket that shares it.

On this dataset, **450 tickets collapsed to 127 cases, which is 71.8% less classification work.**
On real data the collapse will be smaller, because real users vary their wording more. Whatever it
is, it is free, and the script prints the number each run.

The output is `data/batches/batch-NN.md`, each holding up to 40 cases plus the full list of allowed
paths and the rules.

### Step 4. Classify

Claude reads each batch and returns one JSON object per case:

```json
{"case_id":"C001","path":"Access & Identity > Password > Password reset",
 "confidence":"High","reason":"User forgot credentials and needs them reset."}
```

Four rules govern this step.

1. The path must match the allowed list character for character. Anything else is rejected by the
   next script, not silently accepted.
2. If nothing fits, the answer is `UNCATEGORIZED`. Never force a fit.
3. `Low` confidence means a human must look. The classifier is allowed to say it does not know.
4. Judge only from what the user wrote.

**What the classifier is deliberately not shown: `Assignment Group`.** In this dataset each group
maps one to one onto a category, so including it would hand over the answer and the accuracy number
would be meaningless. On real data, check the same thing before adding any field: if a column already
encodes the answer, it does not belong in the input.

The results go into `data/classified.jsonl`.

### Step 5. Apply and score

`apply_classification.py` fans the case answers back out to all tickets, then runs three gates.

1. **Coverage.** Every case classified, exactly once. Missing or duplicate case IDs stop the run.
2. **Validity.** Every path exists in the taxonomy, character for character. An invented category
   stops the run.
3. **Accuracy.** Compare against the Answer Key and report the hit rate at each of the three levels,
   broken down by category and by confidence band.

**This third gate is the point of the whole design.** Without it the report is a set of numbers with
no idea whether the categories underneath them are right, and every finding downstream is an
assertion rather than a measurement.

Output: `data/categorized-tickets.xlsx` with four sheets. Tickets, Accuracy, Needs Review, and
Misclassified. Plus `data/accuracy.json` for the dashboard.

### Step 6. Analyse and report

`analyze.py` computes the numbers. `build_dashboard.py` builds the page.

Everything the dashboard shows is computed from the 450 embedded ticket rows in the browser, not
from a pre-baked summary. That is what stops a filter changing the heading but not the panel below
it, which is the most common bug in a dashboard like this.

The report has six parts.

1. **Headline tiles.** Volume, month-on-month change, SLA, agent hours, reopen rate.
2. **Volume by category, month on month.** Stacked, with a table twin.
3. **Drill down.** Category to subcategory to issue type to the actual tickets, with the raw
   description and the reason the classifier put it there. This is what makes the categorization
   auditable rather than a black box.
4. **Automation shortlist.** The management decision. See below.
5. **Where the agent hours go.** A different question from volume, and it gives a different answer.
6. **Categorizer quality.** The measured accuracy, in the report, not in a footnote.

---

## The automation shortlist rule

A subcategory reaches the shortlist when it clears **all three** checks:

1. At least **12 tickets** in the latest month. Below that, automation costs more than it saves.
2. Resolution-time spread (P90 minus P10) of **3 hours or less**. A tight spread means the fix is
   the same nearly every time, which is what makes it scriptable.
3. No more than **25%** P1 or P2. These should be routine work, not incident firefighting.

The three thresholds live at the top of `analyze.py` and in the dashboard subtitle. They are shown
on screen with the actual value beside each check, so anyone can disagree with a threshold and
re-rank it themselves. It is not a score, and there is no hidden weighting.

Subcategories clearing two of three are shown as **near miss**, because those are next quarter's
candidates.

Three things the shortlist deliberately does not do.

1. It does not raise the change request. It gives the numbers. The call belongs to the service owner.
2. It does not claim the full saving. Agent-hours are measured resolution time only, so triage,
   queue waiting and context switching are excluded. It is the floor, not the number.
3. It does not silently drop small samples. A row built on fewer than 10 resolved tickets is shown
   faded and labelled, because a median from 5 tickets moves a long way on one slow ticket.

---

## Running it

```bash
cd scripts
python3 generate_tickets.py        # step 2, replace with the real export on live data
python3 prepare_batches.py         # step 3
#                                    step 4: Claude reads data/batches/*.md
#                                    -> writes data/classified.jsonl
python3 apply_classification.py    # step 5, prints the measured accuracy
python3 analyze.py                 # step 6a
python3 build_dashboard.py         # step 6b
open ../report/ticket-analysis-dashboard.html
```

Then the deck for management, from the packaged skill:

```bash
python3 ../../../../.claude/skills/ticket-category-analysis/scripts/build_deck.py \
  --input data/categorized-tickets.xlsx --work-dir data \
  --out report/Service-Desk-Ticket-Analysis-Jan-Mar-2026.pptx \
  --title "Service desk ticket analysis" --period "Jan to Mar 2026"
python3 ../../../../.claude/skills/ppt-builder/scripts/check_layout.py \
  report/Service-Desk-Ticket-Analysis-Jan-Mar-2026.pptx
```

Requires `pandas` and `openpyxl`, plus `python-pptx` for the deck. No network calls.

---

## What this draft does not yet do

Stated openly so the review is about the real thing.

1. **Three months gives two deltas.** That is a direction, not a trend. Six months would fix it and
   it is a one-line change to the generator.
2. **The accuracy number is measured, but on sample data.** The descriptions were written from the
   same taxonomy the classifier was scored against, so 100% at subcategory proves the pipeline runs,
   not that it will score 100% on the live queue. The real number comes from running the same check
   against hand-labelled real tickets. That step stays in the workflow.
3. **No discovery pass.** Tickets that fit nothing land in `UNCATEGORIZED` and sit in the review
   queue. Clustering those to propose new buckets is a sensible next step, and it was left out on
   purpose to keep this draft to one decision.
4. **No cost of automation.** The shortlist says what a change gives back. It says nothing about what
   it costs to build, and that number has to come from engineering before anyone decides.

---

## Questions for the review

1. Is the three tier taxonomy the right shape, and are the 6 top-level categories the ones your team
   actually uses? If the real list differs, that is a single file to change.
2. Are the three shortlist thresholds right? 12 tickets, 3 hours spread, 25% P1 and P2 are a starting
   position, not a finding.
3. Should the report carry a fourth section on repeat requesters, meaning the same person raising the
   same category repeatedly? That points at a training gap rather than a system gap.
4. Does the 9-slide deck carry the right slides for your management forum, or do you need a
   different cut? The last slide is the four asks, and everything before it is evidence for them.
5. Do you want the review queue as a separate hand-off, so a person clears the Medium and Low
   confidence tickets before the report is published, or is it fine as an appendix inside it?

Any doubt in this, or anything that reads wrong for how your team actually works, tell me and I will
change it before we turn it into a skill.

---

## Files

| Path | What it is |
|---|---|
| `taxonomy.md` | The 3 tier taxonomy, for humans |
| `scripts/taxonomy.py` | The same taxonomy, as the single source of truth for the code |
| `scripts/generate_tickets.py` | Builds the sample export |
| `scripts/prepare_batches.py` | Normalises, dedupes, writes classification batches |
| `scripts/apply_classification.py` | Applies the answers, validates them, scores them |
| `scripts/analyze.py` | Computes every number in the report |
| `scripts/build_dashboard.py` | Builds the page |
| `scripts/dashboard_template.html` | The page itself |
| `data/servicenow-tickets-jan-mar-2026.xlsx` | The sample export, 450 tickets, 3 sheets |
| `data/categorized-tickets.xlsx` | Categorized output, accuracy, review queue, misses |
| `report/ticket-analysis-dashboard.html` | The interactive report |
| `report/exec-brief.md` | The one page for management |
| `report/Service-Desk-Ticket-Analysis-Jan-Mar-2026.pptx` | 9-slide deck for the management meeting |
