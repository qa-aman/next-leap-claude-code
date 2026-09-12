# Smart Follow-Up PRD - Pressure Test

**Date:** 08-08-2026
**PRD under review:** `08-product-features/01-smart-follow-up/prd-smart-follow-ups.md`
**Method:** Three-role adversarial debate (Engineering Lead, Design, Sales/GTM), two rounds, lead synthesis.
**Reviewed by:** AI Intelligence PM (lead)
**Prior review:** `outputs/june-2026-cohort/smart-followup-pressure-test-23-05-2026.md`

---

## Lead summary

The PRD reads as a document that has already been reviewed once. It has scope cuts with reasons, a confidence vocabulary, a rollout table, and an observability table. That is real progress and it should be said plainly.

But the debate found one pattern underneath everything else.

**The PRD absorbed the cheap findings from the last pressure test and left the expensive ones.**

The 23-05-2026 review had three architectural findings: no defined send path (issue 1), recipient resolution as an unscoped backend service (issue 2), and a review screen built for one draft when the power user has an inbox (issue 4). I checked the current PRD by search. There is no outbox, no cancel, no undo, no recipient resolution, and no batch review anywhere in it. None of the three was absorbed.

What was absorbed: the integration scope cut, the enterprise carve-out, and the vocabulary cleanup. All three are text edits.

Line 155 then states that training data "was the top risk flagged in the 23-05-2026 pressure test." It was not. The top risk was the send path. The PRD promoted a risk it could gate on and dropped the one that needed engineering design.

Engineering and Design both rediscovered those same gaps this round without being shown the old document. That is the signal. A gap that two independent reviews find twice is a real gap, not a reviewer preference.

---

## Top 5 issues to fix before the eng walkthrough

### 1. April GA ships at roughly today's accuracy, which is the thing the feature exists to fix

All three roles landed here from different directions, and it is the only issue that threatens the date outright.

Dependencies (line 154) lists implicit commitments, multi-person items, and conditional actions as gaps to resolve before launch. Line 155 only requires that labeling has **started** by 25-03-2026. The Timeline (line 197) has Scoring v2 shipping March 2026, before that labeling round could retrain or evaluate anything.

Success Metrics (line 100) targets 80% accuracy by end of Q2 2026. GA is April. Company baseline is 66% (`03-product-knowledge/company.md`).

So the feature built to fix action item accuracy launches at approximately the accuracy that caused the problem. The Q1 survey has action items as the top complaint, 19 of 19 mentions (line 12).

**Decide before the walkthrough:** either decouple GA from the 80% target and say so in the PRD, or move the date. Engineering's position is that this is one scope decision, not three findings. I agree.

### 2. There is still no send path, and this is the second review to say so

Carried over unfixed from the 23-05-2026 review, issues 1, 2 and 5.

1. No outbox or cancel window. "What We're NOT Building" (line 139) says every draft requires explicit approval and treats that as the safety story. Once the email leaves, no mechanism in this PRD applies. The 48-hour rollback trigger (line 174) cannot recall a sent email.
2. No recipient resolution. The review screen shows "sent to: [recipients]" (line 118) with nothing on how recipients are determined or corrected. Resolving attendee lists across Zoom, Meet and Teams is engineering weeks, not a screen.
3. No partial-send idempotency. Slack and Notion are separate writes (line 83). Step 7 (line 62) assumes one atomic outcome. Nothing says what happens when Slack succeeds and Notion fails.
4. No edit-after-send or correction path anywhere in the document.

Design raised 4, Engineering raised 3, and the prior review raised all of them in May.

### 3. "Ready" auto-includes and hides content from a 66% accurate model

The review screen (line 124) says Ready items are already in the draft, do not need approval, and sit collapsed as a one-line preview (line 117).

Sarah Chen's interview says the opposite is where the damage happens. From `05-user-personas/sarah-chen.md:36`: confidence scores say high but critical items still get missed. Her interview puts it as "Every. Single. Time."

So the design tells the user to look hardest at the items the model already flagged, and to skim the ones it was confident about. That is the exact failure she reported.

Engineering and Design agreed on the fix and did not agree on who owns it, which does not matter. Fix: Ready items show full text, not a collapsed preview, until the monthly audit shows 80%. Collapse becomes available after the model earns it.

Related and unowned: multi-person items have no assignee field anywhere, yet the Jira and Linear export rule (line 85) requires "the assignee must accept." Nobody can accept an item that names three people or nobody.

### 4. The PRD contradicts itself in four places, and the user stories contradict the PRD

All four are text fixes with no engineering cost. All four block sprint estimation and QA test design as written.

1. **Three labels for two.** "Confidence vocabulary" (line 71) says every surface uses the same two labels, no new words. "Poor audio quality handling" (line 92) says items default to "Suggested". "Zero-state and edge cases" (line 130) says the same condition defaults to "Needs review".
2. **Two thresholds.** PRD says 70% (line 68). User Story 2 says 75% (`user-stories-smart-follow-ups.md:27`).
3. **Two rules for the percentage.** PRD says the raw percentage is never the primary signal (line 70). Story 2 says each item shows its confidence score as a percentage next to it (line 28).
4. **Two scopes.** PRD moves Jira and Linear to May (line 146). Story 5 still ships both at launch (`user-stories-smart-follow-ups.md:53`).

Also fix the broken citation on line 38. The file is real but the path drops its folder. Correct path: `outputs/june-2026-cohort/smart-followup-pressure-test-23-05-2026.md`. And correct line 155, which misstates what that review's top risk was.

### 5. Two of the three named personas cannot use this at launch

"Who It's For" (line 20) says three personas drive this feature.

1. **Marcus Okafor** is named on line 23. He is Enterprise, IT-deployed (`05-user-personas/marcus-okafor.md:8`). Line 145 scopes enterprise out until after June 2026 GA. He cannot use the feature at launch. Separately, the review screen claims its outbound data preview "addresses Marcus's privacy concern" (line 118). His actual objections are storage location, retention, SOC 2, and internal access (`marcus-okafor.md:33-37`). A recipient list answers none of them.
2. **Priya Nair** is named on line 24. Her stated frustration is that summaries are too long, 3-4 bullets wanted instead of 350 words (`priya-nair.md:34`). The PRD keeps the 350-word summary (line 56) and centers a review screen on someone who does not review action items in detail (`priya-nair.md:22`). She is High churn risk with Notion named as her replacement.
3. **Sarah Chen** is the one persona genuinely served, and her workflow is still not designed for. At 8-10 meetings a day and 5-8 items each, she has 50-80 review actions across 10 separate draft screens. The "under 2 minutes per meeting" target (line 133) measures per-draft speed when the real problem is queue volume. The prior review said this in May.

Either cut the personas the April release does not serve, or say what each one gets in April.

---

## 3 questions I need answered before the meeting

1. **Does April GA ship at current accuracy, yes or no?** If labeling has not started by 25-03-2026, which is eight days from now, does the date slip or does the feature ship in a degraded mode? There is no degraded-mode plan in the PRD. I need the decision rule in advance, not on 26-03. This question was asked in the May review and is still open.

2. **Is the send path in April scope, and who owns it?** Outbox with a cancel window, recipient resolution, and partial-send behaviour. It has been open since 23-05-2026 with no owner and no size. If it is out of scope for April, I want that written in "What We're NOT Building" as a decision, not left as a silence.

3. **What do reps sell in April to the three enterprise pilots and to Pro customers churning now?** The pilots are excluded for 10-plus weeks, accuracy is below target at GA, and Salesforce sync belongs to Dana's Platform pillar in May. This was question 3 in the May review and was never answered. It is now two reviews old.

---

## 1 thing in the PRD that's strong and should stay

**The phased, feature-flagged rollout with a defined gate at every phase (lines 166 to 174), now paired with the Observability table (lines 180 to 188).**

Internal dogfood, then top 10% of Pro, then all paid excluding enterprise, then Free, then enterprise. Each phase has an explicit go or no-go condition. For a machine learning change that touches every user's action items, this is the right structure. No role attacked it in this review, and no role attacked it in May either. That is two independent reviews endorsing the same section.

Keep the structure exactly as it is. The only repair it needs is the numbers inside it, covered in issue 1 and in the open item below.

---

## Disagreement worth noting

**Sales says the "Needs review" label is a demo liability. Design and Engineering both say keep it.**

Sales argued that a screen reading "4 Ready, 2 Needs review" (line 116) tells a buyer that MeetFlow's own AI does not trust its output.

Design refused to soften it: hiding uncertainty behind a falsely confident single state is the actual liability, and that is what burned Sarah in the first place. Engineering added that visible review state is the differentiator against a competitor's fire-and-forget approach, and that the May review had already settled this.

**Lead call: keep the labels, fix what sits behind them.** The label is honest. The problem is that "Ready" currently also means "collapsed and auto-included," which is the part that is not honest at 66% accuracy. Issue 3 fixes that without touching the vocabulary. Sales' underlying point stands and gets addressed by the May review's own recommendation: sell governance and control, meaning the send pause, recipient confirm and recoverability, rather than raw drafting quality.

---

## Open items I could not close

1. **Sales did not file a round 2.** Their round-1 position is recorded above and in the issues, but they did not answer Design's and Engineering's counterarguments, and they did not give a recommendation on hold, narrow, or reposition. Question 3 above is the one I most need them to answer.
2. **Launch readiness is disputed, not resolved.** Sales flagged no pricing, enablement, comms or battlecard. Design and Engineering both called this Sales' own deliverable rather than a PRD defect. My view: the battlecard and enablement belong to Sales, but the PRD does owe them a one-line value proposition, and right now it does not have one.
3. **Accessibility was deliberately deferred in May and re-raised now.** Design notes the PRD cites WCAG 2.1 Level A (line 76), but the 4.5:1 contrast minimum is criterion 1.4.3 at Level AA, so the yellow flag's contrast is unverified against the standard actually cited. Also unaddressed: keyboard-only operation of "Approve all," and whether a screen reader announces two or more items changing state at once. The May review deferred the broad audit on purpose. The mis-citation of the standard is worth correcting either way, since it is one line.
4. **Two numbers in the rollout table do not exist in the repo.** The rollback trigger references a "v1 baseline" (line 174) and phase 2 gates on a confirm rate of 75% or higher (line 169). Neither value appears anywhere. As written, neither can be coded into an alert or checked at a gate.

---

## Method note

Three subagents ran as Engineering Lead, Design and Sales/GTM. Round 1 was independent critique with no visibility into each other. Round 2 gave each role the other two positions and required them to concede, disagree, or take ownership.

Every claim above is cited to a file and a line. One finding was withdrawn during the debate: I reported the May pressure test file as missing, and Engineering correctly located it under `outputs/june-2026-cohort/`. It is a broken path in the citation, not missing evidence.
