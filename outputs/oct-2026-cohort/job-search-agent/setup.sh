#!/usr/bin/env bash
# One-time setup: creates the 3 worker agents, the environment, the memory store, then the lead.
# Needs: brew install anthropics/tap/ant  and  export ANTHROPIC_API_KEY=...
set -euo pipefail
cd "$(dirname "$0")"

# 1. Workers, environment and memory store. ant apply records every ID in claude-lock.json.
ant apply agents/job-scout.md agents/fit-scorer.md agents/application-writer.md environment.yaml memory_store.yaml

# 2. The lead lists the workers by ID, so read them from the lockfile and fill the template.
export SCOUT_ID=$(jq -er '.resources["./agents/job-scout.md"].id' claude-lock.json)
export SCORER_ID=$(jq -er '.resources["./agents/fit-scorer.md"].id' claude-lock.json)
export WRITER_ID=$(jq -er '.resources["./agents/application-writer.md"].id' claude-lock.json)
envsubst '$SCOUT_ID $SCORER_ID $WRITER_ID' < agents/job-search-lead.md.tmpl > agents/job-search-lead.md

# 3. The lead.
ant apply agents/job-search-lead.md

echo "Done. IDs are in claude-lock.json. Next: python run.py"
