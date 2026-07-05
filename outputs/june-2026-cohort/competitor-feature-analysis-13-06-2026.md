# Competitor Feature Analysis - AI Meeting Intelligence
**Date:** 13-06-2026
**Scope:** AI Intelligence pillar (Smart Summaries, Action Item Confidence Scoring, Meeting Pattern Insights) plus integrations, transcription, and enterprise where competitors create direct pressure
**Competitors covered:** Notion AI, Granola, Fireflies, Otter.ai, Fathom

---

## Bottom Line

MeetFlow's most acute exposure is on action item reliability and post-meeting workflow automation. Notion AI now ships action items with owner, priority, and due date fields linked into Notion's task system - for free on its Business plan - while MeetFlow's action item accuracy sits at 66% (per `03-product-knowledge/company.md`). That gap is the single most dangerous thing on this list. The one thing to do first: ship Action Item Confidence Scoring v2 with confirmed-dismiss UX and user-correction feedback loops before Smart Follow-Up launches in April 2026, then use that correction data to accelerate model retraining. Everything else on this list is secondary to that.

---

## Competitor Snapshots

### Notion AI
**Positioning:** All-in-one workspace with AI bundled into the Business plan ($20/seat/month). AI meeting notes is not a standalone product - it is one capability inside Notion's workspace, which makes the switching cost low for teams already using Notion.

**Relevant AI features (from official page, validated):**
- No-bot recording via system audio capture - works with Zoom, Google Meet, Teams, and in-person meetings
- Auto-joins calendar events (Notion Calendar integration) and generates summaries immediately after meeting ends
- Summaries are tailored by meeting type: 1:1s, team syncs, client calls, interviews, brainstorms
- Action items extracted with owner, priority, and due date fields attached
- Action items push directly into Notion Agent tasks and existing Notion databases
- Full search across all meeting transcripts via Enterprise Search (Business plan)
- Supports 19 languages (16 fully released, 3 in beta)
- Data retention configurable by admin; zero LLM training on customer data; SOC 2 Type 2

**Pricing:** AI Meeting Notes is included at no additional cost on the Business plan ($20/seat/month, or free trial on Plus). Shipped in Notion 2.51, 13-05-2025.

**Official source:** https://www.notion.com/product/ai-meeting-notes | https://www.notion.com/releases/2025-05-13

---

### Granola
**Positioning:** AI notepad for professionals in back-to-back meetings. Privacy-first, bot-free. Now cross-platform (Mac, Windows, iPhone) after being Mac-only through 2024. $125M Series C raised 25-03-2025. Prosumer and SMB; enterprise tier launching.

**Relevant AI features (from official pages, validated):**
- Bot-free transcription using system audio - no bot joins the meeting
- Enhanced notes: user writes alongside AI, AI fills gaps from transcript rather than replacing human notes
- Meeting Briefs: pre-meeting context card showing who you are meeting, what was discussed last time, and open items
- Agentic Chat: post-meeting questions, draft follow-ups, extract specific data (budgets, objections, decisions) across all meeting history with inline citations
- Customizable note templates per meeting type
- MCP integration: meeting notes connect to Claude, ChatGPT, and Cursor via Model Context Protocol
- Team Folders and shared Spaces for collaborative note access
- CRM push (HubSpot, Attio, Affinity), Notion sync, Slack (Business tier, $14/seat/month)
- API access and Zapier on Business tier
- SOC 2 Type 2 (certified July 2025), GDPR compliant, no audio storage
- Multi-language: 10 languages supported

**Pricing:** Basic free (limited history); Business $14/seat/month (unlimited history, integrations, API); Enterprise $35/seat/month (SSO, admin controls, usage analytics)

**Official source:** https://www.granola.ai | https://www.granola.ai/pricing | https://www.granola.ai/updates

---

### Fireflies
**Positioning:** Integration-first meeting intelligence. 100+ integrations including Salesforce, HubSpot, Pipedrive. Primary buyer is sales ops, RevOps, and enterprise procurement. Not a product you recommend to a friend - a product teams buy. Two-year head start on CRM workflows.

**Relevant AI features (from official pages, validated):**
- AskFred: ChatGPT-like assistant scoped to meeting transcripts; works on individual meetings or across all meetings
- AI Skills: pre-built or custom prompt templates that run automatically after every meeting on a configurable schedule (on-demand, per-meeting, or recurring cross-meeting). Examples: BANT scoring, MEDDIC reports, objection extraction, competitor mention tracking, candidate scorecards
- Conversation Intelligence suite: sentiment analysis (positive/negative/neutral per meeting), topic tracking, talk-time analytics, filler word detection, questions asked per speaker, longest monologue tracking
- Team coaching dashboard: compare rep performance across meetings, identify communication patterns, track trends over time
- Salesforce integration specifics: auto-creates Leads/Contacts/Opportunities, syncs transcript summaries and action items as Salesforce Tasks, enables manual resync of historical meetings, configurable auto-create vs. log-only behavior

**Pricing:** Free ($0, 400 min/team, 20 AI credits); Pro ($10/seat/month annual, 8,000 min, AI Skills, voice agents); Business ($19/seat/month annual, unlimited storage, video recording, conversation intelligence, team analytics); Enterprise ($39/seat/month annual, SSO, SCIM, audit logs, HIPAA, private storage)

**Official source:** https://fireflies.ai/pricing | https://fireflies.ai/conversation-intelligence | https://fireflies.ai/integrations/crm/salesforce | https://fireflies.ai/skills

---

### Otter.ai
**Positioning:** Market leader in brand recognition. Free tier with 300 min/month drives top-of-funnel. Pivoting up-market with Otter Meeting Agent and Otter Sales Agent targeting sales teams and enterprise. CRM sync now available on Pro ($8.33/seat/month annual).

**Relevant AI features (from official pages, validated):**
- Real-time transcription that streams live to all meeting participants (not post-meeting only)
- Automated summaries with action items, takeaways panel, and outline structure
- AI Chat: ask questions like "what did the client say about timeline?" across full meeting history
- Otter Sales Agent: pre-call briefing with deal value, key decision makers, and last interaction summary; real-time coaching tips on objections during live calls; auto-drafts personalized follow-up emails post-call; detects commitments and suggests next steps
- Salesforce and HubSpot sync on Pro+ plans
- Custom AI workflows on Business+; unlimited custom workflows on Enterprise
- MCP server integration (recently shipped)
- 6-language transcription support
- Enterprise: SSO, SCIM, domain capture, HIPAA on Enterprise

**Pricing:** Basic (free, 300 min/month); Pro ($8.33/seat/month annual, 1,200 min, Salesforce/HubSpot sync); Business ($19.99/seat/month annual, unlimited recordings, 4 hours/meeting, 3 concurrent meetings); Enterprise (custom, SSO, HIPAA, Sales Agent, custom CRM integrations)

**Official source:** https://otter.ai/pricing | https://otter.ai/features | https://otter.ai/sales-agent

---

### Fathom
**Positioning:** Free-first individual notetaker. Generous free tier (unlimited recording, transcription, summarization). Paid tiers unlock 15+ meeting templates, follow-up email drafting, CRM sync. Notable for wide template library and clean UX. Less integration depth than Fireflies; less design quality than Granola.

**Relevant AI features (from official pages, validated):**
- 15+ expert meeting templates including BANT, Sandler, and other sales frameworks (Premium+, $16/seat/month annual)
- AI action items (Premium+)
- AI follow-up email drafting (Premium+)
- Ask Fathom: conversational assistant scoped to a single call (Free, limited) or all calls (Premium+, unlimited)
- AI search alerts
- Salesforce and HubSpot CRM sync (all paid tiers); CRM field sync on Business ($25/seat/month annual)
- MCP integration and public API
- Multilingual summaries (28 language translation)

**Pricing:** Free ($0, unlimited recording/transcription/summaries, limited AI); Premium ($16/seat/month annual); Team ($15/seat/month annual, 2-user min); Business ($25/seat/month annual, CRM field sync, advanced controls)

**Official source:** https://fathom.ai/pricing

---

## Head-to-Head Gap Analysis

### AI Intelligence Pillar

| Dimension | MeetFlow | Notion AI | Granola | Fireflies | Otter | Fathom |
|-----------|----------|-----------|---------|-----------|-------|--------|
| Action item accuracy | 66% (34% wrong/missing), per `company.md` | Not publicly disclosed; structured with owner + priority + due date fields | Not publicly disclosed | Not publicly disclosed | Not publicly disclosed | Not publicly disclosed |
| Action item structure | Assignee detected, no due dates or priorities | Owner, priority, due date - pushed to task system | Extracted from transcript, no structured fields documented | Extracted, pushed as Salesforce Tasks | Detected as commitments, assigned next steps | Generated on Premium+ |
| User correction/feedback loop | Not documented in product files | Not documented officially | Not documented officially | Not documented officially | Not documented officially | Not documented officially |
| Pre-meeting briefing | None (per `product.md`) | None documented | Meeting Briefs (who, last discussion, open items) | None documented | Pre-call summary for sales (deal, contacts, last exchange) | None documented |
| Post-meeting AI chat | None (per `product.md`) | Enterprise Search across workspace + meetings | Agentic Chat across all meeting history with citations | AskFred per-meeting and cross-meeting | AI Chat across full history | Ask Fathom per-call and cross-call |
| Automated prompt templates / Skills | None (per `product.md`) | Meeting type-specific summaries (7 types) | Customizable note templates per meeting type | AI Skills: 50+ pre-built + custom, run on schedule | Custom AI workflows (Business+) | 15+ expert templates (BANT, Sandler, etc.) |
| Summary length control | Averaging 350 words/30-min meeting; "too long" - top 2 complaint, per `product.md` | Tailored by meeting type | User can ask AI to adjust tone, length, precision post-generation | Not documented | Not documented | Not documented |
| Meeting Pattern Insights | Weekly digest, 43% open rate, beta (800 users), per `product.md` | None documented | None documented | Conversation Intelligence: sentiment, topics, talk-time, filler words, coaching dashboard | None documented | None documented |
| Conversation Intelligence | None (per `product.md`) | None documented | None documented | Full suite: sentiment, topics, talk-time ratios, speaker analytics, team coaching | Real-time coaching during live calls (Sales Agent) | None documented |
| Real-time/live transcription | Not documented in product files as live-streaming feature | None (post-meeting only) | None (post-meeting only) | None (post-meeting only) | Live streaming transcript to all participants | None |
| Follow-up email drafting | In roadmap (Smart Follow-Up, April 2026) | Via Notion Agent automation | Via Agentic Chat ("draft follow-up") | Via AI Skills templates | Auto-drafts via Sales Agent | Via AI features (Premium+) |
| Bot-free recording | Not documented (uses bot-join per product files) | Bot-free (system audio) | Bot-free (system audio) | Uses bot (Fireflies joins meeting) | Uses bot (Otter joins meeting) | Uses bot |

### Integrations

| Dimension | MeetFlow | Notion AI | Granola | Fireflies | Otter | Fathom |
|-----------|----------|-----------|---------|-----------|-------|--------|
| Salesforce integration | In roadmap (May 2026, Dana's team), per `product.md` | Salesforce in Enterprise Search alpha | Not documented for Business tier | Full: Leads, Contacts, Opportunities, Tasks, resync | Pro+ plan | All paid tiers |
| HubSpot | Not documented | Not documented | Business tier | Yes | Pro+ | All paid tiers |
| Linear | GA, per `product.md` | Not documented | Not documented | Yes | Not documented | Not documented |
| Jira | GA, per `product.md` | Not documented | Not documented | Not documented | Not documented | Not documented |
| MCP | Not documented | Not documented | Yes (Feb 2025) | Not documented | Yes (recently shipped) | Yes |
| API | Not documented | Not documented | Business tier ($14) | Business tier ($19) | Enterprise only | All paid tiers |
| Integration count | Not documented | Limited to Notion ecosystem + connected tools | 6 documented integrations (Business) | 100+ | Selective (CRM, Zapier, Make) | CRM, Zapier, Make, MCP |

### Transcription and Platform

| Dimension | MeetFlow | Notion AI | Granola | Fireflies | Otter | Fathom |
|-----------|----------|-----------|---------|-----------|-------|--------|
| Transcription accuracy | 92% (quiet rooms), below 80% noisy, per `product.md` | Not publicly disclosed | Uses Deepgram and AssemblyAI (best-in-class providers, per official site) | Not publicly disclosed | Not publicly disclosed | Not publicly disclosed |
| Language support | Not documented | 19 languages | 10 languages | Multi-language (Business tier) | 6 languages | 28-language summary translation |
| Speaker diarization failure point | 8+ attendees, per `product.md` | Not documented | Not documented | Not documented | Not documented | Not documented |
| Summary generation speed | 45-90 seconds, per `product.md` | "Instantly after meeting ends" | "Rapid processing" documented | Not publicly disclosed | Not documented | "Delivered the moment call ends" |
| Platform coverage | Zoom, Google Meet, Teams | Zoom, Google Meet, Teams, in-person | Zoom, Google Meet, Teams, Webex, Slack, all platforms, phone | 7+ video platforms including Webex | Zoom, Google Meet, Teams | All major platforms |

### Pricing and Free Tier

| Dimension | MeetFlow | Notion AI | Granola | Fireflies | Otter | Fathom |
|-----------|----------|-----------|---------|-----------|-------|--------|
| Free tier | 12,000 free users, per `company.md` | Limited trial only; full AI on Business ($20) | Basic free (limited history) | Free forever (400 min/team, 20 AI credits) | Free (300 min/month) | Free forever (unlimited recording, limited AI) |
| Pro price | $15/seat/month | $20/seat/month (Business, all AI included) | $14/seat/month (unlimited history + integrations) | $10/seat/month (annual) | $8.33/seat/month (annual) | $16/seat/month (annual) |

---

## Prioritized Recommendations

### Recommendation 1 (TOP PICK): Add structured fields and a user-correction loop to action items - DO THIS FIRST

**Gap closed:** MeetFlow action items have no due date, priority field, or user-correction mechanism. Notion AI ships owner + priority + due date on every extracted action item and pushes them to Notion tasks automatically. The 66% accuracy rate (per `company.md`) makes the absence of correction loops doubly damaging: wrong items accumulate with no way for users to teach the model.

**Competitor pressure answered:** Notion AI's free-trial / Business plan offering. Pro users comparing tools will see Notion deliver structured, linked action items while MeetFlow delivers plain text at 66% accuracy.

**MeetFlow metric moved:** Pro churn (4.1% monthly, per `company.md`). Action item accuracy is cited as the top complaint driving churn (per `company.md`). Structured fields + correction loops attack both the output quality problem and the trust erosion problem simultaneously.

**How to scope it:** Current sprint (Action Item Confidence Scoring v2) should add three things beyond what is planned: (1) due date and priority fields on each action item, (2) a confirm/dismiss/edit UI that captures corrections and feeds the retraining pipeline, and (3) a weekly digest showing users how many of their corrections were incorporated. The third item is a trust signal, not a feature.

**Effort:** M (due date/priority fields are UI work; the correction capture loop is the engineering lift; the retraining pipeline automation is separate but should be a follow-on S sprint).

**Recommendation: DO. This is the single highest-leverage move available. It defends Pro retention, feeds the model retraining pipeline, and positions Smart Follow-Up to ship on clean data.**

---

### Recommendation 2: Ship Meeting Briefs (pre-meeting context card) - DO

**Gap closed:** MeetFlow has no pre-meeting capability. Granola's Briefs feature (shipped 20-05-2025) surfaces who you are meeting, what was discussed last time, and open action items - in a single view before the meeting starts. Otter's Sales Agent does the same for sales calls with deal value and CRM context. MeetFlow's Meeting Pattern Insights data (already collected in beta) contains exactly the raw material needed: past meeting transcripts, action items, recurring attendees.

**Competitor pressure answered:** Granola. The prosumer power users MeetFlow needs on Pro are exactly the users adopting Granola. A pre-meeting brief is a daily active touchpoint that competitors are capturing before MeetFlow enters the conversation.

**MeetFlow metric moved:** Free-to-Pro conversion (6.2%, per `company.md`). A pre-meeting brief is a high-visibility, low-latency feature that is easy to demo and easy to feel value from in the first week. It gives free users a concrete reason to upgrade (brief history requires past meetings to be stored, which gates on Pro).

**Effort:** S-M. The data is already captured in Meeting Pattern Insights beta. The brief generation is a prompt over existing transcript data, scoped per meeting attendee list pulled from calendar. The calendar integration work is largely already done (per `product.md`).

**Recommendation: DO. Ship this before or alongside Smart Follow-Up in April. It is a fast-to-build, high-conversion-signal feature that directly competes with Granola's stickiest differentiator.**

---

### Recommendation 3: Add cross-meeting AI chat - DO (Q3 2026)

**Gap closed:** Every major competitor (Granola, Fireflies, Otter, Fathom, Notion AI) now has a post-meeting AI chat or assistant. MeetFlow has full-text search but no conversational interface over meeting history. The gap is widening: Granola rebuilt its chat as agentic in April 2025; Notion AI added Enterprise Search; Otter added cross-meeting AI Chat; Fathom has account-wide Ask Fathom. MeetFlow users who want to ask "what did we decide on the pricing model across the last three product meetings?" have no path to an answer.

**Competitor pressure answered:** Granola (prosumer), Fathom (individual users), Notion AI (workspace users).

**MeetFlow metric moved:** NPS (34, per `product-vision.md`) and Pro retention. Power users in the Meeting Pattern Insights beta (800 users, 43% open rate) are already the most engaged segment - AI chat gives them a reason to stay in MeetFlow instead of exporting to Notion or Granola for the "ask questions across meetings" workflow.

**Effort:** M-L. Requires a vector search or RAG implementation over the existing transcript corpus, a chat UI, and citation/sourcing logic. Fathom and Granola have shipped this with inline citations - that citation layer is table stakes, not optional.

**Recommendation: DO, but not before Recommendation 1 and 2. Target Q3 2026. Do not build this on top of a weak action item model - the chat will surface the same errors at higher velocity.**

---

### Recommendation 4: Build AI Skills / meeting templates - DO (with Recommendation 1)

**Gap closed:** Fireflies AI Skills, Fathom's 15+ meeting templates, and Granola's customizable templates all let users define what kind of output they want per meeting type. MeetFlow produces a single 350-word summary that users find "too long" (top 2 complaint, per `product.md`). Templates let the AI know whether a meeting is a 1:1, a sales call, a customer discovery session, or a sprint planning - and adjust the summary structure accordingly.

**Competitor pressure answered:** Fireflies (sales teams), Fathom (individuals), Granola (prosumer), Notion AI (meeting-type-specific summaries).

**MeetFlow metric moved:** Summary quality complaint reduction, which feeds NPS (34, per `product-vision.md`). The "too long" complaint is solved by meeting-type-aware summaries, not by truncation.

**Effort:** S-M. Start with 5-7 pre-built templates (1:1, team sync, client call, sales call, interview, retrospective, brainstorm) and a custom template field. The prompt engineering layer is the main work; no new infrastructure needed.

**Recommendation: DO, bundled into the current action item sprint or as a fast follow-on. This is the highest-effort-to-value ratio item on the list because it directly addresses the 2 complaint while differentiating from Otter (which has no template system at the Pro tier).**

---

### Recommendation 5: Accelerate Salesforce integration depth - DO (already planned, raise the scope)

**Gap closed:** Fireflies syncs transcripts, summaries, and action items to Salesforce as Tasks under Leads, Contacts, and Opportunities. It also allows resync of historical meetings and configurable auto-create vs. log-only behavior. Otter syncs meeting data to Salesforce on Pro ($8.33). MeetFlow's Salesforce integration is in roadmap for May 2026 (per `product.md`). The risk is shipping a surface-level sync while Fireflies has a two-year head start in depth.

**Competitor pressure answered:** Fireflies. This is directly cited as the 1 reason sales-heavy teams consider switching (per `competitive.md`).

**MeetFlow metric moved:** Team plan seats (200 current, per `company.md`) and enterprise pipeline. The Salesforce integration is a team/enterprise feature, not an individual Pro feature. It is the unlock for the enterprise motion that Tomás is building.

**Effort:** L. The integration itself is Dana's team's work (May 2026 target). The recommendation here is not to scope-creep Dana's sprint but to ensure the v1 ships Task creation (not just note-logging) and supports configurable object mapping (Leads vs. Contacts vs. Opportunities), matching Fireflies' minimum viable depth. A log-only v1 is insufficient against a competitor with two years of production CRM workflow maturity.

**Recommendation: DO, and push for Task creation in v1 scope. A summary dump to Salesforce is not enough to win deals against Fireflies. Configurable object mapping and Task sync are the table-stakes features sales teams evaluate.**

---

### Recommendation 6: Add sentiment and topic tracking to Meeting Pattern Insights - WATCH (Q3 2026)

**Gap closed:** Fireflies Conversation Intelligence tracks sentiment per meeting, topic frequency across all meetings, talk-time ratios, filler words, and questions asked per speaker. It also provides a team coaching dashboard. MeetFlow's Meeting Pattern Insights beta tracks meeting load, talk-time ratios, and recurring topics (per `product.md`) but has no sentiment signal and no cross-team performance layer.

**Competitor pressure answered:** Fireflies (primarily enterprise and sales teams).

**MeetFlow metric moved:** Team plan expansion and enterprise readiness. Sentiment and topic tracking are enterprise and manager-persona features, not individual Pro features.

**Effort:** M. Sentiment classification on transcripts is a well-solved NLP problem. The lift is in the UI - surfacing it meaningfully in the weekly digest without making it feel like surveillance.

**Recommendation: WATCH for now. Meeting Pattern Insights is in beta with 800 users and 43% open rate (per `product.md`). Validate that this segment wants sentiment data before building it. Run a survey with the beta users. If 30%+ say they want cross-meeting sentiment, build it in Q3. Do not build it before AI chat (Recommendation 3) - the chat interface is the higher-priority engagement vector.**

---

### Recommendation 7: Bot-free recording - DO NOT (now)

**Gap closed:** Granola and Notion AI both capture meetings without sending a bot into the call. Bots are a friction point for some users (participants see "Granola is recording" type notifications; some orgs block bots).

**Competitor pressure answered:** Granola, Notion AI.

**MeetFlow metric moved:** Potentially onboarding friction reduction and free-to-Pro conversion.

**Effort:** L. System audio capture requires a native desktop app with OS-level audio permissions, which is a significant architectural shift from a cloud bot model. Mac, Windows, and Linux each require separate implementations.

**Recommendation: DO NOT build this in 2026. The architectural cost is high, the bot model works for 80% of use cases, and MeetFlow does not have the cross-platform desktop app footprint to make it viable. Monitor bot-blocking adoption rates in enterprise prospects. If enterprise pilots flag bot-blocking as a deal-killer, re-evaluate for 2027.**

---

### Recommendation 8: Real-time live transcription streaming - WATCH

**Gap closed:** Otter streams live transcription to all meeting participants in real time. MeetFlow (and most competitors) process post-meeting. Real-time streaming enables use cases like live note-sharing, in-meeting AI chat, and accessibility.

**Competitor pressure answered:** Otter (brand leader in this capability).

**MeetFlow metric moved:** Potentially transcription accuracy perception (users trust what they can see in real time) and onboarding for accessibility use cases.

**Effort:** L. Real-time streaming at scale requires significant infrastructure investment in streaming transcription pipelines.

**Recommendation: WATCH. This is Otter's primary technical differentiation. It matters most for accessibility use cases and for live note-sharing in large meetings. MeetFlow's 45-90 second post-meeting summary latency (per `product.md`) is already a complaint - fixing that latency first (getting to sub-10 seconds) may be a better use of engineering effort than full live streaming. Reassess after Transcript Accuracy v2 ships in June 2026.**

---

## Consolidated Gap Summary

| Competitor feature | MeetFlow gap | Severity | Tied to | Recommendation |
|---|---|---|---|---|
| Structured action items (owner, priority, due date) | None - plain text only | Critical | 66% accuracy, 4.1% churn | DO - Rec 1 |
| User correction feedback loop | None | Critical | 66% accuracy, model retraining bottleneck | DO - Rec 1 |
| Pre-meeting briefing (Granola Briefs, Otter pre-call) | None | High | 6.2% conversion, Granola threat | DO - Rec 2 |
| Cross-meeting AI chat | Full-text search only | High | NPS 34, Pro retention | DO - Rec 3 (Q3) |
| Meeting type templates / AI Skills | Single 350-word summary | High | Top 2 complaint ("too long") | DO - Rec 4 |
| Salesforce Task creation depth | Roadmap May 2026 | High | Team seats, enterprise pipeline, Fireflies threat | DO - Rec 5 |
| Sentiment and topic analytics | Basic topic tracking in beta | Medium | Team plan, enterprise | WATCH - Rec 6 |
| Bot-free recording | Bot model only | Low-Medium | Onboarding friction | DO NOT - Rec 7 |
| Live transcription streaming | Post-meeting only | Low | Otter differentiation | WATCH - Rec 8 |

---

## Sources (Validated Official Sources Only)

- Notion AI Meeting Notes: [https://www.notion.com/product/ai-meeting-notes](https://www.notion.com/product/ai-meeting-notes)
- Notion Release 2.51 (13-05-2025): [https://www.notion.com/releases/2025-05-13](https://www.notion.com/releases/2025-05-13)
- Notion Pricing: [https://www.notion.com/pricing](https://www.notion.com/pricing)
- Granola Homepage: [https://www.granola.ai](https://www.granola.ai)
- Granola Pricing: [https://www.granola.ai/pricing](https://www.granola.ai/pricing)
- Granola Product Updates: [https://www.granola.ai/updates](https://www.granola.ai/updates)
- Fireflies Pricing: [https://fireflies.ai/pricing](https://fireflies.ai/pricing)
- Fireflies Conversation Intelligence: [https://fireflies.ai/conversation-intelligence](https://fireflies.ai/conversation-intelligence)
- Fireflies Salesforce Integration: [https://fireflies.ai/integrations/crm/salesforce](https://fireflies.ai/integrations/crm/salesforce)
- Fireflies AI Skills: [https://fireflies.ai/skills](https://fireflies.ai/skills)
- Fireflies Integrations: [https://fireflies.ai/integrations](https://fireflies.ai/integrations)
- Otter.ai Pricing: [https://otter.ai/pricing](https://otter.ai/pricing)
- Otter.ai Features: [https://otter.ai/features](https://otter.ai/features)
- Otter.ai Sales Agent: [https://otter.ai/sales-agent](https://otter.ai/sales-agent)
- Fathom Pricing: [https://fathom.ai/pricing](https://fathom.ai/pricing)

**Internal sources:**
- `03-product-knowledge/company.md` (ARR, user counts, churn rate, action item accuracy, key risks)
- `03-product-knowledge/product.md` (feature status, sprint scope, summary latency, diarization limits)
- `03-product-knowledge/competitive.md` (threat levels, competitive positioning)
- `04-strategy/product-vision.md` (metrics baselines, roadmap bets, gaps)
