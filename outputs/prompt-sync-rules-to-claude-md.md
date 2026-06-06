# Sync .claude/rules References into CLAUDE.md

This prompt produces one surgical edit to the project's `CLAUDE.md`: a reference table listing every rule file in `.claude/rules/`, so anyone reading CLAUDE.md can discover all path-specific rules without opening the folder. The consumer is the project owner (a Senior PM) and future workshop cohorts reading CLAUDE.md as the repo's front door.

Discipline rule: surgical edit only. Touch nothing in CLAUDE.md outside the Rules section. Do not rewrite, reorder, or "improve" any other section. Do not modify any file inside `.claude/rules/`.

## Goal

- Done when every `.md` file present in `/Users/amanparmar/Documents/AI-PM/Projects/next-leap-claude-code/.claude/rules/` is referenced by exact filename in `/Users/amanparmar/Documents/AI-PM/Projects/next-leap-claude-code/CLAUDE.md`, and the verification loop in the Verification section reports `MISSING: 0`.

## Inputs

- Directory: `/Users/amanparmar/Documents/AI-PM/Projects/next-leap-claude-code/.claude/rules/` - Markdown files with YAML frontmatter containing a `paths:` list. Snapshot as of 06-06-2026 (6 files, re-derive at runtime, do not trust this list blindly):
  - `feature-writing.md` (paths: `08-product-features/**`)
  - `outputs.md` (paths: `outputs/**`)
  - `product-knowledge.md` (paths: `03-product-knowledge/**`)
  - `prompt-writing.md` (paths: `outputs/*prompt*.md`, `outputs/**/prompt*.md`, `prompts/**`)
  - `ui-design-quality.md` (paths: `15-prototype/**`, `**/ux-zone/**/*.tsx`, `**/prototype/**/*.tsx`)
  - `user-research.md` (paths: `05-user-personas/**`, `06-user-feedback/**`, `07-user-interviews/**`)
- File to edit: `/Users/amanparmar/Documents/AI-PM/Projects/next-leap-claude-code/CLAUDE.md` (~69 lines). The Rules section starts at the `## Rules` heading. The line "Path-specific rules live in `.claude/rules/`..." is the anchor to extend.

## Outputs

- Edited file: `/Users/amanparmar/Documents/AI-PM/Projects/next-leap-claude-code/CLAUDE.md`, same path, edited in place with the Edit tool (never Write/overwrite).
- New content: one Markdown table under the `## Rules` section with exactly one row per rule file. Columns: `Rule file` (as a relative link, e.g. `[.claude/rules/outputs.md](.claude/rules/outputs.md)`), `Applies to` (the frontmatter `paths` globs, comma-separated), `What it enforces` (one line, max 15 words, taken from the file's own content, not invented).
- Size budget: the table plus an optional one-line lead-in, no more than 12 added lines total. Net change to CLAUDE.md is additive only.
- Side effects: none. No other files created or modified. No commits.

## Context the executor needs

- This is a workshop repo for "Claude Code for PMs". CLAUDE.md is the always-loaded project memory; `.claude/rules/` files load automatically only when matching paths are touched, which is why CLAUDE.md must index them for discoverability.
- `prompt-writing.md` is already named in an existing Rules bullet (the "create a prompt" trigger line). Keep that bullet untouched; the table row for `prompt-writing.md` is additional, not a replacement.
- Assumption: rule filenames are stable. If a rule file has no `paths:` frontmatter, write `always check manually` in the Applies to column rather than guessing globs.

## Tools / skills / models

- Bash `ls /Users/amanparmar/Documents/AI-PM/Projects/next-leap-claude-code/.claude/rules/*.md` to derive the authoritative file list at runtime.
- Read tool on each rule file to extract frontmatter `paths` and the one-line purpose. Read CLAUDE.md in full before editing.
- Edit tool for the CLAUDE.md change. No skills or subagents needed. Any model tier handles this; Haiku-class is sufficient.

## Constraints (non-negotiable)

1. No em dashes anywhere in added text. Check: `grep -c '—' CLAUDE.md` returns the same count after the edit as before (currently the title line contains one pre-existing em dash; do not add more).
2. No emojis. Check: visual scan of the diff.
3. All dates, if any are written, use DD-MM-YYYY. Check: `grep -E '[0-9]{4}-[0-9]{2}-[0-9]{2}' CLAUDE.md` matches nothing new.
4. Do not invent rule purposes. Every "What it enforces" line must paraphrase text actually present in that rule file. Check: for each row, the key noun (e.g. "personas", "metrics", "citations") appears in the source rule file via grep.
5. Edit, do not recreate. Check: `git diff --stat CLAUDE.md` shows one file changed, insertions only or near-only, zero files added.
6. Added content stays inside the `## Rules` section, above the next `##` heading. Check: `git diff CLAUDE.md` hunk headers all fall between `## Rules` and `## Time Convention`.
7. Total addition under 500 words (project rule: ask before writing more). The 12-line table is well under; if your draft exceeds 500 words, stop and ask.

## Process (strict order)

1. `ls` the rules directory. Build the authoritative list of `.md` files.
2. Read each rule file. Extract: frontmatter `paths` globs and a max-15-word purpose line from its body.
3. Read CLAUDE.md in full. Locate the `## Rules` section and the existing "Path-specific rules live in `.claude/rules/`" bullet.
4. Draft the table. Present the exact proposed diff (before/after of the Rules section) to the user.

### AWAITING APPROVAL

5. After approval, apply the edit with the Edit tool, extending the existing path-specific-rules bullet with the table directly beneath it.
6. Run the Verification section. Report results verbatim.

## Verification (run before handing back)

1. Completeness loop, expected output `MISSING: 0`:
   ```bash
   cd /Users/amanparmar/Documents/AI-PM/Projects/next-leap-claude-code
   missing=0; for f in .claude/rules/*.md; do
     grep -q "$(basename "$f")" CLAUDE.md || { echo "missing: $f"; missing=$((missing+1)); }
   done; echo "MISSING: $missing"
   ```
2. `git diff CLAUDE.md` - confirm the only hunk is inside the Rules section and is additive.
3. Constraint checks 1-4 from the Constraints section, each run as written.
4. Self-audit against the failure modes below; state explicitly that each was checked.

## Failure modes to defend against

1. **Stale snapshot**: trusting the 6-file list in this prompt instead of re-listing the directory. Defense: step 1 is mandatory; the `ls` output is authoritative.
2. **Invented purposes**: summarizing a rule file from its filename without reading it. Defense: constraint 4 grep check per row.
3. **Overwrite instead of edit**: regenerating CLAUDE.md wholesale and losing sections. Defense: Edit tool only, constraint 5 git diff check.
4. **Duplicate reference**: adding a second `prompt-writing.md` bullet or rewriting the existing trigger bullet. Defense: existing bullet is explicitly preserved; table is the only addition.
5. **Wrong section placement**: table lands under Quick Tasks or Time Convention. Defense: constraint 6 hunk-position check.
6. **Forbidden punctuation drift**: em dashes or ISO dates sneaking into the table. Defense: constraints 1 and 3 greps.
7. **Skipping the approval gate**: editing CLAUDE.md before the user sees the diff. Defense: hard `### AWAITING APPROVAL` marker; no Edit call before it.
8. **Broken relative links**: linking `rules/outputs.md` instead of `.claude/rules/outputs.md`. Defense: verify each link target exists with `test -f` before delivering.

## Audience

- Reader of the edited CLAUDE.md: PMs in a Claude Code workshop, non-engineers. Table must be plain: no glob jargon beyond the literal patterns, no YAML terminology. "Applies to" values are shown as-is since they are paths the reader can recognize from the File Map.

---

Start by running `ls /Users/amanparmar/Documents/AI-PM/Projects/next-leap-claude-code/.claude/rules/*.md` to build the authoritative rule-file list.
