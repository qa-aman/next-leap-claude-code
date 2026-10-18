# Job Search Agent: a managed agent team on Claude Platform

Built 18-10-2026 for the Oct 2026 cohort, Session 3 (Subagents and Managed Agents).

## What it does

Every weekday at 08:00 IST it checks your company watchlist. It scores each open role against your resume. It writes a shortlist and drafts for the top 3. It remembers what it already showed you.

It never applies, emails or submits anything. You decide.

## The team

```
                 job-search-lead  (Sonnet, manager)
                 reads memory, delegates, checks, writes shortlist.md
                /                |                     \
   job-scout x5 (Haiku)     fit-scorer (Sonnet)     application-writer x3 (Sonnet)
   one per company,         scores 0-10 with        resume bullets + note,
   web_fetch to 3 hosts     resume evidence         no internet
```

| Agent | Job | Tools it gets | Why this shape |
|---|---|---|---|
| job-search-lead | Plans, delegates, checks, writes the shortlist | read, write, edit, glob | A manager that cannot fetch or score, so it must delegate |
| job-scout | Fetches one board, filters by profile | web_fetch, read, write | Cheap model, 5 copies run at once (parallel work) |
| fit-scorer | Scores fit with a quote from the resume | read, glob, write | No internet, so it judges only what is on the page |
| application-writer | 3 bullets + a 120-word note per role | read, write | No internet, and banned from inventing facts |

## What a managed agent needs (the 4 parts, from the official overview)

| Part | In this folder | What it is |
|---|---|---|
| Agent | `agents/*.md` | Model, system prompt, tools. Created once, used by ID |
| Environment | `environment.yaml` | The cloud sandbox. Network limited to 3 job-board hosts |
| Session | `run.py` | One run: your files, the memory store, a $3 cap |
| Events | streamed by `run.py` | Every message and tool call, stored in the cloud |

Plus three extras this agent uses:
- **Multiagent block** (in the lead): lists the 3 workers by ID. Inline agents and workflows are off, so the lead can only use your 3 agents.
- **Memory store** (`memory_store.yaml`): `seen-jobs.md` and `feedback.md` persist between runs. Every write is versioned.
- **Scheduled deployment** (`deployment.md.tmpl`): the daily 08:00 IST run, with no laptop needed.

## Subagent vs managed agent, for this job

| | Claude Code subagent | Managed agent |
|---|---|---|
| Runs on | Your laptop | Anthropic's cloud sandbox |
| Daily at 08:00 | Only if your laptop is on | Yes, scheduled deployment |
| Remembers seen jobs | `memory:` in frontmatter, local files | Memory store, versioned |
| Paid from | Claude plan | API usage, capped by session budget |

## Run it

```bash
brew install anthropics/tap/ant      # the ant CLI
pip install anthropic
export ANTHROPIC_API_KEY=sk-ant-...  # from platform.claude.com/settings/keys

# 1. Edit inputs/profile.md and paste your resume into inputs/resume.md
# 2. Create everything once
./setup.sh
# 3. Run once and watch it
python run.py
```

**You should see:** five `[new thread]` lines as the scouts start together. Then the scorer, then three writers. At the end, `results/<session-id>/shortlist.md` and three application files.

Open the session in the Console to see each agent's own thread.

**Make it daily:** fill the IDs in `deployment.md.tmpl` (the agent, environment and store IDs are in `claude-lock.json`, the file IDs are printed by the uploads), save it as `deployment.md`, then `ant apply deployment.md`.

## Teach it

After a run, tell it what was wrong. Add a line to `feedback.md` in the memory store, in the Console: "Skip fintech." "Only Bengaluru." The next run reads it before it picks the top 3. That is the learning loop.

## Where it breaks (show this live)

1. **The scout that roams.** Delete `allowed_hosts` from `environment.yaml`. Ask for "PM jobs at Google". The scout now tries any site. Put it back: it can only reach the 3 boards, and it reports the failure.
2. **The writer that invents.** Remove the "Use only facts" rule. Run with a thin resume. It writes a metric you never had. Put it back: it writes "(add a number)".
3. **The wrong budget.** `"amount": "3"` means 3 cents, not $3. The session pauses at once. Budgets are whole US cents, as a string.

## Cost and safety

- Each run is capped at $3 (`"300"` cents). The cap applies to each run on its own, not to all runs together.
- Your resume goes to Anthropic's cloud. Managed Agents is not covered by Zero Data Retention. Delete sessions and files when done.
- Job boards: only public JSON APIs. LinkedIn and Naukri are not in the watchlist; scraping them breaks their terms.

## References

- Managed Agents overview: https://platform.claude.com/docs/en/managed-agents/overview
- Quickstart: https://platform.claude.com/docs/en/managed-agents/quickstart
- Multiagent orchestration: https://platform.claude.com/docs/en/managed-agents/multiagent-orchestration
- Tools: https://platform.claude.com/docs/en/managed-agents/tools
- Memory stores: https://platform.claude.com/docs/en/managed-agents/memory
- Scheduled deployments: https://platform.claude.com/docs/en/managed-agents/scheduled-deployments
- Session budgets: https://platform.claude.com/docs/en/managed-agents/budgets
- Claude Code subagents: https://code.claude.com/docs/en/sub-agents
