# price-tag

Inline cost line, used inside `restaurant-card`.

- Source URL: https://www.zomato.com/ncr/restaurants
- Source selector: `a[href*="/info"] p:nth-of-type(2)`
- Source quotes (verbatim): `₹3,000 for two`, `₹2,500 for two`, `₹3,300 for two`

Reuses `size-card-meta` tokens. Always render the rupee symbol (`&#8377;`) ahead of the integer with a comma every 3 digits.
