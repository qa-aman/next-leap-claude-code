# Top 5 Churn Drivers — Q1 2026

**Source:** `06-user-feedback/feedback-q1-2026.md` (NPS survey, 05-19 Jan 2026, n=47 Pro and Team users)
**Synthesized:** 23-05-2026
**Current NPS:** 34 (up from 22 in Q3 2025). 30% detractors (n=14).

---

## Summary

Detractors cluster around one root cause: **action item accuracy at 66%**. The product's core value (time savings, summaries, Slack digest) is proven and praised, but trust in AI output collapses when users rely on it as a system of record. Fixing accuracy converts detractors to promoters because the underlying value is already there.

---

## The 5 Drivers (ranked by mention count)

### 1. Action items wrong or missing — 19 mentions

> "I can't trust the action items. I still have to go back and check every single one."

- Largest single complaint theme; cited by 40% of respondents.
- Hits power users hardest, the segment that treats action items as their task system.
- Directly tied to the 34% error rate called out in product vision and company overview.
- **Churn link:** This is the gap between Pro NPS (29) and Team NPS (52). Detractors rely on action items; promoters do not.

### 2. Summaries too long — 14 mentions

> "I want bullet points, not an essay. Give me the 3 things that matter."

- Persists despite Smart Summaries v2 (Nov 2025) already shortening average length by 30%.
- Suggests the format, not just the length, is the issue.

### 3. Need Salesforce integration — 11 mentions

> "We're a sales org. No Salesforce = no deal for Team plan."

- Blocks Team plan expansion in sales-heavy accounts.
- Competitive pressure from Fireflies, which already ships this.
- Addressed on the roadmap: Salesforce integration ships May 2026.

### 4. Privacy and data concerns — 8 mentions

> "Where are recordings stored? Can I auto-delete after 30 days?"

- Enterprise blocker, not just an individual concern.
- Maps to the Enterprise Tier GA (June 2026): on-prem transcript storage, audit logs, admin controls.

### 5. Too expensive for light use — 7 mentions

> "I use it twice a week. $15/month doesn't feel worth it."

- Light-use Pro users (under ~8 meetings/month) don't hit the value threshold of the flat $15 price.
- No usage-based tier exists between Free and Pro today.

---

## What This Means for the AI Intelligence Pillar

- **Driver 1 is mine.** Action Item Confidence Scoring v2 (active sprint, 17-03-2026 to 28-03-2026) and Smart Follow-Up (April 2026) directly attack the largest churn driver.
- **Driver 2 is mine.** Summary format, not just length, needs a second look. Bulleted, 3-item default may outperform the current v2 output.
- Drivers 3, 4, 5 sit with Dana (Platform), Tomás (Enterprise), and pricing respectively.

---

## Caveats

- n=47, Pro and Team only. Free users (12,000) not surveyed here; their churn drivers may differ.
- Team segment is n=9. NPS 52 directional only.
- Quotes are single examples per theme, not exhaustive samples.
