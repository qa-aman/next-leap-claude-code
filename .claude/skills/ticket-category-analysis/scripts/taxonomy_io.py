"""
Load, validate and render a 3-tier ticket taxonomy.

Every other script in this skill imports this one, so the taxonomy has exactly one
definition and the classifier, the analyser and the report can never disagree about
what the buckets are.

Taxonomy JSON shape:

    {
      "domain": "IT Service Desk",
      "categories": {
        "<L1 category>": {
          "assignment_group": "<team that handles it>",
          "subcategories": {
            "<L2 subcategory>": {
              "issues": { "<L3 issue type>": ["how a user phrases it", ...] },
              "simulation": { ... }        // optional, sample generation only
            }
          }
        }
      }
    }

The phrasings under each issue type are only needed when generating a sample dataset.
On a real export they are unused, so a taxonomy you write for a live desk can leave
them as empty lists.
"""

import json
from pathlib import Path

SEP = " > "


class TaxonomyError(ValueError):
    pass


def load(path):
    """Read a taxonomy file and check it before anything downstream depends on it."""
    data = json.loads(Path(path).read_text())
    validate(data)
    return data


def validate(data):
    """Fail loudly and specifically. A silently malformed taxonomy poisons every
    number in the report, so it is worth stopping here rather than debugging a
    strange chart three steps later."""
    if "categories" not in data or not isinstance(data["categories"], dict):
        raise TaxonomyError("Taxonomy needs a top-level 'categories' object.")
    if not data["categories"]:
        raise TaxonomyError("Taxonomy has no categories.")

    seen_paths, problems = set(), []
    for l1, cat in data["categories"].items():
        if SEP in l1:
            problems.append(f"Category name contains '{SEP}': {l1!r}")
        subs = cat.get("subcategories")
        if not isinstance(subs, dict) or not subs:
            problems.append(f"Category {l1!r} has no subcategories.")
            continue
        for l2, sub in subs.items():
            if SEP in l2:
                problems.append(f"Subcategory name contains '{SEP}': {l2!r}")
            issues = sub.get("issues")
            if not isinstance(issues, dict) or not issues:
                problems.append(f"Subcategory {l1} > {l2} has no issue types.")
                continue
            for l3 in issues:
                if SEP in l3:
                    problems.append(f"Issue type name contains '{SEP}': {l3!r}")
                p = f"{l1}{SEP}{l2}{SEP}{l3}"
                if p in seen_paths:
                    problems.append(f"Duplicate path: {p}")
                seen_paths.add(p)

    # A subcategory name reused under two different categories makes the L2 rollup
    # ambiguous, and the analyser groups on L1+L2 to survive it. Worth a warning
    # rather than an error, because sometimes it is genuinely intended.
    if problems:
        raise TaxonomyError("Taxonomy problems:\n  " + "\n  ".join(problems))
    return True


def leaves(data):
    """Yield (l1, l2, l3, phrasings, assignment_group, simulation) for every leaf."""
    for l1, cat in data["categories"].items():
        group = cat.get("assignment_group", "Service Desk")
        for l2, sub in cat["subcategories"].items():
            sim = sub.get("simulation", {})
            for l3, phrasings in sub["issues"].items():
                yield l1, l2, l3, list(phrasings or []), group, sim


def allowed_paths(data):
    """The exact strings the classifier is permitted to return."""
    return [f"{l1}{SEP}{l2}{SEP}{l3}" for l1, l2, l3, *_ in leaves(data)]


def split_path(path):
    parts = path.split(SEP)
    if len(parts) != 3:
        raise TaxonomyError(f"Path must have three levels: {path!r}")
    return parts


def counts(data):
    ls = list(leaves(data))
    return {
        "categories": len(data["categories"]),
        "subcategories": len({(l1, l2) for l1, l2, *_ in ls}),
        "issue_types": len(ls),
    }


def render_markdown(data):
    """A human-readable version, so reviewers argue with the taxonomy instead of the JSON."""
    c = counts(data)
    out = [
        f"# {data.get('domain', 'Ticket')} taxonomy",
        "",
        f"Three tiers. **{c['categories']} categories, {c['subcategories']} subcategories, "
        f"{c['issue_types']} issue types.**",
        "",
        "Generated from the taxonomy JSON, which is the source of truth. Edit the JSON, "
        "then regenerate this file.",
        "",
        "The classifier must return a path matching one of these rows character for "
        "character. Anything else is rejected rather than silently accepted.",
        "",
    ]
    if data.get("notes"):
        out += [data["notes"], ""]
    for l1, cat in data["categories"].items():
        out += [f"## {l1}", "",
                f"Handled by **{cat.get('assignment_group', 'Service Desk')}**.", "",
                "| Subcategory (L2) | Issue Type (L3) | What a user actually writes |",
                "|---|---|---|"]
        for l2, sub in cat["subcategories"].items():
            for i, (l3, ph) in enumerate(sub["issues"].items()):
                ex = f'"{ph[0]}"' if ph else "_add an example phrasing_"
                out.append(f"| {l2 if i == 0 else ''} | {l3} | {ex} |")
        out.append("")
    return "\n".join(out)


if __name__ == "__main__":
    import argparse
    ap = argparse.ArgumentParser(description="Validate a taxonomy and render it to Markdown.")
    ap.add_argument("taxonomy")
    ap.add_argument("--markdown", help="write the human-readable version here")
    a = ap.parse_args()
    d = load(a.taxonomy)
    c = counts(d)
    print(f"Valid. {c['categories']} categories, {c['subcategories']} subcategories, "
          f"{c['issue_types']} issue types.")
    missing = [f"{l1}{SEP}{l2}{SEP}{l3}" for l1, l2, l3, ph, *_ in leaves(d) if not ph]
    if missing:
        print(f"\n{len(missing)} issue types have no example phrasing. That is fine for a "
              f"real export, but sample generation needs them:")
        for m in missing[:10]:
            print(f"  {m}")
    if a.markdown:
        Path(a.markdown).write_text(render_markdown(d))
        print(f"\nWrote {a.markdown}")
