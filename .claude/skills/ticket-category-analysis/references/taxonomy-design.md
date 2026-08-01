# Designing a taxonomy for a new domain

The taxonomy decides what the report can say. Everything downstream is arithmetic on top of it,
so an hour spent here is worth more than a day spent on the charts.

## The JSON shape

```json
{
  "domain": "HR Shared Services",
  "notes": "Optional. Shown at the top of the rendered Markdown.",
  "categories": {
    "Payroll": {
      "assignment_group": "Payroll Operations",
      "subcategories": {
        "Salary Query": {
          "issues": {
            "Amount differs from expectation": [
              "my salary is less this month than what i was told",
              "the amount credited does not match my letter"
            ]
          },
          "simulation": {
            "weight": 20,
            "median_hours": 0.9,
            "sigma": 0.3,
            "priority_mix": [0, 8, 55, 37],
            "reopen_rate": 0.03,
            "monthly_multiplier": {"2026-06": 1.4}
          }
        }
      }
    }
  }
}
```

`issues` phrasings and the whole `simulation` block are **only** used by `generate_sample.py`.
A taxonomy written for a real export can leave the phrasing lists empty. Validate with:

```bash
python3 taxonomy_io.py mytaxonomy.json --markdown taxonomy.md
```

## Sizing the three tiers

| Tier | Good range | What it answers |
|---|---|---|
| L1 Category | 5 to 8 | "Which part of the business is generating work?" A chart legend past 8 stops being readable, and the report folds the tail into Other |
| L2 Subcategory | 3 to 6 per category | "What specifically?" This is the tier the automation shortlist ranks, so it is the one that has to be right |
| L3 Issue Type | 2 to 5 per subcategory | "What exactly happened?" Detail for the drill-down, not for the headline |

Rough total: 20 to 40 subcategories. Fewer and every finding is "Access is big", which nobody
can act on. More and each bucket holds too few tickets a month for a trend to mean anything.

**Sanity check against volume.** A subcategory needs roughly 10 or more tickets a month to
support a median and a spread. Divide your monthly volume by your subcategory count: under 10,
the taxonomy is too fine for the data you have.

## L2 is the tier that carries the decision

The shortlist ranks subcategories, so a subcategory is useful only if it groups tickets that
share a **fix**. That is the test, not whether they share a topic.

"Password" works because every ticket in it ends the same way. "Miscellaneous Access" fails,
because it groups tickets that share only the absence of a better home. If you cannot describe
in one sentence what a person does to resolve a typical ticket in a subcategory, split it or
merge it.

## Write phrasings the way users actually type

Only needed for sample generation, but this is where sample data earns its keep or becomes
useless. A description that names its own category tests nothing.

| Weak | Strong |
|---|---|
| "Password reset required" | "cant get into the system since morning, tried twice already" |
| "VPN connectivity issue" | "the tunnel drops every 20 minutes while working from home" |
| "Payroll discrepancy" | "my salary is less this month than what i was told" |

Two to five phrasings per issue type. Lowercase, no punctuation, no jargon. The generator adds
greetings, sign-offs, typos and random capitals on top, so write the bare complaint.

Include at least one genuinely ambiguous phrasing per taxonomy. A pair that could plausibly land
in two buckets is what tells you whether your accuracy number is real or whether the buckets are
so far apart that anything would score well.

## The simulation block

Ignored entirely on real data. Every field is optional and falls back to a sensible default.

| Field | Meaning |
|---|---|
| `weight` | Relative share of volume. Any scale, they are normalised |
| `median_hours` | Typical resolution time |
| `sigma` | Lognormal spread. **0.2 to 0.4 = scriptable and tight, 0.8 to 1.2 = every ticket is different.** This is what creates or removes automation candidates, so set it deliberately |
| `priority_mix` | Weights over P1, P2, P3, P4 |
| `reopen_rate` | Probability a ticket comes back |
| `monthly_multiplier` | Per-month volume multiplier, for building a trend |

If you want the sample to contain a clear automation candidate, give one subcategory a high
weight, a low `sigma` (0.25 or so) and a rising `monthly_multiplier`. If you want it to contain
an expensive-but-not-automatable queue, give another a high `median_hours` and a `sigma` near 1.

## Changing a taxonomy that is already in use

Renaming or splitting a bucket breaks comparability with previous months, silently. The numbers
still render, they just quietly mean something different.

1. Note the change in that month's report, next to the affected rows.
2. Prefer adding a new subcategory over redefining an existing one.
3. When splitting, keep the old name on the larger half so most of the history still lines up.
4. If several buckets change at once, say plainly that month-on-month comparison does not hold
   for that cycle. A stated gap beats a misleading trend line.
