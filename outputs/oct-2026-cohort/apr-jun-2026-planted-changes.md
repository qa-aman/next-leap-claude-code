# Apr-Jun 2026 export: planted changes

Created 17-10-2026. Source: `servicenow-tickets-apr-jun-2026.xlsx`.

This file is the test answer for the Q2 report. Keep it away from the classifier: it names the trends the report should find on its own.

## How the file was made

- Generated with the `ticket-category-analysis` sample generator, same taxonomy as Jan-Mar, new random seed.
- 521 tickets: April 165, May 172, June 184.
- Ticket IDs run from INC1046575 to INC1047637, after the Jan-Mar file, so the two never clash.
- Same three sheets and columns as `servicenow-tickets-2026.xlsx`. Categories are blank, and the Answer Key holds the true categories.

## The three planted changes

| # | Change | Jan-Mar (true labels) | Apr-Jun (true labels) | What the report should show |
|---|---|---|---|---|
| 1 | VPN surge, and more of it urgent | 9, 7, 11 a month | 11, 13, 39 a month | Network & Connectivity is the top mover in June, led by VPN |
| 2 | Password self-service works from May | 20, 30, 38 a month | 35, 21, 15 a month | Password falls. It may drop off the automation shortlist |
| 3 | P1 SLA fixed | 4 of 11 P1 met SLA | 6 of 7 P1 met SLA | The Risk pointer no longer flags P1 as the worst gap |

Overall SLA stays flat: 83.8% in Jan-Mar, 83.4% in Apr-Jun.

## Unchanged

- `servicenow-tickets-2026.xlsx` (Jan-Mar) was not edited. The published report is built from it.
