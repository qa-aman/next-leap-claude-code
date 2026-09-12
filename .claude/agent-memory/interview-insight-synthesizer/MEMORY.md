# Interview Insight Synthesizer - Memory

Consult this before Stage 3 ranking and again before writing the Stage 4 recommendations.

## Roadmap status that changes how a theme is reported

### Action item accuracy is already in development, shipping in about a month

Recorded 08-08-2026. In the repo's fictional timeline (today is 17-03-2026 per `CLAUDE.md`), the work is the **Action Item Confidence Scoring v2** sprint, 17-03-2026 to 28-03-2026, with **Smart Follow-Up** landing April 2026.

**What this does NOT change:** still extract, cluster, rank and report the accuracy pains exactly as the transcripts state them. The evidence is real, the users said it, and suppressing or downgrading a theme because a fix is in flight would falsify the research. Accuracy has ranked first in every synthesis so far, on Sarah Chen and James Whitfield.

**What this DOES change:** the recommendation line. Do not recommend starting, scoping or prioritising accuracy work as if it were an open decision. It is already funded and in the current sprint. Write the recommendation as a confirmation and a sharpening instead, for example which specific failure mode the shipped version must cover (implicit commitments, confidence-score reliability), or what to measure after it lands.

**Why it matters:** a brief that tells the PM to go build the thing being built this sprint reads as not knowing the roadmap, and it buries the themes that genuinely need a decision.

## Standing observations from prior runs

1. Four transcripts in `07-user-interviews/`: Sarah Chen, Marcus Okafor, Priya Nair, James Whitfield. All four cleared the 3-pain gate on a first read (5 / 6 / 4 / 4).
2. Themes that recur and are NOT covered by the accuracy work, so they carry the real decision weight:
   - **Missing native integrations.** James Whitfield, 22 seats, has a Fireflies pilot lined up against an end-of-Q1-2026 deadline. Salesforce is slated for May 2026, which is after his deadline. This is the live risk.
   - **Distrust blocking expansion revenue.** Sarah Chen has an 8-seat Team upgrade pitched to her CEO and held pending accuracy. Worth reporting because it converts the accuracy fix into a revenue number, not because the fix needs deciding.
   - **Privacy and data control.** Marcus Okafor only, so it ranks last on interview count despite a workflow-breaker severity. Belongs to the Enterprise tier workstream (June 2026 GA), not to AI Intelligence.
   - **Weak perceived value and price sensitivity.** Marcus and Priya. Tolerated today, exposed to Notion bundling.
3. Quote fidelity note: James Whitfield's Salesforce quote in `interview-04-james-whitfield.md` contains an em dash. Preserve it. It is source text, and the no-em-dash writing rule governs your own prose, not a verbatim quote.

## How to maintain this file

Append a roadmap-status entry whenever the user tells you a theme is already being built, already shipped, or explicitly out of scope, and record what it changes about the recommendation rather than about the finding. Keep the distinction sharp: status changes advice, never evidence.
