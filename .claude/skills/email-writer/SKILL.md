---
name: email-writer
description: Draft, rewrite, or reply to a work email that a busy reader will read, understand, and act on. Built on four core frameworks - Rogers and Lasky-Fink's six busy-reader principles (Writing for Busy Readers) as a pre-send gate, Minto's Pyramid Principle with SCQA and BLUF for structure, Axios Smart Brevity for updates, Garner's HBR Guide for craft - plus three modules loaded by email type - Cialdini for asks, Chris Voss for follow-ups and negotiation, Crucial Conversations (STATE) for difficult emails. Use this skill whenever the user wants to write, draft, compose, rewrite, shorten, or reply to an email to a boss, peer, team, stakeholder, or client - status updates, decision requests, recommendations, asks, nudges, chasers when someone has gone quiet, push-backs, saying no, bad news, feedback, apologies, escalations, announcements. Trigger on "draft an email", "email my VP", "reply to this thread", "follow up with", "chase X", "tell the team", "let the client know", "push back on", "how do I say no to", "/email-writer", or when the user pastes an email thread and wants a response, even if they never say the word "email". Not for cold outreach, sales or recruiter emails (use executive-communication), Slack messages, newsletters, or meeting minutes (use mom).
---

# Email Writer

Write work emails that get read, understood, and acted on. The reader is busy and skims, often stopping after the first lines. So the point, the ask, and the deadline have to be visible in the first two lines, and everything after them is support.

The skill has three layers:

1. **Core structure** (every email): Minto's Pyramid Principle, answer first.
2. **Format and module** (by email type): Smart Brevity for updates, or one of three modules in `references/`.
3. **Pre-send gate** (every email): the six busy-reader principles, checked one by one.

Source books and why each was picked: `references/sources.md`. Read it only if the user asks where a rule comes from.

## Step 1 - Classify the email

Pick the type from the request. Do not ask the user to classify it.

| Type | Signals | Load |
|---|---|---|
| **Update / announcement** | status, weekly update, heads-up, launch note, "tell the team" | Core + Smart Brevity (Step 4) |
| **Decision request / recommendation** | need approval, sign-off, "propose", "recommend", choose between options | Core only |
| **Ask** | need help, resources, review, input, a favour, an intro, a budget | Core + `references/ask.md` |
| **Follow-up / negotiation** | no reply, chase, nudge, gone quiet, push back on scope, timeline, or resourcing | Core + `references/follow-up.md` |
| **Difficult** | bad news, saying no, feedback, apology, escalation, conflict, missed commitment | Core + `references/difficult.md` |
| **Reply to a thread** | user pastes a thread, "reply", "respond" | Core, match the thread's register, plus a module if the content fits one |

If an email fits two types (a follow-up that is also bad news), load both modules. The more sensitive one sets the tone.

## Step 2 - Gather only what changes the email

Draft straight away when the request names the recipient, the point, and the ask. When something material is missing, ask at most two questions, and only the ones where a different answer would produce a different email:

- Who is the reader and what is your relationship (manager, peer, exec, client)?
- What is the one thing they need to know or do, and by when?
- For difficult emails: what outcome do you want for the relationship, not just the issue?

Everything else, assume and flag after the draft (Step 6). A draft with a flagged assumption beats a round of questions.

**Grounding.** Use only facts the user gave or that exist in files they pointed to. In this repo, numbers come from repo files (`03-product-knowledge/`, `04-strategy/`, `06-user-feedback/` and so on). Never invent a metric, a date, a name, or a quote. If a needed fact is missing, leave a visible placeholder like `[date]` and flag it.

## Step 3 - Build the core structure (Minto + BLUF)

Every email body follows the pyramid: the governing thought first, then the support, then the next step.

```
Line 1-2:  The answer, recommendation, or ask (BLUF)
Body:      2-3 supporting points, distinct, no overlap (MECE)
Close:     One next step with an owner and a date
```

- **Answer first.** The first sentence states the conclusion or the ask. If the most important sentence is in paragraph three, the email is broken. Readers who stop after two lines should still know what to do.
- **SCQA when the reader lacks context.** Situation (one line they already accept), Complication (what changed), then the Answer. The Question stays implied. For readers already in the loop, skip S and C.
- **Supporting points are distinct.** Two or three reasons, options, or facts that do not repeat each other and do not leave an obvious gap. Number them when there are two or more.
- **Close on an action.** One of: a specific ask with a date, a next step with an owner, or a confirmation request. "Let me know your thoughts" is not an action.

## Step 4 - Format for the type

**Updates and announcements use Smart Brevity** (Axios):

```
Subject:  Short tease, 6 words or fewer where possible, carrying the headline
Lede:     One sentence, the single most important thing
Why it matters: One line on the consequence for the reader
Bullets:  3-5 short facts (progress, risk, what is next)
Go deeper: Link or attachment for anyone who wants detail (optional)
```

Keep the "Why it matters:" label, it is the part busy readers scan for. Do not repeat the lede in it.

**All other types:** short paragraphs (1-3 sentences), numbered options where there is a choice, and the ask on its own line so it cannot be missed.

**Subject lines** (Garner: specific, scannable, the noun and the verb):

| Type | Pattern | Example |
|---|---|---|
| Update | `[Project]: [status] - [headline]` | `Confidence Scoring v2: on track, one data risk` |
| Decision | `Decision by [day DD-MM]: [topic]` | `Decision by Wed 25-03: ship or slip Smart Follow-Up` |
| Ask | `Ask: [what] by [when]` | `Ask: review Salesforce PRD by Fri 20-03` |
| Follow-up | Keep the thread subject so the history stays attached | n/a |
| Difficult | Neutral and specific, never alarming or vague | `Custom field mapping: Q2 answer and an alternative` |

## Step 5 - Craft pass (Garner, HBR Guide to Better Business Writing)

- **Reader first.** Open with what matters to them. "You asked about X" beats "I wanted to follow up on X".
- **Plain words.** "Use" not "utilize", "now" not "at this juncture". Jargon only if the reader uses it daily.
- **Active voice.** "I will send the doc Friday", not "the doc will be sent".
- **One clear view.** Cut stacked hedges ("I think maybe we could possibly"). State the recommendation.
- **No filler.** Cut "Hope this finds you well", "Just wanted to reach out", "Quick question", "Thanks in advance".
- **Tone by reader.** Up the chain: tighter, fewer hedges, the ask in line one. Peers: direct and collegial. Clients: calm, accountable, specific, no internal blame. Replies: match the thread; terse gets terse.
- **House rules.** No em dashes (use commas or hyphens). No emojis. Dates as DD-MM-YYYY, or day plus DD-MM inside a sentence ("Wed 25-03"). In this repo, today is 17-03-2026.
- **Voice.** If the email goes out under Aman's name and the `aman-writing-style` skill is available, load it before drafting.

**Length targets** (body words). Over by more than 30%? Cut. Longer emails get skimmed and the ask gets lost.

| Type | Target |
|---|---|
| Update | 80-150 |
| Decision / recommendation | 100-180 |
| Ask | 60-120 |
| Follow-up | 30-90 |
| Difficult | 100-200 |
| Reply | Match the thread, usually 40-100 |

## Step 6 - Run the busy-reader gate before handing over

Check the draft against each of the six principles from *Writing for Busy Readers*. Fix any failure, then re-check. These six are the reason the email gets acted on, so do not skip them.

| # | Principle | Pass when |
|---|---|---|
| 1 | Less is more | Within the length target. One purpose per email; two unrelated asks become two emails (say so). Every sentence earns its place. |
| 2 | Make reading easy | Short common words. Sentences mostly under 20 words. Active voice. |
| 3 | Design for easy navigation | The key point or ask is in the first two lines. Distinct ideas sit in separate paragraphs or numbered items. |
| 4 | Use enough formatting, but no more | Bold used on at most two items (usually the ask and the deadline). No all-caps, no colour, no mixed styles. |
| 5 | Tell readers why they should care | The email says what it means for this reader. With several recipients, it says who needs to act. |
| 6 | Make responding easy | One clear ask, a deadline, and the effort involved. Where possible the reader can reply in one line ("reply 1 or 2"). Links point to the exact thing to review. |

Then check the module's own pass list if one was loaded.

**Count, do not estimate.** Count the body words with a tool (for example, save the body to a temp file and run `wc -w`), excluding the subject and the notes under `---`. Report the exact number in the Gate line, never "~150". If the count is over the target by more than 30%, cut and count again before reporting a pass. A gate line that claims a pass the email does not meet is worse than no gate line.

## Output format

Give the email first, ready to paste, then up to three short lines below it. No preamble.

```
**Subject:** <subject line>

<body>

---
Assumption: <only if you assumed something material, one line each, max two>
Facts used: <number or fact> (<source file>), only if facts came from files
Gate: 6/6 busy-reader checks passed, <N> words, type: <type>[, module: <module>]
```

No signature block unless the user asks; end on the next step. If the user asks for options, give at most two drafts separated by `---`, each labelled by what varies (tone, length, framing). Do not volunteer variants.

When a difficult email is high-stakes and emotional, say so in one line under the draft: a short call first, then this email to confirm what was agreed, usually lands better (see `references/difficult.md`).

When called by another agent or asked to save the email, write it to the location that agent or user specifies, otherwise return it in chat.

## Example - decision request to a VP

Request: "Email my VP asking whether to slip Smart Follow-Up two weeks. QA found a blocker in the confidence model. Option 1: ship on time with a workaround that drops action item accuracy. Option 2: fix it properly and slip two weeks."

```
**Subject:** Decision by Wed 25-03: ship Smart Follow-Up on time or slip 2 weeks

I recommend we slip Smart Follow-Up by two weeks to fix a blocker QA found in the confidence model.

Two options:

1. Ship on the planned date with a workaround. Action item accuracy drops further, and accuracy is already the top complaint behind Pro churn.
2. Slip two weeks and ship the fix. Accuracy holds; we miss one planned marketing beat.

Option 2 protects the metric this feature exists to improve.

**Can you confirm by Wed 25-03** so engineering can plan the next sprint?

---
Assumption: "drops further" kept qualitative, the size of the drop was not given.
Facts used: accuracy is the top complaint driving churn (03-product-knowledge/company.md)
Gate: 6/6 busy-reader checks passed, 84 words, type: decision request
```

## When the user pastes a thread

Find the last unanswered question or the move the thread is waiting for. Answer it in the first line, match the register, and advance the thread with a next step. Do not re-summarise what everyone has already read.
