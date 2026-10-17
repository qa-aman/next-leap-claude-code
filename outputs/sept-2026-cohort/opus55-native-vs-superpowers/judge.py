#!/usr/bin/env python3
"""Blind judge for the native vs superpowers runs.

Usage: judge.py <experiment_dir>
Writes judgements/absolute-<run>-<pass>.json and judgements/pairwise-<k>-<order>.json
"""
import json, re, subprocess, sys, pathlib, concurrent.futures as cf

E = pathlib.Path(sys.argv[1])
RUNS = ["native-1", "native-2", "superpowers-1", "superpowers-2"]
BRIEF = (E / "brief.md").read_text()
J = E / "judgements"
J.mkdir(exist_ok=True)

REDACT = re.compile(r"superpowers?:?[\w-]*|using-superpowers|writing-plans|executing-plans|subagent-driven-development|brainstorming skill|REQUIRED SUB-SKILL[^\n]*", re.I)


def bundle(run):
    arts = sorted((E / "runs" / run / "artifacts").glob("*.md"))
    parts = []
    for i, p in enumerate(arts, 1):
        parts.append(f"=== Document {i} ===\n" + REDACT.sub("[skill]", p.read_text()))
    return "\n\n".join(parts)


RUBRIC = """Score the candidate's planning documents for building this app. You are a senior staff engineer and a product lead.

The PM's full requirements (the candidate only knew what it asked the PM about):
""" + BRIEF + """

Score each criterion 1-5 (5 = excellent) and justify with a SHORT verbatim quote from the documents.
C1 Requirement capture: for each of R1-R16, is it correctly captured? Output a list of R-ids captured. Wrong or contradicting = not captured.
C2 Architecture soundness: fits budget (R12), free hosting, domain-restricted Google login (R8), 30-day deletion (R7), long notes up to 15,000 words (R2), accuracy handling (R4-R6). Are the tech choices justified?
C3 Plan executability: could an AI coding agent follow it without asking questions? Concrete files, order, dependencies.
C4 Verification: every phase or task has a concrete pass/fail check, including a way to measure extraction accuracy.
C5 Scope discipline: v1 vs later clearly separated, nothing gold-plated beyond the brief.
C6 Risk handling: names the real risks (LLM errors, nicknames, Hinglish, cost, privacy) and says what to do.
C7 Readable by a non-technical PM who must approve it.
Also list: the single biggest strength, the single biggest weakness, and any factual or technical error you spot.

Return ONLY JSON:
{"captured": ["R1",...], "C1":n,"C2":n,"C3":n,"C4":n,"C5":n,"C6":n,"C7":n,
 "quotes": {"C2":"...","C3":"...","C4":"..."}, "strength":"...", "weakness":"...", "errors":["..."]}"""

PAIR = """Two candidates planned the same app. Which set of documents would lead to a better built product for this PM?
PM requirements:
""" + BRIEF + """
Judge on: requirement capture, architecture soundness, plan executability, verification, scope discipline, risk handling.
Return ONLY JSON: {"winner":"X" or "Y" or "tie","margin":"clear|slight","why":["3-5 specific reasons with short quotes"]}"""


def call(prompt):
    p = subprocess.run(["claude", "-p", prompt, "--model", "claude-opus-5-5", "--effort", "high",
                        "--setting-sources", "project", "--tools", "", "--no-session-persistence",
                        "--output-format", "json"], capture_output=True, text=True, timeout=1800, cwd="/tmp")
    r = json.loads(p.stdout)["result"]
    m = re.search(r"\{.*\}", r, re.S)
    return json.loads(m.group(0)) if m else {"raw": r}


jobs = {}
with cf.ThreadPoolExecutor(4) as ex:
    for run in RUNS:
        for k in (1, 2):
            jobs[ex.submit(call, RUBRIC + "\n\nCANDIDATE DOCUMENTS:\n\n" + bundle(run))] = f"absolute-{run}-{k}"
    for k in (1, 2):
        n, s = bundle(f"native-{k}"), bundle(f"superpowers-{k}")
        jobs[ex.submit(call, PAIR + "\n\n### CANDIDATE X\n\n" + n + "\n\n### CANDIDATE Y\n\n" + s)] = f"pairwise-{k}-X=native"
        jobs[ex.submit(call, PAIR + "\n\n### CANDIDATE X\n\n" + s + "\n\n### CANDIDATE Y\n\n" + n)] = f"pairwise-{k}-X=superpowers"
    for f in cf.as_completed(jobs):
        name = jobs[f]
        try:
            res = f.result()
        except Exception as e:
            res = {"error": str(e)}
        (J / f"{name}.json").write_text(json.dumps(res, indent=1, ensure_ascii=False))
        print(name, "done")
