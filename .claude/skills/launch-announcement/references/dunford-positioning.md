# Layer 1 Reference - April Dunford's Positioning Components

From "Obviously Awesome" (April Dunford). Positioning is the input to copy, not copy itself. Fill these five components before writing anything customer-facing.

## The Five Components, In Order

The order is the method. Each component only makes sense relative to the one before it.

### 1. Competitive Alternatives

What would the customer do if this feature did not exist? Not just rival products - also "do nothing", spreadsheets, manual work. Pull rivals from the project's competitive intelligence file, and always include the manual alternative.

> **MeetFlow context:** pull from `03-product-knowledge/competitive.md`: Otter (free transcription mental model), Fireflies (integrations, CRM sync), Granola (premium solo UX), Notion AI (bundled, good enough), plus the manual alternative (re-reading transcripts, writing follow-ups by hand).

Ask: for THIS feature, which alternative is the customer actually comparing against?

### 2. Unique Capabilities

What does this feature have that the alternatives do not? Pull from the feature's PRD or spec. Be literal - list capabilities, not benefits. A capability the alternatives also have is not unique and does not belong here.

### 3. Value (So What?)

For each unique capability, answer "so what does that let the customer do?" Value must chain from a capability. If you cannot draw the line from capability to value, drop it. Use the PRD problem statement and user feedback for evidence of what customers actually care about.

### 4. Target Customer

Who cares a LOT about that value? Not everyone - the segment that feels the problem most. Use the personas the PRD names. Note which persona is primary for this launch; the copy in Layer 2 is written to that persona.

### 5. Market Category

What context makes the value obvious? The category the customer should slot this into so they "get it" instantly. A feature can claim a sharper frame than the product's broad category when that makes the value land faster.

> **MeetFlow context:** usually within "AI meeting assistant", but a sharper frame often wins (e.g. "follow-up automation" rather than "transcription").

## Output Format For This Layer

Write a positioning block like this before drafting any copy:

```markdown
## Positioning - [Feature]
- Alternatives: [what customers do today] (source: file)
- Unique capabilities: [2-4 items] (source: file)
- Value: [capability -> outcome chains] (source: file)
- Target customer: [primary persona + why they care most] (source: file)
- Category frame: [the mental slot] (source: file)
```

## Worked Example (calibration, not a canned answer)

A filled block for a fictional "Auto Follow-Up Draft" feature, showing the level of specificity and the citation pattern expected. Match the shape, not the content.

```markdown
## Positioning - Auto Follow-Up Draft
- Alternatives: writing follow-up emails by hand after each meeting; pasting the transcript into a general AI chat; doing nothing and hoping people remember (source: 03-product-knowledge/competitive.md)
- Unique capabilities: drafts the follow-up directly from the meeting's extracted action items; draft is ready before the meeting ends (source: 08-product-features/auto-follow-up/prd.md)
- Value: drafts from action items -> the follow-up goes out while the meeting is fresh, so commitments get owned instead of forgotten (source: prd.md problem statement)
- Target customer: managers who run back-to-back meetings and are judged on follow-through (source: 05-user-personas/, named in the PRD)
- Category frame: follow-up automation, not transcription (source: 03-product-knowledge/company.md)
```

Note how each value line chains from a named capability, and the category frame is sharper than the product's broad category.

## Common Mistakes

- Starting with the category or tagline. The method runs the other way.
- Listing capabilities competitors also have. Check `competitive.md` before calling anything unique.
- Writing value as a feature restated ("it scores confidence" is a capability; "you know which action items to trust without re-reading the transcript" is value).
