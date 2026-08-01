---
name: ticket-category-analysis
description: Categorize free-text support tickets into a 3-tier taxonomy and produce a month-on-month management report, an interactive dashboard, and a shareable PowerPoint. Use this skill whenever someone has a batch of tickets, requests, incidents, or cases and wants to know what categories they fall into, how the volumes are trending month on month, or what management should act on. Trigger on ServiceNow, Jira Service Management, Freshservice, Zendesk, or any helpdesk export; on phrases like "categorize these tickets", "tag these requests", "what are people raising", "monthly ticket report", "ticket volume trends", "which category is growing", "what should we automate", "service desk analysis", "bucket these descriptions", "how many tickets per category"; and whenever someone describes manually reading ticket descriptions to sort them into buckets, which is the exact pain this removes. Also use it when there is no ticket data yet and a realistic sample plus a working report is needed to show a stakeholder what the output would look like. Works for IT, HR, Finance, or any other desk, since the taxonomy is an input rather than something hardcoded.
---

# Ticket category analysis

Two jobs, and the second one is why this exists.

1. **Report the inflow.** Volume per category per month, with history, and what management
   should do about it.
2. **Categorize the tickets in the first place.** Tickets arrive as free text with no category.
   Somebody currently reads each description and picks a bucket by hand. That is slow,
   inconsistent between people, and the reason job 1 is always late.

The design decision that matters most: **the categorization is measured, not assumed.** Every
volume, trend and recommendation rests on tickets being in the right bucket, so this workflow
scores that step against a labelled sample and prints the number in the report. Without that,
the whole thing is a stack of confident numbers with nothing underneath.

## When you have nothing to work with

If the user has no export yet, generate one with `generate_sample.py`. That is a supported path,
not a fallback, because getting a working report in front of a stakeholder is usually how the
real data gets released. Say clearly in the output that the numbers are sample data.

## The pipeline

```
1. Taxonomy      taxonomy_io.py           once, then only when it changes
2. Load          the monthly export       each cycle
3. Dedupe        prepare_batches.py       each cycle
4. Classify      you read the batches     each cycle
5. Apply + score apply_classification.py  each cycle
6. Report        analyze.py               each cycle  -> interactive HTML
7. Deck          build_deck.py            each cycle  -> PowerPoint for management
```

Run everything from `scripts/`. Needs `pandas`, `openpyxl`, and `python-pptx` for step 7.

### Step 1. Taxonomy

Three tiers: **Category (L1) > Subcategory (L2) > Issue Type (L3)**, defined in a JSON file.
`assets/taxonomies/it-service-desk.json` is a starter with 6 categories, 25 subcategories and
46 issue types. For a different domain, write a new one to the same shape and read
`references/taxonomy-design.md` first, which covers how to size the tiers and what makes a
subcategory useful rather than decorative.

Fix the taxonomy up front rather than discovering it from the data each run. That is what makes
month-on-month numbers comparable. If buckets are regenerated every cycle they shift underneath
the trend, and a rise in one category may just be a rename. When the taxonomy does change, say
so in that month's report, because a category that appears in March and not February is not growth.

```bash
python3 taxonomy_io.py ../assets/taxonomies/it-service-desk.json --markdown taxonomy.md
```

That validates the file and renders a human-readable version. Reviewers argue with the Markdown
rather than the JSON.

### Step 2. Load the export

`Ticket ID`, `Month` and `Description` are required. `Short Description`, `Priority`,
`Assignment Group`, `Resolution Hours`, `SLA Met`, `Reopened`, `Department` and `Channel` each
unlock a section of the report. Missing ones shrink the report rather than breaking it, and the
scripts print what was missing and what it cost.

If the export uses different headers, pass `--column-map 'number=Ticket ID,opened_at=Opened Date'`.

No export yet:

```bash
python3 generate_sample.py --taxonomy ../assets/taxonomies/it-service-desk.json \
  --months 2026-01 2026-02 2026-03 --per-month 140 150 160 --out data/tickets.xlsx
```

### Step 3. Dedupe and batch

```bash
python3 prepare_batches.py --taxonomy tax.json --input data/tickets.xlsx --work-dir work/
```

This strips greetings, sign-offs and common typos, then collapses identical normalised
descriptions into one **case**. A desk gets the same complaint worded the same way repeatedly,
so this routinely removes half or more of the classification work at no cost to quality. The
script prints the saving. Output is `work/batches/batch-NN.md`.

### Step 4. Classify

Read each batch file and append one JSON object per case to `work/classified.jsonl`:

```json
{"case_id":"C001","path":"Access & Identity > Password > Password reset","confidence":"High","reason":"User forgot credentials and needs them reset."}
```

Read `references/classification-rules.md` before starting. The two rules people get wrong:
never force a fit when nothing matches, and never feed the classifier a column that already
encodes the answer. In most exports `Assignment Group` maps almost one to one onto the category,
so including it produces a flattering accuracy number that means nothing.

### Step 5. Apply and score

```bash
python3 apply_classification.py --taxonomy tax.json --input data/tickets.xlsx \
  --work-dir work/ --out data/categorized.xlsx
```

Three gates: every case classified exactly once, every path valid in the taxonomy character for
character, and accuracy measured against an answer key if one exists.

**When there is no answer key the script says so loudly and the report prints "not measured".**
That is the correct behaviour on a first run against real data. Suggest hand-labelling 200 to
300 tickets into an `Answer Key` sheet so the next run carries a real number. Never describe an
unscored categorization as reliable.

### Step 6. The interactive report

```bash
python3 analyze.py --input data/categorized.xlsx --work-dir work/ \
  --out report/dashboard.html --title "Service desk ticket analysis"
```

Self-contained HTML, no network calls, emailable. The whole ticket set is embedded so every
filter recomputes from the raw rows, which is what prevents a filter changing a heading but not
the panel under it. `references/report-spec.md` describes each section and the shortlist rule.

### Step 7. The management deck

```bash
python3 build_deck.py --input data/categorized.xlsx --work-dir work/ \
  --out report/Ticket-Analysis.pptx --title "Service desk ticket analysis" \
  --period "Jan to Mar 2026"
```

Nine slides using the repo's `ppt-builder` design system. The dashboard is for the analyst who
wants to explore. The deck is for the meeting, where nobody explores and somebody has ten
minutes to decide. So it is not a screenshot of the dashboard, it is the argument: the inflow,
the one thing worth acting on, the evidence, what it gives back, and what is still unknown.

Every figure comes from `metrics.py`, the same module the report uses, so the deck cannot
disagree with the dashboard it came from.

Then run the layout checker, which is not optional:

```bash
python3 ../../ppt-builder/scripts/check_layout.py report/Ticket-Analysis.pptx
```

Exit code 0 ships. Exit code 1 means overlapping boxes, which render unpredictably across
PowerPoint versions even when the file that produced them looks fine.

## The automation shortlist, and why it is built this way

Management usually wants one thing from ticket data: what should we stop handling by hand. A
subcategory reaches the shortlist only by clearing all three checks.

1. At least **12 tickets** in the latest month. Below that, automation costs more than it saves.
2. Resolution-time spread (P90 minus P10) of **3 hours or less**. This is the one that matters.
   A tight spread means the fix is nearly identical every time, which is what makes a process
   scriptable. Same volume with a 40 hour spread means each ticket needs a different judgement.
3. No more than **25%** P1 or P2, so it is routine work and not incident firefighting.

Override with `--min-tickets`, `--max-spread`, `--max-p1p2`.

It is deliberately not a weighted score. Both the report and the deck show the actual value
beside each check, so anyone can disagree with a threshold and re-rank it themselves. A hidden
weighting produces a ranking nobody can argue with, which sounds like a strength and is not.

Three things to preserve when you touch this:

1. **It presents, it does not decide.** Name the owning team and the numbers. Raising the change
   request is the service owner's call, and framing it as an instruction reads as auditing
   another team's gaps.
2. **Agent-hours are the floor, not the saving.** They are measured resolution time only, so
   triage, queue waiting and context switching are excluded. Say so wherever the number appears.
3. **Small samples stay visible and stay labelled.** A subcategory with 5 resolved tickets can
   post a huge median off one slow ticket. Fading and labelling it is honest. Dropping it hides
   a real row, and leaving it unmarked invites a staffing decision built on noise.

## Volume and effort are different questions

Expect them to give different answers, and report both. The highest-volume subcategory is often
cheap per ticket, while the expensive one is low volume and long-running. Password resets need
automation. A laptop queue burning 200 agent-hours a month needs someone to ask why a single
ticket takes 18 hours. Collapsing these two into one ranking loses the more useful finding.

## Reading the accuracy number honestly

If the answer key is a generated sample, descriptions and buckets came from the same source and
the score will run high. That measures that the pipeline works end to end. It does not forecast
performance on a live queue. The report and the deck both carry that caveat automatically, and
it should stay there. The number worth trusting comes from hand-labelled real tickets.

## Bundled resources

| Path | What it is |
|---|---|
| `scripts/taxonomy_io.py` | Load, validate, render a taxonomy. Every script imports it |
| `scripts/generate_sample.py` | Build a realistic sample export from any taxonomy |
| `scripts/prepare_batches.py` | Normalise, dedupe, write classification batches |
| `scripts/apply_classification.py` | Apply answers, validate paths, score against the key |
| `scripts/metrics.py` | The single computation of every number |
| `scripts/analyze.py` | Build the interactive HTML report |
| `scripts/build_deck.py` | Build the management PowerPoint |
| `scripts/ticket_columns.py` | Column contract and workbook styling |
| `assets/dashboard_template.html` | The report page |
| `assets/taxonomies/it-service-desk.json` | Starter taxonomy, 6 x 25 x 46 |
| `references/taxonomy-design.md` | How to build a taxonomy for a new domain |
| `references/classification-rules.md` | The classifier contract and its failure modes |
| `references/report-spec.md` | What each report and deck section contains, and why |
