# Service desk ticket analysis, Jan to Mar 2026

One page for management. The full detail is in the interactive dashboard at
`report/ticket-analysis-dashboard.html`. Every number below comes from
`data/categorized-tickets.xlsx`.

---

## The one decision this report asks for

**Password resets should become a self-service flow, raised as a change request.**

1. Password is **88 of 450 tickets**, which is **19.6%** of everything the desk received.
2. It ran **20 in January, 30 in February, 38 in March**. That is **90% growth** in three months.
3. It resolves in **0.78 hours** median, with a spread of only **0.46 hours** between the fastest
   and slowest tenth.
4. Only **4.5%** are P1 or P2. These are routine, not incidents.
5. **42%** already arrive through the self-service portal, so the front door is already built.

The tight spread is the part that matters. A spread of 0.46 hours means the fix is nearly the same
every single time, which is what makes a process scriptable. A category with the same volume but a
40 hour spread would not be automatable, because each ticket needs a different judgement.

**What it gives back:** at least **22.8 agent-hours a month**. That is measured resolution time
only. It excludes triage, queue waiting and context switching, so treat it as the floor and not the
full number.

The call on whether to raise the change request sits with the service owner. This report gives the
numbers, not the decision.

---

## What the inflow looks like

Total volume grew from **140 to 150 to 160** across the three months, which is **14% up** from
January to March.

| Category | Jan | Feb | Mar | Total | Share |
|---|---:|---:|---:|---:|---:|
| Access & Identity | 40 | 39 | 59 | 138 | 30.7% |
| Software & Applications | 33 | 27 | 30 | 90 | 20.0% |
| Hardware | 22 | 29 | 27 | 78 | 17.3% |
| Network & Connectivity | 18 | 21 | 16 | 55 | 12.2% |
| Email & Collaboration | 19 | 20 | 15 | 54 | 12.0% |
| Security & Compliance | 8 | 14 | 13 | 35 | 7.8% |

**Access & Identity is the whole story of the growth.** It jumped from 39 in February to 59 in
March, and it is now nearly a third of the desk. Every other category is flat or down. So the desk
is not getting busier in general, it is getting busier in one place.

One caution on reading this table. Three months gives only two deltas. Read the arrows as a
direction, not as a trend line. If we extend the dataset to six months, the trend becomes real.

---

## Where the hours actually go

Volume and effort are different questions, and they give different answers.

| Subcategory | Tickets | Median hrs | Agent-hrs / month |
|---|---:|---:|---:|
| Laptop | 26 | 18.4 | 238.2 |
| Licensing | 26 | 17.2 | 174.7 |
| CRM System | 14 | 13.8 | 81.8 |
| Peripherals | 25 | 7.6 | 71.0 |
| ERP System | 21 | 7.7 | 68.5 |

Password is the biggest by count and one of the smallest by hours. Laptop is the reverse: 26 tickets
that eat **238 agent-hours a month**. Both are real problems, but they need different answers.
Password needs automation. Laptop needs a look at why a single ticket takes 18 hours.

Two rows in the dashboard are marked as a small sample. Data Access Control shows 170 agent-hours a
month off **5 resolved tickets**, which is one slow ticket away from looking completely different.
It is on the chart, faded and labelled, so nobody builds a plan on it.

---

## Where SLA is breaking

Overall SLA met is **83.8%**. Two subcategories are at half.

| Subcategory | SLA met | Breached | Median hrs | Handled by |
|---|---:|---:|---:|---|
| Laptop | 50.0% | 13 of 26 | 18.4 | Desktop Support |
| Licensing | 50.0% | 13 of 26 | 17.2 | Application Support |
| CRM System | 64.3% | 5 of 14 | 13.8 | Application Support |
| ERP System | 71.4% | 6 of 21 | 7.7 | Application Support |

Licensing is worth a question rather than a conclusion. A licence request is a procurement wait, not
an engineering fix, so the 17 hour median may be a supplier lead time sitting inside our SLA clock.
The team that owns the licensing process will know whether the SLA target is the wrong target here.
That call is theirs.

---

## How the categories were assigned

The tickets arrive with a free-text description and no category. A person had to read each one and
pick a bucket. That is the manual work this workflow removes.

1. The three tier taxonomy is fixed up front, in `taxonomy.md`. **6 categories, 25 subcategories,
   46 issue types.**
2. Descriptions are normalised and deduplicated first. 450 tickets collapsed to **127 unique cases**,
   which cut the classification work by **71.8%**.
3. Claude reads the description, the short description, the department and the channel, then assigns
   all three levels with a confidence rating and a one line reason.
4. Assignment Group is deliberately **not** shown to the classifier, because in this dataset it maps
   one to one onto a category and would hand over the answer.
5. Anything rated Medium or Low goes to a review queue rather than being forced into a bucket.
   **110 tickets** are flagged that way.

**Measured accuracy against the held back answer key: 100% at category, 100% at subcategory,
98.4% at issue type.**

**Read that number for what it is.** These are sample tickets built to design and test the workflow,
so the descriptions were written from the same taxonomy the classifier was scored against. The
number proves the pipeline runs end to end. It is **not** a forecast of how it scores on the real
queue. To get the real number, hand label a few hundred live tickets and run the same answer key
check. The workflow keeps that step in, which is the point of building it this way.

---

## What to look at next

1. Ask why Access & Identity jumped 20 tickets in March. A password policy change, a system
   migration or a new joiner batch would all explain it, and the answer changes what we do.
2. Take the Laptop SLA to Desktop Support. 13 of 26 breaching at an 18 hour median is a process
   question, not a capacity question.
3. Extend the dataset to six months so the direction becomes a trend.
4. Run the answer key check on real hand labelled tickets before trusting the categorizer on live
   data.

---

**Source files.** Raw tickets: `data/servicenow-tickets-jan-mar-2026.xlsx`.
Categorized output and review queue: `data/categorized-tickets.xlsx`.
Computed metrics: `data/metrics.json`. Accuracy: `data/accuracy.json`.
Method: `WORKFLOW.md`.

This is a sample dataset created to design and test the workflow. The numbers are not live service
desk data.
