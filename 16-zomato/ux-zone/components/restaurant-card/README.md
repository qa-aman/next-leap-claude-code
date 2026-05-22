# restaurant-card

The primary listing unit: hero image, optional Promoted badge, optional offer badge, name, rating chip, cuisines, cost, locality + distance.

- Source URL: https://www.zomato.com/ncr/restaurants
- Source selector: `a[href*="/info"]` containing `img[alt="Restaurant Card"]` and `h4`
- Source quotes (verbatim, sample row):
  - name: `Connaught Club House`
  - rating: `4.3`
  - cuisines: `North Indian, Mughlai, Italian, Continental, Asian, Fast Food, Desserts`
  - price: `₹3,000 for two`
  - locality: `Connaught Place, New Delhi`
  - distance: `1 km`
  - promoted: `Promoted`
  - offer: `Flat 10% OFF`

## Composition
Uses `rating-chip` and `price-tag` as sub-components. The dashed divider above the foot row visually separates address from card body.

## Notes
- Card image (`__image`) on the live page is lazy-loaded; the kit ships with a placeholder image from Phase 01. Swap the `src` per prototype.
- Card width 328px matches the listing grid at 1280px (3 columns across the 1024-wide content area).
- Optional badges: omit the `__promoted` and/or `__offer` element to render a clean card.
