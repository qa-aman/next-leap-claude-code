# Video Review Checklist — post-render QA gate

**Purpose.** After the video renders, the agent runs this checklist against the actual output (the assembled `index.html` in the browser AND the final `renders/video.mp4`), fixes every failure, re-renders, and repeats. The video is shared with the user **only when every applicable item passes**. This is a hard gate, not advice.

**Scope of this project.** 9:16 portrait, `1080x1920`, ~26s, warm British female VO (ElevenLabs), upbeat BGM bed (HeyGen), lifestyle photos as full-bleed backdrops, brand CTA close. Items tagged `[portrait]` matter more here; `[captions]` apply only if captions are enabled.

**Sources.** Every item traces to an authenticated source: the HyperFrames frame-worker contract (`product-launch-video/sub-agents/frame-worker.md`), the composition contract (`hyperframes-core`), the CLI check spec (`hyperframes-cli` → `references/lint-validate-inspect.md`), captions authoring/motion (`media-use/audio/references/captions/`), BGM spec (`media-use/audio/references/bgm.md`), and the project UI design-quality rules (`.claude/rules/ui-design-quality.md`, which encode real shipped bugs). WCAG 2.2, NN/g, and WebAIM are cited inline.

---

## How to run this gate (loop protocol)

1. **Build/refresh the assembled video**, then run the automated pass:
   - `npx hyperframes check` (lint + runtime errors + failed requests + layout defects + occlusion + motion-under-seek + WCAG contrast, one browser session). `--strict` gates warnings too.
   - `npx hyperframes snapshot --at <frame-midpoints>` and read `snapshots/contact-sheet.jpg`.
   - `ffprobe -v error -show_format -show_streams renders/video.mp4` for duration, video stream, and **audio stream presence**.
2. **Walk every section below** against the contact sheet, the `check` findings, and by scrubbing the video (start, each frame midpoint, each transition seam, the last frame, and the exact VO-cue times).
3. **Log each item** as PASS / FAIL / N/A in the Results table at the bottom, with the file:selector or timestamp for any FAIL.
4. **Fix every FAIL** at the cheapest safe edit (usually a single `compositions/frames/NN-*.html`), re-run `check`, re-render.
5. **Repeat** from step 1. Do not exit the loop while any applicable item is FAIL.
6. **Only when the whole table is PASS / N/A** across a clean pass: report to the user with the MP4 path, duration, and a filled Results table.

> Anti-cheat: never mark an item PASS you did not actually verify, and never silence a finding by disabling the check. A `check` that "passes" because a rule was removed is a FAIL of this gate. `check` demotes single-sample transients to info; a defect held across samples is real and gates.

---

## A. Framing, cropping, and safe areas `[portrait]`

- **A1 — Nothing important is cut off by the canvas edge.** Every headline, logo, CTA, price, and subject sits fully inside `1080x1920`. No glyph, descender, or logo edge clipped by the frame bound. *Verify:* `check` layout pass flags "off canvas"; also eyeball each frame midpoint. *Source: hyperframes-cli check (layout: text off canvas); frame-worker.*
- **A2 — Caption keep-out respected.** All content stays in the top ~83% (`y ≤ ~1600` on a 1920-tall frame). No headline/CTA/brand mark drifts into the bottom ~17% caption band. Holds even if captions are disabled, for bottom-edge consistency. *Source: frame-worker "Caption keep-out".*
- **A3 — Content fills the portrait area; no lonely mid-frame cluster.** Hero anchored high (~0.2–0.35 × height), supporting elements flow down with rhythm. Portrait must not vertically center one small block on a sea of empty ground. *Source: frame-worker "Fill the content area — especially portrait".*
- **A4 — Full-bleed photos actually cover the frame.** Background images fill edge-to-edge with no letterbox bars, no stray ground color peeking at an edge, correct object-fit (cover, not contain/stretch). Faces and focal subjects are not cropped awkwardly by the 9:16 crop. *Source: frame-worker `roles` (background full-bleed).*
- **A5 — No element kisses or crosses a container border.** Buttons/cards keep ≥8px clear of their parent's stroke and rounded corner, including any glow at rest. *Source: UI design-quality 2.3, 3.1 (real shipped bug: button overflowed card).*
- **A6 — Safe-area padding holds on the short edge.** `pad-edge` negative space preserved on left/right; display type clamps to the shorter axis so portrait does not blow out headlines past the edge. *Source: frame.md aspect-ratio behavior; frame-worker.*

## B. Audio present, in sync, and mixed right

- **B1 — Audio stream exists in the MP4.** `ffprobe` shows an audio stream; the file is not silent. *Verify:* `ffprobe -show_streams` lists `codec_type=audio`. *Source: hyperframes-cli post-render verification.*
- **B2 — Voiceover plays fully, start to end.** No clipped first word, no cut-off final word ("...co dot uk" lands complete), no dropout mid-line. *Source: SCRIPT.md lines 1–6.*
- **B3 — Voice and picture are in sync.** Each frame's on-screen reveal lands on its VO cue; the visual for a line is on screen while that line is spoken, not a beat early/late. Total drift ~0. *Source: frame-worker "reveal lands on its voiceover cue"; storyboard per-frame timing.*
- **B4 — Frame durations match real voice timing.** Durations were synced from TTS word timestamps (`audio.mjs sync-durations`), not left as estimates. A frame is not visibly holding empty after its line ends, nor cut before the line finishes. *Source: product-launch Step 5 duration sync.*
- **B5 — BGM is a bed under the voice, not over it.** Music volume ≈ 0.12 (~-18 dB) under narration; the voice is always intelligible over the music. No section where music masks the VO. *Source: bgm.md `bgmDefaultVolume()`.*
- **B6 — BGM covers the whole video and ends cleanly.** Music runs from first to last frame with no seam/gap/abrupt stop, and no hard clip at the tail. *Source: bgm.md (loop-to-target, crossfade).*
- **B7 — No audio artifacts.** No clipping/distortion, no pops at cuts, no double-tracked VO, no residual `<audio>` inside a sub-composition (audio is orchestrator-owned at root only). *Source: frame-worker "No `<audio>` element in your composition".*

## C. Captions / highlighting (if enabled) `[captions]`

- **C1 — Captions are word-synced to the VO.** Active-word highlight matches the spoken word within a frame or two; no lag/lead drift accumulating over the clip. *Source: captions authoring "Sync to transcript timestamps".*
- **C2 — Highlighting is correct and visible.** The karaoke active-word highlight (color/scale/glow) lands on the right word; emphasis/brand words (e.g. "vidaXL") get the stronger treatment and read clearly. *Source: captions motion (karaoke baseline; emphasis breaks pattern).*
- **C3 — Caption text never clips.** Scaled emphasis words and glow are not cut by an `overflow:hidden` container; caption container uses `overflow:visible` and `maxWidth` leaves headroom for `scale>1`. *Source: captions authoring "hidden clips scaled emphasis words".*
- **C4 — Captions do not double-print the narration in the body.** On-screen headline copy is short motion-graphics text, not a repeat of the spoken sentence the caption track already shows. *Source: frame-worker "no narration sentence rendered as visible text".*
- **C5 — Captions sit in their band and never occlude the hero.** Caption pill lives in the reserved bottom zone; it does not cover a face or the CTA. *Source: frame-worker keep-out.*

## D. Legibility and contrast

- **D1 — Body/label text ≥ 4.5:1 against its background.** Any text below 18pt regular / 14pt bold. *Verify:* `check` contrast pass reports sampled fg/bg + measured vs required ratio + a compliant suggestion. *Source: WCAG 2.2 SC 1.4.3; UI design-quality 1.1.*
- **D2 — Large display text ≥ 3:1.** Headlines/numerals (18pt+ regular or 14pt+ bold). *Source: WCAG 2.2 SC 1.4.3; UI design-quality 1.2.*
- **D3 — Text over photos stays legible.** Where cream/light type sits on a lifestyle photo, a scrim/gradient (plum/dark, ~30–50% dim on the background) guarantees the ratio across the whole text box, including the brightest part of the image. Backgrounds are dimmed so foreground stays legible. *Source: frame-worker `roles` "background full-bleed and dimmed ~30–50%"; WCAG 1.4.3.*
- **D4 — CTA/button is perceivable as a button at rest.** The "Shop now" affordance has fill, border, or distinct shape at ≥3:1 against its surface, never naked text (no ghost-button failure). One primary CTA per scope. *Source: WCAG 2.2 SC 1.4.11; UI design-quality 1.3, 5.1, 5.2 (real shipped bug: invisible ghost button).*
- **D5 — Legibility floor holds.** Any load-bearing line is large enough to read on a phone (display ≥ ~1.4cqw per frame.md); mono/micro-labels are chrome only, not load-bearing copy. *Source: frame.md typography floor.*
- **D6 — Color is not the only signal.** CTA vs secondary text differ in fill/border/weight, not hue alone. *Source: WCAG 2.2 SC 1.4.1; UI design-quality 5.1.*

## E. Motion, seek-safety, and "not a slideshow"

- **E1 — The shot develops across its full duration; no front-loading.** Pieces reveal on their VO cues through the frame (especially the back ~50%), not all dumped at t=0 then frozen. A frozen-from-25% frame reads as a PowerPoint slide and is a FAIL. *Source: frame-worker "Build the whole shot — reveal across the full duration".*
- **E2 — No mid-frame exit tweens on non-final frames.** Only the final frame may settle/fade out; the between-frame transition is the exit. A non-final frame that animates its content out truncates and glitches. *Source: frame-worker "Only EXITS are banned".*
- **E3 — Motion is seek-safe / deterministic.** One paused GSAP timeline per frame registered on `window.__timelines`; no CSS transitions, no `repeat`/`yoyo`, no `Date.now()`/`Math.random()`/network. Elements appear correctly at every seeked sample, not just on live play. *Source: hyperframes-core contract; frame-worker self-check codes.*
- **E4 — No transform-conflict jumps.** No element has a CSS `transform` (e.g. `translate(-50%)` centering) plus a GSAP transform tween on the same element; centering is via margin/inset or folded into the tween. *Source: frame-worker `gsap_css_transform_conflict`.*
- **E5 — Audio-reactive/pulse motion stays subtle.** Any beat-reactive scale/glow is 3–6%; heavy pulsing that makes text hard to read is a FAIL. *Source: captions motion "Keep audio reactivity subtle".*
- **E6 — Nothing renders invisible.** No frame-root styled by a class on the `data-composition-id` element (renders unstyled at render though Studio looks fine); full-bleed grounds ride a `class="clip"` layer, not `#root` (a root background is clip-gated and can fall onto the black host body). Every named font has a matching `@font-face` pointing at a real shipped file. *Source: frame-worker self-check codes `subcomposition_root_styled_by_class`, full-bleed-on-clip, `font_family_without_font_face`.*

## F. Transitions and seams

- **F1 — Every between-frame transition fires and is clean.** `transitions verify` passes; each seam has the intended `transition_in` with no missing transition, no black flash, no double-exposed overlap of two frames' text. *Source: product-launch Step 6 transitions inject/verify; cut-catalog "two texts visible breaks the illusion".*
- **F2 — No black/blank gap between frames.** Frame windows are contiguous; the last fading element of an internal cut dies right at the seam, leaving no empty gap. *Source: cut-catalog timing.*
- **F3 — Within-frame cuts read as one move.** Any Scene-to-Scene swap inside a frame uses a real cut (z-scale/blur/opacity or per-word stagger), not a hard slideshow jump. *Source: cut-catalog.*

## G. Brand fidelity and content correctness

- **G1 — Brand palette is correct.** vidaXL plum (`#93117E` / deep `#420839`) and lemon (`#F3D018`) on warm cream; no leftover generic black/white or off-brand hue from the preset remix. *Source: frame.md (remixed on captured tokens.json).*
- **G2 — Brand font is Poppins, rendering as text.** No text rendered in `vidaXLfont`/`swiper-icons` (icon fonts) showing as glyph soup or tofu. *Source: tokens.json fonts; frame.md fix.*
- **G3 — Logo/wordmark is correct.** The vidaXL mark is the real asset (or a clean Poppins wordmark), right proportions, not stretched, fully inside the frame, legible on its background. *Source: frame-worker asset placement.*
- **G4 — CTA text is exact and correct.** "Shop now" + "vidaXL.co.uk" spelled correctly; the domain matches the spoken CTA. *Source: brief (evergreen brand + Shop now).*
- **G5 — No invented claims.** No fabricated prices, discounts, counts, dates, review scores, or offers. Only positioning language the brief allows ("stylish", "affordable" — from vidaXL's own site copy). Every visible number traces to an approved source. *Source: project rule "No invented metrics"; frame-worker "Numerals & Claims".*
- **G6 — Only approved, real assets.** Every image is a real staged vidaXL asset (no fabricated URL, no placeholder shipped as final, no unapproved embedded clip). Images are sharp, not upscaled to blur or visibly compressed. *Source: frame-worker "never fabricate an image URL".*
- **G7 — No typos anywhere on screen.** Headlines, CTA, wordmark, any label. Global rule: no em dashes in on-screen copy. *Source: user global writing rules.*

## H. Render integrity and duration

- **H1 — MP4 exists and is non-trivial in size.** `[ -s renders/video.mp4 ]` and a plausible byte size (not a truncated/near-empty file). *Source: hyperframes-cli post-render verification.*
- **H2 — Duration is on target.** ~20–30s (brief), and matches the sum of synced frame durations within a small tolerance. `ffprobe` duration is sane, not 0 or truncated. *Source: brief; Step 5 duration sync.*
- **H3 — Runtime is error-free.** `check` reports no runtime console errors and no failed asset requests (every image/font/audio actually loaded). *Source: hyperframes-cli check.*
- **H4 — First and last frames are intentional.** No blank/black first frame before content; the final frame is a deliberate hold on the CTA (not a mid-animation cut). *Source: frame-worker (final frame may settle).*
- **H5 — Quality settings applied.** Rendered at the intended quality; no obvious banding/compression on the photo backdrops. *Source: render `--quality high`.*

---

## Results (fill every row each pass; loop until no FAIL)

Completed pass on 11-07-2026 against `renders/video.mp4` (14.8 MB · 1080x1920 · 27.0s · AAC stereo). One defect found and fixed mid-loop (F2 black flash), then re-verified clean.

| # | Item | Result | Evidence (file:selector / timestamp) |
|---|------|--------|--------------------------------------|
| A1 | Nothing cut off by canvas edge | PASS | `check` layout 0 off-canvas; contact sheet all 6 frames |
| A2 | Caption keep-out (top 83%) | PASS | headlines ≤ y1100; caption pill in bottom band, MP4 samples |
| A3 | Portrait content fills area | PASS | hero high, content flows down; no lonely mid cluster |
| A4 | Full-bleed photos cover frame | PASS | object-fit cover, no letterbox; frames 1-4 |
| A5 | No element crosses container border | PASS | CTA pill 8px+ clear; tiles inside grid |
| A6 | Safe-area padding on short edge | PASS | pad-edge held; no headline blowout |
| B1 | Audio stream present in MP4 | PASS | ffprobe: aac 48kHz stereo |
| B2 | VO plays fully, no clipped words | PASS | F6 duration 5s > voice 4.13s; "...co.uk" complete |
| B3 | Voice/picture in sync | PASS | captions track VO; beat headlines match clause (MP4 7.6/12.4s) |
| B4 | Frame durations match voice timing | PASS | every frame duration ≥ its voice line + headroom |
| B5 | BGM bed under voice (voice intelligible) | PASS | bgm volume 0.12 (~-18dB); mix mean -26.9dB, voice clear |
| B6 | BGM covers whole video, clean tail | PASS | HeyGen 37s track, loop-to-target; max -4.6dB no clip |
| B7 | No audio artifacts / no in-frame audio | PASS | no `<audio>` in frames; no clipping |
| C1 | Captions word-synced | PASS | 25 groups from 55 ElevenLabs word timings; MP4 samples |
| C2 | Highlighting correct + visible | PASS | lemon karaoke active word ("outdoors","you","now") |
| C3 | Caption text not clipped | PASS | preset skin overflow:visible; no clipped glyphs |
| C4 | No double-printed narration | PASS | on-screen = short distilled titles, not the VO sentence |
| C5 | Captions in band, no occlusion | PASS | pill in bottom zone, clear of hero/CTA |
| D1 | Body text ≥ 4.5:1 | PASS | `check` contrast 33/33 WCAG AA |
| D2 | Large text ≥ 3:1 | PASS | `check` contrast 33/33 WCAG AA (after scrim strengthen) |
| D3 | Text over photos legible (scrim) | PASS | plum/green scrim + text-shadow; frames 1-3 |
| D4 | CTA perceivable as button (no ghost) | PASS | solid plum pill, cream text; one primary CTA |
| D5 | Legibility floor (readable on phone) | PASS | display 116-188px; labels chrome only |
| D6 | Color not the only signal | PASS | CTA fill+shape vs text; emphasis via underline+weight |
| E1 | No front-loading; develops across duration | PASS | staggered reveals paced to VO across each frame |
| E2 | No mid-frame exit on non-final frames | PASS | only F6 settles; others no exit tween |
| E3 | Seek-safe / deterministic motion | PASS | `check` motion 0/0; one paused timeline per frame |
| E4 | No transform-conflict jumps | PASS | centering via inset/text-align; gsap from/fromTo only |
| E5 | Audio-reactive motion subtle | N/A | no audio-reactive motion used |
| E6 | Nothing renders invisible (root/clip/font) | PASS | #root styling; full-bleed on clip; Poppins woff2 shipped |
| F1 | Transitions fire and are clean | PASS | transitions verify: 5/5 cross-track overlap |
| F2 | No black/blank gap between frames | PASS (fixed) | was 0.067s black @9s (push-slide) → blur-crossfade; blackdetect clean |
| F3 | Within-frame cuts read as one move | PASS | blur-cut seams frames 2/3 |
| G1 | Brand palette correct | PASS | plum #93117E / #420839 + lemon #F3D018 on cream |
| G2 | Poppins text (no icon-font glyphs) | PASS | vidaXLfont replaced with Poppins; renders as text |
| G3 | Logo/wordmark correct | PASS | official vidaXL.co.uk SVG, cream + plum variants |
| G4 | CTA text exact | PASS | "Shop now" + "vidaXL.co.uk" (logo domain) |
| G5 | No invented claims | PASS | removed "Free returns/Fast delivery"; only "stylish/affordable" (their copy) |
| G6 | Only approved, sharp assets | PASS | real vidaXL 1200px lifestyle images; no fabricated URLs |
| G7 | No typos / no em dashes | PASS | all on-screen copy reviewed |
| H1 | MP4 exists, non-trivial size | PASS | 14.8 MB |
| H2 | Duration on target (~20-30s) | PASS | 27.0s |
| H3 | Runtime error-free (assets loaded) | PASS | `check` runtime clean, no failed requests |
| H4 | First/last frames intentional | PASS | opens on hook, holds on CTA (no black first frame) |
| H5 | Quality applied, no banding | PASS | rendered --quality high; photo backdrops clean |

**Exit condition:** met - one full pass with zero FAIL across all applicable rows (E5 N/A). Cleared to share.
