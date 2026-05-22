# body-paragraph (prose), Figma spec

Frame: `prose` under `Components > Article`. This is a text style + container, not a component instance per paragraph. Apply the text styles below to any text layer in an article column.

## Variants
- `desktop`: body 20/32.5 weight 300
- `mobile` (<=768px): body 18/30

## Text styles
- `text/body` -> Be Vietnam Pro 20 / 32.5 / weight 300 / color `text-body`
- `text/body-bold` -> 20 / 32.5 / weight 500 / color `text-heading` (for strong)
- `text/body-italic` -> 20 / 32.5 / weight 300 / italic / color `text-body` (for em)
- `text/link` -> 20 / 32.5 / weight 300 / color `link` (#7293F3) (for a)

## Auto-layout (container)
- Max width: 896px
- Padding: 0 32px (sides only)
- Gap between paragraphs: 24px (`uxz-5`)
