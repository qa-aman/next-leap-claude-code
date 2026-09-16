# PRD - Meeting Pattern Insights (Beta to GA)

**Pillar:** AI Intelligence
**Owner:** AI Intelligence PM
**Target:** June 2026
**Status:** Draft (feature is live in Beta with 800 users, `03-product-knowledge/product.md`)

---

## Problem

Meeting Pattern Insights is in Beta with 800 users and the weekly digest email opens at 43%, against a Q2 Key Result of 50% (`03-product-knowledge/product.md`, `04-strategy/okrs-q2-2026.md` Objective 2). The people it is built for are not switching it on: Sarah Chen, the target power user, has not enabled it because "if it can't get action items right, why would I trust it to tell me how I spend my time?" (`07-user-interviews/interview-01-sarah-chen.md`). Meanwhile the one digest that does work, the Slack digest, is the second most praised feature with 12 mentions (`06-user-feedback/feedback-q1-2026.md`), and Insights does not ship through it. Team plan sits at 200 seats against a 400 target, and Insights is the only feature on the roadmap built for the "visibility across multiple meetings" that Team users are defined by (`04-strategy/product-vision.md`).

Cross-reference: `03-product-knowledge/product.md` for full feature context.

---

## Who It's For

- **Sarah Chen** - Head of Product, 8-10 meetings a day, Pro. She needs meeting-load and talk-time data she can verify against the meetings it came from, because her trust in the AI is already eroding. See `05-user-personas/sarah-chen.md`.
- **Priya Nair** - Chief of Staff, 2-3 high-stakes meetings a week, Pro. She never opens the app. Her CEO reads the Slack digest every morning, so a weekly pattern digest is only useful to her if it lands in Slack as 3-4 bullets. See `05-user-personas/priya-nair.md`.
- **Marcus Okafor** - Engineering Manager, Enterprise, IT-deployed. He will block any talk-time analytics on his team unless he can see where the data lives and switch it off. Insights on the Team tier has to survive his review. See `05-user-personas/marcus-okafor.md`.

---

## What It Does

- Sends the weekly digest through Slack as well as email, using the same delivery the existing Slack digest already uses.
- Links every number in the digest (hours, talk-time ratio, recurring topic, "could be an email") to the meetings it was computed from, so a user can check it in one click.
- Adds a Team view for Team plan admins: meeting load and recurring topics across the team, with per-person talk-time visible only to that person by default.
- Gives every user an on/off switch for their own analytics, and gives Team admins a written note on what is computed and where it is stored.
- Keeps the four Beta insights (total meeting hours, talk-time ratio, recurring topics, meetings that could be emails) unchanged.

---

## How It Works

1. Every Monday at 08:00 in the user's timezone, the system computes the four insights from the previous week's recorded meetings.
2. The user receives the digest by email and, if the Slack integration is connected, as a 3-4 bullet message in the channel they already use for summaries.
3. Each bullet carries a link. Clicking "6.5 hours in recurring status meetings" opens the list of those meetings with their summaries.
4. The user can mark an insight as "not useful" from the digest. That signal feeds the next week's ranking of which insights lead.
5. A Team plan admin opens the Team view and sees aggregate load and recurring topics for their team. Per-person talk-time is hidden unless the individual has turned sharing on.
6. Any user can switch their analytics off from Settings. When off, their meetings are excluded from the Team aggregates and their digest stops that week.

---

## Success Metrics

- Weekly digest open rate: improve from 43% to 50% by end of Q2 2026 (`04-strategy/okrs-q2-2026.md`, Objective 2).
- Team plan seats: contribute to the move from 200 to 400 by end of Q2 2026 (`04-strategy/okrs-q2-2026.md`, Objective 2). Insights-attributed seats: target to be set with the AI Intelligence PM and Sales, no attribution baseline exists yet.
- Insights enabled among Pro users: baseline 800 Beta users out of 2,800 Pro (`03-product-knowledge/company.md`). Target: to be set with the AI Intelligence PM, no OKR covers enablement.
- Click-through from a digest insight to a source meeting: no baseline, the Beta digest has no links. Target: to be set with the AI Intelligence PM after four weeks of GA data.

Cross-reference: `04-strategy/okrs-q2-2026.md` for how these tie to quarterly goals.

---

## What We're NOT Building

- New insight types (sentiment, engagement scores, speaker interruptions). The four Beta insights ship as they are.
- Manager view of individual talk-time by default. It is opt-in per person, or it does not exist.
- Calendar write-back (auto-declining or shortening meetings flagged as "could be an email").
- Notion or Jira delivery of the digest. Email and Slack only at GA.
- A standalone Insights dashboard in the app. The digest is the product.

---

## Dependencies

- **Action Item Confidence Scoring v2** must ship first (current sprint, 17-03-2026 to 28-03-2026). Sarah's refusal to enable Insights is a trust ceiling set by action item accuracy, and the researcher notes say no new feature moves her until that is fixed (`07-user-interviews/interview-01-sarah-chen.md`).
- **Slack integration (GA)** is the delivery channel. Nothing new to build, but the digest has to reuse its channel configuration rather than ask users to set one up again.
- **Enterprise data-handling documentation** from Tomás Herrera's Enterprise & Security pillar. The Team view will not pass Marcus Okafor's review without a written statement of what is computed and where it is stored (`05-user-personas/marcus-okafor.md`).

---

## Timeline

| Milestone | Date |
|-----------|------|
| Action Item Confidence Scoring v2 ships | 28-03-2026 |
| Slack delivery and source-meeting links live for the 800 Beta users | 15-05-2026 |
| Team view and per-user opt-out live for Beta Team accounts | 05-06-2026 |
| GA to all Pro and Team users | 26-06-2026 |

Open question: Insights GA is not on the Q2 roadmap table in `03-product-knowledge/product.md`, which lists four other bets. The June target assumes it fits alongside Enterprise GA and Transcript Accuracy v2. Confirm with the product team before this leaves Draft.
