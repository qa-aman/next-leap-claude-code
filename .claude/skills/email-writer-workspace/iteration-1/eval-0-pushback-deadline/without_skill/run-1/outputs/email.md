Subject: Salesforce Sync Commitment for 15-05-2026 - Need to Adjust Scope

Hi Marcus,

Thanks for flagging the urgency here, I know both pilots are counting on this.

I want to give you a commitment we can actually hold. Engineering identified on 12-03-2026 that Salesforce's API rate limits cap us at roughly a third of the sync volume the pilots need for full two-way sync. There's no workaround in place yet, so committing to two-way sync by 15-05-2026 would be a promise we can't keep.

What I can commit to by 15-05-2026 is one-way sync, MeetFlow to Salesforce. That covers pushing meeting summaries and action items into Salesforce records, which is likely most of what the pilots actually want to see on day one.

For the two-way piece, I'd rather scope a real solution than give you a date that slips later. Options engineering and I can explore: batching/throttling within the rate limit, requesting a higher API limit tier from Salesforce, or phasing two-way sync to launch after 15-05-2026 once we've solved the throughput problem.

Can we get 30 minutes this week with you and engineering to align on what we tell the pilots? I'd rather we go to them now with "one-way ships 15-05, two-way follows on a confirmed date" than overpromise and have to walk it back later.

Best,
Aman
