# tab-bar, Figma spec

Frame: `tab-bar` under `Components > Navigation`.

## Variants
Component property `state` of type Variant per tab instance:
- `default` (muted label, no underline)
- `selected` (brand-red label + 3px underline)

## Properties (per tab instance)
| Property | Type | Default |
|---|---|---|
| `label` | Text | Dining Out |

## Auto-layout
- Container direction: horizontal
- Gap: 64px (`uxz-8`) desktop, 32px (`uxz-6`) mobile
- Tab padding: 16px top + bottom

## Color styles
- default label: `color/text-muted`
- selected label: `color/brand-red`
- underline: `color/brand-red`
- bottom border: 1px `color/border-pill`

## Text styles
- label: `text/h4` (20 / 28 / weight 600)
