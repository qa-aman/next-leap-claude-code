"""Send the latest service desk review by email. Run by launchd every Friday at 19:00.

The report is refreshed when a new export arrives (monthly or quarterly). This email goes out
every week regardless, so it always states when the figures were last refreshed. Old numbers
must never read as this week's.

Two guards, because this sends to people without anyone pressing Send:
  1. Every recipient must be on the allowlist in state/send-config.json. Anything else stops
     the run before a message is built. Only Aman edits that list.
  2. Composio must be on aman_workspace, and the connected Gmail must be the configured sender.

A failure is never silent: it is written to state/send-log.jsonl and shown as a macOS
notification, once per missed Friday rather than on every retry.

Catch-up: launchd runs this with --if-due at login, every hour and at Friday 19:00. The run sends
only when a Friday 19:00 has passed since the last successful send. So a Mac that was off, asleep
or offline at 19:00 sends on its next run, a failed send retries the next hour, and no week is
sent twice. A send more than 3 hours after 19:00 says it is late.

    python3 weekly_send.py --dry-run     # print the email, send nothing
    python3 weekly_send.py --if-due      # what launchd runs: send only if a Friday is owed
    python3 weekly_send.py               # send now (manual)
"""
import argparse
import datetime as dt
import html
import json
import os
import subprocess
import sys
from pathlib import Path

SKILL = Path(__file__).resolve().parents[1]
REPO = SKILL.parents[2]
CONFIG = SKILL / "state" / "send-config.json"
HISTORY = SKILL / "state" / "history.json"
LOG = SKILL / "state" / "send-log.jsonl"
COMPOSIO = os.path.expanduser("~/.local/bin/composio")
E = html.escape


def log(status, **kw):
    LOG.parent.mkdir(parents=True, exist_ok=True)
    with LOG.open("a") as f:
        f.write(json.dumps({"at": dt.datetime.now().strftime("%d-%m-%Y %H:%M"), "status": status, **kw}) + "\n")


SLOT = None  # the Friday 19:00 this run is sending for, when run with --if-due


def due_slot(now):
    """The most recent Friday 19:00 at or before now."""
    d = now.date() - dt.timedelta(days=(now.weekday() - 4) % 7)
    slot = dt.datetime.combine(d, dt.time(19, 0))
    return slot if slot <= now else slot - dt.timedelta(days=7)


def entries():
    if not LOG.exists():
        return []
    return [json.loads(x) for x in LOG.read_text().splitlines() if x.strip()]


def stamp(e):
    return dt.datetime.strptime(e["at"], "%d-%m-%Y %H:%M")


def fail(msg):
    slot = SLOT.strftime("%d-%m-%Y %H:%M") if SLOT else None
    told = slot and any(e["status"] == "failed" and e.get("slot") == slot for e in entries())
    log("failed", reason=msg, slot=slot)
    if told:
        sys.exit(f"Not sent (retrying hourly, already notified): {msg}")
    subprocess.run(["osascript", "-e", f'display notification "{msg[:180]}" with title "Service desk email not sent"'],
                   check=False)
    sys.exit(f"Not sent: {msg}")


def composio(*args):
    p = subprocess.run([COMPOSIO, *args], capture_output=True, text=True, timeout=120)
    if p.returncode != 0:
        fail(f"composio {' '.join(args[:2])} failed: {(p.stderr or p.stdout).strip()[:300]}")
    return json.loads(p.stdout)


def latest_run(include_test):
    rows = json.loads(HISTORY.read_text()) if HISTORY.exists() else []
    rows = [r for r in rows if r.get("review_url") and (include_test or not r.get("test"))]
    if not rows:
        fail("no run with a published review in history.json")
    return rows[-1]


def build(run, summary, cfg, late_for=None, now=None):
    k, pk = summary["kpis"], summary.get("previous_kpis")
    refreshed = run["run_date"]
    age = ((now or dt.datetime.now()).date() - dt.datetime.strptime(refreshed, "%d-%m-%Y").date()).days
    stale = (f"No new ticket export this week. These figures are from the refresh on {refreshed}."
             if age >= 7 else f"Refreshed on {refreshed}.")
    if late_for:
        stale = (f"Sent late: this was due on Friday {late_for.strftime('%d-%m-%Y')} at 19:00, "
                 "and the Mac was off, asleep or offline. " + stale)
    sample = summary.get("sample_data")
    subject = f"Service desk review: {summary['short_period']}" + (" (sample data)" if sample else "")
    vs = lambda now, was, unit="": f"{now}{unit}" + (f" ({was}{unit} last period)" if was is not None else "")
    body = [
        f"<p>Hi all,</p><p><strong>{E(summary['verdict'])}</strong></p>",
        f"<p>Why it matters: these are the decisions for this period, each with an owner.</p>",
        "<ol>" + "".join(f"<li>{E(d)}</li>" for d in summary["decisions"]) + "</ol>",
        "<p>The numbers for " + E(summary["period"]) + ":</p><ol>"
        f"<li>Tickets: {vs(k['tickets'], pk and pk['tickets'])}</li>"
        f"<li>SLA met: {vs(k['sla_met_pct'], pk and pk['sla_met_pct'], '%')}</li>"
        f"<li>Agent hours: {k['agent_hours']:,}</li>"
        f"<li>Reopened: {k['reopen_pct']}%</li></ol>",
    ]
    if summary.get("to_confirm"):
        body.append("<p>Causes still to confirm with their owners: " + E(", ".join(summary["to_confirm"])) + ".</p>")
    body.append(f'<p>Full review: <a href="{E(run["review_url"])}">{E(run["review_url"])}</a><br>'
                f'Dashboard with filters: <a href="{E(run["url"])}">{E(run["url"])}</a></p>')
    body.append(f"<p>{E(stale)}</p>")
    if sample:
        body.append("<p><em>Sample data: generated test tickets used to design this report, not real results.</em></p>")
    body.append(f"<p>Best,<br>{E(cfg.get('signature', 'Aman'))}</p>")
    return subject, "\n".join(body)


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--dry-run", action="store_true")
    ap.add_argument("--if-due", action="store_true",
                    help="send only if a Friday 19:00 has passed since the last successful send")
    ap.add_argument("--now", help="test only: pretend it is this time, DD-MM-YYYY HH:MM (use with --dry-run)")
    a = ap.parse_args()
    if a.now and not a.dry_run:
        sys.exit("--now is for testing and needs --dry-run")

    global SLOT
    now = dt.datetime.strptime(a.now, "%d-%m-%Y %H:%M") if a.now else dt.datetime.now()
    late_for = None
    if a.if_due:
        SLOT = due_slot(now)
        if any(e["status"] == "sent" and stamp(e) >= SLOT for e in entries()):
            print(f"Nothing due: already sent since {SLOT.strftime('%d-%m-%Y %H:%M')}.")
            return
        if now - SLOT > dt.timedelta(hours=3):
            late_for = SLOT

    cfg = json.loads(CONFIG.read_text())
    allow = {x.lower() for x in cfg["allowlist"]}
    to = [x.lower() for x in cfg["to"]] + [x.lower() for x in cfg.get("cc", [])]
    blocked = [x for x in to if x not in allow]
    if blocked:
        fail(f"recipients not on the allowlist: {', '.join(blocked)}")

    run = latest_run(cfg.get("include_test_runs", False))
    review = REPO / run["review_page"]
    summary_path = review.with_suffix(".json")
    if not summary_path.exists():
        fail(f"{summary_path.name} missing: rerun quarterly_review.py for {run['period']}")
    subject, body = build(run, json.loads(summary_path.read_text()), cfg, late_for, now)

    if a.dry_run:
        if a.if_due:
            print(f"DUE for Friday {SLOT.strftime('%d-%m-%Y')} 19:00" + (" (late)" if late_for else "") + "\n")
        print(f"To: {', '.join(cfg['to'])}\nCc: {', '.join(cfg.get('cc', []))}\nSubject: {subject}\n\n{body}")
        return

    if composio("whoami").get("current_org_name") != "aman_workspace":
        fail("Composio is not on aman_workspace")
    sender = composio("execute", "GMAIL_GET_PROFILE", "-d", "{}").get("data", {}).get("emailAddress", "")
    if sender.lower() != cfg["from"].lower():
        fail(f"connected Gmail is {sender or 'unknown'}, expected {cfg['from']}")
    payload = {"recipient_email": cfg["to"][0], "extra_recipients": cfg["to"][1:], "cc": cfg.get("cc", []),
               "subject": subject, "body": body, "is_html": True}
    out = composio("execute", "GMAIL_SEND_EMAIL", "-d", json.dumps(payload))
    if not out.get("successful"):
        fail(f"Gmail refused the send: {str(out.get('error'))[:300]}")
    log("sent", to=cfg["to"], subject=subject, period=run["period"], message_id=out.get("data", {}).get("id"),
        slot=SLOT.strftime("%d-%m-%Y %H:%M") if SLOT else "manual", late=bool(late_for))
    print(f"Sent '{subject}' to {', '.join(cfg['to'])}")


if __name__ == "__main__":
    main()
