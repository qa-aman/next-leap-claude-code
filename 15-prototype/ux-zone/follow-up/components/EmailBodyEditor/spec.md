# EmailBodyEditor

Subject + body composer for the follow-up email. AI-drafted body that the user can edit; a regenerate affordance lets them re-prompt the same tone.

## Anatomy
- Subject row: label + single-line input
- Body section: label ("Body · AI-drafted") + Regenerate button on the right
- Body textarea: 14-row default, monospace-free for natural reading

## Mirrored from
- `screenshots/apollo-01.png` - AI-drafted multi-paragraph body explicitly referencing the meeting + prefilled "Recap:" subject. CANONICAL structure.
- `screenshots/honeybook-04.png` - refresh / regenerate-draft pattern.

## Props
- `subject: string`
- `body: string`
- `onSubjectChange: (s: string) => void`
- `onBodyChange: (s: string) => void`
- `onRegenerate: () => void`
