---
name: ppt-builder
description: Generate dark-themed, professional PowerPoint (.pptx) files using python-pptx. Invoke this skill whenever the user says "create a PPT", "build slides", "make a presentation", "generate a deck", or wants to turn a session plan, outline, content doc, or conversation into a slide deck. Also trigger when the user says things like "turn this into slides", "I need slides for this", or "make a deck for this session". The output is always a .pptx file using the design system defined in this skill. Do not write ad-hoc python-pptx code — always use this skill and the bundled script as the foundation.
---

# PPT Builder

Generates dark-themed `.pptx` files using python-pptx. The design system is fixed: near-black background, Claude orange accents, white/grey text hierarchy. Every presentation uses this system — do not deviate.

The bundled script `scripts/build_ppt.py` contains the full design system and all helper functions. Always use it as the foundation. Never rewrite helpers from scratch.

---

## Step 1 — Read the script

Before writing any slide code, read the full bundled script:

```
scripts/build_ppt.py
```

This file contains:
- All color constants (`BG_DARK`, `ACCENT`, `WHITE`, `LIGHT_GREY`, `MID_GREY`, `TAG_BG`)
- All slide dimensions (`SLIDE_W`, `SLIDE_H`)
- All helper functions (`bg`, `txbox`, `accent_bar`, `tag`, `bullets`, `divider`)
- A working example of every layout pattern used in the NextLeap Session 1 deck

Use these directly. Do not redefine them.

---

## Step 2 — Understand the content

Before writing slide code, identify:

1. **What is being presented** — session, talk, workshop, pitch, review
2. **How many slides** — rough guide: duration in minutes / 2
3. **What sections exist** — extract from the user's doc, outline, or conversation
4. **Output path** — ask if not specified; default to same folder as the source doc

---

## Step 3 — Map content to slide patterns

Every slide uses one of these patterns. Pick the right one for each slide's content.

### Title slide
```python
# Orange bar + event label (small, grey) + big title (bold, white) + divider + subtitle line
accent_bar(s)
txbox(s, "EVENT NAME", ..., size=13, color=MID_GREY)
txbox(s, "Main Title", ..., size=52, bold=True, color=WHITE)
divider(s, ...)
txbox(s, "Supporting line", ..., size=19, color=LIGHT_GREY)
```

### Agenda / table slide
```python
# Title + alternating shaded rows (TAG_BG on even rows) + two columns: time (ACCENT) + topic (WHITE)
# Do NOT add a mode/type column — this is audience-facing
```

### Concept slide (bullets left, visual panel right)
```python
# Title + divider + bullets on left (Inches 0.6 to 7.5) + dark panel on right (Inches 8.5+)
# Panel contains code snippet or comparison in ACCENT / LIGHT_GREY
```

### Card grid (2, 3, or 4 cards)
```python
# Title + divider + evenly spaced TAG_BG cards with ACCENT border
# Each card: small ACCENT label on top, WHITE bold title, LIGHT_GREY description
```

### Comparison slide (avoid / instead)
```python
# Two columns: red-tinted boxes on left (AVOID), green-tinted boxes on right (INSTEAD)
# Use RGBColor(0x2A, 0x10, 0x10) + RGBColor(0xFF,0x55,0x55) border for avoid
# Use RGBColor(0x0D, 0x2A, 0x10) + RGBColor(0x44,0xBB,0x44) border for instead
```

### Numbered row list
```python
# Title + divider + each item = ACCENT filled square number + bold WHITE title + LIGHT_GREY description on same row
# Divider (dark grey) between rows: RGBColor(0x33, 0x33, 0x33)
```

### Demo / walkthrough slide
```python
# Title + divider + numbered steps as bullet list
# Accent callout line at bottom (ACCENT, bold, size 17)
# No mode tags (SCREENSHARE etc.) — slides are audience-facing
```

### Closing / teaser slide
```python
# Large bold statement (2 lines, size 38) + divider + section heading in ACCENT + bullet list
```

---

## Step 4 — Write the slide generation script

Write a new Python file (e.g., `build_<topic>.py`) that:

1. Imports and reuses all helpers from the bundled script — copy the helper block verbatim, or `import` if the script is in the same directory
2. Adds slides one by one using the patterns above
3. Saves to the specified output path
4. Prints the output path and slide count on completion

### Structure template

```python
# [helpers block copied from scripts/build_ppt.py — colors, dimensions, BLANK, all functions]

prs = Presentation()
prs.slide_width  = SLIDE_W
prs.slide_height = SLIDE_H
BLANK = prs.slide_layouts[6]

# --- SLIDE 1: Title ---
s = prs.slides.add_slide(BLANK)
bg(s)
accent_bar(s)
# ... slide content ...

# --- SLIDE N: ... ---

out = "/path/to/output.pptx"
prs.save(out)
print(f"Saved: {out}")
print(f"Slides: {len(prs.slides)}")
```

---

## Step 5 — Run and verify

```bash
python3 build_<topic>.py
```

Confirm the output path printed matches the expected location. If `python-pptx` is not installed:

```bash
pip3 install python-pptx
```

---

## Step 6 — Layout eval (mandatory before delivery)

After saving, run the bundled layout checker against the generated `.pptx`:

```bash
python3 scripts/check_layout.py <path-to-pptx>
```

The checker catches two failure modes that have shipped repeatedly:

1. **Out-of-bounds shapes** — content positioned past the 13.33 x 7.5 inch canvas.
2. **Overlapping text shapes** — footers sitting on top of the last row, labels colliding with badges, two textboxes inside the same row stepping on each other.

Exit code is `0` if clean, `1` if any issue is found. **Do not hand the deck to the user until the check passes.** If it fails:

- Read the slide number and overlapping text fragments reported.
- Fix the position or size of the offending shape in the build script.
- Re-run the build script, then re-run the checker.
- Repeat until exit code `0`.

The checker excludes the orange accent bar at the top of every slide and the
full-slide background rectangle by heuristic, so it will not false-flag those.
For new decorative shapes that span the full width with negligible height
(e.g. additional dividers), the heuristic catches them automatically.

If a layout truly needs a wide section_tag plus a small chip in the same row,
use `live_badge(s)` (provided in the design system) — its dimensions are tuned
so the bundled `section_tag` width never collides with it.

---

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

---

## Output conventions

- Save the generated `.pptx` to the same folder as the source document unless the user specifies otherwise
- Filename: `<Topic>-<Context>.pptx` (e.g., `Session-1-Claude-Code-NextLeap.pptx`)
- Always print the save path and slide count after saving
- Keep the generation script in the same folder as the output for future edits

---

## Reference

The `scripts/build_ppt.py` file is the canonical example of all patterns in use together. When in doubt about positioning, sizing, or color — consult it. The NextLeap Session 1 deck covers: title, agenda table, concept slide with panel, card grid, numbered row list, comparison (avoid/instead), demo walkthrough, and closing teaser. Every common pattern is represented there.
