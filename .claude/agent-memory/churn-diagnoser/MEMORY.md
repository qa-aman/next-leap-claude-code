# Churn Diagnoser - Memory

Read before writing the fixes. Roadmap status changes the fix, never the diagnosis.

## Roadmap status

### Action item accuracy is already in development, shipping in about a month

Recorded 08-08-2026. In the repo's fictional timeline (today is 17-03-2026 per `CLAUDE.md`), this is the **Action Item Confidence Scoring v2** sprint, 17-03-2026 to 28-03-2026, with **Smart Follow-Up** landing April 2026.

**Diagnosis is unaffected.** Accuracy is named in `company.md` as the top complaint driving churn, and it is corroborated in both the survey and the interviews. It keeps its rank on the evidence.

**Fixes are affected.** Do not list "improve action item accuracy" as a quick win. It is funded and in the current sprint. Mark it in flight, then use the quick-wins section for what is not covered. If you want to add value on accuracy, name the failure mode the shipped version must still cover (implicit commitments, confidence-score reliability) or the retention metric to watch after April 2026.

### Other committed dates, from `04-strategy/product-vision.md`

1. Salesforce integration, May 2026.
2. Enterprise Tier GA and Transcript Accuracy v2, June 2026.

Structural fixes that restate these are not fixes, they are the existing plan. Say the bet is already placed and move on.

## Baselines

From `03-product-knowledge/company.md` and `04-strategy/product-vision.md`. Re-read rather than quoting from here.

| Metric | Baseline |
|---|---|
| Pro monthly churn | 4.1% monthly, hit in Q4 2025 |
| Action item accuracy | 66%, so 34% wrong or missing |
| Free-to-Pro conversion | 6.2% |
| Transcription accuracy | 92%, quiet rooms only |
| NPS | 34 |
| Segments | 12,000 Free, 2,800 Pro, 200 Team |
| Pricing | Pro $15 per month, Team $49 per seat per month |

## Drivers that keep recurring, and their source coverage

1. **Action item accuracy.** Strongest evidence in the repo. In `company.md`, the Q1 survey, and at least two interviews (Sarah Chen, James Whitfield). Clears the two-source bar comfortably.
2. **Missing native integrations, above all Salesforce.** Interview evidence is strong, James Whitfield at 22 seats with a Fireflies pilot at end of Q1 2026, which lands before the May 2026 ship date. Check the survey for corroboration before promoting it, do not assume.
3. **Weak perceived value at the price point.** Priya Nair and Marcus Okafor. Exposed to Notion AI bundling summaries free, which is named as a risk in `company.md`.
4. **Privacy and data control.** Marcus Okafor only in the interviews. Check the survey before it clears the two-source bar, and if it does not, report it as secondary rather than forcing it into the top 3.

## How to maintain this file

Append a roadmap-status entry whenever the user tells you work is committed, shipped or dropped, and record what it changes about the fixes. Update the driver list only with what you actually traced, naming the files.
