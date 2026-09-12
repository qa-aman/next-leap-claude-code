# PRD Drafter - Memory

Read this before drafting. Roadmap status changes what you recommend, never what the evidence says.

## Roadmap status

### Action item accuracy is already in development, shipping in about a month

Recorded 08-08-2026. In the repo's fictional timeline (today is 17-03-2026 per `CLAUDE.md`), this is the **Action Item Confidence Scoring v2** sprint, 17-03-2026 to 28-03-2026, with **Smart Follow-Up** landing April 2026.

If you are asked for a PRD on accuracy, confidence scoring or follow-up, write it as a spec for work already in flight, not as a proposal to start it. Say so in the Problem section. Spend the document on what is still undecided: which failure mode the shipped version must cover (implicit commitments, confidence-score reliability), and what to measure after launch.

### Committed roadmap dates, from `04-strategy/product-vision.md`

1. Smart Follow-Up, April 2026.
2. Salesforce integration, May 2026.
3. Enterprise Tier GA and Transcript Accuracy v2, June 2026.

Do not propose a delivery date that contradicts these, and do not treat any of them as an open question.

## Baselines you will keep reusing

From `03-product-knowledge/company.md` and `04-strategy/product-vision.md`. Re-read them rather than quoting from here, but these are the ones that recur:

| Metric | Baseline |
|---|---|
| Action item accuracy | 66% |
| Pro monthly churn | 4.1% |
| Free-to-Pro conversion | 6.2% |
| Transcription accuracy | 92%, quiet rooms only |
| NPS | 34 |
| ARR / active users | $3M / 15,000 |

Targets come from `04-strategy/okrs-q2-2026.md`, never from your own judgement. If the OKR has no target for the metric you picked, say the target is unset rather than choosing one.

## Persona mapping that keeps recurring

1. **Sarah Chen** - power user, action items are her task system. The right persona for accuracy, confidence scoring and follow-up work. Has an 8-seat Team upgrade held pending accuracy.
2. **Marcus Okafor** - engineering manager, privacy and data control. The right persona for Enterprise tier, retention policy, SOC 2 and on-prem.
3. **Priya Nair** - price-sensitive lower-usage Pro user. The right persona for summary length, pricing and anything exposed to Notion bundling.
4. **James Whitfield** appears in `07-user-interviews/` but has no persona file. He is the Salesforce and integrations evidence, 22 seats, with a Fireflies pilot at end of Q1 2026. Cite him as an interview, not as a persona.

## How to maintain this file

Append a roadmap-status entry whenever the user tells you a feature is already being built, shipped, or out of scope, and record what it changes about the draft. Add a baseline only when you have traced it to a file, with the file named.
