# Competitive Scan — 23-05-2026

Refresh of `03-product-knowledge/competitive.md`. Each cell below is sourced from live competitor sites or first-party announcements. "Last 90 days" = launches dated **23-02-2026 to 23-05-2026**. All cited URLs validated 200 OK on 23-05-2026.

---

## Matrix

| | **Otter.ai** | **Fireflies.ai** | **Granola** | **Notion AI** |
|---|---|---|---|---|
| **Free tier** | 300 min/month per user, 30-min max meeting, 1 concurrent meeting, 3 lifetime file imports [1] | $0 forever. Unlimited transcription, 800 min storage/seat, limited AI summaries, limited AskFred access [3] | Limited meeting-note history, AI chat across meetings, shared folders, templates, multi-language [5] | Free Notion plan exists, but AI Meeting Notes requires Business ($20/user/mo) or Enterprise — not in Free or Plus [7][8] |
| **Paid entry tier** | Pro $16.99/user/mo monthly ($8.33/user/mo annual). 1,200 min/mo, 90-min max meeting, Salesforce/HubSpot/Zapier [1] | Pro $18/seat/mo monthly ($10/seat annual). Unlimited summaries, 8,000 min storage/seat, action items, 20 AI credits [3] | Business $14/user/mo. Unlimited notes, advanced AI models, Notion/Slack/HubSpot/Zapier integrations, API + MCP [5] | Plus $10/member/mo (no AI Meeting Notes); Business $20/member/mo unlocks AI Meeting Notes [7][8] |
| **Mid tier** | Business $30/user/mo monthly ($19.99/user annual). Unlimited transcription, 4-hr max meeting, admin features [1] | Business $29/seat/mo monthly ($19/seat annual). Unlimited storage, video recording, conversation intelligence, 30 AI credits [3] | — (no mid tier) | Business $20/member/mo (also entry into AI Meeting Notes) [7] |
| **Enterprise** | Custom pricing. SSO/SCIM, HIPAA add-on, API/Webhooks, video replay [1] | $39/seat/mo annual. SSO, SCIM, HIPAA, private storage, custom retention, 50 AI credits [3] | $35/user/mo. SSO, admin controls, priority support, org-wide auto-deletion, opt-out from model training [5] | Custom pricing. Zero data retention from AI subprocessors; AI Meeting Notes included [6][7] |
| **Top homepage differentiator #1** | "Your AI notetaker is now also your Conversational Knowledge Engine" — transcription + AI chat across meeting history [2] | "95% accurate" transcription, "the industry leader in transcription accuracy" [4] | "Granola transcribes your computer's audio directly, with no meeting bots joining your call" [9] | Custom Agents that "build, edit, and take action" across the workspace 24/7 [6] |
| **Top differentiator #2** | "4+ hours saved per week" via automated transcription and summaries [2] | "Detailed notes, action items, and customized summaries instantly after every meeting" [4] | AI-enhanced notes — raw notes you write get automatically enhanced post-meeting [9] | Enterprise Search across Slack, Google Drive, GitHub, etc. "in seconds" [6] |
| **Top differentiator #3** | Bot-free capture: desktop app, mobile, Chrome extension, or invite — no bots required to join the call [2] | Enterprise security: SOC 2 Type II, GDPR, HIPAA, Zero Data Retention [4] | One-click share to Slack, email, CRM, Notion, ATS [9] | Zero Data Retention for Enterprise; contractual ban on AI subprocessors using customer data for training [6] |
| **Launches in last 90 days (23-02-2026 to 23-05-2026)** | **28-04-2026:** Conversational Knowledge Engine GA, AI Chat Connectors (Gmail, Drive, Notion, Jira, Salesforce as MCP client), MCP Server for Claude/ChatGPT, redesigned AI Chat, Otter for Desktop on Mac + Windows [10][11] | **Q1-Q2 2026:** Live Assist (real-time in-meeting suggestions, marked NEW on homepage), Desktop App, "Talk to Fireflies" web search powered by Perplexity, Fireflies MCP Server for Claude/Devin/ChatGPT [4][12] | **25-03-2026:** $125M Series C at $1.5B valuation. Launched Spaces (team folders with access controls + folder-level querying), agentic Granola Chat with inline citations and Recipes [13][14]. **Feb 2026:** MCP server + personal/enterprise APIs for note context [14] | **13-05-2026:** AI Meeting Notes GA in Notion 2.51 (system audio + mic capture for Zoom/Meet/Teams, transcript-linked summaries, action items) [15]. **18-03-2026:** Custom instructions for AI Meeting Notes summaries [16] |

---

## Threat read for MeetFlow

Three of the four competitors shipped MCP servers in the last 90 days (Otter, Fireflies, Granola). Becoming an "AI tool that other AI tools can read from" is now table stakes — MeetFlow does not have this on the roadmap per `04-strategy/product-vision.md`.

Otter's 28-04-2026 launch is the biggest shift in posture. They moved from "notetaker" to "Conversational Knowledge Engine" with Salesforce + Jira + Notion connectors. That collapses the differentiation gap MeetFlow was banking on for the Salesforce integration shipping May 2026 (per company.md priorities).

Notion AI Meeting Notes went GA on 13-05-2026 — exactly the existential threat called out in competitive.md line 49. The feature is now available, not theoretical. Priya-type casual users in Notion-heavy teams have a working alternative today.

Granola raised $125M at $1.5B on 25-03-2026 and launched Spaces. The "no team features" gap from competitive.md line 33 is now closed. Their Pro-tier threat to MeetFlow is materially worse than the original landscape doc describes.

---

## Sources

1. [Otter.ai Pricing](https://otter.ai/pricing) — verified 23-05-2026
2. [Otter.ai homepage](https://otter.ai) — verified 23-05-2026
3. [Fireflies.ai Pricing](https://fireflies.ai/pricing) — verified 23-05-2026
4. [Fireflies.ai homepage](https://fireflies.ai) — verified 23-05-2026
5. [Granola Pricing](https://www.granola.ai/pricing) — verified 23-05-2026
6. [Notion AI product page](https://www.notion.com/product/ai) — verified 23-05-2026
7. [Notion Pricing](https://www.notion.com/pricing) — verified 23-05-2026
8. [Notion AI Meeting Notes help center](https://www.notion.com/help/ai-meeting-notes) — verified 23-05-2026
9. [Granola homepage](https://www.granola.ai) — verified 23-05-2026
10. [Otter.ai blog: Conversational Knowledge Engine](https://otter.ai/blog/otter-ai-evolves-from-ai-notetaker-to-create-100b-enterprise-conversational-knowledge-engine-market) — verified 23-05-2026
11. [TechCrunch: Otter's new feature lets users search across their enterprise tools (28-04-2026)](https://techcrunch.com/2026/04/28/otters-new-feature-lets-users-search-across-their-enterprise-tools/) — verified 23-05-2026
12. [Fireflies.ai Pricing (Live Assist + Desktop App listed)](https://fireflies.ai/pricing) — verified 23-05-2026
13. [TechCrunch: Granola raises $125M at $1.5B (25-03-2026)](https://techcrunch.com/2026/03/25/granola-raises-125m-hits-1-5b-valuation-as-it-expands-from-meeting-notetaker-to-enterprise-ai-app/) — verified 23-05-2026
14. [Granola Updates / changelog](https://www.granola.ai/updates) — verified 23-05-2026
15. [Notion AI Meeting Notes product page](https://www.notion.com/product/ai-meeting-notes) — verified 23-05-2026
16. [Notion release notes: Custom instructions for AI Meeting Notes (18-03-2026)](https://www.notion.com/releases/2026-03-18) — verified 23-05-2026
