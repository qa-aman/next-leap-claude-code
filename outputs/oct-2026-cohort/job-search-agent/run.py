"""Run the job search once: upload inputs, start a session, stream events, download the shortlist.

Needs: pip install anthropic  and  export ANTHROPIC_API_KEY=...  and  ./setup.sh run first.
"""
import json
import time
from pathlib import Path

import anthropic

HERE = Path(__file__).parent
BUDGET_CENTS = "300"  # $3.00. The amount is in US cents, as a string. The session pauses at this cap.

lock = json.loads((HERE / "claude-lock.json").read_text())["resources"]
lead_id = lock["./agents/job-search-lead.md"]["id"]
env_id = lock["./environment.yaml"]["id"]
store_id = lock["./memory_store.yaml"]["id"]

client = anthropic.Anthropic()

uploads = []
for name in ["resume.md", "profile.md", "watchlist.md"]:
    f = client.files.upload(file=HERE / "inputs" / name)
    uploads.append({"type": "file", "file_id": f.id, "mount_path": f"/{name}"})

session = client.beta.sessions.create(
    agent=lead_id,
    environment_id=env_id,
    budget={"type": "limit", "max_list_cost": {"amount": BUDGET_CENTS, "currency": "USD"}},
    resources=uploads + [{
        "type": "memory_store",
        "memory_store_id": store_id,
        "access": "read_write",
        "instructions": "Read seen-jobs.md and feedback.md before you start. Update seen-jobs.md at the end.",
    }],
)
print(f"Session: {session.id}  (open it in the Console to watch every thread)\n")

with client.beta.sessions.events.stream(session.id) as stream:
    client.beta.sessions.events.send(
        session.id,
        events=[{"type": "user.message", "content": [{"type": "text", "text": "Run today's job search."}]}],
    )
    for event in stream:
        match event.type:
            case "agent.message":
                for block in event.content:
                    if block.type == "text":
                        print(block.text, end="")
            case "agent.tool_use":
                print(f"\n[tool: {event.name}]")
            case "session.thread_created":
                print(f"\n[new thread: {getattr(event, 'agent_name', '?')}]")
            case "session.status_idle":
                print("\n\nLead finished.")
                break

time.sleep(5)  # output files can appear a few seconds after the session goes idle
out = HERE / "results" / session.id
out.mkdir(parents=True, exist_ok=True)
for f in client.beta.files.list(scope_id=session.id, betas=["managed-agents-2026-04-01"]):
    client.files.download(f.id).write_to_file(out / Path(f.filename).name)
    print(f"saved {out / Path(f.filename).name}")
