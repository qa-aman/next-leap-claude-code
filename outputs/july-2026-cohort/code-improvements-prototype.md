# Code Improvements — MeetFlow Prototype (`15-prototype/`)

Generated: 17-03-2026
Scope: `15-prototype/` (Next.js 14 App Router, React 18, TypeScript, Tailwind 3) — `app/`, `components/`, `lib/`, `ux-zone/`. `16-zomato/` was not reached in this pass.

## Summary

- Scanned 23 TypeScript/TSX files in `15-prototype/`: 5 route pages, 5 shared UI components, 3 `lib/` files, and 10 `ux-zone` feature components.
- Top-impact finding: `setTone` in `lib/store.ts:34-39` silently overwrites `draftSubject`/`draftBody` the moment a user picks a new tone, discarding any manual edits made in `EmailBodyEditor` with no warning — a real state-loss trap on the one screen (`/follow-up`) built to demo well.
- Second-highest impact: three interactive buttons across the app (`Edit`, `Save draft`, plus the `sm` button size used throughout) either have no `onClick` handler or ship below the project's own 44×44px hit-target rule from `.claude/rules/ui-design-quality.md`.
- Readability is otherwise solid; the main gap is the same `initials()` string-splitting logic and the same `SparkleIcon` SVG duplicated verbatim in multiple components instead of living in `lib/`.
- Performance: no changes suggested. Data sets are single-digit arrays, all list rendering is already `useMemo`-guarded where it matters (`app/action-items/page.tsx:12-25`), and nothing rises above micro-optimization.

## Readability

**[R1]** `ux-zone/action-items/components/ActionItemRow/Component.tsx:82-89`, `ux-zone/live-meeting/components/TranscriptStream/Component.tsx:6-7`, `app/summary/page.tsx:120` — duplicated `initials()` logic
```tsx
function initials(name: string) {
  return name.split(" ").map((n) => n[0]).join("").slice(0, 2).toUpperCase();
}
```
```tsx
const initialsFor = (name: string) =>
  name.split(" ").map((n) => n[0]).join("").slice(0, 2).toUpperCase();
```
```tsx
<Avatar initials={a.assigneeName.split(" ").map((n) => n[0]).join("").slice(0, 2).toUpperCase()} size={18} />
```
Suggested change: move one `initialsFrom(name: string)` helper into `lib/cn.ts` or a new `lib/format.ts`, import it in all three sites.
Rationale: identical logic maintained in three places means a bug fix (e.g. handling single-word names) has to be applied three times or drifts.

**[R2]** `ux-zone/live-meeting/components/AiNotesPanel/Component.tsx:54-60` and `ux-zone/post-summary/components/TldrCard/Component.tsx:39-45` — duplicated `SparkleIcon` component
```tsx
function SparkleIcon() {
  return (
    <svg width="13" height="13" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
      <path d="M9.937 15.5A2 2 0 0 0 8.5 14.063l-6.135-1.582a.5.5 0 0 1 0-.962L8.5 9.936A2 2 0 0 0 9.937 8.5l1.582-6.135a.5.5 0 0 1 .963 0L14.063 8.5A2 2 0 0 0 15.5 9.937l6.135 1.581a.5.5 0 0 1 0 .964L15.5 14.063a2 2 0 0 0-1.437 1.437l-1.582 6.135a.5.5 0 0 1-.963 0z" />
    </svg>
  );
}
```
Suggested change: extract to `components/ui/icons/SparkleIcon.tsx` and import in both.
Rationale: byte-for-byte identical SVG path duplicated across two components signals a missing shared icon module; any future icon tweak (size, stroke) needs two edits.

**[R3]** `ux-zone/follow-up/components/ToneSelector/Component.tsx:36-39` — dead conditional, both branches identical
```tsx
<div className={cn(
  "text-[13.5px] font-semibold tracking-tight transition-colors",
  active ? "text-fg" : "text-fg"
)}>
```
Suggested change: drop the ternary, use the class directly: `<div className="text-[13.5px] font-semibold tracking-tight transition-colors">`.
Rationale: a conditional that resolves to the same value in both branches reads as a bug waiting to be "fixed" by someone who assumes the active state should differ, when it currently does nothing.

**[R4]** `lib/store.ts:9-10,27-28` — dead state, never read or set anywhere
```ts
selectedMeetingId: string | null;
setSelectedMeetingId: (id: string | null) => void;
...
selectedMeetingId: null,
setSelectedMeetingId: (id) => set({ selectedMeetingId: id }),
```
Suggested change: remove `selectedMeetingId`/`setSelectedMeetingId` from the store, or wire it up if a future screen needs it.
Rationale: confirmed via `grep -rn "selectedMeetingId"` — the only references are the declaration and initializer in `store.ts` itself; it's unused surface area in the one shared piece of client state.

## Performance

No changes suggested. All arrays in `lib/mock-data.ts` are single-digit length, list filtering in `app/action-items/page.tsx:12-25` is already wrapped in `useMemo`, and the only intervals/timeouts (`ux-zone/live-meeting/components/RecordingControls/Component.tsx:9-12`, `AiNotesPanel/Component.tsx:7-11`, `TranscriptStream/Component.tsx:13-17`) drive small, local re-renders appropriate for a live-demo prototype. Nothing here qualifies as a hot path worth touching.

## Best practices

**[B1]** `lib/store.ts:33-39` — tone switch silently discards unsaved draft edits
```ts
tone: "concise",
setTone: (t) =>
  set({
    tone: t,
    draftSubject: followUpDrafts[t].subject,
    draftBody: followUpDrafts[t].body,
  }),
```
`ux-zone/follow-up/components/ToneSelector/Component.tsx:23` calls `onChange` (i.e. `setTone`) directly on click, and `EmailBodyEditor` (`app/follow-up/page.tsx:67-73`) lets the user free-type into `draftSubject`/`draftBody` right above the tone selector.
Suggested change: only overwrite `draftSubject`/`draftBody` on tone change if they still match the previous tone's template (i.e. the user hasn't edited them), or route the template swap through the existing `regenerate()` action in `app/follow-up/page.tsx:27-31` so overwriting is an explicit user action, not a side effect of clicking a tone chip.
Rationale: a user who edits the AI draft and then clicks a different tone card loses their edits with no confirmation — on the one screen built to demo the "AI draft you can trust and tweak" story.

**[B2]** `ux-zone/action-items/components/ActionItemRow/Component.tsx:73-75`, `app/follow-up/page.tsx:51` — buttons with no `onClick` handler
```tsx
<Button size="sm" variant="ghost">
  Edit
</Button>
```
```tsx
<Button variant="ghost">Save draft</Button>
```
Suggested change: either wire a handler (even a stub `console.log`/toast for prototype purposes) or replace with `disabled` + a tooltip indicating "coming soon" so the affordance doesn't imply working functionality.
Rationale: per this repo's own UX rules (`.claude/rules/ui-design-quality.md` section 9.5, Jakob's Law / Mental Model), a clickable-looking button that does nothing breaks the user's model of the system on first click — a bad look in a stakeholder walkthrough.

**[B3]** `components/ui/Button.tsx:26-28` — `sm` size ships below the project's own 44×44 hit-target rule
```ts
const sizes: Record<Size, string> = {
  sm: "h-7 px-2.5 text-[12px]",
  md: "h-9 px-3.5 text-[13px]",
};
```
`h-7` is 28px tall. This size is used for the Confirm/Reject/Edit actions in `ux-zone/action-items/components/ActionItemRow/Component.tsx:64,67,73`, all four controls in `ux-zone/live-meeting/components/RecordingControls/Component.tsx:44,47,48,49`, and the filter chips in `ux-zone/action-items/components/FilterChips/Component.tsx:29` (`py-1.5` ≈ 28-30px).
Suggested change: bump `sm` to at least `h-11` (44px) where these controls are the primary interaction on the row (Confirm/Reject, recording controls), or keep `h-7` only for genuinely decorative/secondary chips and document the deviation per rule 4.1.
Rationale: `.claude/rules/ui-design-quality.md` section 2.1 sets 44×44 CSS px as "the universal minimum" for this project; the current `sm` button fails that on every screen where it's the primary action (Confirm/Reject on action items, mute/end-meeting controls).

**[B4]** `app/action-items/page.tsx:27-29` — no error boundary or guard around state mutation from user action
```ts
const handleConfirm = (id: string) =>
  setItems((arr) => arr.map((i) => (i.id === id ? { ...i, state: "confirmed" } : i)));
const handleReject = (id: string) => setItems((arr) => arr.filter((i) => i.id !== id));
```
Suggested change: none required for a prototype with local-only mock state — flagging only because `handleReject` permanently removes the row with no undo, which will read as a bug the first time someone accidentally clicks Reject in a demo. Consider a lightweight "Undo" toast if this flow gets promoted past prototype status.
Rationale: irreversible destructive action (permanent removal from a `useState` array) with no confirmation or undo path, worth a one-line note before this pattern is copied into real product code.
