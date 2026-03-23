# Change Log - Smart Follow-Up Emails PRD

## 2026-03-23

Updates based on Technical Review: Action Item Confidence Scoring v2 (`outputs/technical-review-action-item-v2.md`).

### Added

- **Plan Availability section** - Defined feature access by tier (Free: 5 drafts/month no scores, Pro: full feature, Team: full + analytics).
- **Integration export format** - Specified how confidence scores appear in Slack (colored dots), Notion/Jira/Linear (metadata field with Suggested/Confirmed status).
- **Poor audio quality handling** - Added banner warning and default-to-Suggested behavior when transcript quality is low (<80% accuracy).
- **Measurement methodology** - Two-track approach: confirm/dismiss ratio as real-time proxy, monthly labeled audit of 200 meetings as source of truth for 80% target.
- **Review burden for power users** - Addressed Sarah Chen's 50-80 daily review actions with auto-include for high-confidence items, batch review, and 2-minute-per-meeting target.
- **Training data dependency** - Flagged that existing 50K dataset has the same blind spots; ML team needs new labeled data for implicit commitments, multi-person, and conditional items. Blocking dependency.
- **Transcript quality ceiling** - Documented that Transcript Accuracy v2 (Aisha, June 2026) ships after this feature, capping action item quality in noisy environments.
- **Privacy review for feedback loop** - Flagged need to confirm with Tomas whether training data includes meeting content and complies with retention policies for Team users.
- **Rollout Strategy section** - 4-phase feature-flagged rollout: internal dogfood, Pro power users, all paid, then Free. Includes gate criteria per phase.
- **Observability section** - Defined 5 tracking signals (confirm/dismiss ratio, avg confidence, draft acceptance, latency, transcript quality flag rate) with alert thresholds. Added logging requirements with 90-day retention.
- **Rollback criteria** - Confirm/dismiss ratio drops below v1 baseline for 48 hours, or P0 bug.

### Updated

- **What We're NOT Building** - Added: re-processing historical meetings (new meetings only), audit log events deferred to Enterprise GA (June 2026).
- **Dependencies** - Expanded from 2 items to 5, adding training data sourcing, transcript quality ceiling, and privacy review as blocking items.
