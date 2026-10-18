"""Mechanical assertions for email-writer evals. Usage: python3 grade.py <iteration-dir>"""
import json, re, sys, pathlib

LIMITS = {"status-update-vp": 150, "ask-borrow-engineer": 120,
          "follow-up-ghosted-dana": 90, "difficult-say-no-sales": 200}
FILLER = ["hope this finds", "just checking in", "circling back", "just wanted to",
          "let me know your thoughts", "thanks in advance", "bumping this", "touching base"]
BAD_DATE = re.compile(r"\b\d{4}-\d{2}-\d{2}\b|\b\d{1,2}/\d{1,2}/\d{2,4}\b|"
                      r"\b(Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)[a-z]* \d{1,2}\b")
EMOJI = re.compile("[\U0001F300-\U0001FAFF☀-➿]")


def body_of(text):
    t = text.split("\n---", 1)[0]
    lines = [l for l in t.splitlines() if l.strip() and not l.lower().startswith("**subject")
             and not l.lower().startswith("subject:")]
    return "\n".join(lines)


def grade(name, text):
    body = body_of(text)
    words = len(re.findall(r"\b[\w'-]+\b", body))
    limit = int(LIMITS[name] * 1.3)
    hits = [f for f in FILLER if f in text.lower()]
    dates = [m.group(0) for m in BAD_DATE.finditer(body)]
    return [
        {"text": "Has a subject line", "passed": bool(re.search(r"subject:", text, re.I)),
         "evidence": text.splitlines()[0][:120] if text else "empty"},
        {"text": "No em dashes", "passed": "—" not in text,
         "evidence": f"{text.count(chr(0x2014))} em dashes"},
        {"text": "No emojis", "passed": not EMOJI.search(text), "evidence": "regex scan"},
        {"text": "No filler phrases (just checking in, hope this finds you, etc.)",
         "passed": not hits, "evidence": ", ".join(hits) or "none found"},
        {"text": f"Body within length target +30% ({limit} words)", "passed": words <= limit,
         "evidence": f"{words} words"},
        {"text": "No ISO, US-slash or month-name dates in the email body", "passed": not dates,
         "evidence": str(dates) if dates else "none found"},
    ]


it = pathlib.Path(sys.argv[1])
for ev in sorted(p for p in it.glob("eval-*") if p.is_dir()):
    key = ev.name.split("-", 2)[2]
    for cfg in ("with_skill", "without_skill"):
        run = ev / cfg / "run-1"
        f = run / "outputs" / "output.md"
        if not f.exists():
            continue
        res = grade(key, f.read_text())
        extra = run / "judged.json"
        if extra.exists():
            res += json.loads(extra.read_text())
        passed = sum(r["passed"] for r in res)
        json.dump({"expectations": res, "summary": {"passed": passed, "failed": len(res) - passed,
                   "total": len(res), "pass_rate": round(passed / len(res), 2)}},
                  open(run / "grading.json", "w"), indent=2)
        print(f"{ev.name:28} {cfg:14} {passed}/{len(res)}")
