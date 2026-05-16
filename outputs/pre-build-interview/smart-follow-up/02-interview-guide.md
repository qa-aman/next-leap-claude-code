# Interview Guide - Smart Follow-Up

**Date:** 17-03-2026
**Duration:** 45 minutes
**Format:** Video call, recorded with consent

---

## Pre-interview checklist

- [ ] Confirm recording consent at the top.
- [ ] Have the user share their screen if they are willing. Behavioral observation beats reported behavior.
- [ ] Do NOT pitch Smart Follow-Up in the first 35 minutes. The feature reveal is the last 5 to 8 minutes only.
- [ ] Have a blank notes template open: `outputs/pre-build-interview/smart-follow-up/04-interviews/interview-NN.md`.

---

## Warmup (2 questions, 5 minutes)

These exist to relax the user and gather context. Do not skip.

**Q1.** "Walk me through what you do for work and what a typical day looks like for you."

**Q2.** "How many meetings did you have yesterday? Take me through them quickly."

*Why this works:* Anchors them in a real day, not a generalization. Surfaces meeting volume context for the rest of the interview.

---

## Past behavior (3 questions, 12 minutes)

The core of the interview. Every question is rooted in a specific past incident.

**Q3.** "Tell me about your last meeting yesterday. What happened after it ended?"

*Listen for:* Do they mention follow-ups unprompted? What was their next action? Did MeetFlow come up?

**Q4.** "Walk me through the last time you sent a follow-up email or message after a meeting. What did you do step by step, from the moment the meeting ended?"

*Probe:* "What tools did you have open?" "Did you use MeetFlow's summary? How?" "What did you change before sending?"

**Q5.** "Think about the last time an action item from a meeting got missed or went wrong. Tell me about it. What happened, and what did it cost you?"

*Listen for:* concrete cost (lost customer, missed deadline, redo work). Emotional signals (sigh, "ugh", "honestly"). Avoid generalizations.

---

## Current workaround (2 questions, 10 minutes)

**Q6.** "Show me, if you can, how you handle follow-ups today. Walk me through it on your screen."

*This is the commitment rung 2 question. Behavioral observation here is worth 5 stated opinions.*

**Q7.** "Before you used MeetFlow, what did you do? And what have you tried since that didn't stick?"

*Listen for:* graveyard of failed solutions. Strong signal of pull if they have actively searched. Weak signal if they have never tried anything else.

---

## Forces of progress (3 questions, 10 minutes)

Probe each force directly. See `.claude/skills/pre-build-interview/references/jtbd-forces.md`.

**Q8 (Push + Pull):** "If you could wave a magic wand and have the perfect post-meeting workflow, what would happen between the meeting ending and the follow-up being sent?"

*The only acceptable hypothetical in this guide. It surfaces pull without pitching.*

**Q9 (Habit):** "How long have you been doing follow-ups the way you do them now? Have you ever questioned the way you do it?"

*If they shrug or say "it's fine", that is dominant habit. Strong KILL signal.*

**Q10 (Anxiety):** "Imagine a tool drafted your follow-up email automatically using AI. What is the first thing that would worry you?"

*Listen specifically for: trust in accuracy, fear of sending something wrong to a customer or exec, data privacy, the AI hallucinating commitments that were not made.*

---

## Feature reveal (1 question + reactions, 5 to 8 minutes)

ONLY after Q10 is complete. Reveal the concept in one paragraph, then ask:

> "MeetFlow is exploring a feature where after each meeting, you would get a drafted follow-up email with the action items, each one labeled with a confidence score so you know which to double-check. You review it in 2 minutes and send via email, Slack, or push to Notion or Jira."

**Q11.** "What would have to be true for you to actually use this instead of your current workflow?"

*This is the closing question. Do NOT ask "would you use it" or "do you like it". Ask what conditions are required.*

*Probe on:* trust threshold ("how accurate would the action items need to be"), review behavior ("would you trust the confidence score or still check every item"), integrations ("which export channels matter most"), edge cases ("what would make you stop using it").

---

## Closing (1 question, 3 minutes)

**Q12.** "Who else do you know who runs as many meetings as you and might have the same pain? Would you be willing to introduce me?"

*Commitment rung 3. A real intro is worth more than any opinion they gave you in the previous 40 minutes.*

---

## Anti-questions (DO NOT ask)

These are the Mom Test failures. If they come up in the moment, rewrite live.

| Bad question | Why | Rewrite |
|---|---|---|
| "Would you use Smart Follow-Up?" | Pitches the feature, asks for hypothetical commitment. | "What would have to be true for you to switch from your current workflow?" |
| "How frustrating is it when action items are wrong?" | Leading. Embeds the answer. | "Tell me about the last time an action item was wrong. What happened?" |
| "Do you think confidence scores would help?" | Asks for opinion on hypothetical. | "Last time you reviewed an action item, how did you decide whether to trust it?" |
| "How much would you pay for this?" | Future commitment. Numbers will be inflated. | "What have you spent on solving this problem? Tools, time, anything." |
| "Do you wish MeetFlow was better at action items?" | Compliance bias - everyone says yes. | (Cut entirely. Use Q5.) |
