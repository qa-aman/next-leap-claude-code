# User Stories - Smart Follow-Up Emails

These stories break down the PRD into buildable pieces (discrete, shippable units of work). Each story maps to a specific persona and a specific part of the feature. Engineers use these to scope tasks. PMs use them to track progress.

PRD reference: `08-product-features/prd-smart-follow-ups.md`

---

## Stories

---

**Story 1 - Draft generation**
As Sarah Chen (Head of Product), I want a follow-up email drafted automatically after each meeting, so that I don't spend time writing summaries for 8-10 meetings per day.

Acceptance criteria:
- [ ] A draft appears in the dashboard within 2 minutes of a meeting ending.
- [ ] The draft includes a subject line, a 3-5 sentence summary, and a bulleted action item list.
- [ ] The draft is generated only when a summary and at least one action item exist.

---

**Story 2 - Confidence score flagging**
As Sarah Chen, I want low-confidence action items flagged visually in the draft, so that I know exactly what to review before sending.

Acceptance criteria:
- [ ] Action items below 75% confidence are highlighted (yellow) in the review screen.
- [ ] Each item shows its confidence score as a percentage next to it.
- [ ] I can edit, delete, or approve any item individually before sending.

---

**Story 3 - Explicit send approval**
As Marcus Okafor (Engineering Manager), I want to review and approve every draft before it sends, so that no email leaves on my behalf without my explicit action.

Acceptance criteria:
- [ ] No draft is sent automatically. A "Send" button requires a deliberate click.
- [ ] The review screen shows the full email body before I confirm.
- [ ] A sent confirmation and timestamp are logged to the meeting record.

---

**Story 4 - Slack export**
As Priya Nair (Chief of Staff), I want to post the follow-up draft to a Slack channel instead of sending an email, so that I can share meeting outcomes where my team already works.

Acceptance criteria:
- [ ] An "Export to Slack" option appears on the review screen alongside "Send Email".
- [ ] I can choose which Slack channel to post to before confirming.
- [ ] The Slack message matches the email draft content (summary + action items).

---

**Story 5 - Jira/Linear task creation**
As Marcus Okafor, I want action items from the draft exported directly to Jira or Linear (project management tools), so that tasks land in our backlog without manual re-entry.

Acceptance criteria:
- [ ] Each action item has a checkbox to include or exclude it from the export.
- [ ] Exported tasks include the action item text, the meeting date, and a link to the MeetFlow meeting record.
- [ ] Export works for both Jira and Linear. Only one can be selected per meeting.

---

**Story 6 - Casual-user entry point**
As Priya Nair, I want to access the follow-up draft from the Slack digest MeetFlow already sends me, so that I don't have to open the MeetFlow dashboard to use the feature.

Acceptance criteria:
- [ ] The Slack digest includes a "Review Draft" link that opens the draft review screen directly.
- [ ] The link is available for 48 hours after the meeting ends.
- [ ] If I haven't opened a draft after 48 hours, MeetFlow sends a single reminder via Slack.
