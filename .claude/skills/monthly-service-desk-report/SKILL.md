---
name: monthly-service-desk-report
description: "Monthly Service Desk Ticket Report. Turns a ServiceNow or other helpdesk ticket export into the leadership dashboard: profiles the export, categorizes tickets from their text, scores against an answer key, builds a report with a 20-second executive summary, month and category filters, summary cards and volume by subcategory, builds a review page that scores last report's calls against this period with risks, owners, targets and knowledge article candidates, verifies both, republishes to last month's link, and explains how to share it. Use whenever the user shares a ticket export (.xlsx or .csv) and wants a report or update for leadership, says 'monthly ticket report', 'service desk report', 'refresh the ticket dashboard', '/monthly-service-desk-report', or brings a new month of ServiceNow, Jira Service Management, Freshservice or Zendesk tickets, even without naming this skill. Also use it when the user brings back management feedback on the ticket report, so each point is logged and built into the skill. For one-off categorization with no recurring report, use ticket-category-analysis alone."
---

# Monthly Service Desk Ticket Report

A runbook for the monthly cycle. The heavy lifting lives in the sibling skill
`ticket-category-analysis` (dedupe, apply, score, dashboard, deck). This skill calls its scripts
rather than copying them, so a fix there reaches every monthly run. What this skill adds is the
order of work, the checks that caught real defects, and the memory that makes next month a
re-run instead of a rebuild.

The reader is a leader with 15 to 20 seconds. Everything below protects two things they cannot
check for themselves: that the numbers are right, and that the page they open is the same link
they opened last month.

## Paths

```
SKILL=.claude/skills/monthly-service-desk-report
TCA=.claude/skills/ticket-category-analysis
TAX=$TCA/assets/taxonomies/it-service-desk.json
OUT=outputs/<current-month>-cohort/ticket-dashboard-<period>   # e.g. ticket-dashboard-apr-jun-2026
```

Give every run its own `OUT` folder named after the period it covers. A shared folder lets this run
overwrite last run's categorized workbook and work files, which are the audit trail behind a
report someone may already have shared.

Scripts need `pandas` and `openpyxl`. If the system Python lacks them, make a venv in the
scratchpad (`python3 -m venv venv && venv/bin/pip install pandas openpyxl`) and use that
interpreter for every command below.

## Step 0. Read the memory

```bash
python3 $SKILL/scripts/history.py show
```

This prints past runs and the artifact URL to publish to. Then read two files:

- `references/feedback.md`: every review point from management, page comments and Aman. Any
  row still **Open** gets applied (see "After a management review") before this run's report is
  built, or marked **Carried** with a reason you tell the user. A report that ignores a point
  management already raised costs more trust than a late report.
- `references/classification-notes.md`: descriptions misclassified in earlier months, so the
  same mistake is not made twice.

## Step 1. Profile the export

```bash
python3 $SKILL/scripts/profile_export.py --input <export.xlsx> --taxonomy $TAX
```

Tell the user in two or three lines what is in the file: tickets per month, whether categories
are blank, whether an answer key exists, whether the export's Taxonomy sheet matches the JSON.

- **Required columns missing:** stop and map them with `--column-map` (see the TCA skill).
- **Categories already filled:** do not feed them to the classifier. Say so to the user.
- **Taxonomy sheet differs from the JSON:** stop and reconcile with the user. A changed taxonomy
  breaks month-on-month comparison, and the report must say so that month.
- **No answer key:** the run still works, but accuracy prints as "not measured". Suggest
  hand-labelling 200 to 300 tickets into an `Answer Key` sheet.

## Step 2. Categorize

```bash
python3 $TCA/scripts/prepare_batches.py --taxonomy $TAX --input <export.xlsx> --work-dir $OUT/work
```

Read `$TCA/references/classification-rules.md`, then read each `$OUT/work/batches/batch-NN.md`
and write one JSON line per case to `$OUT/work/classified.jsonl`. Judge only from what the user
wrote. Never use `Assignment Group`: it maps almost one to one onto the category, so using it
makes the accuracy score meaningless. Use Medium and Low confidence honestly, since that is what
routes a ticket to human review.

```bash
python3 $TCA/scripts/apply_classification.py --taxonomy $TAX --input <export.xlsx> \
  --work-dir $OUT/work --out $OUT/servicenow-tickets-categorized.xlsx
```

Report the accuracy and the misses. Never edit answers to match the key after scoring: the
score is the only evidence the categories are trustworthy. Instead, append each new miss pattern
to `references/classification-notes.md` (the description, what you picked, what was right, why).

## Step 3. Build the dashboard

```bash
python3 $TCA/scripts/analyze.py --input $OUT/servicenow-tickets-categorized.xlsx \
  --work-dir $OUT/work --out $OUT/ticket-dashboard.html --title "Service Desk Ticket Report"
```

Add `--sample-data` only when the export came from `generate_sample.py`. Without it, real data
gets no "sample" footer, which matters: leadership will not act on numbers labelled as fake.

The page carries, top to bottom: the executive summary (Demand, Risk, Effort, Decision, plus a
trust line on categorization accuracy; fixed to the whole period, filters never change it), the
month and category filters, summary cards, the month-on-month chart, volume by subcategory with
drill-down to the raw tickets, the automation shortlist, agent hours, SLA pressure, and
categorizer quality.

## Step 4. Make the page and gate it

```bash
python3 $SKILL/scripts/make_page.py --dashboard $OUT/ticket-dashboard.html \
  --out $OUT/service-desk-ticket-report.html --title "Service Desk Ticket Report"
```

Exit 1 lists what to fix (em dashes, non DD-MM-YYYY dates, a wrong sample-data footer, a missing
summary, external hosts). Fix them at the source, in the TCA template or `analyze.py`, not in the
output file, or next month brings them back.

## Step 4b. Build the review

The dashboard says what is in this export. The review says whether last report's calls worked
and what leadership decides now. It applies the frameworks agreed in F-004: the bottom line
first (Minto), last report's calls scored against this period (After Action Review), an outcome
chain for last period's Decision (Kirkpatrick, adapted), each risk with evidence, cause, fix and
owner (blameless postmortem), Start / Stop / Continue, targets left for leadership (backward
design), and the top issue types as knowledge article candidates (KCS, typed per Diataxis).

```bash
python3 $SKILL/scripts/quarterly_review.py --current $OUT/servicenow-tickets-categorized.xlsx \
  --previous <last live run's categorized workbook, from history.py show> \
  --out $OUT/service-desk-review.html [--notes $OUT/review-notes.json] [--sample-data]
```

- **No earlier run:** omit `--previous`. The page says it sets the baseline.
- **Causes read from ticket text are hypotheses.** The page marks them "To confirm". When an
  owner confirms a cause, agrees a fix, or leadership sets a target, write it to
  `review-notes.json` (`causes`, `fixes`, `targets`, keyed by subcategory, `P1` or `Overall`)
  and rerun. Never upgrade a hypothesis to a fact without the owner's word.
- **Exit 1** lists defects (dashes, ISO dates, an empty value, a missing section). Fix them in
  the script, not the output.
- Check the console against step 5's `summary_numbers.py` for both periods: last period's
  Risk, Effort and Decision must be the calls the review scores.
- `--show-frameworks` tags each section with its framework. Use it only for an internal review,
  never for the leadership link: a framework label is machinery to that reader.

## Step 5. Verify like the reader will

1. `python3 $SKILL/scripts/summary_numbers.py --input $OUT/servicenow-tickets-categorized.xlsx`
   recomputes the four summary pointers with separate code.
2. Serve `$OUT` locally (`python3 -m http.server 8765 --bind 127.0.0.1`, since browsers block
   `file://`), open the dashboard in a browser tool, and run the snippet in
   `references/verify.md`. It reads back the summary, clicks filters, and checks the category
   chips fit one row at 1280 px.
3. Every summary number must match step 1's output. A mismatch is a bug: find it before publishing.
4. Take one screenshot of the top of the page and look at it. Then stop the server, close the
   browser, and delete the screenshot.

## Step 6. Publish to the same link

- **History has a URL:** publish `$OUT/service-desk-ticket-report.html` with that `url`. If this
  conversation has not read that artifact yet, read it first (`action: "read"`), as the tool
  requires. Omit `icon`. The management team keeps one link and sees the new month.
- **First run:** publish without `url`, with `icon: "chart"` and a one-sentence description.

Then record the run:

```bash
python3 $SKILL/scripts/history.py add --period "<Jan 2026 to Mar 2026>" --export <file> \
  --tickets <n> --accuracy-l2 <pct> --page $OUT/service-desk-ticket-report.html --url <artifact url>
```

Publish the review the same way: to the review link `history.py show` prints, or as a new
artifact (`icon: "clipboard"`) the first time. Then attach it to the run:

```bash
python3 $SKILL/scripts/history.py set-review --period "<period>" \
  --page $OUT/service-desk-review.html --url <review url>
```

## Step 7. Hand over

Give the user, briefly: the dashboard and review links, the four summary pointers as a table,
the review's verdict and its "To confirm" causes (each needs its owner's answer), accuracy and
misses, and anything that changed from last month (taxonomy, missing columns, a new top risk).
Then sharing:

- **Best:** open the link, use the page's Share menu to give the management team access, send
  the link. They always see the latest month, filters work, and they can comment on the page.
  People outside the organization may not be able to open it, so check before sending.
- **Fallback:** attach `$OUT/ticket-dashboard.html` to an email. It is self-contained, opens
  offline in any browser, filters work, but it is a snapshot.
- **For a meeting:** offer the deck, `$TCA/scripts/build_deck.py`, then its layout checker.

The artifact is private until the user shares it. Claude cannot change sharing.

## Weekly email (Fridays 19:00)

`scripts/weekly_send.py` emails the latest review every Friday at 19:00, run by the launchd
job `~/Library/LaunchAgents/com.shipwithai.servicedesk-weekly.plist` on Aman's Mac. It sends
the verdict, the decisions, four numbers and both links, and always says when the figures were
last refreshed, since most weeks bring no new export.

- **Recipients:** `state/send-config.json` (gitignored; copy `send-config.example.json` to start). Every `to` and `cc` address must also be on
  `allowlist`, or the run stops before building the message. Only Aman edits the allowlist.
  Before adding leadership, share both artifacts with them, or the links will not open.
- **Test runs:** `include_test_runs: true` lets a test run's review go out. Set it to `false`
  once live data flows.
- **Check it without sending:** `python3 scripts/weekly_send.py --dry-run`.
- **Catch-up:** launchd runs `weekly_send.py --if-due` at login, every hour and at Friday 19:00.
  It sends only when a Friday 19:00 has passed since the last successful send, so a Mac that was
  off, asleep or offline sends at its next run, a failed send retries hourly, and no week goes
  twice. More than 3 hours late, the email says so. Test any time with
  `--if-due --dry-run --now "DD-MM-YYYY HH:MM"`.
- **Failures** go to `state/send-log.jsonl` and show as one macOS notification per missed Friday.
- **Stop it:** `launchctl bootout gui/$(id -u)/com.shipwithai.servicedesk-weekly`.

## After a management review

Trigger: the user is back from a review and shares the points, in any form (pasted notes, a
transcript, "they said X", a photo of a whiteboard), or says "log the feedback".

1. Log every point in `references/feedback.md`, following the steps at the top of that file:
   one row per distinct point, the reviewer's words in `Said`, the durable rule in `Rule`,
   Status **Open**. Show the user the rows and confirm nothing was missed before changing code.
2. Apply each rule at its source (TCA template, `analyze.py`, a script here, or this file).
3. Rebuild the latest live run and one earlier run from step 3, and check the change with step 5.
   An earlier run catches a fix that only works for this month's data (F-003 is the example).
4. Close each row: Applied with `Fix` and `Checked` filled in, or Declined or Carried with a
   reason. Ask before declining a management point.
5. Republish the latest live run to its link so management sees their feedback acted on, then
   tell the user which points changed what.

## Comments on the page

A comment left on the published page is review feedback too. Log it in
`references/feedback.md` with `Source` as "page comment" and the commenter's role, then make
the change in the TCA template or script (so it survives next month), rebuild from step 3,
republish to the same path, reply in the thread with what changed, and resolve it.

## Bundled resources

| Path | What it is |
|---|---|
| `scripts/profile_export.py` | What is in the export, and whether the run can proceed |
| `scripts/make_page.py` | Strips the document wrapper, sets the title, gates the page |
| `scripts/summary_numbers.py` | Independent recompute of the executive summary |
| `scripts/quarterly_review.py` | The review page: last calls vs this period, risks, targets, articles |
| `assets/review_style.css` | The review page's styles, light and dark |
| `scripts/weekly_send.py` | Friday email of the latest review, allowlist-guarded |
| `state/send-config.json` | Sender, recipients and the allowlist |
| `scripts/history.py` | Run memory: past runs, accuracy trend, the URL to republish to |
| `references/verify.md` | Browser snippet that drives filters and checks the layout |
| `references/feedback.md` | Every review point and how it changed the skill; read at step 0 |
| `references/classification-notes.md` | Miss patterns from earlier months; read before classifying |
| `state/history.json` | Written by `history.py` |
