**Subject:** Action Item Confidence Scoring v2: on track for 28-03 demo, evaluation window is tight

Hi [VP Product name],

Scoring v2 is on track for the demo on 28-03-2026. One risk to flag: our annotation vendor delivered the labelled meeting data 3 days late, so model evaluation is compressed.

**Where we are (sprint runs 17-03 to 28-03)**
- Baseline: action item accuracy is 66% today, against the Q2 target of 80%. The model misses 34% of action items (50K labelled meetings in training).
- Scope: implicit commitments, multi-person items and conditional actions.
- UI: the API contract for scoring v2 landed a day early. The confidence card (High/Medium/Low labels) and the suggested-items confirm/dismiss flow are in build.
- Conditional actions: we had fewer than 500 labelled examples. Yuki pulled about 1,200 from the unlabelled corpus, so Remi is unblocked on that piece.

**The risk**
- The vendor data lost us 3 days of evaluation time. We will have less room to iterate on the model before the demo.
- Smart Follow-Up (April launch) stays internal-only until scoring v2 passes the accuracy bar, so a weak evaluation read would push on April.

**What we are doing about it**
- Evaluating on the three gap categories first, since those are the sprint goal.
- Running evaluation in parallel with the UI work, not after it.
- Holding the demo date. If results are short of the bar, I will show measured numbers by category and say plainly where we are, rather than move the date.

**What I need from you**
- Nothing today. If you would rather I confirm the evaluation read with you before the demo, I can send a short update on 26-03.

I will send the final evaluation numbers right after the demo.

Thanks,
Aman
