# filter-pill

Rounded pill in a horizontal row for filter selection. The first pill on the live page has a filter icon and the label "Filters"; the rest are label-only. Active state is dark fill.

- Source URL: https://www.zomato.com/ncr/restaurants
- Source selector: filter row directly above the listing grid; pills are styled-components instances
- Source quotes (verbatim): `Filters`, `Offers`, `Rating: 4.5+`, `Pet friendly`, `Outdoor seating`, `Serves Alcohol`, `Open Now`

## Variants
- default: white bg, gray border, dark label
- with-icon: `Filters` pill includes a leading icon
- pressed: `[aria-pressed="true"]` switches to dark fill, white label (used for "Open Now" example)

## Note
The source page's styled-components do not expose computed border/padding via simple selectors. Border (`1px solid #E8E8E8`), radius (`full`), padding (`8px 16px`) are visually approximated from the reference screenshot at 1280px. Update once exact values are exposed via DevTools sampling.
