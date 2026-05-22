# footer, Figma spec

Frame: `footer` under `Components > Chrome`.

## Variants
- `desktop` (>=1024px): 5 columns
- `tablet` (768-1023px): 3 columns
- `mobile` (<=768px): 2 columns
- `mobile-narrow` (<=360px): 1 column stacked

## Properties
| Property | Type | Default |
|---|---|---|
| `logoSrc` | Instance Swap | Zomato logo |
| `columns` | Component data | 4 link columns |
| `social` | Component data | 5 icons |
| `stores` | Component data | 2 app store badges |
| `legal` | Text | copyright line |

## Auto-layout
- Outer: vertical, max width 1200px, center
- Padding: 64px (`uxz-8`) top + bottom desktop; 40px (`uxz-7`) tablet; 32px mobile sides
- Grid columns: variant-dependent (see Variants)
- Gap: 40px (`uxz-7`) desktop, 32px tablet

## Color styles
- background: `color/bg-footer`
- column heading: `color/text-footer-heading`
- link: `color/text-muted`; hover -> `color/text-footer-heading`

## Text styles
- column heading: `text/footer-h3` (14 / 20 / weight 500 / letter-spacing 2px / uppercase)
- link: `text/meta` (14 / 20 / weight 300)
- legal: `text/copy` (13 / 21.125 / weight 300)
