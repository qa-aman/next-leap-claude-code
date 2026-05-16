# Standup Summary - 20-03-2026

**Sprint context:** Day 4 of Action Item Confidence Scoring v2 sprint (17-03-2026 to 28-03-2026)
**Attendees:** PM, Kai, Remi, Yuki, Priscilla, Dev, Noor. Priscilla joined late.

## TL;DR
- Conditional actions corpus may be ~15% mislabeled; Remi spot-checking before the 36-hour training run kicks off this afternoon.
- API contract for scoring v2 landed a day early, unblocking Priscilla's backend work on the suggested action items endpoint.
- Smart Follow-Up April launch at risk if 28-03 slips; PM driving a pre-emptive scope cut decision by Tuesday 24-03.

## Progress by person
| Person | Yesterday | Today | Blockers |
|--------|-----------|-------|----------|
| PM | Signed off on Kai's API contract; reviewed Noor's High/Medium/Low Figma; pulled 1,200 conditional action examples with Yuki | 11am eval review with Remi; draft rollout plan (10% Pro → 50% → GA) PR in 08-product-features/; pair with Dev on confirm/dismiss copy | None |
| Kai | Shipped API contract to main, linked wiki doc | Scope retraining automation work for next quarter | None |
| Remi | Implicit commitments tweaks done; sanity check on 100 examples catching ~78% (up from 61%) | Spot check conditional actions corpus; kick off training run after lunch (pending eval review) | Corpus noise risk (~15% mislabeled) |
| Yuki | Wrapped conditional actions corpus pull (~1,200 examples) | Start multi-person item extraction; rewrite speaker attribution logic | None (out Friday afternoon, dentist) |
| Priscilla | Pipeline doc 70% done | Finish pipeline doc; start backend for suggested action items endpoint | None (API contract now in main) |
| Dev | Wireframed UI states for suggested action items | Start coding UI states; copy review with PM on confidence card | Waiting on Noor to finalize dismiss state interaction (button vs swipe) |
| Noor | Polished High/Medium/Low cards | Hand off dismiss spec to Dev; continue card polish | None |

## Blockers and risks
- Conditional actions corpus may be ~15% mislabeled, owner: Remi, needs: spot check before training run kicks off this afternoon
- Dev blocked on dismiss state interaction spec, owner: Noor, needs: handoff by 4pm today
- Smart Follow-Up April launch at risk if 28-03 slips by even 2 days, owner: PM, needs: scope cut decision by 24-03

## Decisions made
- Dismiss state = button this sprint; swipe deferred to v2.1, decided by: Noor
- API contract for scoring v2 approved as-is (no major changes), decided by: PM
- Rollout plan shape: 10% Pro cohort → 50% → GA, decided by: PM (draft to be PR'd today)

## Action items
- [ ] Spot check conditional actions corpus for mislabels, owner: Remi, due: 20-03-2026 (before lunch)
- [ ] Walk through eval set with Remi, owner: PM, due: 20-03-2026 (11am)
- [ ] Kick off 36-hour training run, owner: Remi, due: 20-03-2026 (after lunch)
- [ ] Draft rollout plan PR in 08-product-features/, owner: PM, due: 20-03-2026 (EOD)
- [ ] Pair with Dev on confirm/dismiss UI copy, owner: PM, due: 20-03-2026 (after lunch)
- [ ] Hand off dismiss state spec to Dev, owner: Noor, due: 20-03-2026 (4pm)
- [ ] Finish pipeline doc, owner: Priscilla, due: 20-03-2026
- [ ] Pre-decide Smart Follow-Up scope cut, owner: PM, due: 24-03-2026

## Callouts
- Yuki out Friday afternoon (dentist); heads-down on speaker attribution rewrite until then
- Priscilla joined late (kid's school thing)
- Smart Follow-Up April launch is the looming risk shaping this sprint's scope decisions
