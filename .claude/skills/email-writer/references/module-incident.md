# Module: Own an incident, apologise, post-mortem

Use when something went wrong and the email has to say so: an outage, a missed date, a
wrong number sent to a client, a decision that backfired. Framework: Stone, Patton, and
Heen's *Difficult Conversations*, specifically the shift from blame to contribution.

## The three conversations running at once

Every hard message is heard on three tracks. Write for all three.

1. **What happened.** The facts, the timeline, the impact. Readers want this first and
   they want it precise.
2. **Feelings.** The reader is annoyed, worried, or embarrassed in front of their own
   stakeholders. One sentence that acknowledges the impact on them, not on you.
3. **Identity.** The reader is asking "does this mean I cannot rely on these people?"
   The answer is the fix and the prevention, stated concretely.

## Blame versus contribution

Blame asks "whose fault?" and produces defence. Contribution asks "what did each part of
the system do to get us here, and what changes?" and produces fixes. In the email:

1. Name your own contribution first and plainly. "I approved the scope without checking
   the API rate limits."
2. Describe other contributions as system facts, not as people's failures. "The staging
   environment does not mirror production rate limits" rather than "infra never set up
   staging properly".
3. Never name an individual as the cause in a group email. Roles and systems, not people.

## Structure

1. BLUF: what happened, who is affected, current status. "The Zoom recording sync failed
   for Pro users from 09:10 to 11:40 IST on 16-03-2026. Recordings are restored. No data
   was lost."
2. Impact on the reader, one or two sentences, specific.
3. What we know about the cause, stated as fact, with what we do not yet know marked as
   such. Never a guessed cause presented as certain.
4. What is fixed now, and what prevents recurrence, with an owner and a date for each.
5. What you need from the reader, if anything, or "nothing needed from you".
6. One line offering a call if they want more.

## Apology rules

1. Apologise once, early, specifically. "I am sorry the report went out with the wrong
   churn figure." Not "sorry for any inconvenience caused".
2. No "but". An apology followed by "but" is a defence.
3. No minimising ("a small glitch", "a minor delay"). The reader decides how big it was.
4. The apology is one sentence. The rest of the email is the fix.

## Anti-patterns

1. Passive voice to hide the actor ("mistakes were made").
2. Opening with context and reaching the incident in paragraph three.
3. Promising "this will never happen again". Promise the specific control instead.
4. A post-mortem that lists contributions of others and none of your own.

## Source

Douglas Stone, Bruce Patton, Sheila Heen, *Difficult Conversations*, 1999.
https://www.pon.harvard.edu/shop/difficult-conversations-how-to-discuss-what-matters-most/
