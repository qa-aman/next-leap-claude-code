# filter-pill, Figma spec

Frame: `filter-pill` under `Components > Navigation`.

## Variants
Component properties:
- `state`: `default` | `pressed`
- `icon`: `none` | `leading`

## Properties
| Property | Type | Default |
|---|---|---|
| `label` | Text | Open Now |
| `iconSrc` | Instance Swap | filter icon |

## Auto-layout
- Direction: horizontal
- Gap: 8px (`uxz-2`)
- Padding: 8px top+bottom, 16px (`uxz-4`) sides; 12px (`uxz-3`) left when icon present
- Hug width

## Color styles
- default fill: `color/bg-page`; border 1px `color/border-pill`; text `color/text-card-title`
- pressed fill: `color/text-card-title`; text `color/bg-page`
- hover (default only): shadow `effect/shadow-sm`

## Text styles
- label: `text/pill` (14 / 20 / weight 400)
