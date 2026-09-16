---
name: prd
description: >
  Write a MeetFlow PRD that follows the company PRD template (14-templates/template-prd.md)
  section for section, with every number and persona cited to a repo file. Use this skill
  whenever the user asks for a PRD, product requirements, a requirements doc, "document this
  feature", "spec out X for the roadmap", "turn this idea into a PRD", or wants a feature idea
  formalised for review - even if they do not say "PRD". Also use it when the user asks to
  update or review an existing PRD against the template. Prefer this over write-prd (Shape Up
  pitch format) whenever the output is for MeetFlow or should match the repo template.
---

# PRD (template-driven)

Produce a PRD that a reviewer can check against `assets/template-prd.md` line by line, where
every claim traces to a file in this repo. The template exists so that PRDs across the team
read the same way and so nobody argues about structure in review. The citation rule exists
because a PRD with an invented baseline sends engineering after the wrong target.

## Step 1: Gather evidence before writing anything

Read these in order. Do not draft until all are done, because the Problem and Success
Metrics sections depend on numbers that only live here.

1. `03-product-knowledge/company.md` - baselines (accuracy 66%, churn 4.1%, NPS 34), priorities, risks.
2. `04-strategy/product-vision.md` - the 12-month baseline table and gaps to close.
3. `04-strategy/okrs-q2-2026.md` - every metric target in the PRD must map to a Key Result here. Never invent a target.
4. `05-user-personas/` - pick 2 to 4 personas. Read their files, do not work from memory of their names.
5. `06-user-feedback/` and `07-user-interviews/` - the one or two quotes or stats that make the Problem section concrete.
6. `03-product-knowledge/product.md` - current feature status, plan tiers, and what already exists.
7. Any existing PRD for the same feature in `08-product-features/` - if one exists, tell the user and ask whether to update it or write a new one.

If the feature is already in flight (check `product.md` and `04-strategy/`), say so in the Status line and the Problem section instead of writing it as a fresh proposal.

## Step 2: Fill the template, section by section

Read `assets/template-prd.md` and keep its exact headings and order:

Header (Pillar, Owner, Target, Status) > Problem > Who It's For > What It Does >
How It Works > Success Metrics > What We're NOT Building > Dependencies > Timeline.

All 8 sections are required, none renamed, none reordered. You may add a section (for
example Plan Availability, Rollout Strategy, Observability) only when the feature genuinely
needs it, and it goes after the template section it extends. `references/example-prd.md`
shows this done well: 8 template sections plus 4 additions, template order intact.

Rules per section, drawn from the template comments and `.claude/rules/feature-writing.md`:

1. **Header** - Pillar is one of AI Intelligence, Platform & Integrations, Enterprise & Security, Core Experience (see `company.md`). Owner is the PM who owns that pillar. Target is a month and year. Status starts as Draft.
2. **Problem** - 2 to 4 sentences. Lead with a number and cite the file inline, for example `(34% of action items wrong or missing, 03-product-knowledge/company.md)`. Keep the "Cross-reference" line from the template.
3. **Who It's For** - 2 to 4 personas, each with role, what they need from this feature, and the `See 05-user-personas/<file>.md` pointer. The need must come from that persona's file, not a guess.
4. **What It Does** - 4 to 5 bullets, each a capability the user can see or act on. No implementation detail.
5. **How It Works** - numbered steps from trigger to completion. Say what the system does and what the user sees at each step.
6. **Success Metrics** - 3 to 4 metrics, each with baseline, target, and timeframe. Baseline from `company.md` or `product-vision.md`, target from `okrs-q2-2026.md`. If no OKR covers a metric, write `Target: to be set with <owner>` instead of inventing one. Keep the OKR cross-reference line.
7. **What We're NOT Building** - at least 3 items. Each one should be something a reviewer could plausibly ask for, so the list actually prevents scope arguments.
8. **Dependencies** - name the thing, then the reason it blocks launch.
9. **Timeline** - table, one row per milestone, outcome-based. Dates must be consistent with the Target in the header and the fictional today of 17-03-2026 (see CLAUDE.md).

Delete the HTML comments and every `[PLACEHOLDER]` before saving. A leftover placeholder means the section was not actually written.

## Step 3: Save and self-check

Save to `outputs/<current cohort folder>/prd-<feature-name>.md` (kebab-case, no date in the filename). Glob `outputs/` and use the most recent cohort folder. If the user asks for it to live with the other feature docs, save under `08-product-features/<nn>-<feature-name>/prd-<feature-name>.md` instead.

Before handing over, run the mechanical checks:

```bash
grep -nE "\[[A-Z][A-Z /-]+\]|<!--" <file>          # leftover placeholders or comments: must return nothing
for h in "Problem" "Who It's For" "What It Does" "How It Works" "Success Metrics" "What We're NOT Building" "Dependencies" "Timeline"; do grep -q "^## $h" <file> || echo "MISSING: $h"; done   # must print nothing
grep -nE "[0-9]{4}-[0-9]{2}-[0-9]{2}|[0-9]{1,2}/[0-9]{1,2}/[0-9]{4}" <file>   # wrong date formats: must return nothing
grep -n "—" <file>                                  # em dashes: must return nothing
```

Then confirm by reading, not by assumption: every number has a file citation, every persona has a `See 05-user-personas/` pointer, every target maps to a Key Result. If a section could not be sourced, leave a one-line `Open question:` under it naming who can answer, rather than filling it with a plausible guess.

Report to the user in 3 to 5 lines: the file path, which sources fed the Problem and Success Metrics, and any open questions.

## Style

Short sentences. Numbers over adjectives. DD-MM-YYYY dates. No em dashes, no emojis. Match the voice of `references/example-prd.md`, which is a finished PRD written against this template.
