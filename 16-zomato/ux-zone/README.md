# Zomato Sushi UX Zone

A locked-down kit of components, assets, and tokens extracted from https://www.zomato.com/blog/sushi/. Use this so every prototype you and your teammates build looks the same.

Source page fetched: 17-05-2026 (DD-MM-YYYY). Method: Playwright (the source is client-rendered, WebFetch timed out on raw HTML).

## What you get

- `tokens.css` and `tokens.json`: the colors, fonts, sizes, spacing, radii, and shadows used on the page. Always include `tokens.css` first.
- `assets/`: every image, icon, and font referenced by the page, downloaded locally. No hotlinks.
- `components/`: one folder per component. Each has `index.html` (standalone preview), `style.css` (the styles you copy), and `README.md` (what it is, where it came from).
- `index.html`: a single-page gallery showing every component. Open this to see the kit in one place.

## Use it in 5 minutes

Step 1: copy the `ux-zone/` folder into your prototype directory, or link to it with a relative path.

Step 2: paste this into your new HTML file. It already renders a styled hero and footer using the kit.

```html
<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>My prototype</title>
  <link rel="stylesheet" href="ux-zone/tokens.css">
  <link rel="stylesheet" href="ux-zone/components/header-nav/style.css">
  <link rel="stylesheet" href="ux-zone/components/hero-article/style.css">
  <link rel="stylesheet" href="ux-zone/components/tag-chip/style.css">
  <link rel="stylesheet" href="ux-zone/components/body-paragraph/style.css">
  <link rel="stylesheet" href="ux-zone/components/footer/style.css">
</head>
<body>
  <header class="uxz-header-nav">
    <a class="uxz-header-nav__brand" href="/"><img src="ux-zone/assets/images/b40b97e677bc7b2ca77c58c61db266fe1603954218.png" alt="Zomato" height="26"></a>
  </header>
  <section class="uxz-hero-article">
    <span class="uxz-tag-chip">your-category</span>
    <h1 class="uxz-hero-article__title">Your prototype title goes here</h1>
    <div class="uxz-hero-article__meta">
      <span>Author Name</span><span class="uxz-hero-article__sep">|</span>
      <span>17-05-2026</span><span class="uxz-hero-article__sep">|</span>
      <span>4 mins read</span>
    </div>
  </section>
  <article class="uxz-prose">
    <p>Your first paragraph. The kit handles font, color, and spacing.</p>
  </article>
</body>
</html>
```

Step 3: add more components by linking their `style.css` and copying the HTML snippet from each component's README.

## Component list

| # | Component | What it covers |
|---|---|---|
| 1 | header-nav        | Sticky logo header |
| 2 | tag-chip          | Category label, plain or brand pill |
| 3 | hero-article      | Tag, h1, byline, hero image |
| 4 | body-paragraph    | Default prose: p, strong, em, a |
| 5 | body-heading      | h2, h3, h4 in article context |
| 6 | inline-image      | Figure with italic caption |
| 7 | pull-quote        | Blockquote with brand-red left border |
| 8 | footer            | 5-column footer with social and app stores |
| 9 | header-nav-rich   | Product header: logo + location + search + auth (Phase 02) |
| 10 | breadcrumb       | Home / India / Page, muted gray (Phase 02) |
| 11 | tab-bar          | Dining Out / Delivery / Nightlife, brand-red underline (Phase 02) |
| 12 | filter-pill      | White pill, gray border, dark pressed state (Phase 02) |
| 13 | rating-chip      | Green/yellow/red colored pill with number + star (Phase 02) |
| 14 | price-tag        | "₹3,000 for two" inline meta (Phase 02) |
| 15 | restaurant-card  | Image + name + rating + cuisines + price + locality (Phase 02) |
| 16 | collection-card  | Image card with gradient overlay (Phase 02) |

Components requested but not on the source page (so not built): cta-button, cta-banner, related-articles-card, related-articles-grid, social-share-bar, author-bio (the source has only an inline byline), comments-block. See `VERIFICATION.md`.

## How to add a new component

1. Make a folder under `components/<your-name>/` with `index.html`, `style.css`, `README.md`.
2. In `style.css`, only use tokens from `tokens.css`. No raw hex, no raw px for color and primary spacing.
3. Prefix every class with `uxz-<your-name>` to avoid collisions when two components share a page.
4. In `README.md`, name the source URL and selector if it came from a real page. If it's an extension (not in the source), say so.

## Templates and manifest (Phase 04)

- `UX-ZONE.md` is the single-file manifest. Read it first; paste its "fresh Claude session" block to bootstrap a new conversation.
- `templates/article/index.html` - blog post page
- `templates/listing/index.html` - restaurant listing
- `templates/landing/index.html` - discovery / home

## Framework adapters (Phase 03)

Every component now ships in three forms:

1. **Plain HTML + CSS** (`index.html` + `style.css`): the source of truth, drop into any HTML file.
2. **React (plain CSS)** (`Component.jsx`): imports the existing `style.css`. Drop into Next.js, Vite, CRA, Claude artifacts, v0.
3. **React (Tailwind)** (`Component.tailwind.jsx`): no CSS import. Requires `adapters/tailwind.config.js` extending your project's Tailwind theme.

Plus:

- `adapters/tailwind.config.js` - generated from `tokens.json`, regen with `node adapters/build-tailwind.mjs`.
- `adapters/equality-check.mjs` - asserts tokens.json equals the Tailwind config (regression gate).
- `adapters/tokens.tailwind.css` - imports `tokens.css` and exposes the vars in Tailwind's `@layer base`.
- `adapters/figma-library.md` - Figma library spec (pages, color/text/effect styles, component properties).
- `components/*/figma.md` - per-component Figma spec (variants, properties, auto-layout, constraints).

### Using the React variants in v0 or Claude artifacts
```jsx
import TagChip from "./ux-zone/components/tag-chip/Component.jsx";
<TagChip label="technology" variant="default" />
```

### Using the Tailwind variants in Next.js
1. Merge `ux-zone/adapters/tailwind.config.js` into your project's config (or extend from it).
2. Import the JSX directly: `import RestaurantCard from "@/ux-zone/components/restaurant-card/Component.tailwind.jsx";`

## Rules to keep things identical across prototypes

- Always include `tokens.css` before any component CSS.
- Do not edit `tokens.css` per prototype. If a token needs to change, change it here so every prototype updates.
- Use the class names exactly. Do not duplicate styles inline.
- Self-host fonts and images, do not link to `zmtcdn.com`.

## Files

```
ux-zone/
  tokens.json
  tokens.css
  index.html
  README.md
  VERIFICATION.md
  assets/
    images/   (14 PNGs)
    fonts/    (7 woff2)
    icons/    (5 SVGs)
    reference/ (full-page screenshots)
  components/
    header-nav/, hero-article/, tag-chip/, body-paragraph/,
    body-heading/, inline-image/, pull-quote/, footer/
```
