# MeetFlow — Q1 2026 Churn Driver Analysis

**Source file:** `06-user-feedback/feedback-q1-2026.md`
**Analysis date:** 13-06-2026
**Survey period:** 05-01-2026 to 19-01-2026
**Respondents:** 47 (Pro and Team plan users only)
**Analyst:** churn-pattern-analyst (read-only)

---

**The single biggest churn driver is action item inaccuracy: users who rely on MeetFlow's action items as their task system cannot trust the output and are leaving, while users who avoid action items entirely are staying.**

---

**Ranking logic:** Drivers are ordered by frequency first (raw mention count from the survey's coded theme table), with severity used as a tiebreaker and to surface lower-frequency drivers that carry outsized cancellation risk.

---

### 1. Action item accuracy too low to trust

Frequency: 19 responses (High, the single plurality in the dataset)
Severity: Critical - the survey's own Key Finding states the entire detractor segment maps to this driver, meaning it is not merely dissatisfaction but a direct predictor of churn for users whose core use case is action tracking.

Evidence:
- "I can't trust the action items. I still have to go back and check every single one." (file: 06-user-feedback/feedback-q1-2026.md, line 25)
- "Detractors rely on action items as their task management system and get burned by the 34% error rate." (file: 06-user-feedback/feedback-q1-2026.md, line 45)
- "The gap between promoters and detractors is explained almost entirely by action item accuracy." (file: 06-user-feedback/feedback-q1-2026.md, line 45)

Note: the survey table (lines 23-29) provides one example verbatim per theme. The 19-mention count is the coded aggregate from open-ended responses. No additional individual verbatims appear in the file for this theme beyond what is quoted above.

---

### 2. Summaries too long, not scannable enough

Frequency: 14 responses (High, tied in band with action items at plurality level)
Severity: High - users express explicit frustration with the output format, and the complaint volume (14 mentions) is large enough in a 47-person survey to represent a persistent friction that erodes daily value and makes cancellation easier to rationalize.

Evidence:
- "I want bullet points, not an essay. Give me the 3 things that matter." (file: 06-user-feedback/feedback-q1-2026.md, line 26)

Note: only one verbatim is available in the file for this theme. The 14-mention count is from the coded themes table (lines 23-29). This is not a churn driver in isolation, it is churn-adjacent: the Smart Summaries v2 launch in November 2025 already improved NPS by 12 points (lines 17-18), suggesting this complaint is a residual tail, not a new collapse.

---

### 3. Missing Salesforce integration blocking Team-plan deals

Frequency: 11 responses (Medium)
Severity: Critical for the Team segment - the verbatim uses explicit "no deal" language, meaning this is a stated purchase blocker, not a feature request.

Evidence:
- "We're a sales org. No Salesforce = no deal for Team plan." (file: 06-user-feedback/feedback-q1-2026.md, line 27)

Segment skew: This driver comes from a 47-person survey that includes only 9 Team-plan users (lines 54-56). With 11 mentions of Salesforce across the full 47 respondents, this complaint is almost certainly skewing from sales-team Pro users as well as the Team cohort. The "no deal" framing in the verbatim is a pre-churn or pre-upgrade-block signal, not a post-cancellation one, but its frequency in a small respondent pool makes it load-bearing.

---

### 4. Privacy and data storage concerns

Frequency: 8 responses (Medium)
Severity: High - questions about recording storage and auto-delete are trust signals; unanswered data concerns create a silent churn pathway, especially for users in regulated industries or companies with IT policies, where a single negative answer from IT can end the subscription.

Evidence:
- "Where are recordings stored? Can I auto-delete after 30 days?" (file: 06-user-feedback/feedback-q1-2026.md, line 28)

Note: one verbatim is available in the file. The question framing (unanswered, seeking reassurance) indicates these users have not found clarity in the product or documentation. This is distinct from a feature complaint: it is a trust gap.

---

### 5. Price-to-value mismatch for light users

Frequency: 7 responses (Low)
Severity: Medium - the complaint is anchored to low usage frequency ("twice a week"), meaning these are not power users. Loss of these users hurts conversion and ARR at the margin but does not represent the highest-value segment.

Evidence:
- "I use it twice a week. $15/month doesn't feel worth it." (file: 06-user-feedback/feedback-q1-2026.md, line 29)

Note: this survey covers Pro and Team users only (line 4). These 7 respondents are already paying, meaning this is active-subscriber churn risk, not just conversion friction. A lighter-use tier or usage-based pricing would address this cohort directly.

---

## What's Underneath

All five drivers trace back to a single structural problem: MeetFlow has proven its core value proposition (time savings, Slack digests, summary quality) well enough to earn promoters, but the AI output layer, specifically action items, is not reliable enough to carry users who need it as a system of record rather than a convenience. The detractor segment is not disenchanted with the product idea; they are disenchanted with the execution precision of one specific feature. The 34% action item error rate (referenced in line 45) is the ceiling on NPS and the floor under churn.

The Salesforce gap and the price-to-value complaints are secondary, but they compound the problem for two specific cohorts: sales-team users who have a hard integration requirement, and light users who never built the habit that would justify the price. Neither cohort is rescued by fixing action items alone.

**Segment skew to flag:** Pro users (n=38, NPS 29) are where churn risk concentrates. Team users (n=9, NPS 52) are satisfied, likely because of priority support and custom templates (line 58). The Salesforce complaint and the privacy concerns are the two drivers most likely to harden among Team users as that segment grows.

---

*Analysis based solely on `06-user-feedback/feedback-q1-2026.md`. The file contains one coded verbatim per theme in a summary table, not a row-per-response transcript. All quote citations are to the table rows on lines 25-29 and the Key Finding section on lines 45-47. Counts reflect the survey's own coded-theme tallies, not independent re-counts from raw responses.*
