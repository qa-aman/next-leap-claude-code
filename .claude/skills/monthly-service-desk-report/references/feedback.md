# Review feedback

Every review point on the report, from management reviews, page comments, or Aman, logged in
one place. This file is how the skill improves. Step 0 of every run reads it, and no report is
built while a point is still Open and unaddressed.

## How to log a review

1. **Capture every point.** Review notes bundle several points together, and the important one
   is often hidden in an aside ("also, for example..."). List each distinct point before
   writing anything. One row per point.
2. **Quote, then interpret.** `Said` is the reviewer's words, verbatim or as close as the notes
   allow. `Rule` is the durable lesson behind it, written so it applies to every future month,
   not only the month it was said about. The rule is what changes the skill.
3. **Fix at the source.** Apply each rule in the place that builds the report: the TCA template
   (`ticket-category-analysis/assets/dashboard_template.html`), `analyze.py`, a script here, or
   `SKILL.md`. A fix made only in an output file is gone next month.
4. **Check it, then close it.** Rebuild the latest live run and one earlier run. Confirm the
   change shows, and that nothing else moved. Then set `Status` to Applied and fill in `Fix` and
   `Checked`.
5. **Say no out loud.** If a point should not be applied (it conflicts with another reviewer,
   the data cannot support it, or it was a one-off), set `Status` to Declined and give the
   reason. Tell Aman before declining a management point.

Status values: **Open** (logged, not yet applied), **Applied** (in the skill and checked),
**Declined** (not applied, reason given), **Carried** (deliberately left for a later run,
reason given).

Area values: Summary, Layout, Metric, Data, Categorization, Sharing, Other.

## Log

| ID | Date | Source | Area | Said | Rule | Status | Fix | Checked |
|---|---|---|---|---|---|---|---|---|
| F-001 | 17-10-2026 | Aman, preparing the management share | Summary | "the leadership team member or the management team will only have 15-20 seconds" | The top of the page must give the whole story in 20 seconds: four pointers (Demand, Risk, Effort, Decision), each a number plus one line, a one-sentence headline, and a trust line on accuracy. Fixed to the whole period so filters never change it. | Applied | `renderSummary()` in the TCA template | Numbers matched `summary_numbers.py` for Jan to Mar 2026 |
| F-002 | 17-10-2026 | Aman, comment on the published page | Layout | "fit this in one line... security and compliance is moving to second line" | Filter rows must fit one line at a 1280 px laptop width. Wrapping is allowed only on a phone. | Applied | Chip padding, gap and font in the TCA template; "All categories" became "All" | One row at 1512 px and 1280 px; `verify.md` now checks it every run |
| F-003 | 17-10-2026 | Found in the Apr to Jun 2026 test run | Summary | (no reviewer quote) The page still called P1 the risk after P1 was fixed, and said "automate first" for a shrinking category. | Summary pointers must follow the data: Risk flags P1 only when P1 trails the overall SLA, otherwise the worst subcategory. Decision shows the trend and warns when volume is already falling. The headline is built from the pointers. | Applied | Risk, Decision and headline logic in `renderSummary()`; mirrored in `summary_numbers.py` | Apr to Jun 2026 found all three planted changes; Jan to Mar 2026 still reads the same |
| F-004 | 17-10-2026 | Aman, after reviewing the framework preview | Summary | "apply this framework, and then build the artifact and apply it in the skill" | Every period gets a review alongside the dashboard: the verdict and decisions first, last report's calls scored against this period, an outcome chain for last Decision, each risk with evidence, cause (marked "To confirm" until the owner agrees), fix and owner, Start / Stop / Continue, targets left for leadership, and top issue types as knowledge article candidates. | Applied | `scripts/quarterly_review.py`, `assets/review_style.css`, Step 4b and Step 6 in `SKILL.md`, `set-review` in `history.py` | Apr to Jun 2026 vs Jan to Mar 2026 reproduced the approved preview; Jan to Mar alone runs in first-run mode; last-period calls match `summary_numbers.py` |
| F-005 | 17-10-2026 | Aman | Sharing | "every friday at 7 PM this report is sent to the leadership team" | The review goes out by email every Friday at 19:00, sent only to allowlisted addresses, and always states when the figures were last refreshed so a week with no new export never reads as new numbers. | Applied | `scripts/weekly_send.py`, `state/send-config.json`, launchd job, "Weekly email" in `SKILL.md` | Test email sent to the sender's own address on 17-10-2026; an address off the allowlist was blocked; launchd ran the job and reached Composio |
| F-006 | 17-10-2026 | Aman | Sharing | "if my laptop is switched off at around 7 pm... it should run whenever I open or restart the system next" | A scheduled send is owed, not tied to a clock tick: the run sends whenever a Friday 19:00 has passed since the last successful send, and says so when late. | Applied | `--if-due` in `weekly_send.py`; launchd `RunAtLoad` and hourly `StartInterval` | Six simulated times with `--now`: before 19:00, 21:00 same day, Monday late, after a catch-up send, next Friday; the real job ran at load and found nothing due |
