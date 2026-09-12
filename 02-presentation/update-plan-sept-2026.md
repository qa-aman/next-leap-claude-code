# Update Plan for the September 2026 Batch

Prepared 12-09-2026. Covers what happened in the August 2026 cohort, what learners asked, what changed in Claude Code and the Claude model lineup after 15-08-2026, and which MD and HTML files in `01-setup/` and `02-presentation/` need updating before the next sessions. PPTX files are out of scope and were not touched.

**Sources read for this plan**

1. All 8 August session summaries in `.local/session-transcripts/august-2026/` (01-08, 02-08, 08-08, 15-08-2026).
2. `02-presentation/q&a.md`, August entries Q168 to Q282.
3. `01-setup/mac-setup.md`, `01-setup/windows-setup.md`, `01-setup/integrations.md`, `01-setup/guided-prompts.md`.
4. All 9 HTML decks and `important-links-and-documents.md` in `02-presentation/`.
5. Claude Code changelog, v2.1.234 (17-08-2026) to v2.1.269 (11-09-2026): https://github.com/anthropics/claude-code/blob/main/CHANGELOG.md, release dates from the GitHub releases API.
6. Official docs, fetched as raw markdown on 12-09-2026: https://code.claude.com/docs/en/setup, https://code.claude.com/docs/en/troubleshoot-install, https://code.claude.com/docs/en/commands, https://code.claude.com/docs/en/memory, https://code.claude.com/docs/en/skills, https://code.claude.com/docs/en/agent-teams, https://code.claude.com/docs/en/model-config, https://code.claude.com/docs/en/vs-code, https://code.claude.com/docs/en/desktop-quickstart.
7. Anthropic: https://www.anthropic.com/claude-fable-and-mythos-5-1 (01-09-2026) and https://platform.claude.com/docs/en/about-claude/models/overview.

All URLs above returned HTTP 200 on 12-09-2026.

---

## 1. What happened in August 2026

Eight sessions across three weekends, all on the MeetFlow workshop repo, then a real build in the last two.

| # | Date | Topic | Attendance | Rating |
|---|---|---|---|---|
| 1 | 01-08-2026 AM | Install on Mac and Windows, Pro purchase, login, clone repo, 11 plugins, CLAUDE.md as orchestration, `/init` on an empty folder | 3 | 7/10 |
| 2 | 01-08-2026 PM | Global vs project vs subfolder CLAUDE.md, memory, what a skill is, live ServiceNow ticket-analysis skill built from Kartik's real problem, work-log and session-debrief skills | 3 to 4 | 7.5/10 |
| 3 | 02-08-2026 AM | `ux-designer` skill built from first-party design sources, Shailendra's resume-tailor skill, 200-line SKILL.md rule, portable global CLAUDE.md | 1 | 6/10 |
| 4 | 02-08-2026 PM | Resume skill re-tested on a second JD, ATS tracker, `improvements.md`, first agent (`code-improver`) built by prompt, `/agents` wizard gone, agent memory, MCP vs API | 2 | 7/10 |
| 5 | 08-08-2026 AM | Opus 5 prompting change (goal plus guardrails, not steps), `/doctor`, skill vs agent settled, five MeetFlow agents built, routing agent, evals as checklists, usage windows | 6 | 7/10 |
| 6 | 08-08-2026 PM | `/insights` on a real project, auto mode as default, `claude agents` view, agent teams demo on a PRD, `ccs` session registry, dynamic workflows, skill vs rule | 2 | 7/10 |
| 7 | 15-08-2026 AM | Build hours: job scraper from an empty folder, brainstorm to design to phase 0, API selection, `decisions.md`, Docker, gitignore for personal data | 2 | 8/10 |
| 8 | 15-08-2026 PM | Phases 1 to 5 of the job scraper, per-phase evaluation criteria, `/compact` discipline, tailored resume shipped with a known defect | 2 | 7/10 |

**The three facts that matter for the next batch**

1. Attendance collapsed from 103 enrolled to a ceiling of six and a floor of one. The learners themselves raised it. The cause they were given: the PM half of the combined cohort left. The next batch is 71 people across engineering, product, design, analytics, ops, HR, support, finance and students, so the material must stop assuming PMs.
2. Windows produced every environment failure in Session 1 (SSH clone denied, screenshot paste into the terminal not working, no status line) and none were fixed in the room. They compounded across three sessions. The debriefs flagged "clear the Windows blockers before teaching anything new" three times.
3. Every debrief from Session 4 onward flagged the same gap: the thing that was built was not run on a real input in the same session. The one session that did this (Session 7) scored highest.

## 2. What learners asked

115 questions were logged across the eight sessions (Q168 to Q282 in `q&a.md`). Grouped by theme, with the ones that recurred in more than one session marked.

| Theme | Recurring questions | Sessions |
|---|---|---|
| Fit for non-developers | "Is this only for engineers?", "Is Claude Code in the same bucket as Cursor?", "Do I need two subscriptions?", "Would Antigravity or Copilot do the same?" | 1, 2, 3, 5 |
| Install and billing | Why a terminal command and not an `.exe`, GST on Pro purchase, monthly vs annual, PATH not found on Windows, SSH vs HTTPS clone, screenshot paste failing on Windows | 1, 8 |
| Models, effort, cost | Which model to default to, what effort level, what the 5-hour and 7-day windows mean, what the dollar figure in the status line means, "is it only Opus that takes goals not steps" | 1, 4, 5, 6 |
| CLAUDE.md vs memory | Global vs project vs subfolder, README vs CLAUDE.md, "is memory just the global CLAUDE.md", is memory automatic, "should I run `/init` every session" | 1, 2, 5, 7 |
| Skill vs agent vs sub-agent | Asked in every session from 2 to 8. "Is sub-agent a third thing?", "which do I build first?", "do skills have memory?" | 2, 4, 5, 6, 7 |
| Terminal and session hygiene | Terminals vanish when the editor closes, how to rename tabs, when to `/compact`, Shift+Enter not working, `Ctrl+O` to see background work | 2, 5, 6, 7, 8 |
| Agent teams and workflows | How to enable, difference from sub-agents, difference from dynamic workflows, hierarchy of teams, why 30 agents ran when I built 4 | 6 |
| MCP vs API | "MCP is not clear to me" three sessions in a row, then settled in Session 7 with the bike-key analogy | 4, 5, 7, 8 |
| Shipping their own build | Public vs private repo, keeping resume and API keys out of git, Docker on Windows, installing a community skill from GitHub | 4, 7, 8 |

**Teaching claims made in August that the official docs now contradict.** These need correcting in the decks and in `q&a.md` before they are repeated to 71 people.

| Claim made in August | What the official docs say on 12-09-2026 | Source |
|---|---|---|
| "CLAUDE.md beyond 500 lines is not read" (Session 1, Q177) | Target under 200 lines. A file is skipped only when it is over 4 MiB. Longer files load in full but reduce adherence. | https://code.claude.com/docs/en/memory (section "My CLAUDE.md is too large") |
| "Memory is not automatic, you have to say keep this in memory" (Session 5, Q225) | Auto memory is on by default. Claude writes `user`, `feedback`, `project` and `reference` notes itself. Telling Claude "remember that ..." still forces an entry, and `/memory` browses them. The `#` shortcut taught in August was removed in v2.0.70 and should not be taught. | https://code.claude.com/docs/en/memory (section "Auto memory") |
| "Run `/reload-plugins` after installing plugins" (Session 1 action item, Q176) | Since v2.1.268 (10-09-2026), a plugin install, enable or disable takes effect when you close the `/plugin` menu. `/reload-plugins` is no longer needed. | Changelog v2.1.268 |
| "Enable agent teams with `experimental_agent_teams` in settings.json, and the prompt must say create an agent team" (Session 6, Q244) | The setting is `CLAUDE_CODE_EXPERIMENTAL_AGENT_TEAMS=1` in `settings.json` env or the shell. Once enabled, Claude may form a team on its own when it names a subagent, even if you did not ask. | https://code.claude.com/docs/en/agent-teams |
| "adviser" setting (Session 1, Q178) | The command is `/advisor [model\|off]`, spelled with an o. It consults a second model at key moments. | https://code.claude.com/docs/en/commands |
| "Once is a prompt, twice is a skill" (Session 2) vs "3-Repeat Rule" (Skills deck slide 10) | Docs give no number. They say: create a skill when you keep pasting the same instructions, or when a CLAUDE.md section has become a procedure. Pick one rule and use it everywhere. | https://code.claude.com/docs/en/skills |
| "Git for Windows is required on native Windows" (Setup deck slide 5, error 4) | Git for Windows is optional. Without it Claude Code uses the PowerShell tool. | https://code.claude.com/docs/en/setup (section "Set up on Windows") |

## 3. What changed after 15-08-2026

### 3.1 Models

| Date | Change | What it means for the batch |
|---|---|---|
| 01-09-2026 | Claude Fable 5.1 released (and Claude Mythos 5.1, same model with different safeguards). Fable 5.1 is the new `fable` alias in Claude Code v2.1.257+. Anthropic estimates about 25% less than Fable 5 for typical workloads, list price unchanged. Not the default on any plan. | The model slide is now: Haiku 4.5, Sonnet 5, Opus 5, Fable 5.1. Default recommendation for a Pro plan stays Sonnet 5 with effort set to medium (the built-in effort default is high). Opus 5 is the default model on Max, Team Premium, Enterprise and the API. Fable is opt-in with `/model fable`. |
| v2.1.243 (no GitHub release, between 23-08 and 25-08-2026) | Sonnet 5 pricing shown as the standard $2/$10 per Mtok, no longer a promo | Only matters for API users. |
| 26-08-2026 (v2.1.247) | Sonnet 5 auto-compact window is now its full 1M context | Sessions on Sonnet 5 compact much later. The "compact at 30 to 40 percent" guidance still holds. |

### 3.2 Claude Code (v2.1.234 on 17-08-2026 to v2.1.269 on 11-09-2026)

Only the items a beginner batch will meet. Version and release date in brackets.

1. **`/plugin` changes apply on menu close, no `/reload-plugins`** (v2.1.268, 10-09-2026). Removes one step from Session 1.
2. **`/skill-doctor`** (v2.1.261, 04-09-2026). Shows what each loaded skill costs in context and how often it is used. Directly answers Kartik's Session 8 finding that 70 percent of installed plugins were unused. Needs v2.1.252 or later.
3. **`/diff` panel** (v2.1.260, 03-09-2026). Opens beside the conversation in fullscreen mode and shows uncommitted changes as Claude edits. Good replacement for "open the file and look" in the setup session.
4. **`/focus`** (exists since v2.1.110, v2.1.269 only added a spinner tip pointing to it). A view with only your prompt, a one-line work summary and the response. Fullscreen renderer only. Useful for a projector.
5. **`/advisor` text form** (v2.1.260). `/advisor`, `/advisor <model>`, `/advisor off`.
6. **Auto mode changes.** Bash permission prompts now offer a one-keystroke "Yes, and switch to auto mode" (v2.1.247, 26-08-2026). `/permissions` has an Auto mode tab for classifier rules (v2.1.246). Auto mode asks once before the first file read outside the working directory (v2.1.257). Denial messages now name the rule that blocked the action (v2.1.268). This explains the Session 6 and 8 confusion where a config change was blocked and a three-option prompt appeared.
7. **"Concise" output style** (v2.1.237, 20-08-2026) and `/output-style [name]` (v2.1.269). Claude leads with results and skips narration. Worth setting for a cohort watching a projector.
8. **`SendFeedback` tool and `/feedback` drafts** (v2.1.247). When something goes wrong, Claude drafts a feedback report you review before sending.
9. **`/usage` Loops breakdown** (the docs say v2.1.242, the changelog lists it under v2.1.243, neither has a GitHub release): per-loop run count and tokens, so a chatty `/loop` is visible.
10. **Agent teams: "Default teammate model" removed from `/config`** (v2.1.234). Teammates use the leader's model unless the spawn names one.
11. **`ANTHROPIC_DEFAULT_MODEL`** env var (v2.1.236) sets the model new sessions start on. A `/model` pick still overrides it.
12. **`/import cursor`** now exists in the commands reference. It brings Cursor configuration (instruction files, MCP servers, commands, subagents, skills) into Claude Code. Directly relevant to learners like Kartik who arrive with a Cursor project. Also `/init` offers `/import` when it finds Codex or Gemini CLI config.
13. **Task-tracking tools (TodoWrite) are no longer offered on Claude 5 models.** First removed in v2.1.233 (14-08-2026, the day before the last August session), restated in v2.1.268. The visible to-do list learners saw in August will not appear on Sonnet 5 or Opus 5 unless `CLAUDE_CODE_ENABLE_TODO_TOOLS=1` is set.
14. **Shift+Enter** is native in iTerm2, WezTerm, Ghostty, Kitty, Warp, Apple Terminal and Windows Terminal per the interactive-mode docs. The Session 5 answer ("took 10 to 15 iterations") should be replaced with: use one of those terminals, or follow https://code.claude.com/docs/en/terminal-config.
15. **Windows fixes**: PowerShell tool background commands no longer stop when Claude Code exits (v2.1.269), `claude agents` keyboard fix on Windows (v2.1.248), and a VS Code fix for pasting screenshots on WSL2 (v2.1.267). The native-Windows terminal screenshot-paste failure from Session 1 has no changelog entry, so it is still an open item to test in the room.

### 3.3 Docs changes that affect the setup guides

1. The npm package now requires **Node.js 22 or later** (docs, setup page, "as of v2.1.198"). Both setup guides say v18.
2. Docs say **do not use `sudo npm install -g`**. `mac-setup.md` currently tells the reader to try `sudo curl ... | bash` as a last resort.
3. Docs say **avoid `npm update -g`**, use `npm install -g @anthropic-ai/claude-code@latest`. `mac-setup.md` recommends `npm update -g`.
4. The **CMD vs PowerShell mix-up** is now the first item in the official Windows troubleshooting ("`irm` is not recognized", "`&&` is not valid", "`bash` is not recognized"). Neither setup guide nor the setup deck covers it. This was the Google Doc's Windows failure from earlier batches.
5. **`winget install Anthropic.ClaudeCode`** is the official curl-free fallback. Only `windows-setup.md` mentions it, and only as an alternative, not as the fallback when the script fails.
6. The **Windows desktop app download** URL in the docs is now `.../win32/x64/setup/latest/redirect`. `windows-setup.md` has `.../win32/x64/exe/latest/redirect`. Both return 403 to automated checks, so link to https://code.claude.com/docs/en/desktop-quickstart instead of the raw redirect.
7. The docs say the VS Code extension "also installs in other VS Code forks" via the editor's Extensions view or **Open VSX** (https://open-vsx.org/extension/Anthropic/claude-code). Antigravity is not named anywhere in the official docs. The claim in both setup guides and the setup deck that "Antigravity supports the VS Code extension marketplace, so the extension installs without additional configuration" is not from Anthropic. Test it before the session and add the Open VSX path as the fallback.
8. `/agents` no longer opens a wizard as of v2.1.198 (01-07-2026). Two decks still tell learners to open it.
9. The official **terminal guide** (https://code.claude.com/docs/en/terminal-guide) now exists for people new to the terminal, with Windows and macOS troubleshooting sections. Worth linking from the setup guides for this non-developer batch.

## 4. File-by-file update list

Priority: **P0** = before tomorrow's Session 1, **P1** = before Session 2 or 3, **P2** = before the agents and multi-agent sessions.

### `01-setup/`

| File | Priority | Change |
|---|---|---|
| `windows-setup.md` | P0 | 1. Add a section "Wrong terminal" right after Step 1: if you see `irm is not recognized`, `&& is not valid` or `bash is not recognized`, you are in CMD or ran the Mac command, open PowerShell and re-run. Source: troubleshoot-install. 2. Add the npm fallback with `Set-ExecutionPolicy -Scope CurrentUser -ExecutionPolicy RemoteSigned` then `npm install -g @anthropic-ai/claude-code` (from the Google Doc, matches docs), and promote winget to "fallback when the script fails". 3. Node requirement v18 to v22. 4. Troubleshooting row "Git Bash not found" points to Section 11, should be Section 10. 5. Add clipboard and screenshot paste on native Windows as a known issue with the workaround to test (drag the image file into the terminal, or use the VS Code extension). 6. Add SSH vs HTTPS clone: use the HTTPS URL, SSH keys are optional. 7. Desktop app link to desktop-quickstart page, not the raw redirect. 8. Antigravity section: add Open VSX fallback and mark as "verified in the room on <date>" only after testing. 9. Prerequisites: Windows 10 1809 or later. 10. Source footer: "accessed March 2026" to 12-09-2026. |
| `mac-setup.md` | P0 | 1. Remove the `sudo curl ... \| bash` advice, docs say never use sudo. 2. `npm update -g` to `npm install -g @anthropic-ai/claude-code@latest`. 3. Node v18 to v22. 4. Version example `2.0.30` to `2.1.2xx`. 5. Add "close and reopen the terminal before `claude --version`" as step 3, since it fails inside the install session (Session 1 finding). 6. Homebrew: note the two casks, `claude-code` (stable) and `claude-code@latest`. 7. Antigravity section: same Open VSX note as Windows. 8. Source footer date. |
| `integrations.md` | P2 | No factual errors found. Add `/import cursor` for learners arriving with a Cursor setup. |
| `guided-prompts.md` | P1 | Prompts still valid against the repo. Add one line at the top: "no coding background needed", since the new batch is mostly non-engineers. |
| NEW `windows-one-page-card.md` (optional) | P0 | The Session 1 debrief asked for it: PowerShell not CMD, PATH line, HTTPS clone, clipboard. One screen. The Substack setup post already drafted in `outputs/sept-2026-cohort/` covers most of this and can be the public version. |

### `02-presentation/`

| File | Priority | Change |
|---|---|---|
| `Claude-Code-Setup.html` | P0 | 1. Slide 5 "Five errors": replace error 4 (Git Bash required) with the CMD vs PowerShell mix-up, and add winget as the fallback in error 5. 2. Slide 9 modes: add that auto mode now offers "Yes, and switch to auto mode" on a Bash prompt, and asks once before reading outside the working folder. 3. Slide 12 "CLAUDE.md vs Memory": rewrite Memory as auto memory (Claude writes it, four note types, "remember that ..." and `/memory` for manual; drop the `#` shortcut, removed in v2.0.70), and drop "Anthropic split memory out of CLAUDE.md". 4. Slide 16 Antigravity: soften to "VS Code forks, install from the Extensions view or Open VSX", add Cursor as officially supported. 5. Slide 8 commands: add `/diff`, `/focus`, `/skill-doctor`. 6. Add a "which model" slide: Sonnet 5 medium effort default on Pro, Opus 5 for review passes, Fable 5.1 opt-in. 7. Subtitle "Claude Code for PMs" wherever it appears: this batch is not PMs. |
| `claude-code-commands-reference.html` | P1 | 1. "Updated 11-07-2026" to 12-09-2026. 2. `/agents` row: no longer opens a wizard, it prints a reminder to ask Claude or edit `.claude/agents/`. 3. Add `/skill-doctor`, `/diff`, `/focus`, `/output-style`, `/advisor`, `/import`. 4. `/plugin` row: no `/reload-plugins` needed after v2.1.268. 5. `/model` row: model list is haiku, sonnet, opus, fable, with `fable` now resolving to Fable 5.1. |
| `Claude-Code-Skills.html` | P1 | 1. Slide 10 "3-Repeat Rule" vs the "twice is a skill" taught in August: pick one. Docs give no number. 2. Slide 9 "500-line" rule for SKILL.md matches the docs tip, keep it. But the same 500 number was taught for CLAUDE.md, which is wrong (200-line target, 4 MiB cut-off). Add one line separating the two. 3. Add `/skill-doctor` as the way to find unused skills. 4. Subtitle "Senior Product Manager" byline: keep or change per the batch. |
| `Claude-Code-Agents.html` | P2 | Slides 14 to 16 say "Use `/agents` to create one interactively". Replace with "ask Claude to create an agent, or write the file in `.claude/agents/`". Add the `memory:` frontmatter field, which August learners asked about in Sessions 4 and 5. |
| `Multi-Agent-Architectures.html` | P2 | 1. The "Try it now" steps say run `/agents`, switch to the Library tab, Create new agent. Wizard is gone since v2.1.198. 2. Agent teams: setting is `CLAUDE_CODE_EXPERIMENTAL_AGENT_TEAMS=1`, teammates now use the leader's model, and Claude can form a team without being asked once enabled. 3. Add `/skill-doctor` and `/usage` Loops breakdown to the cost section. |
| `Five-Agent-Patterns.html` | P2 | Already notes the `/agents` wizard is gone. Only change: model names where "fable" appears now mean Fable 5.1. |
| `claude-code-beyond-the-sessions.html` | P1 | Header says "Checked against CHANGELOG v2.1.220, compiled 01-08-2026". Re-check against v2.1.269. Section 4 "Models": add Fable 5.1 (01-09-2026). Add `/skill-doctor`, `/diff`, `/focus`, Concise output style, `SendFeedback`. |
| `important-links-and-documents.md` and `.html` | P1 | All 58 links return 200 (LinkedIn 999). Changes: 1. Add https://code.claude.com/docs/en/terminal-guide under Getting Started. 2. Add https://code.claude.com/docs/en/troubleshoot-install. 3. Add the Fable 5.1 announcement and the models overview page. 4. Decide the Substack URL: file says `amanparmar3.substack.com`, your config says `shipwithailab.substack.com`. 5. Retitle from "Claude Code for PMs" to a role-neutral title. |
| `q&a.md` | P1 | Correct Q176 (`/reload-plugins` no longer needed), Q177 (500-line claim, replace with 200-line target and 4 MiB cut-off), Q178 (`/advisor` spelling and current behaviour), Q225 (auto memory is on by default), Q244 (agent teams setting name). Add a "September 2026 pre-read" block with the CMD vs PowerShell answer, since it will be asked tomorrow. |

### Not changed

1. All `.pptx` files, as instructed.
2. `Building-Effective-AI-Agents.pptx` and the Anthropic "Building Effective Agents" pattern content, which has no changes.

## 5. Order of work

1. **Tonight, before Session 1 (P0):** `windows-setup.md`, `mac-setup.md`, `Claude-Code-Setup.html` slides 5, 9, 12, 16. Test the Antigravity extension install once on your own machine and record the result in the guide. Test screenshot paste on a native Windows terminal if a Windows machine is available.
2. **Before Session 2 or 3 (P1):** commands reference, Skills deck, `q&a.md` corrections, links file, beyond-the-sessions deck.
3. **Before the agents sessions (P2):** Agents deck, Multi-Agent deck, `integrations.md`.

## 6. Two structural changes worth making for this batch

1. **Open Session 1 with the answer to "is this only for engineers".** It was the first question in August and it will be the first question again with 71 mixed-role learners. The August answer (marketing, sales, design, product and service management equally, plus the ticket-report example: 4 to 5 hours down to 15 minutes) worked. Put it on slide 2 rather than waiting for the question.
2. **Run what was built, in the session, on a fresh input.** Four consecutive August debriefs flagged this. Session 7, the only one that did it, was the highest rated. Make it the closing step of every build session, not an intention.
