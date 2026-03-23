# Technical Review: Action Item Confidence Scoring v2

**Reviewed:** 2026-03-21
**Verdict:** Needs Work

## Checklist

### 1. Spec Structure
- [x] Problem statement cites real data (34% error rate from product.md, 19/47 mentions from feedback-q1-2026.md, 4.1% churn from okrs-q2-2026.md)
- [x] Users affected are named personas with specific impact (Sarah, James, Priya - all with revenue figures and behavioral detail)
- [x] Success metrics have baselines AND targets sourced from existing files
- [x] Out of scope is specific - 7 explicit exclusions including Smart Follow-Up, Salesforce, multi-language
- [x] Open questions have owners and due dates

All pass. Structure is solid.

### 2. MeetFlow Architecture Impact
- [x] Action item extraction model - spec correctly identifies fine-tuning (not rebuild) of the 50K-meeting model, addresses all three known gaps (implicit commitments, multi-person, conditional)
- [x] Speaker diarization - spec addresses 8+ attendee failure mode in edge case #10, with "Assignee: unconfirmed" fallback
- [x] Model retraining - spec acknowledges the 2-week manual deployment cycle and explicitly scopes pipeline automation out
- [x] Integrations - spec states confirmed items flow to Slack, Notion, Jira, Linear "as they do today"
- [ ] **Integration format changes** - The spec adds a new "confidence score" field and a "Suggested Items" concept. It does not specify whether confidence scores are included in integration exports, or what the Slack digest format looks like with the new suggested/confirmed split. Open question #2 touches this but it's unresolved. Engineers will need this before building.
- [ ] **Transcription pipeline dependency** - The spec says "no changes to transcription pipeline" in Boundaries, but the extraction model consumes transcription output. If transcript accuracy drops below 80% in noisy environments (per product.md tech debt), action item accuracy will degrade regardless of model improvements. Spec should acknowledge this ceiling and state whether noisy-environment transcripts get different treatment.

### 3. Data and ML Considerations
- [x] Training data source identified (existing 50K labeled meetings for fine-tuning)
- [x] Accuracy target defined (66% to 80%, sourced from OKRs)
- [x] Feedback loop described (user confirm/dismiss logged as training data, available to ML team within 24 hours)
- [ ] **Training data for new gap areas** - The spec says "fine-tune for implicit commitments, multi-person items, conditional actions" but doesn't specify where the labeled training data for these gap areas comes from. The existing 50K dataset presumably has the same blind spots. Does the team need to label new data? How much? Who labels it? This is a blocking question for the ML team.
- [ ] **Measurement methodology** - Open question #3 asks how to measure accuracy in production but has no proposed answer. The spec needs at least a strawman: periodic labeled audit, user confirm/dismiss proxy, or both. Engineers will ask "how do we know if we hit 80%?" and "we shipped, now what?" needs an answer.
- [ ] **A/B testing or rollout strategy** - No mention of how this rolls out. Does it go to all users at once? Phased by plan tier? A/B test with old model as control? For a model change this significant (affects every meeting for every user), a rollout plan is expected.
- [ ] **Data privacy for feedback loop** - The spec logs user confirm/dismiss actions as training data. For Team and Enterprise users (Marcus Okafor's concerns in interview-02), does this training data include meeting content? Is it aggregated or per-user? Does it comply with data retention policies? Tomas's Enterprise pillar may need to weigh in before this ships.

### 4. Performance and Scale
- [x] Latency budget specified (90 seconds total, scoring adds no more than 15 seconds, compared to 45-90 sec baseline from product.md)
- [x] Back-to-back meeting handling addressed (edge case #12, no cross-contamination)
- [ ] **Scale for power users** - Sarah Chen runs 8-10 meetings/day. The spec doesn't address whether the confirm/dismiss UI creates a new daily workflow burden. If she has 5-8 suggested items per meeting across 10 meetings, that's 50-80 review actions per day. Is that better or worse than her current 30 min of manual correction? Quantify the expected suggested item volume so eng can design the right UI.
- [ ] **Concurrent meeting processing** - If a user has overlapping or rapid-fire meetings (common for Sarah's profile), does the system queue extraction jobs? Process in parallel? The spec says "meeting N finalized before N+1 starts processing" but doesn't address what happens if N takes longer than expected and N+1 is already waiting.

### 5. Error Handling and Edge Cases
- [x] Model failure/timeout handled (show raw transcript, retry once)
- [x] Empty state defined (no action items detected, manual add prompt)
- [x] Short meetings (<5 min) - skip suggested items, high-confidence only
- [x] Large meetings (8+) - separate assignee confidence from item confidence
- [ ] **Poor audio quality** - product.md documents transcript accuracy drops below 80% in noisy environments. The spec doesn't address what happens to action item extraction when the input transcript is unreliable. Should the system surface a warning like "Transcript quality was low - action items may be less accurate"? Or suppress low-confidence items entirely?
- [ ] **Transition behavior** - What happens to existing action items already extracted with v1? Do historical meetings get re-processed? Do users see confidence scores on old meetings or only new ones? Engineers need to know the migration story.

### 6. Dependencies and Sequencing
- [x] Downstream dependency identified - Smart Follow-Up (April 2026) depends on this shipping first
- [x] Cross-pillar awareness shown - Salesforce integration (Dana) explicitly scoped out
- [ ] **Upstream dependency on Aisha's team** - The extraction model consumes transcription output. Transcript Accuracy v2 (Aisha, June 2026) ships after this. Should this spec reference the current transcription limitations as a known constraint? If Aisha's improvements later boost transcript quality, does the action item model need retraining again?
- [ ] **Timeline not stated** - The spec has no target ship date. The Q2 roadmap (product.md) shows Smart Follow-Up targeting April 2026 and it depends on this feature. That means this must ship before April. When? March? The spec needs a date so eng can plan sprints.

### 7. Observability and Rollback
- [ ] **No production monitoring defined** - How does engineering know if the v2 model is performing better than v1 in production? What dashboard or metric do they watch? Accuracy is measured by labeled audits (per open question #3), but that's periodic. What's the real-time proxy? Confirm/dismiss ratio? Average confidence score trending?
- [ ] **No rollback criteria** - If the v2 model performs worse than v1 (it happens with ML), what's the trigger to roll back? What metric, at what threshold, over what time window?
- [ ] **No feature flag mentioned** - Can this be feature-flagged so eng can roll out to 10% of users first? For an ML model swap that affects every user's action items, gradual rollout is standard practice. The spec should state whether this is expected.
- [ ] **No logging requirements** - For debugging model outputs, engineers need to know what to log. At minimum: input transcript snippet, extracted items, confidence scores, and user feedback actions. The spec doesn't specify retention or access requirements for these logs.

### 8. Tier and Access Control
- [ ] **Plan availability not specified** - Which plans get confidence scores and suggested items? All plans (Free/Pro/Team)? If Free users get it, that's a broader rollout surface. If only Pro+, the feature flag and rollout are simpler. This affects eng scope.
- [ ] **Enterprise implications** - Enterprise tier GA is June 2026 (Tomas's scope). If enterprise customers need audit logs of AI decision-making (confidence scores, user overrides), this feature may need to emit structured audit events. Worth flagging to Tomas now rather than retrofitting later.

---

## Top 5 Engineer Questions You'll Get

1. **"Where does the training data for implicit commitments come from? The existing 50K dataset has the same gaps."**
   **Suggested answer:** GAP - spec doesn't address this. You need to work with the ML team to determine if new labeling is required, how much, and the timeline impact.

2. **"How do we roll this out - big bang to all users or phased? Can we feature-flag it?"**
   **Suggested answer:** GAP - add a rollout section. Recommend: feature-flagged, phased rollout starting with Pro power users (Sarah Chen segment), measure confirm/dismiss rates and accuracy proxy for 1-2 weeks, then expand.

3. **"What do we log for debugging, and how do we know if the model is regressing in production?"**
   **Suggested answer:** GAP - add observability requirements. At minimum: log extracted items with confidence scores, user feedback actions, and transcript quality signal. Dashboard showing confirm/dismiss ratio and average confidence score as real-time proxies.

4. **"What happens to action items on meetings with bad audio? The transcript is garbage, so won't the action items be garbage too?"**
   **Suggested answer:** PARTIAL - the spec addresses 8+ attendee diarization issues but not poor audio quality. product.md documents <80% accuracy in noisy environments. Add a transcript quality gate or warning.

5. **"What's the actual ship date? Smart Follow-Up depends on us and it's targeting April."**
   **Suggested answer:** GAP - add a target date. Based on the Q2 roadmap dependency chain, this needs to ship by mid-March 2026 at the latest to give Smart Follow-Up beta time in early April.

---

## Summary

The spec is strong on problem framing, user impact, functional requirements, and error handling. The Shape Up structure (boundaries, rabbit holes, no-gos) is well done. The biggest gaps are in **observability/rollback** (entire category missing), **rollout strategy** (no feature flag or phased plan), and **ML training data sourcing** (the spec assumes fine-tuning will work but doesn't address where labeled data for the three gap areas comes from). Fix these three areas and the spec is ready for eng walkthrough.
