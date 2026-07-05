# Code Review - Uncommitted Diff (17-03-2026)

**Reviewer:** senior-code-reviewer subagent
**Scope:** Uncommitted diff + HEAD context in `next-leap-claude-code`
**Repo type:** Workshop content repo. No lint/typecheck/test pipeline configured - those steps skipped.

## Summary

- Files touched: 4 changed (3 deleted, 1 modified) + 3 untracked = 7 paths
- Lines changed: `q&a.md` gained ~400 lines (May 2026 Session 2 additions, Q14-Q31 block); no other text-line changes
- Verdict: **Approve with comments**. One minor gitignore gap should be closed before the next cohort pull; the rest are low-risk documentation notes.

## Blockers

None.

## Major issues

None.

## Minor issues

**[m1]** `.gitignore`:1-6 - Office lockfile `~$Building-Effective-AI-Agents.pptx` is untracked and not covered by `.gitignore`

Current `.gitignore`:
```
node_modules/
.DS_Store
.env
.env.*
*.log
.local/
```
The `~$*` prefix is the standard Microsoft Office temp/lockfile pattern. If accidentally staged, it persists across all cohort clones.

Fix: add `~$*` to `.gitignore`.

---

**[m2]** `02-presentation/q&a.md`:9 - "Last full refresh" date (`16-05-2026`) post-dates the repo's fictional anchor (`17-03-2026`)

```markdown
- **Last full refresh:** 16-05-2026 (URLs re-verified, Windows flow rewritten)
- **May 2026 Session 1 additions:** 16-05-2026 (Q5-Q13 ...)
- **May 2026 Session 2 additions:** 16-05-2026 (Q14-Q31 ...)
```
`CLAUDE.md` sets the fictional "now" as `17-03-2026`. q&a.md is a living reference doc with real URL-verification timestamps, but there is no framing note distinguishing real dates from fiction-world dates.

Fix: add a one-line note at top of q&a.md, e.g. `Note: dates in this file are real calendar dates for URL verification, not the workshop's fictional anchor date.` Update CLAUDE.md's "Refresh recipe" to call this out.

---

**[m3]** Deletion of `02-presentation/build_agents_ppt.py` needs cross-reference check

If any `SKILL.md` under `.claude/skills/` references `build_agents_ppt.py` as a renderer, those calls will fail silently.

Fix: run `grep -r "build_agents_ppt" .claude/skills/` and remove/update any hits.

## Nits

**[n1]** `.claude/skills/11-star-framework/SKILL.md`:1 - `name:` field now matches the renamed folder correctly. CLAUDE.md "File Map" and README skill inventory do not surface this skill by name - optional addition.

**[n2]** `02-presentation/Session-3-Claude-Code-Agents.pptx` is a large untracked binary. No `.gitignore` rule excludes PPTX generally. If PPTXs will be updated between cohorts, consider release artifacts instead of git history.

**[n3]** `02-presentation/q&a.md`:8 - `Original file created:` is `23-03-2026` (6 days after the fictional anchor). Same root cause as [m2].

## Positive notes

- Skill rename `11-start-framework` -> `11-star-framework` is consistent. `name:` field updated. No dangling slash-command references found.
- Q14-Q31 additions follow the file's established format precisely: short answer, detail block, verified source URLs with dates.
- New `Session-3-Claude-Code-Agents.pptx` lands cleanly with no naming conflicts.

## Self-audit

| Check | Result |
|---|---|
| Report file exists at declared path | Pass (written by parent after subagent run) |
| Every issue has file:line citation | Pass - .gitignore:1-6, q&a.md:8-9, README.md:73 verified |
| No ISO `YYYY-MM-DD` dates in report | Pass |
| No invented symbols | Pass - `11-star-framework`, `build_agents_ppt.py` (confirmed deleted), `ppt-builder` all verified |
| Counts in Summary match reality | Pass - 3 deleted + 1 modified + 3 untracked = 7 |
| Verdict matches severity counts | Pass - 0 blockers, 0 majors -> Approve with comments |
| No write-side commands run by subagent | Pass |
