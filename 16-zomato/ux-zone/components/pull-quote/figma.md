# pull-quote, Figma spec

Frame: `pull-quote` under `Components > Article`.

## Properties
| Property | Type | Default |
|---|---|---|
| `quote` | Text | "The effort required to build a design system is tiny compared to the effort required to maintain it." |
| `attribution` | Text | Kyle Peatt |

## Auto-layout
- Direction: horizontal
- Padding: 40px (`uxz-7`) left, 24px (`uxz-5`) right
- Border: 4px solid `color/brand-red` on left edge
- Hug height

## Color styles
- quote fill: `color/text-body`
- attribution fill: `color/text-heading`
- border: `color/brand-red`

## Text styles
- quote: `text/body-italic`
- attribution: `text/blockquote` (18 / 32 / weight 500)

## Note
The source page has no left border; this 4px brand-red strip is an extension noted in the component README.
