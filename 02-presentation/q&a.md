# Q&A - Claude Code Workshop

Answers to open questions from Sessions 1 and 2, sourced from official Anthropic documentation.

---

## Q1: Is my data safe? What about PII?

**Short answer:** Paid Claude Pro/Max users can opt out of model training. Your code is not stored long-term unless you explicitly allow it.

**Details from official docs:**

- Claude Code will use your chats and coding sessions to improve models **only if** you choose to allow it in your Privacy Settings. This is opt-in for consumer plans (Pro, Max).
- Incognito chats are never used for training, even if you have model improvement enabled.
- When you provide thumbs up/down feedback, that conversation is stored for up to 5 years, but is de-linked from your user ID before use.
- Raw content from connectors (Google Drive, MCP servers) is excluded from training unless directly copied into conversations.
- Claude Code has limited retention periods for sensitive information. Consumer users can change their privacy settings at any time at https://claude.ai/settings/privacy.
- For Team and Enterprise plans, different (stricter) policies apply under the Commercial Terms of Service. Your data is not used for training.

**What Claude Code sends to Anthropic servers:**

- Your conversation messages and tool call results (file contents, command outputs) are sent to Anthropic's API for processing.
- Claude Code does not send your entire codebase - only the files and outputs relevant to the current conversation.

**Security safeguards built into Claude Code:**

- Permission-based architecture: sensitive operations require explicit approval.
- Write access is restricted to the folder where Claude Code was started and its subfolders.
- Network requests require user approval by default.
- API keys and tokens are encrypted via secure credential storage.
- Anthropic holds SOC 2 Type 2 and ISO 27001 certifications (see https://trust.anthropic.com).

**Bottom line for PII:** If your organization handles sensitive PII, disable model improvement in Privacy Settings, and consider the Team or Enterprise plan where data is contractually excluded from training. Always review what Claude Code reads and sends before approving tool calls.

**Sources:**
- https://privacy.claude.com/en/articles/10023580-claude-code-privacy
- https://code.claude.com/docs/en/security

---

## Q2: What plugins should a first-time Claude Code user install?

### Recommended "must-have" plugins (covered in Session 2)

Install these first. They cover planning, code quality, and UI workflows:

| Plugin | What it does | Why it matters |
|--------|-------------|----------------|
| **Superpower** | Handles brainstorming, architecture planning, and auto-invokes relevant skills based on context | "The skill that you must have first." It orchestrates other skills automatically so you don't need to remember which one to call |
| **Skill Creator** | Ensures any skill you create follows Anthropic's official skill architecture | Created by Anthropic. Keeps your custom skills structured and maintainable |
| **Code Review** | Reviews code and flags critical issues | Catches bugs and gaps before they reach production |
| **Code Simplifier** | Improves code quality, reuse, and efficiency | Cleans up code after implementation |
| **Front End Design** | Auto-improves UI based on Anthropic's design guidelines | Auto-invoked when you mention front-end work - no need to call it manually |
| **Chrome DevTools** | Opens Chrome from within Claude Code to inspect UI, check fonts, click around | Lets Claude see and interact with your live app directly |

**Also recommended:**

- **Playwright** - for testing web UI elements programmatically
- **Figma MCP** - connects Figma designs to Claude Code for implementation workflows

---

### How Claude Code extensions work

Claude Code has a lightweight extension model. There are no "app store" plugins to browse. Instead, you extend Claude Code through three mechanisms: **bundled skills**, **custom skills**, and **MCP servers**.

### Bundled skills (ship with Claude Code, no setup needed)

These are available out of the box in every session:

| Skill | What it does |
|-------|-------------|
| `/batch <instruction>` | Orchestrate large-scale changes across a codebase in parallel. Decomposes work into 5-30 independent units, spawns one agent per unit in an isolated git worktree |
| `/claude-api` | Load Claude API reference material for your project's language (Python, TypeScript, Java, Go, Ruby, C#, PHP, cURL) and Agent SDK reference |
| `/debug [description]` | Troubleshoot your current Claude Code session by reading the session debug log |
| `/loop [interval] <prompt>` | Run a prompt repeatedly on an interval (e.g., `/loop 5m check if the deploy finished`) |
| `/simplify [focus]` | Review recently changed files for code reuse, quality, and efficiency issues, then fix them |

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

### MCP servers (connect external tools)

MCP (Model Context Protocol) lets Claude Code talk to external services. You configure them in your Claude Code settings. Common examples:

- **Slack** - search channels, send messages
- **Jira/Linear** - read and update tickets
- **Confluence** - read and push documentation
- **Playwright/Chrome DevTools** - browser automation and debugging
- **Figma** - read designs for implementation

To add an MCP server, use `/mcp` inside a Claude Code session or edit your settings file directly.

### Recommended starter setup for PMs

If you are new to Claude Code and working as a PM, start with:

1. **No plugins needed on day one.** Bundled skills and built-in tools (file reading, search, git) cover most PM workflows out of the box.
2. **Add MCP servers as needed.** If you use Confluence, add the Confluence MCP. If you use Jira, add the Jira MCP. Only add what you actually use.
3. **Create project skills for repeated workflows.** If you find yourself giving Claude the same instructions repeatedly (e.g., "write a PRD in this format"), turn those instructions into a skill.

### IDE extension (optional)

If you use an IDE (Antigravity, VS Code, Cursor), install the Claude Code extension:

- Open Extensions (`Cmd+Shift+X` on Mac, `Ctrl+Shift+X` on Windows)
- Search "Claude Code" and install the one by Anthropic
- Open Command Palette (`Cmd+Shift+P` / `Ctrl+Shift+P`), type "Claude Code", select "Open in New Tab"

This gives you inline diffs, @-mentions, and conversation history inside your editor.

### JetBrains plugin (optional)

If you use IntelliJ IDEA, PyCharm, or WebStorm, install the Claude Code plugin from the JetBrains Marketplace.

**Sources:**
- https://code.claude.com/docs/en/skills
- https://code.claude.com/docs/en/mcp
- https://code.claude.com/docs/en/overview

---

## Q3: Why is terminal-based Claude Code more powerful than using it inside an IDE like Cursor?

**Follow-up from Sonar:** "If I pass architecture.md and todo.md to Cursor, won't that compensate?"

### 1. The CLI has the full tool and command set

The official docs confirm the VS Code extension is a subset of the full CLI.

| Capability | Terminal CLI | VS Code Extension |
|-----------|-------------|-------------------|
| Commands and skills | All | Subset (type `/` to see what's available) |
| MCP server config | Full (add, remove, configure) | Partial (manage existing only) |
| `!` bash shortcut | Yes | No |
| Tab completion | Yes | No |
| Non-interactive mode (`claude -p`) | Yes | No |
| Piping data in/out | Yes | No |

### 2. The agentic loop is the real difference vs. Cursor

Claude Code is not a chatbot that answers questions and waits. It autonomously reads files, runs commands, makes changes, and works through problems. The workflow is: explore the codebase, plan the approach, implement across multiple files, then verify its own work (run tests, check output).

Cursor and similar IDE copilots work on a request-response basis within the editor. Passing `architecture.md` and `todo.md` gives Cursor static context, but it doesn't give it the ability to:

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
- `--output-format json` for structured output in automated workflows
- `--allowedTools` to scope permissions for batch operations

### 4. Context management is more explicit in the terminal

The terminal gives direct, keyboard-driven control over context: `/clear` between tasks, `/compact` with custom instructions, `/rewind` to restore checkpoints, `Esc` to stop mid-action. The VS Code extension supports checkpoints and rewind too, but the CLI's full command set and keyboard shortcuts make aggressive context management faster. This matters because context window performance degrades as it fills.

**Bottom line:** Passing context files to Cursor gives it information, but Claude Code's power comes from autonomous tool access and the agentic loop, not just from reading files. The terminal is where the full feature set lives.

**Sources:**
- https://code.claude.com/docs/en/vs-code (extension vs CLI comparison table)
- https://code.claude.com/docs/en/best-practices
- https://code.claude.com/docs/en/cli-reference

---

## Q4: Installation issues following GitHub repo steps

A troubleshooting guide has been added to the setup files in this repo. If you are facing installation issues, check the troubleshooting section at the bottom of the relevant file:

- **Mac users:** `01-setup/mac-setup.md`
- **Windows users:** `01-setup/windows-setup.md`

Both files cover common issues including: command not found, subscription/authentication errors, Node version too old, permission errors, browser not opening on login, and platform-specific fixes.

For additional help beyond what's in these files: https://code.claude.com/docs/en/troubleshooting

---

## Quick reference

| Topic | Official docs |
|-------|--------------|
| Privacy & data handling | https://privacy.claude.com/en/articles/10023580-claude-code-privacy |
| Security architecture | https://code.claude.com/docs/en/security |
| Skills & custom commands | https://code.claude.com/docs/en/skills |
| MCP servers | https://code.claude.com/docs/en/mcp |
| Permissions | https://code.claude.com/docs/en/permissions |
| Trust center (SOC 2, ISO 27001) | https://trust.anthropic.com |
