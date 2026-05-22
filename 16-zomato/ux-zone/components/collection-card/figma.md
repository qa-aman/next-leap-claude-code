# collection-card, Figma spec

Frame: `collection-card` under `Components > Cards`.

## Variants
- `desktop` (>=768px): 274 x 380
- `mobile` (<768px): 220 x 300

## Properties
| Property | Type | Default |
|---|---|---|
| `imgSrc` | Instance Swap | Collection image |
| `title` | Text | Insta-worthy spots |
| `placesLabel` | Text | 82 Places |
| `href` | Text | /ncr/insta-worthy |

## Auto-layout
- Outer: fixed size, image fills frame
- Overlay: positioned at bottom, padding 16px (`uxz-4`) top/bottom, 24px (`uxz-5`) sides
- Background: linear gradient bottom black 65% -> transparent

## Color styles
- text: `color/white`

## Text styles
- title: `text/h4` (20 / 28 / weight 600)
- places: `text/meta` (14 / 20 / weight 300)

## Effect styles
- gradient overlay; no shadow on card itself
