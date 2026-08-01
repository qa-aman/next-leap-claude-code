# What the report and the deck contain, and why

Two artifacts from the same numbers, for two different readers.

**The dashboard** is for the analyst. They want to explore, filter, and drill into a specific
ticket. It is self-contained HTML with the whole ticket set embedded, so filters recompute from
raw rows rather than from a pre-baked summary. That is what stops a filter changing a heading
but not the panel beneath it.

**The deck** is for the meeting. Nobody explores in a meeting and somebody has ten minutes to
decide. It is not a screenshot of the dashboard, it is the argument.

Both read from `metrics.py`, so they cannot disagree.

---

## Dashboard sections

### 1. Headline tiles
Volume, latest month versus previous, SLA met, agent-hours, reopen rate. Each carries a
subtitle with the working, so a number is never presented without its denominator.

### 2. Volume by category, month on month
Stacked bar, one bar per month, with a table twin. Categories are coloured in a fixed order
assigned once, so filtering never repaints a category the reader has already learned.

The month filter **highlights** here rather than slicing, because a month-on-month chart
filtered to a single month would say nothing. The subtitle states that, so the behaviour is not
a surprise.

### 3. Drill down
Category to subcategory to issue type to the actual tickets, showing the raw description, the
confidence badge and the classifier's reason. This is the section that makes the categorization
auditable instead of a black box, and it is usually the part a sceptical stakeholder goes to
first. Examples are sampled across the whole window rather than taken from the top, so the cards
do not all show the oldest month.

### 4. Automation shortlist
The management decision. Detailed below.

### 5. Where the agent hours go
A horizontal bar of agent-hours per month per subcategory. A different question from volume and
usually a different answer. Rows with fewer than 10 resolved tickets are faded and labelled
"small sample", because a median from five tickets moves a long way on one slow ticket.

### 6. SLA pressure
Subcategories with at least 10 resolved tickets, worst first. Status is an icon plus a word, not
a colour alone. The note reminds the reader that a long median can be a supplier or approval
wait rather than a performance problem, and that the owning team knows which.

### 7. Categorizer quality
The measured accuracy, in the report rather than a footnote, with its caveat. When there is no
answer key this section says "Not measured" and explains what to do about it. It never quietly
omits itself.

---

## Deck slides

| # | Slide | Job |
|---|---|---|
| 1 | Title | Names the period and states the ask up front |
| 2 | The month in five numbers | Headline tiles plus what moved |
| 3 | Where the tickets came from | The category table, growth coloured |
| 4 | The decision: what to automate | The shortlist with every check shown, plus near misses |
| 5 | Why this one | The evidence for the top candidate, and why spread is the point |
| 6 | Volume and effort are different questions | The effort ranking, small samples faded |
| 7 | Where service levels are slipping | SLA table, worst first |
| 8 | How the categories were assigned | The method and the measured accuracy, with its caveat |
| 9 | What we are asking for | Decision, review, explain, data |

Slide 9 is the point of the deck. Everything before it is evidence for the asks on it.

Run `ppt-builder/scripts/check_layout.py` afterwards. Exit 0 ships. Overlapping boxes render
unpredictably across PowerPoint versions even when the file that produced them looks fine.

---

## The automation shortlist rule

All three checks must pass.

| Check | Default | Why |
|---|---|---|
| Latest month volume | >= 12 tickets | Below this, automation costs more than it saves |
| Resolution spread, P90 minus P10 | <= 3 hours | The one that matters. A tight spread means the fix is nearly identical every time, which is what makes a process scriptable |
| P1 + P2 share | <= 25% | Routine work, not incident firefighting |

Override per run with `--min-tickets`, `--max-spread`, `--max-p1p2`.

Subcategories clearing two of three appear as **near miss**. Those are next cycle's candidates,
and showing them is what stops the shortlist looking arbitrary when it is short.

### Why it is not a weighted score

A score produces a ranking nobody can argue with, which sounds like a strength and is not. Three
visible thresholds with the actual value printed beside each one let a service owner say "12 is
too low for us" and re-rank it themselves. That conversation is the useful output.

### Three things to preserve

1. **It presents, it does not decide.** Name the owning team and the numbers. Raising the change
   request is the service owner's call. Framing it as an instruction reads as auditing another
   team's gaps, and it is also usually wrong, because the build cost is not in this data.
2. **Agent-hours are the floor.** Measured resolution time only, so triage, queue waiting and
   context switching are excluded. Say so wherever the number appears.
3. **Small samples stay visible and stay labelled.** Dropping them hides a real row. Leaving
   them unmarked invites a staffing decision built on noise. Fading and labelling is the honest
   middle.

---

## Reading trends honestly

With three months there are two comparisons. That is a direction, not a trend line, and both
artifacts say so when the window is three months or shorter. Six months is where a trend
becomes real, and extending the sample generator to six months is one flag.

When a category's share rises while total volume falls, the share is the finding and the count
is not. Both are shown for that reason.
