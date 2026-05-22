# tag-chip, Figma spec

Frame name in library: `tag-chip`. Lives under page `Components > Article`.

## Variants
Component property `variant` of type Variant with values:
- `default` (selected by default)
- `brand`

## Properties
| Property | Type | Default | Maps to |
|---|---|---|---|
| `label` | Text | `technology` | text layer "label" |
| `variant` | Variant | `default` | switches instance |

## Auto-layout
- Direction: horizontal
- Padding: 4px top + bottom (`uxz-1`), 0 left + right for `default`; 4px top + bottom, 12px (`uxz-3`) left + right for `brand`
- Gap: 0
- Hug contents on width, hug on height

## Constraints
- Width: hug
- Height: hug
- Position: relative to parent

## Color styles
- `default` label: `color/text-muted` (token `--uxz-color-text-muted` = #696969)
- `brand` label: `color/bg-page` (#FFFFFF)
- `brand` background fill: `color/brand-red` (#CB202D)

## Text styles
- Font: `Be Vietnam Pro`
- Style name: `text/tag` (size 12 / lh 16 / weight 500 / letter-spacing 1px / uppercase)

## Effect styles
None.

## Mapping back to code
- `uxz-tag-chip` class in HTML/JSX = this Figma component instance with `variant=default`
- `uxz-tag-chip uxz-tag-chip--brand` = instance with `variant=brand`
