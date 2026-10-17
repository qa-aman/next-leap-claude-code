# Extraction test set: how to prepare it

These examples decide whether v1 is done (SPEC.md §11). For each meeting, you write down what the **correct** result is. The app is then checked against your answers.

## What to send

**3–5 meetings.** Between them, cover:

- [ ] A raw Zoom transcript with speaker labels, including at least one label that isn't a person's name (like "iPhone (2)")
- [ ] A messy Google Doc written as prose
- [ ] A Hinglish meeting that uses "kal" or "parso" about a task
- [ ] One long meeting (close to 15,000 words)
- [ ] A meeting that repeats an item still open from an earlier meeting in the same series

One meeting can cover more than one box.

**Two files per meeting**, numbered **starting at 02**. Number `01` is taken by the worked example at the bottom of this page.

```
02-notes.txt    ← the notes, exactly as you'd paste them
02-key.md       ← the answer key (copy the template below)
03-notes.txt
03-key.md
...
```

## Rules for the notes file

1. **Don't clean it up.** Paste it exactly as it came from Google Docs or Zoom: typos, timestamps, half-sentences and all. The mess is what we're testing.
2. **Anonymizing is fine, but be consistent.** Replace a customer or company name with the same fake name everywhere, e.g. "Acme".
3. **Keep the 8 team names as they appear**, including nicknames and misspellings ("Tom", "Tomas"). Owner matching depends on them.
4. **Keep speaker labels exactly as Zoom wrote them.**

## Answer key template

Copy everything between the lines into `NN-key.md` and fill it in.

---

```markdown
# Meeting NN

- Meeting name: Weekly Product Sync
- Meeting date: DD/MM/YYYY
- Weekday: e.g. Thursday
- Type: zoom transcript / google doc / mixed
- Language: English / Hinglish / mixed

## Already open on the board before this meeting
(Only for the duplicate test. Otherwise write "none".)

| Item | Owner | Due date |
|---|---|---|

## Action items that SHOULD be extracted

| # | Item (your words) | Owner | Due date | Date words in notes | Expected flags | Quote from notes |
|---|---|---|---|---|---|---|
| 1 | | | | | | |

## Things that should NOT become items

| Quote from notes | Why not |
|---|---|

## Anything tricky
(Optional. Free text about anything a stranger reading the notes would get wrong.)
```

---

### How to fill in each column

| Column | What to write |
|---|---|
| **Item** | A short description in English. It doesn't need to match the app's wording; items are matched by meaning and by the quote. |
| **Owner** | One of Priya, Marcus, Sarah, Tomás, Aisha, Dana, Ravi, Lena, or **Unassigned** if the notes really don't say who. Answer honestly from the notes, not from what you know happened later. |
| **Due date** | `DD/MM/YYYY`, or **blank** if no date was said or the wording is unclear. Apply the SPEC §5.3 rules: "kal", "parso", "next Friday", "EOW" and "ASAP" all mean **blank**. |
| **Date words in notes** | The exact words used, e.g. `by Friday`, `parso`, `3/10`. Leave empty if none. |
| **Expected flags** | Any of: `needs owner`, `unknown speaker`, `date unclear`, `conditional`, `is this a task?`, `possible duplicate`. Leave empty if none. |
| **Quote from notes** | Copy a short piece of the notes (about 5–15 words) where the task is said. Copy it exactly, since it's used to find the item. |

**Two owners on one task** ("Priya and Marcus to draft proposal"): write **two rows**, one per person.

**"Should NOT become items"** is just as important. Include decisions, things already done, retracted tasks ("scratch that"), and tasks for outside people ("John from Acme"). Put 2–3 per meeting if the notes have them.

## Worked example

`01-notes.txt` (excerpt):

```
00:12:04 Priya Sharma: ok so pricing page — Marcus can you update the copy by Friday?
00:12:10 Marcus: yep
00:13:30 iPhone (2): I'll send the revised deck to the team
00:15:02 Ravi: Tomas aur main vendor list parso tak finalize kar denge
00:16:40 Priya Sharma: we're going with Stripe, decided.
00:17:05 Priya Sharma: John from Acme will send the contract
00:18:00 Dana: if legal signs off, Sarah pushes the release 3/10
```

`01-key.md`:

```markdown
# Meeting 01

- Meeting name: Weekly Product Sync
- Meeting date: 25/09/2026
- Weekday: Friday
- Type: zoom transcript
- Language: mixed

## Already open on the board before this meeting
none

## Action items that SHOULD be extracted

| # | Item (your words) | Owner | Due date | Date words in notes | Expected flags | Quote from notes |
|---|---|---|---|---|---|---|
| 1 | Update pricing page copy | Marcus | | by Friday | date unclear | Marcus can you update the copy by Friday |
| 2 | Send revised deck to team | Unassigned | | | unknown speaker | I'll send the revised deck to the team |
| 3 | Finalize vendor list | Ravi | | parso | date unclear | Tomas aur main vendor list parso tak finalize |
| 4 | Finalize vendor list | Tomás | | parso | date unclear | Tomas aur main vendor list parso tak finalize |
| 5 | Push the release if legal signs off | Sarah | 03/10/2026 | 3/10 | conditional | if legal signs off, Sarah pushes the release 3/10 |

## Things that should NOT become items

| Quote from notes | Why not |
|---|---|
| we're going with Stripe, decided | Decision, no task |
| John from Acme will send the contract | External person |

## Anything tricky
Item 1: the meeting is on a Friday, so "by Friday" could mean today or next week. It should be blank and flagged.
```

## When you're done

Send the files, or put them in this folder. If you're unsure about a row, add a note under "Anything tricky" instead of guessing. The answer key has to be right for the test to mean anything.
