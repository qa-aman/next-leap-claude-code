# Fowler: code smells and the refactoring catalog

**Sources:** https://refactoring.com/catalog/ (the refactoring names below are taken from this page) and https://martinfowler.com/bliki/CodeSmell.html. The smell names come from Martin Fowler, *Refactoring* 2nd edition, chapter 3, "Bad Smells in Code", written with Kent Beck. Both are first-party.

## Contents

1. What a smell is, and its limits
2. Smell to refactoring lookup
3. The full refactoring catalog (66 names)
4. How to use a name in a finding

---

## 1. What a smell is, and its limits

Fowler's own framing on the bliki page is that a code smell is "a surface indication that usually corresponds to a deeper problem in the system", and the two properties that matter are that it is quick to spot and that it does not always mean there is a problem.

That second half is the part reviewers drop. A smell is a prompt to look, not a verdict. A 60-line function that reads as one clear sequence is fine. A 12-line function juggling three responsibilities is not. Report the underlying problem you found, and use the smell name to say how you found it.

---

## 2. Smell to refactoring lookup

This is the working table. Left column is what you noticed, right column is the named fix from the catalog.

| Smell | What you actually saw | Refactorings to reach for |
|---|---|---|
| Mysterious Name | A name that needs a comment to explain it | Rename Variable, Rename Field, Change Function Declaration |
| Duplicated Code | The same shape in two or more places | Extract Function, Slide Statements, Pull Up Method |
| Long Function | One function holding several ideas | Extract Function, Replace Temp with Query, Introduce Parameter Object, Decompose Conditional, Split Loop |
| Long Parameter List | Five arguments, several always passed together | Introduce Parameter Object, Preserve Whole Object, Replace Parameter with Query, Remove Flag Argument |
| Global Data | Mutable state reachable from anywhere | Encapsulate Variable |
| Mutable Data | A variable updated for two different purposes | Split Variable, Encapsulate Variable, Replace Derived Variable with Query, Separate Query from Modifier |
| Divergent Change | One module changed for many unrelated reasons | Split Phase, Move Function, Extract Class |
| Shotgun Surgery | One change forces edits in many modules | Move Function, Move Field, Combine Functions into Class, Inline Class |
| Feature Envy | A function more interested in another object's data | Move Function, Extract Function |
| Data Clumps | The same 3 values travelling together everywhere | Extract Class, Introduce Parameter Object, Preserve Whole Object |
| Primitive Obsession | Strings and numbers standing in for concepts | Replace Primitive with Object, Replace Type Code with Subclasses, Extract Class |
| Repeated Switches | The same conditional repeated in several places | Replace Conditional with Polymorphism |
| Loops | A loop doing filter plus map plus reduce at once | Replace Loop with Pipeline, Split Loop |
| Lazy Element | A class or function that no longer earns its keep | Inline Function, Inline Class, Collapse Hierarchy |
| Speculative Generality | Machinery built for a case that never arrived | Collapse Hierarchy, Inline Function, Remove Dead Code, Change Function Declaration |
| Temporary Field | A field only set in some circumstances | Extract Class, Move Function, Introduce Special Case |
| Message Chains | `a.b().c().d()` | Hide Delegate, Extract Function, Move Function |
| Middle Man | A class that only delegates | Remove Middle Man, Inline Function |
| Insider Trading | Two modules reaching into each other's internals | Move Function, Move Field, Hide Delegate |
| Large Class | A class doing too many jobs | Extract Class, Extract Superclass, Replace Type Code with Subclasses |
| Alternative Classes with Different Interfaces | Two classes doing the same job, named differently | Change Function Declaration, Move Function, Extract Superclass |
| Data Class | A bag of fields with all the logic outside it | Encapsulate Record, Move Function, Extract Function |
| Refused Bequest | A subclass ignoring most of what it inherits | Replace Subclass with Delegate, Replace Superclass with Delegate, Push Down Method |
| Comments | A comment compensating for unclear code | Extract Function, Rename Variable, Introduce Assertion, Change Function Declaration |

On the last row, Fowler's point is that comments are not themselves a smell, they are often a deodorant sprayed over one. A comment saying *why* is valuable and should stay. A comment explaining *what* the next ten lines do is usually a function waiting to be extracted.

---

## 3. The full refactoring catalog

From https://refactoring.com/catalog/, alphabetically. Use the exact name, because the exact name is what the reader can look up.

Change Function Declaration, Change Reference to Value, Change Value to Reference, Collapse Hierarchy, Combine Functions into Class, Combine Functions into Transform, Consolidate Conditional Expression, Decompose Conditional, Encapsulate Collection, Encapsulate Record, Encapsulate Variable, Extract Class, Extract Function, Extract Superclass, Extract Variable, Hide Delegate, Inline Class, Inline Function, Inline Variable, Introduce Assertion, Introduce Parameter Object, Introduce Special Case, Move Field, Move Function, Move Statements into Function, Move Statements to Callers, Parameterize Function, Preserve Whole Object, Pull Up Constructor Body, Pull Up Field, Pull Up Method, Push Down Field, Push Down Method, Remove Dead Code, Remove Flag Argument, Remove Middle Man, Remove Setting Method, Remove Subclass, Rename Field, Rename Variable, Replace Command with Function, Replace Conditional with Polymorphism, Replace Constructor with Factory Function, Replace Control Flag with Break, Replace Derived Variable with Query, Replace Error Code with Exception, Replace Exception with Precheck, Replace Function with Command, Replace Inline Code with Function Call, Replace Loop with Pipeline, Replace Magic Literal, Replace Nested Conditional with Guard Clauses, Replace Parameter with Query, Replace Primitive with Object, Replace Query with Parameter, Replace Subclass with Delegate, Replace Superclass with Delegate, Replace Temp with Query, Replace Type Code with Subclasses, Return Modified Value, Separate Query from Modifier, Slide Statements, Split Loop, Split Phase, Split Variable, Substitute Algorithm.

### The handful that carry most of the weight in this repo

React and TypeScript code is mostly functions and data, not class hierarchies, so in practice these are the ones you will name again and again:

1. **Extract Function** - the answer to Long Function, Duplicated Code, and most Comments smells.
2. **Extract Variable** - name the intermediate expression instead of commenting it.
3. **Replace Nested Conditional with Guard Clauses** - the cure for arrow-shaped code.
4. **Decompose Conditional** - when the condition itself needs a name.
5. **Introduce Parameter Object** - for Data Clumps and Long Parameter List, which in React usually means a prop explosion.
6. **Split Loop** - when one pass is doing two unrelated jobs.
7. **Replace Loop with Pipeline** - map, filter, reduce instead of an accumulator and an index.
8. **Remove Dead Code** - the cheapest improvement anyone ever makes.
9. **Replace Magic Literal** - a bare `0.66` or `'pro'` in a conditional.
10. **Slide Statements** - move related lines together before extracting, which usually makes the extraction obvious.

---

## 4. How to use a name in a finding

Write the smell, then the refactoring, then the concrete edit. The name is a pointer to shared vocabulary, not a substitute for showing the code.

Good:

> **Framework:** Fowler, Long Parameter List -> Introduce Parameter Object
> `DashboardCard` takes 7 positional props, 4 of which are always passed together from the same source object. Grouping them into a single `metric` prop removes the ordering risk and shortens every call site.

Weak:

> This function has a code smell and should be refactored.

The second version gives the author nothing to look up, nothing to disagree with, and nothing to do.
