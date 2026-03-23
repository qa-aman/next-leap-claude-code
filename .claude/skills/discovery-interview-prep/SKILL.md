---
name: discovery-interview-prep
description: |
  Generate user research interview scripts using Mom Test principles. Use this skill when:
  - You are preparing for user interviews or pilot observation sessions
  - You need a question bank organized by behavior, context, pain points, and workflow
  - You want interview guides that avoid leading questions and hypotheticals
  - You need per-persona interview guides
  - You are preparing for field visits or pilot debriefs
---

# Discovery Interview Prep

Generate interview scripts grounded in Mom Test principles (Rob Fitzpatrick). Reads personas and current assumptions from specs, produces question banks and 1-page interview guides per persona type.

## Workflow

1. **Research goal** — Ask user: "What do you want to learn from these interviews?"
2. **Read personas** from your persona files or user research directory
3. **Read assumptions** — If a spec exists, read the Risks/Assumptions section for assumptions to validate
4. **Generate question bank** organized by category
5. **Generate interview guide** — 1-page per persona type
6. **Output** — Print to conversation or write to file

## Mom Test Rules

Core principles (Rob Fitzpatrick):
- Ask about their life, not your idea
- Ask about specifics in the past, not generics or hypotheticals
- Talk less, listen more
- Seek concrete facts, not compliments or opinions

## Question Categories

### Behavior — What they actually do
- "Walk me through the last time you [relevant activity]..."
- "What happened after [specific event]?"
- "How often does [situation] come up?"
- "Show me how you currently do [task]."

### Context — Environment and constraints
- "Where were you when you were doing this?"
- "What else was going on around you?"
- "What tools/devices were you using?"
- "Who else was involved?"

### Pain Points — Problems and frustrations
- "What's the hardest part about [activity]?"
- "Tell me about the last time that was frustrating..."
- "What have you tried to solve this? What happened?"
- "How much time/effort does this cost you?"

### Workflow — Process and sequence
- "What do you do first when you [start activity]?"
- "After [step], what happens next?"
- "Where does this process break down?"
- "What workarounds have you developed?"

### Questions to AVOID

These produce unreliable data:
- "Would you use a feature that does X?" (hypothetical)
- "Do you think X is a good idea?" (opinion, not behavior)
- "Would you pay for X?" (hypothetical)
- "How much would you pay?" (unreliable)
- "Is [problem] important to you?" (leading)
- Any question starting with "Would you..." or "Do you think..."
- "On a scale of 1-10..." (no context, no actionable data)

## Output Format

```markdown
# Interview Guide — {Feature/Research Area}

**Research Goal:** {what we want to learn}
**Date:** {DD-MM-YYYY}
**Duration:** {suggested minutes per interview}

## Assumptions to Validate

| # | Assumption | Source | Question to Ask |
|---|-----------|--------|----------------|
| 1 | {from spec} | {spec section} | {Mom Test question} |

---

## Interview Script: {Persona Type}

### Opening (2 min)
- Introduce yourself, explain purpose
- "We're here to learn from you, not to test you"
- "There are no right or wrong answers"

### Warm-up (3 min)
- {2-3 easy context-setting questions}

### Core Questions (15-20 min)

#### Behavior
1. {question}
2. {question}
3. {question}

#### Pain Points
1. {question}
2. {question}
3. {question}

#### Workflow
1. {question}
2. {question}

### Wrap-up (2 min)
- "Is there anything I didn't ask about that you think is important?"
- "Who else should I talk to about this?"

---

## Questions to Avoid
{list of anti-patterns specific to this research area}

## Observer Notes Template

| Time | Observation | Category | Follow-up? |
|------|------------|----------|-----------|
| | | Behavior/Pain/Context/Workflow | Y/N |
```

## Anti-Patterns

- Don't write leading questions disguised as open ones
- Don't ask hypotheticals — they produce unreliable data
- Don't skip the warm-up — it builds rapport
- Don't combine behavior and opinion questions in one

## Quality Checklist

- [ ] Every question is grounded in past behavior, not hypotheticals
- [ ] Questions are open-ended, not yes/no
- [ ] Each persona gets a tailored script
- [ ] Assumptions to validate are linked to spec sections
- [ ] Observer notes template is included
- [ ] No leading questions remain
