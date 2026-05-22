# UX-ZONE.md, the manifest

Single-file contract for the Zomato Sushi UX Zone at `/Users/amanparmar/Documents/AI-PM/Projects/next-leap-claude-code/16-zomato/ux-zone/`. Read this first. Everything you need to use the kit is here. Detail lives in per-component READMEs.

Last regenerated: 17-05-2026.

---

## 1. What this kit is

A locked-down set of design tokens, components, page templates, and framework adapters extracted from real Zomato pages. Use it so every prototype built against this kit looks visually and behaviourally identical, no matter who built it.

It is plain HTML + CSS + JSON at its core, with optional React (plain CSS or Tailwind) variants and a Figma library spec.

---

## 2. Hard rules

These are not preferences. Breaking any of them will cause prototypes to drift.

1. Always link `tokens.css` before any component CSS. It defines the variables every component reads.
2. Never edit `tokens.css` per prototype. Edit `tokens.json`, then run `node adapters/build-tailwind.mjs` to regenerate.
3. Never invent new components. If a needed pattern is absent, add it to this kit first with the same folder shape, then use it.
4. Never hotlink images, fonts, or icons from external CDNs. All assets are self-hosted under `assets/`.
5. Use `uxz-` prefixed class names exactly as defined. Do not duplicate styles inline or in a separate stylesheet.
6. Dates everywhere are DD-MM-YYYY. Never YYYY-MM-DD or US format.
7. No emojis or em dashes in component output unless they appear in the source.
8. When two components are placed on the same page, both must come from this kit. Do not mix in another design system on the same page.

---

## 3. Token cheatsheet (12 most-used)

Full list in `tokens.json`. CSS variables in `tokens.css`.

| Variable | Value | When to use |
|---|---|---|
| `--uxz-color-text-default` | #020817 | Default page text (anywhere outside article prose) |
| `--uxz-color-text-body` | #293142 | Body paragraphs inside `.uxz-prose` |
| `--uxz-color-text-muted` | #696969 | Footer links, card meta lines |
| `--uxz-color-text-card-title` | #1C1C1C | Restaurant card name, listing page title |
| `--uxz-color-brand-red` | #CB202D | Tabs underline, pull-quote border, brand accents |
| `--uxz-color-link` | #7293F3 | Inline article links |
| `--uxz-color-bg-page` | #FFFFFF | Page background |
| `--uxz-color-bg-footer` | #F8F8F8 | Footer background |
| `--uxz-font-article` | "Be Vietnam Pro", sans-serif | Article body and headings |
| `--uxz-font-footer` | Okra, sans-serif | Product UI (header, cards, footer) |
| `--uxz-space-6` | 32px | Default section padding |
| `--uxz-radius-md` | 8px | Card image, search bar |

---

## 4. Component catalog

Every row maps to a folder under `components/<name>/`. Read that folder's `README.md` for variants and props.

| Name | Use it for | Required props (JSX) | CSS file | Source URL |
|---|---|---|---|---|
| `tag-chip` | Category label above article title | `label` | `components/tag-chip/style.css` | /blog/sushi/ |
| `header-nav` | Logo-only blog header | `logoSrc` | `components/header-nav/style.css` | /blog/sushi/ |
| `header-nav-rich` | Product header (logo + location + search + auth) | `logoSrc` | `components/header-nav-rich/style.css` | /ncr/restaurants |
| `hero-article` | Top of an article (tag + h1 + byline + hero image) | `tag, title, author, date, readTime, heroSrc` | `components/hero-article/style.css` | /blog/sushi/ |
| `body-paragraph` | Article prose wrapper (`.uxz-prose`) | - (wraps children) | `components/body-paragraph/style.css` | /blog/sushi/ |
| `body-heading` | h2, h3, h4 inside an article | `level, children` | `components/body-heading/style.css` | /blog/sushi/ |
| `inline-image` | Figure + italic caption | `src` | `components/inline-image/style.css` | /blog/sushi/ |
| `pull-quote` | Blockquote with brand-red left border | `children` | `components/pull-quote/style.css` | /blog/sushi/ |
| `footer` | 5-column site footer | `columns` | `components/footer/style.css` | /blog/sushi/ |
| `breadcrumb` | Home / Section / Current navigation | `items` | `components/breadcrumb/style.css` | /ncr/restaurants |
| `tab-bar` | Top-level mode switch (Dining/Delivery/Nightlife) | `tabs, selectedId` | `components/tab-bar/style.css` | /ncr/restaurants |
| `filter-pill` | Rounded filter pill in a row | `label` | `components/filter-pill/style.css` | /ncr/restaurants |
| `rating-chip` | Colored rating pill with star | `value` | `components/rating-chip/style.css` | /ncr/restaurants |
| `price-tag` | "₹X for two" inline meta | `amount` | `components/price-tag/style.css` | /ncr/restaurants |
| `restaurant-card` | Image + name + rating + cuisines + price + locality | `imageSrc, name, rating, cuisines, costForTwo, locality, distance` | `components/restaurant-card/style.css` | /ncr/restaurants |
| `collection-card` | Image card with gradient overlay | `imgSrc, title, placesLabel, href` | `components/collection-card/style.css` | /ncr/restaurants |

Components NOT YET in the kit (do not invent these): `cta-button`, `image-carousel`, `modal-dialog`, `author-bio`, `social-share-bar`, `comments-block`. If you need one, propose it in a new component folder with the same shape.

---

## 5. Composition rules

How components nest. Violating these breaks layout.

- `tag-chip` lives inside `hero-article` or freestanding above any heading. Never inside body prose.
- `body-heading` (h2/h3/h4) and `inline-image` and `pull-quote` must live inside a `<article class="uxz-prose">` wrapper. Otherwise prose styles do not apply.
- `rating-chip` and `price-tag` live inside `restaurant-card`. They can stand alone but render best inside the card.
- `header-nav` (logo-only) and `header-nav-rich` (product header) are mutually exclusive. Use one per page, never both.
- `footer` is always the last child of `<body>`.
- `filter-pill` instances live inside a `.uxz-filter-row` container, never bare.
- `breadcrumb` sits between header and main content. Never inside the article body.

---

## 6. Templates

Four templates exist (only three buildable in current kit).

| Template | When to use | Components composed | Path |
|---|---|---|---|
| `article` | Long-form article / blog post | header-nav, hero-article, prose, body-heading, inline-image, pull-quote, footer | `templates/article/index.html` |
| `listing` | Search-results / category listing | header-nav-rich, breadcrumb, tab-bar, filter-pill, restaurant-card grid, footer | `templates/listing/index.html` |
| `landing` | Discovery / home / category landing | header-nav-rich, tab-bar, collection-card scroller, restaurant-card grid, footer | `templates/landing/index.html` |
| `restaurant-detail` | (planned) Restaurant detail page | requires image-carousel and modal-dialog (not yet built) | not built |

Each template has its own README with content-swap instructions.

---

## 7. For a fresh Claude session

Paste the block below into a fresh conversation. Replace `<task>` with what you want built. The prompt is self-contained and does not rely on any previous conversation.

```
You are building a prototype. Use the UX Zone at:
/Users/amanparmar/Documents/AI-PM/Projects/next-leap-claude-code/16-zomato/ux-zone/

Before doing anything else:
1. Read UX-ZONE.md in that folder end to end.
2. Read the README.md of every component you plan to use.

Hard rules (from UX-ZONE.md, restated):
- Link tokens.css first. Then component CSS files in order of use.
- Use only uxz-prefixed class names. Do not invent classes or styles.
- Do not hotlink images, fonts, or icons. Reference assets/ via relative path.
- Do not edit tokens.css per prototype.
- Use DD-MM-YYYY for any date.
- If a needed pattern is absent from the catalog, stop and tell me. Do not invent components.

Task: <task>

When you finish, list the component CSS files you linked and the components you instantiated. Run the prototype HTML through a local server and confirm zero console errors.
```

---

## 8. Forbidden

- Hotlinking assets from `zmtcdn.com` or any external CDN.
- Editing `tokens.css`, `tokens.json`, or any component `style.css` to fit a single prototype.
- Adding a new class that is not prefixed with `uxz-`.
- Mixing this kit with Material UI, Chakra, Bootstrap, or another design system on the same page.
- Using `em` dashes, `en` dashes that look like em dashes, or emojis unless they appear in the source page.
- Using YYYY-MM-DD or MM/DD/YYYY anywhere in component output or filenames.
- Inventing a component that is not in the catalog above.

---

## 9. How to add a new component

1. Create `components/<name>/` with `index.html`, `style.css`, `README.md`, `reference.png`, `Component.jsx`, `Component.tailwind.jsx`, `figma.md`.
2. Use only existing tokens. If a token is missing, add it to `tokens.json` with a `source:` field explaining why no existing token fit, then regen Tailwind config.
3. Prefix every class with `uxz-<component-name>__element` (BEM-style).
4. Add a row to this manifest's component catalog.
5. Append a Phase block to `VERIFICATION.md` with constraint checks.

---

## 10. File map (top level)

```
ux-zone/
  UX-ZONE.md               <- you are here
  README.md                <- usage walkthrough
  VERIFICATION.md          <- audit log per phase
  tokens.json              <- source of truth for all values
  tokens.css               <- CSS variable mirror
  index.html               <- component gallery
  assets/                  <- self-hosted images, fonts, icons, reference screenshots
  components/              <- 16 component folders
  templates/               <- 3 page templates (landing, listing, article)
  adapters/                <- Tailwind config, Figma library, build/check scripts
```
