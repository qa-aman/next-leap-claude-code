---
name: launch-announcement
description: Generate a complete feature launch kit (announcement blurb, customer email, in-app banner copy, social post) grounded in MeetFlow repo files, using a three-layer framework stack - April Dunford positioning for grounding, StoryBrand SB7 for narrative structure, and the SUCCESs checklist for quality scoring. Use whenever the user mentions a launch announcement, launch kit, launch copy, launch messaging, GTM copy, release announcement, "announce [feature]", "marketing copy for [feature]", customer email for a launch, in-app banner, or wants any customer-facing copy for an upcoming or shipped feature - even if they never say the word "launch". Also use when a marketing teammate asks to "write copy" for a feature that exists in 08-product-features/ or 09-release-notes/.
---

# Launch Announcement Kit

Produce a four-part launch kit for a feature: announcement blurb, customer email, in-app banner copy, and social post. Every claim must trace to a repo file. The kit is built in three layers, in this order. Do not skip or reorder layers - the writing layer depends on the grounding layer, and the QA layer catches what the writing layer misses.

## Step 0 - Scope Check

Before anything else, decide which outputs the user actually asked for. "The launch kit" or "announcement copy for the launch" means all four. "A customer email" or "a social post" means exactly that one output and nothing else - do not pad the deliverable with the other three. All three layers still run either way; positioning and QA are what make the single output good, but the user only receives what they asked for.

## Layer 1 - Grounding (Dunford Positioning)

Before writing a single line of copy, fill the positioning components from repo files. Read `references/dunford-positioning.md` for the component definitions and the order rule.

Source files to read:

| Component | Where to find it |
|---|---|
| Competitive alternatives | `03-product-knowledge/competitive.md` |
| Unique capabilities | Feature PRD or spec in `08-product-features/<feature>/` |
| Value (so what?) | PRD problem statement + `06-user-feedback/` if needed |
| Target customer | Personas in `05-user-personas/` (the PRD names which ones) |
| Market category | `03-product-knowledge/company.md` and `product.md` |

Fill the components in strict order: alternatives first, then capabilities, then value, then target customer, then category. The order matters because each component is only meaningful relative to the previous one - a capability is only "unique" against real alternatives, and value is only real if it flows from a unique capability.

Write the completed positioning block at the top of your working notes. If the feature has no PRD or spec in the repo, stop and ask the user which feature they mean before inventing anything.

## Layer 2 - Writing (StoryBrand SB7)

Read `references/storybrand-sb7.md` for the seven parts and per-format mappings. The non-negotiable rule: **the customer is the hero, the product is the guide.** If a draft opens with "We're excited to announce", it has made the brand the hero - rewrite it.

Produce these four outputs, each structured by SB7 but compressed to fit its format:

1. **Announcement blurb** (100-150 words) - full SB7 arc: problem, guide, plan, call to action, stakes.
2. **Customer email** (under 200 words) - subject line + body. Open on the customer's problem, not the feature name. One call to action.
3. **In-app banner** (under 90 characters + a 2-4 word CTA button label) - compress to Problem + Plan + CTA.
4. **Social post** (under 280 characters) - lead with the customer's pain or the stakes, close with the success state.

Voice rules for all four:
- Match the tone of existing release notes in `09-release-notes/` - plain, direct, short sentences.
- Use only numbers that appear in repo files, and keep a source note per number.
- No hype words ("game-changing", "revolutionary", "10x").
- No em dashes. DD-MM-YYYY for any dates.

## Layer 3 - QA (Format Gate + SUCCESs Scorecard)

**Format gate first.** Before any quality scoring, run two mechanical checks:

1. **Count, do not estimate.** Verify the hard limits by running `wc -c` / `wc -w` on the actual copy (write it to a temp file or pipe it). Report the measured number in the scorecard, never a guessed one - a wrong self-reported count undermines the whole scorecard's credibility.
   - In-app banner: 90 characters or fewer, plus a 2-4 word CTA label
   - Social post: 280 characters or fewer
   - Customer email body: 200 words or fewer
2. **Number audit.** Every number that appears in any copy output must also appear in the Sources section with its file. Scan the copy for digits; any number you cannot point to a source line for gets removed or corrected from the source. This catches drift like rounding "30 minutes" into "20 minutes" mid-draft.

These limits are ceilings, not targets. An output over its limit gets compressed until it fits, before scoring. A social post sized for LinkedIn is the most common failure - write for the 280-character constraint from the start.

**Then score.** Read `references/success-checklist.md`. Score each produced output against the six SUCCESs checks (Simple, Unexpected, Concrete, Credible, Emotional, Stories). Each check is pass/fail with a one-line reason.

- An output passing 5 or 6 checks ships as-is.
- An output passing 4 or fewer gets rewritten once, targeting the failed checks, then rescored.
- Include the final scorecard table at the bottom of the kit so the reviewer sees what was checked.

## Output

Write the kit to `outputs/launch-kit-<feature-name>-<DD-MM-YYYY>.md` using this exact structure:

```markdown
# Launch Kit - [Feature Name]
**Date:** DD-MM-YYYY | **Launch target:** [from PRD]

## Positioning Summary
[The five Dunford components, one line each, with source file citations]

## 1. Announcement Blurb
## 2. Customer Email
## 3. In-App Banner
## 4. Social Post

## SUCCESs Scorecard
[Table: output x six checks, pass/fail]

## Sources
[Every file read, every number's origin]
```

## Hard Rules

- No invented metrics, quotes, or customer names. If a number is not in a repo file, do not use it.
- Cite the source file for every number and every persona claim.
- When two repo files disagree on a number or a framing, prefer the rawest source (survey data and interview transcripts over PRD summaries, PRDs over slide decks). If the conflict is material, note it in the Sources section instead of silently picking one.
- The fictional "today" is defined in the project CLAUDE.md time convention - use it for all date math, not the system date.
