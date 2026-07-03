---
name: meetflow-phrase-mapping
description: Cross-source phrase mapping for the same underlying issue - used to normalize language differences across interviews, survey, and churn data in future triangulation runs.
metadata:
  type: reference
---

## Action Item Accuracy

- Interviews: "Confidence score says 'high' but misses the most important item", "implicit commitments not caught"
- Survey: "I can't trust the action items. I still have to go back and check every single one."
- Churn: "action item accuracy is the top complaint driving churn", "34% wrong or missing"
- Normalize to: Action item accuracy / reliability

## Summary Length

- Interviews: "6 paragraphs... I skim them", "3-4 bullet points - the decisions that were made and who's doing what"
- Survey: "I want bullet points, not an essay. Give me the 3 things that matter."
- Churn/Personas: "summaries are too long - the #2 complaint after action item accuracy", "350 words per 30-minute meeting"
- Normalize to: Summary verbosity / scannability

## Salesforce Integration

- Interviews: "I need this in Salesforce. That's where my pipeline lives."
- Survey: "We're a sales org. No Salesforce = no deal for Team plan."
- Churn: "most-requested integration from sales-heavy teams" (company.md)
- Normalize to: Salesforce integration gap

## Privacy and Data Control

- Interviews: "Where does that data go? Who at MeetFlow can access it?"
- Survey: "Where are recordings stored? Can I auto-delete after 30 days?"
- Normalize to: Data privacy and storage control

## Price vs. Value for Light Users

- Survey: "I use it twice a week. $15/month doesn't feel worth it."
- Personas: "$15/mo feels expensive for 2-3 uses per week", "high churn risk, low switching cost"
- Normalize to: Pro pricing vs. value for low-volume users
