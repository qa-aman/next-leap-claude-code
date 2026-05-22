# Zomato Sushi UX Zone, Figma library spec

This file is the single source of truth for the Figma library that mirrors the code kit at `ux-zone/`. A designer can read this, set up the file once, and every Figma instance maps 1:1 to a component class in `ux-zone/components/`.

Source of truth for values: `ux-zone/tokens.json`. Do not invent new colors, sizes, or radii in Figma. If a token does not exist, add it to `tokens.json` first.

## File structure

Pages in the Figma file, in this order:

1. **Cover** - team name, version, last-updated date in DD-MM-YYYY, link to this file in GitHub.
2. **Tokens** - one frame per token group (color, typography, spacing, radius, shadow, breakpoint). Each frame is read-only documentation, not instances.
3. **Components > Article** - tag-chip, body-paragraph (text styles only), body-heading (text styles only), hero-article, inline-image, pull-quote.
4. **Components > Chrome** - header-nav, header-nav-rich, footer.
5. **Components > Navigation** - breadcrumb, tab-bar, filter-pill.
6. **Components > Cards** - restaurant-card, rating-chip, price-tag, collection-card.
7. **Templates** - landing, listing, restaurant-detail, article (built in Phase 04).

## Color styles

Create one Figma color style per token. Name pattern: `color/<token-name>` (matching `--uxz-color-<token-name>`).

| Style name | Hex | Token |
|---|---|---|
| `color/text-default` | #020817 | text-default |
| `color/text-heading` | #111827 | text-heading |
| `color/text-body` | #293142 | text-body |
| `color/text-muted` | #696969 | text-muted |
| `color/text-secondary` | #828282 | text-secondary |
| `color/text-card-title` | #1C1C1C | text-card-title |
| `color/text-footer-heading` | #1C1C1C | text-footer-heading |
| `color/text-h1` | #000000 | text-h1 |
| `color/link` | #7293F3 | link |
| `color/bg-page` | #FFFFFF | bg-page |
| `color/bg-footer` | #F8F8F8 | bg-footer |
| `color/brand-red` | #CB202D | brand-red |
| `color/border-muted` | #E5E7EB | border-muted |
| `color/border-pill` | #E8E8E8 | border-pill |
| `color/rating-green` | #3F7E00 | rating-green |
| `color/rating-yellow` | #9C7E00 | rating-yellow |
| `color/rating-red` | #CB202D | rating-red |
| `color/bg-promoted` | rgba(0,0,0,0.3) | bg-promoted |
| `color/white` | #FFFFFF | white |

## Text styles

Name pattern: `text/<style-name>`. All styles use the family from the relevant token (Be Vietnam Pro for article, Okra for footer / product UI). Numeric values: size / line-height / weight.

| Style name | Family | Size / LH / Weight | Extras |
|---|---|---|---|
| `text/h1` | Be Vietnam Pro | 60 / 72 / 500 | letter-spacing -0.5px |
| `text/h2` | Be Vietnam Pro | 36 / 44 / 600 | |
| `text/h3` | Be Vietnam Pro | 24 / 32 / 600 | |
| `text/h4` | Be Vietnam Pro | 20 / 28 / 600 | |
| `text/body` | Be Vietnam Pro | 20 / 32.5 / 300 | |
| `text/body-bold` | Be Vietnam Pro | 20 / 32.5 / 500 | |
| `text/body-italic` | Be Vietnam Pro | 20 / 32.5 / 300 | italic |
| `text/blockquote` | Be Vietnam Pro | 18 / 32 / 500 | |
| `text/meta` | Okra | 14 / 20 / 300 | |
| `text/footer-h3` | Okra | 14 / 20 / 500 | letter-spacing 2px, uppercase |
| `text/copy` | Okra | 13 / 21.125 / 300 | |
| `text/tag` | Be Vietnam Pro | 12 / 16 / 500 | letter-spacing 1px, uppercase |
| `text/card-title` | Okra | 17 / 20.4 / 500 | |
| `text/card-meta` | Okra | 14 / 21 / 300 | |
| `text/pill` | Okra | 14 / 20 / 400 | |

## Effect styles

| Style name | Value | Token |
|---|---|---|
| `effect/shadow-sm` | 0 1px 2px 0 rgba(0,0,0,0.05) | shadow.sm |
| `effect/shadow-md` | 0 4px 6px -1px rgba(0,0,0,0.1), 0 2px 4px -2px rgba(0,0,0,0.06) | shadow.md |

## Spacing variables (Figma variables, not styles)

Create a variable collection `space` with these number variables (value in pixels):

| Variable | Value |
|---|---|
| `space/0` | 0 |
| `space/1` | 4 |
| `space/2` | 8 |
| `space/3` | 12 |
| `space/4` | 16 |
| `space/5` | 24 |
| `space/6` | 32 |
| `space/7` | 40 |
| `space/8` | 64 |
| `space/9` | 120 |

Use these in auto-layout gap and padding fields. Do not type raw numbers.

## Radius variables

| Variable | Value |
|---|---|
| `radius/none` | 0 |
| `radius/sm` | 4 |
| `radius/md` | 8 |
| `radius/lg` | 12 |
| `radius/full` | 9999 |
| `radius/pill` | 2 |

## Components and component properties

Each component frame mirrors a folder under `ux-zone/components/`. The per-component figma.md inside that folder is the authoritative spec for its variants, properties, auto-layout rules, and constraints.

Quick index:

| Figma component | Folder | Variants | Key properties |
|---|---|---|---|
| `tag-chip` | tag-chip | default, brand | label |
| `header-nav` | header-nav | desktop, mobile | logoSrc, href |
| `header-nav-rich` | header-nav-rich | desktop, tablet, mobile | logoSrc, locationValue, searchPlaceholder, showAuth |
| `hero-article` | hero-article | desktop, tablet, mobile | tag, title, author, date, readTime, heroSrc |
| `breadcrumb` | breadcrumb | (none) | items |
| `tab-bar` | tab-bar | per-tab state | tabs, selectedId |
| `filter-pill` | filter-pill | default, pressed, with-icon | label, iconSrc, pressed |
| `rating-chip` | rating-chip | green, yellow, red | value, tier |
| `price-tag` | price-tag | (none) | amount, suffix, currency |
| `restaurant-card` | restaurant-card | desktop, mobile, promoted, offer | imageSrc, name, rating, cuisines, costForTwo, locality, distance, offerLabel, promoted |
| `collection-card` | collection-card | desktop, mobile | imgSrc, title, placesLabel, href |
| `footer` | footer | desktop, tablet, mobile, mobile-narrow | logoSrc, columns, social, stores, legal |
| `body-paragraph` | body-paragraph | (text styles only, no component) | n/a |
| `body-heading` | body-heading | (text styles only) | n/a |
| `inline-image` | inline-image | (none) | src, caption |
| `pull-quote` | pull-quote | (none) | quote, attribution |

## Rules for designers

1. Never edit a color, text, or effect style locally. Edit the source token, regen the library, push.
2. Every text frame must have a `text/<style>` applied; never set font properties manually.
3. Every fill must reference a `color/<style>` or the closest matching variable; never use a raw hex.
4. Every padding and gap must reference a `space/<n>` variable; never type a raw number.
5. When adding a new component, copy a similar component's frame and rename. Then write a `figma.md` in the matching code folder before merging.

## Rules for engineers reading this

- The library is documentation, not a build dependency. If Figma drifts from code, code wins. The build script `build-tailwind.mjs` regenerates the Tailwind config from `tokens.json`; if a value moved in Figma without moving in tokens.json, push back on the designer.
- All variant names in Figma must match the Tailwind class state (`pressed` -> `aria-pressed="true"`, `selected` -> `aria-selected="true"`). Do not invent new state names.
