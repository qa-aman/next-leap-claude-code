# Action Items Board: project rules

`SPEC.md` is the source of truth. Read the relevant section before changing anything.

## Scope
- Build only what `SPEC.md` describes. **Ask Aman before adding anything he did not ask for**, including features, screens, settings and sections.
- Anything listed in SPEC §3 "Out of scope" is off-limits unless Aman says otherwise.
- If the code and the spec disagree, or the spec is unclear, stop and ask. Don't pick an answer silently.

## Working in phases
- Work one phase at a time, in the order in SPEC §12.
- A phase is done only when its **How we check it** passes. Show Aman the command output or screenshots, then wait for his OK before starting the next phase.
- Never report something as working without running its check. If a check fails, say so and show the output.

## Rules that must not be broken
- **Never guess an owner or a due date.** When unsure, leave it blank and add a flag (SPEC §5).
- Due dates are calculated in code from the meeting date (SPEC §5.3), never by Claude.
- Owners must be roster members. The server rejects anything else.
- Permissions are enforced on the server (SPEC §8). Every change to an item is written to the history.
- All dates and times are IST.
- Raw notes are deleted after 30 days. Don't copy them anywhere else, including logs.

## Claude API
- Model: `claude-sonnet-5`. Don't change it without asking; the budget is a hard cap under $20 a month.
- Every extraction run logs its token usage and cost.

## Secrets
- API keys and passwords live in environment variables only (SPEC §10). Never commit them or print them.

## Talking to Aman
- Aman is not a developer. Use plain language, and give exact click-by-click steps for anything he has to do himself (accounts, settings, deploys).
