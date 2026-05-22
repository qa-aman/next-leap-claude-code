# Template: article

A full blog/article page composed only from Phase 01 components.

## Components used
- header-nav
- hero-article (uses tag-chip)
- body-paragraph (`.uxz-prose` wrapper)
- body-heading (h3, h4)
- inline-image
- pull-quote
- footer

## Where to swap content
- `<h1 class="uxz-hero-article__title">` - article title
- `.uxz-hero-article__meta` spans - author / date / read time
- `.uxz-hero-article__media img` - hero image
- `.uxz-prose` children - body markdown (p, strong, em, a, blockquote, figure, h2/h3/h4)
- `.uxz-footer__cols` - footer columns

## Responsive behavior
- 1280px: 60/72 hero h1, max-width 896px article column
- 768px:  32/40 hero h1, 18/30 body
- 360px:  28/36 hero h1

## Stylesheets linked
8 files in `<head>`. To use in a different prototype, copy this `<link>` block verbatim and update the relative path from `../../` to your kit location.
