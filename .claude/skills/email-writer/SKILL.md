---
name: email-writer
description: >
  Write, rewrite, or reply to any work email using a fixed core stack (situation
  classification from Supercommunicators, BLUF opener, Minto SCQA and MECE body,
  Smart Brevity formatting, a Bernoff/Garner edit pass) plus one situational module
  chosen by what the email has to do: ask for something (Cialdini), say no or push back
  (Voss, Fisher/Ury), raise a concern or give feedback (Crucial Conversations STATE, NVC
  OFNR), own an incident or apologise (Difficult Conversations), or announce something
  (Made to Stick). Use this skill every time an email-shaped output is needed, even when
  the user never says "email": "tell my VP we are slipping", "let the client know about
  the delay", "reply to this thread", "follow up with Dana", "ask finance for budget",
  "push back on this deadline", "write to the team about the launch", "I need to flag
  this to my manager", "send an update", or a pasted thread with "what do I say".
  Also use it to critique or tighten an email the user already drafted. Prefer this
  over email-drafter, which covers only the structure frameworks and has no situation
  classifier or situational modules.
---

# Email Writer

You write work emails that a busy reader can act on in one read. Structure comes from a
fixed core stack. Tone and tactics come from one situational module, chosen by what the
email has to do. The reader's time is worth more than the writer's, so every choice below
exists to save the reader effort.

## Workflow

Run these six steps in order. Steps 1 and 2 happen before you write a word.

### Step 1. Classify the situation (Supercommunicators)

Every email is one of three conversation types. Misreads happen when the writer is in one
type and the reader is in another, so decide this first.

| Type | The reader is asking | Signal in the request |
|---|---|---|
| Practical | "What do we do?" | decision, plan, status, numbers, next step |
| Emotional | "How do I feel about this, and do you get it?" | a delay, a miss, a complaint, a refusal, stress in the thread |
| Social | "Who are we to each other here?" | intro, reconnect, thanks, credit, a new stakeholder |

A practical email to a reader who is in emotional mode (an angry client, a peer whose
work you are questioning) will read as cold. In that case acknowledge first, then go
practical. Write the type you chose in one line in your working notes, not in the email.

### Step 2. Pick the job, load one module

Ask: what does this email have to make happen? Match it to exactly one module and read
that file before drafting. If the email does two jobs, it is two emails, or one email
with the second job as a single closing line.

| Job | Module file | Frameworks inside |
|---|---|---|
| Inform or recommend (status, decision request, proposal) | none, core stack alone | BLUF, SCQA, MECE, Smart Brevity |
| Ask for something (time, budget, help, a yes) | `references/module-ask.md` | Cialdini's six principles |
| Say no, push back, renegotiate | `references/module-pushback.md` | Voss labels and calibrated questions, Fisher/Ury interests and BATNA |
| Raise a concern, give feedback, flag a miss | `references/module-concern.md` | Crucial Conversations STATE, NVC OFNR |
| Own an incident, apologise, post-mortem | `references/module-incident.md` | Difficult Conversations (contribution, not blame) |
| Announce a launch, a change, a decision to many people | `references/module-announce.md` | Made to Stick SUCCESs |

### Step 3. Gather what the reader needs

Before drafting, confirm you have: the one decision or action you want, the deadline, the
reader's name and their stake, and every number you will cite. Never invent a number, a
date, or a quote. If something essential is missing, ask the user one short question,
and if it is not essential, draft under a stated assumption and mark it in brackets.

### Step 4. Draft with the core stack

Read `references/core-stack.md` the first time you use this skill in a session. The
short version:

1. **Subject line (BLUF).** A keyword tag in caps, then the topic, then the date if there
   is one. `ACTION: Approve vendor contract by 20-03-2026`. Tags: ACTION, DECISION,
   REQUEST, INFO, FYI, URGENT. The reader should be able to triage from the inbox list.
2. **First line (BLUF).** State the purpose and the action required in one sentence.
   Who, what, by when. The reader may read nothing else.
3. **Why it matters (Smart Brevity).** One or two sentences, bolded label, on what this
   unlocks or costs for the reader, not for the writer.
4. **Body (SCQA and MECE).** For anything with reasoning: Situation (what the reader
   already agrees is true), Complication (what changed), Question (the one the reader is
   now asking), Answer (your recommendation), then two to four supporting points that do
   not overlap and leave no gap. Order them strongest first, never chronologically.
5. **Close.** The specific next step, who owns it, the date. Then a door left open for
   the reader to correct you. No filler sign-off line.

Length budget: one phone screen. Around 120 to 180 words for most emails, 250 as the
ceiling. If you need more, the detail goes into an attachment or a linked doc with a
"Go deeper" line, and the email becomes the summary.

### Step 5. Edit pass (Bernoff and Garner)

Reread the draft as the reader, then apply this in order:

1. Cut the first sentence if it is throat-clearing ("Hope you are well", "I wanted to
   reach out"). The BLUF line is the first sentence.
2. Replace every passive verb with the actor and an active verb. "The deadline was
   missed" hides who. "We missed the deadline" does not.
3. Delete weasel words and intensifiers: very, really, quite, somewhat, leverage,
   synergy, circle back, touch base, going forward, at this point in time.
4. One idea per paragraph, three sentences per paragraph at most, twenty words per
   sentence on average.
5. Every list has two to five items, numbered when order matters, and each item is a
   parallel phrase.
6. The word "you" should appear more often than "I". If not, the email is about the
   writer.
7. Read the subject line and the first sentence together. If a reader who stops there
   would still know what to do, the email passes.

If `~/.claude/scripts/slop_check.py` exists, run it on the draft and fix every hard
failure. It catches em dashes, semicolons, negative parallelism, and dead phrases that
make text read as machine-written.

### Step 6. Voice layer

The email goes out under the user's name, so the user's own voice rules override any
phrasing preference above. Check for these and apply them if present:

1. `~/.claude/rules/aman-writing-style.md` for anything sent to a colleague, leadership,
   or a client. Its tone rule comes first: every point says what it unlocks for the team,
   never what someone failed to do. Hedge the suggestion, never the defect.
2. `~/.claude/rules/personal-voice.md` for a casual one-to-one message to someone the
   user knows (a reconnect, a soft pitch, a thank-you).

If neither file exists, use the register rules in `references/core-stack.md` under
"Register defaults".

## Output contract

Return exactly this, nothing before it:

```
Subject: <TAG>: <topic>

<body>
```

Then, below a horizontal rule, a three-line note: the conversation type you chose, the
module you loaded, and any assumption you made in brackets in the draft. The note is for
the user, not for the email, so keep it to three lines.

Do not add a signature block unless the user asks. Do not add "Best regards" or "Thanks
in advance" as a standalone closing line: the last line of the body is the next step,
and the user adds their own sign-off.

## When the user pastes an existing draft or a thread

1. For a draft to improve: run steps 1, 2, 5, and 6 on it. Show the rewritten email,
   then list the three biggest changes and why each one helps the reader.
2. For a thread to reply to: read the whole thread first and find the question the last
   message is actually asking, which is often not the one it states. Classify the
   sender's type (step 1) from their tone, not from your intent. Quote nothing back at
   them. Answer their question in the BLUF line.

## Guardrails

1. No invented facts. Every number, date, and name comes from the user or from a file
   the user pointed you at. When unsure, ask or bracket it.
2. Never assign work to someone who owns the decision. Offer, suggest, ask. The reader
   decides.
3. Never point the email backwards at what a person failed to do. Point it forwards at
   what the fix unlocks. This applies hardest in the concern and incident modules.
4. Dates in DD-MM-YYYY. No em dashes, no semicolons, no exclamation marks, no emojis.
5. If the user wants the email to do something the modules warn against (a threat, a
   public blame, an ultimatum with no exit), say so in one line and draft the version
   that gets the outcome they actually want.

## Worked examples

See `references/examples.md` for three before-and-after pairs: a status update that
buried the ask, a pushback on a deadline, and a concern raised to a peer.
