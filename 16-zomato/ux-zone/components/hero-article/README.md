# hero-article

Top of an article: category tag, h1, byline + date + read time, then a full-bleed hero image.

- Source URL: https://www.zomato.com/blog/sushi/
- Source selector: `article > div:first-child` and the following `img`
- Source quotes (verbatim):
  - tag: `technology`
  - title: `Zomato's new Sushi Design System`
  - author: `Vijay Verma`
  - date: `August 26, 2019`
  - read time: `6 mins read`
  - hero alt: `Zomato's new Sushi Design System`

## Composition
Uses `uxz-tag-chip` for the category and `uxz-hero-article__*` for the rest. Image lives inside a `<figure>` for semantics, no caption on the hero.

## Responsive
- 1280px: 60/72 h1
- 1024px: 44/52
- 768px:  32/40
- 360px:  28/36
