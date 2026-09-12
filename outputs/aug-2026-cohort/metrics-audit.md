# Metrics Audit - 03-product-knowledge and 04-strategy

**Date:** 08-08-2026

110 numeric claims were checked across 6 documents, covering 71 distinct metrics.
0 contradictions were confirmed, and 6 candidate contradictions were refuted during verification.

Scope: `03-product-knowledge/company.md`, `03-product-knowledge/competitive.md`, `03-product-knowledge/product.md`, `03-product-knowledge/tech-stack.md`, `04-strategy/okrs-q2-2026.md`, `04-strategy/product-vision.md`.

---

## Confirmed contradictions

No contradictions were confirmed. Every metric that appears in more than one file carries the same value in each place.

---

## Unsourced numbers

101 numeric statements are made with no origin given in the doc itself. No measurement date, no query, no owning system, no survey. 73 of them are grouped into the 20 metrics below because they carry a decision. 28 were dropped as trivial (headcounts, year founded, framework version, architecture layer count, list counts, quarter labels, and repeated ship-date mentions).

Where a metric appears in several places, every occurrence is listed, because each one restates the number without an origin.

1. **Action item accuracy, 66%.** `03-product-knowledge/company.md:40`, `03-product-knowledge/tech-stack.md:30`, `04-strategy/okrs-q2-2026.md:10`, `04-strategy/okrs-q2-2026.md:14`, `04-strategy/product-vision.md:32`. This is the baseline the Q2 objective is measured against.
2. **Action item error rate, 34%.** `03-product-knowledge/company.md:40`, `03-product-knowledge/competitive.md:57`, `03-product-knowledge/product.md:21`, `03-product-knowledge/tech-stack.md:30`, `04-strategy/product-vision.md:39`.
3. **Pro monthly churn, 4.1%.** `03-product-knowledge/company.md:23`, `04-strategy/okrs-q2-2026.md:34`, `04-strategy/okrs-q2-2026.md:38`, `04-strategy/product-vision.md:30`, `04-strategy/product-vision.md:40`.
4. **Transcription accuracy, 92%.** `03-product-knowledge/product.md:8`, `03-product-knowledge/tech-stack.md:27`, `04-strategy/okrs-q2-2026.md:15`, `04-strategy/product-vision.md:33`, `04-strategy/product-vision.md:42`. The reading condition is stated at four of the five places. `04-strategy/okrs-q2-2026.md:15` labels the same 92% baseline as "standard environments", where every other doc says quiet environments or quiet rooms.
5. **Free-to-Pro conversion, 6.2%.** `03-product-knowledge/company.md:23`, `04-strategy/okrs-q2-2026.md:27`, `04-strategy/product-vision.md:29`, `04-strategy/product-vision.md:43`.
6. **Active users, 15,000, split 12,000 Free, 2,800 Pro, 200 Team.** `03-product-knowledge/company.md:14`, `04-strategy/product-vision.md:17`, `04-strategy/product-vision.md:18`, `04-strategy/product-vision.md:19`, `04-strategy/product-vision.md:28`, `04-strategy/product-vision.md:41`.
7. **ARR, $3M.** `03-product-knowledge/company.md:13`, `04-strategy/product-vision.md:27`.
8. **NPS, 34.** `04-strategy/okrs-q2-2026.md:39`, `04-strategy/product-vision.md:31`.
9. **Transcription accuracy in noisy environments, below 80%.** `03-product-knowledge/product.md:49`, `03-product-knowledge/tech-stack.md:27`. This number sets the case for Transcript Accuracy v2.
10. **Meeting content lost within 24 hours, 90%.** `03-product-knowledge/company.md:7`. This is the framing number for the whole product thesis.
11. **Plan pricing, $15 per user per month for Pro and $49 per seat per month for Team.** `03-product-knowledge/company.md:15`, `03-product-knowledge/company.md:16`, `04-strategy/okrs-q2-2026.md:22`.
12. **Model training set, 50K labeled meetings.** `03-product-knowledge/product.md:21`, `03-product-knowledge/tech-stack.md:30`.
13. **Weekly digest open rate, 43%, and Meeting Pattern Insights beta size, 800 users.** `03-product-knowledge/product.md:27`, `04-strategy/okrs-q2-2026.md:28`.
14. **Summary generation time, 45 to 90 seconds, and summary length, 350 words per 30-minute meeting.** `03-product-knowledge/product.md:51`, `03-product-knowledge/tech-stack.md:29`.
15. **Speaker diarization failure threshold, 8 or more attendees.** `03-product-knowledge/product.md:50`, `03-product-knowledge/tech-stack.md:28`.
16. **Model retraining deploy time, 2 weeks.** `03-product-knowledge/product.md:52`, `03-product-knowledge/tech-stack.md:32`.
17. **Competitor figures: Otter.ai free tier at 300 minutes per month, Fireflies.ai at 100+ integrations, a 2-year Salesforce head start, and Salesforce named the #1 switching reason.** `03-product-knowledge/competitive.md:7`, `03-product-knowledge/competitive.md:19`, `03-product-knowledge/competitive.md:23`, `03-product-knowledge/competitive.md:25`.
18. **Q2 quality targets: action item accuracy 80% and transcription accuracy 96%.** `04-strategy/okrs-q2-2026.md:14`, `04-strategy/okrs-q2-2026.md:15`.
19. **Q2 growth targets: Team seats 200 to 400, Free-to-Pro 6.2% to 8%, churn 4.1% to 2.5%, NPS 34 to 45.** `04-strategy/okrs-q2-2026.md:26`, `04-strategy/okrs-q2-2026.md:27`, `04-strategy/okrs-q2-2026.md:38`, `04-strategy/okrs-q2-2026.md:39`, `04-strategy/okrs-q2-2026.md:22`.
20. **Q2 adoption targets on zero baselines: Smart Follow-Up adoption 0% to 40%, Salesforce active Pro users 0 to 500, digest open rate 43% to 50%.** `04-strategy/okrs-q2-2026.md:16`, `04-strategy/okrs-q2-2026.md:40`, `04-strategy/okrs-q2-2026.md:28`.

The owning team will know which of these already have a dashboard or a query behind them. That call is theirs.

---

## Checked and clean

These six looked like conflicts on a first pass and were refuted during verification. They do not need to be raised again.

1. **Salesforce integration ship date, "Q2 2026" and "May".** `03-product-knowledge/competitive.md:25` and `04-strategy/product-vision.md:50`. May sits inside Q2 2026, so the two statements agree at different levels of precision.
2. **Salesforce integration launch date, "Q2 2026" and "May".** `03-product-knowledge/tech-stack.md:46` and `04-strategy/okrs-q2-2026.md:40`. Same pair as above, a quarter and the month inside it.
3. **Transcription accuracy, "92%" and "92% (quiet rooms)".** `03-product-knowledge/product.md:8`, `03-product-knowledge/tech-stack.md:27`, `04-strategy/okrs-q2-2026.md:15`, `04-strategy/product-vision.md:42` and `04-strategy/product-vision.md:33`. The value is identical, and one occurrence adds the reading condition.
4. **Speaker diarization threshold, "8+ attendees" and "8+".** `03-product-knowledge/product.md:50` and `03-product-knowledge/tech-stack.md:28`. Same threshold, one entry drops the noun.
5. **Summary generation time, "45-90 seconds" and "45-90 sec".** `03-product-knowledge/product.md:51` and `03-product-knowledge/tech-stack.md:29`. Same range, abbreviated unit.
6. **Team plan seats, "200 seats" and "200".** `04-strategy/okrs-q2-2026.md:22` and `04-strategy/okrs-q2-2026.md:26`. Same count, one entry drops the noun.
