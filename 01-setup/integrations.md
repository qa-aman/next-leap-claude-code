# Claude Code Integrations Setup

## Atlassian (Jira + Confluence)

Connects Claude Code to your Atlassian Cloud site. You can create Confluence pages, search/create Jira tickets, and more - all from the terminal.

**Source:** [Claude Code MCP docs](https://code.claude.com/docs/en/mcp)

---

### What You Get

| Product | What you can do |
|---------|----------------|
| Jira | Search issues, create/update tickets, bulk create from specs |
| Confluence | Create pages, summarize existing pages, navigate spaces |
| Compass | Create components, query dependencies |

All actions respect your existing Atlassian permissions.

---

### Setup Steps

**Step 1: Add the Atlassian MCP server**

Run this in your terminal (outside Claude Code):

```bash
claude mcp add --transport http atlassian https://mcp.atlassian.com/v1/mcp
```

**Step 2: Verify it was added**

```bash
claude mcp list
```

You should see `atlassian` in the list with status "Needs authentication."

**Step 3: Authenticate**

Start a new Claude Code session and run `/mcp` inside it. This opens your browser with Atlassian's OAuth login page.

- Log in with the Atlassian account you want to use
- Authorize Claude Code to access your Jira and Confluence
- If you have multiple Atlassian accounts, log out of all accounts first at https://id.atlassian.com, then sign in with the correct one before authorizing

**Step 4: Confirm connection**

Run `claude mcp list` again. The atlassian entry should now show "Connected."

---

### Useful Commands

```bash
# Check all MCP server status
claude mcp list

# Check status inside Claude Code
/mcp

# Remove the server if needed
claude mcp remove atlassian

# Get server details
claude mcp get atlassian
```

---

### Troubleshooting

| Problem | Fix |
|---------|-----|
| "Needs authentication" after setup | Run `/mcp` inside Claude Code to trigger the OAuth flow |
| OAuth opens wrong Atlassian account | Log out at https://id.atlassian.com first, sign in with correct account |
| "Failed to connect" | Check your internet connection, try `claude mcp remove atlassian` and re-add |
| Duplicate Atlassian entries in `claude mcp list` | Claude Code plugins may auto-add Atlassian. Remove duplicates with `claude mcp remove` |
