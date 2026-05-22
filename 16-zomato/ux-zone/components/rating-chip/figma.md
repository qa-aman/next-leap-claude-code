# rating-chip, Figma spec

Frame: `rating-chip` under `Components > Cards`.

## Variants
Component property `tier`:
- `green` (rating >= 4.0)
- `yellow` (3.0 - 3.9)
- `red` (< 3.0)

## Properties
| Property | Type | Default |
|---|---|---|
| `value` | Text | 4.3 |
| `tier` | Variant | green |

## Auto-layout
- Direction: horizontal
- Gap: 4px (`uxz-1`)
- Padding: 4px top + bottom, 8px (`uxz-2`) sides
- Corner radius: 4px (`radius/sm`)
- Hug width + height

## Color styles
- green: fill `color/rating-green`
- yellow: fill `color/rating-yellow`
- red: fill `color/rating-red`
- text: `color/white`

## Text styles
- value: `text/meta` weight 500 (14 / 20)

## Note
Tier mapping is derived, not extracted; threshold may shift if a new sample reveals different boundaries.
