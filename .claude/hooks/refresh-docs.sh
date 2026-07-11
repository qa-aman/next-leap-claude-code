#!/usr/bin/env bash
# Stop hook: auto-refresh CLAUDE.md + README.md when project source files change.
#
# Behavior (chosen by the user): AUTO-REWRITE. After a turn that changed source
# files but left the docs untouched, this spawns a cheap, hooks-disabled,
# non-interactive `claude -p` run that updates the two docs from the git diff.
#
# Guards against the two failure modes of that approach:
#   1) Self-trigger loop  -> CLAUDE_DOCS_REFRESH env guard + --settings disableAllHooks
#   2) Needless cost       -> only runs when meaningful source changed AND docs untouched
#
# To dry-run/test without a real model call: set CLAUDE_DOCS_BIN=echo
set -uo pipefail

# 1) Loop guard: never run inside our own spawned child.
[ -n "${CLAUDE_DOCS_REFRESH:-}" ] && exit 0

# 2) Must be inside the git repo.
ROOT="$(git rev-parse --show-toplevel 2>/dev/null)" || exit 0
[ -z "$ROOT" ] && exit 0
cd "$ROOT" || exit 0

# 3) Collect changed paths (tracked + untracked; gitignored dirs like .local/ are excluded by git).
changed="$(git status --porcelain 2>/dev/null | cut -c4-)"
[ -z "$changed" ] && exit 0

# 4) If the docs were already edited this cycle, assume it was handled -> skip (also debounces re-runs).
printf '%s\n' "$changed" | grep -qxE 'CLAUDE\.md|README\.md' && exit 0

# 5) Meaningful source = changed files minus generated/noise paths.
meaningful="$(printf '%s\n' "$changed" | grep -vE '^(outputs/|node_modules/|.*/node_modules/|.*\.log$|\.claude/settings|\.claude/claude-sessions-registry\.md|.*-workspace/)')"
[ -z "$meaningful" ] && exit 0

# 6) Resolve the claude binary (a hook's PATH may not include ~/.local/bin).
CLAUDE_BIN="${CLAUDE_DOCS_BIN:-$(command -v claude 2>/dev/null || echo "$HOME/.local/bin/claude")}"
[ -x "$CLAUDE_BIN" ] || [ "$CLAUDE_BIN" = "echo" ] || exit 0

diff="$(git diff HEAD 2>/dev/null | head -c 12000)"

# 7) Spawn the guarded, hooks-disabled, conservative doc refresh.
CLAUDE_DOCS_REFRESH=1 "$CLAUDE_BIN" -p \
"Project source files just changed. Update CLAUDE.md and README.md ONLY where they are now inaccurate, stale, or missing something, based on the changes below. Be conservative: keep them concise, preserve their existing structure and voice, do not restructure, change nothing except those two files, and if nothing genuinely needs updating, make no edits at all.

Changed files:
$meaningful

Diff (truncated to 12k chars):
$diff" \
  --model sonnet \
  --permission-mode acceptEdits \
  --settings '{"disableAllHooks":true}' \
  >/dev/null 2>&1 || true

exit 0
