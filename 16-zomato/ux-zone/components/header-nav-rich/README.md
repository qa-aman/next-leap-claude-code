# header-nav-rich

Product header used on listing/detail/checkout pages. Logo + combined location-and-search bar + Log in / Sign up. Distinct from `header-nav` (blog logo-only header).

- Source URL: https://www.zomato.com/ncr/restaurants
- Source selector: `header nav`
- Source quotes (verbatim): location placeholder reads `Ywca, Ashoka Rd, Hanuman Road Area, Connaught Place, New Delhi`; search placeholder reads `Search for restaurant, cuisine or a dish`; auth labels `Log in`, `Sign up`

## Variants
- default (>=1024px): all three sections visible
- 768px: auth links hide, location and search stack
- mobile (<360px not specifically styled): inherits 768px rules

## Notes
- The two inputs are real `<input type="text">` with no border, so the surrounding flex container carries the visual chrome.
- The location field is uneditable on the source page (it opens a dropdown); the kit ships it as an editable text input. If you need the dropdown behavior, wire it on the prototype side.
