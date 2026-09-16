# Core stack: the structure every email gets

Five frameworks, applied in this order. Sources are listed at the end.

## 1. BLUF: Bottom Line Up Front (Sehgal, HBR 2016)

Military email discipline, adopted by Amazon and others. Two parts.

**Subject line.** A keyword in caps, a colon, the topic, a date if any action is dated.

| Tag | Use when | Example |
|---|---|---|
| ACTION | The reader must do something | `ACTION: Sign off Smart Follow-Up launch copy by 24-03-2026` |
| DECISION | The reader must choose between options you present | `DECISION: Ship v2 scoring with or without Slack alerts` |
| REQUEST | You are asking for a resource, time, or approval | `REQUEST: Two design days for the confidence badge` |
| INFO | The reader needs to know, no action | `INFO: Sprint 14 status, on track for 28-03-2026` |
| FYI | Low priority, read when convenient | `FYI: Granola shipped a Windows beta` |
| URGENT | Same-day response needed, use rarely | `URGENT: Zoom recording outage affecting Pro users` |

**First sentence.** Purpose plus action, who, what, by when. Test: if the reader reads only
the subject and this sentence, do they know what to do? Example:

> I need your sign-off on the Salesforce integration scope by Friday 20-03-2026 so
> engineering can start on Monday.

Keep the email inside one screen so the reader never scrolls to find the ask.

## 2. SCQA: the introduction that earns agreement (Minto)

Use when the email carries a recommendation or a decision. Four moves, usually four
sentences.

1. **Situation.** A fact the reader already accepts. This anchors them.
2. **Complication.** What changed that created a problem or a choice.
3. **Question.** The one question the reader is now asking themselves.
4. **Answer.** Your recommendation, stated flat.

> Action item accuracy sits at 66% and is the top churn complaint (Situation). The v2
> model we tested last week reaches 81% but adds 400 ms of latency to summary generation
> (Complication). Do we ship with the latency or hold for optimisation (Question)? Ship
> now, and run the optimisation in the following sprint (Answer).

The Answer then becomes the top of the pyramid. Everything below it supports it.

## 3. MECE: support that does not overlap or leak (Minto)

Your two to four supporting points must be Mutually Exclusive (no two say the same thing
from a different angle) and Collectively Exhaustive (a sceptical reader cannot name an
obvious reason you left out). Tests:

1. Can any two points be merged without losing a fact? Merge them.
2. Would the reader ask "but what about X"? Add X or say why it is out of scope.
3. Are points ordered strongest first? The reader may stop after the first one.
4. Are they the same kind of thing (all reasons, or all options, or all risks)? Mixing
   kinds is the most common MECE failure.

## 4. Smart Brevity: the shape on the screen (VandeHei, Allen, Schwartz)

The Axios system for readers who skim on a phone.

1. **One strong first sentence** (this is your BLUF line).
2. **Why it matters**, bolded, one or two sentences, written from the reader's side.
3. **The details**, as short numbered points with bold lead-ins, never paragraphs of
   prose.
4. **Go deeper**, one line linking to the doc, the dashboard, or the ticket for anyone
   who wants the full picture.

Word budgets: first sentence under 25 words, Why it matters under 40, each detail point
under 30, whole email under 200 unless the user says otherwise.

## 5. Edit pass: Iron Imperative and plain style (Bernoff, Garner)

Bernoff's Iron Imperative: treat the reader's time as more valuable than your own. Garner's
HBR guide turns that into line-level rules. Apply them in this order, because earlier
cuts make later ones unnecessary.

1. Delete throat-clearing openers and closers.
2. Convert passive to active and name the actor.
3. Strike jargon, weasel words, and intensifiers. If a word could be deleted without
   changing the meaning, delete it.
4. One idea per paragraph. Three sentences maximum. Average sentence under 20 words.
5. Prefer the short word: use not utilise, help not facilitate, start not commence.
6. Check the "you" to "I" ratio. Reader-first emails use "you" more.
7. Read the subject and first line alone. If they carry the ask, the email works.

## Register defaults

Used when no user voice file is found. Professional register for colleagues, leadership,
clients.

1. Full words. "You", never "u". Correct spelling and apostrophes.
2. "We" over "you" when proposing work. "We need to" reads as a team, "you need to"
   reads as an order.
3. State a problem flat. Hedge your own suggestion. "The limit is missing" is flat.
   "What I feel is a small table would close this, correct me if I am wrong" is hedged.
4. Close with the door open: "Let me know if I have read this wrong" or "Any doubt,
   ask me here".
5. Numbered lists, not bullets. Bold for labels, not for whole sentences.
6. No em dashes, no semicolons, no exclamation marks, no emojis.

## Sources

1. Kabir Sehgal, "How to Write Email with Military Precision", HBR, 2016.
   https://hbr.org/2016/11/how-to-write-email-with-military-precision
2. Barbara Minto, *The Pyramid Principle*. https://www.barbaraminto.com/
3. Jim VandeHei, Mike Allen, Roy Schwartz, *Smart Brevity*, 2022.
   https://www.smartbrevity.com/book
4. Josh Bernoff, *Writing Without Bullshit*, 2016. https://bernoff.com/books and
   https://bernoff.com/blog/iron-imperative-of-writing-dont-waste-time
5. Bryan Garner, *HBR Guide to Better Business Writing*, 2012.
   https://store.hbr.org/product/hbr-guide-to-better-business-writing/10946
6. Charles Duhigg, *Supercommunicators*, 2024 (Step 1 classification).
   https://www.charlesduhigg.com/supercommunicators
