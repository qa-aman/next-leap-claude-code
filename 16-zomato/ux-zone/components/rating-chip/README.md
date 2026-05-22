# rating-chip

Small colored pill showing a numeric rating and a star.

- Source URL: https://www.zomato.com/ncr/restaurants
- Source selector: `a[href*="/info"] img[alt="star-fill"]` and its parent
- Source quote (verbatim): `4.3`, `4.2`, `4.1` (samples from the listing card grid)

## Tiers (derived from observed samples)
- `green` >= 4.0 (most common in listing)
- `yellow` 3.0 to 3.9
- `red` < 3.0

The threshold mapping is derived, not extracted. The live page samples observed were all green (4.1 to 4.5). Document any change here when a real low-rating sample is captured.

## Usage
```html
<span class="uxz-rating-chip" data-tier="green">4.3<img src="ux-zone/assets/icons/star-fill.svg" alt=""></span>
```
