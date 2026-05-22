# header-nav

Sticky top navigation. On the Zomato blog source page this is logo-only, no search, no account menu, no in-page links.

- Source URL: https://www.zomato.com/blog/sushi/
- Source selector: `header` (containing one `a > img` with alt="Zomato")
- Source quote: alt text "Zomato"

## Variants
- default: white background, bottom border, logo left-aligned
- mobile (<=768px): height reduces from 120px to 72px

## When to use
Top of every prototype page that should mirror Zomato blog chrome.

## Snippet
```html
<link rel="stylesheet" href="tokens.css">
<link rel="stylesheet" href="components/header-nav/style.css">
<header class="uxz-header-nav">
  <a class="uxz-header-nav__brand" href="/"><img src="assets/images/b40b97e677bc7b2ca77c58c61db266fe1603954218.png" alt="Zomato" height="26"></a>
</header>
```
