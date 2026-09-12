# Figma Output

Read this only when the user asks for the design in Figma.

## Design in HTML first, then push

Even when Figma is the requested deliverable, build the HTML mockup first and take it through the gate. Two reasons, and both are practical rather than dogmatic.

1. **The gate only runs on HTML.** Contrast, hit targets, focus rings, and spacing can be measured in a browser. They cannot be measured in a Figma file. Pushing an unaudited design to Figma means the accessibility failures get discovered in code review instead of now.
2. **The HTML carries the real values.** Once the tokens are audited, the Figma file is a translation of known-good values rather than a fresh set of guesses.

The exception is when the user already has a Figma design system and wants the new screen assembled from their existing components. Then Figma is the source of truth and the HTML is the by-product, if it is produced at all.

---

## How to push

Figma access comes through the Figma MCP server, and there are dedicated skills for it that carry the current API details. **Do not hand-roll the calls.**

1. **Read `figma:figma-use` first.** It is required before any `use_figma` call and it explains the current contract.
2. **For a full page, view, modal, or multi-section layout, read `figma:figma-generate-design`.** That is the workflow skill for translating an app page into Figma. It discovers existing design-system components, variables, and styles first, then assembles the view section by section using tokens rather than hardcoded values, which is exactly what you want.
3. **For building or extending a design system in Figma, read `figma:figma-generate-library`.**
4. **To read an existing Figma file** rather than write to it, `get_design_context`, `get_metadata`, and `get_screenshot` are the tools. Use these when the user pastes a figma.com URL and wants the design implemented or critiqued.

Note that the `figma` skill in this repo's `.claude/skills/` is a different thing: it imports Figma content into HyperFrames video compositions. It is not the route for pushing a design into Figma.

---

## Before you push

1. **Confirm the destination.** A new file, or an existing one. Never write into an existing file without saying which file and which page, and getting agreement. Writing to Figma is visible to everyone with access, so treat it as an outward-facing action.
2. **Check for an existing design system.** Search the libraries before creating anything. A screen built from the team's real components is worth more than a beautiful orphan built from scratch, and rebuilding what already exists is the fastest way to create drift.
3. **Map tokens to variables.** If the file has Figma variables, bind to them. Hardcoded hex values in a Figma file are the same defect as hardcoded hex in CSS.

---

## Structure the file so it is usable

1. **One frame per state**, not one frame per screen. Default, empty, loading, error, first-run, laid out side by side and labelled. This is the whole reason the design is being reviewed before build, so make the states visible at a glance.
2. **Name layers as components**, matching the atomic breakdown from `design-method.md`. `ActionItemRow`, not `Group 47`. An engineer should be able to read the layer tree and see the component tree.
3. **Auto Layout everywhere**, with padding values from the spacing scale. A frame without Auto Layout cannot be resized honestly and hides every layout problem.
4. **Include the decision panel as a text frame** next to the screens, carrying the same "why this design" block the HTML mockup ships with. A Figma file with no rationale gets misread.
5. **Frame at real sizes.** 1440x900 desktop, 390x844 mobile. Not an arbitrary canvas size that flatters the layout.

---

## What to report back

Give the user the file URL, the frame names, and the same gate result block from `review-gate.md`, with an explicit line saying which checks ran on the HTML and therefore hold for the Figma translation, and which could not be checked in Figma at all. Do not let the Figma file inherit an unearned clean bill of health.
