---
name: session-debrief
description: Process a completed NextLeap workshop session from a Granola link into (1) a session summary file under .local/session-transcripts/may-2026/ and (2) appended Q&A entries in 02-presentation/q&a.md. Trigger whenever the user says "session completed", "session done", "process this Granola session", "debrief this session", "new workshop session", or pastes a Granola URL alongside a request to update the transcripts folder and q&a doc. Also trigger when the user references the q&a.md file or session-transcripts folder in a "just-finished-the-class" context.
---

# Session Debrief - Workshop Granola -> Transcript Summary + Q&A Update

You convert a completed NextLeap Applied Generative AI Bootcamp session into two artifacts:

1. **A session summary** at `.local/session-transcripts/may-2026/session-<N>-<topic>-summary.md` (folder month may differ - match the host's current cohort window).
2. **Appended Q&A entries** in `02-presentation/q&a.md`, continuing the existing question numbering.

## When this skill fires

The user gives you a Granola link (notes.granola.ai/t/...) with a phrase like "session completed", "process this session", "update transcripts and q&a", or just the link with implicit context that they just finished teaching.

## Required inputs

- **Granola UUID** - extracted from the URL (the part after `/t/` and before any suffix). Example: `https://notes.granola.ai/t/9fb2ae8d-e2aa-415a-9518-9b2bd9dbeca3-008umkv4` -> UUID is `9fb2ae8d-e2aa-415a-9518-9b2bd9dbeca3`.
- **Today's date** - use the workshop's fictional "now" if the project is anchored to one (per `CLAUDE.md` -> `## Time Convention`). Otherwise use `currentDate` from system context. Always write dates as **DD-MM-YYYY**.

## Steps

### 1. Fetch the transcript

Use the Granola MCP tool to load the transcript:

```
mcp__claude_ai_Granola__get_meeting_transcript(meeting_id=<UUID>)
```

The result is usually 100k+ chars - it will be saved to a tool-results file. Read it in chunks with Python (`open(path).read()[start:end]`) rather than the Read tool, since lines are very long.

### 2. Locate the existing session structure

Check both files to learn the format you must match:

- `.local/session-transcripts/<month>-2026/` - look at the most recent `session-N-<topic>-summary.md` to mirror structure exactly. As of the June 2026 cohort, the established section order is: title, metadata (date, cohort, Granola link), **Topics Covered**, **Audience Profile**, **Questions Asked (Key Themes)**, **What Went Well**, **What Didn't Work**, **Key Quotes**, **Action Items Generated**, an optional session-specific section if the call warrants one (e.g. a coverage/status recap), then **Session Rating: X / 10** with a **Why this rating - logical reasons** breakdown. Always check the single most recent file in the most recent month folder - older files (pre-June 2026) used a leaner Demos Run Live / Open Items / Followups pattern that has since been superseded; don't mirror that older pattern.
- `02-presentation/q&a.md` - read the date-context header block at the top to learn the current "Last full refresh" / "Additions" log, and skim the last "Session N Additions" block to learn:
  - The last Q number used (so the new questions continue numbering).
  - The exact heading format (e.g. `# May 2026 - Session N Additions`).
  - The per-question format - short answer, body, **Sources:** block with verified URLs.

### 3. Decide session number and topic

- Session number = last session number + 1.
- Topic = the main subject of the call (e.g. "multi-agents", "prototypes", "skills"). Derive from the first 5-10k chars of the transcript.

### 4. Write the session summary

File path: `.local/session-transcripts/<current-month>-2026/session-<N>-<topic>-summary.md`

Mirror the previous session's structure. Each section's quality bar:

- **Topics Covered** - 15-25 numbered items, each one a *specific* moment from the call, not a generic bullet. Use the host's actual phrasing where memorable. Fold live demos into the relevant numbered item (bold the demo name) rather than a separate "Demos Run Live" section - that matches current practice.
- **Audience Profile** - participant count, names if mentioned, behavioral observations (engagement, languages, who asked what kind of question), recurring themes.
- **Questions Asked (Key Themes)** - cluster by theme, quote questions verbatim where possible. This is the source of truth for the Q&A update below.
- **What Went Well** - 4-6 bullets on demos/moments that landed, concrete and specific (name the artifact or exchange, not just "good engagement").
- **What Didn't Work** - 3-6 bullets on friction, unresolved bugs, unclear outcomes, or content that didn't get covered. Bold the headline of each bullet.
- **Key Quotes** - split into **Aman:** and **Participants:** subsections, verbatim quotes pulled from the transcript (attribute participants by name where known, else "a participant").
- **Action Items Generated** - bullet list, prefixed by owner where known (e.g. "Kapil: ...", "All participants: ...", "Aman: ...").
- **Session Rating: X / 10** - one paragraph justifying the score, then a `### Why this rating - logical reasons` subsection with three bolded groups: **What pulled the score up (+)**, **What kept it from a 9 or 10 (-)**, and **What would push this to a 9+ next time**, each 3-5 bullets.
- Add a session-specific section between Action Items and Session Rating only if the call warrants it (e.g. a "what got built vs. still pending" recap for a multi-part build session) - skip it otherwise.

Length target: 110-190 lines (matches the last 10+ sessions in practice).

### 5. Append to q&a.md

Update the date-context header at the top:

```
- **May 2026 Session N additions:** DD-MM-YYYY (Q<start>-Q<end> - see "May 2026 - Session N Additions" section)
```

Then append a new section at the bottom of the file:

```markdown
---

# May 2026 - Session N Additions

New questions raised by the NextLeap Applied Generative AI Bootcamp cohort on DD-MM-YYYY during Session N (<topic>). All URLs verified DD-MM-YYYY.

---

## Q<n>: <question verbatim or tightly paraphrased>

**Short answer:** <one-or-two-sentence direct answer>

<body - tables, lists, code blocks as needed. Cite specific docs, commands, and limits>

**Sources:**
- <url> (verified DD-MM-YYYY)
APPEND_GUARD
```

Convert every "Question Asked" cluster from the session summary into a numbered Q. Aim for 10-15 Qs per session (consolidate near-duplicates).

### 6. Quality checks before returning

- [ ] Session number continues from prior session (no gap, no overlap)
- [ ] Q numbering continues from the last Q in q&a.md (no gap)
- [ ] Every URL is validated via `curl -s -o /dev/null -w "%{http_code}" -L --max-time 10 -A "Mozilla/5.0" <url>` (per global CLAUDE.md rule). Replace any 404s before saving
- [ ] All dates are **DD-MM-YYYY**. No ISO, no US format
- [ ] No em dashes (per global writing rules)
- [ ] No emojis unless the user asked
- [ ] Date in q&a.md header block updated with the new session row
- [ ] File written under `.local/session-transcripts/<month>-2026/`, not `outputs/` or elsewhere
- [ ] Granola link copied into the summary's metadata block
- [ ] Sources are from `code.claude.com`, `docs.anthropic.com`, or `anthropic.com/engineering` only - no third-party blogs unless the user explicitly asked

### 7. URL hygiene (non-negotiable)

This skill writes a lot of citation URLs. Per global rules:

- HEAD/GET-check every URL before writing it. Accept 2xx; LinkedIn/anti-bot 999 is OK.
- Beware **soft-404s** on docs.anthropic.com and code.claude.com - fetch body, grep for "404" / "Page not found".
- Use **official sources only**. If no first-party page exists for a topic, omit the citation rather than substitute a blog.

## Output

End with a one-line summary like:

> Wrote `session-<N>-<topic>-summary.md` and appended Q<start>-Q<end> to `q&a.md`. <N> URLs verified.

Nothing else. The user is busy and just wants confirmation the artifacts are in place.

## Common pitfalls

- **Reading the Granola transcript with the Read tool.** The lines are too long. Use Python char-range slicing instead.
- **Inventing questions that weren't asked.** Stay grounded in the transcript. If a Q is implied but not asked verbatim, mark it as a paraphrase in the heading.
- **Drifting from the established structure.** The host's q&a.md has a strict format developed over 5 sessions. Mirror it exactly - don't introduce new section names or reorder.
- **Mirroring a stale session-summary template.** The session-summary section list evolved (see step 2/4) - always check the single most recent file in the most recent month folder, not an older one, and don't skip What Went Well / What Didn't Work / Key Quotes / Action Items Generated / Session Rating just because an older file in a different month omitted them.
- **Wrong month folder.** Check the existing `.local/session-transcripts/` folder names; don't create a new month folder unless the previous session's month no longer applies.
- **Citing third-party content.** Stick to official Anthropic / Claude docs unless the user explicitly asked otherwise.
