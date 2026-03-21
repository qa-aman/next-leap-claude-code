# Guided Prompts - Claude Code for PMs

Work through these prompts one at a time. Each one builds on what you've learned. Copy-paste the prompt into Claude Code and watch what happens.

---

## Prompt 1: Orientation

**Prompt:**

```
What project is this and what's my role?
```

**What's happening:** Claude Code reads `CLAUDE.md` at the root of the project. This file loads automatically at the start of every conversation - it tells Claude who you are, what you own, and how the workspace is organized. Think of it as your project's always-on briefing doc. You didn't point Claude to any file - it already knew where to look.

---

## Prompt 2: Single File Read

**Prompt:**

```
Read 03-product-knowledge/competitive.md and tell me where MeetFlow is most at risk
```

**What's happening:** Claude opens one specific file, reads it top to bottom, and synthesizes. This is the simplest useful pattern - point Claude at a file, ask a question. Notice it doesn't just summarize. It ranks threats and explains why. The answer should surface that Notion AI is rated an "existential" threat to the free tier - language much stronger than the other competitors.

---

## Prompt 3: Multi-File Synthesis

**Prompt:**

```
Read all files in 07-user-interviews/ and identify the top 3 user frustrations
```

**What's happening:** Claude reads 4 interview transcripts (Sarah Chen, Marcus Okafor, Priya Nair, James Whitfield) and finds patterns across them. This is where Claude Code starts saving you real time - manually reading and synthesizing 4 interviews takes 30-45 minutes. Watch for whether Claude picks up that each person is frustrated about something different: accuracy, privacy, price, and integrations.

---

## Prompt 4: Cross-Reference Discovery

**Prompt:**

```
Read 05-user-personas/ and 07-user-interviews/. Is there anyone mentioned in the interviews who doesn't have a persona file?
```

**What's happening:** Claude reads two directories and compares them. The personas folder has Sarah, Marcus, and Priya. But the interviews folder has a fourth person - James Whitfield, a Sales Director with 22 Team seats ($12,936/yr). He's evaluating Fireflies as a replacement and has a Q1 2026 decision deadline. Claude found a gap in your documentation by cross-referencing two sources. This is the kind of blind spot that's easy to miss when files live in different folders.

---

## Prompt 5: Numbers That Tell a Story

**Prompt:**

```
Read 06-user-feedback/feedback-q1-2026.md. NPS went from 22 to 34. What caused the jump, and what's the biggest thing holding NPS back from reaching 45?
```

**What's happening:** Claude reads the feedback survey and connects it to what it already knows from `CLAUDE.md` (which loaded the company overview and product vision automatically). The NPS jump maps to Smart Summaries v2.4 shipping in November 2025. The blocker to 45 is action item accuracy - 19 of 47 respondents flagged it. Claude is threading together a feedback file, a release, and a target number from the OKRs without you telling it to.

---

## Prompt 6: Deadline Risk Detection

**Prompt:**

```
The PRD says Smart Follow-Up ships in April 2026. Read 11-sprint/sprint-backlog-2026-03-17.md and 11-sprint/retro-2026-03-10.md. Is April still realistic?
```

**What's happening:** Claude reads the PRD, the current sprint backlog, and the previous sprint retro - then does the math. The sprint backlog shows 3 model retraining tasks that haven't started yet. The retro reveals the team completed only 74% of committed points last sprint (31 of 42). The retro also has a hard decision: cap at 32 story points until two clean sprints. But the current sprint has 36 points loaded. Claude is spotting a schedule risk by combining a target date, current velocity, and a policy decision that contradicts the plan.

---

## Prompt 7: The Revenue Question

**Prompt:**

```
Read Sarah Chen's persona and interview. She said she'd move her whole team to the Team plan. How much revenue is that worth, and what's blocking it?
```

**What's happening:** Claude reads two files about the same person and does the revenue math. Sarah has a team of 8. Team plan is $49/seat/month. That's $4,704/year in blocked upgrade revenue. The blocker is action item accuracy - she estimates 2-3 errors per day, costing 30 minutes of manual correction. She won't upgrade until she trusts the AI. Claude connected a qualitative complaint to a dollar amount without being told the pricing - it pulled that from the company overview.

---

## Prompt 8: Stakeholder Prep

**Prompt:**

```
Read 10-meetings/stakeholder-sync-2026-03-14.md and 12-project-tracking/status-report-2026-03-14.md. If I'm walking into a stakeholder meeting today, what are the 3 questions I should be ready to answer?
```

**What's happening:** Claude reads the last stakeholder sync and the latest status report, then anticipates what leadership will ask next. It knows the CEO asked about Smart Follow-Up risk last time. VP Sales asked if accuracy is losing deals. VP Eng asked about manual retraining. Claude uses the pattern of previous questions plus current status (Action Item Scoring v2 is Yellow) to predict follow-up questions. This is Claude acting as your meeting prep partner - not just reading notes, but thinking ahead.

---

## Prompt 9: Write a Real Artifact

**Prompt:**

```
Read 07-user-interviews/interview-04-james-whitfield.md. James doesn't have a persona file yet. Create one at outputs/persona-james-whitfield.md using the same format as 05-user-personas/sarah-chen.md.
```

**What's happening:** Claude reads the interview transcript, reads an existing persona as a format template, and writes a new file. It extracts James's role (Sales Director), team size (22 seats), pain points (no Salesforce integration), risk level (HIGH - actively evaluating Fireflies), and revenue impact ($12,936/yr at risk). This is the pattern for turning raw research into structured artifacts - give Claude a source and a template, and it produces a draft that matches your existing format.

---

## Prompt 10: The Hard Strategic Question

**Prompt:**

```
Read 03-product-knowledge/competitive.md, 05-user-personas/priya-nair.md, and 07-user-interviews/interview-03-priya-nair.md. Is MeetFlow's free tier defensible against Notion AI? Be honest.
```

**What's happening:** Claude reads the competitive landscape, Priya's persona, and her interview - then gives you a straight answer. Priya never opens the MeetFlow app. Her entire experience is the Slack digest. She said she'd check out Notion's meeting features when they launch. She wants to pay $8/month, not $15. The competitive file rates Notion AI as an "existential" threat to the free tier. Claude synthesizes all of this into a strategic assessment. Three files, one uncomfortable conclusion. This is Claude Code at its most useful - not telling you what you want to hear, but connecting dots across your own data to surface what you need to know.

---

## What You Just Learned

| Prompt | Skill |
|--------|-------|
| 1 | CLAUDE.md loads context automatically |
| 2 | Point at a file, ask a question |
| 3 | Read multiple files, find patterns |
| 4 | Cross-reference directories to find gaps |
| 5 | Connect numbers across files to tell a story |
| 6 | Combine dates, velocity, and decisions to spot risk |
| 7 | Turn qualitative feedback into revenue impact |
| 8 | Use past meetings to prep for the next one |
| 9 | Generate artifacts using a source + template |
| 10 | Synthesize strategy from scattered data |

Each prompt added one new capability. By Prompt 10, you were doing in 30 seconds what would take a PM an hour of reading and thinking across files.
