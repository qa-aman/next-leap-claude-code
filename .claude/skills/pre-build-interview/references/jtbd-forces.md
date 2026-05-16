# JTBD Forces of Progress

Source: Bob Moesta and Chris Spiek, popularized in *Demand-Side Sales* and *Competing Against Luck* (Christensen).

The core insight: a problem being real is not enough. Users adopt a new solution only when the forces pushing them toward change exceed the forces holding them in place. Many features die not because the problem was fake, but because habit and anxiety dominated push and pull.

## The four forces

```
        PUSH OF THE SITUATION
        (problems with status quo)
                  |
                  v
    HABIT ----- USER ----- PULL OF NEW SOLUTION
    (inertia)   |          (attraction of the new)
                  ^
                  |
        ANXIETY OF THE NEW
        (fears, risks, switching costs)
```

A user adopts when: **Push + Pull > Habit + Anxiety**.

## What each force looks like in interviews

### Push (forces toward change)

The pain of the current situation. Captured through past-incident questions.

Listen for:
- "I am wasting [X hours / dollars] every week on this"
- "Last time it cost me [specific bad outcome]"
- "My boss / customer / team is complaining about [specific issue]"
- Emotional signals: frustration, embarrassment, guilt, resignation

Weak push: "It would be nice if it was faster."
Strong push: "I lost a customer last month because I forgot the action item from our call."

### Pull (forces toward the new)

The attraction of a different future. Captured by asking what they have tried and what they wish for.

Listen for:
- "I have tried [X, Y, Z] looking for something that does..."
- "I keep hoping someone will just..."
- "When I saw [adjacent product], I thought maybe..."

Weak pull: "I guess that would be nice."
Strong pull: "I have been asking my team if we can build something internal to do exactly that."

### Habit (forces holding them in place)

The comfort of what they already do, even when it is bad.

Listen for:
- "I have been doing it this way for [years]"
- "It is fine, I am used to it"
- "Honestly I do not even notice anymore"
- Workarounds that have become invisible

Strong habit kills features. If users do not see their workaround as a problem, they will not switch even if your solution is better.

### Anxiety (fears about the new)

What could go wrong with switching.

Listen for:
- "I would worry that..."
- "What if the AI gets it wrong"
- "My team would have to learn another tool"
- "Last time I tried something like this..."
- Security, compliance, vendor lock-in, learning curve, accuracy concerns

For AI features, anxiety is usually the dominant blocker. Trust and accuracy concerns kill more AI features than weak push does.

## How to probe each force

Add these to the interview guide in Phase 4 of `references/mom-test.md` structure:

| Force | Question |
|---|---|
| Push | "Tell me about the last time [problem] happened. What did it cost you?" |
| Pull | "If you could wave a magic wand, what would the perfect version of [workflow] look like?" |
| Habit | "Walk me through how you handle this today. How did you start doing it this way?" |
| Anxiety | "What would have to be true for you to actually switch from [current solution]?" |

The magic wand question is the only acceptable hypothetical because it surfaces pull without pitching anything.

## Force mapping in Phase 5

For each interview, classify each force as Strong / Medium / Weak / Absent based on transcript evidence. Then aggregate across the sample:

```
| Interviewee | Push | Pull | Anxiety | Habit | Net |
|---|---|---|---|---|---|
| I-01 | Strong | Strong | Medium | Weak | Switch |
| I-02 | Medium | Weak | Strong | Strong | Stay |
| ... |
```

Net = Switch if Push + Pull clearly exceeds Anxiety + Habit. Otherwise Stay.

## Decision rules

- **Mostly Switch across the sample**: feature has a real chance. Proceed to BUILD if other thresholds also cleared.
- **Mostly Stay because of habit**: problem is tolerated. Most common reason features get built and ignored. Recommend KILL.
- **Mostly Stay because of anxiety**: problem is real but switching fear is high. Recommend ITERATE - the feature design needs to address the specific anxieties (trust, accuracy, learning curve, reversibility).
- **Mixed**: more interviews needed, or segment is too broad.

## AI-feature-specific anxieties to probe

For AI features in MeetFlow context, always probe these directly:

- "What would the AI have to get right for you to trust it?"
- "What would happen if it got [X] wrong - is that a small problem or a big one?"
- "How would you check whether the AI got it right? How much time would that take?"
- "Would you share [data type] with an AI? What is your team's policy?"
