# Module: Raise a concern, give feedback, flag a miss

Use when the email has to tell someone that something in their work, plan, or behaviour
needs to change, and you need them to hear it rather than defend against it. Two
frameworks that share one idea: facts flat, interpretation tentative, request specific.

## Crucial Conversations: STATE

1. **Share your facts.** What you observed, with the artifact: the line, the number, the
   screenshot, the date. Facts are the least controversial thing you can open with.
2. **Tell your story.** Your interpretation, clearly marked as yours. "What I read from
   this is..." or "My concern is that...".
3. **Ask for their path.** Invite their facts and their story. "You will know if I have
   missed context here."
4. **Talk tentatively.** The story is hedged, the facts are not. "The number is missing"
   is a fact, stated flat. "I think this will cause QA to guess" is a story, stated
   tentatively.
5. **Encourage testing.** Make it safe to disagree: "If you see it differently, tell me,
   I would rather be corrected now than after dev starts."

## NVC: OFNR, the four-line skeleton

Rosenberg's sequence for anything the reader might take personally.

1. **Observation.** What happened, without evaluation. "The spec has no default limit
   value" not "the spec is incomplete".
2. **Feeling or impact.** In a work email, translate feeling into impact on the team:
   "so dev, QA, and the school will each assume a different number".
3. **Need.** What the team needs to move: "one number everyone works from".
4. **Request.** Specific, doable, offered not imposed: "if we add a small table with the
   default and the range, that closes it. Does that work?"

## The tone rule that overrides both

Every point must point forwards at what the fix unlocks for the team, never backwards at
what someone failed to do. The same fact can be written both ways:

| Points backwards (do not send) | Points forwards (send) |
|---|---|
| "Why is there no mid-test rule?" | "One case that will help close before dev starts: what happens if the limit is hit in the middle of a test?" |
| "You have not defined the metric." | "This metric tells us the popup fires but not whether the feature helps. One more row would give us that." |
| "This was missed in review." | "Worth adding to the review checklist so it is caught by default next time." |

Never assign rework to the person who owns the decision. Offer the suggestion, let them
decide.

## Structure

1. BLUF: what you noticed and what it affects, one line, no preamble and no compliment
   sandwich.
2. The fact, anchored to the artifact.
3. The impact on the team or the outcome.
4. The suggestion, in "we" form, hedged.
5. The door open: "Just correct me if I am wrong" or "Any doubt, ask me here".

Two to five sentences per concern. More than one concern means a numbered list, one
entry each, worst first.

## Anti-patterns

1. The compliment sandwich. Readers learn that praise means bad news is coming.
2. "Why" questions. In writing they read as interrogation.
3. Hedging the fact ("I might be wrong but it seems possibly missing"). Hedge the
   suggestion instead.
4. Copying the person's manager on a first raise.

## Sources

1. Kerry Patterson, Joseph Grenny, Ron McMillan, Al Switzler, *Crucial Conversations*,
   2002. https://cruciallearning.com/books/
2. Marshall Rosenberg, *Nonviolent Communication*, 1999.
   https://www.nonviolentcommunication.com/product/nvc/
