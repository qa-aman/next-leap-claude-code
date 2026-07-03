---
name: meetflow-triangulated-signals
description: Durable issues confirmed across 2+ independent feedback sources in the 17-03-2026 triangulation run. Use to skip re-deriving top priorities in future runs.
metadata:
  type: project
---

Run date: 17-03-2026. Sources: 07-user-interviews/ (4 transcripts), 06-user-feedback/feedback-q1-2026.md (47 respondents), 03-product-knowledge/ + 05-user-personas/ (churn and retention signals).

## 3/3 Source Issues (Durable Priorities)

1. Action item accuracy - 34% error rate, 40% of survey respondents, top named churn driver in company.md. Primary upgrade blocker for Pro. The single highest-priority issue.
2. Summaries too long - 30% of survey respondents, #2 complaint in product.md, core use case failure for Priya Nair persona.

## 2/3 Source Issues

3. No Salesforce integration - 23% survey, named in interviews (James Whitfield, 10-15 min/call manual work). Not a direct churn driver in churn files, but competitive pressure from Fireflies is real.
4. False confidence labels - interviews (Sarah Chen) + churn files. Survey captures the outcome but not the label mechanism. Rolls into same fix track as action item accuracy.
5. Privacy and data control - 17% survey, interviews (Marcus Okafor). Adoption blocker more than churn driver. Enterprise angle.
6. Price vs. value for low-volume users - 15% survey, Priya Nair persona churn risk High. No lightweight tier exists.

## 1/3 Source Issues (Needs More Investigation)

- Implicit commitments not captured (interviews only, sarah-chen.md) - sub-issue of action item accuracy
- Notion AI substitution risk (churn/competitive files only) - strategic risk, not yet a felt user complaint

**Why:** These are the validated priorities as of 17-03-2026. Use to anchor future runs and avoid reinvestigation of settled questions.

**How to apply:** In future triangulation runs, check whether new data changes the source count for any of these issues. If an issue moves from 1/3 to 2/3, escalate it. If a 3/3 issue drops from churn data, flag it for re-investigation.

See also: [[meetflow-source-file-map]], [[meetflow-phrase-mapping]]
