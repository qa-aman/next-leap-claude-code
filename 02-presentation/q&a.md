# Q&A - Claude Code Workshop

Answers to open questions from workshop sessions, sourced from official Anthropic documentation.

**Date context** (important - Claude Code evolves; answers below may drift over time):

- **Original file created:** 23-03-2026 (March 2026 cohort - Q1 to Q4 below)
- **Last full refresh:** 16-05-2026 (URLs re-verified, Windows flow rewritten)
- **May 2026 Session 1 additions:** 16-05-2026 (Q5-Q13 - see "May 2026 - Session 1 Additions" section)
- **May 2026 Session 2 additions:** 16-05-2026 (Q14-Q31 - see "May 2026 - Session 2 Additions" section)
- **May 2026 Session 3 additions:** 17-05-2026 (Q32-Q45 - see "May 2026 - Session 3 Additions" section)
- **May 2026 Session 4 additions:** 18-05-2026 (Q46-Q56 - see "May 2026 - Session 4 Additions" section)
- **May 2026 Session 5 additions:** 23-05-2026 (Q57-Q70 - see "May 2026 - Session 5 Additions" section)
- **May 2026 Session 6 additions:** 23-05-2026 (Q71-Q76 - Multi-agent architectures, afternoon - see "May 2026 - Session 6 Additions" section)
- **May 2026 Session 7 additions:** 24-05-2026 (Q77-Q83 - Build Hours, Property Finder build - see "May 2026 - Session 7 Additions" section)
- **July 2026 Session 1 additions:** 04-07-2026 (Q84-Q89 - new cohort, Claude Code Setup - see "July 2026 - Session 1 Additions" section)
- **July 2026 Session 2 additions:** 04-07-2026 (Q90-Q95 - Skills, Plugins, and Practical Examples - see "July 2026 - Session 2 Additions" section)
- **July 2026 Session 3 additions:** 05-07-2026 (Q96-Q105 - Skills Creation and PM Frameworks - see "July 2026 - Session 3 Additions" section)
- **July 2026 Session 4 additions:** 05-07-2026 (Q106-Q116 - Building and Using Agents - see "July 2026 - Session 4 Additions" section)
- **July 2026 Session 5 additions:** 11-07-2026 (Q117-Q129 - Workflows, Routines, and Product Automation - see "July 2026 - Session 5 Additions" section)
- **July 2026 Session 6 additions:** 11-07-2026 (Q130-Q141 - Video, Commands, Hooks, and Session Management - see "July 2026 - Session 6 Additions" section)
- **July 2026 Session 7 additions:** 12-07-2026 (Q142-Q153 - Build Hours, Shopping Assistant MVP - see "July 2026 - Session 7 Additions" section)
- **July 2026 Session 8 additions:** 12-07-2026 (Q154-Q167 - Build Hours Part 2, Phase 2 login sessions and product matching - see "July 2026 - Session 8 Additions" section)

If you are reading this after mid-2026, re-verify every URL and command before relying on the answers - product behavior, plan limits, UI labels, and command flags change.

---

## Q1: Is my data safe? What about PII?

**Short answer:** For consumer plans (Free, Pro, Max), model training uses your data only if you opt in. For Team and Enterprise (commercial) plans, your data is not used for training by default.

**Training opt-in/opt-out by plan:**

- **Consumer plans (Free, Pro, Max):** Claude Code uses your chats and coding sessions to improve models only if you choose to allow it in your Privacy Settings. This is opt-in. You can change this at any time at https://claude.ai/settings/privacy.
- **Commercial plans (Team, Enterprise, API):** By default, Anthropic does not use your inputs or outputs for model training. Data may be used only if you explicitly opt in (for example, by submitting feedback).
- **Incognito chats:** Never used for training, even if you have model improvement enabled.

**Data retention:**

- When you submit thumbs up/down feedback, Anthropic stores the related conversation for up to 5 years in secured backend systems. This applies to both consumer and commercial plans. The data is de-linked from your user and customer identifiers before any training use.
- Raw content from connectors (Google Drive, MCP servers) is excluded from training unless directly copied into conversations.

**What Claude Code sends to Anthropic servers:**

- Your conversation messages and tool call results (file contents, command outputs) are sent to Anthropic's API for processing.
- Claude Code does not send your entire codebase - only the files and outputs relevant to the current conversation.

**Security safeguards built into Claude Code:**

- **Permission-based architecture:** Claude Code uses strict read-only permissions by default. File edits, bash commands, and other write actions require explicit approval. Users control whether to approve actions once or allow them automatically.
- **Write access restriction:** Claude Code can only write to the folder where it was started and its subfolders. It cannot modify files in parent directories without explicit permission. Read access outside the working directory (for example, system libraries) is permitted.
- **Network request approval:** Tools that make network requests require user approval by default.
- **Secure credential storage:** API keys and tokens are encrypted. On macOS, credentials are stored in the encrypted macOS Keychain. On Linux, credentials are stored in `~/.claude/.credentials.json` with file mode `0600`. On Windows, credentials are stored in `%USERPROFILE%\.claude\.credentials.json` with user-profile access controls.
- **Anthropic holds SOC 2 Type 2 and ISO 27001 certifications.** See https://trust.anthropic.com for the report and certificate. The security page at https://code.claude.com/docs/en/security links there directly.

**Bottom line for PII:** If your organization handles sensitive PII, use the Team or Enterprise plan where data is not used for training by default. Disable model improvement in Privacy Settings if on a consumer plan. Always review what Claude Code reads and sends before approving tool calls.

**Sources:**
- https://privacy.claude.com/en/articles/10023580-is-my-data-used-for-model-training (consumer products - verified 16-05-2026)
- https://privacy.claude.com/en/articles/7996868-is-my-data-used-for-model-training (commercial products - verified 16-05-2026)
- https://code.claude.com/docs/en/security (verified 16-05-2026)
- https://code.claude.com/docs/en/permissions (verified 16-05-2026)
- https://code.claude.com/docs/en/authentication#credential-management (verified 16-05-2026)

---

## Q2: What plugins should a first-time Claude Code user install?

### How Claude Code extensions work

Claude Code has a lightweight extension model. There is no "app store" to browse. You extend Claude Code through three mechanisms: **bundled skills**, **custom skills**, and **MCP servers**. Separately, there are IDE extensions for VS Code-compatible editors and a JetBrains plugin.

---

### Bundled skills (ship with Claude Code, no setup needed)

These are available out of the box in every session. The commands reference at https://code.claude.com/docs/en/commands marks each with **[Skill]** in the purpose column.

| Skill | What it does |
|-------|-------------|
| `/batch <instruction>` | Orchestrate large-scale changes across a codebase in parallel. Researches the codebase, decomposes work into 5 to 30 independent units, and spawns one background subagent per unit in an isolated git worktree. Requires a git repository |
| `/claude-api [migrate]` | Load Claude API reference material for your project's language (Python, TypeScript, Java, Go, Ruby, C#, PHP, or cURL) and Managed Agents reference. Also activates automatically when your code imports `anthropic` or `@anthropic-ai/sdk`. Run `/claude-api migrate` to upgrade existing Claude API code to a newer model |
| `/debug [description]` | Enable debug logging for the current session and troubleshoot issues by reading the session debug log. Optionally describe the issue to focus the analysis |
| `/fewer-permission-prompts` | Scan your transcripts for common read-only Bash and MCP tool calls, then add a prioritized allowlist to project `.claude/settings.json` to reduce permission prompts |
| `/loop [interval] [prompt]` | Run a prompt repeatedly while the session stays open. Omit the interval and Claude self-paces. Example: `/loop 5m check if the deploy finished` |
| `/simplify [focus]` | Review recently changed files for code reuse, quality, and efficiency issues, then fix them. Spawns three review agents in parallel and aggregates their findings |

---

### Custom skills (create your own)

Skills are markdown files that teach Claude how to do specific tasks. Create a `SKILL.md` file in one of these locations:

| Location | Path | Applies to |
|----------|------|-----------|
| Personal | `~/.claude/skills/<skill-name>/SKILL.md` | All your projects |
| Project | `.claude/skills/<skill-name>/SKILL.md` | This project only |

A minimal skill file looks like this:

```yaml
---
name: my-skill
description: What this skill does and when to use it
---

Your instructions for Claude here...
```

The `description` field is the trigger mechanism. Claude uses it to decide when to load the skill automatically. Keep `SKILL.md` under 500 lines. Files in the legacy `.claude/commands/` directory continue to work and behave identically.

---

### MCP servers (connect external tools)

MCP (Model Context Protocol) lets Claude Code talk to external services. You configure them in your Claude Code settings. Common examples:

- **Slack** - search channels, send messages
- **Jira/Linear** - read and update tickets
- **Confluence** - read and push documentation
- **Playwright/Chrome DevTools** - browser automation and debugging
- **Figma** - read designs for implementation

To add an MCP server, use `/mcp` inside a Claude Code session or run `claude mcp add` from the terminal.

Note: MCP server security is the user's responsibility. Anthropic reviews connectors listed in the Anthropic Directory but does not security-audit third-party MCP servers.

---

### Plugins (install from a marketplace)

Claude Code has a plugin system for distributing bundled skills, MCP servers, and hooks together. In the IDE extension, type `/plugins` to open the plugin manager. From the CLI, use `claude plugin install <name>@<marketplace>`.

Plugins are community- and vendor-contributed. There is no single curated Anthropic list of "recommended" plugins. Common workflow plugins (like skills for code review, frontend design, or Chrome DevTools automation) are distributed via plugin marketplaces that individuals and organizations publish. Before installing any plugin, review what tools and permissions it requests.

---

### Recommended plugins

These are the plugins and MCP servers I install on every machine. They are community- or vendor-contributed, not part of the official Anthropic bundled list. Treat this as a starting point and review each one before installing.

| Plugin / MCP | What it does | Why I use it |
|---|---|---|
| **Superpower** | Handles brainstorming, architecture planning, and auto-invokes relevant skills based on context | The first one I install on a new machine. It orchestrates other skills automatically so you do not have to remember which to call |
| **Skill Creator** | Scaffolds new skills following Anthropic's skill architecture | Keeps custom skills structured and maintainable. Saves the back-and-forth of getting the SKILL.md frontmatter right |
| **Code Review** | Reviews code and flags critical issues | Catches bugs and gaps before they reach production |
| **Code Simplifier** | Improves code quality, reuse, and efficiency | Cleans up code after implementation |
| **Front End Design** | Auto-improves UI based on common design guidelines | Auto-invoked when you mention front-end work |
| **Chrome DevTools (MCP)** | Opens Chrome from within Claude Code to inspect UI, check fonts, click around | Lets Claude see and interact with your live app directly |
| **Playwright (MCP)** | Programmatic web UI testing | Useful when you want Claude to verify a flow end-to-end |
| **Figma (MCP)** | Connects Figma designs to Claude Code | For design-to-code workflows |

Before installing any of these, review the plugin or MCP server's repository for the tools and permissions it requests. Plugins are not security-audited by Anthropic.

---

### Recommended starter setup for PMs

If you are new to Claude Code and working as a PM, start with:

1. **No plugins needed on day one.** Bundled skills and built-in tools (file reading, search, git) cover most PM workflows out of the box.
2. **Add MCP servers as needed.** If you use Confluence, add the Confluence MCP. If you use Jira, add the Jira MCP. Only add what you actually use.
3. **Create project skills for repeated workflows.** If you find yourself giving Claude the same instructions repeatedly (for example, "write a PRD in this format"), turn those instructions into a skill.

---

### IDE extension (optional)

Antigravity IDE uses the VS Code extension marketplace, so the Claude Code VS Code extension works directly in it. The extension is also supported in Cursor, Windsurf, Kiro, and other VS Code forks.

To install:

- Open Extensions (`Cmd+Shift+X` on Mac, `Ctrl+Shift+X` on Windows)
- Search "Claude Code" and install the one by Anthropic
- Open Command Palette (`Cmd+Shift+P` / `Ctrl+Shift+P`), type "Claude Code", select "Open in New Tab"

This gives you inline diffs, @-mentions, plan review, conversation history, and multiple tab support inside your editor.

### JetBrains plugin (optional)

If you use IntelliJ IDEA, PyCharm, or WebStorm, install the Claude Code plugin from the JetBrains Marketplace.

**Sources:**
- https://code.claude.com/docs/en/skills (verified 16-05-2026)
- https://code.claude.com/docs/en/commands (verified 16-05-2026)
- https://code.claude.com/docs/en/mcp (verified 16-05-2026)
- https://code.claude.com/docs/en/vs-code (verified 16-05-2026)

---

## Q3: Why is terminal-based Claude Code more powerful than using it inside an IDE like Cursor?

**Follow-up from Sonar:** "If I pass architecture.md and todo.md to Cursor, won't that compensate?"

### 1. The CLI has the full tool and command set

The official docs confirm the VS Code extension (and by extension, the IDE extension in Antigravity, which uses the same extension marketplace) is a subset of the full CLI.

| Capability | Terminal CLI | IDE Extension |
|-----------|-------------|-------------------|
| Commands and skills | All | Subset (type `/` to see what's available) |
| MCP server config | Full (add, remove, configure via `claude mcp add`) | Partial (`/mcp` manages existing; add via CLI terminal) |
| Checkpoints and rewind | Yes | Yes |
| `!` bash shortcut | Yes | No |
| Tab completion | Yes | No |
| Non-interactive mode (`claude -p`) | Yes | No |
| Piping data in/out | Yes | No |

Note: Antigravity uses the VS Code extension marketplace, so it gets the same extension behavior described above. The terminal CLI you run inside Antigravity's integrated terminal gives you the full feature set.

### 2. The agentic loop is the real difference vs. Cursor

Claude Code is not a chatbot that answers questions and waits. It autonomously reads files, runs commands, makes changes, and works through problems. The workflow is: explore the codebase, plan the approach, implement across multiple files, then verify its own work (run tests, check output).

Cursor and similar IDE copilots work on a request-response basis within the editor. Passing `architecture.md` and `todo.md` gives Cursor static context, but it does not give it the ability to:

- Dynamically discover what files it needs and read them on demand
- Run shell commands (tests, linters, build tools) and react to results
- Search the entire codebase with grep/glob before deciding what to change
- Spawn subagents that investigate different parts of the codebase in parallel
- Chain multi-step workflows (explore, plan, implement, test, commit, PR)

### 3. CLI enables automation and scaling

Terminal-only capabilities that have no IDE equivalent:

- `claude -p "prompt"` for CI pipelines, pre-commit hooks, and scripts
- `cat error.log | claude -p "explain"` for piping data directly
- Fan-out across files: loop through hundreds of files with parallel Claude invocations
- `--output-format json` (or `stream-json`) for structured output in automated workflows
- `--allowedTools` to scope which tools execute without prompting, for batch operations
- `--max-turns` to limit agentic turns in scripted pipelines
- `--max-budget-usd` to cap API spending per invocation

### 4. Context management is more explicit in the terminal

The terminal gives direct, keyboard-driven control over context: `/clear` between tasks, `/compact` with custom focus instructions, `/rewind` to roll code and conversation back to a checkpoint (aliases: `/checkpoint`, `/undo`), `Esc` to stop mid-action. The IDE extension supports checkpoints and rewind too via a hover button on any message. The CLI's full command set and keyboard shortcuts make aggressive context management faster. This matters because context window performance degrades as it fills.

**Bottom line:** Passing context files to Cursor gives it information, but Claude Code's power comes from autonomous tool access and the agentic loop, not just from reading files. The terminal is where the full feature set lives.

**Sources:**
- https://code.claude.com/docs/en/vs-code (verified 16-05-2026)
- https://code.claude.com/docs/en/best-practices (verified 16-05-2026)
- https://code.claude.com/docs/en/cli-reference (verified 16-05-2026)
- https://code.claude.com/docs/en/commands (verified 16-05-2026)

---

## Q4: Installation issues following GitHub repo steps

A troubleshooting guide has been added to the setup files in this repo. If you are facing installation issues, check the troubleshooting section at the bottom of the relevant file:

- **Mac users:** `01-setup/mac-setup.md`
- **Windows users:** `01-setup/windows-setup.md`

Both files cover common issues including: command not found, subscription/authentication errors, Node version too old, permission errors, browser not opening on login, and platform-specific fixes.

For performance, stability, and search issues once Claude Code is running, the official troubleshooting page at https://code.claude.com/docs/en/troubleshooting covers high CPU/memory usage, auto-compact thrashing, and slow search on WSL. For install-specific failures (`command not found`, `EACCES`, OAuth errors), see https://code.claude.com/docs/en/troubleshoot-install.

Run `/doctor` inside Claude Code for an automated check of your installation, settings, MCP servers, and context usage. If `claude` won't start at all, run `claude doctor` from your shell instead.

---

## Quick reference

| Topic | Official docs |
|-------|--------------|
| Privacy: consumer plans (Free, Pro, Max) | https://privacy.claude.com/en/articles/10023580-is-my-data-used-for-model-training |
| Privacy: commercial plans (Team, Enterprise, API) | https://privacy.claude.com/en/articles/7996868-is-my-data-used-for-model-training |
| Security architecture | https://code.claude.com/docs/en/security |
| Permissions and write access | https://code.claude.com/docs/en/permissions |
| Credential management | https://code.claude.com/docs/en/authentication#credential-management |
| Skills and custom commands | https://code.claude.com/docs/en/skills |
| Commands reference (bundled skills listed here) | https://code.claude.com/docs/en/commands |
| MCP servers | https://code.claude.com/docs/en/mcp |
| VS Code / IDE extension | https://code.claude.com/docs/en/vs-code |
| CLI reference | https://code.claude.com/docs/en/cli-reference |
| Trust center (SOC 2, ISO 27001) | https://trust.anthropic.com |
| Troubleshooting (performance, stability) | https://code.claude.com/docs/en/troubleshooting |
| Troubleshooting (install and login) | https://code.claude.com/docs/en/troubleshoot-install |

---

# May 2026 - Session 1 Additions

New questions raised by the NextLeap Applied Generative AI Bootcamp cohort on 16-05-2026. All URLs verified 16-05-2026.

---

## Q5: CLAUDE.md vs README.md - what's the actual difference? Is CLAUDE.md a PRD?

**Short answer:** `CLAUDE.md` is for the agent. `README.md` is for humans. They overlap in content but serve different readers.

- **README.md** is project documentation for any human visiting the repo - install steps, contribution guide, license. Claude Code does not auto-load it.
- **CLAUDE.md** is auto-loaded into the agent's context at the start of every session. It tells Claude *how to behave* in this project - coding conventions, architecture rules, what to never do, where files live.

It is **not** a PRD. A PRD describes *what to build and why*. `CLAUDE.md` describes *how the agent should work inside this codebase*. Use it for: project structure, tech stack, commands to run, style rules, file conventions, things to avoid.

**Hierarchy** (all loaded automatically):

| Scope | Path | When loaded |
|-------|------|-------------|
| Enterprise / managed | OS-specific managed path | All sessions, all users on the machine |
| Global (user) | `~/.claude/CLAUDE.md` | All your projects |
| Project | `<repo>/CLAUDE.md` (committed) | Sessions started in that repo |
| Local project | `<repo>/CLAUDE.local.md` (gitignored) | Same as project, but personal/not committed |
| Subdirectory | `<repo>/<subdir>/CLAUDE.md` | When Claude reads files in that subdir |

**Sources:**
- https://code.claude.com/docs/en/memory (verified 16-05-2026)

---

## Q6: Where is the memory file stored? Is it the "guardrails" of the project?

**Short answer:** "Memory" in Claude Code = the `CLAUDE.md` files described in Q5, plus any auto-managed memory files the harness writes. They function as standing instructions, not hard guardrails.

- The agent **reads** them every session, so anything in there shapes future behavior.
- They are **not enforced** like permissions or hooks. A `CLAUDE.md` rule saying "never delete files" is a strong preference, not a hard block. For hard blocks, use `settings.json` permissions or hooks.
- Use `/memory` inside Claude Code to view and edit memory files quickly.
- Use the `#` shortcut at the start of a message to add a quick memory entry to the appropriate `CLAUDE.md`.

So: memory = soft guardrails (behavior). `settings.json` permissions and hooks = hard guardrails (enforcement).

**Sources:**
- https://code.claude.com/docs/en/memory (verified 16-05-2026)
- https://code.claude.com/docs/en/settings (verified 16-05-2026)

---

## Q7: If I set up the status line / global CLAUDE.md / skills on my personal laptop, will they carry over to my company laptop?

**Short answer:** No, not automatically. Global Claude Code config lives under `~/.claude/` on each machine. It does not sync across devices.

- `~/.claude/CLAUDE.md`, `~/.claude/settings.json`, `~/.claude/skills/`, and the status line config are all machine-local.
- There is no built-in cloud sync for Claude Code config. OAuth tokens, caches, and trust settings are intentionally tied to the machine.
- **What you can do:** keep your personal Claude Code config in a private git repo and clone it on each machine. Some users symlink files into `~/.claude/`. This works but drifts over time and is not officially supported beyond `.claude/rules/`.
- **Project-level config** (the repo's own `CLAUDE.md`, `.claude/skills/`, `.claude/settings.json`) *does* travel with the repo because it is committed to git.

**Bottom line:** commit project config to the repo. Treat global config as personal/per-machine.

**Sources:**
- https://code.claude.com/docs/en/settings (verified 16-05-2026)
- https://code.claude.com/docs/en/memory (verified 16-05-2026)

---

## Q8: When should I use plan mode vs default mode vs accept-edits vs auto (bypass) mode?

Cycle modes with `Shift+Tab`. The current mode is shown in the status line.

| Mode | What it does | Use when |
|------|-------------|----------|
| **Default** | Asks for approval on file edits, bash commands, and other write actions | Day-to-day work where you want to review each change |
| **Plan mode** | Read-only. Claude can explore the codebase, read files, and produce a written plan, but cannot edit, run write commands, or create files. You exit with `ExitPlanMode` to start work | Before any multi-file change, when you want a plan to approve before code is touched. Anthropic specifically recommends this for non-trivial tasks |
| **Accept edits** | Auto-approves file edits but still asks for bash, network, and other tool calls | When you trust the file changes Claude is making (e.g. mechanical refactor) but want a guardrail on shell commands |
| **Auto (bypass permissions)** | Skips most permission prompts. Highest risk | Sandboxed environments, throwaway containers, or CI - never on a machine with important uncommitted work |

Anthropic's best-practices doc explicitly recommends starting in plan mode for anything non-trivial.

**Sources:**
- https://code.claude.com/docs/en/best-practices (verified 16-05-2026)
- https://code.claude.com/docs/en/permissions (verified 16-05-2026)

---

## Q9: I installed Claude Code in my Mac terminal. Do I need to install it again inside the Antigravity / VS Code integrated terminal?

**Short answer:** No. Install once per machine.

The Antigravity / VS Code integrated terminal is the same shell environment as your system terminal - same PATH, same Node, same `claude` binary. If `claude --version` works in your system terminal, it works in the integrated terminal too.

**Caveat:** if the integrated terminal launched before the PATH update from your install, `claude` will appear missing until you open a new integrated terminal window. Close and reopen the terminal, or run `source ~/.zshrc` / `source ~/.bashrc`.

**Sources:**
- https://code.claude.com/docs/en/setup (verified 16-05-2026)

---

## Q10: I have Claude on two Google accounts. How do I know which one is logged in, and how do I switch?

- Run `/status` inside Claude Code - it shows the logged-in account email and the active plan.
- To switch accounts: run `/logout`, then `/login` and pick the other account in the browser.
- Run `/doctor` for a broader check (auth, MCP servers, settings, context usage).

If you authenticate via API key instead of OAuth, the `ANTHROPIC_API_KEY` env var takes precedence over the logged-in account. Unset it to use OAuth.

**Sources:**
- https://code.claude.com/docs/en/authentication (verified 16-05-2026)
- https://code.claude.com/docs/en/commands (verified 16-05-2026)

---

## Q11: Can I configure the 5-hour / 7-day usage window? How do I check how much I have used?

**Short answer:** No, the usage windows are fixed by plan. You can check current usage but cannot extend the window itself.

- Run `/usage` inside Claude Code to see remaining quota for the current 5-hour and weekly windows on Pro and Max plans.
- Run `/cost` to see token / dollar usage for the current session.
- Pro and Max plans have rolling usage windows (5-hour and weekly). Limits depend on plan tier. The fixed window cannot be reset on demand - it rolls automatically.
- If you hit the limit, you can: wait for the window to roll, upgrade plan, or switch to API-key billing (pay-per-token, no window).

For the current published limits, see the pricing page. Limits change over time, so don't trust any number quoted in this doc - check the source URL.

**Sources:**
- https://code.claude.com/docs/en/costs (verified 16-05-2026)
- https://www.anthropic.com/pricing (verified 16-05-2026)

---

## Q12: We don't use GitHub today. Only the developers do. Is Claude Code still useful for me as a PM?

**Yes.** GitHub is not required to use Claude Code. Claude Code is a CLI that works on any local folder.

What you get without GitHub:

- Read and write any files in a folder (specs, notes, PRDs, transcripts, Markdown docs).
- Run skills like `confluence-to-md`, `md-to-confluence`, `write-prd`, `feature-spec`, `meeting-to-spec`.
- Use MCP servers to talk to Confluence, Jira, Linear, Slack, Granola, Google Drive - all independent of GitHub.
- Manage memory, rules, settings, status line, all of it.

What you lose without GitHub:

- The `gh` CLI integration (pull requests, issues, releases). Not relevant if you don't work in code.
- The `/batch` skill, which requires a git repo - but you can `git init` a local folder without ever pushing to GitHub.

**Recommendation:** if you don't use GitHub, still run `git init` inside your working folder. It gives Claude Code checkpoints and lets it run skills that expect a git repo, with zero need for a remote.

**Sources:**
- https://code.claude.com/docs/en/overview (verified 16-05-2026)
- https://code.claude.com/docs/en/commands (verified 16-05-2026)

---

## Q13: Claude Code inside the IDE's integrated terminal vs Claude Code in a separate external terminal - what's the actual difference?

**Short answer:** Functionally identical. Pick based on workflow ergonomics, not capability.

Both run the same `claude` binary, get the same PATH, same auth, same MCP config, same skills, same global `CLAUDE.md`. Anything you can do in one, you can do in the other.

What changes is **ergonomics**:

| Aspect | IDE integrated terminal | External terminal |
|--------|------------------------|-------------------|
| File diffs | Renders inline in the IDE via the Claude Code IDE extension | Shown as text in the terminal |
| Open files | IDE extension can auto-share your current selection / open tab with Claude | No automatic context from your editor |
| `@-mention` files | Tab-completes against the IDE's workspace | Tab-completes from the shell's working directory |
| Window switching | One window, side-by-side with code | Two windows to alt-tab between |
| Screen space | Shares space with editor | Full terminal width |
| Multiple sessions | One per integrated terminal pane | Easier to run many in `tmux` / iTerm tabs |

**Practical rule:** use the IDE-integrated terminal when you want tight feedback loops on code changes (you see the diff land in the file as Claude writes it). Use an external terminal when you want full screen real estate, multiple parallel sessions, or you're working on non-code files (specs, notes) where IDE integration adds little.

**Sources:**
- https://code.claude.com/docs/en/vs-code (verified 16-05-2026)
- https://code.claude.com/docs/en/setup (verified 16-05-2026)

---

# May 2026 - Session 2 Additions

New questions raised by the NextLeap Applied Generative AI Bootcamp cohort on 16-05-2026 during Session 2 (Skills and sub-agents). All URLs verified 16-05-2026.

---

## Q14: When should I create a skill vs just chat with Claude, or put it in CLAUDE.md?

**Short answer:** Three different containers for three different things.

- **Chat** - one-off questions and exploratory work. Don't formalise.
- **Skill** - a repeatable workflow that produces a structured output (PRD, feature spec, release note, PPT, flowchart, standup summary, competitor study). Rule of thumb: if you've done it three times with the same shape, turn it into a skill.
- **CLAUDE.md** - project facts and architecture (what the project is, where files live, tech stack, things to never do here).
- **Memory** - cross-project rules and preferences (date format, tone, formatting, recurring corrections).

Don't make a skill for a single fact, a one-shot task, or a workflow whose output format is still changing.

**Sources:**
- https://code.claude.com/docs/en/skills (verified 16-05-2026)
- https://code.claude.com/docs/en/memory (verified 16-05-2026)

---

## Q15: What's the difference between a skill, a slash command, a sub-agent, and an MCP server?

| Thing | What it is | When to use |
|------|-----------|-------------|
| **Skill** | A folder with `SKILL.md` describing a repeatable workflow in plain English | One specific repeatable task with a stable output shape |
| **Slash command** | A shortcut typed with `/` to invoke a skill or built-in command (`/health`, `/doctor`) | Fast invocation of any skill or built-in |
| **Sub-agent** | A persona with its own context window and tool set that can call multiple skills | Orchestrating multiple skills under one role (e.g. "Senior PM agent") |
| **MCP server** | An external service connection (Confluence, Jira, Slack, Granola, Figma) | Reading from or writing to a system outside the local folder |

Analogy used in the session: *"I am an agent. My PRD-writer skill, my email-drafter skill, my release-note skill - those are the skills I invoke."*

The YAML front matter (`name` + `description`) is what tells Claude *when* to trigger a skill. The body tells it *how* to perform the task.

**Sources:**
- https://code.claude.com/docs/en/skills (verified 16-05-2026)
- https://code.claude.com/docs/en/commands (verified 16-05-2026)
- https://code.claude.com/docs/en/mcp (verified 16-05-2026)

---

## Q16: If a skill exists at both global and project level, which one wins?

**Project level wins.** Same as any standard config hierarchy - the more specific scope overrides the more general.

- Global skills: `~/.claude/skills/<skill-name>/SKILL.md` - apply to all projects.
- Project skills: `<repo>/.claude/skills/<skill-name>/SKILL.md` - apply only to that project, and override a global skill with the same name.

Practical tip from the session: for skills you care about (e.g. PRD writer), keep a copy at both levels and add a global memory like *"whenever I update a skill, sync it across all projects and the global folder"* so Claude prompts you to copy it. Skills don't auto-sync across machines or projects.

**Sources:**
- https://code.claude.com/docs/en/skills (verified 16-05-2026)
- https://code.claude.com/docs/en/memory (verified 16-05-2026)

---

## Q17: Can I rename `SKILL.md`? What about the folder name?

- **File name is fixed.** `SKILL.md` must be exactly that. Same for `AGENT.md` in sub-agent folders. Claude Code looks for those exact filenames.
- **Folder name is free.** Name the folder anything readable (`prd-writer/`, `release-notes/`).
- **`name:` in the front matter is also free.** This is the display name and trigger label.

```
.claude/skills/
  prd-writer/          <- folder name: free
    SKILL.md           <- file name: fixed
    references/        <- subfolders: free
    scripts/
```

**Sources:**
- https://code.claude.com/docs/en/skills (verified 16-05-2026)

---

## Q18: Is a skill just plain English, or do I need to write code?

**The skill itself is plain English.** `SKILL.md` is a markdown file describing the workflow step by step. Claude reads it and follows the instructions.

You add code only when the workflow needs deterministic output that an LLM can't produce reliably:

- Rendering a `.pptx` file - Python script using `python-pptx`.
- Rendering an SVG flowchart - Python or JS script.
- Calling an API with a fixed payload shape - script.
- Anything that must be byte-identical every time.

Scripts live in a `scripts/` subfolder inside the skill. The skill instructs Claude *when* to call the script and *what* to pass in. The LLM decides content; the script renders form.

**Sources:**
- https://code.claude.com/docs/en/skills (verified 16-05-2026)

---

## Q19: My skill is too long. How do I shrink it?

Keep `SKILL.md` short - target 100 to 200 lines. Anything beyond that goes into subfolders so the main file stays loadable and coherent:

| Subfolder | What goes there |
|-----------|----------------|
| `references/` | Long-form rules, style guides, framework cheat sheets, output templates, examples |
| `scripts/` | Executable code the skill calls |
| `assets/` | Images, SVGs, fixed templates, brand assets |

Practical prompt to use on an oversized skill: *"This skill is over 200 lines. Keep `SKILL.md` between 100 and 200 lines and move overflow into `references/`."* Claude will create the subfolder, split content into themed `.md` files, and replace inline blocks with references.

**Sources:**
- https://code.claude.com/docs/en/skills (verified 16-05-2026)

---

## Q20: Can I reuse a skill across projects?

Yes. Two options:

1. **Promote to global.** Move the skill to `~/.claude/skills/<skill-name>/` and every project picks it up.
2. **Copy-paste.** Copy the folder from `<projectA>/.claude/skills/<skill>/` to `<projectB>/.claude/skills/<skill>/`. After copying, ask Claude *"I copied this skill from project A. Check if any paths or references need updating for project B"* and it will fix relative paths.

There's no built-in skill marketplace or `import`. Treat skills as portable folders.

**Sources:**
- https://code.claude.com/docs/en/skills (verified 16-05-2026)

---

## Q21: Will the same skill give the same output for me and my teammate?

**Not by default.** LLMs are probabilistic. Two people running the same skill on the same input will get two different wordings.

What you can control:

- **Structure** - put a strict output template (exact headings, exact section order, exact table columns) as a `.md` file under `references/` and have the skill fill that template. The content varies, the skeleton doesn't.
- **Tone and rules** - codify in `references/style.md` (sentence length, banned phrases, voice).
- **Inputs** - for high-variance inputs, build a "dynamic skill" that pauses and asks the user to select parameters before producing output.

Treat skills like templates plus rules, not deterministic functions.

**Sources:**
- https://code.claude.com/docs/en/skills (verified 16-05-2026)

---

## Q22: What is skill chaining?

A **chained skill** is a master skill whose body calls several smaller skills in sequence to deliver a larger workflow.

Example walked through in the session - a `/wake-up` skill that on invocation:

1. Checks Confluence for updates.
2. Checks Jira for ticket changes.
3. Pulls mail (Zoho mail in my case).
4. Processes meeting notes.
5. Consolidates everything into a single "focus for today" file.

Recommended progression: get individual skills stable first, then chain them, then put an agent on top. Chaining unstable skills compounds errors.

**Sources:**
- https://code.claude.com/docs/en/skills (verified 16-05-2026)
- https://code.claude.com/docs/en/mcp (verified 16-05-2026)

---

## Q23: In a chained workflow, where do I put evaluation criteria - one final check or one per skill?

**One per skill.** Each skill should validate its own output before passing data to the next skill.

If you only evaluate at the end, a bad output from step 1 poisons every downstream step and you have to rerun the whole chain. Per-skill evals fail fast and isolate the problem.

In practice: every skill's `SKILL.md` ends with a short "Quality checks before returning" list (3-5 bullets) that Claude runs against its own output before handing off.

**Sources:**
- https://code.claude.com/docs/en/skills (verified 16-05-2026)

---

## Q24: A recurring rule I want Claude to always follow - does that go in CLAUDE.md or a skill?

**Neither. It goes in memory.**

| Container | What it's for |
|-----------|--------------|
| **CLAUDE.md** | Project-level definition (architecture, tech stack, file map, things never to do *in this project*) |
| **Skill** | A repeatable workflow that produces a structured output |
| **Memory** | A standing rule or preference Claude should apply whenever generating output (date format, formatting, tone, naming, units) |

Memories used to live inside `CLAUDE.md` but Anthropic split them out so `CLAUDE.md` stays focused on project structure and doesn't bloat.

**Sources:**
- https://code.claude.com/docs/en/memory (verified 16-05-2026)

---

## Q25: Do I need an `AGENT.md` for every skill?

**No.** Agents and skills are different layers.

- A **skill** is invokable on its own (`/feature-spec`, `/release-notes`).
- An **agent** is a persona that orchestrates multiple skills under one identity (e.g. "Senior PM" agent that decides which skill to call based on the situation).

Build agents only after your skills are stable and you need a persona-level orchestrator. Agent setup is a Session 3 topic.

**Sources:**
- https://code.claude.com/docs/en/skills (verified 16-05-2026)

---

## Q26: Where does a design system fit? It feels too big for one skill.

It is too big. A design system is a **folder of references, not a single skill**.

Keep it as a folder (e.g. `ux-guidelines/`, `design-system/`) holding markdown files for things like colors, buttons, and component rules, plus any assets - images, SVGs, brand files.

When you want to generate UI, point Claude at the folder: *"Use `.claude/design-system/` for brand and component rules."* Commit the folder to the repo so every teammate's Claude generates UI with the same brand.

If you need live Figma assets, connect via the Figma MCP. Heads-up: read-only Figma accounts hit MCP call limits quickly (around 5-6 calls per session). A Dev account avoids that.

**Sources:**
- https://code.claude.com/docs/en/mcp (verified 16-05-2026)

---

## Q27: Which Claude model should I default to? I want to conserve tokens.

- **Sonnet, medium effort** for almost everything - drafting, editing, skill execution, code review. Sonnet is the best default.
- **Opus** only for complex brainstorming or complex coding.

Set your default model in `/config` or via the status line. Enable the status line so you can watch context usage and 5-hour / 7-day window burn in real time. Switch up to Opus only when you actually need it.

**Sources:**
- https://code.claude.com/docs/en/costs (verified 16-05-2026)
- https://code.claude.com/docs/en/cli-reference (verified 16-05-2026)

---

## Q28: Do I need an Antigravity subscription to use Claude Code?

**No.** Antigravity is just an IDE. Claude Code runs in the terminal and uses your Claude (Pro, Max, Team, Enterprise) subscription or your Anthropic API key for billing.

You only need an Antigravity paid plan if you want to use **Antigravity's own agent features inside that IDE**. For Claude Code itself, the Claude subscription is enough.

**Sources:**
- https://code.claude.com/docs/en/setup (verified 16-05-2026)
- https://code.claude.com/docs/en/vs-code (verified 16-05-2026)

---

## Q29: What's the right way to actually create a skill?

Don't ask Claude to "create a skill" cold. Build the input first, then scaffold.

1. **Define the problem.** What workflow, what input, what output shape.
2. **Have Claude research the domain.** *"Find the top books, frameworks, and authors on user interviews."* Expect names like *The Mom Test*, *Continuous Discovery Habits* (Teresa Torres), *Interviewing Users* (Steve Portigal), *Inspired* (Marty Cagan).
3. **Challenge the picks.** *"Why these and not X?"* See its reasoning. Approve or push back.
4. **Have Claude draft a prompt** that encodes the chosen frameworks - this becomes the basis of `SKILL.md`.
5. **Scaffold the skill folder** with `SKILL.md`, `references/`, `scripts/`.
6. **Test the auto-trigger.** Type a real task and see if the skill fires from the `description` alone.
7. **Iterate.** Every miss becomes a new eval rule inside the skill.

Memorable naming tip: put a keyword you'll actually search for in the skill name (`email-drafter`, `ppt-builder`) so you can recall it months later.

**Sources:**
- https://code.claude.com/docs/en/skills (verified 16-05-2026)

---

## Q30: Can I use Perplexity or Gemini to help build a Claude skill?

**Yes.** Use whichever tool is best for each step.

- **Perplexity / Gemini** - good for gathering up-to-date framework research, comparing methodologies, citing sources.
- **Claude Code** - turns that research into the actual `SKILL.md`, `references/`, and `scripts/` inside your project.

Workflow: research in Perplexity, paste the distilled findings into Claude Code, then have Claude scaffold the skill folder. The skill itself only lives inside Claude Code's folder structure.

---

## Q31: How many memories should I have? What kinds of things belong there?

There is no hard limit. The host's work machine has 400+ memories. The rule is **save once, never repeat the correction**.

Good memory candidates:

- Date format (`DD-MM-YYYY`, never ISO or US).
- Formatting rules (no unnumbered bullet points, table column headers in title case).
- Tone rules (collaborative phrasing, no blame in exec summaries).
- Tool-specific quirks (use Confluence's native table column property, not manual serial numbers).
- Disambiguation (two people named "Sarah" - clarify which one).
- Banned phrases.

Every time Claude makes the same mistake twice, save the correction as a memory. It compounds fast.

**Sources:**
- https://code.claude.com/docs/en/memory (verified 16-05-2026)

---

# May 2026 - Session 3 Additions

New questions raised by the NextLeap Applied Generative AI Bootcamp cohort on 17-05-2026 during Session 3 (Agents and sub-agents). All URLs verified 17-05-2026.

---

## Q32: What is an agent, and how does it differ from a prompt or a skill?

| Layer | What it is | Example |
|-------|-----------|---------|
| **Prompt** | One instruction. You guide every turn manually | "Write me a LinkedIn post" |
| **Skill** | A repeatable workflow with a fixed shape | `/feature-spec`, `/release-notes` |
| **Agent** | A persona with its own context, tools, and memory that picks the route on its own based on a goal | "Find three relevant stories from my industry, study my past posts for voice, draft a new post, revise against my style guide, schedule for Tuesday" |

A prompt is a single instruction. A skill is a repeatable task. An agent is a goal plus the ability to iterate, call tools, and adapt mid-run when something breaks. The real test of an agent is *"when the first path breaks, can it find another?"*

**Sources:**
- https://code.claude.com/docs/en/sub-agents (verified 17-05-2026)
- https://code.claude.com/docs/en/skills (verified 17-05-2026)

---

## Q33: Do I have to specify a role (analyst, planner, operator) when creating an agent?

**No.** Claude infers the role from the description and prompt you give. If your description says "review code and surface issues", it acts as an auditor. If it says "plan a release", it acts as a planner. You don't need to label the persona explicitly.

The role types (analyst, planner, operator) are useful for *thinking* about what kind of agent you're building, not for configuring one.

**Sources:**
- https://code.claude.com/docs/en/sub-agents (verified 17-05-2026)

---

## Q34: When I save agent memory at project level, does it sync with my Claude.ai project (web app)?

**No.** Project-level agent memory lives inside the repo at `.claude/agents/<agent-name>/memory/` (or a similar path the agent picks). It is a local filesystem artifact tied to that folder.

The "Project" feature inside the Claude.ai web app (where you upload files for chat context) is a separate construct. It does not auto-sync with `.claude/` folders on your machine. Treat them as two different systems that happen to share the word "project".

**Sources:**
- https://code.claude.com/docs/en/sub-agents (verified 17-05-2026)
- https://code.claude.com/docs/en/memory (verified 17-05-2026)

---

## Q35: Should a code reviewer agent have edit access, or should I create a separate agent to apply fixes?

**Start read-only. Always.**

- First few iterations: read-only access. The agent produces a report file (`outputs/code-review-*.md`). You read it, validate it, and refine the agent based on what it got right or wrong.
- Once you trust the output across multiple iterations, you can either (a) grant the same agent edit access and update its prompt to apply fixes, or (b) create a second agent (e.g. `code-fixer`) that consumes the review file and edits the code.

Two-agent separation is cleaner: one auditor that finds problems, one operator that fixes them. Easier to test, easier to swap one without breaking the other.

**Sources:**
- https://code.claude.com/docs/en/sub-agents (verified 17-05-2026)
- https://code.claude.com/docs/en/permissions (verified 17-05-2026)

---

## Q36: What is a sub-agent, and how do I invoke one?

A sub-agent is a fresh, isolated Claude instance that the main session dispatches via the `Agent` tool. It runs in its own context window with its own tool set, returns a single result, and goes away. Use it to keep large or specialised work off your main session's context.

Two ways to invoke:

1. **By name** - `@agent-name do this task`. Triggers your custom agent file.
2. **Generic dispatch** - just say "use a sub-agent to review this". Claude picks a default sub-agent and runs it. You don't have to define one yourself for generic review tasks.

The point of a sub-agent in this session was *LLM as a judge*: have one agent produce output, then have a second sub-agent review that output against a rubric and iterate until it hits a quality bar (e.g. "score > 95/100").

**Sources:**
- https://code.claude.com/docs/en/sub-agents (verified 17-05-2026)

---

## Q37: How do I make the sub-agent use a different model than my main session (e.g. Opus to review Sonnet's output)?

Two steps:

1. Run `/model` and pick the model you want available (e.g. switch to Opus).
2. In your prompt, explicitly tell the sub-agent which model to use: *"use a sub-agent with the Opus model to review this against the rubric"*.

This is the practical "LLM as a judge" pattern - Sonnet generates, Opus reviews. Opus is more expensive, so reserve it for the reviewer role, not the generator.

**Sources:**
- https://code.claude.com/docs/en/cli-reference (verified 17-05-2026)
- https://code.claude.com/docs/en/sub-agents (verified 17-05-2026)

---

## Q38: My agent's output went into the chat instead of the `outputs/` folder. Why?

This happened mid-session: the agent file's stage 4 clearly said *"write synthesis to `outputs/`"*, but the output came back inline. Root cause - when you invoke an agent with a custom prompt (e.g. "run this agent and just give me the result"), the custom prompt can override the agent's own stage instructions.

Fix:

1. Ask the agent in chat *"why was the output file not created?"* - it will explain which instruction got bypassed.
2. Save the lesson to **agent memory**, not project memory. The instruction is agent-specific, not project-wide.
3. Add a non-negotiable rule to the agent memory file: *"Always write output to `outputs/`. Stage 4 is non-negotiable even if invoked via a custom prompt."*

**Sources:**
- https://code.claude.com/docs/en/sub-agents (verified 17-05-2026)
- https://code.claude.com/docs/en/memory (verified 17-05-2026)

---

## Q39: I'm starting a brand new project folder. What's the right first step?

1. Open Antigravity / IDE, open the new folder.
2. Open the integrated terminal in that folder.
3. Run `claude` to start a session.
4. Run `/init`.
5. When prompted, type a short description of what the project is *before* `/init` finishes - otherwise it will guess from sibling folders and produce a misleading `CLAUDE.md`.

If `/init` starts inspecting sibling directories outside your project, press `Ctrl+C`, then re-prompt with explicit context: *"This folder is for X. Don't look at other folders. Create a `CLAUDE.md` for this project."*

**Sources:**
- https://code.claude.com/docs/en/commands (verified 17-05-2026)
- https://code.claude.com/docs/en/memory (verified 17-05-2026)

---

## Q40: What does `/init` actually do?

`/init` initialises a `CLAUDE.md` for the current folder.

- If `CLAUDE.md` doesn't exist - it explores the folder, infers what the project is, and writes a fresh `CLAUDE.md` describing structure, tech stack, and conventions.
- If `CLAUDE.md` already exists - it reads what's there and updates it with anything it has learned since.
- If the folder is empty - it falls back to parent directories to guess context. This is why providing your own context up front matters (see Q39).

**Sources:**
- https://code.claude.com/docs/en/commands (verified 17-05-2026)
- https://code.claude.com/docs/en/memory (verified 17-05-2026)

---

## Q41: Agent vs routine - what's the actual difference?

| Aspect | Agent | Routine (scheduled task) |
|--------|-------|-------------------------|
| Purpose | Goal-seeking persona with reasoning | Scheduled execution of a fixed instruction |
| Memory | Yes - evolves over time via `agent-memory/` | No persistent memory |
| Adapts on failure | Yes - re-routes when a step breaks | No - fails or skips |
| Trigger | On demand by name or via main agent | Cron schedule (daily, weekly, etc.) |
| Where it runs | Same session or sub-agent | Local machine OR Anthropic's cloud environment |
| Use case | "Review this PR", "Draft this PRD" | "Email me Anthropic's docs digest every day at 7 AM" |

If you ask Claude to "create an agent that runs daily at 7 AM and emails me X", it will create a **routine**, not an agent - because the time trigger plus deterministic instruction is a cron job, not a reasoning loop. The session demoed exactly this: prompt said "create an agent", Claude correctly built a routine instead.

**Sources:**
- https://code.claude.com/docs/en/sub-agents (verified 17-05-2026)
- The `/schedule` skill (built-in) and Claude Code routines feature.

---

## Q42: When I create a routine in the terminal, does it appear in the Claude.ai web app too?

**Yes.** Routines created via Claude Code (terminal) sync automatically to the Routines panel in the Claude.ai web app, provided both are signed into the same account.

To view, edit, or manually trigger a routine, open Claude.ai, go to **Claude Code > Routines**. You'll see each routine with its schedule, environment, connectors, and inspection log. Hit *Test* / *Run now* to fire it on demand and see the log.

---

## Q43: How many routines can I run per day?

Plan-dependent rolling limits:

- **Pro:** 5 routine runs per rolling 24 hours (included).
- **Max:** 15 routine runs per rolling 24 hours (included).
- Beyond the included quota, extra runs consume "extra usage" - only billed if you've explicitly enabled it in settings. Otherwise the routine is skipped.

Practical tip: if you have many candidate routines, keep low-value ones on weekly or monthly schedules so daily slots stay free for the high-value ones.

Verify current limits at the Claude.ai usage page - quotas change.

**Sources:**
- https://www.anthropic.com/pricing (verified 17-05-2026)

---

## Q44: What is Claude.ai Co-work, and how does it differ from Claude Code?

Three Claude surfaces, three different jobs:

| Surface | What it is | Best for |
|--------|-----------|----------|
| **Claude.ai chat** | Standard web chatbot | One-off questions, exploration, no folder context |
| **Claude.ai Co-work** (desktop app) | Folder-aware chat - point at a local folder, ask questions, get summaries | Non-technical members who want folder context without the IDE or terminal |
| **Claude Code** (terminal / IDE) | Full agentic loop - file edits, bash, sub-agents, skills, memory, MCP servers | The actual power tool. Skills you create, agents you define, memories you save - all live here |

Co-work limitations vs Claude Code:
- Co-work cannot see custom skills under `.claude/skills/` (it only sees its own plugin/skill library).
- Co-work cannot create or modify agent files, agent memory, or rules.
- Co-work shows chat output, not a diff view of file changes.

Think of it as **chat > Co-work > Code** on the capability ladder. Co-work is a stepping stone for non-technical teammates; Claude Code is where the real customisation lives.

**Sources:**
- https://code.claude.com/docs/en/overview (verified 17-05-2026)

---

## Q45: Can I build one master agent (e.g., `aman.md`) that has access to all my skills?

**Yes, but don't start there.**

It is possible to build a single PM agent with system-prompt access to all your skills (PRD writer, user interview synthesiser, release notes, competitor analysis, etc.). Sub-agents do not auto-inherit your skill set, but you can list the skills explicitly in the agent's system prompt and the agent will dispatch them.

Trade-offs:

- **Pro:** single entry point - "write a PRD for Smart Follow-Up" routes itself to the right skill. Long-running drafts don't bloat your main session. Your standing PM rules (date format, no em dashes, cite sources) apply across every skill.
- **Con:** the master agent runs in fresh context. If you say *"write user stories for what we just discussed"*, the sub-agent does not know what you were discussing. You'd have to brief it.

**Recommendation:** get each individual skill stable first. Then chain related skills. Only after those work end-to-end, wrap them in a master agent. Building the master agent first compounds errors and gives you a system you can't debug.

**Sources:**
- https://code.claude.com/docs/en/sub-agents (verified 17-05-2026)
- https://code.claude.com/docs/en/skills (verified 17-05-2026)

---

# May 2026 - Session 4 Additions

New questions raised by the NextLeap Applied Generative AI Bootcamp cohort on 18-05-2026 during Session 4 (Building prototypes with Claude Code). All URLs verified 18-05-2026.

---

## Q46: What is a "UX zone" and why bother building one?

A **UX zone** is a folder inside your repo that holds everything a prototype needs to look like it belongs to your product family - components, design tokens, assets, screen notes, reference screenshots. Every prototype in the company points at the same UX zone, so output is consistent regardless of who built it.

A typical UX zone:

```
ux-zone/
  components/        React + Tailwind component files
  tokens/            color, type, spacing JSON
  assets/            SVG icons, brand images, fonts
  screens/           reference screenshots from Mobbin / your own product
  screen-notes/      per-screen guidance (which references to mirror)
  spec.md            human-readable design system rules
```

**Why bother:**

- Same prototype, two teammates = same look and feel. Without a UX zone, every prototype is a snowflake.
- Engineering hand-off becomes much cleaner - the UX zone is the source of truth, not a Figma file + verbal context.
- Future Figma MCP / Figma Code Connect flows can map UX zone components to Figma frames automatically.

**Sources:**
- https://code.claude.com/docs/en/skills (verified 18-05-2026)
- Anthropic Frontend Design skill (`frontend-design` plugin) - see https://code.claude.com/docs/en/mcp (verified 18-05-2026)

---

## Q47: How is a plugin different from an MCP server?

| | Plugin | MCP server |
|---|--------|------------|
| What it is | A packaged bundle of skills, hooks, and slash commands distributed via a marketplace | A connection to an external service (Slack, Jira, Confluence, Figma, Granola) |
| Where the code lives | Hosted remotely; you install via `/plugin install <name>@<marketplace>` | Configured locally via `/mcp` or `claude mcp add`; the MCP server runs as a separate process |
| What it does | Adds new in-session capabilities (a brainstorming skill, a code review skill, a frontend design skill) | Adds tools that read from / write to a system outside your local folder |
| Example | `superpower` plugin auto-invokes brainstorming when you say "let's brainstorm..." | `mcp__claude_ai_Granola__get_meeting_transcript` fetches a Granola transcript |

**Rule of thumb:** if it changes how Claude thinks/works in-session, it's a plugin (or a skill inside one). If it lets Claude talk to a system outside your folder, it's an MCP server.

**Sources:**
- https://code.claude.com/docs/en/skills (verified 18-05-2026)
- https://code.claude.com/docs/en/mcp (verified 18-05-2026)

---

## Q48: How do I discover useful plugins? Will Claude tell me which ones to install?

**Claude won't tell you proactively.** You have to know what to install.

How to discover:

1. Inside Claude Code, run `/plugin`. The picker lists plugins available across marketplaces - Anthropic's official directory, community marketplaces, and any you've added.
2. Browse by purpose - design, code review, web automation, observability, productivity.
3. For unfamiliar plugins, take a screenshot of the plugin description and paste it into another Claude session: *"What does this plugin do? When would I use it?"*

**A working starter set for PMs and prototyping:**

- `superpower` - brainstorming, planning, auto-invokes other skills
- `skill-creator` - scaffolds new skills with correct frontmatter
- `frontend-design` - auto-improves UI on prototypes
- `code-review` - flags critical issues before commit
- `code-simplifier` - cleans up after implementation
- `chrome-devtools` (MCP) - inspect live UI from inside Claude
- `playwright` (MCP) - browser automation for testing flows
- `figma` (MCP) - design-to-code if you use Figma

Install once at session start. Verify each plugin's permissions before installing - plugins are community-contributed and not security-audited by Anthropic.

**Sources:**
- https://code.claude.com/docs/en/skills (verified 18-05-2026)
- https://code.claude.com/docs/en/mcp (verified 18-05-2026)

---

## Q49: What does the Superpower plugin actually do?

Superpower is a meta-plugin that auto-routes to the right skill based on what you say:

- "Let's brainstorm X" → fires the brainstorming skill (asks 3-5 scoping questions before any code/draft)
- "Plan this implementation" → fires the planning skill
- "I'm stuck debugging" → fires the systematic-debugging skill
- "Write a spec for..." → fires the relevant feature/PRD skill if installed

You don't have to remember which sub-skill to call. Superpower watches the conversation and invokes the right one. If it's not installed, your sessions will look "flatter" - no auto-brainstorming, no auto-planning.

It is **not required** to use Claude Code, but if you skip it, you'll re-type the scoping questions yourself every time. Install it.

**Sources:**
- https://code.claude.com/docs/en/skills (verified 18-05-2026)

---

## Q50: How is this different from prototyping in Cursor? Can't I do the same thing there?

**Short answer:** you can build a single-shot prototype in Cursor. You cannot build the *assembly line* in Cursor.

A single prototype in Cursor and a single prototype in Claude Code can look the same. The difference shows up the **second time** you build something:

| Capability | Cursor | Claude Code |
|-----------|--------|-------------|
| Build one prototype | Yes | Yes |
| Run a brainstorming skill that scopes before coding | No | Yes (via plugins) |
| Reuse a UX zone folder across projects | Manual | Manual, but enforced via project rules + skills |
| Spawn sub-agents to review the prototype after build | No | Yes |
| Install plugins (frontend-design, code-review, playwright) | No | Yes |
| Add MCP servers for Mobbin, Figma, Chrome DevTools | No | Yes |
| Run `make it 10x better` as a structured sub-agent review | Manual | Yes |
| Schedule a routine that re-runs the workflow weekly | No | Yes |

**The one-line answer:** Cursor is a better editor. Claude Code is a better workshop. The moment you want to build the *thing that builds the thing*, you need the workshop.

**Sources:**
- https://code.claude.com/docs/en/overview (verified 18-05-2026)
- https://code.claude.com/docs/en/skills (verified 18-05-2026)

---

## Q51: Mobbin vs Google Stitch vs Figma Make - which one for which job?

| Tool | What it is | Best for |
|------|-----------|----------|
| **Mobbin** | Curated library of real-world app UI references (mobile + web) | Building a **UX zone** of reference screenshots before you prototype - "show me how 5 meeting apps handle action items" |
| **Google Stitch** | AI tool that generates UI designs from prompts | Generating a fresh UI when you have no reference - works for both web and mobile |
| **Figma Make** | Figma's AI tool that generates production-ready designs in Figma | Same category as Lovable / Bolt - prompt-to-app, but inside Figma |

**Rule of thumb:**
- Need **references** to mirror? → Mobbin
- Need a **fresh design** generated from a prompt? → Google Stitch or Figma Make
- Need to **build the prototype** that consumes references and produces real code? → Claude Code with a UX zone, optionally pulling Figma assets via the Figma MCP

These are not competitors; they sit at different stages of the pipeline.

**Sources:**
- https://www.mobbin.com (verified 18-05-2026)
- https://stitch.withgoogle.com (verified 18-05-2026)

---

## Q52: Do I need a paid Mobbin plan, or can I get by without?

**You can get by without.** Mobbin is the easiest path because it's curated for UI references, but the same UX-zone outcome works from any public source:

- Public design system articles (e.g. Zomato's published design system) - use the Playwright MCP to scrape components, tokens, and assets into your UX zone.
- Open-source design systems (Material, Carbon, shadcn/ui, Radix) - clone the repo or point Claude at the docs and ask it to extract tokens + components.
- Your own product screenshots + a written style guide - feed both into Claude and ask it to build the UX zone from those.

If you do go paid: Mobbin "deep mode" with narrower queries produces meaningfully better references than the default fast mode. Worth knowing if your team commits to it.

**Sources:**
- https://www.mobbin.com (verified 18-05-2026)

---

## Q53: When do I use Frontend Design (plugin) vs Figma MCP vs Playwright?

| Tool | Purpose | Trigger |
|------|---------|---------|
| **Frontend Design skill** (plugin) | Polish a prototype's UI for visual quality and component reuse after it's been built | Run as a sub-agent after first build: *"use the frontend-design sub-agent to review and improve this prototype"* |
| **Figma MCP** | Read your team's Figma file - pull design tokens, component specs, frames - to inform code generation | When your source of truth is Figma and you want code that mirrors it |
| **Playwright MCP** | Drive a real browser - scrape sites, automate flows, capture screenshots, test the running prototype | When you need to either (a) extract from a live website, or (b) verify a flow end-to-end after the build |

You can use all three in one session - Playwright scrapes a reference site into the UX zone, Figma MCP pulls your brand tokens, and Frontend Design polishes the final output.

**Heads-up:** Figma MCP requires a **Figma Dev account**. Free / read-only Figma accounts hit MCP rate limits within ~5-6 calls per session.

**Sources:**
- https://code.claude.com/docs/en/mcp (verified 18-05-2026)

---

## Q54: What does "build the assembly line" actually mean in practice?

The framing: spend **20% of your time on the work, 80% on the system that does the work** (CLAUDE.md, rules, skills, agents, UX zones, knowledge folders).

What that looks like for a PM in practice:

1. **Knowledge folders.** A `product-knowledge/`, `user-research/`, `competitive-landscape/`, and `team-structure/` folder per project. Any time you learn something new (a customer quote, a Confluence page, a Jira pattern), drop it in.
2. **Project rules.** When you correct Claude's output, save the correction as a memory or a rule under `.claude/rules/`. The same correction never has to be made twice.
3. **Skills.** Every workflow you do more than three times - PRD writing, release notes, retro synthesis, user interview synthesis - becomes a skill.
4. **Agents.** Wrap your skills behind a persona (e.g. "Senior PM agent") that picks the right skill for the situation.
5. **Routines.** For the work that needs to happen on a schedule (weekly competitor digest, daily Anthropic docs digest), put it on cron.

**The compounding effect:** after a few months, the system is producing output that would take a teammate days, in minutes. That is the "moat" referenced earlier in the workshop.

**The career framing:** *"Want to isolate your job? Put everything you know into the factory. The more you can document and automate, the more high-value work you free up - for yourself."*

**Sources:**
- https://code.claude.com/docs/en/memory (verified 18-05-2026)
- https://code.claude.com/docs/en/skills (verified 18-05-2026)

---

## Q55: My Claude Code terminal / sidebar / pinned panel vanished. How do I get it back?

In Antigravity / VS Code:

- The right-hand pinned panel (where Claude Code, the agents view, and the terminal sit) is the **Secondary Side Bar**. Toggle it via `View → Appearance → Secondary Side Bar`, or `Cmd+Alt+B` (Mac) / `Ctrl+Alt+B` (Win/Linux).
- The Secondary Activity Bar (the vertical icon strip on the right) is on by default. If it's gone, right-click the title bar and ensure `Secondary Activity Bar Position` is set to `default` (not `hidden`).
- If a Claude Code session "disappeared" mid-task, it's usually paused, not killed. Re-open the terminal and type `continue` and hit enter - it will resume from where it stopped.
- If you accidentally pressed `Ctrl+C` or `Esc` during a Claude operation, the run stopped. Re-issue the prompt or type `continue` to resume the agent loop.

If the cursor moves but selection doesn't work inside Claude Code's TUI - that's normal. Use arrow keys + Enter, not the mouse, for selection inside the agent / plugin pickers.

**Sources:**
- https://code.claude.com/docs/en/vs-code (verified 18-05-2026)
- https://code.claude.com/docs/en/troubleshooting (verified 18-05-2026)

---

## Q56: How do I write a PRD without forgetting business rules or edge cases?

**Don't try to remember them. Put them in `product-knowledge/`.**

The pattern:

1. Maintain a `product-knowledge/business-rules.md` (or equivalent) - every business rule, every edge case, every constraint that should never be missed.
2. Wire your PRD-writer skill so it **always** reads `product-knowledge/business-rules.md` before drafting.
3. Maintain a PRD template (`14-templates/prd-template.md`) the skill must follow.
4. When a meeting or interview surfaces a new edge case, drop the transcript into Granola → save the relevant chunk as a new entry in `business-rules.md`. The next PRD draft pre-empts it automatically.

The PRD skill becomes a function over three inputs - business rules, template, current feature context. The skill never forgets, because the knowledge isn't in the skill; it's in the knowledge folder the skill consumes.

**Sources:**
- https://code.claude.com/docs/en/skills (verified 18-05-2026)
- https://code.claude.com/docs/en/memory (verified 18-05-2026)

---

# May 2026 - Session 5 Additions

New questions raised by the NextLeap Applied Generative AI Bootcamp cohort on 23-05-2026 during Session 5 (Multi-agent architectures). All URLs verified 23-05-2026.

---

## Q57: Is "knowledge base" the same as project context, or is it a separate feature?

**Same thing, different label.** In Claude Code there's no separate "knowledge base" product - what teams call a knowledge base is just the set of context files in your project folder that Claude reads automatically.

Concretely, the knowledge base for a MeetFlow-style project is:

- `CLAUDE.md` - project-level standing instructions
- `03-product-knowledge/` - company, product, competitive context
- `04-strategy/` - vision, OKRs, roadmap
- `05-user-personas/` - persona deep-dives
- `07-user-interviews/` - transcripts

If those files don't exist, Claude falls back to generic LLM knowledge and the output is shallow. The richer the context folder, the richer the output. Some teams call it "context", "project OS", or "knowledge base" - it's the same thing.

**Sources:**
- https://code.claude.com/docs/en/memory (verified 23-05-2026)

---

## Q58: How do I feed books or large PDFs to Claude without burning tokens?

**Don't feed PDFs directly.** Two-step pattern:

1. **Convert PDF/PPT/Word -> Markdown** via a Python script (e.g. `pypdf` + your own converter). Drop the script in `.claude/scripts/pdf-to-md.py` and invoke it via a skill.
2. **Add a front-matter ToC** to the resulting MD so Claude can jump straight to the relevant chapter. If chapter 5 is what you need, the front-matter index points there - Claude doesn't have to scan chapters 1-4.

If the MD is still huge (5000+ lines), generate a per-chapter summary file alongside the full MD. Claude consults the summary first, then opens only the chapter it needs.

**Rule of thumb:** never let Claude ingest binary documents. Convert, index, summarize. Each step cuts tokens 10x.

**Sources:**
- https://code.claude.com/docs/en/memory (verified 23-05-2026)

---

## Q59: How do I store per-stakeholder context (manager, PM peers, exec)?

**One folder, one MD per stakeholder.** Keep it out of `CLAUDE.md` - that file is for project-wide rules, not personal relationships.

Suggested layout:

```
.claude/personas/
  amit-manager.md
  priya-engineering-lead.md
  raj-design-partner.md
```

Each file holds: what they care about, communication style, recurring feedback, current open threads, last 1:1 notes. Update after each 1:1. When you prompt Claude for "prep for my 1:1 with Amit", it reads `amit-manager.md` first and the prep reflects Amit's actual style, not generic manager advice.

**Sources:**
- https://code.claude.com/docs/en/memory (verified 23-05-2026)

---

## Q60: If I have 50 interview transcripts, do I spawn 50 sub-agents or 10 sub-agents reading 5 each?

**Let Claude decide unless you have a strong reason.** Prompt: *"I have 50 transcripts. Launch the right number of sub-agents to extract themes - decide based on file size and parallelism."* Claude inspects file sizes, estimates per-agent context, and picks a count.

If you do want to fix the count, say it explicitly: *"Launch exactly 10 sub-agents, 5 transcripts each."*

There is no documented hard cap on sub-agent count, but each sub-agent burns tokens and Anthropic plan limits (5h / weekly windows) apply. For 50+ transcripts, the practical sweet spot tends to be 5-10 sub-agents each handling a batch, not 50 in parallel.

The lead agent then reads only the per-batch summaries (not the raw transcripts), keeping its own context clean.

**Sources:**
- https://code.claude.com/docs/en/sub-agents (verified 23-05-2026)

---

## Q61: What is a "lead orchestrator" and how do I trigger one?

A **lead orchestrator** is the top-level agent in a multi-agent run that splits work, dispatches helpers, reads their summaries, and assembles the final output. Mental model: project lead + 3 developers + 1 QA. The lead never reads the raw code - only the helpers' status reports.

You don't configure the orchestrator manually for sub-agent flows - Claude takes that role implicitly when you say *"spawn sub-agents to do X in parallel"*.

For the formal **agent-teams** feature (where the orchestration is explicit), you must:

1. Enable the experimental flag in `settings.json`.
2. Use the phrase "**create an agent team**" in your prompt.
3. Define the helpers (e.g. front-end agent, back-end agent, QA agent).

Anthropic's published benchmark: a lead + several helpers outperformed a single agent by 90.2% on their internal multi-agent research evaluation.

**Sources:**
- https://www.anthropic.com/engineering/built-multi-agent-research-system (verified 23-05-2026)
- https://code.claude.com/docs/en/sub-agents (verified 23-05-2026)

---

## Q62: Sub-agent vs agent team vs agent view vs work tree - which do I pick?

| Pattern | Use when | Trigger |
|---------|----------|---------|
| **Sub-agent** | Side task in parallel without polluting your main context | "Use a sub-agent to..." |
| **Agent team** | 3+ angles or specialized roles working together (front-end / back-end / QA) | "Create an agent team for..." (needs experimental flag) |
| **Agent view** | Background long-running tasks; you want to close the terminal and have it keep running | `claude agents` (instead of `claude`) |
| **Work tree** | Multiple agents editing the *same file* concurrently without conflicts | Configure git worktrees; Claude operates on isolated copies |
| **Single session** | Small, linear task with no parallelism needed | Just `claude` |

Cost scales the other way: single session < sub-agent < agent view < agent team. Agent teams burn the most tokens. Reserve them for high-value work.

**Sources:**
- https://code.claude.com/docs/en/sub-agents (verified 23-05-2026)
- https://code.claude.com/docs/en/cli-reference (verified 23-05-2026)

---

## Q63: How do I define an agent's responsibilities? Where do I write the role?

You write one or two sentences describing the role, and Claude generates the rest. Flow via `/agents`:

1. `/agents` -> Create new agent
2. "Generate with Claude" -> paste a one-line description like *"Churn-pattern analyst that reads survey responses and pulls out the top churn drivers with verbatim quotes, frequency tags, and severity tags."*
3. Pick tool permissions (default to **read-only** until you trust the agent)
4. Pick model (Sonnet for most; Opus for complex review)
5. Pick scope (project vs global)

Claude generates the full system prompt - rubric, non-negotiable rules, output format - from your one-liner. You can edit `.claude/agents/<agent>.md` afterwards.

Practical default: **read-only first**. Only grant write access after 2-3 iterations where the agent's output is reliable.

**Sources:**
- https://code.claude.com/docs/en/sub-agents (verified 23-05-2026)
- https://code.claude.com/docs/en/permissions (verified 23-05-2026)

---

## Q64: Can I share an agent with my team, or publish it as a plugin?

**Share via git, yes. Publish as a plugin, technically yes but not the same flow.**

To share:

- Agent file lives at `.claude/agents/<agent-name>.md` (project-scope) or `~/.claude/agents/<name>.md` (global).
- Commit the project-scope file to your repo. Teammates pull, and the agent is available locally.
- Agent teams that run on Anthropic's infrastructure (the experimental orchestration feature) **cannot** be shared this way - the orchestration runs on Anthropic's side, not in your repo.

For wider distribution, package the agent + any companion skills into a plugin and publish to a marketplace (`/plugin`). Most teams stop at "commit to repo" because plugin packaging is overkill for an internal tool.

**Sources:**
- https://code.claude.com/docs/en/sub-agents (verified 23-05-2026)
- https://code.claude.com/docs/en/plugins (verified 23-05-2026)

---

## Q65: How do skills relate to agents? Can one agent use multiple skills?

**Yes.** An agent is a persona. Skills are the verbs it knows. One agent can list any number of skills in its system prompt; it will invoke the right one based on the situation.

Example - a single `aman-pm.md` agent that lists:

- `write-prd`
- `feature-spec`
- `release-notes`
- `competitive-analysis`
- `user-interview-synthesis`

When you say "draft a PRD for Smart Follow-Up", the agent dispatches `write-prd`. When you say "summarize last week's interviews", it dispatches `user-interview-synthesis`.

**Caveat from the session:** stuffing every skill into one master agent bloats context. Better pattern - create role-scoped agents (`aman-prd.md`, `aman-stakeholder.md`, `aman-research.md`) that each carry a focused skill set. Start small, expand once each role's skills are stable.

**Sources:**
- https://code.claude.com/docs/en/skills (verified 23-05-2026)
- https://code.claude.com/docs/en/sub-agents (verified 23-05-2026)

---

## Q66: How do I track live token consumption? Can I put it in the status line?

- `/usage` shows current 5-hour and weekly window consumption.
- `/cost` shows session-level token + dollar usage.
- Status line - take a screenshot of any existing rich status line, paste it into Claude, and prompt *"create a similar status line for me with folder, model, branch, context %, 5h / weekly window usage, and PID"*. Claude generates the status line config; iterate on color, separator, order in plain English.

The status line is just a config string Claude can edit - no special command syntax to learn. Anything you can describe, you can add.

To remove the token-usage element later: *"remove the weekly window from my status line"*. Done in one prompt.

**Sources:**
- https://code.claude.com/docs/en/cli-reference (verified 23-05-2026)
- https://code.claude.com/docs/en/statusline (verified 23-05-2026)

---

## Q67: My Claude seems stuck or in a loop. What do I do?

Three-step recovery:

1. `Ctrl+C` to interrupt the current operation.
2. Type `continue` or *"retry the last action"* - the agent resumes from where it stopped.
3. If it's a write-to-file issue ("the write was rejected" / "no output produced"), prompt *"retry the write to `<file>`"* and it picks up.

If a sub-agent loop never terminates (Claude shows activity but no file ever lands), it's usually a silent stall. `Ctrl+C` + retry resolves it almost every time. Don't kill the whole session - you'll lose context.

For the specific Windows `/agents` JSON parse error seen this session, the workaround is: paste the description as plain text (`Ctrl+Shift+V` to strip newline formatting) or type it manually. If that fails, edit `.claude/agents/<name>.md` directly.

**Sources:**
- https://code.claude.com/docs/en/troubleshooting (verified 23-05-2026)

---

## Q68: What does `/feedback` do, and where does the GitHub issue actually appear?

`/feedback` files a bug report against Anthropic's Claude Code GitHub repo from inside your session. Flow:

1. Run `/feedback` in the terminal interface (not all CLI variants expose it - if missing, you're likely in a chat-only Claude session).
2. Describe the issue. You can also paste a screenshot if you open the resulting URL in a browser.
3. Submit. You get a **feedback ID** back.
4. Press Enter to open the GitHub issue page in your browser.

**Known oddity (observed 23-05-2026):** the feedback ID does not always surface under the **Issues** filter for your own GitHub account. The issue is logged on Anthropic's side regardless. Workarounds:

- Save the feedback ID locally for reference.
- Tag `@AnthropicAI` on X with the feedback ID if you need a faster response.
- Search for the ID in the Anthropic Claude Code GitHub repository's issues directly.

**Sources:**
- https://github.com/anthropics/claude-code (verified 23-05-2026)
- https://code.claude.com/docs/en/troubleshooting (verified 23-05-2026)

---

## Q69: How do I keep multiple Claude sessions organized across features?

**Pattern used in the session - PID-based session registry.** Each Claude session has a process ID. Register it against a feature name in a local file (`.claude/claude-sessions-registry.md`), so closing the terminal or restarting the machine doesn't lose the chat.

Workflow:

1. Open new terminal, start `claude`.
2. Note the PID (shown in the status line if configured).
3. Register via a small shell helper (`ccs "create-agent-task"`) that appends an entry to the registry file with PID + task description.
4. To resume after a terminal close: open registry, copy the PID-based resume command, paste in a new terminal. Claude reopens the same session with full history.

This is a **user-built convention**, not a built-in Claude Code feature. The host's setup is shareable - ask Claude to read `.claude/claude-sessions-registry.md` and replicate the `ccs` helper in your shell config.

**Sources:**
- https://code.claude.com/docs/en/cli-reference (verified 23-05-2026)

---

## Q70: What's "ReAct" and is it a Claude Code thing I need to learn?

**ReAct (Reason + Act)** is a generic LLM-agent design pattern from academic literature (Yao et al., 2022) where an agent alternates between reasoning about the next step and taking an action. It's a framing for *how* agents work, not a Claude Code feature.

- Claude Code's agents already follow a ReAct-style loop internally. You don't configure it.
- Third-party blogs may reference ReAct, ReWOO, Reflexion, etc. - useful conceptually, but **don't substitute them for the official Claude docs**.
- For Claude-specific patterns, anchor on `code.claude.com/docs` and `anthropic.com/engineering`. Third-party content is often outdated or inaccurate for Claude Code specifics.

**Bottom line:** read the official docs. ReAct is background reading, not a thing you have to implement.

**Sources:**
- https://www.anthropic.com/engineering/built-multi-agent-research-system (verified 23-05-2026)
- https://code.claude.com/docs/en/sub-agents (verified 23-05-2026)

---

# May 2026 - Session 6 Additions

New questions raised by the NextLeap Applied Generative AI Bootcamp cohort on 23-05-2026 during Session 6 (Multi-agent architectures, afternoon - agent view, worktrees, agent teams, MCP connectors). All URLs verified 24-05-2026.

---

## Q71: How do I open "agent view" and run several tasks in parallel? How do I stop one?

**Agent view** is the interface that shows every background task Claude Code is running, with status and elapsed time. You launch parallel work by asking Claude to run tasks concurrently, then watch them in agent view.

- Each task runs in its own context. The view shows which tasks are running, which are waiting on your input or permission, and which are done.
- To stop a single task, select it in the view and stop it - the others keep running.
- This is the right tool for **background long-runs** (a competitive scan, a feedback synthesis) where you want to keep working while they execute.

In the workshop, two tasks ran at once - a competitive-metrics refresh from `03-product-knowledge/competitive.md` and a churn-driver synthesis from `06-user-feedback/` - and one was stopped mid-run to demonstrate the control.

**Sources:**
- https://code.claude.com/docs/en/sub-agents (verified 24-05-2026)
- https://code.claude.com/docs/en/common-workflows (verified 24-05-2026)

---

## Q72: Why did Claude create extra branches/folders (worktrees) when I ran parallel agents?

A **Git worktree** is a second working copy of your repo on its own branch, sharing the same Git history. When tasks run in parallel and each may edit files, Claude isolates them in separate worktrees so they don't collide on the same files.

- After a parallel run you'll see new folders/branches - one per task.
- This lets two agents edit code concurrently without overwriting each other. You review and merge the branches afterward, like any Git workflow.
- Use worktrees specifically when concurrent tasks touch the **same files**. For independent read-only tasks you don't strictly need them, but agent view may still create them.

**Sources:**
- https://code.claude.com/docs/en/common-workflows (verified 24-05-2026)

---

## Q73: How do I turn on "agent teams"? It's not showing up by default.

Agent teams is an **experimental** feature, off by default. You enable it through `settings.json` and then restart Claude Code. In the session the flag used was `CLAUDE_CODE_EXPERIMENTAL_AGENT_TEAMS=1`.

Because experimental flags change between releases, **verify the exact key against the current settings docs before relying on it** - don't copy a flag name from memory.

- Edit `settings.json` (project- or user-level), add the experimental flag, restart Claude Code.
- If Claude blocks a shell command that edits its own settings (a self-modification guard), drag-and-drop `settings.json` into the conversation and ask Claude to edit the file directly.
- Treat the feature as exploratory, not production-grade; report bugs with `/feedback`.

**Sources:**
- https://code.claude.com/docs/en/settings (verified 24-05-2026)
- https://code.claude.com/docs/en/sub-agents (verified 24-05-2026)

---

## Q74: How do the agents in a team actually communicate with each other?

Through a **lead orchestrator**, not by talking peer-to-peer. The lead agent assigns each teammate a task, collects their written outputs, and decides the next step. In a multi-round run the lead feeds round-one outputs back into round-two prompts so each agent can respond to the others - but the routing always goes through the lead.

- Coordination is in natural-language prompts and summaries the lead composes, not a hidden JSON protocol you configure.
- The lead reads only the teammates' summaries, keeping its own context clean (the same pattern as sub-agents - see Q60, Q61).
- You can inspect the exact prompts the lead generates for each teammate with `Ctrl+O` in the terminal.

**Sources:**
- https://www.anthropic.com/engineering/built-multi-agent-research-system (verified 24-05-2026)
- https://code.claude.com/docs/en/sub-agents (verified 24-05-2026)

---

## Q75: Why can the Google Drive connector create files but not edit existing ones?

The Google Drive connector exposes a **read-and-create** tool set - copy, create, download, get metadata, get permissions, list recent, read, search - but no update/edit tool. So Claude can read your Drive and make new files, but it can't modify a file in place.

Practical workaround used in session: have Claude generate the content locally as Markdown, convert it (e.g. a small `md_to_docx` Python script), and upload it as a **new** file rather than editing the original.

Confluence's connector, by contrast, does support updating an existing page - so always **pull before you push**, or you risk overwriting a teammate's inline comments.

**Sources:**
- https://code.claude.com/docs/en/mcp (verified 24-05-2026)

---

## Q76: When should I build a custom skill instead of just using a raw MCP server?

Use a **custom skill with a small script** when the same transformation runs repeatedly and the raw MCP server would load a large tool surface (and many tokens) into context each time.

Concrete example from the session: pushing/pulling Confluence pages through the raw Confluence MCP loads all its tool definitions every run. The `confluence-to-md` / `md-to-confluence` skills wrap a Python script that does just the one job, so they cost far fewer tokens.

Rule of thumb:
- **One-off or genuinely interactive task** -> MCP server is fine.
- **Repeated, well-defined transformation** -> wrap it in a skill (`.claude/skills/<name>/`) with a script, commit it, reuse it.

**Sources:**
- https://code.claude.com/docs/en/mcp (verified 24-05-2026)
- https://code.claude.com/docs/en/slash-commands (verified 24-05-2026)

---

# May 2026 - Session 7 Additions

New questions raised by the NextLeap Applied Generative AI Bootcamp cohort on 24-05-2026 during Session 7 (Build Hours - building a multi-agent Property Finder end to end). All URLs verified 24-05-2026.

---

## Q77: What does `/init` do, and do I have to run it?

`/init` bootstraps a project for Claude Code. It scans the folder and creates a `CLAUDE.md` with a starting picture of the codebase; in a fresh project it can also scaffold a sensible folder structure based on what you tell it you're building.

- You don't *have* to run it - Claude works without it - but a project with a `CLAUDE.md` and a clear structure gives much richer output than a blank folder (see Q57).
- In the workshop, `/init` produced a hybrid layout: `docs/`, `src/`, `agents/`, `tests/`, and `.claude/` with `skills/` and `rules/`.
- Re-running `/init` later refreshes `CLAUDE.md` against the current state of the repo.

**Sources:**
- https://code.claude.com/docs/en/memory (verified 24-05-2026)
- https://code.claude.com/docs/en/slash-commands (verified 24-05-2026)

---

## Q78: What is the usage/insights report and how do I get it?

Claude Code can produce a usage report on how you've been working - message counts, lines created/removed, files touched, languages, session types, and peak hours - plus suggestions (in the session it surfaced the rubric-driven-refinement habit and offered a `CLAUDE.md` snippet to copy).

- For an individual usage report, generate it from the CLI as shown in the analytics/costs docs; run it periodically (monthly is plenty) to spot patterns.
- For **team-level** usage tracking, the Analytics dashboard is the official surface.
- Newcomers will see thin data at first - it's worth running once anyway to see the shape of the report.

**Sources:**
- https://code.claude.com/docs/en/analytics (verified 24-05-2026)
- https://code.claude.com/docs/en/costs (verified 24-05-2026)

---

## Q79: Plan mode vs Auto mode - what's the difference and how do I switch?

Both are interactive modes you cycle through with **`Shift+Tab`**:

- **Plan mode** - Claude investigates and proposes a plan *before* editing anything. It often spawns an explore sub-agent to map the project first. Best for any change touching several files.
- **Auto mode (auto-accept edits)** - Claude carries out steps without pausing for per-action approval. Faster, but you give up the per-step checkpoint.
- Default mode sits between them, asking permission for write actions.

Press `Shift+Tab` repeatedly to rotate through the modes; the current mode shows in the input bar. If you don't see the toggle, keep pressing - some builds show it only after the first action.

**Sources:**
- https://code.claude.com/docs/en/interactive-mode (verified 24-05-2026)
- https://code.claude.com/docs/en/common-workflows (verified 24-05-2026)

---

## Q80: How do I resume a Claude Code session after closing the terminal?

Claude Code persists sessions, so you can pick up where you left off:

- **`claude --continue`** resumes the most recent session in the current directory.
- **`claude --resume`** lets you choose a past session from a list.

The instructor's `ccs` ("Claude Code sessions") setup is a personal shell helper that registers a named session against its process ID so he can map sessions to features and reopen the right one - it's a convenience wrapper on top of the built-in resume, not a separate Claude feature. The built-in `--continue` / `--resume` flags are all you need to recover a session.

**Sources:**
- https://code.claude.com/docs/en/cli-reference (verified 24-05-2026)

---

## Q81: Where do global skills and CLAUDE.md live, and how do I create a global skill?

There are two levels:

- **Project-level:** `./.claude/` in the repo (skills in `./.claude/skills/`, plus the project `CLAUDE.md`). Shared with the team when you commit it.
- **User (global) level:** `~/.claude/` in your home directory (`~/.claude/skills/`, and a user `CLAUDE.md`). Available in every project, personal to you.

The `~` prefix is the tell: `~/.claude` is global, a bare `.claude` is the project's. On macOS, reveal the hidden `~/.claude` folder in Finder with `Command+Shift+.`.

To make a skill global, create it under `~/.claude/skills/<name>/` (or ask Claude to create it at both project and user level). To borrow a skill from another project, copy its folder into `~/.claude/skills/`.

**Sources:**
- https://code.claude.com/docs/en/memory (verified 24-05-2026)
- https://code.claude.com/docs/en/slash-commands (verified 24-05-2026)

---

## Q82: I selected Opus, but Claude used a cheaper model for a sub-task. Why?

That's expected. The model you pick is for the **main session**; when Claude spawns a sub-agent or sub-task it can route that work to a smaller, cheaper model when the task doesn't need the top model. A web-search or extraction step doesn't need Opus, so it may run on a Sonnet-class model to save tokens and time.

- The lead/main agent stays on your chosen model for the reasoning that matters; helpers get right-sized models.
- You can constrain models explicitly in configuration if you need to, but the default delegation is a cost optimization, not a bug.

**Sources:**
- https://code.claude.com/docs/en/model-config (verified 24-05-2026)
- https://code.claude.com/docs/en/sub-agents (verified 24-05-2026)

---

## Q83: How do I make sure my `.env` / API keys never get committed?

Keep secrets in a `.env` file and add `.env` to `.gitignore` so Git never stages it. State the rule in your project `CLAUDE.md` (e.g. "never commit `.env`; secrets stay local") so Claude respects it too, and commit a `.env.example` with placeholder keys instead of real values.

- Claude Code only writes inside the working folder and asks before write actions, but the durable guard is `.gitignore` + the explicit `CLAUDE.md` rule.
- For shared repos, anyone cloning adds their own keys to a local `.env`; the keys are never in the repo.

This is exactly how the Property Finder repo was shared: private repo, `.env` git-ignored, teammates add their Gemini and Google Maps keys after cloning.

**Sources:**
- https://code.claude.com/docs/en/settings (verified 24-05-2026)
- https://code.claude.com/docs/en/memory (verified 24-05-2026)

---

# July 2026 - Session 1 Additions

New questions raised by a new NextLeap Applied Generative AI Bootcamp cohort on 04-07-2026 during Session 1 (Claude Code Setup, morning). All URLs verified 05-07-2026.

---

## Q84: What's the difference between Claude Chat, Claude Cowork, and Claude Code?

**Short answer:** They are three separate surfaces with increasing capability. Chat is a plain conversational interface. Cowork has access to a local folder but not to skills, plugins, or MCP servers. Claude Code is the terminal-based tool with the full skill/plugin/MCP architecture, and it works inside any IDE (Antigravity, Cursor, VS Code) or a bare terminal.

- If a command like `/database` or a custom skill only responds inside a terminal running `claude`, that's the tell you're in Claude Code, not Cowork or Chat.
- The VS Code extension is a graphical wrapper around the same Claude Code CLI, so it supports most but not all CLI features (see Q90).
- An IDE's own built-in agent panel (e.g. Antigravity's Gemini-based agent) is a separate product from Claude Code, even when it can also call Claude models - see Q95.

**Sources:**
- https://code.claude.com/docs/en/skills (verified 05-07-2026)
- https://code.claude.com/docs/en/vs-code (verified 05-07-2026)

---

## Q85: Do I need Antigravity (or any specific IDE) to use Claude Code?

**Short answer:** No. Claude Code is a standalone CLI that works in any terminal or any IDE's integrated terminal - Antigravity, Cursor, VS Code, JetBrains, or a bare shell.

- Antigravity is a personal workflow preference (single-window layout: file explorer, file viewer, and the Claude Code terminal side by side), not a requirement.
- If your employer restricts installing new IDEs, you can still install the standalone Claude Code CLI and run `claude` in whatever terminal you already have access to.
- The VS Code extension is a separate, optional graphical layer on top of the same CLI; it does not require Antigravity either.

**Sources:**
- https://code.claude.com/docs/en/vs-code (verified 05-07-2026)

---

## Q86: I get "command not found: claude" (or "'claude' is not recognized") after installing on Windows. How do I fix it?

**Short answer:** The install succeeded but the install directory isn't on your PATH yet. Add `%USERPROFILE%\.local\bin` to your User PATH and open a new terminal.

In PowerShell:

```powershell
$currentPath = [Environment]::GetEnvironmentVariable('PATH', 'User')
[Environment]::SetEnvironmentVariable('PATH', "$currentPath;$env:USERPROFILE\.local\bin", 'User')
```

Then close and reopen the terminal and re-check with `claude --version`. This was the single most common install blocker in session - closing memory-heavy apps (extra Chrome tabs, the Claude desktop app) before installing also resolved several stalls, since Claude Code needs roughly 512 MB of free memory to install.

**Sources:**
- https://code.claude.com/docs/en/troubleshoot-install (verified 05-07-2026)
- https://code.claude.com/docs/en/troubleshooting (verified 05-07-2026)

---

## Q87: Can I use my company's shared Claude account instead of buying my own Pro subscription?

**Short answer:** Only if your company's policy explicitly allows it, and be aware a shared team account exposes your chat history to whoever else has access. For a workshop or personal exploration, a personal $20/month Pro subscription keeps your sessions private and is the safer default.

- A shared/team account means other members with access can see your conversation history and session data.
- If your company later approves a tool, you can simply cancel the personal subscription - there's no lock-in.

**Sources:**
- https://code.claude.com/docs/en/settings (verified 05-07-2026)

---

## Q88: What's the practical difference between Windows PowerShell and Command Prompt when installing Claude Code?

**Short answer:** Both can install Claude Code, but they use different installer commands and PATH mechanics, so copying a command meant for one shell into the other is the most common install failure.

- PowerShell: `irm https://claude.ai/install.ps1 | iex`
- Command Prompt (cmd.exe): `curl -fsSL https://claude.ai/install.cmd -o install.cmd && install.cmd && del install.cmd`
- Running the PowerShell command in cmd.exe fails with "'irm' is not recognized"; running the cmd.exe command in PowerShell fails on the `&&` operator or on curl being aliased to `Invoke-WebRequest`.
- If unsure which shell you're in, open PowerShell specifically from the Start menu (not "PowerShell (x86)") and use the PowerShell installer.

**Sources:**
- https://code.claude.com/docs/en/troubleshoot-install (verified 05-07-2026)

---

## Q89: What does `/plugins` do, and how do I pick which ones to install?

**Short answer:** `/plugins` opens an interactive picker where you toggle plugins with Space and install the selected set with `i`. Plugins bundle skills, agents, and MCP servers that aren't available in a plain chat model or a generic IDE agent.

- After installing, run `/reload` (or the reload-plugins command shown in the picker) to activate them in the current session.
- A reasonable starter set for a PM/product workshop: front-end design, superpowers (brainstorming), code-review, context7, skill-creator, code-simplifier, Playwright, Chrome DevTools, security guidance, and TypeScript - add Figma if you work in design.
- Plugins installed this way are available across any project you open with Claude Code, not just the one you were in when you installed them.

**Sources:**
- https://code.claude.com/docs/en/skills (verified 05-07-2026)

---

# July 2026 - Session 2 Additions

New questions raised by the same NextLeap Applied Generative AI Bootcamp cohort on 04-07-2026 during Session 2 (Skills, Plugins, and Practical Examples, afternoon). All URLs verified 05-07-2026.

---

## Q90: Why does the Claude Code terminal show more information (status line) than Cowork or the VS Code extension?

**Short answer:** The status line is a Claude Code CLI feature - a customizable bar that runs a shell script and can display model, effort level, context window usage, cost, git branch, and your 5-hour/7-day usage window. Cowork and the more limited surfaces don't expose this level of customization.

- Configure it under `/statusline` or in `settings.json`; the script receives session data as JSON on stdin and prints whatever you want shown.
- The VS Code extension shows an equivalent breakdown in its own Account & Usage dialog, but it isn't the same customizable status line.

**Sources:**
- https://code.claude.com/docs/en/statusline (verified 05-07-2026)
- https://code.claude.com/docs/en/vs-code (verified 05-07-2026)

---

## Q91: Should I save a new skill at the project level or the global level?

**Short answer:** Project level (`.claude/skills/`) if the skill only makes sense for that codebase; global level (`~/.claude/skills/`) if you want it available in every project. A common pattern is to keep a copy at both levels - project level for visibility inside that repo, global level so it follows you everywhere.

- A skill created at project scope will not show up in the `/` menu of a different project unless it's also copied to `~/.claude/skills/`.
- When copying a skill between projects, ask Claude to strip project-specific context and re-add context for the new project rather than reusing it verbatim.

**Sources:**
- https://code.claude.com/docs/en/skills (verified 05-07-2026)

---

## Q92: My skill file is getting long. When should I split content into a references/ folder?

**Short answer:** Keep the `SKILL.md` body itself short - long reference material (a scoring rubric, a research benchmark, a detailed template) should live in a `references/` file that the skill points to, since a skill's body loads only when it's invoked and long inline content costs context on every run.

- In the session's Competitor Page Audit skill, the scoring rubric and a sales-benchmark writeup were moved into separate `references/` files rather than bloating the main skill.
- If a skill keeps growing past what feels manageable, ask Claude directly to split it - it will extract detail into references and leave the procedure in the main file.

**Sources:**
- https://code.claude.com/docs/en/skills (verified 05-07-2026)

---

## Q93: I want a skill for an open-ended task like brainstorming. Should I build it right away?

**Short answer:** Not immediately. Open-ended, judgment-heavy tasks don't compress well into a fixed skill on the first try. Instead, work the problem in a dedicated chat for a while and have Claude maintain a `learnings.md` file of the decisions, corrections, and paths you actually took. After a month or two of real usage, that file has enough context to generate a genuinely useful skill or agent.

- Treat the eventual skill or agent like a new hire: it only works well once it has the same context a person would need to make the same calls you do.
- A skill built without that accumulated context tends to produce generic, low-value output on a task that's inherently about judgment rather than a fixed procedure.

**Sources:**
- https://code.claude.com/docs/en/memory (verified 05-07-2026)
- https://code.claude.com/docs/en/skills (verified 05-07-2026)

---

## Q94: What is "effort level" in Claude Code, and how does it affect cost?

**Short answer:** Effort level controls how much extended-thinking budget a model uses per request. Medium effort is the default recommendation for most day-to-day work; higher effort levels (high, very high) spend more thinking tokens and cost more, and are best reserved for genuinely complex reasoning or planning tasks.

- Switch model and effort with `/model`, or change effort alone with `/effort`.
- Combine with model choice for cost control: Sonnet at medium effort covers most day-to-day work; reserve Opus and higher effort for complex architectural or multi-step reasoning tasks.

**Sources:**
- https://code.claude.com/docs/en/model-config (verified 05-07-2026)
- https://code.claude.com/docs/en/costs (verified 05-07-2026)

---

## Q95: Why does Antigravity's built-in agent panel behave differently from Claude Code, even though both can use Claude models?

**Short answer:** They're different products with different tool access, not just different chat windows. Antigravity's native agent panel is Antigravity's own agent (it can call several model providers, including Claude models), while Claude Code is Anthropic's own CLI with its own skill, plugin, and MCP architecture. Selecting a Claude model inside Antigravity's panel does not give you Claude Code's skills - you still need to run `claude` in a terminal to access those.

- A skill invoked with `/skill-name` only works inside an actual Claude Code session (terminal or the Claude Code VS Code extension), not inside a generic IDE agent panel, even one powered by the same underlying model.
- This is why the workshop repeatedly moves the Claude Code terminal into the IDE's secondary sidebar rather than relying on the IDE's own agent panel.

**Sources:**
- https://code.claude.com/docs/en/vs-code (verified 05-07-2026)
- https://code.claude.com/docs/en/skills (verified 05-07-2026)

---

# July 2026 - Session 3 Additions

New questions raised by the same NextLeap Applied Generative AI Bootcamp cohort on 05-07-2026 during Session 3 (Skills Creation and Product Management Frameworks, morning). All URLs verified 05-07-2026.

---

## Q96: When should something become a Claude Code skill versus just a one-off prompt?

**Short answer:** Build a skill only when the output is stable and repeatable, a defined format you produce the same way each time. If the task needs fresh logical judgment on every run (open-ended strategy, brainstorming), it is not a good skill yet.

- A skill captures a repeatable workflow you can invoke in one shot; it does not capture a decision that changes shape every time.
- For judgment-heavy tasks, work the problem in a chat first, accumulate real examples over time, then generate a skill once the pattern is stable.

**Sources:**
- https://code.claude.com/docs/en/skills (verified 05-07-2026)

---

## Q97: How long should a SKILL.md file be, and what do I do when it gets too long?

**Short answer:** Keep the body in the 100-200 line range. When it overflows, do not split into multiple skills, move the long material (rubrics, benchmarks, templates) into a `references/` subfolder that the skill points to.

- The skill body loads into context when invoked, so long inline content costs tokens on every run; reference files are pulled only when needed.
- If a skill keeps growing, ask Claude to improve or refactor it and it will extract detail into `references/` while leaving the procedure in the main file.

**Sources:**
- https://code.claude.com/docs/en/skills (verified 05-07-2026)

---

## Q98: How do I log improvement ideas for a skill without bloating its context?

**Short answer:** Keep a separate feedback file (for example `improvements.md`) that is deliberately NOT referenced inside `SKILL.md`, so it never loads into context automatically. Add as much detail as possible per entry, including a screenshot of the exact iteration you are critiquing.

- Because the file is not linked from the skill, it costs nothing at runtime but stays available when you next sit down to improve the skill.
- The skill cannot automatically know which past run your feedback refers to, so you must supply that context (screenshot, link, specific description) yourself.

**Sources:**
- https://code.claude.com/docs/en/skills (verified 05-07-2026)

---

## Q99: What is the difference between a global-level and a project-level skill?

**Short answer:** Global skills (`~/.claude/skills/`) are reusable across every project, general capabilities like email drafting, an OKR writer, or a presentation builder. Project-level skills (`.claude/skills/`) are specific to one project's workflows, templates, and conventions.

- A project skill will not appear in another project's `/` menu unless it is also copied to the global folder.
- When moving a skill between projects, strip the old project's context and re-add context for the new one rather than reusing it verbatim.

**Sources:**
- https://code.claude.com/docs/en/skills (verified 05-07-2026)

---

## Q100: How do I invoke a skill that needs a file input, like an Excel dashboard skill?

**Short answer:** Invoke the skill by name and let it prompt you. A well-written skill asks for the input it needs (the file, the dataset), so you do not have to pre-format the request; you provide the file when it asks.

- If the skill is defined to expect a file, it will request one rather than failing silently.
- The same skill can produce a downstream artifact such as a standalone HTML dashboard from the file you hand it.

**Sources:**
- https://code.claude.com/docs/en/skills (verified 05-07-2026)

---

## Q101: What is an "embedded independent HTML file" and why does it matter for sharing dashboards?

**Short answer:** It is a single HTML file with all CSS and JavaScript inlined, so it does not depend on separate files or a local server. That makes it shareable over WhatsApp or email, and anyone can open it directly.

- The failure mode to avoid is a file that points at a localhost path or external assets, it will only work on the machine that generated it.
- When building a dashboard skill, specify embedded independent HTML as the output so the result is portable by default.

**Sources:**
- https://code.claude.com/docs/en/skills (verified 05-07-2026)

---

## Q102: Should I base a new skill on a known industry framework when one exists?

**Short answer:** Yes. Where an established framework exists (from books or standard practice, like Amazon's PR-FAQ), build the skill around that official framework rather than inventing an ad hoc structure. It makes the skill more robust and the output more credible.

- In the session, the PR-FAQ skill was built by having Claude research the official working-backwards framework first, then generate the skill from it.
- Grounding a skill in a named framework also gives you validated reference material to cite in the output.

**Sources:**
- https://code.claude.com/docs/en/skills (verified 05-07-2026)

---

## Q103: What does the PR-FAQ skill do?

**Short answer:** It applies Amazon's working-backwards Press Release / FAQ method to a feature decision. It interviews you (customer problem, alternatives, economics), then returns a build or do-not-build verdict plus a full PR-FAQ document, so you talk yourself into or out of the feature through the questions.

- The value is the structured interrogation: after answering the skill's questions you are usually convinced one way or the other.
- Output can be the interview and verdict, the full PR-FAQ document, or both.

**Sources:**
- https://code.claude.com/docs/en/skills (verified 05-07-2026)

---

## Q104: How do I resume a specific Claude Code session after I have closed the terminal?

**Short answer:** Use the built-in resume flow to reopen a prior conversation with its full context instead of starting blank. Claude Code supports continuing the most recent session or picking a past one, and the workshop wraps this in a named session registry (`ccs`) for convenience.

- From the CLI, `claude --continue` resumes the most recent conversation and `claude --resume` lets you pick a specific past session.
- The workshop's `ccs add` / `ccs open` commands are a thin naming layer on top of this so long-running threads can be reopened by name.

**Sources:**
- https://code.claude.com/docs/en/cli-reference (verified 05-07-2026)
- https://code.claude.com/docs/en/common-workflows (verified 05-07-2026)

---

## Q105: How does Claude's memory system work, and what is a good example use?

**Short answer:** Memory stores facts Claude should carry across conversations, at either project scope or global scope, indexed by a `MEMORY.md` file. You create a memory by telling Claude to remember something; it writes the fact and updates the index.

- Project memory applies only to that project (for example, "save outputs under the current month's cohort folder"); global memory applies across every project on your account.
- Examples shown: disambiguating two people with the same first name, "use the Antigravity IDE, not VS Code," and enforcing DD-MM-YYYY dates.

**Sources:**
- https://code.claude.com/docs/en/memory (verified 05-07-2026)

---

# July 2026 - Session 4 Additions

New questions raised by the same NextLeap Applied Generative AI Bootcamp cohort on 05-07-2026 during Session 4 (Building and Using Agents, afternoon). All URLs verified 05-07-2026.

---

## Q106: What is the difference between project-level and global-level memory?

**Short answer:** Project memory lives with one project and only applies there; global memory is tied to your Claude account and applies across every project you open. Same idea as skills, different scope.

- Project example: the rule that generated outputs go under the current month's cohort folder in this repo.
- Global example: the rule that "create a session / ccs" means adding a row to the session registry, which should hold in any project.

**Sources:**
- https://code.claude.com/docs/en/memory (verified 05-07-2026)

---

## Q107: Can a skill directly reference a saved memory?

**Short answer:** No. A skill cannot invoke or read a memory. If a skill needs persistent context, put that context in a `references/` file inside the skill folder instead.

- Memory is for Claude's project-level or global understanding, not for a skill's runtime.
- Reference files are the supported way to give a skill durable background it can pull when it runs.

**Sources:**
- https://code.claude.com/docs/en/skills (verified 05-07-2026)
- https://code.claude.com/docs/en/memory (verified 05-07-2026)

---

## Q108: What is the difference between an agent and a skill?

**Short answer:** An agent is a persona, the "who," with its own instructions, tools, and model. A skill is a capability, the "what," that can be invoked. Consider the agent as yourself and skills as what skills you have.

- One agent can invoke several skills to do its job, the way a person uses several abilities.
- You build an agent when you want a role that decides and acts; you build a skill when you want a repeatable capability.

**Sources:**
- https://code.claude.com/docs/en/sub-agents (verified 05-07-2026)
- https://code.claude.com/docs/en/skills (verified 05-07-2026)

---

## Q109: Are agents project-level or global, and can I reuse one across projects?

**Short answer:** Agents default to project level, stored in `.claude/agents/`. To reuse one in another project, copy its `.md` file (and any associated agent-memory file), or create the agent at the global level so it follows you everywhere.

- The agent's filename is the agent name itself; there is no fixed filename like `SKILL.md`.
- Copying the definition carries the persona; copy its memory file too if it has accumulated context you want to keep.

**Sources:**
- https://code.claude.com/docs/en/sub-agents (verified 05-07-2026)

---

## Q110: Why not bundle every skill into one big agent?

**Short answer:** A mega-agent loads all its skills and instructions into context on every invocation, which burns tokens fast. Build category-specific agents first (documentation, research, review), then consolidate only once the pattern is proven.

- More skills in one agent means more context cost per call, even for a request that needs only one of them.
- Narrow agents are cheaper to run and easier to reason about; a router agent can sit in front of them if you need one entry point.

**Sources:**
- https://code.claude.com/docs/en/sub-agents (verified 05-07-2026)

---

## Q111: How do I see what Claude is doing behind the scenes while it works?

**Short answer:** Press Control+O to expand the live view of Claude's plan and the commands and permissions it is working through. It is a useful window into the reasoning, not just the final output.

- This is how the session showed plan mode, the exit-plan step, and the write-to-outputs-only permission for a new agent.
- Watching the backend plan is a fast way to learn how Claude decomposes a task.

**Sources:**
- https://code.claude.com/docs/en/interactive-mode (verified 05-07-2026)

---

## Q112: Does Claude Code auto-select the best model for each prompt?

**Short answer:** No. There is no auto-mode that analyzes your prompt and picks the best model per request the way some IDE assistants do. The model you select in the terminal is the one used; you steer cost by choosing the model and effort yourself.

- Set model and effort with `/model` (and effort alone with `/effort`); guide defaults in CLAUDE.md if you want a standing preference.
- Note that subagents commonly default to Sonnet even when the top-level session is on Opus, unless you specify otherwise.

**Sources:**
- https://code.claude.com/docs/en/model-config (verified 05-07-2026)
- https://code.claude.com/docs/en/sub-agents (verified 05-07-2026)

---

## Q113: What is the routing (orchestrator) agent pattern?

**Short answer:** A dispatcher agent classifies an incoming request into one of several categories and forwards it, verbatim, to the matching specialist agent, without answering the request itself. In the session, pm-request-router sorted a request into PRD, COMPETITOR, CHURN, or UNCLEAR and dispatched to prd-drafter, competitor-snapshot, or churn-diagnoser.

- Giving the router only the ability to dispatch (not to read or write) keeps it from doing a specialist's job.
- For an unclear request it asks one clarifying question rather than guessing a category.

**Sources:**
- https://code.claude.com/docs/en/sub-agents (verified 05-07-2026)

---

## Q114: How do I connect a third-party tool that has no existing MCP server or connector?

**Short answer:** Check first for a genuinely official MCP server (verify it is from the vendor, not an unverified community fork). If none exists, use an API token for the integration. If neither exists, the integration is not currently possible.

- Always cross-check an MCP server's provenance before trusting it, an unofficial server can expose you to risk.
- For a single integration, an API token is often lighter than an MCP server, which loads its full tool list into context each session.

**Sources:**
- https://code.claude.com/docs/en/mcp (verified 05-07-2026)

---

## Q115: How should I roll out a new categorization or triage agent safely?

**Short answer:** Do not let it act on live systems on day one. Run it write-only to a local review file first (listing issues and who they would be assigned to), check its accuracy, then let it act once you trust it. Log every misclassification back as guidance so it improves.

- Feed the agent examples of how you actually work (past review comments, prior triage decisions) rather than hand-writing exhaustive instructions.
- This staged approach is what makes an automated PR-triage or ticket-routing agent trustworthy before it touches real tickets.

**Sources:**
- https://code.claude.com/docs/en/sub-agents (verified 05-07-2026)

---

## Q116: What is the token budget in Claude Code, and when does it reset?

**Short answer:** Usage counts against a large token budget shown in the status line, and it resets on rolling windows, a 5-hour window and a weekly window, rather than a single daily reset. Watch the status line to see how much of each window remains.

- Effort level and model choice are your main levers on how fast you consume the budget; medium effort and Sonnet cover most day-to-day work.
- Two people running similar prompts can consume very different amounts, often because accumulated project memory changes how much searching Claude does per task.

**Sources:**
- https://code.claude.com/docs/en/costs (verified 05-07-2026)
- https://code.claude.com/docs/en/statusline (verified 05-07-2026)

---

# July 2026 - Session 5 Additions

New questions raised by the same NextLeap Applied Generative AI Bootcamp cohort on 11-07-2026 during Session 5 (Workflows, Routines, and Product Automation). All URLs verified 11-07-2026.

---

## Q117: What is the `/loop` command, and how does it work as a cron-like scheduler?

**Short answer:** `/loop` re-runs a prompt on an interval while your session stays open, so it behaves like a lightweight cron. Both the interval and the prompt are optional, and you can pass a skill as the prompt so it re-runs each iteration.

- Example: `/loop 20m /review-pr 1234` re-runs that skill every 20 minutes; omit the interval and Claude self-paces.
- Practical use from the session: point a data-filling skill at an Excel of clients and loop it hourly to populate each row unattended (your machine must stay on).
- For scheduling that survives a closed laptop, use routines instead (Q119), which run on Anthropic-managed cloud infrastructure.

**Sources:**
- https://code.claude.com/docs/en/scheduled-tasks (verified 11-07-2026)
- https://code.claude.com/docs/en/slash-commands (verified 11-07-2026)

---

## Q118: What are dynamic workflows and the `/workflow` command, and how are they different from just prompting?

**Short answer:** A workflow moves the orchestration from Claude's context into a script. Instead of Claude deciding turn by turn what to spawn, a workflow script holds the loop, the branching, and the intermediate results itself, so your context holds only the final answer. You invoke and manage them with `/workflow` and `/workflows`.

- Workflows run in the background, so the session stays responsive while agents work; run `/workflows` to list running and completed ones and open a progress view.
- In the session, a workflow prompt named which agents to use (senior QA, senior software engineer, product manager, product designer) and Claude generated a `product-audit.js` file; next time you just say "continue this workflow."
- Workflows are token-heavy because they can spawn many agents and sub-agents; use them when you have the budget and a well-defined context.

**Sources:**
- https://code.claude.com/docs/en/workflows (verified 11-07-2026)
- https://code.claude.com/docs/en/sub-agents (verified 11-07-2026)

---

## Q119: What are routines, and how many can I schedule on my plan?

**Short answer:** A routine is a saved Claude Code configuration (a prompt, one or more repositories, and a set of connectors) that runs automatically on a schedule, on an API trigger, or in reaction to GitHub events. Routines execute on Anthropic-managed cloud infrastructure, so they keep working when your laptop is closed.

- Session example: a daily 7:00 AM digest of new Anthropic and Claude Code releases, running since mid-June.
- The number of routines you can run depends on your plan tier; check the routines documentation and your account for the current limit rather than assuming a fixed number.
- Good second use: a routine that tracks a competitor's changes and DMs you a summary.

**Sources:**
- https://code.claude.com/docs/en/routines (verified 11-07-2026)
- https://code.claude.com/docs/en/scheduled-tasks (verified 11-07-2026)

---

## Q120: What is the parallelization (fan-out) agent pattern?

**Short answer:** Dispatch several workers at once, each reading a different source, then run a second step that combines and ranks their results. In the session, three general-purpose workers read user interviews, the Q1 survey, and churn/company files in parallel, then a step-two pass ranked issues that appeared in two or three sources.

- The key difference from prompt chaining is that the workers run at the same time, not one after another, so the read is faster.
- Give each worker a tight brief (read exactly these files, return the top five issues with title, one-line description, and source file) so the outputs are easy to merge.
- The merge step is where you find corroboration, an issue in two or three sources is a stronger signal than one that appears once.

**Sources:**
- https://code.claude.com/docs/en/sub-agents (verified 11-07-2026)
- https://code.claude.com/docs/en/common-workflows (verified 11-07-2026)

---

## Q121: How do I decide between a skill, an agent, and a workflow?

**Short answer:** Start with a skill (one repeatable capability). Build an agent when you need a persona that calls several skills end to end. Use a workflow when you want those agents to loop automatically and you have the token budget.

- Skill: a single job you do repeatedly, like drafting a spec or filling a data sheet.
- Agent: a role that decides and acts, invoking one or more skills, for example a PM agent that creates a spec, gets it reviewed, and updates it.
- Workflow: the whole team looping (build, test, synthesize, repeat), best run when you have time and tokens to spare.

**Sources:**
- https://code.claude.com/docs/en/skills (verified 11-07-2026)
- https://code.claude.com/docs/en/sub-agents (verified 11-07-2026)
- https://code.claude.com/docs/en/workflows (verified 11-07-2026)

---

## Q122: What should I do when a sub-agent seems stuck or frozen?

**Short answer:** Do not kill the session. Send a short prompt like "are you stuck?" to nudge it to continue or report its state. If the timestamp keeps moving but no tokens are being consumed, your request is queued behind load, not dead.

- Killing and restarting loses the work in progress; a nudge is cheaper and usually enough.
- If it is genuinely stalled, check the status page (Q123) for an outage before assuming it is your setup.
- Agent view (`/agents` view) helps you see what multiple agents and sub-agents are doing when a large task spawns many of them.

**Sources:**
- https://code.claude.com/docs/en/troubleshooting (verified 11-07-2026)
- https://code.claude.com/docs/en/agent-view (verified 11-07-2026)

---

## Q123: Where do I check whether Claude or Claude Code is having an outage?

**Short answer:** Use the official status page at https://status.claude.com. It lists uptime and incidents for the models and Claude Code, so you can tell a real outage from a problem on your end.

- The session referenced a partial outage on 7 July and errors around July 10, both posted there.
- Check the status page first when a task appears frozen but you have already nudged it and it still will not move.

**Sources:**
- https://status.claude.com/ (verified 11-07-2026)
- https://code.claude.com/docs/en/troubleshooting (verified 11-07-2026)

---

## Q124: Why did a workflow report using 30+ agents when I only built four?

**Short answer:** Your four agents are the named roles you defined. When a task is large, each of those agents can spawn its own sub-agents to parallelize the work, which is why a run can show 22, 27, or 33 agents in total.

- The four roles (for example QA, engineer, PM, designer) are the orchestration; the extra agents are sub-agents doing the work in parallel across many files or personas.
- You can steer this by prompting "using sub-agents, review these documents" and even naming how many, rather than letting Claude decide.
- More sub-agents means more tokens, so scope the task if cost matters.

**Sources:**
- https://code.claude.com/docs/en/sub-agents (verified 11-07-2026)
- https://code.claude.com/docs/en/workflows (verified 11-07-2026)

---

## Q125: Can Claude Code build an end-to-end product, and how?

**Short answer:** Yes, but through spec-driven development, not a single prompt. Brainstorm the problem, the users, and the plan with Claude first, and do not start building until you are confident in that plan. Then proceed step by step, the same way you would without AI.

- The discipline is the same product process you already follow; the agents do the execution instead of humans.
- Feed the project rich context (personas, prior feedback, engineering review patterns) as Markdown files so the output needs less correction.
- Session examples built this way included an HRMS, Property Finder, a job-search tool, and MeetScribe.

**Sources:**
- https://code.claude.com/docs/en/common-workflows (verified 11-07-2026)
- https://code.claude.com/docs/en/skills (verified 11-07-2026)

---

## Q126: How do I create and use user personas in Claude Code?

**Short answer:** Personas are not a Claude feature; you create them as a file. Feed Claude your interview or survey data (for example "we ran 50 interviews and users said this") and ask it to produce a `personas.md`. Then reference that file to drive per-persona decisions.

- Once you have personas, you can run AB tests per persona, for example enabling a new feature only for the persona that uses that area most, to get fast, relevant feedback.
- Keep personas grounded in real data (database events, NPS, interviews), not assumptions.
- The same file becomes reusable context for future features and agents.

**Sources:**
- https://code.claude.com/docs/en/common-workflows (verified 11-07-2026)
- https://code.claude.com/docs/en/skills (verified 11-07-2026)

---

## Q127: How do I connect a product analytics tool like Mixpanel to Claude Code?

**Short answer:** Use a connector or MCP server for the tool if an official one exists, then query it in natural language. First make sure your product logs the events you care about; without event data there is nothing for the tool to analyze.

- Connectors exist for several analytics tools (the session named Mixpanel, Amplitude, Pendo, and PostHog); always confirm a server is official before trusting it.
- If no MCP server exists (Google Analytics was cited as an example without one), export the data and feed it to Claude directly.
- Caveat raised in the session: session-recording tools like Microsoft Clarity can consume a lot of tokens and may not return enriched, conclusive data, so test before relying on them.

**Sources:**
- https://code.claude.com/docs/en/mcp (verified 11-07-2026)

---

## Q128: Why do workflows, sub-agents, and recording summaries consume so many tokens, and how do I control cost?

**Short answer:** Cost scales with how much content is read and how many agents run. Workflows spawn many sub-agents, and summarizing large inputs like session recordings reads a lot of tokens. Your main levers are model choice, effort level, and scoping the task.

- Watch usage in the status line, and remember the budget resets on rolling windows (a 5-hour window and a weekly window), not a single daily reset.
- Prefer Sonnet and medium effort for routine work; reserve the largest models for the hardest reasoning.
- Scope inputs (fewer files per agent, narrower tasks) rather than pointing a workflow at an entire codebase when you do not need to.

**Sources:**
- https://code.claude.com/docs/en/costs (verified 11-07-2026)
- https://code.claude.com/docs/en/sub-agents (verified 11-07-2026)

---

## Q129: How do I generate product or feature videos from Claude Code?

**Short answer:** Install a video plugin or skill, then describe the video you want. In the session, installing the HyperFrames skill added an `agents.md` and around 20 video skills (product launch, website-to-video, motion graphics, and others), and a product-launch-video workflow crawled a live site for real brand assets.

- Voiceover uses a third-party text-to-speech key (11 Labs in the session), stored in the project's `.env` file; the skill scripts run locally and do not themselves call an AI model for the video assembly.
- Add an eval/checklist file so the agent self-reviews the output (for example audio-video sync) before sharing the final cut, and let that checklist improve with each video.
- Install only official or clearly first-party plugins and skills, and review what an install adds before running it.

**Sources:**
- https://code.claude.com/docs/en/plugins (verified 11-07-2026)
- https://code.claude.com/docs/en/skills (verified 11-07-2026)

---

# July 2026 - Session 6 Additions

New questions raised by the same NextLeap Applied Generative AI Bootcamp cohort on 11-07-2026 during Session 6 (Video, Commands, Hooks, and Session Management, afternoon). All URLs verified 11-07-2026.

---

## Q130: How do I control the length, language, and captions of a generated video?

**Short answer:** Set them in your prompt. Ask for a specific length (for example one minute), name the audio language, and say whether you want captions; the video skill and its voice provider handle the rest. Give it a screenshot plus a rough user-journey script for the best result.

- Voice comes from a third-party text-to-speech provider (11 Labs in the session); pick a language and paste a specific voice ID copied from that provider to lock the voice.
- Captions are optional; you can regenerate a cleaner cut without them if the captioned version looks busy.
- Treat it like non-AI video work: draft and review the script first, then render.

**Sources:**
- https://code.claude.com/docs/en/skills (verified 11-07-2026)
- https://code.claude.com/docs/en/plugins (verified 11-07-2026)

---

## Q131: What is the `/loop` command good for, and what does it depend on?

**Short answer:** `/loop` re-runs a prompt on an interval so a long task keeps going unattended. A common use is recovering from transient errors: loop every 15 minutes to send "continue" until a set time so an overnight build finishes on its own. Its one dependency is that your machine must stay on.

- Other examples: email your open Jira tickets at 8:00 AM daily, or send a scrum digest to stakeholders every morning.
- Keep your display set to always-on so the machine does not sleep mid-loop.
- If you need it to run when your laptop is closed, use a routine (Q132) instead.

**Sources:**
- https://code.claude.com/docs/en/scheduled-tasks (verified 11-07-2026)

---

## Q132: Why would I use a routine instead of `/loop` if I can already schedule things?

**Short answer:** A routine runs on Anthropic's cloud infrastructure, so it works when your laptop is off, but it is capped by plan (roughly 5 per day on Pro and 15 per day on Max). `/loop` has no such cap but depends on your machine staying on. Choose by whether you need cloud independence or unlimited local runs.

- The routine cap exists because it consumes Anthropic's infrastructure, not your machine.
- Routines can use connectors; note a limitation raised in the session, the Gmail connector creates a draft rather than sending, so Slack was used for digests.

**Sources:**
- https://code.claude.com/docs/en/routines (verified 11-07-2026)
- https://code.claude.com/docs/en/scheduled-tasks (verified 11-07-2026)

---

## Q133: What is plan mode, and how do I toggle it?

**Short answer:** Plan mode makes Claude draft a reviewable plan before it acts, which you approve before execution. Use it for any complex task with multiple dependencies. Toggle modes with Shift+Tab rather than typing a slash command.

- Reviewing the plan first catches a wrong approach before tokens are spent building it.
- Shift+Tab cycles through the available modes, shown at the bottom of the terminal.

**Sources:**
- https://code.claude.com/docs/en/interactive-mode (verified 11-07-2026)

---

## Q134: How do I get a report analyzing my past Claude Code sessions?

**Short answer:** Run the insights bundled skill. It reads your saved session transcripts and produces an HTML report of what you did, what went well, what to improve, and suggested CLAUDE.md additions. It is a retro for your Claude Code usage; run it monthly.

- In the session it covered 860 messages across 86 sessions and flagged recurring issues (stale MCP, missing Python packages, unverified URLs) plus concrete config suggestions.
- It works because every session is saved continuously to local transcript files (see Q135).

**Sources:**
- https://code.claude.com/docs/en/sessions (verified 11-07-2026)
- https://code.claude.com/docs/en/skills (verified 11-07-2026)

---

## Q135: Where are my Claude Code sessions stored, and how do I stop them being deleted after 30 days?

**Short answer:** Sessions are saved as JSONL transcript files under your global `.claude` directory (created when you installed Claude Code), grouped by project. By default they are cleaned up after 30 days. Set `cleanupPeriodDays` in your global `settings.json` to keep them longer.

- Aman set `cleanupPeriodDays` to 3650 (ten years) so nothing is auto-deleted.
- The same global `.claude` folder holds your global skills and memory, so back it up (or copy it) when moving machines; deleting it removes those skills.

**Sources:**
- https://code.claude.com/docs/en/settings (verified 11-07-2026)
- https://code.claude.com/docs/en/sessions (verified 11-07-2026)

---

## Q136: What do `/compact` and `/clear` do to my context window?

**Short answer:** `/compact` summarizes the conversation so far and keeps only that summary, freeing up context while retaining the gist. `/clear` wipes the conversation entirely and starts fresh. Use compact when you are running low on the context window but still need continuity.

- The context window is large (shown as a percentage remaining in the session); compact when the used portion starts crowding out room to work.
- Clear is the harder reset for when you are switching to an unrelated task.

**Sources:**
- https://code.claude.com/docs/en/costs (verified 11-07-2026)
- https://code.claude.com/docs/en/interactive-mode (verified 11-07-2026)

---

## Q137: What are the ways to give Claude persistent memory, and how do I add a quick one?

**Short answer:** There are three places: CLAUDE.md, the project memory file, and a rules file referenced from CLAUDE.md. For a rule that must not be missed, add it in more than one place. To add a quick memory, start a message with `#` and Claude will save it.

- Keep CLAUDE.md lean (roughly under 200 lines); if it grows too large it eats the context window and stops being fully effective.
- Memories are sometimes not recalled if a request is not specific, which is why duplicating a critical rule into both memory and a referenced rules file is safer.

**Sources:**
- https://code.claude.com/docs/en/memory (verified 11-07-2026)

---

## Q138: How do I set up a hook that auto-updates my docs when code changes?

**Short answer:** Use a PostToolUse hook in `settings.json` that fires after a turn changes source files, then runs a cheap `claude -p` pass to refresh CLAUDE.md and README.md from the git diff. This keeps docs from going stale without you remembering to update them.

- Hooks fire on events like PreToolUse and PostToolUse; doc-refresh belongs on PostToolUse, after the edits land.
- Removing the hook config (or the hook file) stops it, so it is easy to turn off.

**Sources:**
- https://code.claude.com/docs/en/hooks (verified 11-07-2026)

---

## Q139: How do I connect a design tool like Google Stitch to Claude Code via MCP?

**Short answer:** Add the tool's MCP server (Stitch provides one) using its setup snippet for your client, authenticate, and then generate designs in natural language. Stitch returns a full design-token system (primary, secondary, neutral, headline, body, label) you can apply to a page.

- Confirm the server is the official one before adding it, and check whether it needs an API token or subscription.
- The same MCP approach works for other design and analytics tools; the design tokens come from the server, not from Claude inventing them.

**Sources:**
- https://code.claude.com/docs/en/mcp (verified 11-07-2026)

---

## Q140: What is the difference between sub-agent-driven and inline execution, and how do I reduce token usage?

**Short answer:** Sub-agent-driven execution runs work in parallel across multiple strategies and burns far more tokens; inline execution runs steps one by one, slower but cheaper for the same outcome. To control cost, tell Claude "do not use sub agents," use Sonnet for any sub-agents, and keep effort at medium.

- The outcome is usually the same; the trade-off is speed versus token spend.
- To feel the difference, run the same task in two folders, one sub-agent-driven and one inline, and compare tokens and time.
- If you built a skill with sub-agents, it will not force sub-agents later unless you ask; specify inline when you invoke it to stay cheap.

**Sources:**
- https://code.claude.com/docs/en/sub-agents (verified 11-07-2026)
- https://code.claude.com/docs/en/costs (verified 11-07-2026)

---

## Q141: How do I enable Shift+Enter for multiline input in my terminal?

**Short answer:** Run the `/terminal-setup` command, which configures your terminal (including the Shift+Enter key binding) for Claude Code. After that you can type multi-line prompts with Shift+Enter.

- This is part of general terminal configuration for Claude Code and is a one-time setup per terminal.

**Sources:**
- https://code.claude.com/docs/en/terminal-config (verified 11-07-2026)

---

# July 2026 - Session 7 Additions

New questions raised by the same NextLeap Applied Generative AI Bootcamp cohort on 12-07-2026 during Session 7 (Build Hours, Shopping Assistant MVP). All URLs verified 12-07-2026.

---

## Q142: How do I avoid doing the work twice between a Claude prototype and Figma?

**Short answer:** Give Claude your Figma context (component links and guidelines) so it prototypes in your design system, then import the generated HTML into Figma so only a small share of work remains there. Connect Figma through its MCP server to make this two-way.

- Feed Claude the Figma links so it can build a UX zone that matches your fonts, components, and system, then iterate until nothing on Figma is missing from the UX zone.
- A Figma developer or company account is needed because Figma restricts MCP calls on free accounts.
- The point is the same as everywhere: build the design-system context first, or the prototype stays generic.

**Sources:**
- https://code.claude.com/docs/en/mcp (verified 12-07-2026)

---

## Q143: What is the difference between a generic prompt and a leading prompt when brainstorming?

**Short answer:** A leading prompt tells Claude which direction to solve in, so it only explores that lane. A generic prompt gives just the problem and asks for options, so the model searches across many possibilities. For brainstorming, use the generic prompt.

- Example: "here is the problem, give me different ways to automate or solve it" beats "solve this using semantic matching."
- You narrow later, once you have seen the range of options, not before.

**Sources:**
- https://code.claude.com/docs/en/best-practices (verified 12-07-2026)
- https://code.claude.com/docs/en/common-workflows (verified 12-07-2026)

---

## Q144: How do I test whether something is feasible before building it, and can Claude drive a browser?

**Short answer:** Run a Phase 0 feasibility spike. Claude can drive a real browser through the Playwright or Chrome DevTools MCP tools, so it can prove a fetch or flow works on one real case before you write any product code.

- In the session, Claude opened Amazon in a real browser and confirmed it could read live prices and product URLs before the spec was written.
- Testing the risky assumption first is what stops you building on a fantasy; if the spike fails, you redesign, not rebuild.

**Sources:**
- https://code.claude.com/docs/en/mcp (verified 12-07-2026)
- https://code.claude.com/docs/en/common-workflows (verified 12-07-2026)

---

## Q145: What is spec-driven development in Claude Code, and what is the flow?

**Short answer:** Brainstorm the problem, prove feasibility (Phase 0), write a spec, turn it into a phased implementation plan, then build phase by phase. It is the same product process you follow without AI; the agents do the execution.

- The flow in the session: problem statement, open brainstorm, Phase 0 browser spike, committed spec (goal, core decisions, data model, phases), implementation plan, then build.
- Do not proceed to the next phase until you are confident in the current one; keep the spec, plan, and progress as living files.

**Sources:**
- https://code.claude.com/docs/en/common-workflows (verified 12-07-2026)
- https://code.claude.com/docs/en/best-practices (verified 12-07-2026)

---

## Q146: How do I run test-driven development while Claude builds?

**Short answer:** Derive test cases from the spec first, then build against them, so testing happens in parallel with development rather than at the end. Split each module into a pure, deterministic part you unit-test against saved fixtures and a thin live-IO wrapper you cover with a manual smoke script.

- In the session, each site module was split into a pure DOM parser (unit-tested on saved HTML fixtures) and a thin browser-fetch wrapper (manual smoke test), because live sites are too flaky for a tight test loop.
- A QA-engineer agent can author the test cases from the spec so the build satisfies them as it goes.

**Sources:**
- https://code.claude.com/docs/en/common-workflows (verified 12-07-2026)
- https://code.claude.com/docs/en/best-practices (verified 12-07-2026)

---

## Q147: What does the `/init` command do?

**Short answer:** `/init` scans your project and generates a starter CLAUDE.md with the build commands, test instructions, and conventions it discovers. If a CLAUDE.md already exists, it suggests improvements rather than overwriting, and you refine from there.

- Run it when you open or scaffold a project so Claude has a baseline of project context.
- Follow up by editing CLAUDE.md (or using `/memory`) to add anything Claude would not discover on its own, like a preferred stack.

**Sources:**
- https://code.claude.com/docs/en/commands (verified 12-07-2026)
- https://code.claude.com/docs/en/memory (verified 12-07-2026)

---

## Q148: How do plugins like Superpowers add skills such as brainstorming and planning?

**Short answer:** A plugin bundles skills, and once installed those skills auto-invoke when relevant. The Superpowers plugin adds brainstorming and writing-plan skills, so a brainstorm produces structured output and an approved spec turns into an implementation plan automatically.

- The skills fire based on their descriptions, you do not have to call them by name each time.
- Confirm a plugin is from a trusted source before installing, since it runs skills in your project.

**Sources:**
- https://code.claude.com/docs/en/plugins (verified 12-07-2026)
- https://code.claude.com/docs/en/skills (verified 12-07-2026)

---

## Q149: How do I reuse agents from one project in another and strip the old project's context?

**Short answer:** Copy the agent definitions and their agent-memory folder into the new project, then prompt Claude to remove all references to the old project, pull in any rule files those agents reference, and loop a review sub-agent until every file scores above your bar (95/100 in the session).

- The agents carry a persona plus accumulated memory; the memory is where prior corrections live, so decide whether to keep or reset it.
- The rubric loop matters because agents almost always miss some stale reference on the first pass.

**Sources:**
- https://code.claude.com/docs/en/sub-agents (verified 12-07-2026)

---

## Q150: Why do I have to restart Claude Code after creating a new sub-agent?

**Short answer:** Claude's watcher only picks up agent directories that existed when the session started, so a sub-agent created mid-session is not dispatchable until you restart. Restart, and it loads from the on-disk definition.

- If Claude "can't find" a sub-agent you just created, a restart is the fix.
- Register or reopen your session after the restart so you continue with the same context.

**Sources:**
- https://code.claude.com/docs/en/sub-agents (verified 12-07-2026)

---

## Q151: How does Claude choose the tech stack, and can I override my global default?

**Short answer:** Claude picks a stack that fits the task, not blindly your global default. In the session it chose TypeScript with Playwright for a browser-driving CLI even though the global default was Python, because Python was set for FastAPI backends, not browser automation. You can override by naming the stack you want.

- State your standing preferences in CLAUDE.md, but expect Claude to deviate with a stated reason when the task calls for it.
- If you want a specific technology, say so in the prompt and Claude will build to it.

**Sources:**
- https://code.claude.com/docs/en/memory (verified 12-07-2026)
- https://code.claude.com/docs/en/common-workflows (verified 12-07-2026)

---

## Q152: What is the status line, and how do I set one up?

**Short answer:** The status line is the bar at the bottom of the terminal showing context like the current model, effort level, branch, and how much of the context window remains. You configure it in settings, and you can have Claude build a custom one for you.

- Watching the remaining context window tells you when to `/compact` (roughly when only 20-30% is left) before responses degrade.
- In the session the status line also carried the project name and the PID used to register sessions in the CCS registry.

**Sources:**
- https://code.claude.com/docs/en/statusline (verified 12-07-2026)

---

## Q153: How should I structure a project so anyone can understand what was built and why?

**Short answer:** Keep living documents alongside the code: a spec, an implementation plan, a progress file, and architecture and decisions files. Rendering the architecture as an interactive HTML file (not plain text) lets non-technical readers follow the problem, the options rejected, and the decisions taken.

- These files also feed future agents, so a new contributor (or Claude itself) can pick up the project without re-deriving the context.
- Record not just what was decided but why, so a later "why did you build it this way" has an answer.

**Sources:**
- https://code.claude.com/docs/en/common-workflows (verified 12-07-2026)
- https://code.claude.com/docs/en/memory (verified 12-07-2026)

---

# July 2026 - Session 8 Additions

New questions raised by the same NextLeap Applied Generative AI Bootcamp cohort on 12-07-2026 during Session 8 (Build Hours Part 2, Phase 2 login sessions and product matching). All URLs verified 12-07-2026.

---

## Q154: Is it safe to give an agent my credentials, and where should they live?

**Short answer:** Never type credentials into the chat. Put them in a `.env` file and tell the agent to read them from there. Anything pasted into the chat becomes part of the session, and an API key exposed that way has to be rotated.

- Claude Code treats `.env` as sensitive and will add it to `.gitignore` before committing, even if you forgot to.
- Best of all is not handing over a password at all: for a site that supports it, log in yourself in a real browser window and let the tool store only the resulting session cookies.
- The honest caveat a participant raised is worth keeping in mind: the agent already sees your repo, your commit history, and your file tree. Scope what you open, do not assume `.env` alone is the whole boundary.

**Sources:**
- https://code.claude.com/docs/en/security (verified 12-07-2026)
- https://code.claude.com/docs/en/settings (verified 12-07-2026)

---

## Q155: What is the safe architecture for logging into a site the tool needs to read?

**Short answer:** The tool opens a real browser window, you sign in yourself with your phone number and OTP, and the tool saves only the encrypted session cookies on your machine. It never sees or stores a password, and nothing is committed to the repo.

- Most Indian grocery apps use phone plus OTP, so often there is no password to hand over in the first place.
- The encryption key can sit in the macOS Keychain, so a leaked session file on its own is useless. On Windows, keeping it in `.env` is a fine substitute.
- Fully unattended login is not possible where OTP or two-factor is involved. You complete the login yourself each time the session expires.
- If the tool stores a session outside `.env`, build the delete command at the same time so you can wipe it on demand.

**Sources:**
- https://code.claude.com/docs/en/security (verified 12-07-2026)
- https://code.claude.com/docs/en/settings (verified 12-07-2026)

---

## Q156: Why did the interactive login have to run in a real terminal instead of inside Claude Code?

**Short answer:** An interactive step that needs a human, such as typing an OTP, is the one thing the agent cannot do for you. Run that command in a normal terminal tab, then hand the result back to the agent.

- In the session, the first login attempt run through Claude Code wrote its output to a temp directory that never touched the project, and logged success unconditionally, so it looked like it had worked. It had not.
- The lesson generalises: a step that reports success without checking anything is worse than a step that fails, because it removes your reason to look.
- After the fix wrote to the project root, both site sessions persisted and returned live pincode-correct prices with no re-login.

**Sources:**
- https://code.claude.com/docs/en/interactive-mode (verified 12-07-2026)
- https://code.claude.com/docs/en/common-workflows (verified 12-07-2026)

---

## Q157: What is harness engineering, and how is it different from prompt and context engineering?

**Short answer:** Prompt engineering is the single instruction. Context engineering is the documentation, knowledge, and project structure you build around the agent. Harness engineering is the guardrails that stop the agent taking a path you never wanted, even when it cannot find the path you did want.

- The worked example from the session: the tool may search and compare a product, but it must never add to cart or place an order. It must refuse even if you prompt it to, until you remove the guardrail yourself.
- In Claude Code the practical carriers of a harness are permission rules, `disallowedTools` on an agent, and hooks that block a tool call before it runs.
- The point of a harness is that it holds without a human watching. If a rule only works when you are reading the output, it is not a guardrail.

**Sources:**
- https://code.claude.com/docs/en/iam (verified 12-07-2026)
- https://code.claude.com/docs/en/hooks (verified 12-07-2026)
- https://code.claude.com/docs/en/sub-agents (verified 12-07-2026)

---

## Q158: What is loop engineering?

**Short answer:** Loop engineering is feeding the blocked or wrong attempt back to the agent so it stops choosing that path next time, instead of you correcting the same thing manually every run.

- The pattern: the harness stops the agent going somewhere it should not, and the record of why it tried is returned to the agent as input for the next iteration.
- The engineering version of this is feeding pull-request review comments back into the agent that writes the code, so the same review comment stops recurring and the agent improves rather than the individual developer.
- This is what turns a one-off correction into a durable behaviour change.

**Sources:**
- https://code.claude.com/docs/en/hooks (verified 12-07-2026)
- https://code.claude.com/docs/en/memory (verified 12-07-2026)

---

## Q159: How do I make sure the test cases cover the edge cases a human would miss?

**Short answer:** Put the testing methods themselves into a rules file, then ask the agent to generate test cases against those methods rather than against one happy path.

- Name the methods explicitly: exhaustive testing, black box, white box, boundary value analysis.
- Add the domain checks that matter for your product. In this build those were same quantity, same variant, and correct pack size, because a peanut butter query returned a protein bar and it was not flagged as a bad match.
- Also test the negative case honestly. If you can find a product by hand that the agent reports as unavailable, that is a defect in the search route, not an absent product.

**Sources:**
- https://code.claude.com/docs/en/memory (verified 12-07-2026)
- https://code.claude.com/docs/en/common-workflows (verified 12-07-2026)

---

## Q160: How do I keep a record of what I tested and when?

**Short answer:** Ask the agent to write every test run into an HTML report capturing the query, each site or path it checked, the direct URL, the value it found, and the recommendation it made. That file becomes your test suite record.

- The value is the timeline: which test ran on which date, what the product did at that moment, and what changed since.
- HTML over plain Markdown here for the same reason as the architecture doc: a non-technical reader can open it and follow the run without being walked through it.

**Sources:**
- https://code.claude.com/docs/en/common-workflows (verified 12-07-2026)

---

## Q161: Does the QA agent start automatically after the engineering agent, and is that test-driven?

**Short answer:** Yes, if you set it up that way. In this build the test cases were written alongside each component rather than after the build finished, and the QA engineer agent ran in parallel with the software engineer agent.

- The four agents in play were product manager (writes the spec), QA engineer (test cases), software engineer (builds), and designer (usability).
- Sub-agent driven execution is Claude Code's default offer when a task is large enough, so you often do not have to ask for it by name.
- By the end of the session 122 test cases were passing, including a new module added mid-session.

**Sources:**
- https://code.claude.com/docs/en/sub-agents (verified 12-07-2026)

---

## Q162: How do I put those agents into a loop, and where does the loop stop?

**Short answer:** Once the specs exist, ask for a dynamic workflow that runs the agents in sequence and repeats: engineer builds, QA tests, PM reviews, designer flags usability, then back to the engineer with the fixes. You stop it with a gate.

- A sensible gate is severity: keep looping while any high-priority issue or enhancement remains, and leave medium and low outside the loop.
- The cost caveat is real. Dynamic workflows consume a lot of tokens, so use them once the spec is stable rather than while you are still exploring.

**Sources:**
- https://code.claude.com/docs/en/sub-agents (verified 12-07-2026)
- https://code.claude.com/docs/en/costs (verified 12-07-2026)

---

## Q163: What is the difference between a skill and a workflow, and when does a skill become one?

**Short answer:** A skill is the capability. A workflow is the capability running without you invoking it. If you are still calling the skill by hand every time, you have built half of it.

- The example from the session: instead of pasting a meeting link and invoking the transcript skill each time, schedule a routine that runs every evening, checks the day's recordings, and files each transcript in its folder.
- This is a general workflow, not the `/workflow` dynamic-workflow feature. The dynamic workflow is the multi-agent loop from Q162, which is a different and more expensive thing.
- The test to apply to your own setup: what is the next step, and how do I remove myself from it.

**Sources:**
- https://code.claude.com/docs/en/skills (verified 12-07-2026)
- https://code.claude.com/docs/en/slash-commands (verified 12-07-2026)

---

## Q164: My company will never let development happen inside an agent. How do I still use Claude on our codebase?

**Short answer:** Use it for understanding and testing rather than writing. Give Claude the repository plus your domain knowledge as context, then work feature by feature to reverse-engineer specs and generate the test cases humans miss.

- Start by listing features and sub-features at a high level, then take one feature at a time. Do not point it at the whole repo and ask for everything.
- Where no requirement document exists, build the spec from the code. Where one does exist, compare the requirement to the code.
- The comparison is where the value is: if the requirement says A, B, C and the code does A, B, C, D, then D was built outside the spec. That is a test case and a PM decision, either update the spec or remove the code.
- Do not scale to the next module until you are confident the current feature's test cases are genuinely complete.

**Sources:**
- https://code.claude.com/docs/en/common-workflows (verified 12-07-2026)
- https://code.claude.com/docs/en/memory (verified 12-07-2026)

---

## Q165: Is my session data used for training, and what is the feedback prompt asking me?

**Short answer:** Claude Code periodically shows an interactive feedback prompt that asks you to rate the session and then asks separately whether you want to share it. Sharing is a choice you make there, and the current policy is the place to confirm the details for your plan.

- Consumer plans use your data for model training only if you opt in. Commercial plans (Team, Enterprise) do not use your data for training by default.
- This is a good reason to keep credentials out of the chat regardless of the setting. Anything you paste is in the session.

**Sources:**
- https://code.claude.com/docs/en/data-usage (verified 12-07-2026)
- https://privacy.anthropic.com/en/articles/10023580-is-my-data-used-for-model-training (verified 12-07-2026)

---

## Q166: Is Claude Code free, and what do I need to use it?

**Short answer:** Claude Code is not free. It starts with the Pro plan at 20 dollars a month, and you can also use it against API billing.

- Higher usage limits come with the Max plans, which is what matters most if you run sub-agent loops or dynamic workflows, since those consume tokens quickly.
- The Superpowers plugin used in this build is installed separately from the plugin list, and without it the brainstorm, spec, and plan documents are not created as part of the process.

**Sources:**
- https://www.anthropic.com/pricing (verified 12-07-2026)
- https://code.claude.com/docs/en/costs (verified 12-07-2026)
- https://code.claude.com/docs/en/plugins (verified 12-07-2026)

---

## Q167: A command is stuck and burning time without progress. What do I do?

**Short answer:** Press Ctrl+C to stop the current execution, then give the next command. The stuck execution ends and the new one starts.

- Watch the signal that matters: if time is passing but tokens are not being consumed, the agent is waiting on something rather than working.
- In this session that state came from a site putting up a login wall mid-run, which the agent could not pass on its own. Stopping it and running the manual login was the correct move, not waiting longer.

**Sources:**
- https://code.claude.com/docs/en/interactive-mode (verified 12-07-2026)
