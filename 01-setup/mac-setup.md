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

Never used a terminal before? Anthropic's step-by-step terminal guide covers the basics: https://code.claude.com/docs/en/terminal-guide

---

## Section 2: Install Claude Code (Native Install - Recommended)

Run this single command in your terminal:

```bash
curl -fsSL https://claude.ai/install.sh | bash
```

This downloads and installs the Claude Code binary to `~/.local/bin/claude`. The native installer requires no dependencies (no Node.js, no npm). It auto-updates in the background.

**Wait for the installation to complete.** You should see a success message.

**Then close the Terminal window and open a new one.** The `claude --version` check in the next section fails inside the same window that ran the install, because that window's PATH was read before the install happened. This caught participants in the August 2026 cohort.

### Alternative: Install via Homebrew

If you prefer Homebrew, there are two casks. `claude-code` tracks the stable channel (about a week behind). `claude-code@latest` tracks the latest channel:

```bash
brew install --cask claude-code
```

Note: Homebrew installations do not auto-update. Run `brew upgrade claude-code` (or `brew upgrade claude-code@latest`) periodically, or set `CLAUDE_CODE_PACKAGE_MANAGER_AUTO_UPDATE=1` to have Claude Code run the upgrade for you.

---

## Section 3: Verify the Installation

Confirm Claude Code installed correctly:

```bash
claude --version
```

You should see a version number printed (e.g., `2.1.269 (Claude Code)`).

For a more detailed check:

```bash
claude doctor
```

This runs diagnostics on your installation and configuration. You can also run `/doctor` from inside an active Claude Code session to check installation integrity, subscription status, and system configuration at any time.

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
   - When prompted, select **"Claude account with subscription"** (not the API key option)
   - Claude Code will open your default browser automatically
   - If the browser does not open, press `c` in the terminal to copy the login URL, then paste it into your browser manually
   - Log in with your Claude.ai account (Pro, Max, Teams, or Enterprise)
   - After successful login, return to the terminal - Claude Code is now authenticated
   - On first launch, Claude Code asks you to pick a **terminal text style** (light or dark theme). Choose whichever matches your terminal background

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

## Section 8: Install the Claude Code Extension in Your Editor (Optional)

Anthropic ships the Claude Code extension for VS Code and Cursor, and it also installs in other VS Code forks (Antigravity, Devin Desktop, Kiro) from the editor's Extensions view or from the Open VSX registry. Source: https://code.claude.com/docs/en/vs-code

1. Open your editor (Antigravity, VS Code, or Cursor)
2. Press `Cmd + Shift + X` to open Extensions
3. Search for "Claude Code" and click Install on the extension by Anthropic
4. If the search finds nothing, install from Open VSX: https://open-vsx.org/extension/Anthropic/claude-code
5. Press `Cmd + Shift + P`, type "Claude Code", and select "Open in New Tab"

This gives you inline diffs, @-mentions, and conversation history directly in your editor. The extension bundles its own copy of the CLI for the chat panel. To type `claude` in the editor's integrated terminal you still need the standalone install from Section 2.

**Terminal tips inside the editor:**

1. Run `/terminal-setup` once inside Claude Code so Shift+Enter inserts a newline instead of submitting. Needed in VS Code and Cursor. Apple Terminal, iTerm2, Warp and Ghostty support it natively. Source: https://code.claude.com/docs/en/terminal-config
2. If the display flickers or the scrollback jumps, run `/tui fullscreen` inside Claude Code.

---

## Section 9: Install the Desktop App (Optional)

If you prefer a graphical interface over the terminal:

1. Download the macOS Desktop App (universal build for Intel and Apple Silicon) from the official page: https://code.claude.com/docs/en/desktop-quickstart
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
| `claude: command not found` (install succeeded) | Native install puts the binary in `~/.local/bin`, which is not on your PATH. See **Case 1** below for the exact one-line fix |
| `curl: (22) ... error: 403` when running the install script | The install URL is being blocked (corporate network, proxy, or VPN). See **Case 2** below for the npm fallback |
| Browser does not open on login | Press `c` to copy the login URL, paste it in your browser |
| Subscription required / authentication fails | Verify you have an active Claude Pro or Max subscription at https://claude.ai. Log out and log back in to refresh credentials |
| Node version too old (npm route only) | Run `node --version` to check. The npm package needs Node.js 22 or later. Download from https://nodejs.org/en/download |
| Permission errors during install | Never `sudo npm install -g`, the docs say so explicitly. The native installer puts the binary in `~/.local/bin/` which does not need root. If `~/.local` itself is not writable, the docs' fix is `sudo chown -R $(whoami) ~/.local`, then re-run the installer. See https://code.claude.com/docs/en/troubleshoot-install |
| Search not working | Claude Code includes ripgrep. If search fails, install it manually: `brew install ripgrep` |
| Shift+Enter submits instead of adding a new line | Run `/terminal-setup` once inside Claude Code (VS Code, Cursor). Apple Terminal, iTerm2, Warp and Ghostty support it natively |
| Screen flickers or scrollback jumps | Run `/tui fullscreen` inside Claude Code |
| `git clone` says `Permission denied (publickey)` | You used the SSH clone URL with no SSH key set up. Use the HTTPS URL instead: `git clone https://github.com/qa-aman/next-leap-claude-code.git` |

For more help: https://code.claude.com/docs/en/troubleshooting

---

## Real Setup Issues From Live Cohorts (and Exact Fixes)

These two issues hit participants during a live setup session. Both look like the install failed - it did not. Here is exactly what happened and how to fix each.

### Case 1: Install succeeded, but `claude: command not found`

**What you see:** The installer prints `✓ Claude Code successfully installed!` with a version number, and a `⚠ Setup notes` line that says:

```
Native installation exists but ~/.local/bin is not in your PATH.
```

Then running `claude` still returns `zsh: command not found: claude`.

**Why:** The install worked. The binary is at `~/.local/bin/claude`, but your shell (zsh) does not look in that folder yet, so it cannot find the command. This is a PATH issue, not an install failure.

**Fix:** Add the folder to your shell config, then reload it:

```bash
echo 'export PATH="$HOME/.local/bin:$PATH"' >> ~/.zshrc && source ~/.zshrc
```

Then launch Claude Code:

```bash
claude
```

This is a one-time fix. The installer itself prints this exact command in its Setup notes - if you see it on screen, just copy that line. After this, `claude` works in every new terminal.

### Case 2: `curl: (22) The requested URL returned error: 403`

**What you see:** Running the native install command fails immediately:

```
curl -fsSL https://claude.ai/install.sh | bash
curl: (22) The requested URL returned error: 403
```

**Why:** A `403` means the request to the install script was rejected before it ever downloaded. This is almost always a network block - a corporate laptop, an office proxy, a VPN, or a firewall sitting between you and `claude.ai`. It is not a problem with your Mac.

**Fix - try these in order:**

**Option A (fastest): switch networks.** Disconnect from the office VPN, or move to a personal hotspot, then re-run the native install command. On an unfiltered network the `403` usually disappears.

**Option B (most reliable): install via npm.** The npm package is the official Anthropic build and routes around the blocked script URL:

```bash
npm install -g @anthropic-ai/claude-code
```

Check npm is available first:

```bash
node --version
npm --version
```

If npm is not installed, install Node.js with Homebrew:

```bash
brew install node
```

Then run the npm install command above. Once installed, `claude --help` should work right away - npm's global bin is usually already on your PATH. (If you still hit `command not found`, apply the Case 1 fix.)

**Option C: if Homebrew is not installed either,** install it first, then use Option B:

```bash
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
```

Note: the npm and Homebrew routes do not auto-update. To upgrade an npm install run `npm install -g @anthropic-ai/claude-code@latest` (not `npm update -g`, which may not move you to the newest release). For Homebrew run `brew upgrade claude-code`. The npm package needs Node.js 22 or later.

---

## Source

All instructions verified against the official Claude Code documentation at https://code.claude.com/docs/en/setup, https://code.claude.com/docs/en/troubleshoot-install, https://code.claude.com/docs/en/terminal-guide and https://code.claude.com/docs/en/vs-code (accessed 12-09-2026). The fixes were also cross-checked against the live cohort write-up at https://shipwithailab.substack.com/p/claude-code-install-fails-the-same.
