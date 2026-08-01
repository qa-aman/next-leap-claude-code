#!/usr/bin/env python3
"""Extract work-log evidence from this project's Claude Code JSONL transcripts.

Two modes:

  --index            List every date (IST) that has session activity, with a
                     count of prompts and whether a log file already exists.
  --date DD-MM-YYYY  Print a compact evidence digest for that single date.
                     Repeatable.

Timestamps in the JSONL are UTC. Everything here is converted to IST
(Asia/Kolkata) so a "day" means Aman's day, not a UTC day.
"""

import argparse
import json
import os
import re
import sys
from collections import OrderedDict, defaultdict
from datetime import datetime, timedelta, timezone
from pathlib import Path

IST = timezone(timedelta(hours=5, minutes=30))

PROJECT_ROOT = Path(__file__).resolve().parents[4]
JSONL_DIR = Path.home() / ".claude" / "projects" / (
    "-" + str(PROJECT_ROOT).lstrip("/").replace("/", "-")
)
LOG_ROOT = PROJECT_ROOT / ".local" / "log"

MONTHS = [
    "january", "february", "march", "april", "may", "june",
    "july", "august", "september", "october", "november", "december",
]

# User turns that are machine noise, not something Aman typed.
NOISE_PREFIXES = (
    "<system-reminder>",
    "<command-name>",
    "<command-message>",
    "<local-command-stdout>",
    "<local-command-caveat>",
    "<task-notification>",
    "[Image:",
    "Caveat: The messages below were generated",
    "[Request interrupted",
    "API Error",
    "This session is being continued from a previous conversation",
    "Base directory for this skill:",  # a skill body injected as a user turn
)

WRITE_TOOLS = {"Write", "Edit", "NotebookEdit", "MultiEdit"}
READ_TOOLS = {"Read", "Glob", "Grep"}


def commit_messages(cmd):
    """Pull commit subjects out of a bash command, including the heredoc form
    `git commit -m "$(cat <<'EOF' ... EOF)"` where the subject is the next line."""
    out = []
    lines = cmd.splitlines()
    for i, line in enumerate(lines):
        if "git commit" not in line:
            continue
        m = re.search(r"-m\s+[\"']([^\"'$][^\"']*)[\"']", line)
        if m:
            out.append(m.group(1).strip())
            continue
        if "<<" in line:  # heredoc: subject is the first non-empty following line
            for nxt in lines[i + 1:]:
                nxt = nxt.strip()
                if nxt and nxt != "EOF":
                    out.append(nxt)
                    break
    return out


def log_path_for(date_str):
    """.local/log/<MM-monthname-YYYY>/<DD-MM-YYYY>.md"""
    dd, mm, yyyy = date_str.split("-")
    folder = f"{mm}-{MONTHS[int(mm) - 1]}-{yyyy}"
    return LOG_ROOT / folder / f"{date_str}.md"


def to_ist(ts):
    if not ts:
        return None
    try:
        return datetime.fromisoformat(ts.replace("Z", "+00:00")).astimezone(IST)
    except ValueError:
        return None


def text_of(content):
    """Flatten a message content field to plain text."""
    if isinstance(content, str):
        return content
    if isinstance(content, list):
        parts = []
        for block in content:
            if isinstance(block, dict) and block.get("type") == "text":
                parts.append(block.get("text", ""))
        return "\n".join(parts)
    return ""


def clean_prompt(txt):
    txt = re.sub(r"<system-reminder>.*?</system-reminder>", "", txt, flags=re.S)
    return txt.strip()


def is_noise(txt):
    return (not txt) or txt.startswith(NOISE_PREFIXES)


def scan():
    """Walk every JSONL once. Returns {date: session records}."""
    if not JSONL_DIR.is_dir():
        sys.exit(f"No transcript directory found at {JSONL_DIR}")

    days = defaultdict(lambda: OrderedDict())

    for jf in sorted(JSONL_DIR.glob("*.jsonl")):
        sid = jf.stem
        title = None
        # events keyed by IST date so one session spanning midnight splits correctly
        per_date = defaultdict(lambda: {
            "session": sid[:8],
            "title": None,
            "branch": None,
            "first": None,
            "last": None,
            "prompts": [],
            "files": OrderedDict(),
            "reads": OrderedDict(),
            "bash": [],
            "commits": [],
            "skills": OrderedDict(),
            "agents": [],
            "todos": [],
        })

        with jf.open(encoding="utf-8", errors="replace") as fh:
            for line in fh:
                line = line.strip()
                if not line:
                    continue
                try:
                    d = json.loads(line)
                except json.JSONDecodeError:
                    continue

                typ = d.get("type")
                if typ == "ai-title":
                    title = d.get("aiTitle")
                    continue
                if typ not in ("user", "assistant"):
                    continue
                if d.get("isSidechain"):
                    continue

                stamp = to_ist(d.get("timestamp"))
                if stamp is None:
                    continue
                key = stamp.strftime("%d-%m-%Y")
                rec = per_date[key]
                rec["branch"] = d.get("gitBranch") or rec["branch"]
                if rec["first"] is None or stamp < rec["first"]:
                    rec["first"] = stamp
                if rec["last"] is None or stamp > rec["last"]:
                    rec["last"] = stamp

                msg = d.get("message") or {}
                content = msg.get("content")

                if typ == "user":
                    txt = clean_prompt(text_of(content))
                    if not is_noise(txt):
                        rec["prompts"].append((stamp.strftime("%H:%M"), txt))
                    continue

                for block in content if isinstance(content, list) else []:
                    if not isinstance(block, dict) or block.get("type") != "tool_use":
                        continue
                    name = block.get("name", "")
                    inp = block.get("input") or {}

                    if name in WRITE_TOOLS:
                        fp = inp.get("file_path") or inp.get("notebook_path")
                        if fp:
                            rec["files"].setdefault(fp, name)
                    elif name in READ_TOOLS:
                        fp = inp.get("file_path") or inp.get("pattern") or inp.get("path")
                        if fp:
                            rec["reads"].setdefault(str(fp), name)
                    elif name == "Bash":
                        cmd = (inp.get("command") or "").strip()
                        if cmd:
                            rec["bash"].append(cmd)
                            rec["commits"].extend(commit_messages(cmd))
                    elif name == "Skill":
                        s = inp.get("skill")
                        if s:
                            rec["skills"].setdefault(s, inp.get("args") or "")
                    elif name in ("Agent", "Task"):
                        rec["agents"].append(
                            f"{inp.get('subagent_type') or 'general-purpose'}: "
                            f"{inp.get('description') or ''}"
                        )
                    elif name == "TodoWrite":
                        for t in inp.get("todos") or []:
                            if isinstance(t, dict) and t.get("content"):
                                rec["todos"].append(t["content"])

        for key, rec in per_date.items():
            rec["title"] = title
            if rec["prompts"] or rec["files"] or rec["bash"]:
                days[key][sid] = rec

    return days


def sort_dates(keys):
    return sorted(keys, key=lambda k: datetime.strptime(k, "%d-%m-%Y"))


def cmd_index(days, today):
    print(f"TODAY (IST): {today}")
    print(f"TRANSCRIPTS: {JSONL_DIR}")
    print(f"LOG ROOT:    {LOG_ROOT}")
    print()
    print(f"{'DATE':<12} {'SESS':>5} {'PROMPTS':>8} {'FILES':>6}  LOG")
    missing = []
    for key in sort_dates(days):
        recs = days[key].values()
        prompts = sum(len(r["prompts"]) for r in recs)
        files = len({f for r in recs for f in r["files"]})
        exists = log_path_for(key).exists()
        if not exists:
            missing.append(key)
        print(f"{key:<12} {len(days[key]):>5} {prompts:>8} {files:>6}  "
              f"{'yes' if exists else 'MISSING'}")
    print()
    print(f"DATES WITH ACTIVITY: {len(days)}")
    print(f"MISSING LOGS: {len(missing)}")
    if missing:
        print("MISSING_DATES: " + " ".join(missing))


def trim(txt, limit):
    txt = " ".join(txt.split())
    return txt if len(txt) <= limit else txt[:limit] + " [...]"


def cmd_date(days, date_str, prompt_chars, max_bash):
    recs = days.get(date_str)
    print(f"===== {date_str} =====")
    print(f"LOG FILE: {log_path_for(date_str)} "
          f"({'exists' if log_path_for(date_str).exists() else 'not created'})")
    if not recs:
        print("No session activity found for this date.")
        return
    print(f"SESSIONS: {len(recs)}")
    for sid, r in recs.items():
        span = ""
        if r["first"] and r["last"]:
            span = f"{r['first']:%H:%M} - {r['last']:%H:%M} IST"
        print()
        print(f"--- SESSION {r['session']} | {r['title'] or 'untitled'} | {span} "
              f"| branch: {r['branch'] or '?'}")

        if r["prompts"]:
            print("  PROMPTS:")
            for t, p in r["prompts"]:
                print(f"    [{t}] {trim(p, prompt_chars)}")

        if r["files"]:
            print("  FILES WRITTEN/EDITED:")
            for fp, tool in r["files"].items():
                try:
                    rel = str(Path(fp).relative_to(PROJECT_ROOT))
                except ValueError:
                    rel = fp
                print(f"    {tool:<12} {rel}")

        if r["skills"]:
            print("  SKILLS: " + ", ".join(r["skills"]))
        if r["agents"]:
            print("  AGENTS:")
            for a in r["agents"][:15]:
                print(f"    {trim(a, 120)}")
        if r["commits"]:
            print("  GIT COMMITS:")
            for c in r["commits"]:
                print(f"    {c}")
        if r["todos"]:
            seen = list(dict.fromkeys(r["todos"]))[:20]
            print("  TODOS:")
            for t in seen:
                print(f"    {trim(t, 120)}")
        if r["bash"] and max_bash:
            print(f"  BASH ({len(r['bash'])} calls, showing {min(max_bash, len(r['bash']))}):")
            for c in r["bash"][:max_bash]:
                print(f"    {trim(c, 160)}")
        if r["reads"]:
            print(f"  READ/SEARCHED: {len(r['reads'])} paths")
            for fp in list(r["reads"])[:25]:
                try:
                    rel = str(Path(fp).relative_to(PROJECT_ROOT))
                except (ValueError, TypeError):
                    rel = fp
                print(f"    {rel}")


def main():
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--index", action="store_true",
                    help="list all dates with activity and whether a log exists")
    ap.add_argument("--date", action="append", default=[],
                    help="DD-MM-YYYY, repeatable; print evidence digest")
    ap.add_argument("--today", action="store_true", help="shorthand for --date <today IST>")
    ap.add_argument("--prompt-chars", type=int, default=600,
                    help="truncate each prompt to N chars (default 600)")
    ap.add_argument("--max-bash", type=int, default=25,
                    help="max bash commands to show per session (0 to hide)")
    args = ap.parse_args()

    today = datetime.now(IST).strftime("%d-%m-%Y")
    days = scan()

    if args.index or (not args.date and not args.today):
        cmd_index(days, today)
        return

    targets = list(args.date)
    if args.today:
        targets.append(today)
    for date_str in targets:
        try:
            datetime.strptime(date_str, "%d-%m-%Y")
        except ValueError:
            sys.exit(f"Bad date '{date_str}'. Use DD-MM-YYYY.")
        cmd_date(days, date_str, args.prompt_chars, args.max_bash)
        print()


if __name__ == "__main__":
    main()
