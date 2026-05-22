# header-nav, Figma spec

Frame: `header-nav` under `Components > Chrome`.

## Variants
- `default` (>=1024px viewport): 120px tall
- `mobile` (<=768px viewport): 72px tall

Component property `viewport` of type Variant with the two values above.

## Properties
| Property | Type | Default | Maps to |
|---|---|---|---|
| `logoSrc` | Instance Swap | Zomato logo | `img` layer |
| `href` | Text | `/` | link target |

## Auto-layout
- Direction: horizontal
- Padding: 32px (`uxz-6`) left/right on default, 16px (`uxz-4`) on mobile
- Align: center vertical
- Gap: 0

## Constraints
- Width: fill container
- Height: fixed (120px / 72px)

## Color styles
- Fill: `color/bg-page` (#FFFFFF)
- Bottom border: 1px solid `color/border-muted` (#E5E7EB)

## Text styles
None (logo only).

## Effect styles
None.
