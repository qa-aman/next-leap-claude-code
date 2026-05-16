# Q&A - Claude Code Workshop

Answers to open questions from Sessions 1 and 2, sourced from official Anthropic documentation. All URLs verified 16-05-2026.

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
