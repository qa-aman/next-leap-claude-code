# The classification contract

Read this before classifying a batch. The rules are short, and each one exists because breaking
it produces a specific, believable, wrong number.

## The output

One JSON object per line, appended to `work/classified.jsonl`. Nothing else in the file.

```json
{"case_id":"C001","path":"Access & Identity > Password > Password reset","confidence":"High","reason":"User forgot credentials and needs them reset."}
```

| Field | Rule |
|---|---|
| `case_id` | Exactly as it appears in the batch. One line per case, no duplicates, none skipped |
| `path` | Matches an allowed path character for character, or the literal `UNCATEGORIZED` |
| `confidence` | `High`, `Medium`, or `Low` |
| `reason` | One short line a service desk manager could read and agree or disagree with |

`apply_classification.py` rejects the run on a missing case, a duplicate, or an invented path.
That is deliberate. A category that exists only in the output file is worse than a crash,
because it appears in the report as a real bucket.

## What the classifier sees, and what it must not

**Sees:** the description, the short description, and the departments and channels that case
appeared in.

**Does not see: `Assignment Group`.** In most exports the group maps almost one to one onto the
category, because the desk already routed the ticket. Feeding it in means the classifier is
reading the answer off the routing rather than the text, and the accuracy score becomes a
measure of nothing. If you ever add a field, ask first whether it already encodes the answer.
Resolution notes, resolver team, and category-derived tags all fail that test.

The same caution applies to a real export that already has a partially filled category column.
Exclude it, or you are scoring the classifier against its own input.

## Judge only from what the user wrote

Do not infer a system, a team, or a cause that is not in the text. "cannot log in" is not an
Active Directory ticket unless the user said so. The report drills down to the raw description
beside your reason, so a reason that describes something the ticket never said is visible to
whoever reads it, which is the point of showing it.

## Never force a fit

If nothing matches, return `UNCATEGORIZED` with `Low` confidence. A forced fit disappears into
a volume number where nobody will ever find it, and it corrupts the trend for a bucket that did
not deserve it. An honest gap sits in the review queue where somebody deals with it.

A cluster of `UNCATEGORIZED` cases is a useful signal in its own right: it usually means the
taxonomy is missing a bucket that the desk actually has.

## Confidence is a real signal, so use the range

`Medium` and `Low` route to the review queue, which is what a human clears before the report is
published. Marking everything `High` because the answer looks plausible removes the only
mechanism that catches the near-misses.

| Band | Use when |
|---|---|
| `High` | The text names the problem. A second reader would pick the same bucket |
| `Medium` | The bucket is a reasonable read but another is defensible. Two subcategories genuinely compete |
| `Low` | You are guessing, or the description is too vague to place. A human must decide |

Vague short descriptions are normal and are not by themselves a reason for low confidence.
"Please assist" as the short description with a clear long description is still `High`. Reserve
`Low` for cases where the actual complaint is unclear.

## Batching

Batches hold up to 40 cases. Work through them in order and append as you go rather than
holding everything to the end, so a long run does not lose completed work.

Cases are sorted with the highest ticket counts first, so the first batch carries the most
weight. Case C001 covering 35 tickets matters 35 times more than a case covering one.

## After the run

`apply_classification.py` prints, per confidence band, how often that band was right. If
`High` is not clearly more accurate than `Medium`, the confidence signal is not being used
properly and the review queue is not pointing at the right tickets.

It also lists every distinct description that landed in the wrong subcategory. Read that list.
It usually shows one of three things, and the fix differs:

1. **Two buckets that genuinely overlap.** Fix the taxonomy, not the classifier.
2. **A phrasing that is ambiguous to any reader.** Correct behaviour, and it belongs in the
   review queue rather than in a rule.
3. **A rule that was applied inconsistently across batches.** Fix the reading and rerun.
