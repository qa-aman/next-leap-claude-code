---
name: pptx-editor
description: Edit, update, and add slides to PowerPoint (.pptx) files using python-pptx. Use this skill whenever the user wants to modify a presentation - adding slides, editing text, changing styling, reordering slides, inserting links, or fixing design consistency. Trigger on any mention of "slide", "presentation", "PowerPoint", "pptx", "deck", "add a slide", "update the slide", "fix the slides", "last slide", "thank you slide", or any request involving .pptx files - even if the user just references a .pptx path without explicitly saying "edit".
---

# PPTX Editor

Edit PowerPoint files programmatically using python-pptx while preserving visual consistency with the existing deck.

## Why this skill exists

PowerPoint editing through code is error-prone because small mismatches in background color, font inheritance, shape positioning, or line styling make new slides look obviously wrong next to existing ones. This skill enforces a "inspect first, match exactly" workflow that prevents those mismatches.

## Core workflow

Every PPTX edit follows three phases: **Inspect, Edit, Verify**. Never skip the inspect phase - it is what prevents visual mismatches.

### Phase 1: Inspect the existing deck

Before making any changes, run the inspect script to extract the deck's design system. This is non-negotiable because presentations vary wildly in how they're built - some use layouts, some use manual shapes, some mix both.

```bash
python3 .claude/skills/pptx-editor/scripts/inspect-deck.py <path-to-pptx>
```

The script extracts every shape, text style, color, position, and font across all slides, then prints a design token summary at the end.

From this output, build a mental model of the deck's design tokens:

| Token | What to capture | Why it matters |
|-------|----------------|----------------|
| Background | Solid color RGB or theme reference | New slides without this look white against dark decks |
| Accent color | The color used for bars, separators, labels | Usually one dominant accent throughout |
| Heading style | Font size, bold, color, position | Titles must match exactly |
| Body style | Font size, bold/None, color | Subtle: bold=None is different from bold=False |
| Font typeface | Explicit name or THEME inheritance | If existing slides use THEME, new slides must NOT set font.name |
| Decorative shapes | Top bars, separators - exact position, size, fill, line style | These define the visual rhythm of the deck |
| Text positions | Left margin, top positions for titles, bodies, footers | Consistent alignment across slides |

### Phase 2: Edit the deck

Build new or modified slides using the exact values from Phase 1.

**Critical rules:**

1. **Set the slide background explicitly.** The Blank layout does not inherit the master slide background in python-pptx. Always set it:
   ```python
   slide.background.fill.solid()
   slide.background.fill.fore_color.rgb = RGBColor(0x0D, 0x0D, 0x0D)
   ```

2. **Match font inheritance.** If existing slides use theme fonts (no explicit typeface), do NOT set `font.name` on new text. Setting it forces an explicit typeface that may render differently:
   ```python
   # CORRECT - inherits theme font
   run = p.add_run()
   run.text = "Hello"
   run.font.size = Emu(457200)
   run.font.bold = True
   run.font.color.rgb = RGBColor(0xFF, 0xFF, 0xFF)
   # Do NOT set run.font.name

   # WRONG - overrides theme font
   run.font.name = "Calibri"  # Don't do this if originals use theme
   ```

3. **Reproduce decorative shapes exactly.** Copy the position, size, fill color, and line style from the inspection. Pay special attention to:
   ```python
   # Line style must match - most decks use background (invisible) lines
   shape.line.fill.background()
   shape.line.width = 0
   ```

4. **Use Emu units consistently.** The inspection gives values in EMUs. Use them directly - do not convert to Inches or Pt and back, because rounding errors accumulate.

5. **Preserve bold=None vs bold=True vs bold=False.** In python-pptx, `None` means "inherit from style", `False` means "explicitly not bold", and `True` means "explicitly bold". Match what existing slides use.

6. **Add hyperlinks correctly.** Use `run.hyperlink.address`, not shape-level links:
   ```python
   run = p.add_run()
   run.text = "linkedin.com/in/someone"
   run.font.size = Emu(228600)
   run.font.color.rgb = WHITE
   run.hyperlink.address = "https://www.linkedin.com/in/someone"
   ```

7. **Delete slides properly** when replacing them:
   ```python
   from pptx.oxml.ns import qn
   rId = prs.slides._sldIdLst[index].get(qn('r:id'))
   prs.part.drop_rel(rId)
   del prs.slides._sldIdLst[index]
   ```
   Delete from highest index first when removing multiple slides.

### Phase 3: Verify

After saving, run a verification script that compares the new slides against existing ones:

```python
# Check that new slides match the design system
for idx in [<new_slide_indices>]:
    slide = prs.slides[idx]
    bg_color = slide.background.fill.fore_color.rgb if slide.background.fill.type else "MISSING"
    print(f"Slide {idx+1}: background={bg_color}")
```

Confirm:
- Background color matches existing slides
- Top decorative shapes are present with correct position/size/color
- Text colors and sizes match equivalent elements on other slides
- No explicit font names set when originals use theme fonts

## Common operations

### Adding slides to the end
Use `prs.slides.add_slide(layout)`. Always use the same layout as existing slides (inspect first to find which one).

### Editing text on existing slides
Find the shape by name or by iterating, then modify `shape.text_frame.paragraphs[n].runs[m]`.

### Reordering slides
python-pptx does not have a native reorder API. To move a slide, you need to manipulate the XML directly by reordering elements in `prs.slides._sldIdLst`.

### Changing styling across all slides
Use `replace_all`-style loops. Extract the current value first to avoid changing things that shouldn't change.

## Dependencies

Requires `python-pptx`. Install with:
```bash
pip3 install python-pptx
```

## Reference

- `scripts/inspect-deck.py` - Run this in Phase 1 to extract design tokens from any PPTX file.
- `references/design-tokens-checklist.md` - Copy-paste checklist to fill in during the inspect phase.
