# Stakeholder Sync - March 14, 2026

**Date:** March 14, 2026
**Meeting type:** Weekly leadership sync
**Attendees:** You, Dana Rivera (Platform PM), Tomás Herrera (Enterprise PM), Aisha Patel (Core PM), CEO, VP Engineering, VP Sales

---

## Updates Shared

**AI Intelligence (you):**
- Action Item Confidence Scoring v2 sprint starts Monday March 17. Goal is to close the 34% miss rate on action items before Smart Follow-Up enters beta.
- NPS improved from 22 (Q3 2025) to 34 (Q1 2026). The Smart Summaries v2.4 launch in November is the main driver.
- Smart Follow-Up is on track for April. It depends on Scoring v2 shipping clean.

**Enterprise (Tomás):**
- Three enterprise pilots in progress. Two are actively using the product. One is stalled waiting for SSO.
- Enterprise GA still targeting June 2026.

**Platform (Dana):**
- Salesforce integration scoping is complete. Engineering starts in April. Target: May 2026.

**Core (Aisha):**
- Transcript Accuracy v2 is on track for June. Addressing the below-80% accuracy in noisy environments.

---

## Questions from Leadership

**CEO:** "What's the risk to Smart Follow-Up if Scoring v2 slips?"

You: Smart Follow-Up is built on the scoring model. If Scoring v2 doesn't ship by end of March, the April beta for Follow-Up moves to May. That pushes everything in Q2 by one month.

**VP Sales:** "Are we losing deals over action item accuracy?"

You: Yes - the Q1 NPS survey shows 19 out of 47 respondents cited wrong or missing action items as their top complaint. Pro churn was 4.1% monthly in Q4 2025. Action item quality is the clearest driver of that churn.

**VP Engineering:** "Is the retraining pipeline still manual?"

You: Yes. Current timeline to deploy a new model version is 2 weeks, fully manual. We're documenting the process this sprint. Automation is a Q3 candidate.

---

## Decisions Made

- Smart Follow-Up beta will be internal-only until Action Item Scoring v2 passes accuracy bar.
- No scope changes to Q2 roadmap. All four features stay as planned.
- Weekly status report format will now include a traffic-light section by workstream. Starts this week.

---

## Action Items

| Action | Owner | Due |
|--------|-------|-----|
| Share retrain pipeline doc with VP Eng when complete | You | March 28 |
| Confirm SSO timeline for stalled enterprise pilot | Tomás | March 17 |
| Send Q2 roadmap one-pager to board | CEO | March 21 |
| Begin Salesforce integration kickoff | Dana | April 1 |

---

## Cross-References

- OKRs: `04-strategy/okrs-q2-2026.md`
- This week's status report: `12-project-tracking/status-report-2026-03-14.md`
