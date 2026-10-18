# PRD: Action Item Confidence Scoring v2

Status: already in development. Sprint runs 17-03-2026 to 28-03-2026 (`10-meetings/sprint-planning-2026-03-17.md`). This PRD specs work in flight. It is not a proposal to start it.

## 1. Problem
Action items are wrong or missing 34% of the time (`04-strategy/product-vision.md`). It is the top complaint: 19 of 47 survey respondents (`06-user-feedback/feedback-q1-2026.md`). One said: "I can't trust the action items. I still have to go back and check every single one."

## 2. Target User
Sarah Chen (`05-user-personas/sarah-chen.md`). She uses action items as her task list, and "high" confidence labels still miss critical items. Marcus and Priya do not rely on action items as their task system.

## 3. Solution
- Catches implicit commitments, such as "I'll look into that", as action items.
- Catches items owned by several people.
- Catches conditional items, such as "if X, then Y".
- Shows confidence on the card as High, Medium or Low, not hidden in a tooltip.
- Flags low-confidence items in yellow. The user confirms or dismisses each suggestion.

## 4. Success Metric
Action item accuracy (correct and complete). Baseline: 66% (`04-strategy/product-vision.md`). Target: 80% (`04-strategy/okrs-q2-2026.md`, Objective 1).
Gap: no file sets a date or owner for re-measuring accuracy after launch. Confirm one before sprint close.

## 5. Risks
1. Conditional actions have fewer than 500 labeled examples (`10-meetings/sprint-planning-2026-03-17.md`). Model quality on that type may stay low.
2. False "high" labels are Sarah's core complaint (`05-user-personas/sarah-chen.md`). If they persist, her 8-seat Team upgrade stays blocked.
3. Transcription is 92% in quiet rooms only (`04-strategy/product-vision.md`). Scoring cannot beat that ceiling until Transcript Accuracy v2 ships in June 2026. Granola is gaining with power users (`03-product-knowledge/company.md`).

## 6. What we're NOT building
1. Free-text editing of suggested items. Confirm or dismiss only; editing is v2.1 (`10-meetings/sprint-planning-2026-03-17.md`).
2. Percentage confidence scores. Text labels only (same file).
3. Automating the 2-week manual retraining pipeline. This sprint only documents it (same file).
