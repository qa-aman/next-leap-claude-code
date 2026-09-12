# Visual System - the craft layer, as numbers

This is Layer 4. Its job is to convert taste into values you can pick from, because a model choosing spacing by feel produces the flat grey admin panel that everyone recognises as machine-made.

The rules here come from [Refactoring UI](https://www.refactoringui.com/) (Adam Wathan and Steve Schoger), [Laws of UX](https://lawsofux.com/) (Jon Yablonski), [Material Design 3](https://m3.material.io/), and the [Apple Human Interface Guidelines](https://developer.apple.com/design/human-interface-guidelines/). Accessibility numbers come from [WCAG 2.2](https://www.w3.org/WAI/WCAG22/quickref/) and are hard limits, not preferences.

**If the target is `15-prototype/`, ignore the token values below and use `15-prototype/tailwind.config.ts`.** That file is the source of truth for that app. This file is the default for a standalone mockup.

---

## 1. Hierarchy - the thing that separates good from generic

Most weak UI has every element shouting at the same volume. Hierarchy is deciding what the user sees first, second, and last, and then making the design say that.

**Rank before you style.** Write the order out: primary, secondary, tertiary. Then apply emphasis with these levers, in this order of preference:

1. **Colour and contrast.** Dark text for primary, mid-grey for secondary, light grey for tertiary. This is cheaper and more effective than size.
2. **Weight.** 600 or 700 for primary, 400 or 500 for the rest. Avoid weights under 400 for small text, they turn to mush.
3. **Size.** The blunt instrument. Reach for it after colour and weight, not before.
4. **Position and space.** Whitespace around an element is emphasis. Crowding is de-emphasis.

**Specific moves that reliably help:**

1. **De-emphasise instead of emphasising.** If the primary is not standing out, try making everything else quieter before making it louder.
2. **Do not use grey text on a coloured background.** Reduce the opacity of white, or pick a lighter tint of the background hue. Grey on colour looks muddy every time.
3. **Labels are usually not important.** "Email: aman@x.com" wants the value emphasised and the label shrunk, or the label deleted entirely when the value is self-evident.
4. **Semantics are not hierarchy.** An `<h2>` does not have to look big. Style by importance, mark up by meaning.
5. **Balance weight against size.** When you make text bigger, you can often make it lighter. When you make it smaller, make it heavier so it does not disappear.

---

## 2. Spacing - one 4px scale, no exceptions

Use this scale. Nothing between the steps.

```
2, 4, 8, 12, 16, 20, 24, 32, 40, 48, 64, 80, 96, 128
```

**Start with too much space and remove it.** Designs are far more often too tight than too loose, and it is much easier to see what to remove than what to add.

**Gaps must be unambiguous.** If the gap between two groups is 16px and the gap inside a group is 12px, the eye cannot tell them apart, and the Law of Proximity groups the wrong things. Make the between-group gap at least 1.5x, ideally 2x, the within-group gap.

**Defaults that work:**

| Context | Value |
|---|---|
| Inside a chip or pill | 8px horizontal, 2 to 4px vertical |
| Button padding | 12 to 16px horizontal, 8 to 12px vertical |
| Card body padding | 16px minimum, 24px for hero cards |
| Gap between cards in a grid | 16 or 24px |
| Between major page sections | 32 to 48px |
| Page gutter, desktop | 24 to 32px |
| Page gutter, mobile | 16px |

Off-grid values such as `padding: 13px` mean the scale was abandoned. If a value genuinely must be off-grid, for example matching a fixed asset, leave a one-line comment saying why.

---

## 3. Type

**Pick a scale, do not use a ratio.** Hand-picked values beat a modular ratio because they land on whole pixels and avoid near-identical steps.

```
12, 14, 16, 18, 20, 24, 30, 36, 48, 60, 72
```

**Rules:**

1. **Body text 16px.** 14px is acceptable for dense sovereign UI, but never for long reading.
2. **Line height scales inversely with size.** Body at 1.5 to 1.6. Headings at 1.1 to 1.25. Large display type can go tighter still.
3. **Line length 45 to 75 characters** for anything read in sentences. Use `max-width: 65ch`.
4. **Letter spacing.** Tighten large headings slightly (-0.01em to -0.02em). Loosen small uppercase labels (+0.04em to +0.08em), because uppercase at 10 to 12px is unreadable without it.
5. **Two weights are usually enough.** 400 and 600. A third only if it earns its place.
6. **Align numbers in tables to the right** and use tabular figures (`font-variant-numeric: tabular-nums`), so digits line up and scan.
7. **Never centre more than about three lines** of text. Centred paragraphs are hard to read because the eye loses the left edge.

Default stack, no network fetch required, so the mockup stays self-contained:

```css
font-family: ui-sans-serif, system-ui, -apple-system, "Segoe UI", Roboto, "Helvetica Neue", Arial, sans-serif;
```

---

## 4. Colour

**Every semantic colour needs a ramp, not a value.** One "danger red" cannot serve as text, border, fill, and tinted background at once. Define roughly nine steps per colour, from a near-white tint to a near-black shade.

**What you actually need:**

1. **One neutral ramp**, 9 to 10 steps. This does the vast majority of the work.
2. **One primary/brand ramp**, 9 steps.
3. **Three semantic ramps**: success, warning, danger. 3 to 5 steps each is enough (tinted background, border, text).
4. **Optionally one accent** for charts or highlights.

**Rules:**

1. **Avoid pure black and pure white.** Pure black backgrounds look unnatural and pure white text on a tint glares. Start from a very dark grey with a slight hue, for example `#0b0b0f`, and an off-white, for example `#f5f5f7`.
2. **Do not lighten and darken with grey.** Adjust saturation and hue. Lighter shades want higher saturation and a shift toward warmer hues, darker shades want a shift toward cooler.
3. **Role to shade convention:** text on a tinted background uses the darkest step, borders use a mid step at 30 to 40% alpha, tinted backgrounds use the lightest step or the base at 8 to 12% alpha, solid fills use the base, hover shifts exactly one step.
4. **Never carry meaning in colour alone.** WCAG 2.2 SC 1.4.1. Status is always icon plus label plus colour. A red dot alone is invisible to a large number of users and to anyone glancing.
5. **Contrast is a hard floor.** 4.5:1 for body text, 3:1 for large text (18pt regular or 14pt bold and above), 3:1 for the boundary of any interactive element against its surface. These are checked by the gate, so failing them is not a style disagreement, it is a failing build.

---

## 5. Depth and elevation

Depth communicates layering, and it is where machine-made UI most often looks flat and dated.

1. **Shadows are a scale too**, matched to how far off the page something sits. Five steps is plenty: subtle, small, medium, large, and modal.
2. **Two-part shadows read as real.** A tight, darker shadow for the contact edge plus a wide, softer one for the ambient cast.
3. **Shadows are vertical.** Light comes from above, so offset down on the Y axis with no X offset.
4. **A top inset highlight** (`inset 0 1px 0 rgba(255,255,255,0.06)`) makes a raised element look genuinely raised. This one line does more than an extra shadow layer.
5. **Elevation can also be flat.** A subtle background shift plus a 1px border often reads better than a shadow, especially in dark UI where shadows are nearly invisible. In dark themes, elevate with *lighter surfaces*, not heavier shadows.
6. **Overlapping elements create depth cheaply.** A card that crosses a section boundary, an avatar overlapping an image edge.

Reference set:

```css
--shadow-sm:  0 1px 2px rgba(0,0,0,.06);
--shadow-md:  0 1px 2px rgba(0,0,0,.06), 0 4px 8px -2px rgba(0,0,0,.08);
--shadow-lg:  0 2px 4px rgba(0,0,0,.06), 0 12px 24px -6px rgba(0,0,0,.12);
--shadow-xl:  0 4px 8px rgba(0,0,0,.08), 0 24px 48px -12px rgba(0,0,0,.18);
```

---

## 6. Radius, borders, and edges

1. **Pick two radii and stick to them.** One for small elements (buttons, inputs, chips), one for containers (cards, modals). A third for pills (`9999px`).
2. **Nested radii must be concentric.** Inner radius = outer radius minus the padding between them. Otherwise the corners look wrong and nobody can say why.
3. **Borders should be low contrast.** A border's job is to separate, not to draw attention. Use a neutral step close to the surface it sits on, except where WCAG requires 3:1 for an interactive boundary.
4. **Prefer a background shift over a border** when separating sections. Fewer lines, cleaner result.

---

## 7. Interaction states - all six, every time

An element is not done until all of these exist. Missing states are the most common gap in generated UI.

| State | Requirement |
|---|---|
| **Rest** | Perceivable as interactive without hovering. 3:1 boundary contrast. |
| **Hover** | A real change: background shift, border shift, or elevation. Opacity alone reads as disabled and is easy to miss. |
| **Focus-visible** | A visible ring at 3:1 contrast. Use `:focus-visible`, not `:focus`, so it appears on keyboard navigation and not on every mouse click. |
| **Active** | A pressed signal. Slight scale down or a darker fill. |
| **Disabled** | Reduced contrast plus `cursor: not-allowed`, and always a reason nearby. A disabled button with no explanation is a dead end. |
| **Loading** | For anything over 400ms (the Doherty Threshold). A skeleton beats a spinner because it also communicates the shape of what is coming. |

---

## 8. Motion

1. **Fast.** 150 to 250ms for most transitions. Above 400ms feels sluggish.
2. **Ease out for entrances** (`cubic-bezier(.2,.8,.2,1)`), ease in for exits. Linear only for continuous things like a progress bar.
3. **Animate transform and opacity.** Animating width, height, top, or left causes layout thrash and jank.
4. **Respect the user.** Wrap non-essential motion in `@media (prefers-reduced-motion: reduce)` and disable it there. This is an accessibility requirement, not a nicety.

---

## 9. Layout

1. **12-column grid** on desktop, with a max content width of 1200 to 1440px. Full-bleed content is hard to read.
2. **Breakpoints:** 640, 768, 1024, 1280, 1536.
3. **Design mobile first** in the markup, then add complexity upward. It is far easier than removing it downward.
4. **Touch targets 44x44 CSS px minimum**, everywhere, not just on mobile. If the visible control is smaller, expand the hit area with padding or a pseudo-element.
5. **8px minimum gap between adjacent interactive elements**, 12px comfortable. Below that, Fitts's Law produces mis-taps.
6. **Cap any list, menu, or option group at around seven items** per group (Miller's Law). Beyond that, chunk it or paginate it.

---

## 10. The default token block

Copy this into a standalone mockup. It is already in `assets/mockup-shell.html`, tuned so that every foreground and background pair passes its WCAG threshold in both light and dark.

```css
:root {
  color-scheme: light dark;

  --space-1:4px;  --space-2:8px;  --space-3:12px; --space-4:16px;
  --space-5:20px; --space-6:24px; --space-8:32px; --space-10:40px;
  --space-12:48px; --space-16:64px;

  --text-xs:12px; --text-sm:14px; --text-base:16px; --text-lg:18px;
  --text-xl:20px; --text-2xl:24px; --text-3xl:30px; --text-4xl:36px;

  --radius-sm:6px; --radius-md:10px; --radius-lg:16px; --radius-full:9999px;

  /* light */
  --bg:#ffffff;          --bg-subtle:#f7f7f8;   --bg-inset:#f0f0f2;
  --surface:#ffffff;     --border:#e3e3e8;      --border-strong:#c9c9d1;
  --fg:#16161a;          --fg-muted:#5c5c68;    --fg-subtle:#8a8a96;
  --primary:#4f39d9;     --primary-hover:#4130b8; --primary-fg:#ffffff;
  --primary-tint:#eeebfd;
  --success:#0f7b3f;     --success-tint:#e6f5ec;
  --warning:#8a5a00;     --warning-tint:#fdf3e0;
  --danger:#b3261e;      --danger-tint:#fdeceb;
}

@media (prefers-color-scheme: dark) {
  :root:not([data-theme="light"]) {
    --bg:#0b0b0f;        --bg-subtle:#131318;   --bg-inset:#08080b;
    --surface:#16161c;   --border:#2a2a33;      --border-strong:#3d3d4a;
    --fg:#f2f2f5;        --fg-muted:#a3a3b0;    --fg-subtle:#74748a;
    --primary:#a894ff;   --primary-hover:#bcadff; --primary-fg:#12101f;
    --primary-tint:#1e1a35;
    --success:#5fd98a;   --success-tint:#0f2a1b;
    --warning:#e8b45c;   --warning-tint:#2b2109;
    --danger:#ff8f87;    --danger-tint:#301413;
  }
}
```

Two things to notice, because they are the usual mistakes. Dark mode is not the light palette inverted: the primary gets *lighter* and its foreground gets *darker*, or the button becomes unreadable. And `--fg-subtle` is deliberately close to the 4.5:1 floor, so it is for decoration and never for anything the user must read.
