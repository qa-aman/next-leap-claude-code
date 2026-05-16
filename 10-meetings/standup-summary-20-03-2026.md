# Standup Summary - 20-03-2026

**Sprint context:** Day 4 of Action Item Confidence Scoring v2 sprint
**Attendees:** PM (me), Kai, Remi, Yuki, Priscilla, Dev, Noor. Priscilla joined late.

## TL;DR
- Smart Follow-Up April launch is at risk if sprint slips past 28-03-2026. PM will pre-decide a scope cut by 24-03-2026.
- Remi's implicit commitments model is catching ~78% (up from 61%), but the conditional actions corpus may be ~15% mislabeled and needs a spot check before the 36-hour training run kicks off.
- Scoring v2 API contract is signed off and in main a day ahead of schedule, unblocking Priscilla's backend work.

## Progress by person
| Person | Yesterday | Today | Blockers |
|--------|-----------|-------|----------|
| PM (me) | Signed off scoring v2 API contract, reviewed H/M/L Figma with Noor, pulled ~1,200 conditional action examples with Yuki | 11am eval review with Remi, draft 10/50/GA rollout plan PR, pair with Dev on confirm/dismiss UI copy | None |
| Kai | Shipped API contract to main, posted wiki doc in channel | Scope retraining automation work for next quarter | None |
| Remi | Implicit commitments model tweaks done, sanity check on 100 examples at ~78% (up from 61%) | Spot check corpus for mislabels, then kick off 36-hour training run after lunch | Conditional actions corpus may be ~15% mislabeled |
| Yuki | Wrapped corpus pull (~1,200 examples) | Start multi-person item extraction (speaker attribution rewrite), heads down | None |
| Priscilla | Pipeline doc 70% done | Finish pipeline doc, then start backend for suggested action items endpoint | None (API contract now in main) |
| Dev | Wireframed UI states for suggested action items | Start coding UI states, pair with PM on confidence card copy | Waiting on Noor's dismiss state spec |
| Noor | Polished H/M/L cards, decided dismiss interaction | Hand off dismiss spec to Dev by 4pm, continue card polish | None |

## Blockers and risks
- Conditional actions corpus may be ~15% mislabeled, owner: Remi, needs: spot check before training run kicks off after lunch
- Smart Follow-Up April launch at risk if sprint end (28-03-2026) slips by 2+ days, owner: PM (me), needs: pre-decided scope cut by 24-03-2026
- Dev blocked on dismiss state interaction spec, owner: Noor, needs: handoff by 4pm today (on track)
- 36-hour training run means a bad eval set costs a full sprint day, owner: PM + Remi, needs: tight eval review at 11am

## Decisions made
- Dismiss state will use a button this sprint; swipe deferred to v2.1, decided by: Noor
- Scoring v2 API contract finalized and merged to main, decided by: Kai + PM

## Action items
Every item must include both an owner and a due date. Due date is in DD-MM-YYYY, with an optional time qualifier in parentheses.

- [ ] Pre-decide scope cut for Smart Follow-Up April launch, owner: PM (me), due: 24-03-2026
- [ ] Spot check conditional actions corpus quality before training run, owner: Remi, due: 20-03-2026 (before lunch)
- [ ] Run eval review with Remi before training kicks off, owner: PM (me), due: 20-03-2026 (11am)
- [ ] Pair with Dev on confirm/dismiss UI copy, owner: PM (me) + Dev, due: 20-03-2026 (after lunch)
- [ ] Hand off dismiss state spec to Dev, owner: Noor, due: 20-03-2026 (4pm)
- [ ] Draft 10% / 50% / GA rollout plan PR in 08-product-features/, owner: PM (me), due: 20-03-2026 (EOD)

## Callouts
- Yuki out Friday afternoon 27-03-2026 (dentist).
- Training run is 36 hours, so any issue in the 11am eval review eats a full day of the sprint.
- Priscilla joined standup late (kid's school).
