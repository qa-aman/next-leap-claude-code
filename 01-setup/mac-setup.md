# Claude Code Setup - macOS

Step-by-step guide to install and configure Claude Code on a Mac.

**Time required:** 5-10 minutes

---

## Prerequisites

Before you start, make sure you have:

1. **macOS 13.0 or later** - Click the Apple menu > About This Mac to check your version
2. **4 GB+ RAM** - Any modern Mac meets this
3. **Internet connection** - Required throughout setup and usage
4. **A Claude subscription** - Pro, Max, Teams, or Enterprise. The free Claude.ai plan does not include Claude Code access. Subscribe at https://claude.com/pricing
5. **A terminal app** - Use the built-in Terminal (Applications > Utilities > Terminal) or iTerm2

---

## Section 1: Open Your Terminal

1. Press `Cmd + Space` to open Spotlight Search
2. Type `Terminal` and press Enter
3. A terminal window opens with a command prompt

If you prefer iTerm2 or another terminal, use that instead. Any terminal app works.

---

## Section 2: Install Claude Code (Native Install - Recommended)

Run this single command in your terminal:

```bash
curl -fsSL https://claude.ai/install.sh | bash
```

This downloads and installs the Claude Code binary to `~/.local/bin/claude`. The native installer requires no dependencies (no Node.js, no npm). It auto-updates in the background.

**Wait for the installation to complete.** You should see a success message.

### Alternative: Install via Homebrew

If you prefer Homebrew:

```bash
brew install --cask claude-code
```

Note: Homebrew installations do not auto-update. Run `brew upgrade claude-code` periodically to stay current.

---

## Section 3: Verify the Installation

Confirm Claude Code installed correctly:

```bash
claude --version
```

You should see a version number printed (e.g., `2.0.30`).

For a more detailed check:

```bash
claude doctor
```

This runs diagnostics on your installation and configuration.

---

## Section 4: Start Claude Code and Log In

1. Navigate to any project folder (or just stay in your home directory for now):

```bash
cd ~/Desktop
```

2. Launch Claude Code:

```bash
claude
```

3. **First-time login flow:**
   - Claude Code will open your default browser automatically
   - If the browser does not open, press `c` in the terminal to copy the login URL, then paste it into your browser manually
   - Log in with your Claude.ai account (Pro, Max, Teams, or Enterprise)
   - After successful login, return to the terminal - Claude Code is now authenticated

Your credentials are stored securely in the macOS Keychain. You will not need to log in again unless you explicitly log out.

---

## Section 5: Confirm Everything Works

You should now see the Claude Code welcome screen in your terminal. It shows:
- Your session information
- Recent conversations (empty on first run)
- Latest updates

Try your first prompt by typing:

```
what can Claude Code do?
```

Claude will respond with its capabilities. You are now ready to use Claude Code.

---

## Section 6: Essential Commands to Know

| Command | What it does |
|---------|-------------|
| `claude` | Start an interactive session |
| `claude "task"` | Run a one-time task |
| `claude -p "query"` | Run a query and exit |
| `claude -c` | Continue the most recent conversation |
| `claude commit` | Create a git commit |
| `/help` | Show available commands (inside a session) |
| `/clear` | Clear conversation history |
| `exit` or `Ctrl+C` | Exit Claude Code |

---

## Section 7: Using Claude Code in a Project

To use Claude Code on a real project:

```bash
cd /path/to/your/project
claude
```

Try these starter prompts:

```
what does this project do?
```

```
explain the folder structure
```

```
where is the main entry point?
```

Claude Code reads your project files automatically. You do not need to manually point it at files.

---

## Section 8: Install the Antigravity IDE Extension (Optional)

If you use Google Antigravity IDE (built on VS Code's extension ecosystem):

1. Open Antigravity IDE
2. Press `Cmd + Shift + X` to open Extensions
3. Search for "Claude Code"
4. Click Install on the extension by Anthropic
5. Press `Cmd + Shift + P`, type "Claude Code", and select "Open in New Tab"

This gives you inline diffs, @-mentions, and conversation history directly in your editor. Antigravity supports the VS Code extension marketplace, so the Claude Code extension works without any additional configuration.

---

## Section 9: Install the Desktop App (Optional)

If you prefer a graphical interface over the terminal:

1. Download the macOS Desktop App from: https://claude.ai/api/desktop/darwin/universal/dmg/latest/redirect
2. Open the `.dmg` file and drag Claude to your Applications folder
3. Launch Claude from Applications
4. Sign in with your Claude account
5. Click the "Code" tab to start coding

The Desktop App works alongside the terminal CLI. Your settings and CLAUDE.md files are shared across both.

---

## Updating Claude Code

**Native install:** Updates happen automatically in the background. To force an immediate update:

```bash
claude update
```

**Homebrew install:** Run manually:

```bash
brew upgrade claude-code
```

---

## Uninstalling Claude Code

If you need to remove Claude Code:

**Native install:**

```bash
rm -f ~/.local/bin/claude
rm -rf ~/.local/share/claude
```

**Homebrew install:**

```bash
brew uninstall --cask claude-code
```

**Remove configuration files (optional - this deletes all settings and history):**

```bash
rm -rf ~/.claude
rm ~/.claude.json
```

---

## Troubleshooting

| Problem | Solution |
|---------|----------|
| `claude: command not found` | Close and reopen your terminal, or run `source ~/.zshrc` |
| Browser does not open on login | Press `c` to copy the login URL, paste it in your browser |
| Permission errors during install | Do not use `sudo`. The native installer puts the binary in `~/.local/bin/` which does not require root |
| Search not working | Claude Code includes ripgrep. If search fails, install it manually: `brew install ripgrep` |

For more help: https://code.claude.com/docs/en/troubleshooting

---

## Source

All instructions verified against the official Claude Code documentation at https://code.claude.com/docs/en/overview and https://code.claude.com/docs/en/setup (accessed March 2026).
