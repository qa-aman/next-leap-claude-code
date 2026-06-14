---
name: feedback-critic-patterns
description: Recurring prd-critic failure modes and the fixes that cleared the quality bar, sourced from the Collaborative Live Notes review loop (17-03-2026).
metadata:
  type: feedback
---

## Patterns the prd-critic consistently flags

### 1. Paraphrased quotes presented as direct quotes
Rule: Only use text that appears verbatim in the persona files (blockquoted with ">"). Strip quotation marks from any description that is a paraphrase, even if it closely mirrors the source.
**Why:** Violates the user-research rules in `.claude/rules/user-research.md`. Creates a verifiability gap the critic catches immediately.
**How to apply:** Before wrapping any Problem section language in quotes, check the persona file for the exact blockquoted line. If not present verbatim, restate without quotes.

### 2. Persona fit misread - naming a persona whose blocker the feature does not solve
Rule: If a persona's primary blocker is not addressed by the feature, say so explicitly. Do not frame them as a conversion opportunity if the feature cannot convert them.
**Why:** The critic reads persona files to verify fit. If Marcus Okafor's blocker is data privacy and the feature is live notes, claiming live notes converts him is a factual error.
**How to apply:** For each persona in "Who It's For," test: does this feature directly address their primary blocker? If not, state the dependency explicitly (e.g., "Live Notes does not solve his primary blocker; conversion requires Enterprise data controls shipping first").

### 3. Missing Risks section
Rule: The repo template (14-templates/template-prd.md) does not have a named Risks section, but the prd-critic rubric scores it as a standalone dimension. Always add a Risks section with exactly 3 prioritized entries (High/Medium/Medium is a proven structure).
**Why:** Risks score was 0/2 on the first pass because the Dependencies section was being used as a proxy for risk. The critic distinguishes them.
**How to apply:** Insert "## Risks" between "## Success Metrics" and "## What We're NOT Building". Three entries: one ship-sequence risk (around inter-feature or privacy dependencies), one dependency drift risk (model/infra gap between dependent feature ship and this feature's launch), one engagement risk (behavior change friction).

### 4. Unsourced target numbers on the primary feature-level metric
Rule: If the adoption target for a new feature has no comparable real-world baseline (0% baseline is trivially true for any new feature), anchor the target to a real comparable KR in okrs-q2-2026.md.
**Why:** The critic treats "0% baseline, 35% target" as soft unless the target is grounded in something real. Smart Follow-Up's 40% adoption KR is the canonical comparable for AI Intelligence pillar features.
**How to apply:** Find the closest launched or upcoming feature with an OKR adoption target. Cite file, objective, and exact KR text. Set the new feature's target slightly below if it requires higher-friction user behavior (e.g., in-meeting vs. post-meeting).

### 5. Procedural mitigations in risk entries
Rule: Risk mitigations must name a hard action tied to a concrete threshold. "Evaluate criteria before GA" is not a mitigation. "If X metric is below Y at day Z, defer GA and take action A" is.
**Why:** The critic downgraded the engagement risk entry from passing to a half-point deduction for procedural language. Concrete thresholds make risks actionable rather than deferred.
**How to apply:** Structure every mitigation as: "If [measurable signal] at [date/milestone], then [specific action]."

## What scored 8+ on the second iteration

- Marcus persona rewrite: explicitly stating the feature does not solve his primary blocker AND naming the dependency that would change that (Enterprise Tier GA shipping data controls) scored 2/2 on user specificity.
- Risks section with High/Medium/Medium priority labels and concrete mitigations scored 1/2 (half point lost for procedural language, fixed in post-8 polish).
- OKR-anchored success metrics with explicit Objective + KR text references scored passing on measurability.

## Files with the strongest citable stats per feature area

- Action item accuracy: `03-product-knowledge/product.md` (34% wrong/missing) and `03-product-knowledge/company.md` (same stat with churn context)
- Pro churn baseline: `03-product-knowledge/company.md` (4.1% monthly)
- OKR targets: `04-strategy/okrs-q2-2026.md` - contains churn target (2.5%), NPS target (45), Team seats target (400), Smart Follow-Up adoption KR (40%), Free-to-Pro target (8%)
- Competitor threat levels: `03-product-knowledge/competitive.md` - exact "High threat" language for Granola and Fireflies
- Tech debt signals: `03-product-knowledge/product.md` Tech Debt section - 45-90s summary latency, diarization fails at 8+ attendees

## Persona-to-feature mappings the critic accepted

- Sarah Chen: fits any AI Intelligence feature that addresses action item accuracy or in-meeting trust
- Priya Nair: fits features that reduce friction or the pull toward Notion AI for casual users
- Marcus Okafor: appropriate to name only when (a) the feature addresses his data privacy/SOC 2 blocker directly, OR (b) the PRD explicitly acknowledges his primary blocker is unsolved and names the dependency that would unlock him

See [[feedback-critic-patterns]] for the full loop history.
