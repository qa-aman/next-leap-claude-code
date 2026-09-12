/**
 * ux-designer runtime audit.
 *
 * Paste the whole file into browser_evaluate (Playwright MCP) or evaluate_script
 * (Chrome DevTools MCP) with the mockup or the page under review loaded.
 * Returns a JSON-serialisable object.
 *
 * This catches what static analysis honestly cannot: real contrast against
 * whatever actually rendered underneath, real hit-target sizes, real overlap.
 *
 * Run it once per theme and once per viewport width that matters. A page can
 * pass at 1440px light and fail at 390px dark, and that is a real failure.
 *
 * Elements inside [data-ux-chrome] are review furniture and are skipped.
 *
 * Run it in a REAL browser. A DOM shim such as jsdom has no layout engine, does
 * not resolve var() in computed styles, and does not apply :focus-visible, so it
 * reports a storm of false ghost-button, overlap, clipping and focus findings.
 * Those are artifacts of the shim, not defects in the page.
 */
(function () {
  var MIN_TARGET = 44;      // CSS px, Apple HIG / NN-g touch research
  var MIN_GAP = 8;          // CSS px between adjacent interactive elements
  var SCALE = [0, 1, 2, 4, 8, 12, 16, 20, 24, 32, 40, 48, 64, 80, 96, 128];

  var findings = [];

  /** innerText is not implemented everywhere (jsdom, some embedded engines). */
  function label(el) {
    if (!el) return '';
    var t = el.innerText;
    if (t === undefined || t === null) t = el.textContent;
    return String(t || el.value || el.alt || '').trim();
  }

  function add(rule, severity, el, message, evidence) {
    findings.push({
      rule: rule,
      severity: severity,
      selector: path(el),
      text: label(el).slice(0, 60),
      message: message,
      evidence: evidence === undefined ? null : evidence
    });
  }

  function path(el) {
    if (!el || !el.tagName) return null;
    var parts = [];
    while (el && el.tagName && parts.length < 5) {
      var s = el.tagName.toLowerCase();
      if (el.id) { parts.unshift(s + '#' + el.id); break; }
      if (el.className && typeof el.className === 'string') {
        s += '.' + el.className.trim().split(/\s+/).slice(0, 2).join('.');
      }
      var sibs = el.parentElement ? [].filter.call(el.parentElement.children, function (c) {
        return c.tagName === el.tagName;
      }) : [];
      if (sibs.length > 1) s += ':nth-of-type(' + ([].indexOf.call(sibs, el) + 1) + ')';
      parts.unshift(s);
      el = el.parentElement;
    }
    return parts.join(' > ');
  }

  // ---------------------------------------------------------------- colour
  function rgb(str) {
    var m = String(str).match(/rgba?\(([^)]+)\)/);
    if (!m) return null;
    var p = m[1].split(/[,\s/]+/).filter(Boolean).map(parseFloat);
    return { r: p[0], g: p[1], b: p[2], a: p.length > 3 ? p[3] : 1 };
  }
  function over(fg, bg) {                       // alpha-composite fg onto bg
    var a = fg.a;
    return { r: fg.r * a + bg.r * (1 - a), g: fg.g * a + bg.g * (1 - a), b: fg.b * a + bg.b * (1 - a), a: 1 };
  }
  function lum(c) {
    function ch(v) { v /= 255; return v <= 0.04045 ? v / 12.92 : Math.pow((v + 0.055) / 1.055, 2.4); }
    return 0.2126 * ch(c.r) + 0.7152 * ch(c.g) + 0.0722 * ch(c.b);
  }
  function ratio(a, b) {
    var x = lum(a), y = lum(b);
    return (Math.max(x, y) + 0.05) / (Math.min(x, y) + 0.05);
  }
  /** Walk ancestors compositing backgrounds until fully opaque. */
  function effectiveBg(el) {
    var acc = null;
    var node = el;
    while (node && node.nodeType === 1) {
      var c = rgb(getComputedStyle(node).backgroundColor);
      if (c && c.a > 0) acc = acc ? over(acc, c) : c;
      if (acc && acc.a >= 0.999) return acc;
      node = node.parentElement;
    }
    var body = rgb(getComputedStyle(document.body).backgroundColor);
    var base = body && body.a > 0 ? body : { r: 255, g: 255, b: 255, a: 1 };
    return acc ? over(acc, base) : base;
  }

  function visible(el) {
    var s = getComputedStyle(el);
    if (s.display === 'none' || s.visibility === 'hidden' || parseFloat(s.opacity) === 0) return false;
    var r = el.getBoundingClientRect();
    return r.width > 0 && r.height > 0;
  }
  function chrome(el) { return !!el.closest('[data-ux-chrome]'); }

  var INTERACTIVE = 'a[href], button, input:not([type=hidden]), select, textarea, [role=button], [role=link], [role=tab], [role=switch], [tabindex]:not([tabindex="-1"])';

  // ---------------------------------------------------------------- 1. text contrast
  var walker = document.createTreeWalker(document.body, NodeFilter.SHOW_TEXT, null);
  var seen = new Set();
  var node;
  while ((node = walker.nextNode())) {
    if (!node.nodeValue.trim()) continue;
    var el = node.parentElement;
    if (!el || seen.has(el) || chrome(el) || !visible(el)) continue;
    seen.add(el);
    var cs = getComputedStyle(el);
    var fg = rgb(cs.color);
    if (!fg) continue;
    var bg = effectiveBg(el);
    var composed = fg.a < 1 ? over(fg, bg) : fg;
    var r = ratio(composed, bg);
    var size = parseFloat(cs.fontSize);
    var weight = parseInt(cs.fontWeight, 10) || 400;
    var large = size >= 24 || (size >= 18.66 && weight >= 700);
    var need = large ? 3 : 4.5;
    if (r < need) {
      add('contrast', r < need - 1 ? 4 : 3, el,
          'text contrast ' + r.toFixed(2) + ':1, needs ' + need + ':1 (WCAG 1.4.3)',
          { ratio: +r.toFixed(2), required: need, color: cs.color, background: 'rgb(' + [bg.r, bg.g, bg.b].map(Math.round).join(',') + ')', fontSize: size, fontWeight: weight });
    }
  }

  // ---------------------------------------------------------------- 2. interactive elements
  var boxes = [];
  [].forEach.call(document.querySelectorAll(INTERACTIVE), function (el) {
    if (chrome(el) || !visible(el)) return;
    var r = el.getBoundingClientRect();
    boxes.push({ el: el, r: r });

    // 2a hit target
    if (r.width < MIN_TARGET || r.height < MIN_TARGET) {
      add('hit-target', r.width < 24 || r.height < 24 ? 4 : 3, el,
          'hit target ' + Math.round(r.width) + 'x' + Math.round(r.height) + 'px, needs ' + MIN_TARGET + 'x' + MIN_TARGET,
          { width: Math.round(r.width), height: Math.round(r.height) });
    }

    // 2b perceivable at rest: needs fill, border, or outline distinct from its surface
    var cs = getComputedStyle(el);
    var tag = el.tagName.toLowerCase();
    if (tag === 'button' || el.getAttribute('role') === 'button') {
      var own = rgb(cs.backgroundColor);
      var surface = effectiveBg(el.parentElement || document.body);
      var hasFill = own && own.a > 0.05 && ratio(over(own, surface), surface) >= 1.1;
      var bw = ['borderTopWidth', 'borderRightWidth', 'borderBottomWidth', 'borderLeftWidth']
        .map(function (p) { return parseFloat(cs[p]) || 0; });
      var borderCol = rgb(cs.borderTopColor);
      var hasBorder = Math.max.apply(null, bw) > 0 && borderCol && borderCol.a > 0.05 &&
                      ratio(over(borderCol, surface), surface) >= 3;
      var hasOutline = (parseFloat(cs.outlineWidth) || 0) > 0 && cs.outlineStyle !== 'none';
      if (!hasFill && !hasBorder && !hasOutline) {
        add('ghost-button', 4, el,
            'button is not perceivable at rest: no fill, no 3:1 border, no outline (WCAG 1.4.11)',
            { background: cs.backgroundColor, border: cs.border });
      }
    }

    // 2c focus indicator
    try {
      var before = getComputedStyle(el);
      var beforeSig = [before.outlineWidth, before.outlineStyle, before.boxShadow, before.borderColor].join('|');
      el.focus({ preventScroll: true });
      var after = getComputedStyle(el);
      var afterSig = [after.outlineWidth, after.outlineStyle, after.boxShadow, after.borderColor].join('|');
      if (beforeSig === afterSig) {
        add('focus-indicator', 3, el, 'no visible change on focus (WCAG 2.4.7)', null);
      }
      el.blur();
    } catch (e) { /* focus can throw on detached nodes */ }

    // 2d off-grid padding
    ['paddingTop', 'paddingRight', 'paddingBottom', 'paddingLeft'].forEach(function (p) {
      var v = parseFloat(cs[p]);
      if (!isNaN(v) && v > 0 && SCALE.indexOf(Math.round(v)) === -1 && Math.round(v) % 4 !== 0) {
        add('spacing-grid', 1, el, 'off-grid ' + p + ': ' + v + 'px', { value: v });
      }
    });
  });

  // ---------------------------------------------------------------- 3. gaps and overlap
  for (var i = 0; i < boxes.length; i++) {
    for (var j = i + 1; j < boxes.length; j++) {
      var a = boxes[i], b = boxes[j];
      if (a.el.contains(b.el) || b.el.contains(a.el)) continue;
      var dx = Math.max(a.r.left - b.r.right, b.r.left - a.r.right);
      var dy = Math.max(a.r.top - b.r.bottom, b.r.top - a.r.bottom);
      if (dx < 0 && dy < 0) {
        add('overlap', 4, a.el, 'overlaps another interactive element: ' + path(b.el), null);
      } else {
        var gap = Math.max(dx, dy);
        if (gap >= 0 && gap < MIN_GAP && dx * dy <= 0) {
          add('gap', 2, a.el, 'only ' + gap.toFixed(1) + 'px from ' + path(b.el) + ', needs ' + MIN_GAP + 'px',
              { gap: +gap.toFixed(1) });
        }
      }
    }
  }

  // ---------------------------------------------------------------- 4. clipping
  [].forEach.call(document.querySelectorAll('*'), function (el) {
    if (chrome(el) || !visible(el)) return;
    var cs = getComputedStyle(el);
    if (cs.overflow !== 'hidden' && cs.overflow !== 'clip') return;
    var pr = el.getBoundingClientRect();
    [].forEach.call(el.children, function (child) {
      if (!visible(child)) return;
      var ccs = getComputedStyle(child);
      if (ccs.boxShadow === 'none') return;
      var cr = child.getBoundingClientRect();
      var slack = Math.min(cr.left - pr.left, pr.right - cr.right, cr.top - pr.top, pr.bottom - cr.bottom);
      if (slack < 4) {
        add('clipping', 2, child,
            'shadow will clip: only ' + slack.toFixed(1) + 'px clear of an overflow:hidden parent',
            { slack: +slack.toFixed(1) });
      }
    });
  });

  // ---------------------------------------------------------------- 5. semantics
  [].forEach.call(document.querySelectorAll('img'), function (el) {
    if (chrome(el) || !visible(el)) return;
    if (!el.hasAttribute('alt')) add('alt-text', 3, el, 'image has no alt attribute (WCAG 1.1.1)', null);
  });
  [].forEach.call(document.querySelectorAll('input:not([type=hidden]), select, textarea'), function (el) {
    if (chrome(el) || !visible(el)) return;
    var labelled = el.labels && el.labels.length ||
                   el.getAttribute('aria-label') || el.getAttribute('aria-labelledby') || el.getAttribute('title');
    if (!labelled) add('label', 3, el, 'form control has no accessible label (WCAG 1.3.1)', null);
  });
  [].forEach.call(document.querySelectorAll('button, [role=button], a[href]'), function (el) {
    if (chrome(el) || !visible(el)) return;
    var name = label(el) || el.getAttribute('aria-label') || el.getAttribute('title') ||
               (el.querySelector('img[alt]') || {}).alt;
    if (!name) add('accessible-name', 3, el, 'interactive element has no accessible name', null);
  });

  // ---------------------------------------------------------------- 6. one primary per scope
  [].forEach.call(document.querySelectorAll('[data-scope]'), function (scope) {
    var n = scope.querySelectorAll('[data-primary]').length;
    if (n > 1) {
      add('primary-cta', 2, scope,
          'scope "' + scope.getAttribute('data-scope') + '" has ' + n + ' primary CTAs, so it has none', { count: n });
    }
  });

  // ---------------------------------------------------------------- summary
  var bySeverity = { 4: 0, 3: 0, 2: 0, 1: 0 };
  findings.forEach(function (f) { bySeverity[f.severity] = (bySeverity[f.severity] || 0) + 1; });
  findings.sort(function (x, y) { return y.severity - x.severity; });

  var osDark = typeof matchMedia === 'function' && matchMedia('(prefers-color-scheme: dark)').matches;
  var activeEl = document.querySelector('[data-state][data-active]');

  return {
    url: location.href,
    viewport: { width: innerWidth, height: innerHeight },
    theme: document.documentElement.getAttribute('data-theme') || (osDark ? 'dark(os)' : 'light(os)'),
    activeState: activeEl ? activeEl.getAttribute('data-state') : null,
    total: findings.length,
    blocking: bySeverity[4] + bySeverity[3],
    bySeverity: bySeverity,
    verdict: (bySeverity[4] + bySeverity[3]) > 0 ? 'FAIL' : (findings.length ? 'PASS with minor findings' : 'PASS'),
    findings: findings.slice(0, 120)
  };
})();
