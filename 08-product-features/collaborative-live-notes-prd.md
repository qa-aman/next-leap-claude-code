# PRD - Collaborative Live Notes

**Pillar:** AI Intelligence
**Owner:** Senior PM, AI Intelligence
**Target:** September 2026 (beta) / Q4 2026 (GA)
**Status:** Draft

---

## Problem

MeetFlow's output is fully automated: the user receives a summary and action items after the meeting and has no way to write alongside the AI while it happens. This breaks down for the exact users MeetFlow needs most. Action items are wrong or missing 34% of the time (`03-product-knowledge/product.md`), so power users like Sarah Chen double-check every action item manually, defeating the purpose (`05-user-personas/sarah-chen.md`). Teams like Marcus Okafor's take notes in Google Docs, not MeetFlow, and work around the tool entirely (`05-user-personas/marcus-okafor.md`).

Granola is winning these users on exactly this gap: its "enhanced notes" approach lets users write alongside the AI, creating a collaborative note-taking experience rather than pure automation, and it is rated a **High** threat for power users (`03-product-knowledge/competitive.md`). When users keep their real notes in another tool, MeetFlow stops being the system of record, trust erodes, and Pro churn (4.1% monthly per `03-product-knowledge/company.md`) compounds.

Cross-reference: `03-product-knowledge/product.md` for full feature context.

---

## Who It's For

- **Sarah Chen - "The Power User"** - Head of Product. Runs 8-10 back-to-back meetings daily and uses AI action items as her primary task list, but manually re-checks everything because she can't trust the output. A live notes layer lets her capture and correct in the moment instead of cleaning up after. See `05-user-personas/sarah-chen.md`.
- **Marcus Okafor - "The Skeptic"** - Engineering Manager at an Enterprise fintech. His team takes notes in Google Docs and ignores MeetFlow's AI summaries; his primary blocker is data privacy and the absence of SOC 2 Type II certification, not note-taking habit alone. Live Notes does not solve that blocker. However, a shared notes layer inside MeetFlow can reduce the Google Docs workaround for teams that do become comfortable enough to engage, provided Enterprise data controls (SOC 2, on-prem storage) ship first via the Enterprise Tier GA in June 2026. Marcus is a renewal risk, not a conversion opportunity, and this PRD does not claim otherwise. See `05-user-personas/marcus-okafor.md`.
- **Priya Nair - "The Casual"** - Wants "good enough" notes without another tool. A simple in-meeting note pane that merges with the AI summary reduces the pull toward Notion AI for casual capture. See `05-user-personas/priya-nair.md`.

---

## What It Does

- Opens a live notes pane during the meeting where the user types alongside the running transcript and AI capture.
- Merges user-written notes with the AI-generated summary into a single document after the meeting, with user edits clearly distinguished from AI text.
- Lets the user promote any line of their own notes into a tracked action item, bypassing the extraction model for things they want to guarantee are captured.
- Lets the user accept, edit, or dismiss AI-suggested action items inline rather than only reviewing them after the fact.
- Supports shared notes on Team plan meetings, so multiple attendees write into the same live document in real time.

---

## How It Works

1. The user joins a meeting MeetFlow is recording and opens the Live Notes pane (available in the desktop and web app during an active session).
2. As the meeting runs, MeetFlow streams the live transcript on one side and AI-suggested action items as they are detected; the user's note pane sits alongside.
3. The user types free-form notes during the meeting; their text is saved continuously and visibly marked as user-authored.
4. The user can highlight a line and "make this an action item," or accept/edit/dismiss any AI-suggested action item inline.
5. On Team meetings, other attendees with access see and add to the shared note in real time, with authorship attribution per contributor.
6. When the meeting ends, MeetFlow merges the user notes and the AI summary into one final document, preserving the distinction between human and AI content, and syncs to the user's existing destinations (Notion, Slack).

---

## Success Metrics

- Live Notes adoption: target 35% of Pro users use the live notes pane in at least one meeting within 90 days of GA. Baseline: 0% (new feature). Benchmark: Smart Follow-Up carries a 40% Pro adoption KR in `04-strategy/okrs-q2-2026.md` (Objective 1, Key Result 3 - "Smart Follow-Up adoption rate: 40%"); 35% is set slightly below that because live notes requires active in-meeting behavior, a higher-friction bar than reviewing a follow-up draft after the meeting ends.
- Pro monthly churn: contribute to the reduction from 4.1% to the 2.5% target. Baseline: 4.1% (`04-strategy/okrs-q2-2026.md`, Objective 3).
- NPS: contribute to the move from 34 to the 45 target by giving power users a reason to trust and stay. Baseline: 34 (`04-strategy/okrs-q2-2026.md`, Objective 3).
- Team plan seats: support the 200 to 400 seat target by making shared live notes a concrete Team-tier differentiator. Baseline: 200 seats (`04-strategy/okrs-q2-2026.md`, Objective 2).

Cross-reference: `04-strategy/okrs-q2-2026.md` for how these tie to quarterly goals (Objective 2: Grow Team plan adoption; Objective 3: Stop Pro users from leaving).

---

## Risks

- **Ship-sequence risk (High):** Shared live notes on Team meetings lands directly on the data privacy fault line that makes Marcus Okafor a renewal detractor. Real-time sync of shared notes in Enterprise accounts will surface data residency and SOC 2 objections before Enterprise Tier GA ships those controls in June 2026. If Live Notes Team-tier beta ships to enterprise accounts before SOC 2 is confirmed, it accelerates the renewal risk rather than reducing it. Mitigation: gate shared Team notes behind the Enterprise Tier GA milestone (31-12-2026 GA aligns with this).
- **Dependency drift risk (Medium):** Action Item Confidence Scoring v2 ships 28-03-2026, but Live Notes beta is 30-09-2026 - a 6-month gap. The inline accept/edit/dismiss flow depends on a model that may change or degrade in the interim. If the model is retrained between March and September, the UX assumptions built around its output format may break. Mitigation: product and engineering alignment checkpoint at the real-time sync infrastructure readiness milestone (31-07-2026).
- **Engagement risk (Medium):** Live Notes requires users to change behavior during a meeting, the highest-friction moment to introduce a new tool. If adoption stays below 15% at 60 days post-beta, the feature does not move churn or NPS at a scale that justifies the real-time sync infrastructure investment. Mitigation: if the 60-day beta cohort adoption is below 15%, defer GA and run a targeted in-product onboarding experiment (prompted entry into the notes pane at the start of each meeting) before committing the Team-tier real-time sync infrastructure spend. GA decision is contingent on crossing the 15% floor, not on completing the calendar milestone.

---

## What We're NOT Building

- Offline note-taking - Live Notes requires an active, connected meeting session in v1.
- A standalone notes app or general doc editor - notes exist only attached to a meeting, not as free-floating documents.
- Rich formatting beyond basic text and bullets - no tables, embeds, or images at launch.
- Mobile live editing - desktop and web only in v1; mobile is view-only.
- Retroactive editing of past meetings' transcripts - users edit notes and action items, not the underlying transcript.
- Replacing the action item extraction model - Live Notes complements Action Item Confidence Scoring, it does not remove the need to fix it.

---

## Dependencies

- **Action Item Confidence Scoring v2** must ship first. Inline accept/edit/dismiss of suggested action items only adds value if the suggestions are worth reviewing; garbage suggestions make the inline flow noise (`03-product-knowledge/product.md`, current sprint).
- **Real-time sync infrastructure** is required for shared Team notes and continuous save. Today summary generation runs as a 45-90 second post-meeting batch (`03-product-knowledge/product.md`, Tech Debt); live collaborative editing needs new low-latency sync that does not exist yet.
- **Speaker diarization reliability** affects attribution in shared notes; diarization currently fails for meetings with 8+ attendees (`03-product-knowledge/product.md`, Tech Debt).
- **Platform team (Dana)** for Notion and Slack sync of the merged document into existing destinations.

---

## Timeline

| Milestone | Date |
|-----------|------|
| Action Item Confidence Scoring v2 ships (prerequisite) | 28-03-2026 |
| Real-time sync infrastructure ready | 31-07-2026 |
| Beta (Pro single-user live notes) | 30-09-2026 |
| GA (Pro + Team shared notes) | 31-12-2026 |
