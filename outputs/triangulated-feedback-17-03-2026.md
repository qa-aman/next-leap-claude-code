# Triangulated User Feedback - 17-03-2026

Sources: 07-user-interviews/ (4 transcripts), 06-user-feedback/feedback-q1-2026.md (47 respondents), 03-product-knowledge/company.md + 04-strategy/product-vision.md + 05-user-personas/ (churn and retention signals).

---

## Triangulated Issues (2+ sources) - Top Priorities

### 1. Action item accuracy is broken - appears in 3/3 sources

The single strongest signal. The AI misses or misfires on 34% of action items. False "high confidence" labels compound the damage - users act on bad output and lose trust in the whole system.

- Interviews: "Confidence score says 'high' but misses the most important item. Every. Single. Time. Yesterday it caught 'send the invite' but missed 'we need to realign the roadmap before board review.' That's the one that matters." (interview-01-sarah-chen.md). Also raised in interview-04-james-whitfield.md. Sub-issue: implicit commitments ("I'll circle back on that") are not caught at all.
- Survey: 19/47 respondents (40%) flagged it. Exact phrase: "I can't trust the action items. I still have to go back and check every single one." (feedback-q1-2026.md). Survey notes this issue "explains almost entirely" the split between promoters and detractors.
- Churn: "Action item accuracy is the top complaint driving churn." (company.md). Error rate cited as 34% wrong or missing (product-vision.md). Pro churn is 4.1% monthly (company.md) and this is the named primary driver. Sarah Chen persona: upgrade from Free to Pro is blocked entirely by accuracy, not price (sarah-chen.md).

---

### 2. Summaries are too long - appears in 3/3 sources

Users and their stakeholders skim rather than read. The expected format is 3-4 bullets covering decisions and owners. Current output averages 350 words per 30-minute meeting.

- Interviews: "The summaries are, like, 6 paragraphs? I skim them. My CEO skims them. I want 3-4 bullet points - the decisions that were made and who's doing what. That's it." (interview-03-priya-nair.md).
- Survey: 14/47 respondents (30%) flagged it. Exact phrase: "I want bullet points, not an essay. Give me the 3 things that matter." (feedback-q1-2026.md).
- Churn: Listed as the #2 complaint after action item accuracy (product.md). Priya Nair persona uses MeetFlow specifically for the CEO Slack digest - when output is a wall of text, her core use case breaks (priya-nair.md).

---

### 3. No Salesforce integration - appears in 2/3 sources

Sales-heavy teams manually copy meeting output into Salesforce. Fireflies already solves this, creating direct competitive pressure and a hard blocker on Team plan sales.

- Interviews: "I need this in Salesforce. That's where my pipeline lives... Right now my team manually copies meeting summaries into Salesforce. That's 10-15 minutes per call." James Whitfield, 15-rep sales team. (interview-04-james-whitfield.md).
- Survey: 11/47 respondents (23%) flagged it. Exact phrase: "We're a sales org. No Salesforce = no deal for Team plan." (feedback-q1-2026.md).
- Churn: Not named as a direct churn driver in the churn files. Note: company.md lists Salesforce integration as the "most-requested integration from sales-heavy teams" and flags direct competitive pressure from Fireflies, but this is strategic framing rather than a churn signal.

---

### 4. False confidence labels eroding trust - appears in 2/3 sources

Distinct from raw accuracy: the confidence scoring system actively mislabels bad outputs as reliable. Silent failure would be preferable - users get a false quality signal, act on it, then discover the error downstream.

- Interviews: "Trust in the AI is eroding the more this happens." Sarah Chen explicitly calls out that "high confidence" labels on wrong items are the core trust problem, not just the misses themselves. (interview-01-sarah-chen.md).
- Churn: Confidence scoring model gaps cited in product.md. Sarah Chen persona: upgrade to Pro blocked entirely by this trust problem, not price (sarah-chen.md).
- Survey: No direct survey signal. Note: survey respondents describe the outcome ("I still have to check every single one") without naming confidence labels specifically.

---

### 5. Privacy and data control blocking adoption - appears in 2/3 sources

Security-conscious users - primarily in engineering, legal, and finance - will not actively adopt the product without SOC 2, on-prem storage, and configurable retention. Risk of blocking multi-seat contract renewals.

- Interviews: "I don't trust any system that records my engineering reviews. We discuss production incidents, security vulnerabilities, sometimes compensation. Where does that data go? Who at MeetFlow can access it?" (interview-02-marcus-okafor.md).
- Survey: 8/47 respondents (17%) flagged it. Exact phrase: "Where are recordings stored? Can I auto-delete after 30 days?" (feedback-q1-2026.md).
- Churn: Not named as a direct Pro churn driver in churn files. Churn signal is lower here; this is more of a blocker to initial adoption and enterprise expansion.

---

### 6. Price vs. value mismatch for low-volume users - appears in 2/3 sources

Users who attend 2-3 meetings per week find the $15/month Pro price hard to justify. No lighter tier exists. Switching cost is low, making these users the first to leave when a cheaper substitute (Notion AI) reaches "good enough."

- Survey: 7/47 respondents (15%) flagged it. Exact phrase: "I use it twice a week. $15/month doesn't feel worth it." (feedback-q1-2026.md).
- Churn: "$15/mo feels expensive for 2-3 uses per week." Priya Nair persona churn risk rated High specifically because low usage means low switching cost (priya-nair.md). No lower pricing tier exists in current plan structure (company.md).
- Interviews: Not raised as a standalone issue in interview transcripts. Priya's interview focus was summary format, not price.

---

## Source-Specific Issues (1 source) - Needs More Investigation

- **Implicit commitments not captured** - Interviews only. The model misses softer language like "I'll circle back on that" or "let's think about whether we should revisit pricing" - both recognized by experienced users as real commitments. Raised in interview-01-sarah-chen.md. Not yet surfaced in survey or churn data, but closely related to the action item accuracy issue above (consider rolling into the same fix track).

- **Notion AI substitution risk** - Churn/persona files only. If Notion adds meeting summaries at "good enough" quality, casual Pro users (especially Priya Nair profile) leave immediately. Named as "existential for the free tier and casual users" in competitive.md and company.md. Not raised in interviews or survey - users may not consciously track Notion's roadmap, making this a strategic blind spot rather than a felt user complaint.

---

## Triangulation Strength Notes

All three workers returned clean results. No source is missing. Triangulation strength is full (3 independent sources).

The action item accuracy issue is the only issue confirmed in all three sources and is the only one named as the primary churn driver. It should be treated as the #1 roadmap priority with no ambiguity.

The false confidence label issue (rank 4) overlaps significantly with action item accuracy (rank 1). They share the same root cause and likely the same fix track. Evidence from 2 sources but would be 3/3 if survey respondents had been asked about confidence labels specifically.
