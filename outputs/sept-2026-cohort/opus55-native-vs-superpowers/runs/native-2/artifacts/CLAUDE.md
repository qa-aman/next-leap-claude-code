# CLAUDE.md

Internal web app: paste meeting notes, extract action items with owner and due date, review, publish to one shared board. Built for one 8-person team.

## Source of truth
- `SPEC.md` is the source of truth. If the code, a request, or your own idea conflicts with it, stop and ask.
- **Ask Aman before adding anything SPEC.md doesn't call for**: features, screens, fields, settings, or statuses. `SPEC.md` §17 lists what we are not building.

## How we build
- Build in the phase order in `SPEC.md` §18. A phase is done only when its "How we check it" passes. Report the actual result, including failures.
- **After each phase, stop and wait for Aman's OK before starting the next one.**
- Automated tests never call the real Claude API; they use recorded responses. Only `npm run eval` calls the real API, and it costs money. Don't run it without asking.
- Commands (created in Phase 1): `npm test`, `npm run test:phase1` … `test:phase5`, `npm run test:duplicates`, `npm run eval`.

## Product rules that must never break
- **Flag, never guess.** Owners must exactly match a roster name or alias; anything else is flagged "Needs review".
- The model never picks the owner. It reports owner mentions as written; code does the roster matching (`SPEC.md` §6.4).
- Never invent a due date. No date mentioned means blank; vague phrases keep their wording with no date (§6.5).
- All dates, "today" and "overdue" use IST (Asia/Kolkata).
- Only active roster members can sign in, checked on every request.
- Meeting notes are confidential: never log them or send them anywhere except the Anthropic API. Raw notes are deleted after 30 days.
- The GitHub repository must be private; it contains confidential meeting notes (the eval set).
- Model name comes from `EXTRACTION_MODEL`; never hard-code it. Secrets live only in Cloudflare secrets.

## Stack
Cloudflare Workers + D1 + Workflows + Cron Triggers, TypeScript, official Anthropic TypeScript SDK. Keep running costs under $20/month in total. Choose nothing that needs an engineer to operate it.

## Working with Aman
Aman owns the project and is not technical. Explain decisions and results in plain language. When he needs to do something (click something in a dashboard, add a secret), give exact step-by-step instructions.
