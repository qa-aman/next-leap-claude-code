# Smart follow-up composer — Screen Notes

**Route:** `/follow-up`
**Purpose:** Demo Smart Follow-Up (April 2026 launch). AI-drafted email tied to action items, with tone control.

---

## References to mirror

### Recipient picker (multi-select chips)
- Reference: `apollo-01.png` — Mirror the **To: field with email chips + dropdown selector + From row above** for the recipient header.
- Reference: `superhuman-05.png` — Mirror the **single-line To: with chip removal + right-rail recipient detail panel** for a denser variant.

### Subject line
- Reference: `apollo-01.png` — Mirror the **prefilled "Recap: [Meeting title]" subject pattern** + Use template dropdown. CANONICAL — the subject should auto-fill from the meeting title.
- Reference: `superhuman-05.png` — Mirror the **single-line Subject field with no chrome** for a clean composer feel.

### Email body (AI-drafted, editable)
- Reference: `apollo-01.png` — Mirror the **AI-drafted multi-paragraph body** that explicitly references the meeting (e.g., "Here's an overview from our meeting:") + recipe of next steps. CANONICAL body structure.
- Reference: `honeybook-04.png` — Mirror the **AI composer modal body with inline editing + refresh-draft icon**. Use for the regenerate affordance.

### Tone selector (Concise / Warm / Direct)
- Reference: `strut-02.png` — **BEST reference for the tone selector.** Mirror the **AI Edit > Adjust tone > sub-menu (Neutral / Friendly / Professional / Casual)** dropdown structure. Adapt the menu items to Concise / Warm / Direct.
- Reference: `pipedrive-03.png` — Mirror the **Email tone dropdown + Email length dropdown side-by-side** for a structured tone+length picker.
- Reference: `honeybook-04.png` — Mirror the **inline tone chips ("Change tone" / "Make it shorter" / "Make it longer")** below the draft for quick re-prompts.

### Send button + confirmation
- Reference: `apollo-01.png` — Mirror the **Schedule + Send Now split button** at the bottom-right + Save as new template secondary action.
- Reference: `honeybook-04.png` — Mirror the **Review before sending dark CTA** as the final-step affordance.

---

## Layout rationale

Single composer screen with three layers from top to bottom: recipient header (To + Subject), AI-drafted body (editable, ~60% of vertical space), and the tone/action control rail (Tone selector + Send). The tone selector is the differentiator — it must feel native to the composer (Strut's Adjust tone submenu pattern), not bolted on as a separate modal. The body prefills with content that references the action items from `/action-items` so the demo tells a continuous story across screens.

---

## Components to extract

- `RecipientPicker` — Apollo-01 To row with chips
- `SubjectInput` — Apollo-01 prefilled "Recap:" pattern
- `EmailBodyEditor` — Apollo-01 AI-drafted body + HoneyBook-04 refresh-draft icon
- `ToneSelector` — Strut-02 Adjust tone dropdown (Concise / Warm / Direct)
- `SendButton` — Apollo-01 Schedule + Send Now split CTA
