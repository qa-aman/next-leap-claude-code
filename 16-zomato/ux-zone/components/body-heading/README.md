# body-heading

In-article section headings: h2 (added for completeness), h3, h4.

- Source URL: https://www.zomato.com/blog/sushi/
- Source selectors: `article h3`, `article h4`
- Source quotes (verbatim):
  - h3: `What is a Design System?`, `Why build a Design System?`, `How did we come up with a brand new system?`, `The real deal`, `Development`, `What next?`
  - h4: `Design Principle`, `Structure of Design System`, `Creating Foundations`, `Pattern & Templates`

## Note on h2
The source page does not use `<h2>` between h1 and h3. A token-driven h2 style (36/44 weight 600) is provided for prototypes that need it; the value is interpolated between h1 and h3, marked in tokens as `scale step`.
