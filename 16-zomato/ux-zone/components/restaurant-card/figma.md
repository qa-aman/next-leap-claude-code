# restaurant-card, Figma spec

Frame: `restaurant-card` under `Components > Cards`. Composes `rating-chip` and `price-tag` as instances.

## Variants
- `desktop`: 328 width
- `mobile`: fluid up to 480px
- `promoted`: Boolean property toggles "Promoted" overlay
- `offer`: Boolean property toggles offer pill in image overlay

## Properties
| Property | Type | Default |
|---|---|---|
| `imageSrc` | Instance Swap | Restaurant image |
| `name` | Text | Connaught Club House |
| `rating` | Text (number) | 4.3 |
| `cuisines` | Text | North Indian, Mughlai, Italian, ... |
| `costForTwo` | Text (number) | 3,000 |
| `locality` | Text | Connaught Place, New Delhi |
| `distance` | Text | 1 km |
| `offerLabel` | Text | Flat 10% OFF |
| `promoted` | Boolean | false |

## Auto-layout
- Outer card: vertical, gap 12px (`uxz-3`)
- Media: 16:9 aspect, radius 8px (`radius/md`)
- Body: vertical, gap 2px between rows, 8px before foot divider
- Foot row: horizontal, dashed top border `color/border-muted`

## Color styles
- title: `color/text-card-title`
- cuisines / price / locality / distance: `color/text-muted`
- offer fill: `color/bg-page` (chip is on top of image)
- offer text: `color/brand-red`
- promoted overlay: `color/bg-promoted` (rgba 0,0,0,0.3)

## Text styles
- title: `text/card-title` (17 / 20.4 / weight 500)
- card meta: `text/card-meta` (14 / 21 / weight 300)
- promoted: 11 / 16 / weight 400
- offer: 12 / 16 / weight 500

## Composition rules
- Always include `rating-chip` instance to the right of the title
- `price-tag` always immediately below cuisines line
- `promoted` and `offer` overlays are independent toggles
