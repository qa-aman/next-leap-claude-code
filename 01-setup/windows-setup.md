# Claude Code Setup - Windows

Step-by-step guide to install and configure Claude Code on Windows.

**Time required:** 10-15 minutes

---

## Prerequisites

Before you start, make sure you have:

1. **Windows 10 or Windows 11** - Press `Win + I` > System > About to check
2. **4 GB+ RAM** - Any modern PC meets this
3. **Internet connection** - Required throughout setup and usage
4. **A Claude subscription** - Pro, Max, Teams, or Enterprise. The free Claude.ai plan does not include Claude Code access. Subscribe at https://claude.com/pricing

---

## Section 1: Open PowerShell

1. Press `Win + S` (or click the search bar)
2. Type `PowerShell`
3. Click **"Windows PowerShell"** (you do NOT need to run as Administrator)

A blue PowerShell window opens with a command prompt.

> **Important: pick the 64-bit PowerShell, not the x86 one.**
> The search results may show two entries: `Windows PowerShell` and `Windows PowerShell (x86)`.
> Always pick the one **without** `(x86)`. The x86 version is 32-bit, and Claude Code does not support 32-bit Windows. If you accidentally install from the x86 PowerShell, you will see an error like:
>
> ```
> Claude Code does not support 32-bit Windows. Please use the 64-bit version.
> ```
>
> Close that window, search again, and pick the entry **without** `(x86)`.

---

## Section 2: Install Claude Code (Native Install - Recommended)

Run all three steps below in order. Steps 1 and 2 run in the same PowerShell window. Step 3 runs in a fresh window.

### Step 1: Download and install Claude Code

In the open PowerShell window, run:

```powershell
irm https://claude.ai/install.ps1 | iex
```

This downloads and installs Claude Code. The native installer requires no dependencies (no Node.js, no npm). It auto-updates in the background. **Wait for the installation to complete** before continuing. You should see a success message.

### Step 2: Add Claude to your User PATH

The installer drops the `claude` binary into `C:\Users\<YourName>\.local\bin`, but on most Windows machines that folder is not yet in your User PATH, so typing `claude` will not work until you add it. In the **same PowerShell window**, run:

```powershell
[Environment]::SetEnvironmentVariable("PATH", [Environment]::GetEnvironmentVariable("PATH", "User") + ";$HOME\.local\bin", "User")
```

This appends the install location to your User PATH and saves it permanently. The command prints nothing on success - that is expected.

### Step 3: Open a new PowerShell and verify

PATH changes only take effect in **new** PowerShell windows. Close the current PowerShell window completely, then open a fresh one (`Win + S` > type `PowerShell` > Enter) and run:

```powershell
claude --help
```

You should see the Claude Code help output listing all available commands. If you see `The term 'claude' is not recognized...`, Step 2 did not save (see Troubleshooting at the bottom).

---

### Alternative: Install via CMD

If you prefer Command Prompt instead of PowerShell:

1. Press `Win + R`, type `cmd`, press Enter
2. Run:

```batch
curl -fsSL https://claude.ai/install.cmd -o install.cmd && install.cmd && del install.cmd
```

### Alternative: Install via WinGet

If you have WinGet available (included in Windows 11 and recent Windows 10 updates):

```powershell
winget install Anthropic.ClaudeCode
```

Note: WinGet installations do not auto-update. Run `winget upgrade Anthropic.ClaudeCode` periodically.

---

## Section 3: Run Detailed Diagnostics

You already ran `claude --help` in Step 3 of Section 2, so the install is verified. For a deeper diagnostic of your installation and configuration, run:

```powershell
claude --version
```

```powershell
claude doctor
```

`claude doctor` runs a full health check (subscription status, PATH, dependencies, IDE integration). You can also run `/doctor` from inside an active Claude Code session at any time.

---

## Section 4: Start Claude Code and Log In

1. In PowerShell, navigate to any project folder (or stay in your user directory):

```powershell
cd ~\Desktop
```

2. Launch Claude Code:

```powershell
claude
```

3. **First-time login flow:**
   - When prompted, select **"Claude account with subscription"** (not the API key option)
   - Claude Code will open your default browser automatically
   - If the browser does not open, press `c` in the terminal to copy the login URL, then paste it into your browser manually
   - Log in with your Claude.ai account (Pro, Max, Teams, or Enterprise)
   - After successful login, return to PowerShell - Claude Code is now authenticated
   - On first launch, Claude Code asks you to pick a **terminal text style** (light or dark theme). Choose whichever matches your terminal background

Your credentials are stored in `~\.claude\.credentials.json`. You will not need to log in again unless you explicitly log out.

---

## Section 5: Confirm Everything Works

You should now see the Claude Code welcome screen. It shows:
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

```powershell
cd C:\path\to\your\project
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
2. Press `Ctrl + Shift + X` to open Extensions
3. Search for "Claude Code"
4. Click Install on the extension by Anthropic
5. Press `Ctrl + Shift + P`, type "Claude Code", and select "Open in New Tab"

This gives you inline diffs, @-mentions, and conversation history directly in your editor. Antigravity supports the VS Code extension marketplace, so the Claude Code extension works without any additional configuration.

---

## Section 9: Install the Desktop App (Optional)

If you prefer a graphical interface over the terminal:

1. Download the Windows Desktop App:
   - **x64 (most PCs):** https://claude.ai/api/desktop/win32/x64/exe/latest/redirect
   - **ARM64:** https://claude.ai/api/desktop/win32/arm64/exe/latest/redirect (remote sessions only)
2. Run the `.exe` installer
3. Launch Claude from the Start Menu
4. Sign in with your Claude account
5. Click the "Code" tab to start coding

The Desktop App works alongside PowerShell/CMD. Your settings and CLAUDE.md files are shared across both.

---

## Section 10: Git Bash Path Troubleshooting

If Claude Code cannot find your Git Bash installation, you need to set the path manually.

1. Find your `settings.json` file at `%USERPROFILE%\.claude\settings.json`
2. Add the following:

```json
{
  "env": {
    "CLAUDE_CODE_GIT_BASH_PATH": "C:\\Program Files\\Git\\bin\\bash.exe"
  }
}
```

If Git is installed in a non-default location, adjust the path accordingly.

---

## Section 11: Alternative - Using WSL (Windows Subsystem for Linux)

If you prefer a Linux environment on Windows:

1. Open PowerShell as Administrator
2. Run:

```powershell
wsl --install
```

3. Restart your computer
4. Open the installed Linux distribution (Ubuntu by default) from the Start Menu
5. Inside WSL, install Claude Code using the Linux/macOS command:

```bash
curl -fsSL https://claude.ai/install.sh | bash
```

Both WSL 1 and WSL 2 are supported. WSL 2 additionally supports sandboxing for enhanced security.

---

## Section 12: Install Git for Windows (Optional)

**You do not need this to complete the workshop.** Claude Code on Windows installs and runs without Git for Windows. This setup guide has been verified end-to-end on a Windows machine that did not have Git for Windows installed.

**What you lose by skipping it:**
Per the [official Claude Code setup doc](https://code.claude.com/docs/en/setup), "Git for Windows is recommended on native Windows so Claude Code can use the Bash tool. If Git for Windows is not installed, Claude Code uses PowerShell as the shell tool instead." That fallback covers most workflows. The only commands that may misbehave under PowerShell-only are skills or scripts that assume Unix shell behavior (`grep`, `awk`, piped chains, shell scripts).

**Install it later if you need it:**

1. Go to https://git-scm.com/downloads/win
2. Download the 64-bit installer (default for most machines)
3. Run the installer and accept the defaults through the wizard
4. Click Install, then Finish

**Verify Git is installed:**

```
git --version
```

You should see something like `git version 2.47.0.windows.1`.

If Claude Code cannot find your Git Bash installation after install, see Section 10 (Git Bash Path Troubleshooting) for the manual path setting.

---

## Updating Claude Code

**Native install:** Updates happen automatically in the background. To force an immediate update:

```powershell
claude update
```

**WinGet install:** Run manually:

```powershell
winget upgrade Anthropic.ClaudeCode
```

---

## Uninstalling Claude Code

If you need to remove Claude Code:

**Native install (PowerShell):**

```powershell
Remove-Item -Path "$env:USERPROFILE\.local\bin\claude.exe" -Force
Remove-Item -Path "$env:USERPROFILE\.local\share\claude" -Recurse -Force
```

**WinGet install:**

```powershell
winget uninstall Anthropic.ClaudeCode
```

**Remove configuration files (optional - this deletes all settings and history):**

```powershell
Remove-Item -Path "$env:USERPROFILE\.claude" -Recurse -Force
Remove-Item -Path "$env:USERPROFILE\.claude.json" -Force
```

---

## Troubleshooting

| Problem | Solution |
|---------|----------|
| `Claude Code does not support 32-bit Windows. Please use the 64-bit version.` | You launched the x86 (32-bit) PowerShell. Close it. Press `Win + S`, type `PowerShell`, and pick the entry labeled **"Windows PowerShell"** without the `(x86)` suffix. Re-run the install command from the 64-bit window |
| `claude: command not recognized` / `The term 'claude' is not recognized...` | Your User PATH is missing `C:\Users\<YourName>\.local\bin`. Run this in PowerShell, then open a fresh PowerShell window: `[Environment]::SetEnvironmentVariable("PATH", [Environment]::GetEnvironmentVariable("PATH", "User") + ";$HOME\.local\bin", "User")`. If you prefer the GUI: System Properties > Environment Variables > Edit User PATH > New > `%USERPROFILE%\.local\bin`, then restart PowerShell |
| Browser does not open on login | Press `c` to copy the login URL, paste it in your browser |
| Subscription required / authentication fails | Verify you have an active Claude Pro or Max subscription at https://claude.ai. Log out and log back in to refresh credentials |
| Node version too old | Run `node --version` to check. If below v18.0.0, download the latest LTS version from https://nodejs.org |
| "Git Bash not found" error | Install Git for Windows from https://git-scm.com/downloads/win, or set the path manually (see Section 11) |
| Permission errors during install | You do NOT need to run as Administrator. The installer puts the binary in your user profile directory. If you still get permission denied, right-click PowerShell and select "Run as Administrator" |
| WinGet update not available yet | Claude Code may notify you of updates before WinGet has the new version. Wait and try again later |

For more help: https://code.claude.com/docs/en/troubleshooting

---

## Source

All instructions verified against the official Claude Code documentation at https://code.claude.com/docs/en/overview and https://code.claude.com/docs/en/setup (accessed March 2026).
