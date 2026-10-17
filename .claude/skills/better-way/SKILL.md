---
name: better-way
description: Challenge Aman's stated approach and propose a clearly better one before doing the work. Use when he types /better-way, "better?", "is there a better approach", "any better idea", "what would you do instead", or shares his own idea and asks whether it is the best way. Works in any project.
---

# Better way

Aman gives his idea, then wants to know if there is a better way before anything is built. Answer that first, briefly, then do the work he picks.

## Steps

1. **Restate his approach in one line**, so he can see it was understood.
2. **Find the better options.** Look for, in this order:
   - a mechanical guard instead of a written rule (a hook, a test, a check that fails)
   - a system that runs every time instead of a one-off (AI-native: system, evidence, memory, learning loop, see `~/.claude/rules/ai-native-solutions.md`)
   - a native feature of the tool instead of a hand-rolled one (check the first-party docs)
   - something that removes a step he would otherwise have to remember
3. **Check before proposing:** each option must be feasible on the real platform (the feasibility gate in `~/.claude/CLAUDE.md`), and for a design question, say what the best teams shipped (the benchmark gate).
4. **Answer in this shape, nothing longer:**
   - His way: one line.
   - Better way: what it is, the concrete gain over his way, the cost or limit.
   - My pick, in one line. If his way is already the best, say so in one line and stop.
5. **Wait for his pick** when the choice changes what gets built. If the request also contained the task itself and the better way is only an improvement, do his way and offer mine.
6. **Log the outcome** once he picks: append one line to `~/.claude/better-way/ledger.md` (`- DD-MM-YYYY | accepted/rejected | suggestion | why`). Read the last lines of that file before step 2, so suggestions follow his taste.
