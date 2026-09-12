# Official React, Next.js and TypeScript guidance

**Sources, all first-party:**
1. https://react.dev/learn/you-might-not-need-an-effect
2. https://nextjs.org/docs/app/getting-started/server-and-client-components
3. https://www.typescriptlang.org/docs/handbook/declaration-files/do-s-and-don-ts.html
4. https://web.dev/articles/vitals

This is the lens that produces most real findings in `15-prototype/` and `16-zomato/` (Next.js 14 App Router, React 18, TypeScript, Tailwind).

## Contents

1. React: the thirteen Effect anti-patterns
2. React: the official recap, verbatim
3. Next.js: Server and Client Component boundaries
4. TypeScript: the do's and don'ts
5. Performance: measure before you claim

---

## 1. React: the thirteen Effect anti-patterns

From "You Might Not Need an Effect". An unnecessary `useEffect` is the single most common real defect in React code, because it adds a render pass, a stale-value risk, and a dependency array nobody maintains. Each row below is a named anti-pattern with the documented fix.

| Anti-pattern | The fix |
|---|---|
| Transforming data for rendering | Calculate it at the top level during render. `const visibleTodos = getFilteredTodos(todos, filter)` |
| Handling user events | Put the logic in the event handler, not an Effect |
| Updating state based on props or state | Do not put calculated values in state. `const fullName = firstName + ' ' + lastName` |
| Caching expensive calculations | `useMemo`, not `useEffect` |
| Resetting all state when a prop changes | Pass a `key`. `<Profile userId={userId} key={userId} />` |
| Adjusting some state when a prop changes | Adjust during rendering, or store the id and derive the object |
| Sharing logic between event handlers | Extract a shared function and call it from both handlers |
| Chains of computations | Compute all the next state in one pass inside the event handler |
| Initializing the application | Run it at module level, or guard with a flag, because Effects fire twice in development |
| Notifying parent components about state changes | Update both pieces of state in the same event handler |
| Passing data to the parent | Let the parent own the fetch and pass data down as props |
| Subscribing to an external store | `useSyncExternalStore` |
| Fetching data | Add a cleanup function and ignore stale responses, or the race condition is real |

When you flag one of these, name it. "Unnecessary Effect: transforming data for rendering" is checkable. "This useEffect looks off" is not.

## 2. React: the official recap, verbatim

> - If you can calculate something during render, you don't need an Effect.
> - To cache expensive calculations, add `useMemo` instead of `useEffect`.
> - To reset the state of an entire component tree, pass a different `key` to it.
> - To reset a particular bit of state in response to a prop change, set it during rendering.
> - Code that runs because a component was *displayed* should be in Effects, the rest should be in events.
> - If you need to update the state of several components, it's better to do it during a single event.
> - Whenever you try to synchronize state variables in different components, consider lifting state up.
> - You can fetch data with Effects, but you need to implement cleanup to avoid race conditions.

---

## 3. Next.js: Server and Client Component boundaries

In the App Router, layouts and pages are Server Components by default. The official split:

**Use Client Components when you need:** state and event handlers (`onClick`, `onChange`), lifecycle logic such as `useEffect`, browser-only APIs (`localStorage`, `window`, geolocation), or custom hooks.

**Use Server Components when you need:** to fetch data close to the source, to use API keys and secrets without exposing them to the client, to reduce the JavaScript sent to the browser, or to improve First Contentful Paint and stream content progressively.

### The rule that produces the most findings

> "Once a file is marked with `'use client'`, **all of its imports and the components it directly renders are included in the client bundle**."

So a `'use client'` at the top of a large layout or page silently drags its whole import graph into the browser bundle. The official guidance is to push the boundary down:

> "To reduce the size of your client JavaScript bundles, add `'use client'` to specific interactive components instead of marking large parts of your UI as Client Components."

The documented example is a `<Layout>` that stays a Server Component while only the interactive `<Search />` inside it is a Client Component.

### The escape hatch that keeps things on the server

The boundary applies to the module graph, not to children:

> "It does not apply to Server Components passed as children or other props. Those components are not imported into the Client Component's module graph. They are rendered on the server and passed to the Client Component as rendered output."

So a Client `<Modal>` taking `{children}` can still wrap a Server `<Cart>`. When you see a whole subtree marked client-side only so it can sit inside a modal or a tab panel, this is the fix.

### Two more from the same page

1. **Context providers go as deep as possible.** "You should render providers as deep as possible in the tree, notice how `ThemeProvider` only wraps `{children}` instead of the entire `<html>` document."
2. **Environment poisoning.** Only `NEXT_PUBLIC_`-prefixed env vars reach the client. A module holding a secret should `import 'server-only'` so misuse becomes a build-time error rather than a silent empty string.

### What to check on a `.tsx` finding

1. Does this file need `'use client'` at all, or only one component inside it does.
2. If it is a Client Component, what does its import graph pull into the bundle.
3. Is there an Effect here that the table in section 1 says should not exist.
4. Is a value recomputed every render that `useMemo` should hold, and is it genuinely expensive rather than a cheap expression wrapped out of habit.

---

## 4. TypeScript: the do's and don'ts

Verbatim rules from the official handbook page.

**General types**

1. Don't ever use the types `Number`, `String`, `Boolean`, `Symbol`, or `Object`. "These types refer to non-primitive boxed objects that are almost never used appropriately in JavaScript code." Do use `number`, `string`, `boolean`, `symbol`, and the non-primitive `object`.
2. Don't ever have a generic type which doesn't use its type parameter.
3. Don't use `any` "unless you are in the process of migrating a JavaScript project to TypeScript. Use `unknown` instead when you don't know the type or want to accept anything you'll pass through without interacting with it."

**Callbacks**

4. Don't use the return type `any` for callbacks whose value will be ignored. Do use `void`, because it "prevents you from accidentally using the return value of `x` in an unchecked way".
5. Don't use optional parameters in callbacks unless you really mean it.
6. Don't write separate overloads that differ only on callback arity. Write a single overload using the maximum arity, since "it's always legal for a callback to disregard a parameter".

**Overloads**

7. Don't put more general overloads before more specific ones, because "TypeScript chooses the first matching overload when resolving function calls".
8. Don't write several overloads that differ only in trailing parameters. Use optional parameters, but only when all overloads share a return type.
9. Don't write overloads that differ by type in only one argument position. Use a union type.

In this repo the ones that actually come up are 1 and 3. An `any` in prototype code is worth a Minor finding, because `npm run typecheck` is the only automated gate here and `any` is precisely what blinds it.

---

## 5. Performance: measure before you claim

Web Vitals (https://web.dev/articles/vitals) is the reference for what "slow" means on the user side. The discipline that matters for a review is narrower.

State a performance finding only when you can point at the mechanism, not a feeling. Legitimate mechanisms in this codebase:

1. A `'use client'` boundary shipping a large import graph to the browser.
2. An Effect chain causing extra render passes, per section 1.
3. A genuinely expensive computation re-running every render with no `useMemo`.
4. Work inside a loop that does not need to be there, or an accidental O(n squared) over a list that can grow.

Not legitimate:

1. Wrapping cheap expressions in `useMemo` or `useCallback` on principle. That adds code and dependency arrays for no measured gain.
2. Micro-optimising a code path that runs once at build time.

Both Fowler and Google land in the same place on this. Restructuring for speed without a measurement is a guess, and a guess presented as a finding costs the author real time.
