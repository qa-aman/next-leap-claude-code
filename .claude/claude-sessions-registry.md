# Claude Code Sessions Registry

Manage 15-20 named Claude Code sessions across terminals without using the `/resume` picker.
Registry file: `~/.claude/named-sessions.json`

---

## Registered Sessions

> Auto-synced on every `ccs add`, `ccs rename`, `ccs remove`, and `ccs sync`.

| Name | PID | Status | Created | Last Used | Msgs | Description |
|---|---|---|---|---|---|---|
| `multi-agent` | 53891 | ○ idle | 19-05-2026 | 23-05-2026 00:13 | 19 | Multi agent session |
| `multi-agent-html-file` | 37182 | ● live | 23-05-2026 | 23-05-2026 11:01 | 29 | this chat is used to create the multi agent file for cohort |
| `create-agent-task` | 59871 | ● live | 23-05-2026 | 23-05-2026 12:30 | 1 | this chat is being used to create the agent |
---

## Quick Reference

| Command | What it does |
|---|---|
| `ccs list` | Show all named sessions with live/idle status, created date, last used, message count |
| `ccs pids` | Show all running Claude processes with PIDs |
| `ccs open <name>` | Resume a session by name |
| `ccs add <name> <pid>` | Register a session using its PID |
| `ccs add <name> <session-id>` | Register using full session ID |
| `ccs add <name> <pid> "<desc>"` | Register with a custom description |
| `ccs update <name> "<desc>"` | Update description of an existing session |
| `ccs rename <old> <new>` | Rename a session |
| `ccs remove <name>` | Delete a session from registry |
| `ccs sync` | Force-rebuild the registry table in this file from JSON |
| `ccs sessions` | Browse last 30 sessions from history |

---

## How to Add a Session

**Step 1** — Glance at the statusline in the terminal you want to register. The PID is shown
directly next to the project name: `⊡ project-name  pid:54057`.

**Step 2** — Register it with a name.

From the terminal prompt (outside Claude Code):
```bash
ccs add my-session 54057
```

From inside a Claude Code session (prefix with `!`):
```bash
! ccs add my-session 54057
```

Optional description: `ccs add main 66459 "Main spec work"`

---

## How to Open a Session

Must be run **outside** an active Claude Code session — in the raw terminal:

```bash
ccs open my-session
```

---

## Notes

1. `ccs open` must be run outside an active Claude Code session.
2. All other commands work both in terminal and inside Claude Code via `!`.
3. `○ idle` means the terminal process ended but the session is still resumable.
4. Session names are case-sensitive. Use lowercase kebab-case.
5. The Registered Sessions table is auto-maintained — never edit it manually. Run `ccs sync` if it looks stale.
6. Description is auto-populated from the session's first message if not provided.
