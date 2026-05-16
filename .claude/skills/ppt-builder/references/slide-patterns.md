# Slide Patterns

Every slide uses one of these patterns. Pick the right one for each slide's content. See `scripts/build_ppt.py` for working examples of all of them.

## Title slide
```python
# Orange bar + event label (small, grey) + big title (bold, white) + divider + subtitle line
accent_bar(s)
txbox(s, "EVENT NAME", ..., size=13, color=MID_GREY)
txbox(s, "Main Title", ..., size=52, bold=True, color=WHITE)
divider(s, ...)
txbox(s, "Supporting line", ..., size=19, color=LIGHT_GREY)
```

## Agenda / table slide
```python
# Title + alternating shaded rows (TAG_BG on even rows) + two columns: time (ACCENT) + topic (WHITE)
# Do NOT add a mode/type column — this is audience-facing
```

## Concept slide (bullets left, visual panel right)
```python
# Title + divider + bullets on left (Inches 0.6 to 7.5) + dark panel on right (Inches 8.5+)
# Panel contains code snippet or comparison in ACCENT / LIGHT_GREY
# Keep panel height <= 4.4in if you also include a bottom callout line at top=6.5in
```

## Card grid (2, 3, or 4 cards)
```python
# Title + divider + evenly spaced TAG_BG cards with ACCENT border
# Each card: small ACCENT label on top, WHITE bold title, LIGHT_GREY description
```

## Comparison slide (avoid / instead)
```python
# Two columns: red-tinted boxes on left (AVOID), green-tinted boxes on right (INSTEAD)
# Use RGBColor(0x2A, 0x10, 0x10) + RGBColor(0xFF,0x55,0x55) border for avoid
# Use RGBColor(0x0D, 0x2A, 0x10) + RGBColor(0x44,0xBB,0x44) border for instead
```

## Numbered row list
```python
# Title + divider + each item = ACCENT filled square number + bold WHITE title + LIGHT_GREY description on same row
# Divider (dark grey) between rows: RGBColor(0x33, 0x33, 0x33)
```

## Demo / walkthrough slide
```python
# Title + divider + numbered steps as bullet list
# Accent callout line at bottom (ACCENT, bold, size 17)
# No mode tags (SCREENSHARE etc.) — slides are audience-facing
```

## Closing / teaser slide
```python
# Large bold statement (2 lines, size 38) + divider + section heading in ACCENT + bullet list
```
