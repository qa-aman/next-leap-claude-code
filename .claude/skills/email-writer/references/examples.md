# Worked examples

Three before-and-after pairs. Each "before" is the kind of draft a busy PM writes in two
minutes. Each "after" went through the six steps. MeetFlow context is used throughout.

## Example 1: Status update that buried the ask (core stack only)

**Type:** practical. **Module:** none.

**Before**

> Subject: Update
>
> Hi Dana, hope you are doing well. I wanted to give you a quick update on where we are
> with the Salesforce integration work. The team has been making good progress over the
> last two weeks and we have completed the OAuth flow and the basic object mapping.
> There have been some challenges with the rate limits on the Salesforce side which we
> are still investigating. We also found that the sandbox environment behaves differently
> from production in some cases. Given all this, I think we might need to look at the
> timeline again. It would be great if we could find some time to discuss. Let me know
> what works for you. Thanks!

**After**

> Subject: DECISION: Salesforce integration, hold May launch or cut scope, by 20-03-2026
>
> I need your call by Friday 20-03-2026 on whether we hold the May launch date and cut
> the scope, or keep the full scope and move to June.
>
> **Why it matters:** Sales has promised the integration to two of the three enterprise
> pilots, so whichever way we go, they need to hear it from us next week, not from a slip.
>
> Where we are:
>
> 1. **Done:** OAuth flow and core object mapping, on plan.
> 2. **Blocking:** Salesforce API rate limits cap us at roughly one third of the sync
>    volume the pilots need. We found this on 12-03-2026 and do not yet have a
>    workaround.
> 3. **Risk:** The sandbox does not mirror production limits, so we cannot prove a fix
>    until we test against a real org.
>
> Two options:
>
> 1. **May, reduced:** ship one-way sync (MeetFlow to Salesforce) in May, two-way in June.
> 2. **June, full:** hold the full two-way scope and move the date to the second week of
>    June.
>
> My recommendation is option 1, because the pilots asked for notes-into-Salesforce
> first and the reverse direction second. If you see the pilot priority differently,
> tell me and I will redo the plan. Happy to walk through it in 15 minutes any day this
> week.

**What changed:** the ask moved from the last line to the subject. The reader gets a
decision with two options and a recommendation instead of "let us find time". Every
fact has a date. The "you" count went from 3 to 6, the word count from 130 to 210 but
with a decision inside it.

## Example 2: Pushing back on a deadline (pushback module)

**Type:** emotional first, then practical. The reader is under pressure from their own
stakeholder. **Module:** pushback (Voss labels, Fisher/Ury options).

**Before**

> Subject: Re: Confidence scoring v2 demo
>
> Hi Marcus, unfortunately I do not think we can have v2 ready for the 24th. The team is
> stretched with the Smart Follow-Up launch and the model still needs another round of
> evaluation. Sorry about this. Can we push it out a couple of weeks?

**After**

> Subject: Re: Confidence scoring v2 demo, two ways to keep 24-03-2026
>
> We cannot have the full v2 model in production for the 24-03-2026 demo. We can still
> give you a demo on that date, two ways below.
>
> It sounds like the 24th matters because the three enterprise pilots are in the room and
> they raised action item accuracy in every call. That is the thing to land.
>
> The constraint: the v2 model is at 81% accuracy on the eval set against 66% today, but
> we have one more evaluation round to run before it touches live meetings, and that round
> takes six working days from when the Smart Follow-Up launch frees the team on 19-03.
>
> Options:
>
> 1. **Recorded demo, 24-03:** v2 running on five real pilot meetings we have consent for,
>    shown as a recorded walkthrough. Production follows on 02-04-2026.
> 2. **Live on staging, 24-03:** v2 live against staging data in the room. Same production
>    date, more risk of a visible glitch.
>
> How would you want the pilots to experience it, recorded and safe or live and
> slightly risky? Either works for us. If you can tell me by Wednesday 18-03, we can
> prepare the right one properly.

**What changed:** the "no" is in the first line and is not apologised for. The label
("it sounds like the 24th matters because...") shows the interest was understood. The six
working days is a criterion, not a feeling. Two options meet the reader's interest. The
close is a calibrated question, not a request to push.

## Example 3: Raising a concern with a peer (concern module)

**Type:** emotional. A peer's spec, a gap that will cost the team. **Module:** concern
(STATE, OFNR), with the forwards-pointing tone rule.

**Before**

> Subject: Smart Follow-Up spec issues
>
> Hi Aisha, I went through the Smart Follow-Up spec and noticed a few issues. The tone
> options are not defined anywhere, there is no mention of what happens when the
> recipient list is empty, and the success metric is just "emails sent" which does not
> really measure anything. Can you fix these before the sprint starts?

**After**

> Subject: Smart Follow-Up spec, three points that will help dev and QA start clean
>
> I read the Smart Follow-Up spec end to end today. Three things stood out that I think
> will save the team a round of questions once the sprint starts on 17-03-2026.
>
> 1. **Tone options.** Section 4 says the user picks a tone, and I could not find the
>    list. If we add the three or four tones with a one-line example each, dev builds
>    the right dropdown first time and QA has something to test against.
> 2. **Empty recipient list.** The flow assumes at least one attendee with an email. In
>    the interview set, two of the four users had meetings with external dial-in guests
>    and no addresses. One line on what the user sees in that case would close it.
> 3. **Success metric.** "Emails sent" will show the feature is firing but not whether
>    it is helping. What I feel is one more row, follow-ups opened or replied to within
>    48 hours, gives us the answer in six weeks. Just correct me if I am wrong on what we
>    can measure.
>
> These are suggestions, the final call on all three is yours. Any doubt, ask me here and
> I can walk through the interview examples.

**What changed:** every point opens with the observation anchored to a section, says what
it unlocks for the team, and offers the fix in "we" form. "Can you fix these" became
"the final call is yours". The subject names the benefit, not the "issues".
