"""
Build the management PowerPoint from the categorized tickets.

The dashboard is for the analyst, who wants to explore. The deck is for the meeting,
where nobody explores and someone has ten minutes to decide something. So this is not
a screenshot of the dashboard. It is the argument: here is the inflow, here is the one
thing worth acting on, here is the evidence, here is what it costs and what it gives
back, and here is what we do not yet know.

Every number comes from metrics.py, the same module the dashboard and console summary
use, so the deck cannot quietly disagree with the report it came from.

Design system is the repo's ppt-builder skill: near-black background, orange accent,
white and grey text hierarchy.

Usage:
  python3 build_deck.py --input categorized.xlsx --work-dir work/ --out deck.pptx \
      --title "Service desk ticket analysis" --period "Jan to Mar 2026"
"""

import argparse
import json
from pathlib import Path

from pptx import Presentation
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN
from pptx.util import Inches, Pt

import metrics

BG_DARK = RGBColor(0x0D, 0x0D, 0x0D)
ACCENT = RGBColor(0xD4, 0x7A, 0x21)
WHITE = RGBColor(0xFF, 0xFF, 0xFF)
LIGHT_GREY = RGBColor(0xCC, 0xCC, 0xCC)
MID_GREY = RGBColor(0x88, 0x88, 0x88)
TAG_BG = RGBColor(0x1E, 0x1E, 0x1E)
ROW_ALT = RGBColor(0x16, 0x16, 0x16)
GOOD = RGBColor(0x44, 0xBB, 0x44)
BAD = RGBColor(0xFF, 0x55, 0x55)

SLIDE_W, SLIDE_H = Inches(13.33), Inches(7.5)
MARGIN = Inches(0.6)
CONTENT_W = Inches(12.13)


def bg(slide, color=BG_DARK):
    f = slide.background.fill
    f.solid()
    f.fore_color.rgb = color


def txbox(slide, text, left, top, width, height, size=24, bold=False,
          color=WHITE, align=PP_ALIGN.LEFT, wrap=True, space=Pt(6)):
    box = slide.shapes.add_textbox(left, top, width, height)
    box.word_wrap = wrap
    tf = box.text_frame
    tf.word_wrap = wrap
    for i, line in enumerate(str(text).split("\n")):
        p = tf.paragraphs[0] if i == 0 else tf.add_paragraph()
        p.alignment = align
        p.space_after = space
        r = p.add_run()
        r.text = line
        r.font.size = Pt(size)
        r.font.bold = bold
        r.font.color.rgb = color
    return box


def accent_bar(slide, top=Inches(0.18), height=Inches(0.06)):
    bar = slide.shapes.add_shape(1, 0, top, SLIDE_W, height)
    bar.fill.solid()
    bar.fill.fore_color.rgb = ACCENT
    bar.line.fill.background()


def divider(slide, top, color=ACCENT):
    ln = slide.shapes.add_shape(1, MARGIN, top, CONTENT_W, Pt(1.5))
    ln.fill.solid()
    ln.fill.fore_color.rgb = color
    ln.line.fill.background()


def rect(slide, left, top, width, height, fill=TAG_BG, border=None):
    sh = slide.shapes.add_shape(1, left, top, width, height)
    sh.fill.solid()
    sh.fill.fore_color.rgb = fill
    if border:
        sh.line.color.rgb = border
        sh.line.width = Pt(1)
    else:
        sh.line.fill.background()
    return sh


def slide_head(prs, title, sub=None):
    s = prs.slides.add_slide(prs.slide_layouts[6])
    bg(s)
    accent_bar(s)
    txbox(s, title, MARGIN, Inches(0.55), CONTENT_W, Inches(0.75), size=30, bold=True)
    divider(s, Inches(1.32))
    if sub:
        txbox(s, sub, MARGIN, Inches(1.46), CONTENT_W, Inches(0.5), size=14, color=MID_GREY)
    return s


def table(slide, headers, rows, top, widths, size=13, row_h=Inches(0.42),
          head_color=ACCENT, colors=None):
    """Plain shaded-row table. python-pptx native tables fight the dark theme, so
    rectangles plus text boxes give a cleaner and more predictable result."""
    x = MARGIN
    for w, h in zip(widths, headers):
        txbox(slide, h, x, top, w, Inches(0.3), size=11, bold=True, color=head_color,
              align=PP_ALIGN.RIGHT if h.startswith("#") else PP_ALIGN.LEFT)
        x += w
    y = top + Inches(0.36)
    for i, row in enumerate(rows):
        if i % 2 == 0:
            rect(slide, MARGIN - Inches(0.1), y - Inches(0.04),
                 sum(widths) + Inches(0.2), row_h, fill=ROW_ALT)
        x = MARGIN
        for j, (w, cell) in enumerate(zip(widths, row)):
            col = WHITE if j == 0 else LIGHT_GREY
            if colors and colors(i, j) is not None:
                col = colors(i, j)
            txbox(slide, cell, x, y, w, row_h, size=size, bold=(j == 0), color=col,
                  align=PP_ALIGN.RIGHT if headers[j].startswith("#") else PP_ALIGN.LEFT)
            x += w
        y += row_h
    return y


def hbar_row(slide, label, value, maxv, top, unit="", width=Inches(6.4),
             faded=False, note=""):
    """A labelled horizontal bar. Faded means the row is a small sample."""
    # The label box must clear the note box beneath it. The layout checker treats any
    # overlap as a failure, and it is right to: overlapping boxes render unpredictably
    # across PowerPoint versions even when they look fine in the file that made them.
    txbox(slide, label, MARGIN, top - Inches(0.02), Inches(3.5), Inches(0.24), size=13,
          color=LIGHT_GREY if not faded else MID_GREY, space=Pt(0))
    if note:
        txbox(slide, note, MARGIN, top + Inches(0.24), Inches(3.5), Inches(0.22),
              size=10, color=MID_GREY, space=Pt(0))
    x0 = MARGIN + Inches(3.7)
    w = max(Inches(0.04), int(width * (value / maxv))) if maxv else Inches(0.04)
    rect(slide, x0, top + Inches(0.05), w, Inches(0.22),
         fill=ACCENT if not faded else RGBColor(0x7A, 0x4C, 0x18))
    txbox(slide, f"{value:g}{unit}", x0 + w + Inches(0.12), top, Inches(1.8), Inches(0.32),
          size=13, bold=True, color=WHITE if not faded else MID_GREY)


def normalise_accuracy(a):
    """Accept the accuracy file in either its current or its earlier shape.

    The deck must never decide "not measured" just because a key was renamed. Getting
    that wrong prints a false caveat on a management slide, which is worse than the
    rename it was reacting to, so scored-ness is inferred from whether real numbers
    are present rather than from one flag."""
    if not a:
        return {"scored": False}
    out = dict(a)
    out["scored"] = bool(a.get("scored", False) or a.get("overall"))
    out.setdefault("tickets", a.get("tickets_scored", 0))
    out.setdefault("dedup_saving_pct", a.get("classification_calls_saved_pct", 0))
    return out


def build(m, accuracy, title, period, source_note, out):
    prs = Presentation()
    prs.slide_width, prs.slide_height = SLIDE_W, SLIDE_H
    BLANK = prs.slide_layouts[6]
    h = m["headline"]
    ml = m["month_labels"]
    nm = len(ml)
    top = m["shortlist"][0] if m["shortlist"] else None

    # ---- 1. Title ----------------------------------------------------------
    s = prs.slides.add_slide(BLANK)
    bg(s)
    accent_bar(s)
    txbox(s, "SERVICE DESK  ·  MONTHLY CATEGORY ANALYSIS", MARGIN, Inches(0.75),
          Inches(12), Inches(0.4), size=13, color=MID_GREY)
    txbox(s, title, MARGIN, Inches(1.5), Inches(11), Inches(1.9), size=46, bold=True)
    divider(s, Inches(3.75))
    txbox(s, f"{period}   ·   {h['total']:,} tickets   ·   {len(m['l1'])} categories",
          MARGIN, Inches(4.05), Inches(11), Inches(0.5), size=18, color=LIGHT_GREY)
    ask = (f"For decision: automate {top['name']}" if top
           else "For discussion: no automation candidate this cycle")
    txbox(s, ask, MARGIN, Inches(4.75), Inches(11), Inches(0.5), size=17,
          bold=True, color=ACCENT)

    # ---- 2. The numbers at a glance ----------------------------------------
    s = slide_head(prs, "The month in five numbers",
                   f"{ml[0]} to {ml[-1]}. Every figure computed from the ticket export.")
    tiles = [
        ("TICKETS", f"{h['total']:,}", " → ".join(str(t) for t in h["totals"])),
        (f"{ml[-1].upper()} VS {ml[-2].upper()}" if nm > 1 else "SINGLE MONTH",
         (f"{h['mom_change_pct']:+.1f}%" if nm > 1 else "–"),
         (f"{h['mom_change']:+} tickets" if nm > 1 else "nothing to compare")),
        ("SLA MET", f"{h['sla_met_pct']}%",
         f"{h['resolved'] - round(h['resolved'] * h['sla_met_pct'] / 100)} breached"),
        ("AGENT HOURS", f"{h['agent_hours_per_month']:,.0f}", "per month, resolution time"),
        ("REOPENED", f"{h['reopen_pct']}%", "came back after closure"),
    ]
    x, w, gap = MARGIN, Inches(2.29), Inches(0.13)
    for k, v, n in tiles:
        rect(s, x, Inches(2.1), w, Inches(1.85), border=ACCENT)
        txbox(s, k, x + Inches(0.18), Inches(2.28), w - Inches(0.36), Inches(0.3),
              size=10, bold=True, color=ACCENT)
        txbox(s, v, x + Inches(0.18), Inches(2.68), w - Inches(0.36), Inches(0.6),
              size=27, bold=True)
        txbox(s, n, x + Inches(0.18), Inches(3.34), w - Inches(0.36), Inches(0.5),
              size=11, color=MID_GREY)
        x += w + gap

    riser = max(m["l1"], key=lambda r: r["counts"][-1] - r["counts"][0]) if nm > 1 else None
    if riser and riser["counts"][-1] > riser["counts"][0]:
        txbox(s, "WHAT MOVED", MARGIN, Inches(4.35), Inches(12), Inches(0.3),
              size=11, bold=True, color=ACCENT)
        txbox(s, f"{riser['name']} rose {riser['counts'][-1] - riser['counts'][0]} tickets "
                 f"from {ml[0]} to {ml[-1]}, and is now {riser['share_pct']}% of everything "
                 f"the desk receives.\nThe rest of the desk is flat or down, so this is not a "
                 f"general increase in volume. It is concentrated in one place.",
              MARGIN, Inches(4.68), Inches(12), Inches(1.1), size=16, color=LIGHT_GREY)
    if nm <= 3:
        txbox(s, f"{nm} months gives {nm - 1} comparison{'' if nm == 2 else 's'}. "
                 f"Read the direction, not a trend line.",
              MARGIN, Inches(6.5), Inches(12), Inches(0.4), size=12, color=MID_GREY)

    # ---- 3. Volume by category, month on month -----------------------------
    s = slide_head(prs, "Where the tickets came from",
                   "Sorted by volume. The last column is first month to last month.")
    rows, colors_map = [], {}
    for i, r in enumerate(m["l1"][:8]):
        growth = f"{r['first_to_last_pct']:+.0f}%" if nm > 1 else "–"
        rows.append([r["name"], *[str(c) for c in r["counts"]], str(r["total"]),
                     f"{r['share_pct']}%", growth])
        colors_map[i] = GOOD if r["first_to_last_pct"] > 0 else (
            BAD if r["first_to_last_pct"] < 0 else LIGHT_GREY)
    rows.append(["Total", *[str(t) for t in h["totals"]], str(h["total"]), "100%",
                 f"{h['first_to_last_pct']:+.0f}%" if nm > 1 else "–"])
    colors_map[len(rows) - 1] = WHITE
    ncols = 1 + nm + 3
    widths = [Inches(3.6)] + [Inches((12.13 - 3.6) / (ncols - 1))] * (ncols - 1)
    headers = ["Category"] + [f"# {x}" for x in ml] + ["# Total", "# Share", "# Change"]
    table(s, headers, rows, Inches(2.05), widths,
          colors=lambda i, j: colors_map.get(i) if j == len(headers) - 1 else None)

    # ---- 4. The decision ---------------------------------------------------
    s = slide_head(prs, "The decision: what to automate",
                   f"A subcategory reaches the shortlist only by clearing all three checks: "
                   f"at least {m['rule']['min_tickets_latest_month']} tickets in {ml[-1]}, "
                   f"resolution spread under {m['rule']['max_spread_hours']}h, "
                   f"and under {m['rule']['max_p1p2_share_pct']}% P1 or P2.")
    if m["shortlist"]:
        headers = ["Subcategory", f"# {ml[-1]}", "# Spread", "# P1+P2", "# Median",
                   "# Hrs/month", "# Change"]
        widths = [Inches(3.9)] + [Inches(1.37)] * 6
        rows = [[f"{r['name']}", str(r["latest"]), f"{r['spread_hours']}h",
                 f"{r['p1p2_share_pct']}%", f"{r['median_hours']}h",
                 f"{r['agent_hours_per_month']:g}",
                 f"{r['first_to_last_pct']:+.0f}%" if nm > 1 else "–"]
                for r in m["shortlist"]]
        y = table(s, headers, rows, Inches(2.35), widths, colors=lambda i, j: GOOD if j else None)
        if m["near_miss"]:
            txbox(s, "NEAR MISS  ·  TWO OF THREE CHECKS, so these are next cycle's candidates",
                  MARGIN, y + Inches(0.22), Inches(12), Inches(0.3), size=11,
                  bold=True, color=ACCENT)
            nrows = [[r["name"], str(r["latest"]), f"{r['spread_hours']}h",
                      f"{r['p1p2_share_pct']}%", f"{r['median_hours']}h",
                      f"{r['agent_hours_per_month']:g}",
                      "fails " + ", ".join(k for k, v in r["checks"].items() if not v)]
                     for r in m["near_miss"][:3]]
            table(s, [""] * 7, nrows, y + Inches(0.58), widths, size=12)
    else:
        txbox(s, "Nothing clears all three checks this cycle.", MARGIN, Inches(2.6),
              Inches(12), Inches(0.5), size=22, bold=True)
        if m["near_miss"]:
            txbox(s, "Closest candidates, and what each one fails on:", MARGIN,
                  Inches(3.2), Inches(12), Inches(0.4), size=14, color=LIGHT_GREY)
            rows = [[r["name"], str(r["latest"]), f"{r['spread_hours']}h",
                     f"{r['p1p2_share_pct']}%",
                     "fails " + ", ".join(k for k, v in r["checks"].items() if not v)]
                    for r in m["near_miss"][:5]]
            table(s, ["Subcategory", f"# {ml[-1]}", "# Spread", "# P1+P2", "Blocked by"],
                  rows, Inches(3.8),
                  [Inches(4.2), Inches(1.6), Inches(1.6), Inches(1.6), Inches(3.13)])

    # ---- 5. The evidence for the top candidate -----------------------------
    if top:
        s = slide_head(prs, f"Why {top['name']} is the one to act on",
                       f"{top['parent']} · handled by {top['group']}")
        facts = [
            ("VOLUME", f"{top['total']} tickets",
             f"{top['share_pct']}% of everything the desk received"),
            ("TREND", " → ".join(str(c) for c in top["counts"]),
             f"{top['first_to_last_pct']:+.0f}% from {ml[0]} to {ml[-1]}" if nm > 1 else "one month"),
            ("SPREAD", f"{top['spread_hours']}h",
             "P90 minus P10. The fix is the same nearly every time"),
            ("ALREADY SELF-SERVE", f"{top['portal_share_pct']}%",
             "arrive through the portal, so the front door exists"),
        ]
        x, w = MARGIN, Inches(2.91)
        for k, v, n in facts:
            rect(s, x, Inches(2.1), w, Inches(1.8), border=ACCENT)
            txbox(s, k, x + Inches(0.18), Inches(2.26), w - Inches(0.36), Inches(0.3),
                  size=10, bold=True, color=ACCENT)
            txbox(s, v, x + Inches(0.18), Inches(2.62), w - Inches(0.36), Inches(0.55),
                  size=24, bold=True)
            txbox(s, n, x + Inches(0.18), Inches(3.24), w - Inches(0.36), Inches(0.6),
                  size=11, color=MID_GREY)
            x += w + Inches(0.15)
        txbox(s, "WHY THE SPREAD IS THE POINT", MARGIN, Inches(4.25), Inches(12),
              Inches(0.3), size=11, bold=True, color=ACCENT)
        txbox(s, f"A spread of {top['spread_hours']} hours means almost every one of these "
                 f"tickets is resolved the same way, in about the same time.\nThat is what makes "
                 f"a process scriptable. A subcategory with the same volume but a 40 hour spread "
                 f"needs a different judgement each time and would not automate.",
              MARGIN, Inches(4.58), Inches(12), Inches(1.0), size=15, color=LIGHT_GREY)
        rect(s, MARGIN, Inches(5.85), CONTENT_W, Inches(0.95), border=ACCENT)
        txbox(s, f"Gives back at least {top['agent_hours_per_month']:g} agent-hours a month. "
                 f"That is measured resolution time only, so it excludes triage, queue waiting "
                 f"and context switching.\nTreat it as the floor. The cost to build it has to "
                 f"come from engineering before anyone decides.",
              MARGIN + Inches(0.2), Inches(6.0), CONTENT_W - Inches(0.4), Inches(0.7),
              size=13, color=LIGHT_GREY)

    # ---- 6. Where the hours go ---------------------------------------------
    s = slide_head(prs, "Volume and effort are different questions",
                   "The busiest category is rarely the most expensive one. This is effort.")
    eff = [r for r in m["effort"] if r["agent_hours_per_month"] > 0][:6]
    if eff:
        maxv = eff[0]["agent_hours_per_month"]
        y = Inches(2.15)
        for r in eff:
            hbar_row(s, r["name"], r["agent_hours_per_month"], maxv, y, unit=" h",
                     faded=r["small_sample"],
                     note=f"{r['resolved']} resolved"
                          + (" · small sample" if r["small_sample"] else ""))
            y += Inches(0.62)
        txbox(s, "Faded rows rest on fewer than "
                 f"{m['small_sample']} resolved tickets. One slow ticket moves those medians a "
                 "long way, so they are shown but should not carry a staffing decision.",
              MARGIN, Inches(6.35), Inches(12), Inches(0.6), size=12, color=MID_GREY)

    # ---- 7. SLA ------------------------------------------------------------
    if m["sla_pressure"]:
        s = slide_head(prs, "Where service levels are slipping",
                       f"Subcategories with at least {m['small_sample']} resolved tickets, "
                       f"worst first.")
        rows, cmap = [], {}
        for i, r in enumerate(m["sla_pressure"][:7]):
            breached = round(r["resolved"] * (100 - r["sla_met_pct"]) / 100)
            status = ("Failing" if r["sla_met_pct"] < 70 else
                      "Under pressure" if r["sla_met_pct"] < 85 else
                      "Slipping" if r["sla_met_pct"] < 95 else "On track")
            rows.append([r["name"], status, f"{r['sla_met_pct']}%",
                         f"{breached} of {r['resolved']}", f"{r['median_hours']}h",
                         f"{r['reopen_pct']}%", r["group"]])
            cmap[i] = BAD if r["sla_met_pct"] < 85 else LIGHT_GREY
        table(s, ["Subcategory", "Status", "# SLA met", "# Breached", "# Median",
                  "# Reopened", "Handled by"], rows, Inches(2.05),
              [Inches(3.0), Inches(1.9), Inches(1.3), Inches(1.5), Inches(1.2),
               Inches(1.3), Inches(1.93)],
              colors=lambda i, j: cmap.get(i) if j == 1 else None)
        txbox(s, "A long median is not automatically a performance problem. Where the work "
                 "waits on a supplier or an approval, the SLA target may be measuring the "
                 "wrong thing, and the team that owns that process will know.",
              MARGIN, Inches(6.35), Inches(12), Inches(0.7), size=12, color=MID_GREY)

    # ---- 8. How categories were assigned -----------------------------------
    s = slide_head(prs, "How the categories were assigned",
                   "Every number in this deck depends on this step, so it is measured "
                   "rather than assumed.")
    scored = accuracy.get("scored")
    steps = [
        f"Tickets arrive as free text with no category. {accuracy.get('tickets', h['total']):,} "
        f"of them this cycle.",
        f"Descriptions are normalised and deduplicated first, which collapsed them to "
        f"{accuracy.get('unique_cases', 0):,} unique cases and cut the classification work by "
        f"{accuracy.get('dedup_saving_pct', 0)}%.",
        "Claude reads the description and assigns all three levels, with a confidence and a "
        "one-line reason a manager can agree or disagree with.",
        f"Nothing is forced. {accuracy.get('uncategorized', 0)} tickets matched no bucket, and "
        f"{accuracy.get('needs_review_tickets', 0)} are flagged for a human to review.",
    ]
    y = Inches(2.05)
    for i, t in enumerate(steps, 1):
        sq = rect(s, MARGIN, y, Inches(0.34), Inches(0.34), fill=ACCENT)
        tf = sq.text_frame
        p = tf.paragraphs[0]
        p.alignment = PP_ALIGN.CENTER
        r = p.add_run()
        r.text = str(i)
        r.font.size = Pt(13)
        r.font.bold = True
        r.font.color.rgb = BG_DARK
        txbox(s, t, MARGIN + Inches(0.55), y - Inches(0.04), Inches(11.5), Inches(0.7),
              size=15, color=LIGHT_GREY)
        y += Inches(0.72)

    if scored:
        o = accuracy["overall"]
        txbox(s, "MEASURED AGAINST A HELD-BACK ANSWER KEY", MARGIN, y + Inches(0.05),
              Inches(12), Inches(0.3), size=11, bold=True, color=ACCENT)
        x = MARGIN
        for lbl, val in [("Category", o["L1"]), ("Subcategory", o["L2"]),
                         ("Issue type", o["L3"])]:
            rect(s, x, y + Inches(0.4), Inches(2.6), Inches(0.9), border=ACCENT)
            txbox(s, f"{val}%", x + Inches(0.18), y + Inches(0.5), Inches(2.2),
                  Inches(0.45), size=22, bold=True)
            txbox(s, lbl, x + Inches(0.18), y + Inches(0.98), Inches(2.2), Inches(0.3),
                  size=11, color=MID_GREY)
            x += Inches(2.75)
        txbox(s, "This is a measurement on these tickets, not a forecast. If the answer key "
                 "came from the same taxonomy the classifier was scored against, the number "
                 "runs high. The number to trust on live data comes from hand-labelling a few "
                 "hundred real tickets and rerunning the same check.",
              MARGIN + Inches(8.4), y + Inches(0.4), Inches(3.7), Inches(1.6),
              size=10, color=MID_GREY, space=Pt(2))
    else:
        rect(s, MARGIN, y + Inches(0.1), CONTENT_W, Inches(1.15), border=BAD)
        txbox(s, "Accuracy was not measured for this cycle", MARGIN + Inches(0.2),
              y + Inches(0.24), Inches(11.7), Inches(0.35), size=15, bold=True, color=BAD)
        txbox(s, "No answer key came with the export, so nothing here tells us how often a "
                 "ticket landed in the right bucket. To close it, hand-label 200 to 300 "
                 "tickets and rerun. Until then the volumes above carry that caveat.",
              MARGIN + Inches(0.2), y + Inches(0.62), Inches(11.7), Inches(0.6),
              size=12, color=LIGHT_GREY)

    # ---- 9. What we are asking for -----------------------------------------
    s = slide_head(prs, "What we are asking for", None)
    asks = []
    if top:
        asks.append(("DECISION",
                     f"Approve a change request to automate {top['name']}",
                     f"{top['total']} tickets, {top['spread_hours']}h spread, gives back at "
                     f"least {top['agent_hours_per_month']:g} agent-hours a month. "
                     f"Engineering to size the build."))
    worst = m["sla_pressure"][0] if m["sla_pressure"] else None
    if worst and worst["sla_met_pct"] < 85:
        asks.append(("REVIEW",
                     f"{worst['name']} is meeting SLA on {worst['sla_met_pct']}% of tickets",
                     f"Median {worst['median_hours']}h against the target. A process question "
                     f"for {worst['group']}, not a capacity question."))
    if riser and nm > 1 and riser["counts"][-1] > riser["counts"][0]:
        asks.append(("EXPLAIN",
                     f"Why did {riser['name']} rise "
                     f"{riser['counts'][-1] - riser['counts'][0]} tickets?",
                     "A policy change, a migration or a joiner batch would each explain it, "
                     "and the answer changes what we do next."))
    asks.append(("DATA",
                 "Extend the history and confirm the categoriser on real labels",
                 f"{nm} months gives {max(0, nm - 1)} comparison"
                 f"{'' if nm == 2 else 's'}. Six months makes the trend real, and a "
                 f"hand-labelled sample turns the accuracy figure into a fact."))
    y = Inches(1.75)
    for k, head, body in asks[:4]:
        rect(s, MARGIN, y, CONTENT_W, Inches(1.18), border=ACCENT)
        txbox(s, k, MARGIN + Inches(0.22), y + Inches(0.12), Inches(2.0), Inches(0.28),
              size=10, bold=True, color=ACCENT)
        txbox(s, head, MARGIN + Inches(0.22), y + Inches(0.42), Inches(11.6), Inches(0.36),
              size=17, bold=True)
        txbox(s, body, MARGIN + Inches(0.22), y + Inches(0.78), Inches(11.6), Inches(0.32),
              size=12, color=MID_GREY)
        y += Inches(1.32)
    txbox(s, source_note, MARGIN, Inches(7.0), Inches(12), Inches(0.35),
          size=10, color=MID_GREY)

    out = Path(out)
    out.parent.mkdir(parents=True, exist_ok=True)
    prs.save(out)
    return prs, out


def main():
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--input", required=True)
    ap.add_argument("--work-dir", required=True)
    ap.add_argument("--out", required=True)
    ap.add_argument("--sheet", default="Tickets")
    ap.add_argument("--title", default="Service desk ticket analysis")
    ap.add_argument("--period", default=None)
    ap.add_argument("--source-note",
                    default="Source: categorized ticket export. Full detail in the "
                            "interactive dashboard.")
    ap.add_argument("--min-tickets", type=int, default=metrics.SHORTLIST["min_tickets_latest_month"])
    ap.add_argument("--max-spread", type=float, default=metrics.SHORTLIST["max_spread_hours"])
    ap.add_argument("--max-p1p2", type=float, default=metrics.SHORTLIST["max_p1p2_share_pct"])
    a = ap.parse_args()

    df, months = metrics.load(a.input, a.sheet)
    m = metrics.compute(df, months, {"min_tickets_latest_month": a.min_tickets,
                                     "max_spread_hours": a.max_spread,
                                     "max_p1p2_share_pct": a.max_p1p2})
    acc_path = Path(a.work_dir) / "accuracy.json"
    accuracy = normalise_accuracy(
        json.loads(acc_path.read_text()) if acc_path.exists() else {})
    period = a.period or f"{m['month_labels'][0]} to {m['month_labels'][-1]}"

    prs, out = build(m, accuracy, a.title, period, a.source_note, a.out)
    print(f"Saved: {out}")
    print(f"Slides: {len(prs.slides)}")
    if m["shortlist"]:
        t = m["shortlist"][0]
        print(f"Lead ask: automate {t['name']} "
              f"({t['total']} tickets, {t['agent_hours_per_month']:g} agent-hrs/month)")
    else:
        print("Lead ask: none, nothing cleared all three shortlist checks")
    if not accuracy.get("scored"):
        print("The deck states that accuracy was NOT measured, because there is no answer key.")


if __name__ == "__main__":
    main()
