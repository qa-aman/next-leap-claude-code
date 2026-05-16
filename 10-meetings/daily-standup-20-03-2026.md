# Daily Standup Notes - 20-03-2026

Scratch notes from this morning's 9:30 standup. Day 4 of the scoring v2 sprint.

Attendees: me, Kai, Remi, Yuki, Priscilla, Dev, Noor. Priscilla joined late (kid's school thing).

---

**Me (PM):**

Ok so yesterday was actually a decent day. Kai dropped the API contract for scoring v2 a full day ahead of schedule, signed off on it last night, no major changes. Also spent like 45 min with Noor going through the High/Medium/Low confidence label thing, she's got a Figma draft up, looks clean. And finally got that unlabeled corpus thing sorted with Yuki, we pulled around 1,200 conditional action examples so Remi isn't sitting around waiting for data anymore.

Today... bunch of stuff. Got an 11am with Remi to walk through the eval set before he kicks off the training run. Need to make sure that's tight because the run is 36 hours and if something's off we eat a day. Also want to get the rollout plan drafted, thinking 10% Pro cohort first, then 50, then GA. Will push a PR in 08-product-features/ by end of day. And Dev pinged me last night about the confirm/dismiss UI copy, going to pair with him sometime after lunch.

Not blocked on anything. But honestly, the Smart Follow-Up April thing is still looming. If we slip 28-03 by even 2 days the April launch gets messy. I want us to pre-decide a scope cut by Tuesday 24-03 so we're not scrambling on the 27th.

**Kai:**

Quick one. API contract is in main, doc is in the wiki, I linked it in the channel. Today I'm going to start scoping the retraining automation work for next quarter — Priscilla's doc helped a lot. No blockers.

**Remi:**

Training run kicks off after lunch assuming the eval review with PM goes well. Yesterday I finished the implicit commitments model tweaks, ran a quick sanity check on 100 examples and it's catching ~78% which is up from 61%. Need to get the full eval done to confirm. Worried about one thing — the conditional actions corpus Yuki pulled, some of it looks noisy, like maybe 15% mislabeled. Could hurt the training. Going to spot check more this morning.

**Yuki:**

Wrapped the corpus pull yesterday, like the PM said. Today I'm starting on multi-person item extraction, basically a rewrite of the speaker attribution logic. Going to be heads down. Heads up — I'll be out Friday afternoon, dentist.

**Priscilla:**

Pipeline doc is 70% done, will finish today. After that I'm picking up the backend work for the suggested action items endpoint. Need the final API contract from Kai (which I see is now in main, good).

**Dev:**

UI states for suggested action items are wireframed, going to start coding today. Confidence card redesign needs copy review with PM. Blocker: I'm waiting on Noor to finalize the dismiss state interaction — should it be a swipe or a button? She said by EOD today.

**Noor:**

Dismiss state — going with button for now, swipe is v2.1. Will hand off to Dev by 4pm. Otherwise polishing the High/Medium/Low cards. No blockers.

---

**Decisions / followups:**
- Pre-decide scope cut for Smart Follow-Up by Tue 24-03 (owner: me)
- Remi to spot check conditional actions corpus quality before training (owner: Remi)
- Dismiss state = button this sprint, swipe deferred to v2.1 (decided)
- Noor handing off dismiss spec to Dev by 4pm today
