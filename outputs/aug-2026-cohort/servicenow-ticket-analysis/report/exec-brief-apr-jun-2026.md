# Service desk ticket analysis, April to June 2026

One page for management. Run on 01-08-2026.

Full detail is in the interactive dashboard at `report/ticket-analysis-dashboard-apr-jun-2026.html`.
Every number below comes from `data/categorized-apr-jun-2026.xlsx`. The previous cycle is in
`report/exec-brief.md` (January to March 2026).

---

## The one decision this report asks for

**Password resets should become a self-service flow, raised as a change request.**

This is the same finding as last quarter, and it got bigger.

1. Password is **110 of 522 tickets**, which is **21.1%** of everything the desk received.
2. It ran **28 in April, 33 in May, 49 in June**. That is **75% growth** across the quarter.
3. It resolves in **0.72 hours** median, with a spread of only **0.50 hours** between the fastest
   and slowest tenth.
4. Only **10.0%** are P1 or P2. This is routine work, not incident firefighting.
5. **43.6%** already arrive through the self-service portal, so the front door already exists.

The tight spread is the part that matters. A spread of 0.50 hours means the fix is nearly identical
every time, which is what makes a process scriptable. A category with the same volume and a 40 hour
spread would not be automatable, because each ticket would need a different judgement.

**What it gives back: at least 27.2 agent-hours a month.** That is measured resolution time only.
It excludes triage, queue waiting and context switching, so treat it as the floor and not the full
number.

Password sits with IAM Support. The call on raising the change request is the service owner's. This
report gives the numbers, not the decision.

---

## What the inflow looks like

Volume grew from **165 to 172 to 185** across the three months. That is **12.1% up** from April to
June, and **+7.6%** in the latest month alone.

| Category | Apr | May | Jun | Total | Share | Agent-hrs / month |
|---|---:|---:|---:|---:|---:|---:|
| Access & Identity | 51 | 50 | 71 | 172 | 33.0% | 125.3 |
| Software & Applications | 25 | 33 | 33 | 91 | 17.4% | 431.4 |
| Hardware | 28 | 30 | 29 | 87 | 16.7% | 383.7 |
| Email & Collaboration | 28 | 23 | 25 | 76 | 14.6% | 116.9 |
| Network & Connectivity | 26 | 19 | 17 | 62 | 11.9% | 220.1 |
| Security & Compliance | 7 | 17 | 10 | 34 | 6.5% | 143.1 |

**Access & Identity is again the whole story of the growth.** It jumped 21 tickets in June and is now
a third of the desk. Network & Connectivity is down 34.6% across the quarter. Everything else is flat.

---

## Six months, now that we have them

Last quarter's brief asked for six months so the direction becomes a trend. We have it now.

| Category | Q1 total | Q2 total | Change |
|---|---:|---:|---:|
| Access & Identity | 138 | 172 | +24.6% |
| Email & Collaboration | 54 | 76 | +40.7% |
| Network & Connectivity | 55 | 62 | +12.7% |
| Hardware | 78 | 87 | +11.5% |
| Software & Applications | 90 | 91 | +1.1% |
| Security & Compliance | 35 | 34 | -2.9% |
| **Total** | **450** | **522** | **+16.0%** |

Password alone went from **88 tickets in Q1 to 110 in Q2**, and from 20 in January to 49 in June.
Across six months that is a real trend, not two deltas. It is the single clearest signal in the data.

One caution. Q1 and Q2 were classified in two separate runs against the same fixed taxonomy, so the
buckets are comparable. The taxonomy did not change between the runs.

---

## Where the hours actually go

Volume and effort are different questions, and they give different answers.

| Subcategory | Tickets | Median hrs | Spread (P90-P10) | Agent-hrs / month |
|---|---:|---:|---:|---:|
| Laptop | 38 | 18.6 | 38.5 | 264.2 |
| ERP System | 24 | 8.1 | 56.4 | 170.0 |
| Licensing | 14 | 34.4 | 46.3 | 165.2 |
| Peripherals | 24 | 7.0 | 19.4 | 78.5 |
| WiFi | 19 | 8.6 | 22.9 | 75.5 |

Password is the biggest by count and one of the smallest by hours, at 27.2 a month. Laptop is the
reverse: 38 tickets that eat **264 agent-hours a month**. Both are real problems and they need
different answers. Password needs automation. Laptop needs someone to ask why a single ticket takes
18 hours.

**10 subcategories are marked small sample** in the dashboard. Audit and Review posts 73.5 agent-hours
a month off **6 resolved tickets**, which is one slow ticket away from looking completely different.
Those rows stay on the chart, faded and labelled, so nobody builds a staffing plan on them.

---

## Where SLA is breaking

Overall SLA met is **87.0%**, up from 83.8% last quarter. Reopens rose from 3.9% to **6.3%**.

| Subcategory | SLA met | Median hrs | Reopened | Handled by |
|---|---:|---:|---:|---|
| Laptop | 48.6% | 18.6 | 10.8% | Desktop Support |
| Licensing | 53.8% | 34.4 | 7.7% | Application Support |
| WiFi | 68.4% | 8.6 | 5.3% | Network Operations |
| ERP System | 69.6% | 8.1 | 8.7% | Application Support |

Licensing is worth a question rather than a conclusion. A licence request is a procurement wait, not
an engineering fix, so the 34 hour median may be a supplier lead time sitting inside our SLA clock.
The team that owns the licensing process will know whether the SLA target is the right target here.
That call is theirs.

Two observations worth putting in front of the owning teams rather than resolving here.

1. **Laptop volume fell from 17 in May to 5 in June** while Peripherals rose from 4 to 13. Desktop
   Support will know whether that is a real shift in what users are raising or a change in how the
   two are being logged.
2. **VPN reopens are at 14.3%**, the highest of any subcategory. A reopen means the first fix did not
   hold, so this is a quality question for Network Operations, not a volume one.

---

## The automation shortlist, and the rule behind it

A subcategory reaches the shortlist only by clearing all three checks. The rule is stated in the open
and there is no hidden weighting, so anyone can disagree with a threshold and re-rank it.

1. At least **12 tickets** in the latest month.
2. Resolution-time spread (P90 minus P10) of **3 hours or less**.
3. No more than **25%** P1 or P2.

**Cleared all three: Password.** 49 tickets in June, 0.50 hour spread, 10.0% P1 or P2.

**Cleared two of three, all failing on spread:** Peripherals (78.5 agent-hrs/month), Account
Provisioning (69.1), Office Productivity Suite (46.2), Mail Client (30.2). These have the volume and
they are routine, but the work varies too much per ticket to script as it stands. They are the right
place to look next quarter if any of them can be narrowed into a tighter sub-flow.

---

## How the categories were assigned

The tickets arrive with a free-text description and no category. A person had to read each one and
pick a bucket. That is the manual work this workflow removes.

1. The three tier taxonomy is fixed up front, in `taxonomy.md`. **6 categories, 25 subcategories,
   46 issue types.** It did not change from the Q1 run.
2. Descriptions are normalised and deduplicated first. 522 tickets collapsed to **126 unique cases**,
   which cut the classification work by **75.9%**.
3. Claude reads the description, the short description, the department and the channel, then assigns
   all three levels with a confidence rating and a one line reason.
4. Assignment Group is deliberately **not** shown to the classifier. In this dataset it maps almost
   one to one onto a category, so feeding it in would hand over the answer.
5. Anything rated Medium or Low goes to a review queue rather than being forced into a bucket.
   **122 tickets** are flagged that way. **0 tickets** came back uncategorized.

**Measured accuracy against the held back answer key: 99.4% at category, 99.4% at subcategory,
98.1% at issue type.**

The confidence signal did its job. High confidence scored **100.0%** at subcategory across 400
tickets. The only subcategory misses were 3 cases, all flagged Medium, all the same complaint:
"keeps disconnecting during calls". That reads as a meetings problem and is actually a VPN problem.
It landed in the review queue, which is exactly where an ambiguous ticket should land.

**Read the accuracy number for what it is.** These are sample tickets built to design and test the
workflow, so the descriptions and the answer key came from the same taxonomy. The number proves the
pipeline runs end to end. It is **not** a forecast of how it scores on a live queue. To get the real
number, hand label 200 to 300 live tickets into an Answer Key sheet and run the same check.

---

## What to look at next

1. Take the Password trend to IAM Support. Six months of growth from 20 to 49 a month is now a trend,
   and the self-service portal already carries 43.6% of the volume.
2. Ask Desktop Support about the Laptop SLA. Under half meeting target at an 18.6 hour median is a
   process question, not a capacity question.
3. Ask Network Operations about the 14.3% VPN reopen rate.
4. Try to narrow one of the four near-miss subcategories into a tighter sub-flow with a smaller
   spread. Peripherals carries the most hours of the four.
5. Run the answer key check on real hand labelled tickets before trusting the categorizer on live
   data.

---

**Source files.** Raw tickets: `data/servicenow-tickets-apr-jun-2026.xlsx`.
Categorized output, accuracy sheet and review queue: `data/categorized-apr-jun-2026.xlsx`.
Case answers: `work-apr-jun/classified.jsonl`. Accuracy: `work-apr-jun/accuracy.json`.
Dashboard: `report/ticket-analysis-dashboard-apr-jun-2026.html`.
Deck: `report/Service-Desk-Ticket-Analysis-Apr-Jun-2026.pptx`.
Previous cycle: `report/exec-brief.md` and `data/categorized-tickets.xlsx`.
Method: `WORKFLOW.md` and the `ticket-category-analysis` skill.

This is a sample dataset created to design and test the workflow. The numbers are not live service
desk data.
