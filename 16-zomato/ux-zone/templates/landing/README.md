# Template: landing

Discovery/landing page: header, mode tabs, collection carousel, top picks grid, footer.

## Components used
- header-nav-rich
- tab-bar
- collection-card (×4 in horizontal scroller)
- restaurant-card (×3 in 3-column grid)
- footer

## Page-level styles
Local-only: `.uxz-landing` wrapper, `.uxz-landing__section`, `.uxz-landing__section-title`, `.uxz-landing__hscroll` (horizontal scroller), `.uxz-landing__grid`.

## Where to swap content
- Header search defaults
- Tab labels and selected state
- Collection cards: image, title, place count, href
- Top picks grid: same as listing template
- Footer columns

## Responsive
- 1280px: 3-col grid, horizontal collection scroll
- 1024px: 2-col grid
- 640px: 1-col grid
- Collection scroller stays horizontal at all widths
