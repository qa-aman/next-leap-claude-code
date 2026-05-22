# tab-bar

Top-level mode switcher. On the source page it switches between Dining Out / Delivery / Nightlife. Active tab is brand-red with a 3px underline.

- Source URL: https://www.zomato.com/ncr/restaurants
- Source selector: `[role="tablist"]` and its `[role="tab"]` children
- Source quotes (verbatim): `Dining Out`, `Delivery`, `Nightlife`

## Variants
- default: muted label
- selected: `aria-selected="true"` sets brand-red color and underline indicator

## Note
The source tabs include illustration images per tab; this component renders text-only for kit reuse. Add illustrations by placing an `<img>` before `.uxz-tab-bar__label`.
