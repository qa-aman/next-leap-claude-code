# Browser verification

Run against the locally served `ticket-dashboard.html` (not `file://`, which browser tools
block). Use whichever browser tool the session has (Playwright, Chrome DevTools, Claude in
Chrome). Paste this function into its evaluate/JavaScript call.

```js
() => {
  const exec = () => document.querySelector('.exec')?.innerText || 'MISSING';
  const chips = id => [...document.querySelectorAll(`#${id} button`)];
  const tiles = () => [...document.querySelectorAll('#tiles > *')].map(e => e.innerText.replace(/\s+/g, ' '));
  const out = { summary: exec(), allTiles: tiles() };
  const before = out.summary;
  chips('monthchips').at(-1).click();          // latest month
  chips('catchips')[1].click();                // first category
  out.scope = document.getElementById('scope').innerText;
  out.filteredTiles = tiles();
  out.subcategories = [...document.querySelectorAll('#l2list > *')].map(e => e.innerText.replace(/\s+/g, ' '));
  out.summaryUnchangedByFilters = before === exec();
  out.categoryChipRows = new Set(chips('catchips').map(b => b.offsetTop)).size;
  chips('monthchips')[0].click(); chips('catchips')[0].click();
  return out;
}
```

Pass when:

- `summary` shows four pointers and a trust line, and every number matches `summary_numbers.py`.
- `scope` names the month and category you clicked, and `filteredTiles` differ from `allTiles`.
- `subcategories` lists only that category's subcategories, sorted by volume.
- `summaryUnchangedByFilters` is `true`.
- `categoryChipRows` is `1` with the viewport at 1280 px wide (resize first). A phone width may
  wrap; that is intended.
- The console has no errors other than a missing `favicon.ico` from the local server.
