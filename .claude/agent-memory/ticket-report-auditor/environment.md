---
name: environment
description: Tooling facts for auditing ticket reports on this machine (verified 18-10-2026).
metadata:
  type: reference
---

- Neither `pandas` nor `openpyxl` is installed. Don't pip install them. Use the stdlib zip/XML reader in the agent body.
- `python3 -I` drops the script directory from the import path, so `import xl` fails. Run scripts as files with plain `python3`, or put the reader inline.
- Chrome is at `/Applications/Google Chrome.app/Contents/MacOS/Google Chrome`. Run it with `--headless=new --dump-dom` to get the rendered DOM, so you read JS-generated text the way a reader sees it.
- To check filters, copy the page into the scratch dir and add a `<script>` before `</body>`. On load, it clicks each `#monthchips .chip` x `#catchips .chip` and dumps `#tiles .tile` and `#l2list > *` into `<pre id="AUDITOUT">`. Chip selectors come from the monthly-service-desk-report pages, so confirm them in the page first.
- The pages embed every ticket row in `const D = {...}`. Parse it with a regex over the `const D =` line, then use `json.loads`.
- In the monthly-service-desk-report exports, Opened/Resolved dates are text `DD-MM-YYYY HH:MM`, not Excel serials, and blank cells come back as `''` (not None) when the sheet writes empty strings. Test blanks with `v in (None,'')`.
- Embedded D.rows are positional arrays: [id, monthIdx, l1Idx, l2, l3, priIdx, hours, slaBool, reopenBool, chanIdx, dept, desc, conf, reason, group]. Diff them against the Excel row by row.
