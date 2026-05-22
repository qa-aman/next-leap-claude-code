# hero-article, Figma spec

Frame: `hero-article` under `Components > Article`. Composes one instance of `tag-chip`.

## Variants
- `desktop` (>=1024px)
- `tablet` (768-1023px): h1 44/52
- `mobile` (<768px): h1 32/40

## Properties
| Property | Type | Default | Maps |
|---|---|---|---|
| `tag` | Text | technology | nested tag-chip instance label |
| `title` | Text | h1 text node |
| `author` | Text | meta row first item |
| `date` | Text | meta row third item |
| `readTime` | Text | meta row fifth item |
| `heroSrc` | Instance Swap | figure image fill |

## Auto-layout
- Direction: vertical
- Padding: 120px (`uxz-9`) top, 32px (`uxz-6`) sides, 32px bottom
- Gap: 24px between tag, h1, meta row, figure
- Max width: 896px (`maxWidth.uxz-article`)
- Mx auto: yes

## Color styles
- h1: `color/text-h1` (#000000)
- meta: `color/text-body` (#293142)
- meta separator: `color/text-muted`

## Text styles
- h1: `text/h1` (60 / 72 / weight 500)
- meta: `text/meta` (14 / 20 / weight 300)
- responsive: switch to `text/h1-tablet` 44/52 and `text/h1-mobile` 32/40 per variant.
