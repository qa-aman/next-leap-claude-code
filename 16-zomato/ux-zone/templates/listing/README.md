# Template: listing

Restaurant listing page. Uses Phase 02 components and a small page-level grid wrapper.

## Components used
- header-nav-rich (logo + location + search + auth)
- breadcrumb
- tab-bar (Dining Out / Delivery / Nightlife)
- filter-pill row
- restaurant-card (×6 in 3-column grid)
- footer

## Page-level styles
This template introduces a `.uxz-listing` wrapper, an `.uxz-listing__h1` page title style, and a `.uxz-listing__grid` 3-column grid. These are template-only and not a new component.

## Where to swap content
- `.uxz-header-rich input[type="text"]` - location and search values
- `.uxz-breadcrumb` items
- `.uxz-tab-bar__tab` labels and aria-selected
- `.uxz-filter-row` pills (add or remove, set `aria-pressed="true"` for active)
- `.uxz-restaurant-card` grid children - duplicate the card markup, swap image, name, rating, cuisines, price, locality, distance

## Responsive
- 1280px: 3 columns
- 1024px: 2 columns
- 640px:  1 column
