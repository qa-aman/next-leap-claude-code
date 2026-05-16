---
name: ppt-builder
description: Generate dark-themed, professional PowerPoint (.pptx) files using python-pptx. Invoke this skill whenever the user says "create a PPT", "build slides", "make a presentation", "generate a deck", or wants to turn a session plan, outline, content doc, or conversation into a slide deck. Also trigger when the user says things like "turn this into slides", "I need slides for this", or "make a deck for this session". The output is always a .pptx file using the design system defined in this skill. Do not write ad-hoc python-pptx code — always use this skill and the bundled script as the foundation.
---

# PPT Builder

Generates dark-themed `.pptx` files using python-pptx. The design system is fixed: near-black background, Claude orange accents, white/grey text hierarchy. Every presentation uses this system — do not deviate.

`scripts/build_ppt.py` is the canonical reference deck containing the full design system, all helpers, and a working example of every layout pattern. Always read it before generating slides. Never rewrite helpers from scratch.

## Workflow

### 1. Read the reference script
Read `scripts/build_ppt.py` for color constants (`BG_DARK`, `ACCENT`, `WHITE`, `LIGHT_GREY`, `MID_GREY`, `TAG_BG`), slide dimensions (`SLIDE_W`, `SLIDE_H`), and helpers (`bg`, `txbox`, `accent_bar`, `tag`, `bullets`, `divider`). Use them directly.

### 2. Understand the content
Identify:
- **What is being presented** — session, talk, workshop, pitch, review
- **How many slides** — rough guide: duration in minutes / 2
- **What sections exist** — extract from the user's doc, outline, or conversation
- **Output path** — ask if not specified; default to same folder as the source doc

### 3. Pick slide patterns
Map each slide's content to one of the patterns documented in `references/slide-patterns.md`: title, agenda/table, concept (bullets + panel), card grid, comparison (avoid/instead), numbered row list, demo walkthrough, closing/teaser. Read that file before writing slide code.

### 4. Write the build script
Create `build_<topic>.py`. Copy the helper block verbatim from `scripts/build_ppt.py` (or import if same directory). Add slides one by one. Save and print path + slide count.

```python
# [helpers block from scripts/build_ppt.py — colors, dimensions, BLANK, all functions]

prs = Presentation()
prs.slide_width  = SLIDE_W
prs.slide_height = SLIDE_H
BLANK = prs.slide_layouts[6]

# --- SLIDE 1: Title ---
s = prs.slides.add_slide(BLANK)
bg(s); accent_bar(s)
# ... slide content ...

out = "/path/to/output.pptx"
prs.save(out)
print(f"Saved: {out}")
print(f"Slides: {len(prs.slides)}")
```

### 5. Run the build
```bash
python3 build_<topic>.py
```
If `python-pptx` is missing: `pip3 install python-pptx`.

### 6. Run the layout checker (mandatory)
```bash
python3 scripts/check_layout.py <path-to-pptx>
```
Exit code `0` = ship. Exit code `1` = fix and re-run. **Do not hand the deck to the user until the check passes.** See `references/layout-checker.md` for what it catches, what's excluded, and common collision fixes.

## Design rules (non-negotiable)

- **Background**: always `BG_DARK` (`#0D0D0D`)
- **Accent**: always `ACCENT` (`#D47A21` — Claude orange)
- **Text hierarchy**: titles in `WHITE`, body in `LIGHT_GREY`, metadata in `MID_GREY`
- **Cards and panels**: `TAG_BG` fill (`#1E1E1E`) with `ACCENT` border
- **Accent bar**: always present at top of every slide (`accent_bar(s)`)
- **No speaker-direction labels**: tags like "SCREENSHARE" or "SLIDES" are internal — do not include on audience-facing decks
- **No emojis** in slide content unless explicitly requested
- **Bullet spacing**: `spacing_after=Pt(10)` default, increase to `Pt(14)` for fewer items
- **Max bullets per slide**: 5. More than 5 = split into two slides
- **Slide titles**: state the takeaway, not the topic. "CLAUDE.md Is the Context File Claude Reads First" not "CLAUDE.md Overview"

## Output conventions

- Save the `.pptx` to the same folder as the source document unless the user specifies otherwise
- Filename: `<Topic>-<Context>.pptx` (e.g., `Session-1-Claude-Code-NextLeap.pptx`)
- Print save path and slide count after saving
- Keep the generation script in the same folder as the output for future edits

## Bundled resources

- `scripts/build_ppt.py` — canonical reference deck with every pattern
- `scripts/check_layout.py` — layout validator (run before delivery)
- `references/slide-patterns.md` — code snippet for each slide pattern
- `references/layout-checker.md` — checker details, exclusions, common collision fixes
