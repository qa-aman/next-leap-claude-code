# Experiment brief (the simulated PM's knowledge)

## The idea (given to both arms, word for word)

A web app where my team pastes meeting notes and gets a list of action items with owner and due date. The team sees all open items on one board and ticks them off. It works when every action item from a meeting shows up with the right owner, and nobody has to retype them.

## What the PM knows (answer sheet). Reveal only when asked.

R1. Team: 8 people on a product team at a 60-person startup. Roster: Priya, Marcus, Sarah, Tomás, Aisha, Dana, Ravi, Lena.
R2. Notes are pasted text from Google Docs or Zoom transcripts, 500 to 15,000 words each. About 10 meetings a week.
R3. Some notes mix Hindi and English (Hinglish).
R4. Names in notes can be nicknames ("Tom" is Tomás). An owner who is not on the roster must be flagged, never guessed.
R5. Relative due dates ("by next Friday", "EOD tomorrow") are resolved against the meeting date. No date mentioned means "no due date", never an invented one.
R6. Accuracy matters most. The current tool gets 34% of action items wrong or missing, which is why we are building this. Prefer a "needs review" flag over a wrong item.
R7. Privacy: raw notes are deleted after 30 days. Only the action items are kept.
R8. Login: Google sign-in, restricted to the company's Google Workspace domain. Must have, notes are confidential.
R9. Board: filter by owner and by meeting, overdue items highlighted, tick an item to mark it done.
R10. Editing: an owner can edit an item's text, owner, or due date. Keep a record of who changed it.
R11. Weekly Slack digest every Monday 9am IST. Nice to have, v2, not v1.
R12. Budget: under $20 a month total, including AI costs. Free-tier hosting preferred.
R13. The builder is a non-technical PM who will build with Claude Code and wants a URL the team can open.
R14. Timeline: a usable v1 in 2 weeks.
R15. Out of scope: calendar integration, audio recording, mobile app, Jira sync.
R16. The same action item said in two meetings should not show up twice. Nice to have.

Tech preferences: none. If asked, say "no preference, recommend what fits".
