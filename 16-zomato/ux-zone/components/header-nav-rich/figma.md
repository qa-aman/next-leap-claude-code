# header-nav-rich, Figma spec

Frame: `header-nav-rich` under `Components > Chrome`.

## Variants
- `desktop` (>=1024px): logo + search bar + auth, single row
- `tablet` (768-1023px): narrower location max-width, same row
- `mobile` (<=768px): location and search stack vertically, auth hidden

## Properties
| Property | Type | Default |
|---|---|---|
| `logoSrc` | Instance Swap | Zomato logo |
| `locationValue` | Text | (empty) |
| `searchPlaceholder` | Text | Search for restaurant, cuisine or a dish |
| `showAuth` | Boolean | true |

## Auto-layout
- Outer: horizontal, gap 32px (`uxz-6`), padding 16px top/bottom, 40px sides
- Search container: horizontal, gap 12px, padding 8px / 16px, 1px border `color/border-pill`, radius 8px (`radius/md`), shadow `shadow/sm`
- Divider: 1px vertical line, height 24px

## Color styles
- background: `color/bg-page`
- input placeholder: `color/text-secondary`
- input text: `color/text-card-title`
- auth hover: `color/brand-red`

## Text styles
- input + auth: `text/meta` (14 / 20 / weight 400)
