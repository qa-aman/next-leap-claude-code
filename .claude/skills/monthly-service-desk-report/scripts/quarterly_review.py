"""Build the period review page: what last report asked for, what happened, and what to do next.

The dashboard answers "what is in this export". This page answers the question leadership asks
next: "did last time's calls work, and what do we decide now". It applies eight frameworks Aman
agreed on 17-10-2026 (logged as F-004 in references/feedback.md):

  1. Pyramid Principle / BLUF   verdict and three decisions first
  2. After Action Review        last report's calls vs this period, one result each
  3. Outcome chain              Kirkpatrick adapted: was a fix used, did volume move, were hours freed
  4. Blameless postmortem       each risk: evidence, impact, likely cause, fix, owner
  5. Start / Stop / Continue    next period's list
  6. Backward design            outcomes with targets leadership sets, so the next review has a plan
  7. KCS + 8. Diataxis          top recurring issues as knowledge article candidates, typed

Every number comes from the sibling skill's metrics module, the same code behind the dashboard,
so the two pages cannot disagree. A cause read from ticket text is labelled "to confirm" until
the owner confirms it in the notes file.

    python3 quarterly_review.py --current OUT/servicenow-tickets-categorized.xlsx \
        --previous PREV_OUT/servicenow-tickets-categorized.xlsx \
        --out OUT/service-desk-review.html [--notes notes.json] [--sample-data] [--show-frameworks]

notes.json (optional, written after owners reply):
    {"causes": {"VPN": "confirmed cause"}, "fixes": {"VPN": "agreed fix"},
     "targets": {"Laptop": "75%", "Overall": "85%"}}

Exit 0 = page written and gate passed. Exit 1 = fix the listed defects first.
"""
import argparse
import html
import json
import re
import sys
from collections import Counter
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "ticket-category-analysis" / "scripts"))
from metrics import L2, L3, SMALL_SAMPLE, compute, label_month, load, pct  # noqa: E402

E = html.escape
TYPOS = {"teh": "the", "adn": "and", "nto": "not", "agian": "again", "workign": "working",
         "mornign": "morning", "sytem": "system", "acces": "access", "cannt": "cannot", "plz": "please"}
TIME_WORDS = re.compile(r"\b(yesterday|morning|evening|today|week|month|holiday|\d+ ?am|\d+ ?pm|monday|"
                        r"tuesday|wednesday|thursday|friday|weekend)\b")
GREETING = re.compile(r"^(hi team|hi|hello|good morning|team|raising this again|second time reporting this)[,.: ]+")
POLITE = re.compile(r"[ ,.]*(thanks in advance|please help|need this today|kindly look into it urgently|"
                    r"appreciate a quick fix|this is blocking my work|let me know if you need anything "
                    r"from my side)$")
CLOSE_NOTES = ("close notes", "resolution notes", "work notes", "resolution")
WAIT_REASON = ("wait reason", "on hold reason", "pending reason", "hold reason")


def clean(text):
    t = " ".join(TYPOS.get(w, w) for w in str(text).lower().split())
    for _ in range(3):
        t = GREETING.sub("", t).strip()
        t = POLITE.sub("", t).strip()
    return t


def short_period(months):
    a, b = label_month(months[0]), label_month(months[-1])
    return f"{a[:3]}-{b}" if a[-4:] == b[-4:] else f"{a} to {b}"


def sla_counts(rows):
    r = rows[rows["Resolution Hours"].notna()]
    return int((r["SLA Met"] == "Yes").sum()), int(len(r))


class Period:
    def __init__(self, path):
        self.df, self.months = load(path)
        self.m = compute(self.df, self.months)
        self.res = self.df[self.df["Resolution Hours"].notna()]
        self.label = short_period(self.months)
        self.sla_ok, self.sla_n = sla_counts(self.df)
        self.sla_pct = pct(self.sla_ok, self.sla_n)
        self.l2 = {r["name"]: r for r in self.m["l2"]}
        self.p1 = self.df[self.df["Priority"].astype(str).str.upper().str.startswith("P1")]

    def sub(self, name):
        return self.df[self.df[L2] == name]

    def sub_sla(self, name):
        return sla_counts(self.sub(name))

    def urgent_by_month(self, name):
        g = self.sub(name)
        hi = g["Priority"].astype(str).str.upper().str.startswith(("P1", "P2"))
        return [int(((g["Month"] == m) & hi).sum()) for m in self.months]

    def portal_by_month(self, name):
        g = self.sub(name)
        portal = g["Channel"].astype(str).str.lower().str.contains("portal|self", regex=True, na=False)
        return [pct(int(((g["Month"] == m) & portal).sum()), int((g["Month"] == m).sum()))
                for m in self.months]

    def hours(self, name):
        return int(round(self.hours_raw(name)))

    def hours_raw(self, name):
        return float(self.res[self.res[L2] == name]["Resolution Hours"].sum())

    def pointers(self):
        """The dashboard's four summary pointers, by the same rules (see renderSummary and F-003)."""
        g = [r for r in self.m["l2"] if r["resolved"] >= SMALL_SAMPLE]
        effort = sorted(g, key=lambda r: -self.hours(r["name"]))[:2]
        p1ok, p1n = sla_counts(self.p1)
        if p1n and pct(p1ok, p1n) < self.sla_pct:
            risk = {"kind": "p1", "name": "P1", "ok": p1ok, "n": p1n}
        else:
            rest = sorted([r for r in g if r["name"] not in {e["name"] for e in effort}],
                          key=lambda r: r["sla_met_pct"])
            ok, n = self.sub_sla(rest[0]["name"]) if rest else (0, 0)
            risk = {"kind": "sub", "name": rest[0]["name"], "ok": ok, "n": n} if rest else None
        dec = self.m["shortlist"][0]["name"] if self.m["shortlist"] else None
        return {"risk": risk, "effort": [e["name"] for e in effort], "decision": dec}

    def mover(self, exclude=()):
        """The subcategory whose latest month rose most, when the rise is large enough to matter."""
        if len(self.months) < 2:
            return None
        best = None
        for r in self.m["l2"]:
            c = r["counts"]
            d = c[-1] - c[-2]
            if r["name"] in exclude or d < max(5, 0.5 * c[-2]):
                continue
            if not best or d > best[1]:
                best = (r["name"], d)
        return best[0] if best else None

    def phrase(self, name):
        """A 'since <change>' phrase repeated in the ticket text: a lead, not a finding."""
        g = self.sub(name)
        hits = Counter()
        first = {}
        for _, r in g.iterrows():
            t = clean(r["Description"])
            for m in re.finditer(r"since (?:the |a |an )?((?:[a-z]+ ){0,3}[a-z]+)", t):
                p = m.group(0)
                if TIME_WORDS.search(p):
                    continue
                hits[p] += 1
                first.setdefault(p, r["Month"])
                first[p] = min(first[p], r["Month"])
        if not hits:
            return None
        p, n = hits.most_common(1)[0]
        return {"text": p, "n": n, "first": label_month(first[p])} if n >= 3 else None

    def weak_issue(self, name):
        g = self.res[self.res[L2] == name]
        overall = pct(int((g["SLA Met"] == "Yes").sum()), len(g))
        worst = None
        for l3, x in g.groupby(L3):
            if len(x) < 5:
                continue
            p = pct(int((x["SLA Met"] == "Yes").sum()), len(x))
            if p <= overall - 10 and (not worst or p < worst[1]):
                worst = (l3, p, int((x["SLA Met"] == "Yes").sum()), len(x),
                         round(float(x["Resolution Hours"].median()), 1))
        return worst

    def has_column(self, names):
        cols = [c.lower() for c in self.df.columns]
        return any(n in cols for n in names)


def chip(cls, text):
    return f'<span class="chip {cls}">{E(text)}</span>'


def trend(counts):
    return " → ".join(str(c) for c in counts)


def build(cur, prev, notes, sample, show_fw):
    causes, fixes, targets = notes.get("causes", {}), notes.get("fixes", {}), notes.get("targets", {})
    calls, gaps = [], []

    # ---- 2. After Action Review: last report's calls, scored against this period
    if prev:
        pp = prev.pointers()
        r = pp["risk"]
        if r and r["kind"] == "p1":
            ok, n = sla_counts(cur.p1)
            now = pct(ok, n)
            st = ("ok", "Fixed") if n and now >= cur.sla_pct else \
                 ("warn", "Better") if now > pct(r["ok"], r["n"]) else ("crit", "Worse")
            calls.append({"call": "Risk: urgent P1 tickets miss SLA", "sub": None,
                          "was": f"{r['ok']} of {r['n']} met", "now": f"{ok} of {n} met", "st": st})
        elif r:
            calls.append({"call": f"Risk: {r['name']} misses SLA most", "sub": r["name"]})
        for e in pp["effort"]:
            calls.append({"call": f"Effort: {e} takes the most agent hours", "sub": e})
        for c in calls:
            if c.get("sub") and "st" not in c:
                ok0, n0 = prev.sub_sla(c["sub"])
                ok1, n1 = cur.sub_sla(c["sub"])
                p0, p1 = pct(ok0, n0), pct(ok1, n1)
                c["was"] = f"{ok0} of {n0} met ({p0}%)"
                c["now"] = f"{ok1} of {n1} met ({p1}%)" if n1 else "no tickets"
                c["p_now"] = p1
                if n1 and p1 >= cur.sla_pct:
                    c["st"] = ("ok", "Fixed")
                elif p1 >= p0 + 5:
                    c["st"] = ("warn", "Better, still below 70%") if p1 < 70 else ("warn", "Better")
                elif p1 <= p0 - 5:
                    c["st"] = ("crit", "Worse")
                else:
                    c["st"] = ("warn", "No change")
        dec = pp["decision"]
        if dec:
            c0 = prev.l2[dec]["counts"]
            c1 = cur.l2[dec]["counts"] if dec in cur.l2 else [0] * len(cur.months)
            st = ("ok", "Falling") if c1[-1] < c1[0] * 0.8 else \
                 ("crit", "Rising") if c1[-1] > c1[0] * 1.2 else ("warn", "Flat")
            calls.append({"call": f"Decision: automate {dec} tickets first", "sub": dec, "decision": True,
                          "was": f"{trend(c0)} a month", "now": f"{trend(c1)} a month", "st": st})
    seen = {c.get("sub") for c in calls}
    mover = cur.mover(exclude=() if not prev else ())
    if mover and prev and mover not in seen:
        calls.append({"call": f"Not foreseen: {mover}", "sub": mover,
                      "was": f"{trend(prev.l2[mover]['counts']) if mover in prev.l2 else '0'} a month",
                      "now": f"{trend(cur.l2[mover]['counts'])} a month", "st": ("crit", "New risk")})

    # ---- 4. Postmortem items: the mover, then last calls still failing, then this period's risks
    items = []
    if mover:
        items.append(mover)
    for c in sorted([c for c in calls if c.get("sub") and not c.get("decision") and c.get("p_now", 100) < 70],
                    key=lambda c: c.get("p_now", 100)):
        if c["sub"] not in items:
            items.append(c["sub"])
    cp = cur.pointers()
    p1ok, p1n = sla_counts(cur.p1)
    if cp["risk"] and cp["risk"]["kind"] == "p1":
        items.append("P1")
    for s in cp["effort"] + ([cp["risk"]["name"]] if cp["risk"] and cp["risk"]["kind"] == "sub" else []):
        if s not in items and cur.l2[s]["sla_met_pct"] < cur.sla_pct:
            items.append(s)
    items = items[:3]

    post = []
    for s in items:
        if s == "P1":
            post.append({"name": "P1", "title": "Urgent P1 tickets",
                         "evidence": f"{p1ok} of {p1n} P1 tickets met SLA, against {cur.sla_pct}% overall",
                         "impact": "The most urgent work waits longest",
                         "cause": causes.get("P1", "Not visible in the export"),
                         "confirmed": "P1" in causes, "fix": fixes.get("P1", "Review P1 breaches one by one with the service owner"),
                         "owner": "Service desk lead", "phrase": None})
            continue
        r = cur.l2[s]
        ok, n = cur.sub_sla(s)
        urg = cur.urgent_by_month(s)
        ph = cur.phrase(s)
        weak = cur.weak_issue(s)
        ev = f"{trend(r['counts'])} tickets a month. {ok} of {n} met SLA, median {round(r['median_hours'], 1)} hours"
        if s == mover and urg[-1] > urg[0]:
            ev = f"{trend(r['counts'])} tickets a month. P1 and P2 went {trend(urg)}"
        hrs = cur.hours(s)
        imp = f"{hrs} agent hours this period" + (f" vs {prev.hours(s)} last period" if prev and s in prev.l2 else "")
        if s == mover:
            imp = f"{r['counts'][-1]} tickets in {label_month(cur.months[-1])[:3]}, {urg[-1]} of them urgent. " + imp
        group_ok, group_n = sla_counts(cur.df[cur.df["Assignment Group"] == r["group"]])
        if not ph and not weak:
            imp += f". {r['group']} meets SLA on {pct(group_ok, group_n)}% of its tickets"
        if s in causes:
            cause, confirmed = causes[s], True
        elif ph:
            cause, confirmed = f'{ph["n"]} tickets say "{ph["text"]}", first seen in {ph["first"][:3]}', False
        elif weak:
            cause, confirmed = (f"The gap is in {weak[0]}: {weak[2]} of {weak[3]} met SLA, median "
                                f"{weak[4]} hours"), False
        else:
            cause, confirmed = "Not visible in the export. It has no field for why a ticket waited", False
            if not cur.has_column(WAIT_REASON):
                gaps.append("wait")
        fix = fixes.get(s) or (
            f'Check what changed "{ph["text"]}" and publish a known-error article' if ph else
            f"Review how {weak[0].lower()} tickets are handled, with the service owner" if weak else
            "Add a wait-reason field to the export, then split breaches by reason")
        post.append({"name": s, "title": s, "evidence": ev, "impact": imp, "cause": cause,
                     "confirmed": confirmed, "fix": fix, "owner": r["group"], "phrase": ph,
                     "sla_now": pct(ok, n), "weak": weak})

    # ---- 3. Outcome chain for last period's Decision
    chain = None
    dec_call = next((c for c in calls if c.get("decision")), None)
    if dec_call and dec_call["sub"] in cur.l2:
        d = dec_call["sub"]
        por0, por1 = prev.portal_by_month(d), cur.portal_by_month(d)
        # Same rounding as the dashboard (divide the raw hours, round once), so the two pages agree.
        r0, r1 = prev.hours_raw(d) / len(prev.months), cur.hours_raw(d) / len(cur.months)
        h0, h1 = round(r0, 1), round(r1, 1)
        top = sorted(cur.m["l2"], key=lambda r: -cur.hours(r["name"]))[:4]
        chain = {"name": d, "por": (por0[-1], por1[-1]), "vol": (prev.l2[d]["counts"][-1], cur.l2[d]["counts"][-1]),
                 "vol_months": (label_month(prev.months[-1])[:3], label_month(cur.months[-1])[:3]),
                 "hpm": (h0, h1), "freed": round(h0 - h1, 1), "top": [(t["name"], cur.hours(t["name"])) for t in top],
                 "own": cur.hours(d), "median": round(cur.l2[d]["median_hours"], 1)}

    # ---- 1. BLUF
    good = [c for c in calls if c["st"][0] == "ok"]
    worse = [c for c in calls if c["st"][1] == "Worse"]
    names = lambda cs: " and ".join(c["sub"] or "P1 SLA" for c in cs)
    if prev:
        verdict = (f"{len(good)} of last period's {len([c for c in calls if not c['call'].startswith('Not foreseen')])} "
                   f"calls moved the right way: {names(good) if good else 'none'}. ")
        if worse:
            verdict += f"{names(worse)} got worse"
        if mover:
            verdict += (", and " if worse else "") + f"a {label_month(cur.months[-1])[:3]} rise in {mover} tickets is the new risk"
        verdict = verdict.rstrip() + "."
    else:
        verdict = "First review on record. The decisions below set the baseline the next review checks."

    stop = None
    if chain and chain["vol"][1] < chain["vol"][0] and chain["freed"] < 10:
        stop = (f"Leading automation with {chain['name']}. It already fell and frees "
                f"{chain['freed']} hours a month")
    decisions = [f"<strong>{E(p['title'])}:</strong> {E(p['owner'])} to {E(p['fix'][0].lower() + p['fix'][1:])}."
                 for p in post[:2]]
    if stop and chain:
        decisions.append(f"<strong>Automation:</strong> pause the {E(chain['name'])} automation build. Volume already "
                         f"fell from {chain['vol'][0]} in {chain['vol_months'][0]} to {chain['vol'][1]} in {chain['vol_months'][1]}, and the bigger agent hours sit in "
                         f"{E(', '.join(n for n, _ in chain['top'][:2]) + ' and ' + chain['top'][2][0])}.")
    elif len(post) > 2:
        p = post[2]
        decisions.append(f"<strong>{E(p['title'])}:</strong> {E(p['owner'])} to {E(p['fix'][0].lower() + p['fix'][1:])}.")

    # ---- 7. KCS candidates
    l3 = cur.df.groupby([L2, L3])
    top_issues = sorted(l3, key=lambda kv: -len(kv[1]))[:6]
    ph_subs = {p["name"] for p in post if p.get("phrase")}
    kcs_rows, article = [], None
    for (s, i), g in top_issues:
        rg = g[g["Resolution Hours"].notna()]
        known = s in ph_subs
        kcs_rows.append({"issue": i, "n": len(g), "portal": cur.portal_by_month(s) and pct(int(g["Channel"].astype(str)
                         .str.lower().str.contains("portal|self", regex=True, na=False).sum()), len(g)),
                         "median": round(float(rg["Resolution Hours"].median()), 1) if len(rg) else 0,
                         "type": "Known error" if known else "How-to", "group": g["Assignment Group"].mode().iat[0]})
        if not article and (known or i == top_issues[0][0][1]):
            words = Counter(clean(d) for d in g["Description"])
            p = next((x for x in post if x["name"] == s), None)
            article = {"issue": i, "said": words.most_common(1)[0][0], "known": known, "n": len(g),
                       "last": int((g["Month"] == cur.months[-1]).sum()), "group": g["Assignment Group"].mode().iat[0],
                       "env": (f'Some tickets from {p["phrase"]["first"][:3]} onward say "{p["phrase"]["text"]}"'
                               if p and p.get("phrase") else "Not stated in the tickets"),
                       "cause": "Under investigation (see the risks above)" if known else "Not stated in the tickets"}
    if not cur.has_column(CLOSE_NOTES):
        gaps.append("close")

    return {"calls": calls, "post": post, "chain": chain, "verdict": verdict, "decisions": decisions,
            "stop": stop, "kcs": kcs_rows, "article": article, "gaps": sorted(set(gaps)), "mover": mover,
            "targets": targets}


CSS = Path(__file__).resolve().parents[1] / "assets" / "review_style.css"


def render(cur, prev, r, sample, show_fw):
    fw = lambda t: f'<span class="fw">{E(t)}</span>' if show_fw else ""
    note = lambda t: f'<p class="note">{E(t)}</p>' if show_fw else ""
    h = cur.m["headline"]
    out = [f"<title>Service Desk Review {E(cur.label)}</title>",
           '<meta name="claude:viewport-fit-sides" content="cover">',
           '<link rel="preconnect" href="https://fonts.googleapis.com">',
           '<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=IBM+Plex+Sans+Condensed:wght@500;600;700'
           '&family=IBM+Plex+Sans:wght@400;500;600&family=IBM+Plex+Mono:wght@400;500&display=swap">',
           f"<style>\n{CSS.read_text()}</style>", '<div class="wrap">', "<header>",
           '<div class="eyebrow">Service desk review · ticket export</div>',
           f"<h1>Service desk review: {E(label_month(cur.months[0]))} to {E(label_month(cur.months[-1]))}</h1>",
           f'<div class="meta"><span>{h["total"]} tickets</span>' +
           (f"<span>Compared with {E(label_month(prev.months[0]))} to {E(label_month(prev.months[-1]))} "
            f"({prev.m['headline']['total']} tickets)</span>" if prev else "") + "</div>"]
    if sample:
        out.append('<p class="sample"><strong>Sample data.</strong> These are generated test tickets used to design '
                   "this report. The numbers show how the review works. They are not real service desk results.</p>")
    out.append("</header>")

    # 1. Bottom line
    out.append(f'<section><div class="head"><h2>1. Bottom line</h2>{fw("BLUF · Minto")}</div>'
               f'<div class="panel bluf"><p class="verdict">{E(r["verdict"])}</p>'
               f'<h3>Decisions for this period</h3><ol>{"".join(f"<li>{d}</li>" for d in r["decisions"])}</ol></div>')
    ph = prev.m["headline"] if prev else None
    kp = [("Tickets", f'{h["total"]:,}', f'{ph["total"]:,} last period, {"+" if h["total"] >= ph["total"] else ""}'
           f'{pct(h["total"] - ph["total"], ph["total"])}%' if ph else ""),
          ("SLA met", f'{h["sla_met_pct"]}%', f'{ph["sla_met_pct"]}% last period' if ph else ""),
          ("Agent hours", f'{round(h["agent_hours"]):,}', f'{round(ph["agent_hours"]):,} last period' if ph else ""),
          ("Reopened", f'{h["reopen_pct"]}%', f'{ph["reopen_pct"]}% last period' if ph else "")]
    out.append('<div class="kpis">' + "".join(f'<div class="kpi"><span>{k}</span><b>{v}</b><small>{E(s)}</small></div>'
                                              for k, v, s in kp) + "</div></section>")

    # 2. AAR
    out.append(f'<section><div class="head"><h2>2. What last report asked for, and what happened</h2>'
               f'{fw("After Action Review")}</div>')
    if r["calls"]:
        out.append('<div class="tbl"><table><thead><tr><th>Last report\'s call</th>'
                   f'<th>{E(prev.label)}</th><th>{E(cur.label)}</th><th>Result</th></tr></thead><tbody>')
        for c in r["calls"]:
            head, _, rest = c["call"].partition(": ")
            out.append(f'<tr><td><strong>{E(head)}:</strong> {E(rest)}</td><td class="n">{E(c["was"])}</td>'
                       f'<td class="n">{E(c["now"])}</td><td>{chip(*c["st"])}</td></tr>')
        out.append("</tbody></table></div>")
        good = [c for c in r["calls"] if c["st"][0] == "ok"]
        bad = [c for c in r["calls"] if c["st"][0] == "crit"]
        out.append('<div class="quad">'
                   f'<div class="panel"><div class="q">What was supposed to happen</div><p>The last report asked to act on '
                   f'{E(", ".join(c["sub"] or "P1 SLA" for c in r["calls"] if not c["call"].startswith("Not foreseen")))}.</p></div>'
                   f'<div class="panel"><div class="q">What happened</div><p>Moved the right way: '
                   f'{E(", ".join(c["sub"] or "P1 SLA" for c in good) or "none")}. Needs attention: '
                   f'{E(", ".join(c["sub"] or "P1 SLA" for c in bad) or "none")}.</p></div>'
                   '<div class="panel"><div class="q">Why it was different</div><p>The export shows what changed, not why. '
                   "Each result needs its owner to confirm the cause before the next review.</p></div>"
                   '<div class="panel"><div class="q">What to do next period</div><p>Keep what worked, move the focus to the '
                   "risks below, and set targets now so the next review has numbers to check against.</p></div></div>")
    else:
        out.append("<p>No earlier review to compare against. This review sets the baseline that the next one checks.</p>")
    out.append(note("Each period opens with the last report's calls and a result for each. A cause read from the data stays a hypothesis until the owner confirms it.") + "</section>")

    # 3. Outcome chain
    ch = r["chain"]
    if ch:
        out.append(f'<section><div class="head"><h2>3. Did the {E(ch["name"])} change pay off?</h2>'
                   f'{fw("Outcome chain · adapted from Kirkpatrick")}</div><div class="chain">'
                   f'<div class="step"><span class="n">1 · Used</span><b>{ch["por"][1]}%</b><p>{E(ch["name"])} tickets arriving '
                   f'through the portal in {E(label_month(cur.months[-1])[:3])}, against {ch["por"][0]}% in '
                   f'{E(label_month(prev.months[-1])[:3])}.</p></div>'
                   f'<div class="step"><span class="n">2 · Volume moved</span><b>{ch["vol"][0]} → {ch["vol"][1]}</b>'
                   f'<p>{E(ch["name"])} tickets a month, {E(label_month(prev.months[-1])[:3])} to '
                   f'{E(label_month(cur.months[-1])[:3])}.</p></div>'
                   f'<div class="step"><span class="n">3 · Hours freed</span><b>{ch["freed"]} h</b><p>A month. '
                   f'{E(ch["name"])} used {ch["hpm"][0]} agent hours a month last period and {ch["hpm"][1]} this period.</p></div>'
                   '<div class="step"><span class="n">4 · Business result</span><span class="chip na">Not in the export</span>'
                   "<p>Needs cost per agent hour or user downtime, which the export does not carry.</p></div></div>"
                   f'<p>Each {E(ch["name"])} ticket takes about {ch["median"]} hours. This period '
                   + E(", ".join(f"{n} used {hh}" for n, hh in ch["top"][:4]))
                   + f' agent hours, against {ch["own"]} for {E(ch["name"])}.</p>'
                   + note("Every past Decision gets this 4-step chain the following period, so a fix is judged on hours freed, not only on volume.")
                   + "</section>")

    # 4. Risks
    n = 4 if ch else 3
    out.append(f'<section><div class="head"><h2>{n}. The risks</h2>{fw("Blameless postmortem")}</div>'
               '<div class="tbl"><table><thead><tr><th>Risk and evidence</th><th>Impact</th><th>Likely cause</th>'
               "<th>Fix to trial</th><th>Owner</th></tr></thead><tbody>")
    for p in r["post"]:
        tag = "" if p["confirmed"] else ' <span class="chip warn">To confirm</span>'
        out.append(f'<tr><td><strong>{E(p["title"])}.</strong> {E(p["evidence"])}</td><td>{E(p["impact"])}</td>'
                   f'<td>{E(p["cause"])}{tag}</td><td>{E(p["fix"])}</td><td>{E(p["owner"])}</td></tr>')
    out.append("</tbody></table></div>" + note("Blameless: a cause is written as a missing step, field or check, never as a team's failure.") + "</section>")

    # 5. Start / Stop / Continue
    n += 1
    start = [p["fix"] for p in r["post"]]
    if "close" in r["gaps"] or "wait" in r["gaps"]:
        start.append("Add " + " and ".join(x for x in (("close notes" if "close" in r["gaps"] else ""),
                                                       ("a wait reason" if "wait" in r["gaps"] else "")) if x) + " to the export")
    if not r["targets"]:
        start.append("Agreed targets for the next period")
    cont = [f"Whatever fixed {c['sub'] or 'P1 SLA'}" for c in r["calls"] if c["st"][1] == "Fixed"]
    if ch and ch["vol"][1] < ch["vol"][0] and ch["por"][1] >= 50:
        cont.append(f"Portal-first for {ch['name']}, now {ch['por'][1]}% of those tickets")
    li = lambda xs, empty: "".join(f"<li>{E(x)}</li>" for x in xs) or f"<li>{E(empty)}</li>"
    out.append(f'<section><div class="head"><h2>{n}. Next period</h2>{fw("Start / Stop / Continue")}</div><div class="ssc">'
               f'<div class="panel"><h3 class="s">Start</h3><ol>{li(start, "Nothing new")}</ol></div>'
               f'<div class="panel"><h3 class="t">Stop</h3><ol>{li([r["stop"]] if r["stop"] else [], "Nothing flagged this period")}</ol></div>'
               f'<div class="panel"><h3 class="c">Continue</h3><ol>{li(cont, "Nothing flagged this period")}</ol></div></div></section>')

    # 6. Targets
    n += 1
    out.append(f'<section><div class="head"><h2>{n}. Targets for next period</h2>{fw("Backward design · outcomes first")}</div>'
               "<p>Without agreed goals, the next review can say what changed but not whether it was enough. "
               "Proposed outcomes, with the target left for leadership:</p>"
               f'<div class="tbl"><table><thead><tr><th>Outcome</th><th class="n">{E(cur.label)}</th><th>Target</th>'
               "<th>Owner</th></tr></thead><tbody>")
    tset = lambda k, extra="": (f'<td>{E(r["targets"][k])}</td>' if k in r["targets"]
                                else f'<td class="blank">Leadership to set{E(extra)}</td>')
    for p in r["post"]:
        if p["name"] == "P1":
            out.append(f'<tr><td>P1 tickets meet SLA</td><td class="n">{p1_text(cur)}</td>{tset("P1")}<td>{E(p["owner"])}</td></tr>')
        elif p["name"] == r["mover"]:
            c = cur.l2[p["name"]]["counts"]
            out.append(f'<tr><td>{E(p["name"])} tickets a month back to the earlier level</td><td class="n">{c[-1]} in '
                       f'{E(label_month(cur.months[-1])[:3])}</td>{tset(p["name"], " (earlier months: " + ", ".join(map(str, c[:-1])) + ")")}'
                       f'<td>{E(p["owner"])}</td></tr>')
        elif p.get("weak"):
            w = p["weak"]
            out.append(f'<tr><td>{E(w[0])} tickets meet SLA</td><td class="n">{w[2]} of {w[3]}</td>{tset(p["name"])}'
                       f'<td>{E(p["owner"])}</td></tr>')
        else:
            out.append(f'<tr><td>{E(p["name"])} tickets meet SLA</td><td class="n">{p["sla_now"]}%</td>{tset(p["name"])}'
                       f'<td>{E(p["owner"])}</td></tr>')
    out.append(f'<tr><td>Overall SLA met</td><td class="n">{h["sla_met_pct"]}%</td>{tset("Overall")}<td>Service desk lead</td></tr>'
               "</tbody></table></div></section>")

    # 7. KCS
    n += 1
    out.append(f'<section class="kcs"><div class="head"><h2>{n}. Knowledge articles to write</h2>{fw("KCS + Diataxis")}</div>'
               "<p>The six most common issue types this period. Each repeats often enough that an article could let users "
               "fix it themselves, or tell them a fix is coming.</p>"
               '<div class="tbl"><table><thead><tr><th>Issue type</th><th class="n">Tickets</th><th class="n">Via portal</th>'
               '<th class="n">Median hrs</th><th>Article type</th><th>Writer</th></tr></thead><tbody>')
    for k in r["kcs"]:
        out.append(f'<tr><td>{E(k["issue"])}</td><td class="n">{k["n"]}</td><td class="n">{k["portal"]}%</td>'
                   f'<td class="n">{k["median"]}</td><td>{chip("crit" if k["type"] == "Known error" else "na", k["type"])}</td>'
                   f'<td>{E(k["group"])}</td></tr>')
    out.append("</tbody></table></div>")
    a = r["article"]
    if a:
        res = (f'To be written by {a["group"]}. The export has no close notes, so the steps cannot be taken from it'
               if "close" in r["gaps"] else f'To be written by {a["group"]} from the close notes')
        out.append(f'<article><h3>Sample article: {E(a["issue"])}</h3><dl>'
                   f'<dt>Issue</dt><dd>In the user\'s words: "{E(a["said"])}"</dd>'
                   f'<dt>Environment</dt><dd>{E(a["env"])}</dd>'
                   f'<dt>Resolution</dt><dd class="blank">{E(res)}</dd>'
                   f'<dt>Cause</dt><dd>{E(a["cause"])}</dd>'
                   f'<dt>Type</dt><dd>{chip("crit" if a["known"] else "na", "Known error" if a["known"] else "How-to")} '
                   f'{"Tells users a fix is in progress and what to do meanwhile" if a["known"] else "Steps a user can follow alone"}</dd>'
                   f'<dt>Volume</dt><dd>{a["n"]} tickets this period, {a["last"]} of them in {E(label_month(cur.months[-1])[:3])}</dd>'
                   "</dl></article>")
    out.append(note("Top issue types become article candidates every period. The resolution stays blank until the export carries close notes.") + "</section>")

    src = lambda p: E(f"{Path(p).parent.name}/{Path(p).name}")
    out.append(f'<footer><p>Source: <code>{src(cur.path)}</code>'
               + (f' and <code>{src(prev.path)}</code>' if prev else "")
               + ". Every figure is computed from the categorized exports with the same code as the dashboard.</p>"
               + ("<p>Sample data: generated tickets for designing and testing the report.</p>" if sample else "")
               + "</footer></div>")
    if show_fw:
        out.insert(out.index("</header>"), FW_MAP)
    return "\n".join(out) + "\n"


def p1_text(cur):
    ok, n = sla_counts(cur.p1)
    return f"{ok} of {n}"


FW_MAP = """<div class="bar"><p>Framework tags are on (--show-frameworks). Publish without the flag for leadership.</p></div>"""


def gate(page):
    text = re.sub(r"<style>.*?</style>", "", page, flags=re.S)
    problems = []
    if "—" in text or "–" in text:
        problems.append("em or en dash in page text")
    if re.search(r"\b\d{4}-\d{2}-\d{2}\b|\b\d{1,2}/\d{1,2}/\d{4}\b", text):
        problems.append("non DD-MM-YYYY date in page text")
    if re.search(r">\s*(nan|None|NaN)\s*<|\bnan%|None\b", text):
        problems.append("an empty value (nan or None) reached the page")
    for s in ("1. Bottom line", "Targets for next period", "Knowledge articles to write"):
        if s not in text:
            problems.append(f"section missing: {s}")
    return problems


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--current", required=True, help="this period's categorized workbook")
    ap.add_argument("--previous", help="last period's categorized workbook, from history.py show")
    ap.add_argument("--notes", help="owners' confirmed causes, agreed fixes and targets (JSON)")
    ap.add_argument("--out", required=True)
    ap.add_argument("--sample-data", action="store_true")
    ap.add_argument("--show-frameworks", action="store_true",
                    help="tag each section with its framework, for an internal review only")
    a = ap.parse_args()

    cur = Period(a.current)
    cur.path = a.current
    prev = None
    if a.previous:
        prev = Period(a.previous)
        prev.path = a.previous
    notes = json.loads(Path(a.notes).read_text()) if a.notes else {}
    r = build(cur, prev, notes, a.sample_data, a.show_frameworks)
    page = render(cur, prev, r, a.sample_data, a.show_frameworks)
    Path(a.out).write_text(page)
    # The weekly email reads this instead of parsing the page.
    h = cur.m["headline"]
    Path(a.out).with_suffix(".json").write_text(json.dumps({
        "period": f"{label_month(cur.months[0])} to {label_month(cur.months[-1])}",
        "short_period": cur.label, "sample_data": a.sample_data, "verdict": r["verdict"],
        "decisions": [re.sub(r"<[^>]+>", "", html.unescape(d)) for d in r["decisions"]],
        "kpis": {"tickets": h["total"], "sla_met_pct": h["sla_met_pct"],
                 "agent_hours": round(h["agent_hours"]), "reopen_pct": h["reopen_pct"]},
        "previous_kpis": ({"tickets": prev.m["headline"]["total"], "sla_met_pct": prev.m["headline"]["sla_met_pct"]}
                          if prev else None),
        "to_confirm": [p["title"] for p in r["post"] if not p["confirmed"]],
    }, indent=2))

    print(f"Wrote {a.out} ({len(page.encode()) // 1024} KB)")
    print(f"Verdict  : {r['verdict']}")
    for c in r["calls"]:
        print(f"AAR      : {c['call']} | {c['was']} -> {c['now']} | {c['st'][1]}")
    for p in r["post"]:
        print(f"Risk     : {p['title']} | cause {'confirmed' if p['confirmed'] else 'to confirm'}: {p['cause']} | owner {p['owner']}")
    if r["chain"]:
        ch = r["chain"]
        print(f"Chain    : {ch['name']} portal {ch['por'][0]}% -> {ch['por'][1]}%, volume {ch['vol'][0]} -> {ch['vol'][1]}, "
              f"hours/month {ch['hpm'][0]} -> {ch['hpm'][1]} (freed {ch['freed']})")
    print(f"Data gaps: {', '.join(r['gaps']) or 'none'}")
    problems = gate(page)
    if problems:
        print("NOT READY:")
        for p in problems:
            print("  -", p)
        sys.exit(1)
    print("Review gate passed.")


if __name__ == "__main__":
    main()
