#!/usr/bin/env python3
"""Opus 5.5 native loop vs Superpowers: one arm, one run.

Usage: run_experiment.py <arm: native|superpowers> <run_id> <workdir> <outdir>

Builder = Claude Code on claude-opus-5-5, user settings skipped (no personal
plugins, hooks or CLAUDE.md). The superpowers arm adds only the superpowers
plugin via --plugin-dir. A simulated PM (Sonnet) answers from brief.md.
"""
import json, os, re, subprocess, sys, time, uuid, shutil, pathlib

ARM, RUN_ID, WORK, OUT = sys.argv[1], sys.argv[2], pathlib.Path(sys.argv[3]), pathlib.Path(sys.argv[4])
HERE = pathlib.Path(__file__).parent
BRIEF = (HERE / "brief.md").read_text()
IDEA = re.search(r"## The idea.*?\n\n(.+?)\n\n", BRIEF, re.S).group(1).strip()
IDEA = IDEA[0].lower() + IDEA[1:]
SP_DIR = os.path.expanduser("~/.claude/plugins/cache/claude-plugins-official/superpowers/6.4.1")
MAX_ROUNDS = 30

NONINTERACTIVE = (
    "You are running non-interactively. The AskUserQuestion tool is unavailable. "
    "Whenever you would ask the user something, write the question(s) in your reply, "
    "exactly as you would have asked them, and end your turn. The user answers in the next message. "
    "Do not write any application code in this session."
)

NATIVE_STEPS = [
    # Step 2 of the guide, verbatim from code.claude.com/docs/en/best-practices
    ("same", f"I want to build {IDEA} Interview me in detail using the AskUserQuestion tool. Ask about technical implementation, UI/UX, edge cases, concerns, and tradeoffs. Don't ask obvious questions, dig into the hard parts I might not have considered. Keep interviewing until we've covered everything, then write a complete spec to SPEC.md."),
    # Step 3 of the guide
    ("same", 'Read SPEC.md. Add three sections: 1) "Out of scope" listing what we are NOT building. 2) "Phases": split the build into 3-5 small phases, each one testable on its own. 3) For every phase, a "How we check it" line: a test, a command, or a screenshot that gives a clear pass or fail. Also create a short CLAUDE.md with the rules for this project. Ask me before adding anything I did not ask for.'),
    # Step 4-5 of the guide, fresh session, plan written to a file so it can be compared
    ("fresh", "Read SPEC.md and CLAUDE.md. Write a detailed implementation plan for every phase to PLAN.md: the architecture, every file you will create or change, the order, and how each phase is checked. Do not write application code."),
]
SUPERPOWERS_STEPS = [
    ("same", f"I want to build {IDEA} Use your superpowers skills to brainstorm this with me and then write the implementation plan. Do not start implementing."),
]

SIM_SYSTEM = f"""You are simulating a non-technical product manager answering an AI assistant that is helping you plan an app.
Your knowledge is ONLY this brief:
---
{BRIEF}
---
Rules:
- Answer only what the assistant asked. Short, plain, like a busy PM. Do not volunteer brief items it did not ask about.
- If it asks a broad "anything else?" question, you may mention at most two brief items it has not covered yet.
- If it asks something the brief does not cover, say you have no preference and ask it to recommend.
- If it offers options or asks for approval of a design section, pick or approve what best fits the brief, and correct anything that contradicts the brief.
- If it offers a visual companion, a browser, or asks about git, worktrees or how to execute (subagents vs inline), decline and say to just write the documents.
- If it asks to start implementing or coding, or the documents requested are written and it is not asking you anything, reply with exactly: <<DONE>>
Reply with only your answer text."""


def claude(args, prompt, cwd):
    t = time.time()
    p = subprocess.run(["claude", "-p", prompt, "--output-format", "json", *args],
                       cwd=cwd, capture_output=True, text=True, timeout=1800)
    try:
        d = json.loads(p.stdout)
    except Exception:
        d = {"result": f"PARSE_ERROR stdout={p.stdout[:500]} stderr={p.stderr[:500]}", "is_error": True}
    d["_wall"] = round(time.time() - t, 1)
    return d


def builder_args(session, new):
    a = ["--model", "claude-opus-5-5", "--setting-sources", "project",
         "--permission-mode", "acceptEdits",
         "--allowedTools", "Read,Write,Edit,Glob,Grep,Skill,Agent,Task,TodoWrite,Bash(mkdir:*),Bash(ls:*),Bash(git:*)",
         "--append-system-prompt", NONINTERACTIVE]
    if ARM == "superpowers":
        a += ["--plugin-dir", SP_DIR]
    a += (["--session-id", session] if new else ["--resume", session])
    return a


def simulate(history_tail):
    d = claude(["--model", "sonnet", "--setting-sources", "project", "--tools", "",
                "--system-prompt", SIM_SYSTEM, "--no-session-persistence"],
               "The assistant just said:\n\n" + history_tail + "\n\nYour reply:", WORK)
    return d.get("result", "").strip(), d


def main():
    WORK.mkdir(parents=True, exist_ok=True)
    OUT.mkdir(parents=True, exist_ok=True)
    log, metrics = [], {"arm": ARM, "run": RUN_ID, "builder_calls": 0, "sim_calls": 0,
                        "builder_cost_usd": 0.0, "sim_cost_usd": 0.0, "wall_s": 0.0,
                        "questions_rounds": 0, "errors": 0}
    steps = NATIVE_STEPS if ARM == "native" else SUPERPOWERS_STEPS
    session, rounds = None, 0
    for mode, first_prompt in steps:
        new = session is None or mode == "fresh"
        if new:
            session = str(uuid.uuid4())
        msg = first_prompt
        while rounds < MAX_ROUNDS:
            rounds += 1
            b = claude(builder_args(session, new), msg, WORK)
            new = False
            metrics["builder_calls"] += 1
            metrics["builder_cost_usd"] += b.get("total_cost_usd") or 0
            metrics["wall_s"] += b["_wall"]
            if b.get("is_error"):
                metrics["errors"] += 1
            out = b.get("result", "")
            log.append({"role": "user", "text": msg})
            log.append({"role": "builder", "text": out, "turns": b.get("num_turns"), "session": session})
            reply, s = simulate(out[-12000:])
            metrics["sim_calls"] += 1
            metrics["sim_cost_usd"] += s.get("total_cost_usd") or 0
            if "<<DONE>>" in reply:
                log.append({"role": "sim", "text": "<<DONE>>"})
                break
            metrics["questions_rounds"] += 1
            log.append({"role": "sim", "text": reply})
            msg = reply
    metrics["rounds_total"] = rounds
    (OUT / "transcript.json").write_text(json.dumps(log, indent=1, ensure_ascii=False))
    with open(OUT / "transcript.md", "w") as f:
        for e in log:
            f.write(f"\n\n### {e['role'].upper()}\n\n{e['text']}\n")
    arts = OUT / "artifacts"
    arts.mkdir(exist_ok=True)
    for pth in WORK.rglob("*.md"):
        if ".git" in pth.parts:
            continue
        dest = arts / str(pth.relative_to(WORK)).replace("/", "__")
        shutil.copy(pth, dest)
    metrics["artifact_files"] = sorted(p.name for p in arts.iterdir())
    metrics["artifact_words"] = sum(len(p.read_text().split()) for p in arts.iterdir())
    (OUT / "metrics.json").write_text(json.dumps(metrics, indent=1))
    print(json.dumps(metrics))


if __name__ == "__main__":
    main()
