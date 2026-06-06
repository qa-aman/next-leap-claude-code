# Layer 1 Reference - April Dunford's Positioning Components

From "Obviously Awesome" (April Dunford). Positioning is the input to copy, not copy itself. Fill these five components before writing anything customer-facing.

## The Five Components, In Order

The order is the method. Each component only makes sense relative to the one before it.

### 1. Competitive Alternatives

What would the customer do if this feature did not exist? Not just rival products - also "do nothing", spreadsheets, manual work. For MeetFlow, pull from `03-product-knowledge/competitive.md`: Otter (free transcription mental model), Fireflies (integrations, CRM sync), Granola (premium solo UX), Notion AI (bundled, good enough), plus the manual alternative (re-reading transcripts, writing follow-ups by hand).

Ask: for THIS feature, which alternative is the customer actually comparing against?

### 2. Unique Capabilities

What does this feature have that the alternatives do not? Pull from the feature's PRD or spec. Be literal - list capabilities, not benefits. A capability the alternatives also have is not unique and does not belong here.

### 3. Value (So What?)

For each unique capability, answer "so what does that let the customer do?" Value must chain from a capability. If you cannot draw the line from capability to value, drop it. Use the PRD problem statement and user feedback for evidence of what customers actually care about.

### 4. Target Customer

Who cares a LOT about that value? Not everyone - the segment that feels the problem most. Use the personas the PRD names. Note which persona is primary for this launch; the copy in Layer 2 is written to that persona.

### 5. Market Category

What context makes the value obvious? The category the customer should slot this into so they "get it" instantly. For MeetFlow features this is usually within "AI meeting assistant", but a feature can claim a sharper frame (e.g. "follow-up automation" rather than "transcription").

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

## Common Mistakes

- Starting with the category or tagline. The method runs the other way.
- Listing capabilities competitors also have. Check `competitive.md` before calling anything unique.
- Writing value as a feature restated ("it scores confidence" is a capability; "you know which action items to trust without re-reading the transcript" is value).
