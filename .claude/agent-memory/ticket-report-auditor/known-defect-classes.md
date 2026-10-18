---
name: known-defect-classes
description: Defect classes found in ticket report audits (18-10-2026, Jan-Mar and Apr-Jun 2026 folders); the checklist every audit runs, with fix status so a fixed class is checked as a regression.
metadata:
  type: feedback
---

The first two audits (18-10-2026) found that the Excel row data and the dashboard counts were correct. Every defect was in derived figures, in prose, or in the review and preview pages. So spend most of the effort there.

Status: **fixed at source 18-10-2026** means the generator was changed. Still check it every run: a pass confirms the fix held, a fail is a regression and ranks High.

1. **Rounding the same metric twice.** Shortlist and summary used `round(sum)/3`, the effort chart used `sum/3` (22.7 shown, 22.8 true). It shows on one page when a category chip puts the same subcategory in both tables, so always drive the chips and compare. The review's "hours freed" is the difference of the two shown figures (22.8 - 18.3 = 4.5), not of the raw ones. *Fixed at source 18-10-2026 (template `hoursSum`, quarterly_review `hours_raw`).*
2. **A verdict count disagreeing with its own table.** "2 of 4 calls moved the right way" while the table marked 3 as Better/Fixed/Falling. Count the chips and check every table row lands in one bucket of the prose ("moved the right way" / "needs attention"). Also check the number of calls in prose ("three") against the table rows (4). *Open.*
3. **Unverified "first seen" or "new" claims.** "VPN client wording first seen in May" was false: the phrase appeared in every Jan-Mar month. Grep the PRIOR period's descriptions for the exact phrase, and count exact vs loose match separately. *Open.*
4. **A wrong top-N list.** The preview's top 6 swapped in a 15-ticket item for a 19-ticket one. Recompute every top-N list and its order. *Fixed by hand in the preview 18-10-2026; the preview has no generator.*
5. **An accuracy tile's subtext contradicting its headline.** L3 at 97.1% carried "6 distinct descriptions landed wrong", which is the L2 error count. Compare tile % x tickets with any error count quoted. *Fixed at source 18-10-2026 (count moved to the L2 tile).*
6. **Two category bases on one page.** Accuracy table uses answer-key categories, volume table uses classified ones (Network 55 vs 60). Not wrong; flag if unlabelled. *Open, Low.*
7. **A direction word whose sign contradicts the number.** "(-57.1% up)" from a template that always appended "up". Check the word next to every signed percentage. *Fixed at source 18-10-2026 (up / down / flat).*
8. **Paired pages that differ.** Dashboard and report were built at different times: sample-data note on in one, off in the other; different Decision wording; hard-coded "urgent tickets miss SLA most". Diff the rendered text of the pair beyond the title, and the JS too. The report must come from `make_page.py` on the same dashboard. *Fixed 18-10-2026 by rebuilding both from one dashboard with `--sample-data`.*
9. **Unstated denominators.** Reopen rate uses resolved tickets (17/437 = 3.9%), against all tickets it is 3.8%. Also "top 8" tables that don't say they are cut. *Open, Low.*
10. **Stale source lines.** The preview footer named Excel files not in the folder and an answer key the workbook lacks. Check every cited filename against the folder. *Open, Low.*
11. **Two start months for the same trend.** "38 to 15" (Mar to Jun) vs "35 → 21 → 15" (Apr to Jun). Both right, unlabelled. *Fixed at source 18-10-2026 (review now says "38 in Mar to 15 in Jun").*
12. **A superlative whose picker excludes candidates.** "Licensing misses SLA most" because the code skipped subcategories already in the Effort point; Laptop was worst. For every most / worst / biggest claim, rank the full set yourself and read the picker JS for `.filter(!already shown)` exclusions. Same code exists in `quarterly_review.py` `pointers()`. *Open, High.*
13. **A preview page that lags the review page.** The hand-written preview kept older decisions, a different top 6 and "three calls". Diff the preview against the review claim by claim, not only against Excel. *Open: the preview has no generator.*
14. **A "takes the most" label on a call that was second.** "Licensing takes the most agent hours" for Jan-Mar, behind Laptop. Check ranks against the PRIOR Excel. *Open, Low.*

## Method notes (not defects)

- Python `round()` is banker's rounding; the pages use JS `Math.round` (half up). Use `floor(x*10+0.5)/10` in the recompute or you will report false 0.1 mismatches (81.25 -> 81.3).
- When a Misclassified sheet (predicted vs true L2) exists, rebuild the answer-key category counts and L1/L2 accuracy from it; only L3 stays "matches stored sheet only". With no answer key at all, report accuracy as "matches stored sheet only", never as verified.
- The text extraction in headless Chrome includes elements with the `hidden` attribute. To check whether the sample note shows, read `sample_data` in the embedded `D`, not the rendered text.
