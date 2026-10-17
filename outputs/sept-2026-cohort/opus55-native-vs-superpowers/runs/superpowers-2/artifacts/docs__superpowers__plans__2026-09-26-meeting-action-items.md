# Meeting Action Items Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** A web app where the team pastes meeting notes, reviews the extracted action items (owner from a fixed roster, due date worked out from the meeting date), and tracks them on one shared board with a full change history.

**Architecture:** One Next.js 15 (App Router) TypeScript app backed by Postgres through Drizzle. Claude pulls items out of the notes and copies the owner and due-date text exactly as written. Pure, unit-tested functions then decide the owner (roster and alias match, never guessed), the due date, and where each item came from in the notes. A service layer holds all database writes and records every board change in `item_events`. Pages call it through server actions.

**Tech Stack:** Next.js 15, React 19, TypeScript, Auth.js v5 (`next-auth@beta`, Google provider), Drizzle ORM + `pg`, PGlite (tests only), Zod, chrono-node, `@anthropic-ai/sdk` (structured outputs via `client.messages.parse` + `zodOutputFormat`), Vitest, Playwright.

**Spec:** `docs/superpowers/specs/2026-09-26-meeting-action-items-design.md`

## Global Constraints

- Node 20.9+ (Node 22 LTS recommended). Postgres 16 for dev, E2E and production. Tests use PGlite (in-process Postgres), so `npm test` needs no Docker.
- Roster (seeded from `config/roster.json`): Priya, Marcus, Sarah, Tomás, Aisha, Dana, Ravi, Lena. Seed alias: Tomás → `tom`.
- **Owner is never guessed.** It is assigned only when the name exactly matches a normalized display name or alias. Anything else gets a flag.
- Blocking flags: `missing_owner`, `unknown_owner`, `multiple_owners`. Warning flags: `unparsed_due`, `quote_not_found`, `possible_duplicate`.
- Items with status `open`/`done` must have an owner. This is enforced both in the service layer and by the DB check `status = 'draft' OR owner_member_id IS NOT NULL`.
- Notes are limited to 50,000 characters (`MAX_NOTES_CHARS`). Notes text and item text never appear in logs.
- `ALLOWED_DOMAIN` placeholder: `ourcompany.com`. Sign-in requires `email_verified === true`, `hd === ALLOWED_DOMAIN`, and an email ending in `@ALLOWED_DOMAIN`.
- `CLAUDE_MODEL` defaults to `claude-opus-5`. The Anthropic client uses `timeout: 120_000` and `maxRetries: 1`; the extractor retries once more itself if the output is malformed.
- `DATE_LOCALE` defaults to `en-US` (numeric dates are month/day); `en-GB` means day/month.
- `EXTRACTOR=fake` and `AUTH_TEST_BYPASS=1` are for tests only. Both throw when `NODE_ENV=production`.
- Every board change (text, owner, due date, done/reopened) and the initial commit writes an `item_events` row in the same transaction. Alias changes write `roster_events`.
- Import alias: `@/*` → `src/*`.

## Review Focus

1. **Owner written as a handle or with a qualifier** ("@priya", "Priya K.", "Marcus (eng)"). "@priya" should resolve to Priya. The other two must be flagged `unknown_owner`, never assigned. Test: Task 2, `resolveOwner` "handles and qualifiers".
2. **Notes pasted from Word or Google Docs** (CRLF line endings, non-breaking spaces, curly quotes, en dashes) while Claude quotes in plain ASCII. Items should still link to their source text and not get a spurious `quote_not_found`. Tests: Task 4 normalization cases; Task 6 "Word-pasted notes".
3. **The same action listed inline and again in an "Action items" recap.** Both rows appear, and the second is flagged `possible_duplicate` so the reviewer can delete it. Test: Task 6 "recap duplicates".
4. **Double-clicking "Add to board", or two reviewers committing the same draft.** Exactly one set of items and `created` events is written, and the second attempt gets "already on the board". Test: Task 8 "second commit is rejected".
5. **A stale review tab edits a draft that someone else already committed.** The edit is refused with a clear message and doesn't silently change a board item without an audit event. Test: Task 8 "draft edits after commit are refused".

## File Structure

```
config/roster.json                     roster seed
docker-compose.yml, scripts/pg-init.sql  local Postgres (actions_dev, actions_e2e)
drizzle/                               generated SQL migrations
drizzle.config.ts
scripts/migrate.ts, scripts/seed.ts
src/
  auth.ts                              Auth.js config (Google, domain check)
  middleware.ts                        redirect unauthenticated requests
  instrumentation.ts                   refuse test-only flags in production at startup
  lib/
    types.ts                           Flag, RosterEntry, isBlocking
    limits.ts, config.ts, env.ts, errors.ts, flagLabels.ts
    roster/normalize.ts                normalizeName
    roster/resolveOwner.ts             buildKeyIndex, resolveOwner
    roster/aliases.ts                  validateAliases
    roster/suggest.ts                  suggestMemberFromText
    roster/repository.ts               getRoster
    roster/service.ts                  updateAliases
    dates/isoDate.ts                   ISO date arithmetic (UTC, no DST issues)
    dates/resolveDue.ts                resolveDue
    dates/display.ts                   todayLocalIso, isOverdue, formatDue
    notes/locateQuote.ts               locateQuote
    notes/segments.ts                  buildSegments, selectionToRange
    extraction/schema.ts, extractor.ts, prompt.ts,
      claudeExtractor.ts, fakeExtractor.ts, index.ts, buildDraft.ts
    db/schema.ts, db/client.ts, db/seed.ts
    meetings/service.ts                paste → draft → review → commit
    items/service.ts                   board list, edits, done, history
    items/describeEvent.ts
    auth/domain.ts, auth/bypass.ts, auth/requireUser.ts
  app/
    layout.tsx, page.tsx, globals.css
    signin/page.tsx, restricted/page.tsx, api/auth/[...nextauth]/route.ts
    actions/result.ts, meetings.ts, review.ts, board.ts, team.ts
    new/page.tsx, new/PasteForm.tsx
    meetings/[id]/page.tsx             read-only notes view
    meetings/[id]/review/page.tsx, ReviewWorkspace.tsx, ItemRow.tsx
    components/NotesPane.tsx, components/FlagBadges.tsx
    board/page.tsx, board/BoardTable.tsx, board/HistoryPanel.tsx
    team/page.tsx, team/TeamEditor.tsx
tests/
  fixtures/roster.ts
  helpers/testDb.ts, helpers/factories.ts
  unit/…, integration/…, e2e/…
eval/golden/*.json, eval/score.ts, eval/run-eval.ts
```

---

### Task 1: Project scaffold and tooling

**Files:**
- Create: `package.json`, `tsconfig.json`, `next.config.ts`, `vitest.config.ts`, `.gitignore`, `.env.example`, `docker-compose.yml`, `scripts/pg-init.sql`
- Create: `src/app/layout.tsx`, `src/app/page.tsx`, `src/app/globals.css`, `src/lib/types.ts`
- Test: `tests/unit/types.test.ts`

**Interfaces:**
- Produces: `Flag`, `BlockingFlag`, `WarningFlag`, `BLOCKING_FLAGS`, `WARNING_FLAGS`, `isBlocking(flag: Flag): boolean`, `RosterEntry { id: string; displayName: string; aliases: string[] }` from `src/lib/types.ts`.

- [ ] **Step 1: Write `package.json`**

The directory already contains `docs/` and `.git`, and `create-next-app` refuses to run in a non-empty directory. Scaffold by hand instead:

```json
{
  "name": "meeting-action-items",
  "private": true,
  "engines": { "node": ">=20.9" },
  "scripts": {
    "dev": "next dev",
    "build": "next build",
    "start": "next start",
    "typecheck": "tsc --noEmit",
    "test": "vitest run",
    "test:watch": "vitest",
    "e2e": "playwright test",
    "db:generate": "drizzle-kit generate",
    "db:migrate": "tsx --env-file=.env.local scripts/migrate.ts",
    "db:seed": "tsx --env-file=.env.local scripts/seed.ts",
    "eval": "tsx --env-file=.env.local eval/run-eval.ts"
  }
}
```

- [ ] **Step 2: Install dependencies**

```bash
npm install next@15 react@19 react-dom@19 next-auth@beta @anthropic-ai/sdk drizzle-orm pg chrono-node
npm view @anthropic-ai/sdk peerDependencies
```

Install the `zod` major version that the SDK's `zod` peer range allows. For example, if the peer range is `^3.25.0 || ^4.0.0`, run `npm install zod@^4`:

```bash
npm install zod@<major from the peer range>
npm install -D typescript @types/node @types/react @types/react-dom @types/pg vitest drizzle-kit @electric-sql/pglite tsx @playwright/test
npx playwright install chromium
```

- [ ] **Step 3: Write config files**

`tsconfig.json`:

```json
{
  "compilerOptions": {
    "target": "ES2022",
    "lib": ["dom", "dom.iterable", "es2022"],
    "skipLibCheck": true,
    "strict": true,
    "noEmit": true,
    "esModuleInterop": true,
    "module": "esnext",
    "moduleResolution": "bundler",
    "resolveJsonModule": true,
    "isolatedModules": true,
    "jsx": "preserve",
    "incremental": true,
    "plugins": [{ "name": "next" }],
    "paths": { "@/*": ["./src/*"] }
  },
  "include": ["next-env.d.ts", "**/*.ts", "**/*.tsx", ".next/types/**/*.ts"],
  "exclude": ["node_modules"]
}
```

`next.config.ts`:

```ts
import type { NextConfig } from "next";

const nextConfig: NextConfig = {
  serverExternalPackages: ["pg"],
};

export default nextConfig;
```

`vitest.config.ts`:

```ts
import { fileURLToPath } from "node:url";
import { defineConfig } from "vitest/config";

export default defineConfig({
  resolve: { alias: { "@": fileURLToPath(new URL("./src", import.meta.url)) } },
  test: {
    environment: "node",
    include: ["tests/unit/**/*.test.ts", "tests/integration/**/*.test.ts"],
    testTimeout: 20_000,
  },
});
```

`.gitignore`:

```
node_modules/
.next/
next-env.d.ts
.env
.env*.local
test-results/
playwright-report/
*.tsbuildinfo
```

`.env.example`:

```
DATABASE_URL=postgres://postgres:postgres@localhost:5432/actions_dev
# generate with: npx auth secret
AUTH_SECRET=
AUTH_GOOGLE_ID=
AUTH_GOOGLE_SECRET=
AUTH_TRUST_HOST=true
# Placeholder - replace with the real Google Workspace domain before launch
ALLOWED_DOMAIN=ourcompany.com
ANTHROPIC_API_KEY=
# CLAUDE_MODEL=claude-opus-5
# DATE_LOCALE=en-US
# Local development without the Claude API (never in production):
# EXTRACTOR=fake
```

`docker-compose.yml`:

```yaml
services:
  postgres:
    image: postgres:16
    environment:
      POSTGRES_USER: postgres
      POSTGRES_PASSWORD: postgres
    ports:
      - "5432:5432"
    volumes:
      - ./scripts/pg-init.sql:/docker-entrypoint-initdb.d/pg-init.sql:ro
      - pgdata:/var/lib/postgresql/data
volumes:
  pgdata:
```

`scripts/pg-init.sql`:

```sql
CREATE DATABASE actions_dev;
CREATE DATABASE actions_e2e;
```

- [ ] **Step 4: Write the failing test**

`tests/unit/types.test.ts`:

```ts
import { describe, expect, it } from "vitest";
import { BLOCKING_FLAGS, WARNING_FLAGS, isBlocking } from "@/lib/types";

describe("flags", () => {
  it("treats owner flags as blocking", () => {
    for (const f of BLOCKING_FLAGS) expect(isBlocking(f)).toBe(true);
  });
  it("treats warning flags as non-blocking", () => {
    for (const f of WARNING_FLAGS) expect(isBlocking(f)).toBe(false);
  });
});
```

- [ ] **Step 5: Run it and confirm it fails**

Run: `npm test`
Expected: FAIL. Cannot resolve `@/lib/types`.

- [ ] **Step 6: Write `src/lib/types.ts` and the minimal app shell**

`src/lib/types.ts`:

```ts
export const BLOCKING_FLAGS = ["missing_owner", "unknown_owner", "multiple_owners"] as const;
export const WARNING_FLAGS = ["unparsed_due", "quote_not_found", "possible_duplicate"] as const;

export type BlockingFlag = (typeof BLOCKING_FLAGS)[number];
export type WarningFlag = (typeof WARNING_FLAGS)[number];
export type Flag = BlockingFlag | WarningFlag;

export function isBlocking(flag: Flag): flag is BlockingFlag {
  return (BLOCKING_FLAGS as readonly string[]).includes(flag);
}

export interface RosterEntry {
  id: string;
  displayName: string;
  aliases: string[];
}
```

`src/app/layout.tsx`:

```tsx
import "./globals.css";

export const metadata = { title: "Meeting Action Items" };

export default function RootLayout({ children }: { children: React.ReactNode }) {
  return (
    <html lang="en">
      <body>
        <main>{children}</main>
      </body>
    </html>
  );
}
```

`src/app/page.tsx`:

```tsx
import { redirect } from "next/navigation";

export default function Home() {
  redirect("/board");
}
```

`src/app/globals.css`:

```css
* { box-sizing: border-box; }
body { font-family: system-ui, sans-serif; margin: 0; color: #1a1a1a; }
main { padding: 1rem 1.5rem; max-width: 1200px; margin: 0 auto; }
.topbar { display: flex; justify-content: space-between; align-items: center; padding: 0.5rem 1.5rem; border-bottom: 1px solid #ddd; }
.topbar nav { display: flex; gap: 1rem; }
.narrow { max-width: 480px; }
.stack { display: flex; flex-direction: column; gap: 0.75rem; }
.row { display: flex; gap: 0.5rem; align-items: center; flex-wrap: wrap; }
.muted { color: #666; font-size: 0.875rem; }
.error { color: #b00020; }
.warning { background: #fff4e5; border: 1px solid #f0b050; padding: 0.5rem 0.75rem; }
.overdue { color: #b00020; font-weight: 600; }
.review-grid { display: grid; grid-template-columns: 1fr 1fr; gap: 1.5rem; align-items: start; }
.notes { white-space: pre-wrap; font-family: ui-monospace, monospace; font-size: 0.85rem; background: #fafafa; padding: 0.75rem; max-height: 75vh; overflow: auto; }
.notes mark { background: #fff1a8; cursor: pointer; }
.notes mark.active { background: #ffd24d; }
.items { list-style: none; padding: 0; display: flex; flex-direction: column; gap: 0.75rem; }
.items li { border: 1px solid #ddd; padding: 0.5rem 0.75rem; }
.items li.blocked { border-color: #b00020; }
.flag { display: inline-block; font-size: 0.75rem; padding: 0.1rem 0.4rem; border-radius: 3px; background: #eee; margin-right: 0.25rem; }
.flag.blocking { background: #fde0e0; color: #8a0015; }
button.link { background: none; border: none; color: #0645ad; cursor: pointer; padding: 0; }
table.board { width: 100%; border-collapse: collapse; }
table.board td, table.board th { border-bottom: 1px solid #eee; padding: 0.4rem; text-align: left; vertical-align: top; }
```

- [ ] **Step 7: Run tests, typecheck and build**

Run: `npm test && npm run typecheck && npm run build`
Expected: 2 tests PASS, no type errors, and the build succeeds. (`/board` doesn't exist yet. That's fine: the redirect only happens at request time.)

- [ ] **Step 8: Commit**

```bash
git add -A
git commit -m "chore: scaffold Next.js app, test tooling and shared flag types"
```

---

### Task 2: Roster matching (normalize, resolveOwner, aliases, suggestions)

**Files:**
- Create: `src/lib/roster/normalize.ts`, `src/lib/roster/resolveOwner.ts`, `src/lib/roster/aliases.ts`, `src/lib/roster/suggest.ts`, `tests/fixtures/roster.ts`
- Test: `tests/unit/roster/normalize.test.ts`, `tests/unit/roster/resolveOwner.test.ts`, `tests/unit/roster/aliases.test.ts`, `tests/unit/roster/suggest.test.ts`

**Interfaces:**
- Consumes: `RosterEntry` (Task 1).
- Produces:
  - `normalizeName(input: string): string`
  - `buildKeyIndex(roster: RosterEntry[]): Map<string, string>`: maps a normalized key to a member id. Keys claimed by two members are left out.
  - `type OwnerResolution = { kind: "assigned"; memberId: string } | { kind: "flagged"; flag: "missing_owner" | "unknown_owner" | "multiple_owners"; suggestions: string[] }`
  - `resolveOwner(mention: string | null, roster: RosterEntry[]): OwnerResolution`
  - `type AliasValidation = { ok: true; aliases: string[] } | { ok: false; error: string }`
  - `validateAliases(roster: RosterEntry[], memberId: string, rawAliases: string[]): AliasValidation`
  - `suggestMemberFromText(text: string, roster: RosterEntry[]): string | null`

- [ ] **Step 1: Write the roster fixture and failing tests**

`tests/fixtures/roster.ts`:

```ts
import type { RosterEntry } from "@/lib/types";

export const ROSTER: RosterEntry[] = [
  { id: "m-priya", displayName: "Priya", aliases: ["pk"] },
  { id: "m-marcus", displayName: "Marcus", aliases: [] },
  { id: "m-sarah", displayName: "Sarah", aliases: [] },
  { id: "m-tomas", displayName: "Tomás", aliases: ["tom"] },
  { id: "m-aisha", displayName: "Aisha", aliases: [] },
  { id: "m-dana", displayName: "Dana", aliases: [] },
  { id: "m-ravi", displayName: "Ravi", aliases: [] },
  { id: "m-lena", displayName: "Lena", aliases: [] },
];
```

`tests/unit/roster/normalize.test.ts`:

```ts
import { describe, expect, it } from "vitest";
import { normalizeName } from "@/lib/roster/normalize";

describe("normalizeName", () => {
  it.each([
    ["Tomás", "tomas"],
    ["  PRIYA ", "priya"],
    ["Priya's", "priya"],
    ["Priya’s", "priya"],
    ["@priya", "priya"],
    ["Marcus.", "marcus"],
    ["(Dana)", "dana"],
    ["Priya   K.", "priya k"],
    ["", ""],
    ["  ,; ", ""],
  ])("%j -> %j", (input, expected) => {
    expect(normalizeName(input)).toBe(expected);
  });
});
```

`tests/unit/roster/resolveOwner.test.ts`:

```ts
import { describe, expect, it } from "vitest";
import { resolveOwner } from "@/lib/roster/resolveOwner";
import { ROSTER } from "../../fixtures/roster";

describe("resolveOwner", () => {
  it.each([
    ["Priya", "m-priya"],
    ["PK", "m-priya"],
    ["Tom", "m-tomas"],
    ["Tomas", "m-tomas"],
    ["Tomás", "m-tomas"],
    ["Priya's", "m-priya"],
    ["Tom / Tomás", "m-tomas"],
  ])("assigns %j", (mention, memberId) => {
    expect(resolveOwner(mention, ROSTER)).toEqual({ kind: "assigned", memberId });
  });

  it.each([[null], [""], ["   "]])("flags missing owner for %j", (mention) => {
    expect(resolveOwner(mention, ROSTER)).toEqual({ kind: "flagged", flag: "missing_owner", suggestions: [] });
  });

  it.each([["Tommy"], ["Sam"], ["team"], ["everyone"], ["legal"], ["Tom and legal"]])(
    "flags unknown owner for %j (never guesses)",
    (mention) => {
      expect(resolveOwner(mention, ROSTER)).toEqual({ kind: "flagged", flag: "unknown_owner", suggestions: [] });
    },
  );

  it("handles and qualifiers: @handle resolves, surname initial or role is flagged", () => {
    expect(resolveOwner("@ravi", ROSTER)).toEqual({ kind: "assigned", memberId: "m-ravi" });
    expect(resolveOwner("Priya K.", ROSTER)).toMatchObject({ kind: "flagged", flag: "unknown_owner" });
    expect(resolveOwner("Marcus (eng)", ROSTER)).toMatchObject({ kind: "flagged", flag: "unknown_owner" });
  });

  it("flags multiple owners with suggestions in mention order", () => {
    expect(resolveOwner("Tom and Priya", ROSTER)).toEqual({
      kind: "flagged",
      flag: "multiple_owners",
      suggestions: ["m-tomas", "m-priya"],
    });
    expect(resolveOwner("Lena, Dana & Ravi", ROSTER)).toEqual({
      kind: "flagged",
      flag: "multiple_owners",
      suggestions: ["m-lena", "m-dana", "m-ravi"],
    });
  });

  it("never assigns a key that two members share", () => {
    const clashing = [
      { id: "a", displayName: "Sam A", aliases: ["sam"] },
      { id: "b", displayName: "Sam B", aliases: ["sam"] },
    ];
    expect(resolveOwner("Sam", clashing)).toMatchObject({ kind: "flagged", flag: "unknown_owner" });
  });
});
```

`tests/unit/roster/aliases.test.ts`:

```ts
import { describe, expect, it } from "vitest";
import { validateAliases } from "@/lib/roster/aliases";
import { ROSTER } from "../../fixtures/roster";

describe("validateAliases", () => {
  it("normalizes, drops blanks and dedupes", () => {
    expect(validateAliases(ROSTER, "m-tomas", ["Tom", " tommy ", "TOM", ""])).toEqual({
      ok: true,
      aliases: ["tom", "tommy"],
    });
  });
  it("rejects an alias that normalizes to nothing", () => {
    expect(validateAliases(ROSTER, "m-tomas", ["!!!"])).toEqual({ ok: false, error: "“!!!” isn't a usable alias" });
  });
  it("rejects a clash with another member's display name", () => {
    expect(validateAliases(ROSTER, "m-tomas", ["Priya"])).toEqual({
      ok: false,
      error: "“priya” is already used by Priya",
    });
  });
  it("rejects a clash with another member's alias", () => {
    expect(validateAliases(ROSTER, "m-ravi", ["tom"])).toEqual({
      ok: false,
      error: "“tom” is already used by Tomás",
    });
  });
});
```

`tests/unit/roster/suggest.test.ts`:

```ts
import { describe, expect, it } from "vitest";
import { suggestMemberFromText } from "@/lib/roster/suggest";
import { ROSTER } from "../../fixtures/roster";

describe("suggestMemberFromText", () => {
  it("suggests the single roster member named in the text", () => {
    expect(suggestMemberFromText("Tom will send the deck", ROSTER)).toBe("m-tomas");
    expect(suggestMemberFromText("Lena will draft the FAQ", ROSTER)).toBe("m-lena");
  });
  it("returns null when two members are named", () => {
    expect(suggestMemberFromText("Priya and Tom to sync", ROSTER)).toBeNull();
  });
  it("matches whole words only", () => {
    expect(suggestMemberFromText("Tomorrow we ship", ROSTER)).toBeNull();
  });
  it("returns null when nobody is named", () => {
    expect(suggestMemberFromText("Book the venue", ROSTER)).toBeNull();
  });
});
```

- [ ] **Step 2: Run them and confirm they fail**

Run: `npm test -- tests/unit/roster`
Expected: FAIL. The modules don't exist yet.

- [ ] **Step 3: Implement**

`src/lib/roster/normalize.ts`:

```ts
const EDGE_PUNCTUATION = /^[^\p{L}\p{N}]+|[^\p{L}\p{N}]+$/gu;

export function normalizeName(input: string): string {
  let s = input.normalize("NFD").replace(/\p{M}+/gu, "").toLowerCase();
  s = s.replace(/\s+/g, " ").trim();
  s = s.replace(EDGE_PUNCTUATION, "");
  s = s.replace(/['’]s$/u, "");
  s = s.replace(EDGE_PUNCTUATION, "");
  return s;
}
```

`src/lib/roster/resolveOwner.ts`:

```ts
import type { RosterEntry } from "../types";
import { normalizeName } from "./normalize";

export type OwnerResolution =
  | { kind: "assigned"; memberId: string }
  | { kind: "flagged"; flag: "missing_owner" | "unknown_owner" | "multiple_owners"; suggestions: string[] };

export function buildKeyIndex(roster: RosterEntry[]): Map<string, string> {
  const index = new Map<string, string>();
  const conflicted = new Set<string>();
  for (const member of roster) {
    for (const key of [member.displayName, ...member.aliases].map(normalizeName)) {
      if (key === "") continue;
      const existing = index.get(key);
      if (existing !== undefined && existing !== member.id) conflicted.add(key);
      else index.set(key, member.id);
    }
  }
  for (const key of conflicted) index.delete(key);
  return index;
}

const SEPARATORS = /\s*(?:,|&|\/|\band\b)\s*/i;

export function resolveOwner(mention: string | null, roster: RosterEntry[]): OwnerResolution {
  if (mention === null || normalizeName(mention) === "") {
    return { kind: "flagged", flag: "missing_owner", suggestions: [] };
  }
  const index = buildKeyIndex(roster);
  const whole = index.get(normalizeName(mention));
  if (whole) return { kind: "assigned", memberId: whole };

  const parts = mention.split(SEPARATORS).map(normalizeName).filter((p) => p !== "");
  if (parts.length > 1) {
    const ids = parts.map((p) => index.get(p));
    if (ids.every((id): id is string => id !== undefined)) {
      const distinct = [...new Set(ids)];
      if (distinct.length === 1) return { kind: "assigned", memberId: distinct[0] };
      return { kind: "flagged", flag: "multiple_owners", suggestions: distinct };
    }
  }
  return { kind: "flagged", flag: "unknown_owner", suggestions: [] };
}
```

`src/lib/roster/aliases.ts`:

```ts
import type { RosterEntry } from "../types";
import { normalizeName } from "./normalize";

export type AliasValidation = { ok: true; aliases: string[] } | { ok: false; error: string };

export function validateAliases(roster: RosterEntry[], memberId: string, rawAliases: string[]): AliasValidation {
  const aliases: string[] = [];
  for (const raw of rawAliases) {
    if (raw.trim() === "") continue;
    const key = normalizeName(raw);
    if (key === "") return { ok: false, error: `“${raw.trim()}” isn't a usable alias` };
    if (!aliases.includes(key)) aliases.push(key);
  }
  for (const other of roster) {
    if (other.id === memberId) continue;
    const otherKeys = [other.displayName, ...other.aliases].map(normalizeName);
    const clash = aliases.find((a) => otherKeys.includes(a));
    if (clash) return { ok: false, error: `“${clash}” is already used by ${other.displayName}` };
  }
  return { ok: true, aliases };
}
```

`src/lib/roster/suggest.ts`:

```ts
import type { RosterEntry } from "../types";
import { buildKeyIndex } from "./resolveOwner";

const escapeRegExp = (s: string) => s.replace(/[.*+?^${}()|[\]\\]/g, "\\$&");

export function suggestMemberFromText(text: string, roster: RosterEntry[]): string | null {
  const haystack = text.normalize("NFD").replace(/\p{M}+/gu, "").toLowerCase();
  const found = new Set<string>();
  for (const [key, memberId] of buildKeyIndex(roster)) {
    const pattern = new RegExp(`(?<![\\p{L}\\p{N}])${escapeRegExp(key)}(?![\\p{L}\\p{N}])`, "u");
    if (pattern.test(haystack)) found.add(memberId);
  }
  return found.size === 1 ? [...found][0] : null;
}
```

- [ ] **Step 4: Run the tests and confirm they pass**

Run: `npm test -- tests/unit/roster`
Expected: all PASS.

- [ ] **Step 5: Commit**

```bash
git add src/lib/roster tests/fixtures tests/unit/roster
git commit -m "feat: roster owner matching with aliases, never guessing"
```

---

### Task 3: Due-date resolution

**Files:**
- Create: `src/lib/dates/isoDate.ts`, `src/lib/dates/resolveDue.ts`
- Test: `tests/unit/dates/resolveDue.test.ts`

**Interfaces:**
- Produces:
  - `isIsoDate(s: string): boolean`, `addDays(iso: string, n: number): string`, `weekdayOf(iso: string): number` (0 = Sunday), `lastDayOfMonth(iso: string): string`, `isoFromParts(y: number, m: number, d: number): string`
  - `interface DueResolution { dueDate: string | null; flag: "unparsed_due" | null }`
  - `resolveDue(mention: string | null, meetingDate: string, locale?: string): DueResolution`

Reference weekdays: 2026-09-26 is a Saturday, 2026-09-30 a Wednesday, 2026-10-02 a Friday, and 2026-12-30 a Wednesday.

- [ ] **Step 1: Write the failing test**

`tests/unit/dates/resolveDue.test.ts`:

```ts
import { describe, expect, it } from "vitest";
import { isIsoDate } from "@/lib/dates/isoDate";
import { resolveDue } from "@/lib/dates/resolveDue";

const WED = "2026-09-30";
const ok = (dueDate: string) => ({ dueDate, flag: null });
const UNPARSED = { dueDate: null, flag: "unparsed_due" };

describe("resolveDue", () => {
  it("treats no mention as no date, without a flag", () => {
    expect(resolveDue(null, WED)).toEqual({ dueDate: null, flag: null });
    expect(resolveDue("   ", WED)).toEqual({ dueDate: null, flag: null });
  });

  it.each([
    ["Friday", "2026-10-02"],
    ["by Friday", "2026-10-02"],
    ["By Friday.", "2026-10-02"],
    ["fri", "2026-10-02"],
    ["this Friday", "2026-10-02"],
    ["Wednesday", "2026-10-07"],
    ["tomorrow", "2026-10-01"],
    ["today", WED],
    ["EOD", WED],
    ["next week", "2026-10-05"],
    ["end of week", "2026-10-02"],
    ["by the end of the week", "2026-10-02"],
    ["EOW", "2026-10-02"],
    ["end of month", "2026-09-30"],
    ["Oct 3", "2026-10-03"],
    ["October 3rd", "2026-10-03"],
    ["10/3", "2026-10-03"],
    ["Sep 1", "2027-09-01"],
  ])("%j on Wed 2026-09-30 -> %s", (mention, expected) => {
    expect(resolveDue(mention, WED)).toEqual(ok(expected));
  });

  it("reads numeric dates day-first for en-GB", () => {
    expect(resolveDue("3/10", WED, "en-GB")).toEqual(ok("2026-10-03"));
  });

  it.each([["next Friday"], ["ASAP"], ["when possible"]])("does not resolve %j", (mention) => {
    expect(resolveDue(mention, WED)).toEqual(UNPARSED);
  });

  it("handles weekend meetings", () => {
    expect(resolveDue("end of week", "2026-09-26")).toEqual(ok("2026-10-02")); // Saturday
    expect(resolveDue("end of week", "2026-09-27")).toEqual(ok("2026-10-02")); // Sunday
    expect(resolveDue("next week", "2026-09-27")).toEqual(ok("2026-09-28"));
    expect(resolveDue("end of week", "2026-10-02")).toEqual(ok("2026-10-02")); // Friday itself
    expect(resolveDue("Friday", "2026-10-02")).toEqual(ok("2026-10-09"));
  });

  it("rolls over month and year boundaries", () => {
    expect(resolveDue("Friday", "2026-12-30")).toEqual(ok("2027-01-01"));
    expect(resolveDue("Jan 5", "2026-12-30")).toEqual(ok("2027-01-05"));
    expect(resolveDue("end of month", "2026-12-30")).toEqual(ok("2026-12-31"));
    expect(resolveDue("tomorrow", "2026-01-31")).toEqual(ok("2026-02-01"));
    expect(resolveDue("tomorrow", "2028-02-28")).toEqual(ok("2028-02-29"));
  });
});

describe("isIsoDate", () => {
  it("accepts real dates only", () => {
    expect(isIsoDate("2026-09-30")).toBe(true);
    expect(isIsoDate("2026-02-30")).toBe(false);
    expect(isIsoDate("30/09/2026")).toBe(false);
  });
});
```

- [ ] **Step 2: Run it and confirm it fails**

Run: `npm test -- tests/unit/dates`
Expected: FAIL. The modules don't exist yet.

- [ ] **Step 3: Implement**

`src/lib/dates/isoDate.ts`:

```ts
const ISO = /^(\d{4})-(\d{2})-(\d{2})$/;

function toUtc(iso: string): Date {
  const m = ISO.exec(iso);
  if (!m) throw new Error(`Invalid ISO date: ${iso}`);
  return new Date(Date.UTC(Number(m[1]), Number(m[2]) - 1, Number(m[3])));
}

function fromUtc(d: Date): string {
  return d.toISOString().slice(0, 10);
}

export function isIsoDate(s: string): boolean {
  return ISO.test(s) && fromUtc(toUtc(s)) === s;
}

export function addDays(iso: string, n: number): string {
  const d = toUtc(iso);
  d.setUTCDate(d.getUTCDate() + n);
  return fromUtc(d);
}

export function weekdayOf(iso: string): number {
  return toUtc(iso).getUTCDay();
}

export function lastDayOfMonth(iso: string): string {
  const d = toUtc(iso);
  return fromUtc(new Date(Date.UTC(d.getUTCFullYear(), d.getUTCMonth() + 1, 0)));
}

export function isoFromParts(y: number, m: number, d: number): string {
  return `${String(y).padStart(4, "0")}-${String(m).padStart(2, "0")}-${String(d).padStart(2, "0")}`;
}
```

`src/lib/dates/resolveDue.ts`:

```ts
import * as chrono from "chrono-node";
import { addDays, isoFromParts, lastDayOfMonth, weekdayOf } from "./isoDate";

export interface DueResolution {
  dueDate: string | null;
  flag: "unparsed_due" | null;
}

const UNPARSED: DueResolution = { dueDate: null, flag: "unparsed_due" };
const FILLER = /^(?:by|before|due|on|until|till|no later than)\s+/;

const WEEKDAYS: Record<string, number> = {
  sunday: 0, sun: 0,
  monday: 1, mon: 1,
  tuesday: 2, tue: 2, tues: 2,
  wednesday: 3, wed: 3,
  thursday: 4, thu: 4, thur: 4, thurs: 4,
  friday: 5, fri: 5,
  saturday: 6, sat: 6,
};

/** Returns a date, `null` for a recognised-but-ambiguous phrase, or `undefined` if not a relative phrase. */
function resolveRelative(text: string, meetingDate: string): string | null | undefined {
  const wd = weekdayOf(meetingDate);
  if (["today", "eod", "end of day", "end of today"].includes(text)) return meetingDate;
  if (text === "tomorrow") return addDays(meetingDate, 1);
  if (text === "next week") return addDays(meetingDate, (1 - wd + 7) % 7 || 7);
  if (["end of week", "end of the week", "eow", "this week"].includes(text)) {
    return addDays(meetingDate, wd === 6 ? 6 : 5 - wd);
  }
  if (["end of month", "end of the month", "eom", "this month"].includes(text)) return lastDayOfMonth(meetingDate);
  const m = /^(this |next )?([a-z]+)$/.exec(text);
  if (m && Object.hasOwn(WEEKDAYS, m[2])) {
    if (m[1] === "next ") return null;
    return addDays(meetingDate, (WEEKDAYS[m[2]] - wd + 7) % 7 || 7);
  }
  return undefined;
}

function resolveExplicit(text: string, meetingDate: string, locale: string): string | null {
  const [y, mo, d] = meetingDate.split("-").map(Number);
  const reference = new Date(y, mo - 1, d, 12, 0, 0);
  const parser = locale.toLowerCase() === "en-gb" ? chrono.en.GB : chrono.en.casual;
  const results = parser.parse(text, reference);
  if (results.length !== 1) return null;
  const start = results[0].start;
  if (!start.isCertain("day") || !start.isCertain("month")) return null;
  const dt = start.date();
  let iso = isoFromParts(dt.getFullYear(), dt.getMonth() + 1, dt.getDate());
  if (!start.isCertain("year") && iso < meetingDate) {
    iso = isoFromParts(dt.getFullYear() + 1, dt.getMonth() + 1, dt.getDate());
  }
  return iso;
}

export function resolveDue(mention: string | null, meetingDate: string, locale = "en-US"): DueResolution {
  if (mention === null) return { dueDate: null, flag: null };
  let text = mention.toLowerCase().replace(/\s+/g, " ").trim();
  while (FILLER.test(text)) text = text.replace(FILLER, "");
  text = text.replace(/^the\s+/, "").replace(/[.!,;]+$/, "").trim();
  if (text === "") return { dueDate: null, flag: null };

  const relative = resolveRelative(text, meetingDate);
  if (relative !== undefined) return relative === null ? UNPARSED : { dueDate: relative, flag: null };

  const explicit = resolveExplicit(text, meetingDate, locale);
  return explicit ? { dueDate: explicit, flag: null } : UNPARSED;
}
```

- [ ] **Step 4: Run the tests and confirm they pass**

Run: `npm test -- tests/unit/dates`
Expected: all PASS. If only the chrono cases fail (`Oct 3`, `10/3`, `3/10` with en-GB), print `chrono.en.GB` and `chrono.en.casual` to check which parser names the installed chrono-node version exports. Keep the rules in `resolveDue` unchanged.

- [ ] **Step 5: Commit**

```bash
git add src/lib/dates tests/unit/dates
git commit -m "feat: resolve due dates relative to the meeting date"
```

---

### Task 4: Source quote location

**Files:**
- Create: `src/lib/notes/locateQuote.ts`
- Test: `tests/unit/notes/locateQuote.test.ts`

**Interfaces:**
- Produces: `interface QuoteRange { start: number; end: number }` and `locateQuote(quote: string, notes: string): QuoteRange | null`. The range indexes into the original `notes` string, so `notes.slice(start, end)` returns the original text.

- [ ] **Step 1: Write the failing test**

`tests/unit/notes/locateQuote.test.ts`:

```ts
import { describe, expect, it } from "vitest";
import { locateQuote } from "@/lib/notes/locateQuote";

function sliceFor(quote: string, notes: string) {
  const r = locateQuote(quote, notes);
  return r ? notes.slice(r.start, r.end) : null;
}

describe("locateQuote", () => {
  it("finds an exact substring (first occurrence)", () => {
    const notes = "Intro\nTom to send deck\nTom to send deck";
    expect(locateQuote("Tom to send deck", notes)).toEqual({ start: 6, end: 22 });
  });

  it("ignores surrounding whitespace in the quote", () => {
    expect(sliceFor("  Tom to send deck \n", "x Tom to send deck y")).toBe("Tom to send deck");
  });

  it("matches across CRLF and repeated spaces", () => {
    const notes = "Priya to  review\r\npricing today";
    expect(sliceFor("Priya to review pricing", notes)).toBe("Priya to  review\r\npricing");
  });

  it("matches non-breaking spaces, curly quotes and en dashes pasted from Word/Docs", () => {
    const notes = "Dana to “own” the Q4–plan";
    expect(sliceFor('Dana to "own" the Q4-plan', notes)).toBe(notes);
  });

  it("returns null when the quote is not in the notes", () => {
    expect(locateQuote("Ravi to book venue", "Nothing like that here")).toBeNull();
  });

  it("returns null for an empty quote", () => {
    expect(locateQuote("   ", "anything")).toBeNull();
  });
});
```

- [ ] **Step 2: Run it and confirm it fails**

Run: `npm test -- tests/unit/notes`
Expected: FAIL. The module doesn't exist yet.

- [ ] **Step 3: Implement**

`src/lib/notes/locateQuote.ts`:

```ts
export interface QuoteRange {
  start: number;
  end: number;
}

const CHAR_MAP: Record<string, string> = {
  "‘": "'", "’": "'", "‚": "'", "‛": "'",
  "“": '"', "”": '"', "„": '"', "‟": '"',
  "–": "-", "—": "-",
};

function canon(ch: string): string {
  if (/\s/.test(ch)) return " "; // includes \r, \n, \t, NBSP, narrow NBSP
  return CHAR_MAP[ch] ?? ch;
}

/** Normalized text plus, for each normalized char, its index in the original. */
function normalizeWithMap(s: string): { text: string; map: number[] } {
  let text = "";
  const map: number[] = [];
  for (let i = 0; i < s.length; i++) {
    const c = canon(s[i]);
    if (c === " " && text.endsWith(" ")) continue;
    text += c;
    map.push(i);
  }
  return { text, map };
}

export function locateQuote(quote: string, notes: string): QuoteRange | null {
  const q = quote.trim();
  if (q === "") return null;

  const exact = notes.indexOf(q);
  if (exact !== -1) return { start: exact, end: exact + q.length };

  const n = normalizeWithMap(notes);
  const nq = normalizeWithMap(q).text.trim();
  if (nq === "") return null;
  const idx = n.text.indexOf(nq);
  if (idx === -1) return null;
  return { start: n.map[idx], end: n.map[idx + nq.length - 1] + 1 };
}
```

- [ ] **Step 4: Run the tests and confirm they pass**

Run: `npm test -- tests/unit/notes`
Expected: all PASS.

- [ ] **Step 5: Commit**

```bash
git add src/lib/notes tests/unit/notes
git commit -m "feat: locate source quotes in pasted notes, tolerant of Word/Docs formatting"
```

---

### Task 5: Extraction module (Claude + fake)

**Files:**
- Create: `src/lib/extraction/schema.ts`, `src/lib/extraction/extractor.ts`, `src/lib/extraction/prompt.ts`, `src/lib/extraction/claudeExtractor.ts`, `src/lib/extraction/fakeExtractor.ts`, `src/lib/extraction/index.ts`
- Test: `tests/unit/extraction/claudeExtractor.test.ts`, `tests/unit/extraction/fakeExtractor.test.ts`

**Interfaces:**
- Produces:
  - `ExtractedItemSchema`, `ExtractionSchema`, `type ExtractedItem = { text: string; owner_mention: string | null; due_mention: string | null; source_quote: string }`, `type Extraction = { items: ExtractedItem[] }`
  - `interface Extractor { extract(notes: string): Promise<ExtractedItem[]> }`, `class ExtractionError extends Error`
  - `EXTRACTION_SYSTEM_PROMPT`, `buildUserMessage(notes: string): string`
  - `DEFAULT_MODEL = "claude-opus-5"`, `type ParseFn`, `createClaudeExtractor({ model, parse }): Extractor`, `createClaudeExtractorFromEnv(): Extractor`
  - `FAKE_FAILURE_MARKER`, `createLineFakeExtractor(): Extractor`. The fake reads lines like `- ACTION: <text> | owner: <name> | due: <when>`.
  - `assertExtractorConfig(env?)`, `getExtractor(env?): Extractor`

SDK usage follows the bundled Claude API skill's TypeScript structured-outputs example: `client.messages.parse({ …, output_config: { format: zodOutputFormat(schema) } })`, then read `response.parsed_output` (which is null if parsing failed). Check `stop_reason` before reading output.

- [ ] **Step 1: Write the failing tests**

`tests/unit/extraction/claudeExtractor.test.ts`:

```ts
import Anthropic from "@anthropic-ai/sdk";
import { describe, expect, it, vi } from "vitest";
import { createClaudeExtractor, type ExtractionResponse, type ParseFn } from "@/lib/extraction/claudeExtractor";
import { ExtractionError } from "@/lib/extraction/extractor";
import { EXTRACTION_SYSTEM_PROMPT } from "@/lib/extraction/prompt";

const item = { text: "Send deck", owner_mention: "Tom", due_mention: "Friday", source_quote: "Tom to send deck Friday" };
const good: ExtractionResponse = { stop_reason: "end_turn", parsed_output: { items: [item] } };

function stub(...responses: Array<ExtractionResponse | Error>) {
  const parse = vi.fn<ParseFn>();
  for (const r of responses) {
    if (r instanceof Error) parse.mockRejectedValueOnce(r);
    else parse.mockResolvedValueOnce(r);
  }
  return parse;
}

describe("createClaudeExtractor", () => {
  it("sends the notes with the system prompt and returns items", async () => {
    const parse = stub(good);
    const items = await createClaudeExtractor({ model: "claude-opus-5", parse }).extract("Tom to send deck Friday");
    expect(items).toEqual([item]);
    const req = parse.mock.calls[0][0];
    expect(req.model).toBe("claude-opus-5");
    expect(req.system).toBe(EXTRACTION_SYSTEM_PROMPT);
    expect(req.messages[0].content).toContain("<meeting_notes>\nTom to send deck Friday\n</meeting_notes>");
  });

  it("drops items with empty text", async () => {
    const parse = stub({ stop_reason: "end_turn", parsed_output: { items: [item, { ...item, text: "  " }] } });
    expect(await createClaudeExtractor({ model: "m", parse }).extract("n")).toEqual([item]);
  });

  it("retries once when the output is malformed, then succeeds", async () => {
    const parse = stub(new Error("bad JSON"), good);
    expect(await createClaudeExtractor({ model: "m", parse }).extract("n")).toEqual([item]);
    expect(parse).toHaveBeenCalledTimes(2);
  });

  it("gives up after two malformed outputs", async () => {
    const parse = stub({ stop_reason: "end_turn", parsed_output: null }, { stop_reason: "end_turn", parsed_output: null });
    await expect(createClaudeExtractor({ model: "m", parse }).extract("n")).rejects.toBeInstanceOf(ExtractionError);
    expect(parse).toHaveBeenCalledTimes(2);
  });

  it("does not retry API errors (the SDK already retried)", async () => {
    const parse = stub(new Anthropic.APIConnectionError({ message: "network down" }));
    await expect(createClaudeExtractor({ model: "m", parse }).extract("n")).rejects.toBeInstanceOf(ExtractionError);
    expect(parse).toHaveBeenCalledTimes(1);
  });

  it.each(["refusal", "max_tokens"])("fails without retrying on stop_reason %s", async (stop_reason) => {
    const parse = stub({ stop_reason, parsed_output: null });
    await expect(createClaudeExtractor({ model: "m", parse }).extract("n")).rejects.toBeInstanceOf(ExtractionError);
    expect(parse).toHaveBeenCalledTimes(1);
  });
});
```

`tests/unit/extraction/fakeExtractor.test.ts`:

```ts
import { describe, expect, it } from "vitest";
import { ExtractionError } from "@/lib/extraction/extractor";
import { FAKE_FAILURE_MARKER, createLineFakeExtractor } from "@/lib/extraction/fakeExtractor";
import { assertExtractorConfig } from "@/lib/extraction";

describe("createLineFakeExtractor", () => {
  it("turns ACTION lines into items and ignores other lines", async () => {
    const notes = "Intro\n- ACTION: Send deck | owner: Tom | due: Friday\n* action: Book venue\nOutro";
    expect(await createLineFakeExtractor().extract(notes)).toEqual([
      { text: "Send deck", owner_mention: "Tom", due_mention: "Friday", source_quote: "- ACTION: Send deck | owner: Tom | due: Friday" },
      { text: "Book venue", owner_mention: null, due_mention: null, source_quote: "* action: Book venue" },
    ]);
  });

  it("simulates an extraction failure on the marker", async () => {
    await expect(createLineFakeExtractor().extract(`x ${FAKE_FAILURE_MARKER}`)).rejects.toBeInstanceOf(ExtractionError);
  });
});

describe("assertExtractorConfig", () => {
  it("refuses the fake extractor in production", () => {
    expect(() => assertExtractorConfig({ EXTRACTOR: "fake", NODE_ENV: "production" })).toThrow(/never be used in production/);
    expect(() => assertExtractorConfig({ EXTRACTOR: "fake", NODE_ENV: "development" })).not.toThrow();
  });
});
```

- [ ] **Step 2: Run them and confirm they fail**

Run: `npm test -- tests/unit/extraction`
Expected: FAIL. The modules don't exist yet.

- [ ] **Step 3: Implement**

`src/lib/extraction/schema.ts`:

```ts
import { z } from "zod";

export const ExtractedItemSchema = z.object({
  text: z.string(),
  owner_mention: z.string().nullable(),
  due_mention: z.string().nullable(),
  source_quote: z.string(),
});

export const ExtractionSchema = z.object({ items: z.array(ExtractedItemSchema) });

export type ExtractedItem = z.infer<typeof ExtractedItemSchema>;
export type Extraction = z.infer<typeof ExtractionSchema>;
```

`src/lib/extraction/extractor.ts`:

```ts
import type { ExtractedItem } from "./schema";

export interface Extractor {
  extract(notes: string): Promise<ExtractedItem[]>;
}

/** A failure the user can act on (retry). The message is shown in the UI; it never contains notes text. */
export class ExtractionError extends Error {
  constructor(message: string, options?: { cause?: unknown }) {
    super(message, options);
    this.name = "ExtractionError";
  }
}
```

`src/lib/extraction/prompt.ts`:

```ts
export const EXTRACTION_SYSTEM_PROMPT = `You extract action items from a team's meeting notes.

An action item is a commitment for a specific person or group to do something after the meeting. Decisions, FYIs, status updates and open discussion points are not action items unless someone committed to act on them.

Return every action item in the notes. If you are unsure whether something is an action item, include it: a person reviews your list and can delete extras, but a missed item may never be noticed. If the same action appears more than once (for example inline and again in an "Action items" recap), return it each time it appears.

For each item return:
- text: a short, imperative description of the task, staying close to the notes' wording (for example "Send the Q3 deck to legal").
- owner_mention: the name, nickname, initials or group that owns the task, copied exactly as it appears in the notes (for example "Tom", "PK", "legal team", "Tom and Priya"). Do not expand, correct, complete or guess names. If no owner is written for this item, return null.
- due_mention: the deadline copied exactly as written (for example "by Friday", "Oct 3", "EOW"). Do not convert it to a date. If none is written, return null.
- source_quote: a short excerpt of the notes (one line or sentence) that this item comes from, copied character for character so it can be found in the notes.

If there are no action items, return an empty items list.`;

export function buildUserMessage(notes: string): string {
  return `<meeting_notes>\n${notes}\n</meeting_notes>`;
}
```

`src/lib/extraction/claudeExtractor.ts`:

```ts
import Anthropic from "@anthropic-ai/sdk";
import { zodOutputFormat } from "@anthropic-ai/sdk/helpers/zod";
import { ExtractionError, type Extractor } from "./extractor";
import { EXTRACTION_SYSTEM_PROMPT, buildUserMessage } from "./prompt";
import { ExtractionSchema, type Extraction } from "./schema";

export const DEFAULT_MODEL = "claude-opus-5";
export const EXTRACTION_FORMAT = zodOutputFormat(ExtractionSchema);

export interface ExtractionRequest {
  model: string;
  max_tokens: number;
  system: string;
  messages: Array<{ role: "user"; content: string }>;
  output_config: { format: typeof EXTRACTION_FORMAT };
}

export interface ExtractionResponse {
  stop_reason: string | null;
  parsed_output: Extraction | null;
}

export type ParseFn = (request: ExtractionRequest) => Promise<ExtractionResponse>;

export function createClaudeExtractor(opts: { model: string; parse: ParseFn }): Extractor {
  return {
    async extract(notes) {
      const request: ExtractionRequest = {
        model: opts.model,
        max_tokens: 16000,
        system: EXTRACTION_SYSTEM_PROMPT,
        messages: [{ role: "user", content: buildUserMessage(notes) }],
        output_config: { format: EXTRACTION_FORMAT },
      };
      for (let attempt = 1; attempt <= 2; attempt++) {
        let response: ExtractionResponse;
        try {
          response = await opts.parse(request);
        } catch (err) {
          if (err instanceof Anthropic.APIError) {
            throw new ExtractionError("The Claude API request failed. Try again in a minute.", { cause: err });
          }
          continue; // output could not be parsed: retry once
        }
        if (response.stop_reason === "refusal") {
          throw new ExtractionError("Claude declined to process these notes.");
        }
        if (response.stop_reason === "max_tokens") {
          throw new ExtractionError("These notes produced more output than expected. Try splitting them into two meetings.");
        }
        const checked = ExtractionSchema.safeParse(response.parsed_output);
        if (checked.success) return checked.data.items.filter((i) => i.text.trim() !== "");
      }
      throw new ExtractionError("Claude returned an unexpected response twice. Try again.");
    },
  };
}

export function createClaudeExtractorFromEnv(): Extractor {
  const client = new Anthropic({ timeout: 120_000, maxRetries: 1 });
  return createClaudeExtractor({
    model: process.env.CLAUDE_MODEL || DEFAULT_MODEL,
    parse: async (request) => {
      const response = await client.messages.parse(request);
      return { stop_reason: response.stop_reason, parsed_output: response.parsed_output };
    },
  });
}
```

`src/lib/extraction/fakeExtractor.ts`:

```ts
import { ExtractionError, type Extractor } from "./extractor";
import type { ExtractedItem } from "./schema";

export const FAKE_FAILURE_MARKER = "FAKE_EXTRACTION_FAILURE";
const LINE = /^\s*(?:[-*•]\s*)?action:\s*(.+?)\s*$/i;

/** Deterministic extractor for local dev and E2E: `- ACTION: <text> | owner: <name> | due: <when>`. */
export function createLineFakeExtractor(): Extractor {
  return {
    async extract(notes) {
      if (notes.includes(FAKE_FAILURE_MARKER)) throw new ExtractionError("Simulated extraction failure.");
      const items: ExtractedItem[] = [];
      for (const line of notes.split(/\r?\n/)) {
        const m = LINE.exec(line);
        if (!m) continue;
        const [text, ...fields] = m[1].split("|").map((s) => s.trim());
        const field = (key: string) => {
          const f = fields.find((x) => x.toLowerCase().startsWith(`${key}:`));
          const value = f?.slice(key.length + 1).trim();
          return value ? value : null;
        };
        items.push({ text, owner_mention: field("owner"), due_mention: field("due"), source_quote: line.trim() });
      }
      return items;
    },
  };
}
```

`src/lib/extraction/index.ts`:

```ts
import { createClaudeExtractorFromEnv } from "./claudeExtractor";
import type { Extractor } from "./extractor";
import { createLineFakeExtractor } from "./fakeExtractor";

type Env = Record<string, string | undefined>;

export function assertExtractorConfig(env: Env = process.env): void {
  if (env.EXTRACTOR === "fake" && env.NODE_ENV === "production") {
    throw new Error("EXTRACTOR=fake must never be used in production");
  }
}

export function getExtractor(env: Env = process.env): Extractor {
  assertExtractorConfig(env);
  return env.EXTRACTOR === "fake" ? createLineFakeExtractor() : createClaudeExtractorFromEnv();
}
```

- [ ] **Step 4: Run the tests and typecheck**

Run: `npm test -- tests/unit/extraction && npm run typecheck`
Expected: all PASS, with no type errors. If `client.messages.parse(request)` reports a type mismatch, the SDK expects a different request shape. Fix `ExtractionRequest` to match the SDK's `MessageCreateParams` fields. Don't cast.

- [ ] **Step 5: Commit**

```bash
git add src/lib/extraction tests/unit/extraction
git commit -m "feat: Claude extractor with structured outputs, plus a deterministic fake"
```

---

### Task 6: Build draft items from an extraction

**Files:**
- Create: `src/lib/extraction/buildDraft.ts`
- Test: `tests/unit/extraction/buildDraft.test.ts`

**Interfaces:**
- Consumes: `resolveOwner` (Task 2), `resolveDue` (Task 3), `locateQuote` (Task 4), `ExtractedItem` (Task 5), `Flag`, `RosterEntry` (Task 1).
- Produces:
  - `interface DraftItemInput { text: string; ownerMemberId: string | null; ownerRaw: string | null; ownerSuggestions: string[]; dueDate: string | null; dueRaw: string | null; sourceQuote: string; sourceStart: number | null; sourceEnd: number | null; flags: Flag[] }`. Field names match the `action_items` columns from Task 7.
  - `interface DraftContext { notes: string; meetingDate: string; roster: RosterEntry[]; locale: string }`
  - `normalizeItemText(s: string): string`
  - `buildDraftItems(extracted: ExtractedItem[], ctx: DraftContext): DraftItemInput[]`

- [ ] **Step 1: Write the failing test**

`tests/unit/extraction/buildDraft.test.ts`:

```ts
import { describe, expect, it } from "vitest";
import { buildDraftItems } from "@/lib/extraction/buildDraft";
import type { ExtractedItem } from "@/lib/extraction/schema";
import { ROSTER } from "../../fixtures/roster";

const ctx = (notes: string) => ({ notes, meetingDate: "2026-09-30", roster: ROSTER, locale: "en-US" });
const item = (over: Partial<ExtractedItem>): ExtractedItem => ({
  text: "Send deck", owner_mention: "Tom", due_mention: null, source_quote: "Tom to send deck", ...over,
});

describe("buildDraftItems", () => {
  it("resolves owner, due date and source range for a clean item", () => {
    const notes = "Sync\nTom to send deck by Friday";
    const [d] = buildDraftItems([item({ due_mention: "by Friday", source_quote: "Tom to send deck by Friday" })], ctx(notes));
    expect(d).toEqual({
      text: "Send deck", ownerMemberId: "m-tomas", ownerRaw: "Tom", ownerSuggestions: [],
      dueDate: "2026-10-02", dueRaw: "by Friday", sourceQuote: "Tom to send deck by Friday",
      sourceStart: 5, sourceEnd: 31, flags: [],
    });
  });

  it("collects owner, due and quote flags", () => {
    const [d] = buildDraftItems(
      [item({ owner_mention: "Tom and Priya", due_mention: "ASAP", source_quote: "not in the notes" })],
      ctx("Tom and Priya to review pricing"),
    );
    expect(d.ownerMemberId).toBeNull();
    expect(d.ownerSuggestions).toEqual(["m-tomas", "m-priya"]);
    expect(d.flags).toEqual(["multiple_owners", "unparsed_due", "quote_not_found"]);
  });

  it("recap duplicates: flags a repeated item as possible_duplicate, keeps both", () => {
    const notes = "Tom to send deck\n\nAction items:\n- Tom: send deck";
    const drafts = buildDraftItems(
      [item({ text: "Send deck" }), item({ text: "send deck.", source_quote: "Tom: send deck" })],
      ctx(notes),
    );
    expect(drafts).toHaveLength(2);
    expect(drafts[0].flags).toEqual([]);
    expect(drafts[1].flags).toEqual(["possible_duplicate"]);
  });

  it("Word-pasted notes: finds ASCII quotes in CRLF/NBSP/curly-quote notes", () => {
    const notes = "Agenda\r\nDana to “own” the Q4–plan\r\n";
    const [d] = buildDraftItems(
      [item({ text: "Own the Q4 plan", owner_mention: "Dana", source_quote: 'Dana to "own" the Q4-plan' })],
      ctx(notes),
    );
    expect(d.flags).toEqual([]);
    expect(notes.slice(d.sourceStart!, d.sourceEnd!)).toBe("Dana to “own” the Q4–plan");
  });
});
```

- [ ] **Step 2: Run it and confirm it fails**

Run: `npm test -- tests/unit/extraction/buildDraft.test.ts`
Expected: FAIL. The module doesn't exist yet.

- [ ] **Step 3: Implement**

`src/lib/extraction/buildDraft.ts`:

```ts
import { resolveDue } from "../dates/resolveDue";
import { locateQuote } from "../notes/locateQuote";
import { resolveOwner } from "../roster/resolveOwner";
import type { Flag, RosterEntry } from "../types";
import type { ExtractedItem } from "./schema";

export interface DraftItemInput {
  text: string;
  ownerMemberId: string | null;
  ownerRaw: string | null;
  ownerSuggestions: string[];
  dueDate: string | null;
  dueRaw: string | null;
  sourceQuote: string;
  sourceStart: number | null;
  sourceEnd: number | null;
  flags: Flag[];
}

export interface DraftContext {
  notes: string;
  meetingDate: string;
  roster: RosterEntry[];
  locale: string;
}

export function normalizeItemText(s: string): string {
  return s
    .normalize("NFD")
    .replace(/\p{M}+/gu, "")
    .toLowerCase()
    .replace(/[^\p{L}\p{N}\s]/gu, "")
    .replace(/\s+/g, " ")
    .trim();
}

export function buildDraftItems(extracted: ExtractedItem[], ctx: DraftContext): DraftItemInput[] {
  const seen = new Set<string>();
  return extracted.map((item) => {
    const flags: Flag[] = [];
    const owner = resolveOwner(item.owner_mention, ctx.roster);
    if (owner.kind === "flagged") flags.push(owner.flag);
    const due = resolveDue(item.due_mention, ctx.meetingDate, ctx.locale);
    if (due.flag) flags.push(due.flag);
    const range = locateQuote(item.source_quote, ctx.notes);
    if (!range) flags.push("quote_not_found");
    const key = normalizeItemText(item.text);
    if (seen.has(key)) flags.push("possible_duplicate");
    else seen.add(key);

    return {
      text: item.text.trim(),
      ownerMemberId: owner.kind === "assigned" ? owner.memberId : null,
      ownerRaw: item.owner_mention,
      ownerSuggestions: owner.kind === "flagged" ? owner.suggestions : [],
      dueDate: due.dueDate,
      dueRaw: item.due_mention,
      sourceQuote: item.source_quote,
      sourceStart: range?.start ?? null,
      sourceEnd: range?.end ?? null,
      flags,
    };
  });
}
```

- [ ] **Step 4: Run the tests and confirm they pass**

Run: `npm test -- tests/unit/extraction`
Expected: all PASS.

- [ ] **Step 5: Commit**

```bash
git add src/lib/extraction/buildDraft.ts tests/unit/extraction/buildDraft.test.ts
git commit -m "feat: turn extracted items into flagged draft items"
```

---

### Task 7: Database schema, migrations, roster seed

**Files:**
- Create: `src/lib/db/schema.ts`, `src/lib/db/client.ts`, `src/lib/db/seed.ts`, `src/lib/roster/repository.ts`, `src/lib/env.ts`, `drizzle.config.ts`, `config/roster.json`, `scripts/migrate.ts`, `scripts/seed.ts`
- Create (generated): `drizzle/0000_init.sql` and metadata
- Create: `tests/helpers/testDb.ts`, `tests/helpers/factories.ts`
- Test: `tests/integration/db/schema.test.ts`

**Interfaces:**
- Consumes: `Flag`, `RosterEntry` (Task 1).
- Produces:
  - Tables `users`, `teamMembers`, `meetings`, `actionItems`, `itemEvents`, `rosterEvents`. Enums: `meetingStatus`, `extractionState`, `itemStatus`, `itemOrigin`, `eventKind`.
  - `type Db = PgDatabase<PgQueryResultHKT, typeof schema>` and `getDb(): Db` from `src/lib/db/client.ts`
  - `interface RosterSeedEntry { displayName: string; aliases: string[] }` and `seedRoster(db: Db, entries: RosterSeedEntry[]): Promise<void>`. Inserts only missing members and never overwrites edited aliases.
  - `getRoster(db: Db): Promise<RosterEntry[]>`, ordered by display name
  - `requiredEnv(name: string): string`
  - Test helpers: `createTestDb(): Promise<Db>`, `resetDb(db)`, `createUser(db, email?)`, `seedTestRoster(db): Promise<Record<string, string>>` (display name → id), `createCommittedItem(db, opts)`

- [ ] **Step 1: Write the schema and config**

`src/lib/db/schema.ts`:

```ts
import { sql } from "drizzle-orm";
import { bigint, check, date, index, integer, jsonb, pgEnum, pgTable, text, timestamp, uuid } from "drizzle-orm/pg-core";
import type { Flag } from "../types";

export const meetingStatus = pgEnum("meeting_status", ["draft", "committed"]);
export const extractionState = pgEnum("extraction_state", ["pending", "done", "failed"]);
export const itemStatus = pgEnum("item_status", ["draft", "open", "done"]);
export const itemOrigin = pgEnum("item_origin", ["extracted", "manual_selection"]);
export const eventKind = pgEnum("event_kind", ["created", "text", "owner", "due_date", "completed", "reopened"]);

const createdAt = () => timestamp("created_at", { withTimezone: true }).notNull().defaultNow();

export const users = pgTable("users", {
  id: uuid("id").primaryKey().defaultRandom(),
  email: text("email").notNull().unique(),
  name: text("name"),
  createdAt: createdAt(),
});

export const teamMembers = pgTable("team_members", {
  id: uuid("id").primaryKey().defaultRandom(),
  displayName: text("display_name").notNull().unique(),
  aliases: text("aliases").array().notNull().default(sql`'{}'::text[]`),
  createdAt: createdAt(),
});

export const meetings = pgTable(
  "meetings",
  {
    id: uuid("id").primaryKey().defaultRandom(),
    title: text("title").notNull(),
    meetingDate: date("meeting_date", { mode: "string" }).notNull(),
    notesText: text("notes_text").notNull(),
    notesHash: text("notes_hash").notNull(),
    status: meetingStatus("status").notNull().default("draft"),
    extractionState: extractionState("extraction_state").notNull().default("pending"),
    extractionError: text("extraction_error"),
    createdBy: uuid("created_by").notNull().references(() => users.id),
    createdAt: createdAt(),
    committedAt: timestamp("committed_at", { withTimezone: true }),
  },
  (t) => [index("meetings_notes_hash_idx").on(t.notesHash)],
);

export const actionItems = pgTable(
  "action_items",
  {
    id: uuid("id").primaryKey().defaultRandom(),
    meetingId: uuid("meeting_id").notNull().references(() => meetings.id),
    text: text("text").notNull(),
    ownerMemberId: uuid("owner_member_id").references(() => teamMembers.id),
    ownerRaw: text("owner_raw"),
    ownerSuggestions: uuid("owner_suggestions").array().notNull().default(sql`'{}'::uuid[]`),
    dueDate: date("due_date", { mode: "string" }),
    dueRaw: text("due_raw"),
    sourceQuote: text("source_quote").notNull(),
    sourceStart: integer("source_start"),
    sourceEnd: integer("source_end"),
    flags: text("flags").array().$type<Flag[]>().notNull().default(sql`'{}'::text[]`),
    origin: itemOrigin("origin").notNull(),
    status: itemStatus("status").notNull().default("draft"),
    position: integer("position").notNull().default(0),
    completedBy: uuid("completed_by").references(() => users.id),
    completedAt: timestamp("completed_at", { withTimezone: true }),
    createdAt: createdAt(),
    updatedAt: timestamp("updated_at", { withTimezone: true }).notNull().defaultNow(),
  },
  () => [
    check("owner_required_off_draft", sql`status = 'draft' OR owner_member_id IS NOT NULL`),
  ],
);

export const itemEvents = pgTable(
  "item_events",
  {
    id: bigint("id", { mode: "number" }).primaryKey().generatedAlwaysAsIdentity(),
    itemId: uuid("item_id").notNull().references(() => actionItems.id),
    actorId: uuid("actor_id").notNull().references(() => users.id),
    at: timestamp("at", { withTimezone: true }).notNull().defaultNow(),
    kind: eventKind("kind").notNull(),
    oldValue: jsonb("old_value").$type<Record<string, unknown> | null>(),
    newValue: jsonb("new_value").$type<Record<string, unknown> | null>(),
  },
  (t) => [index("item_events_item_idx").on(t.itemId)],
);

export const rosterEvents = pgTable("roster_events", {
  id: bigint("id", { mode: "number" }).primaryKey().generatedAlwaysAsIdentity(),
  memberId: uuid("member_id").notNull().references(() => teamMembers.id),
  actorId: uuid("actor_id").notNull().references(() => users.id),
  at: timestamp("at", { withTimezone: true }).notNull().defaultNow(),
  oldAliases: text("old_aliases").array().notNull(),
  newAliases: text("new_aliases").array().notNull(),
});
```

`src/lib/env.ts`:

```ts
export function requiredEnv(name: string): string {
  const value = process.env[name];
  if (!value) throw new Error(`Missing required environment variable ${name}`);
  return value;
}
```

`src/lib/db/client.ts`:

```ts
import { drizzle } from "drizzle-orm/node-postgres";
import type { PgDatabase, PgQueryResultHKT } from "drizzle-orm/pg-core";
import { Pool } from "pg";
import { requiredEnv } from "../env";
import * as schema from "./schema";

export type Db = PgDatabase<PgQueryResultHKT, typeof schema>;

const globalForDb = globalThis as unknown as { db?: Db };

export function getDb(): Db {
  if (!globalForDb.db) {
    const pool = new Pool({ connectionString: requiredEnv("DATABASE_URL") });
    globalForDb.db = drizzle(pool, { schema }) as unknown as Db;
  }
  return globalForDb.db;
}
```

`src/lib/db/seed.ts`:

```ts
import type { Db } from "./client";
import { teamMembers } from "./schema";

export interface RosterSeedEntry {
  displayName: string;
  aliases: string[];
}

export async function seedRoster(db: Db, entries: RosterSeedEntry[]): Promise<void> {
  for (const entry of entries) {
    await db
      .insert(teamMembers)
      .values({ displayName: entry.displayName, aliases: entry.aliases })
      .onConflictDoNothing({ target: teamMembers.displayName });
  }
}
```

`src/lib/roster/repository.ts`:

```ts
import { asc } from "drizzle-orm";
import type { Db } from "../db/client";
import { teamMembers } from "../db/schema";
import type { RosterEntry } from "../types";

export async function getRoster(db: Db): Promise<RosterEntry[]> {
  return db
    .select({ id: teamMembers.id, displayName: teamMembers.displayName, aliases: teamMembers.aliases })
    .from(teamMembers)
    .orderBy(asc(teamMembers.displayName));
}
```

`config/roster.json`:

```json
[
  { "displayName": "Priya", "aliases": [] },
  { "displayName": "Marcus", "aliases": [] },
  { "displayName": "Sarah", "aliases": [] },
  { "displayName": "Tomás", "aliases": ["tom"] },
  { "displayName": "Aisha", "aliases": [] },
  { "displayName": "Dana", "aliases": [] },
  { "displayName": "Ravi", "aliases": [] },
  { "displayName": "Lena", "aliases": [] }
]
```

`drizzle.config.ts`:

```ts
import { defineConfig } from "drizzle-kit";

export default defineConfig({
  dialect: "postgresql",
  schema: "./src/lib/db/schema.ts",
  out: "./drizzle",
  dbCredentials: { url: process.env.DATABASE_URL ?? "" },
});
```

`scripts/migrate.ts`:

```ts
import { drizzle } from "drizzle-orm/node-postgres";
import { migrate } from "drizzle-orm/node-postgres/migrator";
import { Pool } from "pg";
import { requiredEnv } from "../src/lib/env";

async function main() {
  const pool = new Pool({ connectionString: requiredEnv("DATABASE_URL") });
  await migrate(drizzle(pool), { migrationsFolder: "drizzle" });
  await pool.end();
  console.log("Migrations applied");
}

main().catch((err) => {
  console.error(err);
  process.exit(1);
});
```

`scripts/seed.ts`:

```ts
import { drizzle } from "drizzle-orm/node-postgres";
import { Pool } from "pg";
import roster from "../config/roster.json";
import type { Db } from "../src/lib/db/client";
import * as schema from "../src/lib/db/schema";
import { seedRoster } from "../src/lib/db/seed";
import { requiredEnv } from "../src/lib/env";

async function main() {
  const pool = new Pool({ connectionString: requiredEnv("DATABASE_URL") });
  await seedRoster(drizzle(pool, { schema }) as unknown as Db, roster);
  await pool.end();
  console.log(`Roster seeded (${roster.length} members)`);
}

main().catch((err) => {
  console.error(err);
  process.exit(1);
});
```

- [ ] **Step 2: Generate the migration**

Run: `npx drizzle-kit generate --name init`
Expected: `drizzle/0000_init.sql` is created. Open it and check that it contains `CONSTRAINT "owner_required_off_draft" CHECK (status = 'draft' OR owner_member_id IS NOT NULL)` and the five enums.

- [ ] **Step 3: Write the test helpers**

`tests/helpers/testDb.ts`:

```ts
import { PGlite } from "@electric-sql/pglite";
import { sql } from "drizzle-orm";
import { drizzle } from "drizzle-orm/pglite";
import { migrate } from "drizzle-orm/pglite/migrator";
import type { Db } from "@/lib/db/client";
import * as schema from "@/lib/db/schema";

export async function createTestDb(): Promise<Db> {
  const db = drizzle(new PGlite(), { schema });
  await migrate(db, { migrationsFolder: "drizzle" });
  return db as unknown as Db;
}

export async function resetDb(db: Db): Promise<void> {
  await db.execute(
    sql`TRUNCATE item_events, roster_events, action_items, meetings, users, team_members RESTART IDENTITY CASCADE`,
  );
}
```

`tests/helpers/factories.ts`:

```ts
import roster from "../../config/roster.json";
import type { Db } from "@/lib/db/client";
import { actionItems, meetings, teamMembers, users } from "@/lib/db/schema";
import { seedRoster } from "@/lib/db/seed";

export async function createUser(db: Db, email = "reviewer@ourcompany.com") {
  const [user] = await db.insert(users).values({ email, name: email.split("@")[0] }).returning();
  return user;
}

export async function seedTestRoster(db: Db): Promise<Record<string, string>> {
  await seedRoster(db, roster);
  const rows = await db.select().from(teamMembers);
  return Object.fromEntries(rows.map((r) => [r.displayName, r.id]));
}

export async function createCommittedItem(
  db: Db,
  opts: { text: string; ownerId: string; createdBy: string; dueDate?: string | null; meetingTitle?: string },
) {
  const [meeting] = await db
    .insert(meetings)
    .values({
      title: opts.meetingTitle ?? "Sync",
      meetingDate: "2026-09-30",
      notesText: opts.text,
      notesHash: `hash-${opts.text}`,
      status: "committed",
      extractionState: "done",
      createdBy: opts.createdBy,
      committedAt: new Date(),
    })
    .returning();
  const [item] = await db
    .insert(actionItems)
    .values({
      meetingId: meeting.id,
      text: opts.text,
      ownerMemberId: opts.ownerId,
      dueDate: opts.dueDate ?? null,
      sourceQuote: opts.text,
      sourceStart: 0,
      sourceEnd: opts.text.length,
      origin: "extracted",
      status: "open",
    })
    .returning();
  return { meeting, item };
}
```

- [ ] **Step 4: Write the failing test**

`tests/integration/db/schema.test.ts`:

```ts
import { eq } from "drizzle-orm";
import { beforeAll, beforeEach, describe, expect, it } from "vitest";
import roster from "../../../config/roster.json";
import type { Db } from "@/lib/db/client";
import { actionItems, meetings, teamMembers } from "@/lib/db/schema";
import { seedRoster } from "@/lib/db/seed";
import { getRoster } from "@/lib/roster/repository";
import { createUser } from "../../helpers/factories";
import { createTestDb, resetDb } from "../../helpers/testDb";

let db: Db;
beforeAll(async () => {
  db = await createTestDb();
});
beforeEach(async () => {
  await resetDb(db);
});

describe("roster seed", () => {
  it("seeds the 8 members, sorted by name, with Tomás → tom", async () => {
    await seedRoster(db, roster);
    const r = await getRoster(db);
    expect(r.map((m) => m.displayName)).toEqual(["Aisha", "Dana", "Lena", "Marcus", "Priya", "Ravi", "Sarah", "Tomás"]);
    expect(r.find((m) => m.displayName === "Tomás")?.aliases).toEqual(["tom"]);
  });

  it("is idempotent and keeps aliases edited in the app", async () => {
    await seedRoster(db, roster);
    await db.update(teamMembers).set({ aliases: ["tom", "tommy"] }).where(eq(teamMembers.displayName, "Tomás"));
    await seedRoster(db, roster);
    const r = await getRoster(db);
    expect(r).toHaveLength(8);
    expect(r.find((m) => m.displayName === "Tomás")?.aliases).toEqual(["tom", "tommy"]);
  });
});

describe("owner_required_off_draft constraint", () => {
  it("rejects an open item without an owner", async () => {
    const user = await createUser(db);
    const [meeting] = await db
      .insert(meetings)
      .values({ title: "t", meetingDate: "2026-09-30", notesText: "n", notesHash: "h", createdBy: user.id })
      .returning();
    await expect(
      db.insert(actionItems).values({ meetingId: meeting.id, text: "x", sourceQuote: "x", origin: "extracted", status: "open" }),
    ).rejects.toThrow();
    await expect(
      db.insert(actionItems).values({ meetingId: meeting.id, text: "x", sourceQuote: "x", origin: "extracted", status: "draft" }),
    ).resolves.toBeDefined();
  });
});
```

- [ ] **Step 5: Run the tests and confirm they pass**

Run: `npm test -- tests/integration/db`
Expected: 3 PASS. (The schema and migration were written in Steps 1–2, so this run checks that they're correct. If you want to see it fail first, temporarily delete the `check(...)` line, regenerate the migration, and watch the constraint test fail. Then restore the line and regenerate again.)

- [ ] **Step 6: Apply to the local dev database**

```bash
cp .env.example .env.local   # then set EXTRACTOR=fake for now
docker compose up -d postgres
npm run db:migrate && npm run db:seed
```

Expected: "Migrations applied" and "Roster seeded (8 members)".

- [ ] **Step 7: Commit**

```bash
git add src/lib/db src/lib/env.ts src/lib/roster/repository.ts drizzle drizzle.config.ts config scripts tests/helpers tests/integration/db
git commit -m "feat: database schema, migrations and roster seed"
```

---

### Task 8: Meetings service (paste → draft → review → commit)

**Files:**
- Create: `src/lib/limits.ts`, `src/lib/errors.ts`, `src/lib/meetings/service.ts`
- Test: `tests/integration/meetings/service.test.ts`

**Interfaces:**
- Consumes: `Db`, tables (Task 7), `getRoster` (Task 7), `buildDraftItems` (Task 6), `Extractor`/`ExtractionError` (Task 5), `suggestMemberFromText` (Task 2), `isIsoDate` (Task 3), `isBlocking`/`Flag` (Task 1).
- Produces:
  - `MAX_NOTES_CHARS = 50_000` (`src/lib/limits.ts`, safe to import in client code)
  - `NotFoundError`, `ValidationError`, and `ConflictError` with `code: "already_committed" | "blocking_flags" | "not_draft" | "extraction_not_done"`
  - `MeetingInputSchema` and `type MeetingInput = { title: string; meetingDate: string; notes: string }`
  - `hashNotes(notes: string): string`
  - `findDuplicateMeeting(db, notesHash): Promise<{ id: string; title: string; status: "draft" | "committed"; createdAt: Date } | null>`
  - `createDraftMeeting(db, input: MeetingInput, userId: string): Promise<string>`
  - `getMeetingOrThrow(db, meetingId)`, which returns the `meetings` row
  - `runExtraction(db, meetingId, extractor, locale): Promise<{ ok: true; itemCount: number } | { ok: false; error: string }>`
  - `getMeetingWithItems(db, meetingId): Promise<{ meeting; items: ActionItemRow[]; roster: RosterEntry[] }>`
  - `type DraftItemPatch = { text?: string; ownerMemberId?: string | null; dueDate?: string | null }` and `updateDraftItem(db, itemId, patch): Promise<void>`
  - `splitDraftItem(db, itemId): Promise<void>`, `addManualItem(db, meetingId, range: { start: number; end: number }): Promise<string>`, `deleteDraftItem(db, itemId): Promise<void>`
  - `commitMeeting(db, meetingId, actorId): Promise<{ committed: number }>`
  - `listDraftMeetings(db): Promise<Array<{ id: string; title: string; meetingDate: string; createdAt: Date }>>`
  - `type ActionItemRow = typeof actionItems.$inferSelect`

- [ ] **Step 1: Write the failing test**

`tests/integration/meetings/service.test.ts`:

```ts
import { eq } from "drizzle-orm";
import { beforeAll, beforeEach, describe, expect, it } from "vitest";
import type { Db } from "@/lib/db/client";
import { actionItems, itemEvents, meetings } from "@/lib/db/schema";
import { ConflictError, ValidationError } from "@/lib/errors";
import { ExtractionError, type Extractor } from "@/lib/extraction/extractor";
import type { ExtractedItem } from "@/lib/extraction/schema";
import { MAX_NOTES_CHARS } from "@/lib/limits";
import {
  MeetingInputSchema, addManualItem, commitMeeting, createDraftMeeting, deleteDraftItem, findDuplicateMeeting,
  getMeetingWithItems, hashNotes, listDraftMeetings, runExtraction, splitDraftItem, updateDraftItem,
} from "@/lib/meetings/service";
import { createUser, seedTestRoster } from "../../helpers/factories";
import { createTestDb, resetDb } from "../../helpers/testDb";

const NOTES = [
  "Weekly sync",
  "- Tom to send the launch deck by Friday",
  "- Tom and Priya to review pricing",
  "- Someone from legal to check the contract",
  "Lena will draft the FAQ",
].join("\n");

const EXTRACTED: ExtractedItem[] = [
  { text: "Send the launch deck", owner_mention: "Tom", due_mention: "by Friday", source_quote: "Tom to send the launch deck by Friday" },
  { text: "Review pricing", owner_mention: "Tom and Priya", due_mention: null, source_quote: "Tom and Priya to review pricing" },
  { text: "Check the contract", owner_mention: "Someone from legal", due_mention: null, source_quote: "Someone from legal to check the contract" },
];

const extractorReturning = (items: ExtractedItem[]): Extractor => ({ extract: async () => items });
const failingExtractor = (message: string): Extractor => ({
  extract: async () => {
    throw new ExtractionError(message);
  },
});

let db: Db;
let ids: Record<string, string>;
let userId: string;

beforeAll(async () => {
  db = await createTestDb();
});
beforeEach(async () => {
  await resetDb(db);
  ids = await seedTestRoster(db);
  userId = (await createUser(db)).id;
});

async function draft(items: ExtractedItem[] = EXTRACTED) {
  const meetingId = await createDraftMeeting(db, { title: "Weekly sync", meetingDate: "2026-09-30", notes: NOTES }, userId);
  const result = await runExtraction(db, meetingId, extractorReturning(items), "en-US");
  expect(result).toEqual({ ok: true, itemCount: items.length });
  const { items: rows } = await getMeetingWithItems(db, meetingId);
  return { meetingId, rows };
}

async function resolveAllOwners(rows: Array<{ id: string; ownerMemberId: string | null }>) {
  for (const r of rows) if (!r.ownerMemberId) await updateDraftItem(db, r.id, { ownerMemberId: ids.Marcus });
}

describe("MeetingInputSchema", () => {
  const base = { title: "Sync", meetingDate: "2026-09-30", notes: "x" };
  it("accepts valid input and trims the title", () => {
    expect(MeetingInputSchema.parse({ ...base, title: "  Sync " }).title).toBe("Sync");
  });
  it.each([
    [{ ...base, title: "  " }, "Title is required"],
    [{ ...base, notes: " \n " }, "Paste the meeting notes"],
    [{ ...base, meetingDate: "2026-02-30" }, "Meeting date must be a valid date"],
    [{ ...base, notes: "a".repeat(MAX_NOTES_CHARS + 1) }, "Notes must be 50,000 characters or fewer"],
  ])("rejects %#", (input, message) => {
    const r = MeetingInputSchema.safeParse(input);
    expect(r.success).toBe(false);
    expect(r.error?.issues[0].message).toBe(message);
  });
  it("accepts notes of exactly the limit", () => {
    expect(MeetingInputSchema.safeParse({ ...base, notes: "a".repeat(MAX_NOTES_CHARS) }).success).toBe(true);
  });
});

describe("duplicates", () => {
  it("hashes CRLF and trailing whitespace the same", () => {
    expect(hashNotes("a\r\nb\n")).toBe(hashNotes("a\nb"));
  });
  it("finds an earlier meeting with the same notes", async () => {
    const id = await createDraftMeeting(db, { title: "Weekly sync", meetingDate: "2026-09-30", notes: NOTES }, userId);
    expect(await findDuplicateMeeting(db, hashNotes(NOTES))).toMatchObject({ id, title: "Weekly sync", status: "draft" });
    expect(await findDuplicateMeeting(db, hashNotes("other"))).toBeNull();
  });
});

describe("runExtraction", () => {
  it("stores flagged draft items in order", async () => {
    const { meetingId, rows } = await draft();
    const meeting = (await getMeetingWithItems(db, meetingId)).meeting;
    expect(meeting.extractionState).toBe("done");
    expect(rows.map((r) => [r.text, r.ownerMemberId, r.dueDate, r.flags, r.position])).toEqual([
      ["Send the launch deck", ids["Tomás"], "2026-10-02", [], 0],
      ["Review pricing", null, null, ["multiple_owners"], 1],
      ["Check the contract", null, null, ["unknown_owner"], 2],
    ]);
    expect(rows[1].ownerSuggestions).toEqual([ids["Tomás"], ids.Priya]);
    expect(await listDraftMeetings(db)).toHaveLength(1);
  });

  it("records a failure without losing the notes, and a retry recovers", async () => {
    const meetingId = await createDraftMeeting(db, { title: "S", meetingDate: "2026-09-30", notes: NOTES }, userId);
    expect(await runExtraction(db, meetingId, failingExtractor("API down"), "en-US")).toEqual({ ok: false, error: "API down" });
    let data = await getMeetingWithItems(db, meetingId);
    expect(data.meeting).toMatchObject({ extractionState: "failed", extractionError: "API down", notesText: NOTES });
    expect(data.items).toHaveLength(0);

    await runExtraction(db, meetingId, extractorReturning(EXTRACTED), "en-US");
    data = await getMeetingWithItems(db, meetingId);
    expect(data.meeting).toMatchObject({ extractionState: "done", extractionError: null });
    expect(data.items).toHaveLength(3);
  });
});

describe("draft editing", () => {
  it("choosing an owner clears owner flags; clearing it flags missing_owner", async () => {
    const { rows } = await draft();
    await updateDraftItem(db, rows[2].id, { ownerMemberId: ids.Marcus });
    let row = (await getMeetingWithItems(db, rows[2].meetingId)).items[2];
    expect(row).toMatchObject({ ownerMemberId: ids.Marcus, flags: [] });
    await updateDraftItem(db, rows[2].id, { ownerMemberId: null });
    row = (await getMeetingWithItems(db, rows[2].meetingId)).items[2];
    expect(row).toMatchObject({ ownerMemberId: null, flags: ["missing_owner"] });
  });

  it("setting a due date clears unparsed_due; empty text is rejected", async () => {
    const { rows } = await draft([{ ...EXTRACTED[0], due_mention: "ASAP" }]);
    expect(rows[0].flags).toEqual(["unparsed_due"]);
    await updateDraftItem(db, rows[0].id, { dueDate: "2026-10-09" });
    expect((await getMeetingWithItems(db, rows[0].meetingId)).items[0]).toMatchObject({ dueDate: "2026-10-09", flags: [] });
    await expect(updateDraftItem(db, rows[0].id, { text: "   " })).rejects.toBeInstanceOf(ValidationError);
    await expect(updateDraftItem(db, rows[0].id, { dueDate: "2026-02-30" })).rejects.toBeInstanceOf(ValidationError);
  });

  it("split creates one assigned copy per suggested owner", async () => {
    const { meetingId, rows } = await draft();
    await splitDraftItem(db, rows[1].id);
    const items = (await getMeetingWithItems(db, meetingId)).items;
    const copies = items.filter((i) => i.text === "Review pricing");
    expect(copies.map((c) => c.ownerMemberId).sort()).toEqual([ids["Tomás"], ids.Priya].sort());
    expect(copies.every((c) => c.flags.length === 0)).toBe(true);
    expect(items).toHaveLength(4);
  });

  it("adds a missed item from a selection, suggesting but not assigning the owner", async () => {
    const { meetingId } = await draft();
    const start = NOTES.indexOf("Lena will draft the FAQ");
    const id = await addManualItem(db, meetingId, { start: start - 1, end: start + "Lena will draft the FAQ".length });
    const item = (await getMeetingWithItems(db, meetingId)).items.find((i) => i.id === id)!;
    expect(item).toMatchObject({
      text: "Lena will draft the FAQ",
      ownerMemberId: null,
      ownerSuggestions: [ids.Lena],
      flags: ["missing_owner"],
      origin: "manual_selection",
      sourceStart: start,
      position: 3,
    });
    await expect(addManualItem(db, meetingId, { start: 5, end: 5 })).rejects.toBeInstanceOf(ValidationError);
    await expect(addManualItem(db, meetingId, { start: 0, end: NOTES.length + 1 })).rejects.toBeInstanceOf(ValidationError);
  });

  it("deletes a draft item", async () => {
    const { meetingId, rows } = await draft();
    await deleteDraftItem(db, rows[2].id);
    expect((await getMeetingWithItems(db, meetingId)).items).toHaveLength(2);
  });
});

describe("commitMeeting", () => {
  it("refuses while blocking flags remain", async () => {
    const { meetingId } = await draft();
    await expect(commitMeeting(db, meetingId, userId)).rejects.toMatchObject({ code: "blocking_flags" });
  });

  it("moves items to the board and writes one created event each", async () => {
    const { meetingId, rows } = await draft();
    await resolveAllOwners(rows);
    expect(await commitMeeting(db, meetingId, userId)).toEqual({ committed: 3 });
    const items = await db.select().from(actionItems).where(eq(actionItems.meetingId, meetingId));
    expect(items.every((i) => i.status === "open")).toBe(true);
    const events = await db.select().from(itemEvents);
    expect(events).toHaveLength(3);
    expect(events[0]).toMatchObject({ kind: "created", actorId: userId });
    expect(events.find((e) => e.itemId === rows[2].id)?.newValue).toMatchObject({
      ownerMemberId: ids.Marcus,
      ownerRaw: "Someone from legal",
    });
    const [m] = await db.select().from(meetings).where(eq(meetings.id, meetingId));
    expect(m.status).toBe("committed");
  });

  it("second commit is rejected and writes nothing more", async () => {
    const { meetingId, rows } = await draft();
    await resolveAllOwners(rows);
    await commitMeeting(db, meetingId, userId);
    await expect(commitMeeting(db, meetingId, userId)).rejects.toMatchObject({ code: "already_committed" });
    expect(await db.select().from(itemEvents)).toHaveLength(3);
  });

  it("draft edits after commit are refused", async () => {
    const { meetingId, rows } = await draft();
    await resolveAllOwners(rows);
    await commitMeeting(db, meetingId, userId);
    await expect(updateDraftItem(db, rows[0].id, { text: "Changed" })).rejects.toMatchObject({ code: "not_draft" });
    await expect(deleteDraftItem(db, rows[0].id)).rejects.toBeInstanceOf(ConflictError);
    await expect(addManualItem(db, meetingId, { start: 0, end: 5 })).rejects.toBeInstanceOf(ConflictError);
  });

  it("refuses when extraction has not succeeded", async () => {
    const meetingId = await createDraftMeeting(db, { title: "S", meetingDate: "2026-09-30", notes: NOTES }, userId);
    await runExtraction(db, meetingId, failingExtractor("down"), "en-US");
    await expect(commitMeeting(db, meetingId, userId)).rejects.toMatchObject({ code: "extraction_not_done" });
  });
});
```

- [ ] **Step 2: Run it and confirm it fails**

Run: `npm test -- tests/integration/meetings`
Expected: FAIL. The modules don't exist yet.

- [ ] **Step 3: Implement**

`src/lib/limits.ts`:

```ts
export const MAX_NOTES_CHARS = 50_000;
```

`src/lib/errors.ts`:

```ts
export class NotFoundError extends Error {
  constructor(message: string) {
    super(message);
    this.name = "NotFoundError";
  }
}

export class ValidationError extends Error {
  constructor(message: string) {
    super(message);
    this.name = "ValidationError";
  }
}

export type ConflictCode = "already_committed" | "blocking_flags" | "not_draft" | "extraction_not_done";

export class ConflictError extends Error {
  constructor(public readonly code: ConflictCode, message: string) {
    super(message);
    this.name = "ConflictError";
  }
}
```

`src/lib/meetings/service.ts`:

```ts
import { createHash } from "node:crypto";
import { and, asc, desc, eq, max } from "drizzle-orm";
import { z } from "zod";
import type { Db } from "../db/client";
import { actionItems, itemEvents, meetings, teamMembers } from "../db/schema";
import { isIsoDate } from "../dates/isoDate";
import { ConflictError, NotFoundError, ValidationError } from "../errors";
import { buildDraftItems } from "../extraction/buildDraft";
import { ExtractionError, type Extractor } from "../extraction/extractor";
import { MAX_NOTES_CHARS } from "../limits";
import { getRoster } from "../roster/repository";
import { suggestMemberFromText } from "../roster/suggest";
import { isBlocking, type Flag } from "../types";

export type ActionItemRow = typeof actionItems.$inferSelect;

export const MeetingInputSchema = z.object({
  title: z.string().trim().min(1, "Title is required").max(200, "Title must be 200 characters or fewer"),
  meetingDate: z.string().refine(isIsoDate, "Meeting date must be a valid date"),
  notes: z
    .string()
    .refine((s) => s.trim().length > 0, "Paste the meeting notes")
    .refine((s) => s.length <= MAX_NOTES_CHARS, `Notes must be ${MAX_NOTES_CHARS.toLocaleString("en-US")} characters or fewer`),
});
export type MeetingInput = z.infer<typeof MeetingInputSchema>;

export type DraftItemPatch = { text?: string; ownerMemberId?: string | null; dueDate?: string | null };

const NOT_DRAFT = "This meeting is already on the board. Reload to see the latest.";

export function hashNotes(notes: string): string {
  return createHash("sha256").update(notes.replace(/\r\n/g, "\n").trim()).digest("hex");
}

export async function findDuplicateMeeting(db: Db, notesHash: string) {
  const [row] = await db
    .select({ id: meetings.id, title: meetings.title, status: meetings.status, createdAt: meetings.createdAt })
    .from(meetings)
    .where(eq(meetings.notesHash, notesHash))
    .orderBy(asc(meetings.createdAt))
    .limit(1);
  return row ?? null;
}

export async function createDraftMeeting(db: Db, input: MeetingInput, userId: string): Promise<string> {
  const [row] = await db
    .insert(meetings)
    .values({
      title: input.title,
      meetingDate: input.meetingDate,
      notesText: input.notes,
      notesHash: hashNotes(input.notes),
      createdBy: userId,
    })
    .returning({ id: meetings.id });
  return row.id;
}

export async function getMeetingOrThrow(db: Db, meetingId: string) {
  const [meeting] = await db.select().from(meetings).where(eq(meetings.id, meetingId));
  if (!meeting) throw new NotFoundError("Meeting not found");
  return meeting;
}

async function getDraftMeeting(db: Db, meetingId: string) {
  const meeting = await getMeetingOrThrow(db, meetingId);
  if (meeting.status !== "draft") throw new ConflictError("not_draft", NOT_DRAFT);
  return meeting;
}

async function getDraftItem(db: Db, itemId: string): Promise<ActionItemRow> {
  const [item] = await db.select().from(actionItems).where(eq(actionItems.id, itemId));
  if (!item) throw new NotFoundError("Action item not found");
  if (item.status !== "draft") throw new ConflictError("not_draft", NOT_DRAFT);
  return item;
}

export async function runExtraction(
  db: Db,
  meetingId: string,
  extractor: Extractor,
  locale: string,
): Promise<{ ok: true; itemCount: number } | { ok: false; error: string }> {
  const meeting = await getDraftMeeting(db, meetingId);
  let extracted;
  try {
    extracted = await extractor.extract(meeting.notesText);
  } catch (err) {
    const message = err instanceof ExtractionError ? err.message : "Extraction failed unexpectedly. Try again.";
    if (!(err instanceof ExtractionError)) console.error("Unexpected extraction error", err instanceof Error ? err.name : typeof err);
    await db.update(meetings).set({ extractionState: "failed", extractionError: message }).where(eq(meetings.id, meetingId));
    return { ok: false, error: message };
  }
  const roster = await getRoster(db);
  const drafts = buildDraftItems(extracted, { notes: meeting.notesText, meetingDate: meeting.meetingDate, roster, locale });
  await db.transaction(async (tx) => {
    await tx.delete(actionItems).where(and(eq(actionItems.meetingId, meetingId), eq(actionItems.status, "draft")));
    if (drafts.length > 0) {
      await tx.insert(actionItems).values(
        drafts.map((d, i) => ({ ...d, meetingId, origin: "extracted" as const, status: "draft" as const, position: i })),
      );
    }
    await tx.update(meetings).set({ extractionState: "done", extractionError: null }).where(eq(meetings.id, meetingId));
  });
  return { ok: true, itemCount: drafts.length };
}

export async function getMeetingWithItems(db: Db, meetingId: string) {
  const meeting = await getMeetingOrThrow(db, meetingId);
  const items = await db
    .select()
    .from(actionItems)
    .where(eq(actionItems.meetingId, meetingId))
    .orderBy(asc(actionItems.position), asc(actionItems.createdAt), asc(actionItems.id));
  const roster = await getRoster(db);
  return { meeting, items, roster };
}

async function assertMemberExists(db: Db, memberId: string) {
  const [m] = await db.select({ id: teamMembers.id }).from(teamMembers).where(eq(teamMembers.id, memberId));
  if (!m) throw new ValidationError("Unknown team member");
}

export async function updateDraftItem(db: Db, itemId: string, patch: DraftItemPatch): Promise<void> {
  const item = await getDraftItem(db, itemId);
  let flags: Flag[] = [...item.flags];
  const set: Partial<typeof actionItems.$inferInsert> = { updatedAt: new Date() };

  if (patch.text !== undefined) {
    const text = patch.text.trim();
    if (text === "") throw new ValidationError("Action item text cannot be empty");
    set.text = text;
  }
  if (patch.ownerMemberId !== undefined) {
    flags = flags.filter((f) => !isBlocking(f));
    if (patch.ownerMemberId === null) flags.push("missing_owner");
    else await assertMemberExists(db, patch.ownerMemberId);
    set.ownerMemberId = patch.ownerMemberId;
  }
  if (patch.dueDate !== undefined) {
    if (patch.dueDate !== null && !isIsoDate(patch.dueDate)) throw new ValidationError("Due date must be a valid date");
    flags = flags.filter((f) => f !== "unparsed_due");
    set.dueDate = patch.dueDate;
  }
  set.flags = flags;
  await db.update(actionItems).set(set).where(eq(actionItems.id, itemId));
}

export async function splitDraftItem(db: Db, itemId: string): Promise<void> {
  const item = await getDraftItem(db, itemId);
  if (!item.flags.includes("multiple_owners") || item.ownerSuggestions.length < 2) {
    throw new ValidationError("Only items with several owners can be split");
  }
  const { id: _id, createdAt: _c, updatedAt: _u, ...rest } = item;
  await db.transaction(async (tx) => {
    await tx.insert(actionItems).values(
      item.ownerSuggestions.map((memberId) => ({
        ...rest,
        ownerMemberId: memberId,
        ownerSuggestions: [],
        flags: item.flags.filter((f) => !isBlocking(f)),
      })),
    );
    await tx.delete(actionItems).where(eq(actionItems.id, itemId));
  });
}

export async function addManualItem(db: Db, meetingId: string, range: { start: number; end: number }): Promise<string> {
  const meeting = await getDraftMeeting(db, meetingId);
  const { start, end } = range;
  if (!Number.isInteger(start) || !Number.isInteger(end) || start < 0 || end > meeting.notesText.length || start >= end) {
    throw new ValidationError("Select some text in the notes first");
  }
  const raw = meeting.notesText.slice(start, end);
  const quote = raw.trim();
  if (quote === "") throw new ValidationError("Select some text in the notes first");
  const sourceStart = start + (raw.length - raw.trimStart().length);
  const text = quote.replace(/^(?:[-*•]|\d+[.)])\s+/, "").replace(/\s+/g, " ");
  const suggestion = suggestMemberFromText(quote, await getRoster(db));
  const [{ maxPos }] = await db
    .select({ maxPos: max(actionItems.position) })
    .from(actionItems)
    .where(eq(actionItems.meetingId, meetingId));
  const [row] = await db
    .insert(actionItems)
    .values({
      meetingId,
      text,
      ownerMemberId: null,
      ownerRaw: null,
      ownerSuggestions: suggestion ? [suggestion] : [],
      dueDate: null,
      dueRaw: null,
      sourceQuote: quote,
      sourceStart,
      sourceEnd: sourceStart + quote.length,
      flags: ["missing_owner"],
      origin: "manual_selection",
      status: "draft",
      position: (maxPos ?? -1) + 1,
    })
    .returning({ id: actionItems.id });
  return row.id;
}

export async function deleteDraftItem(db: Db, itemId: string): Promise<void> {
  await getDraftItem(db, itemId);
  await db.delete(actionItems).where(eq(actionItems.id, itemId));
}

export async function commitMeeting(db: Db, meetingId: string, actorId: string): Promise<{ committed: number }> {
  return db.transaction(async (tx) => {
    const [meeting] = await tx.select().from(meetings).where(eq(meetings.id, meetingId)).for("update");
    if (!meeting) throw new NotFoundError("Meeting not found");
    if (meeting.status === "committed") throw new ConflictError("already_committed", "This meeting is already on the board.");
    if (meeting.extractionState !== "done") {
      throw new ConflictError("extraction_not_done", "Extraction hasn't finished for this meeting. Retry it first.");
    }
    const items = await tx
      .select()
      .from(actionItems)
      .where(and(eq(actionItems.meetingId, meetingId), eq(actionItems.status, "draft")));
    if (items.some((i) => i.ownerMemberId === null || i.flags.some(isBlocking))) {
      throw new ConflictError("blocking_flags", "Some items still need an owner.");
    }
    const now = new Date();
    if (items.length > 0) {
      await tx
        .update(actionItems)
        .set({ status: "open", updatedAt: now })
        .where(and(eq(actionItems.meetingId, meetingId), eq(actionItems.status, "draft")));
      await tx.insert(itemEvents).values(
        items.map((i) => ({
          itemId: i.id,
          actorId,
          at: now,
          kind: "created" as const,
          oldValue: null,
          newValue: {
            text: i.text,
            ownerMemberId: i.ownerMemberId,
            dueDate: i.dueDate,
            ownerRaw: i.ownerRaw,
            dueRaw: i.dueRaw,
            origin: i.origin,
          },
        })),
      );
    }
    await tx.update(meetings).set({ status: "committed", committedAt: now }).where(eq(meetings.id, meetingId));
    return { committed: items.length };
  });
}

export async function listDraftMeetings(db: Db) {
  return db
    .select({ id: meetings.id, title: meetings.title, meetingDate: meetings.meetingDate, createdAt: meetings.createdAt })
    .from(meetings)
    .where(eq(meetings.status, "draft"))
    .orderBy(desc(meetings.createdAt));
}
```

- [ ] **Step 4: Run the tests and confirm they pass**

Run: `npm test -- tests/integration/meetings && npm run typecheck`
Expected: all PASS, with no type errors.

- [ ] **Step 5: Commit**

```bash
git add src/lib/limits.ts src/lib/errors.ts src/lib/meetings tests/integration/meetings
git commit -m "feat: meeting draft, review edits and audited commit"
```

---

### Task 9: Board item service, history and display helpers

**Files:**
- Create: `src/lib/items/service.ts`, `src/lib/items/describeEvent.ts`, `src/lib/dates/display.ts`
- Test: `tests/integration/items/service.test.ts`, `tests/unit/items/describeEvent.test.ts`, `tests/unit/dates/display.test.ts`

**Interfaces:**
- Consumes: `Db`, tables (Task 7), errors (Task 8), `isIsoDate`/`isoFromParts` (Task 3), `createCommittedItem` (Task 7 test helper).
- Produces:
  - `interface BoardFilters { ownerId?: string; meetingId?: string; includeDoneSince?: Date }`
  - `interface BoardRow { id: string; text: string; status: "open" | "done"; dueDate: string | null; ownerMemberId: string; ownerName: string; meetingId: string; meetingTitle: string; meetingDate: string; completedAt: Date | null; createdAt: Date }`
  - `listBoard(db, filters): Promise<BoardRow[]>`. Open items come first, then done; within each group, due date ascending with no-date items last, then oldest first.
  - `type BoardItemPatch = { text?: string; ownerMemberId?: string; dueDate?: string | null }` and `updateItem(db, itemId, actorId, patch): Promise<number>`, which returns the number of events written
  - `setDone(db, itemId, actorId, done: boolean): Promise<boolean>`, which returns whether anything changed
  - `interface HistoryEvent { id: number; kind: "created" | "text" | "owner" | "due_date" | "completed" | "reopened"; at: Date; actorName: string; oldValue: Record<string, unknown> | null; newValue: Record<string, unknown> | null }` and `getItemHistory(db, itemId): Promise<HistoryEvent[]>`
  - `describeEvent(e: Pick<HistoryEvent, "kind" | "oldValue" | "newValue">): string`
  - `todayLocalIso(now?: Date): string`, `isOverdue(dueDate: string | null, todayIso: string): boolean`, `formatDue(dueDate: string | null): string`

Owner events store `{ memberId, name }` in both `oldValue` and `newValue`, so the history can still show the name later.

- [ ] **Step 1: Write the failing tests**

`tests/unit/dates/display.test.ts`:

```ts
import { describe, expect, it } from "vitest";
import { formatDue, isOverdue, todayLocalIso } from "@/lib/dates/display";

describe("display helpers", () => {
  it("formats due dates", () => {
    expect(formatDue("2026-10-02")).toBe("Fri, Oct 2");
    expect(formatDue(null)).toBe("No date");
  });
  it("is overdue only strictly before today", () => {
    expect(isOverdue("2026-09-29", "2026-09-30")).toBe(true);
    expect(isOverdue("2026-09-30", "2026-09-30")).toBe(false);
    expect(isOverdue(null, "2026-09-30")).toBe(false);
  });
  it("uses the local calendar date", () => {
    expect(todayLocalIso(new Date(2026, 8, 30, 23, 30))).toBe("2026-09-30");
  });
});
```

`tests/unit/items/describeEvent.test.ts`:

```ts
import { describe, expect, it } from "vitest";
import { describeEvent } from "@/lib/items/describeEvent";

describe("describeEvent", () => {
  it.each([
    [{ kind: "created", oldValue: null, newValue: { text: "x" } }, "added this item"],
    [{ kind: "text", oldValue: { text: "Old" }, newValue: { text: "New" } }, "changed the text from “Old” to “New”"],
    [
      { kind: "owner", oldValue: { memberId: "a", name: "Tomás" }, newValue: { memberId: "b", name: "Ravi" } },
      "changed the owner from Tomás to Ravi",
    ],
    [
      { kind: "due_date", oldValue: { dueDate: null }, newValue: { dueDate: "2026-10-02" } },
      "changed the due date from no date to Fri, Oct 2",
    ],
    [{ kind: "completed", oldValue: { status: "open" }, newValue: { status: "done" } }, "marked it done"],
    [{ kind: "reopened", oldValue: { status: "done" }, newValue: { status: "open" } }, "reopened it"],
  ] as const)("%j", (event, expected) => {
    expect(describeEvent(event)).toBe(expected);
  });
});
```

`tests/integration/items/service.test.ts`:

```ts
import { eq } from "drizzle-orm";
import { beforeAll, beforeEach, describe, expect, it } from "vitest";
import type { Db } from "@/lib/db/client";
import { actionItems, itemEvents } from "@/lib/db/schema";
import { ConflictError, ValidationError } from "@/lib/errors";
import { getItemHistory, listBoard, setDone, updateItem } from "@/lib/items/service";
import { createCommittedItem, createUser, seedTestRoster } from "../../helpers/factories";
import { createTestDb, resetDb } from "../../helpers/testDb";

let db: Db;
let ids: Record<string, string>;
let alice: { id: string };
let bob: { id: string };

beforeAll(async () => {
  db = await createTestDb();
});
beforeEach(async () => {
  await resetDb(db);
  ids = await seedTestRoster(db);
  alice = await createUser(db, "alice@ourcompany.com");
  bob = await createUser(db, "bob@ourcompany.com");
});

const make = (text: string, owner: string, dueDate: string | null = null, meetingTitle?: string) =>
  createCommittedItem(db, { text, ownerId: ids[owner], createdBy: alice.id, dueDate, meetingTitle });

describe("listBoard", () => {
  it("lists open items by due date, no-date last, with owner and meeting", async () => {
    await make("No date", "Priya");
    await make("Later", "Ravi", "2026-10-09");
    await make("Sooner", "Tomás", "2026-10-01", "Planning");
    const rows = await listBoard(db, {});
    expect(rows.map((r) => r.text)).toEqual(["Sooner", "Later", "No date"]);
    expect(rows[0]).toMatchObject({ ownerName: "Tomás", meetingTitle: "Planning", status: "open" });
  });

  it("filters by owner and meeting, and excludes drafts", async () => {
    const { meeting } = await make("Mine", "Priya");
    await make("Theirs", "Ravi");
    const [draftRow] = await db.select().from(actionItems).where(eq(actionItems.text, "Theirs"));
    await db.update(actionItems).set({ status: "draft" }).where(eq(actionItems.id, draftRow.id));
    expect((await listBoard(db, {})).map((r) => r.text)).toEqual(["Mine"]);
    expect(await listBoard(db, { ownerId: ids.Ravi })).toEqual([]);
    expect((await listBoard(db, { meetingId: meeting.id })).map((r) => r.text)).toEqual(["Mine"]);
  });

  it("includes recently done items only when asked", async () => {
    const { item } = await make("Done thing", "Priya");
    await setDone(db, item.id, bob.id, true);
    expect(await listBoard(db, {})).toEqual([]);
    const since = new Date(Date.now() - 14 * 86_400_000);
    expect((await listBoard(db, { includeDoneSince: since }))[0]).toMatchObject({ text: "Done thing", status: "done" });
    expect(await listBoard(db, { includeDoneSince: new Date(Date.now() + 60_000) })).toEqual([]);
  });
});

describe("updateItem", () => {
  it("writes one event per changed field and none for unchanged fields", async () => {
    const { item } = await make("Send deck", "Tomás", "2026-10-02");
    const written = await updateItem(db, item.id, bob.id, {
      text: "Send final deck",
      ownerMemberId: ids.Ravi,
      dueDate: "2026-10-02",
    });
    expect(written).toBe(2);
    const history = await getItemHistory(db, item.id);
    expect(history.map((h) => h.kind)).toEqual(["text", "owner"]);
    expect(history[1]).toMatchObject({
      actorName: "bob",
      oldValue: { memberId: ids["Tomás"], name: "Tomás" },
      newValue: { memberId: ids.Ravi, name: "Ravi" },
    });
    expect(await updateItem(db, item.id, bob.id, { text: "Send final deck" })).toBe(0);
  });

  it("can clear the due date", async () => {
    const { item } = await make("Send deck", "Tomás", "2026-10-02");
    await updateItem(db, item.id, bob.id, { dueDate: null });
    const [h] = await getItemHistory(db, item.id);
    expect(h).toMatchObject({ kind: "due_date", oldValue: { dueDate: "2026-10-02" }, newValue: { dueDate: null } });
  });

  it("rejects empty text, unknown members, invalid dates and draft items", async () => {
    const { item } = await make("Send deck", "Tomás");
    await expect(updateItem(db, item.id, bob.id, { text: " " })).rejects.toBeInstanceOf(ValidationError);
    await expect(
      updateItem(db, item.id, bob.id, { ownerMemberId: "00000000-0000-0000-0000-000000000000" }),
    ).rejects.toBeInstanceOf(ValidationError);
    await expect(updateItem(db, item.id, bob.id, { dueDate: "2026-13-01" })).rejects.toBeInstanceOf(ValidationError);
    await db.update(actionItems).set({ status: "draft" }).where(eq(actionItems.id, item.id));
    await expect(updateItem(db, item.id, bob.id, { text: "x" })).rejects.toBeInstanceOf(ConflictError);
  });
});

describe("setDone", () => {
  it("records who completed it, is idempotent, and reopening clears it", async () => {
    const { item } = await make("Send deck", "Tomás");
    expect(await setDone(db, item.id, bob.id, true)).toBe(true);
    expect(await setDone(db, item.id, bob.id, true)).toBe(false);
    let [row] = await db.select().from(actionItems).where(eq(actionItems.id, item.id));
    expect(row).toMatchObject({ status: "done", completedBy: bob.id });
    expect(row.completedAt).toBeInstanceOf(Date);

    await setDone(db, item.id, alice.id, false);
    [row] = await db.select().from(actionItems).where(eq(actionItems.id, item.id));
    expect(row).toMatchObject({ status: "open", completedBy: null, completedAt: null });

    const events = await db.select().from(itemEvents).where(eq(itemEvents.itemId, item.id));
    expect(events.map((e) => e.kind)).toEqual(["completed", "reopened"]);
  });
});
```

- [ ] **Step 2: Run them and confirm they fail**

Run: `npm test -- tests/unit/dates/display.test.ts tests/unit/items tests/integration/items`
Expected: FAIL. The modules don't exist yet.

- [ ] **Step 3: Implement**

`src/lib/dates/display.ts`:

```ts
import { isoFromParts } from "./isoDate";

export function todayLocalIso(now: Date = new Date()): string {
  return isoFromParts(now.getFullYear(), now.getMonth() + 1, now.getDate());
}

export function isOverdue(dueDate: string | null, todayIso: string): boolean {
  return dueDate !== null && dueDate < todayIso;
}

export function formatDue(dueDate: string | null): string {
  if (!dueDate) return "No date";
  const [y, m, d] = dueDate.split("-").map(Number);
  return new Date(Date.UTC(y, m - 1, d)).toLocaleDateString("en-US", {
    weekday: "short",
    month: "short",
    day: "numeric",
    timeZone: "UTC",
  });
}
```

`src/lib/items/describeEvent.ts`:

```ts
import { formatDue } from "../dates/display";

type EventLike = {
  kind: "created" | "text" | "owner" | "due_date" | "completed" | "reopened";
  oldValue: Record<string, unknown> | null;
  newValue: Record<string, unknown> | null;
};

const str = (v: unknown): string | null => (typeof v === "string" ? v : null);
const dateLabel = (v: unknown) => (typeof v === "string" ? formatDue(v) : "no date");

export function describeEvent(e: EventLike): string {
  switch (e.kind) {
    case "created":
      return "added this item";
    case "text":
      return `changed the text from “${str(e.oldValue?.text) ?? ""}” to “${str(e.newValue?.text) ?? ""}”`;
    case "owner":
      return `changed the owner from ${str(e.oldValue?.name) ?? "unknown"} to ${str(e.newValue?.name) ?? "unknown"}`;
    case "due_date":
      return `changed the due date from ${dateLabel(e.oldValue?.dueDate)} to ${dateLabel(e.newValue?.dueDate)}`;
    case "completed":
      return "marked it done";
    case "reopened":
      return "reopened it";
  }
}
```

`src/lib/items/service.ts`:

```ts
import { and, asc, eq, gte, inArray, or, sql, type SQL } from "drizzle-orm";
import type { Db } from "../db/client";
import { actionItems, itemEvents, meetings, teamMembers, users } from "../db/schema";
import { isIsoDate } from "../dates/isoDate";
import { ConflictError, NotFoundError, ValidationError } from "../errors";

export interface BoardFilters {
  ownerId?: string;
  meetingId?: string;
  includeDoneSince?: Date;
}

export interface BoardRow {
  id: string;
  text: string;
  status: "open" | "done";
  dueDate: string | null;
  ownerMemberId: string;
  ownerName: string;
  meetingId: string;
  meetingTitle: string;
  meetingDate: string;
  completedAt: Date | null;
  createdAt: Date;
}

export type BoardItemPatch = { text?: string; ownerMemberId?: string; dueDate?: string | null };

export interface HistoryEvent {
  id: number;
  kind: "created" | "text" | "owner" | "due_date" | "completed" | "reopened";
  at: Date;
  actorName: string;
  oldValue: Record<string, unknown> | null;
  newValue: Record<string, unknown> | null;
}

type Tx = Parameters<Parameters<Db["transaction"]>[0]>[0];

export async function listBoard(db: Db, filters: BoardFilters): Promise<BoardRow[]> {
  const conditions: SQL[] = [];
  conditions.push(
    filters.includeDoneSince
      ? or(
          eq(actionItems.status, "open"),
          and(eq(actionItems.status, "done"), gte(actionItems.completedAt, filters.includeDoneSince)),
        )!
      : eq(actionItems.status, "open"),
  );
  if (filters.ownerId) conditions.push(eq(actionItems.ownerMemberId, filters.ownerId));
  if (filters.meetingId) conditions.push(eq(actionItems.meetingId, filters.meetingId));

  const rows = await db
    .select({
      id: actionItems.id,
      text: actionItems.text,
      status: actionItems.status,
      dueDate: actionItems.dueDate,
      ownerMemberId: teamMembers.id,
      ownerName: teamMembers.displayName,
      meetingId: meetings.id,
      meetingTitle: meetings.title,
      meetingDate: meetings.meetingDate,
      completedAt: actionItems.completedAt,
      createdAt: actionItems.createdAt,
    })
    .from(actionItems)
    .innerJoin(teamMembers, eq(actionItems.ownerMemberId, teamMembers.id))
    .innerJoin(meetings, eq(actionItems.meetingId, meetings.id))
    .where(and(...conditions))
    .orderBy(asc(actionItems.status), sql`${actionItems.dueDate} asc nulls last`, asc(actionItems.createdAt), asc(actionItems.id));

  return rows.map((r) => ({ ...r, status: r.status as "open" | "done" }));
}

async function lockBoardItem(tx: Tx, itemId: string) {
  const [item] = await tx.select().from(actionItems).where(eq(actionItems.id, itemId)).for("update");
  if (!item) throw new NotFoundError("Action item not found");
  if (item.status === "draft") throw new ConflictError("not_draft", "This item is still in review. Edit it on the review screen.");
  return item;
}

export async function updateItem(db: Db, itemId: string, actorId: string, patch: BoardItemPatch): Promise<number> {
  return db.transaction(async (tx) => {
    const item = await lockBoardItem(tx, itemId);
    const set: Partial<typeof actionItems.$inferInsert> = {};
    const events: Array<Pick<typeof itemEvents.$inferInsert, "kind" | "oldValue" | "newValue">> = [];

    if (patch.text !== undefined) {
      const text = patch.text.trim();
      if (text === "") throw new ValidationError("Action item text cannot be empty");
      if (text !== item.text) {
        set.text = text;
        events.push({ kind: "text", oldValue: { text: item.text }, newValue: { text } });
      }
    }
    if (patch.ownerMemberId !== undefined && patch.ownerMemberId !== item.ownerMemberId) {
      const members = await tx
        .select({ id: teamMembers.id, name: teamMembers.displayName })
        .from(teamMembers)
        .where(inArray(teamMembers.id, [item.ownerMemberId!, patch.ownerMemberId]));
      const name = (id: string) => members.find((m) => m.id === id)?.name;
      if (!name(patch.ownerMemberId)) throw new ValidationError("Unknown team member");
      set.ownerMemberId = patch.ownerMemberId;
      events.push({
        kind: "owner",
        oldValue: { memberId: item.ownerMemberId, name: name(item.ownerMemberId!) ?? null },
        newValue: { memberId: patch.ownerMemberId, name: name(patch.ownerMemberId) },
      });
    }
    if (patch.dueDate !== undefined && patch.dueDate !== item.dueDate) {
      if (patch.dueDate !== null && !isIsoDate(patch.dueDate)) throw new ValidationError("Due date must be a valid date");
      set.dueDate = patch.dueDate;
      events.push({ kind: "due_date", oldValue: { dueDate: item.dueDate }, newValue: { dueDate: patch.dueDate } });
    }

    if (events.length === 0) return 0;
    const now = new Date();
    await tx.update(actionItems).set({ ...set, updatedAt: now }).where(eq(actionItems.id, itemId));
    await tx.insert(itemEvents).values(events.map((e) => ({ ...e, itemId, actorId, at: now })));
    return events.length;
  });
}

export async function setDone(db: Db, itemId: string, actorId: string, done: boolean): Promise<boolean> {
  return db.transaction(async (tx) => {
    const item = await lockBoardItem(tx, itemId);
    const target = done ? "done" : "open";
    if (item.status === target) return false;
    const now = new Date();
    await tx
      .update(actionItems)
      .set({ status: target, completedBy: done ? actorId : null, completedAt: done ? now : null, updatedAt: now })
      .where(eq(actionItems.id, itemId));
    await tx.insert(itemEvents).values({
      itemId,
      actorId,
      at: now,
      kind: done ? "completed" : "reopened",
      oldValue: { status: item.status },
      newValue: { status: target },
    });
    return true;
  });
}

export async function getItemHistory(db: Db, itemId: string): Promise<HistoryEvent[]> {
  const rows = await db
    .select({
      id: itemEvents.id,
      kind: itemEvents.kind,
      at: itemEvents.at,
      oldValue: itemEvents.oldValue,
      newValue: itemEvents.newValue,
      actorName: users.name,
      actorEmail: users.email,
    })
    .from(itemEvents)
    .innerJoin(users, eq(itemEvents.actorId, users.id))
    .where(eq(itemEvents.itemId, itemId))
    .orderBy(asc(itemEvents.id));
  return rows.map(({ actorEmail, ...r }) => ({
    ...r,
    actorName: r.actorName ?? actorEmail,
    oldValue: r.oldValue ?? null,
    newValue: r.newValue ?? null,
  }));
}
```

- [ ] **Step 4: Run the tests and confirm they pass**

Run: `npm test -- tests/unit/dates tests/unit/items tests/integration/items && npm run typecheck`
Expected: all PASS, with no type errors.

- [ ] **Step 5: Commit**

```bash
git add src/lib/items src/lib/dates/display.ts tests/unit/items tests/unit/dates/display.test.ts tests/integration/items
git commit -m "feat: board listing, audited item edits, done/reopen and history"
```

---

### Task 10: Roster alias service

**Files:**
- Create: `src/lib/roster/service.ts`
- Test: `tests/integration/roster/service.test.ts`

**Interfaces:**
- Consumes: `validateAliases`, `AliasValidation`, `resolveOwner` (Task 2), `getRoster` (Task 7), `NotFoundError` (Task 8).
- Produces: `updateAliases(db: Db, memberId: string, actorId: string, rawAliases: string[]): Promise<AliasValidation>`. It writes a `roster_events` row only when the aliases actually change.

- [ ] **Step 1: Write the failing test**

`tests/integration/roster/service.test.ts`:

```ts
import { beforeAll, beforeEach, describe, expect, it } from "vitest";
import type { Db } from "@/lib/db/client";
import { rosterEvents } from "@/lib/db/schema";
import { NotFoundError } from "@/lib/errors";
import { getRoster } from "@/lib/roster/repository";
import { resolveOwner } from "@/lib/roster/resolveOwner";
import { updateAliases } from "@/lib/roster/service";
import { createUser, seedTestRoster } from "../../helpers/factories";
import { createTestDb, resetDb } from "../../helpers/testDb";

let db: Db;
let ids: Record<string, string>;
let userId: string;

beforeAll(async () => {
  db = await createTestDb();
});
beforeEach(async () => {
  await resetDb(db);
  ids = await seedTestRoster(db);
  userId = (await createUser(db)).id;
});

describe("updateAliases", () => {
  it("saves normalized aliases, logs the change, and future matching uses them", async () => {
    expect(await updateAliases(db, ids.Ravi, userId, ["RJ", " rav "])).toEqual({ ok: true, aliases: ["rj", "rav"] });
    const [event] = await db.select().from(rosterEvents);
    expect(event).toMatchObject({ memberId: ids.Ravi, actorId: userId, oldAliases: [], newAliases: ["rj", "rav"] });
    expect(resolveOwner("RJ", await getRoster(db))).toEqual({ kind: "assigned", memberId: ids.Ravi });
  });

  it("rejects clashes without writing anything", async () => {
    expect(await updateAliases(db, ids.Ravi, userId, ["tom"])).toEqual({ ok: false, error: "“tom” is already used by Tomás" });
    expect(await db.select().from(rosterEvents)).toHaveLength(0);
  });

  it("does not log a no-op save", async () => {
    await updateAliases(db, ids["Tomás"], userId, ["Tom"]);
    expect(await db.select().from(rosterEvents)).toHaveLength(0);
  });

  it("throws for an unknown member", async () => {
    await expect(updateAliases(db, "00000000-0000-0000-0000-000000000000", userId, ["x"])).rejects.toBeInstanceOf(NotFoundError);
  });
});
```

- [ ] **Step 2: Run it and confirm it fails**

Run: `npm test -- tests/integration/roster`
Expected: FAIL. The module doesn't exist yet.

- [ ] **Step 3: Implement**

`src/lib/roster/service.ts`:

```ts
import { eq } from "drizzle-orm";
import type { Db } from "../db/client";
import { rosterEvents, teamMembers } from "../db/schema";
import { NotFoundError } from "../errors";
import { validateAliases, type AliasValidation } from "./aliases";
import { getRoster } from "./repository";

export async function updateAliases(db: Db, memberId: string, actorId: string, rawAliases: string[]): Promise<AliasValidation> {
  const roster = await getRoster(db);
  const member = roster.find((m) => m.id === memberId);
  if (!member) throw new NotFoundError("Team member not found");

  const result = validateAliases(roster, memberId, rawAliases);
  if (!result.ok) return result;

  const unchanged =
    result.aliases.length === member.aliases.length && result.aliases.every((a, i) => a === member.aliases[i]);
  if (unchanged) return result;

  await db.transaction(async (tx) => {
    await tx.update(teamMembers).set({ aliases: result.aliases }).where(eq(teamMembers.id, memberId));
    await tx.insert(rosterEvents).values({ memberId, actorId, oldAliases: member.aliases, newAliases: result.aliases });
  });
  return result;
}
```

- [ ] **Step 4: Run the tests and confirm they pass**

Run: `npm test -- tests/integration/roster`
Expected: all PASS.

- [ ] **Step 5: Commit**

```bash
git add src/lib/roster/service.ts tests/integration/roster
git commit -m "feat: alias editing with clash checks and audit log"
```

---

### Task 11: Authentication (Google, domain-restricted)

**Files:**
- Create: `src/lib/auth/domain.ts`, `src/lib/auth/bypass.ts`, `src/lib/auth/requireUser.ts`, `src/auth.ts`, `src/middleware.ts`, `src/instrumentation.ts`, `src/app/api/auth/[...nextauth]/route.ts`, `src/app/signin/page.tsx`, `src/app/restricted/page.tsx`
- Modify: `src/app/layout.tsx` (add nav and sign-out)
- Test: `tests/unit/auth/domain.test.ts`, `tests/unit/auth/bypass.test.ts`

**Interfaces:**
- Consumes: `getDb`, `users` (Task 7), `requiredEnv` (Task 7), `assertExtractorConfig` (Task 5).
- Produces:
  - `isAllowedGoogleProfile(profile: Record<string, unknown> | null | undefined, allowedDomain: string): boolean`
  - `testBypassEmail(env?): string | null`. Throws when `AUTH_TEST_BYPASS=1` and `NODE_ENV=production`.
  - `interface AppUser { id: string; email: string; name: string | null }` and `requireUser(): Promise<AppUser>`. Redirects to `/signin` or `/restricted` when the user isn't allowed. On first sight, creates or updates the user's `users` row.
  - `handlers`, `auth`, `signIn`, `signOut` from `src/auth.ts`

- [ ] **Step 1: Write the failing tests**

`tests/unit/auth/domain.test.ts`:

```ts
import { describe, expect, it } from "vitest";
import { isAllowedGoogleProfile } from "@/lib/auth/domain";

const D = "ourcompany.com";
const good = { email: "priya@ourcompany.com", email_verified: true, hd: "ourcompany.com" };

describe("isAllowedGoogleProfile", () => {
  it("allows a verified Workspace account on the domain", () => {
    expect(isAllowedGoogleProfile(good, D)).toBe(true);
    expect(isAllowedGoogleProfile({ ...good, email: "Priya@OurCompany.com", hd: "OURCOMPANY.COM" }, D)).toBe(true);
  });
  it.each([
    ["personal Gmail (no hd)", { email: "priya@gmail.com", email_verified: true }],
    ["other Workspace domain", { ...good, email: "p@other.com", hd: "other.com" }],
    ["unverified email", { ...good, email_verified: false }],
    ["lookalike hd", { ...good, hd: "ourcompany.com.evil.io" }],
    ["hd matches but email domain does not", { ...good, email: "p@evil-ourcompany.com" }],
    ["missing profile", undefined],
  ])("rejects %s", (_label, profile) => {
    expect(isAllowedGoogleProfile(profile, D)).toBe(false);
  });
  it("rejects everything when the allowed domain is blank", () => {
    expect(isAllowedGoogleProfile(good, " ")).toBe(false);
  });
});
```

`tests/unit/auth/bypass.test.ts`:

```ts
import { describe, expect, it } from "vitest";
import { testBypassEmail } from "@/lib/auth/bypass";

describe("testBypassEmail", () => {
  it("is off by default", () => {
    expect(testBypassEmail({})).toBeNull();
  });
  it("returns the test user when enabled outside production", () => {
    expect(testBypassEmail({ AUTH_TEST_BYPASS: "1", NODE_ENV: "development", ALLOWED_DOMAIN: "ourcompany.com" })).toBe(
      "e2e-tester@ourcompany.com",
    );
    expect(testBypassEmail({ AUTH_TEST_BYPASS: "1", AUTH_TEST_BYPASS_EMAIL: "x@ourcompany.com" })).toBe("x@ourcompany.com");
  });
  it("refuses to run in production", () => {
    expect(() => testBypassEmail({ AUTH_TEST_BYPASS: "1", NODE_ENV: "production" })).toThrow(/not allowed/);
  });
});
```

- [ ] **Step 2: Run them and confirm they fail**

Run: `npm test -- tests/unit/auth`
Expected: FAIL. The modules don't exist yet.

- [ ] **Step 3: Implement the pure helpers**

`src/lib/auth/domain.ts`:

```ts
export function isAllowedGoogleProfile(
  profile: Record<string, unknown> | null | undefined,
  allowedDomain: string,
): boolean {
  if (!profile) return false;
  const domain = allowedDomain.trim().toLowerCase();
  if (domain === "") return false;
  const email = typeof profile.email === "string" ? profile.email.toLowerCase() : "";
  const hd = typeof profile.hd === "string" ? profile.hd.toLowerCase() : "";
  return profile.email_verified === true && hd === domain && email.endsWith(`@${domain}`);
}
```

`src/lib/auth/bypass.ts`:

```ts
type Env = Record<string, string | undefined>;

/** E2E-only sign-in bypass. Fails closed in production. */
export function testBypassEmail(env: Env = process.env): string | null {
  if (env.AUTH_TEST_BYPASS !== "1") return null;
  if (env.NODE_ENV === "production") {
    throw new Error("AUTH_TEST_BYPASS=1 is not allowed when NODE_ENV=production");
  }
  return env.AUTH_TEST_BYPASS_EMAIL || `e2e-tester@${env.ALLOWED_DOMAIN ?? "ourcompany.com"}`;
}
```

- [ ] **Step 4: Run the tests and confirm they pass**

Run: `npm test -- tests/unit/auth`
Expected: all PASS.

- [ ] **Step 5: Wire up Auth.js, middleware and `requireUser`**

`src/auth.ts`:

```ts
import NextAuth from "next-auth";
import Google from "next-auth/providers/google";
import { isAllowedGoogleProfile } from "./lib/auth/domain";

export const { handlers, auth, signIn, signOut } = NextAuth({
  providers: [
    Google({
      authorization: { params: { hd: process.env.ALLOWED_DOMAIN, prompt: "select_account" } },
    }),
  ],
  session: { strategy: "jwt" },
  pages: { signIn: "/signin", error: "/restricted" },
  callbacks: {
    signIn({ account, profile }) {
      if (account?.provider !== "google") return false;
      const allowed = isAllowedGoogleProfile(profile as Record<string, unknown> | undefined, process.env.ALLOWED_DOMAIN ?? "");
      return allowed ? true : "/restricted";
    },
  },
});
```

`src/app/api/auth/[...nextauth]/route.ts`:

```ts
import { handlers } from "@/auth";

export const { GET, POST } = handlers;
```

`src/middleware.ts`:

```ts
import { auth } from "@/auth";
import { testBypassEmail } from "@/lib/auth/bypass";

const PUBLIC_PREFIXES = ["/signin", "/restricted", "/api/auth"];

export default auth((req) => {
  if (testBypassEmail()) return;
  const { pathname } = req.nextUrl;
  if (PUBLIC_PREFIXES.some((p) => pathname.startsWith(p))) return;
  if (!req.auth) return Response.redirect(new URL("/signin", req.nextUrl));
});

export const config = { matcher: ["/((?!_next/static|_next/image|favicon.ico).*)"] };
```

`src/lib/auth/requireUser.ts`:

```ts
import { redirect } from "next/navigation";
import { auth } from "@/auth";
import { getDb } from "../db/client";
import { users } from "../db/schema";
import { requiredEnv } from "../env";
import { testBypassEmail } from "./bypass";

export interface AppUser {
  id: string;
  email: string;
  name: string | null;
}

export async function requireUser(): Promise<AppUser> {
  const allowedDomain = requiredEnv("ALLOWED_DOMAIN").trim().toLowerCase();
  let email: string;
  let name: string | null;

  const bypass = testBypassEmail();
  if (bypass) {
    email = bypass;
    name = "E2E Tester";
  } else {
    const session = await auth();
    if (!session?.user?.email) redirect("/signin");
    email = session.user.email;
    name = session.user.name ?? null;
  }

  // Defence in depth: re-check the domain on every request, not only at sign-in.
  email = email.toLowerCase();
  if (!email.endsWith(`@${allowedDomain}`)) redirect("/restricted");

  const [user] = await getDb()
    .insert(users)
    .values({ email, name })
    .onConflictDoUpdate({ target: users.email, set: { name } })
    .returning();
  return { id: user.id, email: user.email, name: user.name };
}
```

`src/instrumentation.ts`:

```ts
export async function register() {
  if (process.env.NEXT_RUNTIME === "nodejs") {
    const { testBypassEmail } = await import("./lib/auth/bypass");
    const { assertExtractorConfig } = await import("./lib/extraction");
    testBypassEmail(); // throws at startup if the E2E bypass is enabled in production
    assertExtractorConfig(); // throws at startup if the fake extractor is enabled in production
  }
}
```

`src/app/signin/page.tsx`:

```tsx
import { signIn } from "@/auth";

export default function SignInPage() {
  return (
    <div className="narrow stack">
      <h1>Meeting Action Items</h1>
      <p>Sign in with your company Google account.</p>
      <form
        action={async () => {
          "use server";
          await signIn("google", { redirectTo: "/board" });
        }}
      >
        <button type="submit">Sign in with Google</button>
      </form>
    </div>
  );
}
```

`src/app/restricted/page.tsx`:

```tsx
import Link from "next/link";

export default function RestrictedPage() {
  return (
    <div className="narrow stack">
      <h1>Access restricted</h1>
      <p>This app is only available to verified @{process.env.ALLOWED_DOMAIN} Google Workspace accounts.</p>
      <Link href="/signin">Try a different account</Link>
    </div>
  );
}
```

Replace `src/app/layout.tsx` with:

```tsx
import Link from "next/link";
import { signOut } from "@/auth";
import "./globals.css";

export const metadata = { title: "Meeting Action Items" };

export default function RootLayout({ children }: { children: React.ReactNode }) {
  return (
    <html lang="en">
      <body>
        <header className="topbar">
          <nav>
            <Link href="/board">Board</Link>
            <Link href="/new">New meeting</Link>
            <Link href="/team">Team</Link>
          </nav>
          <form
            action={async () => {
              "use server";
              await signOut({ redirectTo: "/signin" });
            }}
          >
            <button type="submit" className="link">Sign out</button>
          </form>
        </header>
        <main>{children}</main>
      </body>
    </html>
  );
}
```

- [ ] **Step 6: Typecheck, test and build**

Run: `npm test && npm run typecheck && npm run build`
Expected: all tests PASS, and the build succeeds.

Manual check (needs Google OAuth credentials for a test Workspace; skip if you don't have them yet). Run `npm run dev` without `AUTH_TEST_BYPASS`. Opening `/board` should redirect to `/signin`. Signing in with a personal Gmail account should land on `/restricted`.

- [ ] **Step 7: Commit**

```bash
git add src/auth.ts src/middleware.ts src/instrumentation.ts src/lib/auth src/app/api src/app/signin src/app/restricted src/app/layout.tsx tests/unit/auth
git commit -m "feat: Google sign-in restricted to the Workspace domain"
```

---

### Task 12: Paste page and E2E harness

**Files:**
- Create: `src/lib/config.ts`, `src/app/actions/result.ts`, `src/app/actions/meetings.ts`, `src/app/new/page.tsx`, `src/app/new/PasteForm.tsx`
- Create: `playwright.config.ts`, `tests/e2e/global-setup.ts`, `tests/e2e/helpers.ts`, `tests/e2e/paste.spec.ts`

**Interfaces:**
- Consumes: `requireUser` (Task 11), `getDb` (Task 7), `MeetingInputSchema`, `hashNotes`, `findDuplicateMeeting`, `createDraftMeeting`, `runExtraction` (Task 8), `getExtractor` (Task 5), `MAX_NOTES_CHARS` (Task 8), `FAKE_FAILURE_MARKER` (Task 5).
- Produces:
  - `dateLocale(): string`
  - `type ActionResult = { ok: true } | { ok: false; error: string }` and `runAction(fn: () => Promise<unknown>): Promise<ActionResult>`. It turns `ValidationError`/`ConflictError`/`NotFoundError` into `{ ok: false }` and rethrows anything else.
  - `type CreateMeetingState = { fieldErrors?: Record<string, string>; duplicate?: { id: string; title: string; createdAt: string } }` and `createMeetingAction(prev, formData)`
  - E2E helpers: `uniqueTag(): string`, `pasteMeeting(page, title, lines): Promise<void>` (ends on the review screen), `selectInNotes(page, phrase)`

- [ ] **Step 1: Write the E2E harness and failing test**

`playwright.config.ts`:

```ts
import { defineConfig } from "@playwright/test";

export const E2E_DATABASE_URL = process.env.E2E_DATABASE_URL ?? "postgres://postgres:postgres@localhost:5432/actions_e2e";

export default defineConfig({
  testDir: "tests/e2e",
  workers: 1,
  fullyParallel: false,
  retries: 0,
  expect: { timeout: 15_000 },
  use: { baseURL: "http://localhost:3100", trace: "retain-on-failure" },
  globalSetup: "./tests/e2e/global-setup.ts",
  webServer: {
    command: "npx next dev --port 3100",
    url: "http://localhost:3100/signin",
    reuseExistingServer: false,
    timeout: 180_000,
    env: {
      DATABASE_URL: E2E_DATABASE_URL,
      AUTH_TEST_BYPASS: "1",
      EXTRACTOR: "fake",
      ALLOWED_DOMAIN: "ourcompany.com",
      AUTH_SECRET: "e2e-only-secret-not-for-production",
      AUTH_GOOGLE_ID: "e2e",
      AUTH_GOOGLE_SECRET: "e2e",
      DATE_LOCALE: "en-US",
    },
  },
});
```

`tests/e2e/global-setup.ts`:

```ts
import { drizzle } from "drizzle-orm/node-postgres";
import { migrate } from "drizzle-orm/node-postgres/migrator";
import { Pool } from "pg";
import roster from "../../config/roster.json";
import type { Db } from "../../src/lib/db/client";
import * as schema from "../../src/lib/db/schema";
import { seedRoster } from "../../src/lib/db/seed";
import { E2E_DATABASE_URL } from "../../playwright.config";

export default async function globalSetup() {
  const pool = new Pool({ connectionString: E2E_DATABASE_URL });
  const db = drizzle(pool, { schema });
  await migrate(db, { migrationsFolder: "drizzle" });
  await pool.query(
    "TRUNCATE item_events, roster_events, action_items, meetings, users, team_members RESTART IDENTITY CASCADE",
  );
  await seedRoster(db as unknown as Db, roster);
  await pool.end();
}
```

`tests/e2e/helpers.ts`:

```ts
import { expect, type Page } from "@playwright/test";

export const uniqueTag = () => `${Date.now().toString(36)}${Math.random().toString(36).slice(2, 6)}`;

export async function pasteMeeting(page: Page, title: string, lines: string[]) {
  await page.goto("/new");
  await page.getByLabel("Meeting title").fill(title);
  await page.getByLabel("Notes").fill(lines.join("\n"));
  await page.getByRole("button", { name: "Extract action items" }).click();
  await expect(page).toHaveURL(/\/meetings\/[0-9a-f-]+\/review$/);
}

/** Selects `phrase` inside the notes pane, the way a user would with the mouse. */
export async function selectInNotes(page: Page, phrase: string) {
  await page.evaluate((p) => {
    const pre = document.querySelector('[data-testid="notes"]');
    if (!pre) throw new Error("Notes pane not found");
    for (const el of Array.from(pre.querySelectorAll("[data-seg-start]"))) {
      const node = el.firstChild;
      if (!node || node.nodeType !== Node.TEXT_NODE) continue;
      const i = (node.textContent ?? "").indexOf(p);
      if (i === -1) continue;
      const range = document.createRange();
      range.setStart(node, i);
      range.setEnd(node, i + p.length);
      const sel = window.getSelection()!;
      sel.removeAllRanges();
      sel.addRange(range);
      return;
    }
    throw new Error(`Phrase not found in notes: ${p}`);
  }, phrase);
}
```

`tests/e2e/paste.spec.ts`:

```ts
import { expect, test } from "@playwright/test";
import { pasteMeeting, uniqueTag } from "./helpers";

test("pasting notes creates a draft and opens the review screen", async ({ page }) => {
  const tag = uniqueTag();
  await pasteMeeting(page, `Weekly sync ${tag}`, [`Notes ${tag}`, "- ACTION: Send launch deck | owner: Tom | due: Friday"]);
});

test("pasting the same notes twice warns before creating a duplicate", async ({ page }) => {
  const tag = uniqueTag();
  const lines = [`Duplicate check ${tag}`, "- ACTION: Book venue | owner: Dana"];
  await pasteMeeting(page, `First ${tag}`, lines);

  await page.goto("/new");
  await page.getByLabel("Meeting title").fill(`Second ${tag}`);
  await page.getByLabel("Notes").fill(lines.join("\n"));
  await page.getByRole("button", { name: "Extract action items" }).click();
  await expect(page.getByRole("alert")).toContainText(`These notes were already added`);
  await expect(page.getByRole("alert")).toContainText(`First ${tag}`);
  await page.getByRole("button", { name: "Add anyway" }).click();
  await expect(page).toHaveURL(/\/review$/);
});

test("whitespace-only notes are rejected with a message", async ({ page }) => {
  await page.goto("/new");
  await page.getByLabel("Meeting title").fill("Empty");
  await page.getByLabel("Notes").fill("   \n  ");
  await page.getByRole("button", { name: "Extract action items" }).click();
  await expect(page.getByText("Paste the meeting notes")).toBeVisible();
  await expect(page).toHaveURL(/\/new$/);
});
```

- [ ] **Step 2: Run it and confirm it fails**

Run: `docker compose up -d postgres && npm run e2e -- paste.spec.ts`
Expected: FAIL. `/new` returns 404, so the "Meeting title" label isn't found.

- [ ] **Step 3: Implement the action and page**

`src/lib/config.ts`:

```ts
export function dateLocale(): string {
  return process.env.DATE_LOCALE || "en-US";
}
```

`src/app/actions/result.ts`:

```ts
import { ConflictError, NotFoundError, ValidationError } from "@/lib/errors";

export type ActionResult = { ok: true } | { ok: false; error: string };

export async function runAction(fn: () => Promise<unknown>): Promise<ActionResult> {
  try {
    await fn();
    return { ok: true };
  } catch (err) {
    if (err instanceof ValidationError || err instanceof ConflictError || err instanceof NotFoundError) {
      return { ok: false, error: err.message };
    }
    throw err;
  }
}
```

`src/app/actions/meetings.ts`:

```ts
"use server";

import { redirect } from "next/navigation";
import { requireUser } from "@/lib/auth/requireUser";
import { dateLocale } from "@/lib/config";
import { getDb } from "@/lib/db/client";
import { getExtractor } from "@/lib/extraction";
import { MeetingInputSchema, createDraftMeeting, findDuplicateMeeting, hashNotes, runExtraction } from "@/lib/meetings/service";

export type CreateMeetingState = {
  fieldErrors?: Record<string, string>;
  duplicate?: { id: string; title: string; createdAt: string };
};

export async function createMeetingAction(_prev: CreateMeetingState, formData: FormData): Promise<CreateMeetingState> {
  const user = await requireUser();
  const parsed = MeetingInputSchema.safeParse({
    title: String(formData.get("title") ?? ""),
    meetingDate: String(formData.get("meetingDate") ?? ""),
    notes: String(formData.get("notes") ?? ""),
  });
  if (!parsed.success) {
    return { fieldErrors: Object.fromEntries(parsed.error.issues.map((i) => [String(i.path[0]), i.message])) };
  }

  const db = getDb();
  if (formData.get("confirmDuplicate") !== "1") {
    const dup = await findDuplicateMeeting(db, hashNotes(parsed.data.notes));
    if (dup) return { duplicate: { id: dup.id, title: dup.title, createdAt: dup.createdAt.toISOString() } };
  }

  const meetingId = await createDraftMeeting(db, parsed.data, user.id);
  await runExtraction(db, meetingId, getExtractor(), dateLocale()); // failures are stored and shown on the review screen
  redirect(`/meetings/${meetingId}/review`);
}
```

`src/app/new/page.tsx`:

```tsx
import { requireUser } from "@/lib/auth/requireUser";
import { PasteForm } from "./PasteForm";

export default async function NewMeetingPage() {
  await requireUser();
  return (
    <div className="stack">
      <h1>New meeting</h1>
      <p className="muted">Paste the notes. You'll review the action items before they go on the board.</p>
      <PasteForm />
    </div>
  );
}
```

`src/app/new/PasteForm.tsx`:

```tsx
"use client";

import { useActionState, useEffect, useState } from "react";
import { createMeetingAction, type CreateMeetingState } from "@/app/actions/meetings";
import { MAX_NOTES_CHARS } from "@/lib/limits";

export function PasteForm() {
  const [state, formAction, pending] = useActionState<CreateMeetingState, FormData>(createMeetingAction, {});
  const [title, setTitle] = useState("");
  const [meetingDate, setMeetingDate] = useState("");
  const [notes, setNotes] = useState("");

  // Default to today in the browser's time zone (set after mount to avoid a server/client mismatch).
  useEffect(() => {
    setMeetingDate((d) => d || new Date().toLocaleDateString("en-CA"));
  }, []);

  const tooLong = notes.length > MAX_NOTES_CHARS;
  const errors = state.fieldErrors ?? {};

  return (
    <form action={formAction} className="stack">
      <label className="stack">
        Meeting title
        <input name="title" value={title} onChange={(e) => setTitle(e.target.value)} required maxLength={200} />
      </label>
      {errors.title && <p className="error">{errors.title}</p>}

      <label className="stack">
        Meeting date
        <input type="date" name="meetingDate" value={meetingDate} onChange={(e) => setMeetingDate(e.target.value)} required />
      </label>
      {errors.meetingDate && <p className="error">{errors.meetingDate}</p>}

      <label className="stack">
        Notes
        <textarea name="notes" rows={18} value={notes} onChange={(e) => setNotes(e.target.value)} />
      </label>
      <p className={tooLong ? "error" : "muted"}>
        {notes.length.toLocaleString("en-US")} / {MAX_NOTES_CHARS.toLocaleString("en-US")} characters
        {tooLong && " (too long; split the notes into two meetings)"}
      </p>
      {errors.notes && <p className="error">{errors.notes}</p>}

      {state.duplicate && (
        <div className="warning" role="alert">
          These notes were already added on {new Date(state.duplicate.createdAt).toLocaleDateString()} as “
          {state.duplicate.title}”. <a href={`/meetings/${state.duplicate.id}/review`}>Open it</a>, or add them again.
          <input type="hidden" name="confirmDuplicate" value="1" />
        </div>
      )}

      <button type="submit" disabled={pending || tooLong}>
        {pending ? "Extracting action items…" : state.duplicate ? "Add anyway" : "Extract action items"}
      </button>
    </form>
  );
}
```

- [ ] **Step 4: Run the tests and confirm they pass**

Run: `npm run e2e -- paste.spec.ts && npm run typecheck`
Expected: 3 PASS. (The review page is built in the next task. This test only checks the redirect URL.)

- [ ] **Step 5: Commit**

```bash
git add src/lib/config.ts src/app/actions src/app/new playwright.config.ts tests/e2e
git commit -m "feat: paste page with duplicate warning, plus Playwright harness"
```

---

### Task 13: Review screen

**Files:**
- Create: `src/lib/notes/segments.ts`, `src/lib/flagLabels.ts`, `src/app/actions/review.ts`
- Create: `src/app/components/NotesPane.tsx`, `src/app/components/FlagBadges.tsx`
- Create: `src/app/meetings/[id]/review/page.tsx`, `src/app/meetings/[id]/review/ReviewWorkspace.tsx`, `src/app/meetings/[id]/review/ItemRow.tsx`
- Test: `tests/unit/notes/segments.test.ts`, `tests/e2e/review.spec.ts`

**Interfaces:**
- Consumes: meetings service (Task 8), `runAction`/`ActionResult` (Task 12), `requireUser` (Task 11), `getExtractor` (Task 5), `dateLocale` (Task 12), `isBlocking`/`Flag` (Task 1), E2E helpers (Task 12).
- Produces:
  - `interface Segment { start: number; end: number; text: string; itemIds: string[] }`, `buildSegments(notes, ranges: Array<{ id: string; start: number; end: number }>): Segment[]`, `selectionToRange(a: { segmentStart: number; offset: number }, b: same): { start: number; end: number } | null`
  - `FLAG_LABELS: Record<Flag, string>`
  - `NotesPane` props: `{ notes: string; ranges: Array<{ id: string; start: number; end: number }>; activeItemId?: string | null; onHighlightClick?: (itemId: string) => void; onSelectRange?: (range: { start: number; end: number }) => void }`. The "Add selected text" button only appears when `onSelectRange` is given.
  - `FlagBadges` props: `{ flags: Flag[] }`
  - Server actions: `updateDraftItemAction(itemId, patch)`, `splitDraftItemAction(itemId)`, `addManualItemAction(meetingId, start, end)`, `deleteDraftItemAction(itemId)`, `retryExtractionAction(meetingId)`, `commitMeetingAction(meetingId)`. All return `Promise<ActionResult>`; commit redirects to `/board?meeting=<id>` on success.

- [ ] **Step 1: Write the failing tests**

`tests/unit/notes/segments.test.ts`:

```ts
import { describe, expect, it } from "vitest";
import { buildSegments, selectionToRange } from "@/lib/notes/segments";

describe("buildSegments", () => {
  it("returns one plain segment when nothing is highlighted", () => {
    expect(buildSegments("hello", [])).toEqual([{ start: 0, end: 5, text: "hello", itemIds: [] }]);
  });
  it("splits around overlapping ranges", () => {
    expect(buildSegments("abcdefgh", [{ id: "a", start: 1, end: 4 }, { id: "b", start: 3, end: 6 }])).toEqual([
      { start: 0, end: 1, text: "a", itemIds: [] },
      { start: 1, end: 3, text: "bc", itemIds: ["a"] },
      { start: 3, end: 4, text: "d", itemIds: ["a", "b"] },
      { start: 4, end: 6, text: "ef", itemIds: ["b"] },
      { start: 6, end: 8, text: "gh", itemIds: [] },
    ]);
  });
  it("ignores out-of-bounds or empty ranges", () => {
    expect(buildSegments("abc", [{ id: "x", start: 2, end: 9 }, { id: "y", start: 1, end: 1 }])).toEqual([
      { start: 0, end: 3, text: "abc", itemIds: [] },
    ]);
  });
});

describe("selectionToRange", () => {
  it("orders backwards selections and rejects empty ones", () => {
    expect(selectionToRange({ segmentStart: 10, offset: 4 }, { segmentStart: 0, offset: 2 })).toEqual({ start: 2, end: 14 });
    expect(selectionToRange({ segmentStart: 5, offset: 0 }, { segmentStart: 5, offset: 0 })).toBeNull();
  });
});
```

`tests/e2e/review.spec.ts`:

```ts
import { expect, test } from "@playwright/test";
import { FAKE_FAILURE_MARKER } from "../../src/lib/extraction/fakeExtractor";
import { pasteMeeting, selectInNotes, uniqueTag } from "./helpers";

const row = (page: import("@playwright/test").Page, text: string) => page.locator(`[data-item-text="${text}"]`);

test("reviewer resolves flags, adds a missed item, and commits", async ({ page }) => {
  const tag = uniqueTag();
  await pasteMeeting(page, `Review ${tag}`, [
    `Planning ${tag}`,
    "- ACTION: Send launch deck | owner: Tom | due: Friday",
    "- ACTION: Book venue | owner: Sam",
    "- ACTION: Review pricing | owner: Tom and Priya",
    "Lena will draft the FAQ",
  ]);

  await expect(page.getByTestId("item-row")).toHaveCount(3);
  await expect(row(page, "Send launch deck").locator('[data-flag]')).toHaveCount(0);
  await expect(row(page, "Book venue").locator('[data-flag="unknown_owner"]')).toBeVisible();
  await expect(row(page, "Book venue")).toContainText("Notes say: “Sam”");
  const commit = page.getByRole("button", { name: "Add to board" });
  await expect(commit).toBeDisabled();
  await expect(page.getByText("2 items need an owner")).toBeVisible();

  await row(page, "Book venue").getByLabel("Owner").selectOption({ label: "Marcus" });
  await expect(row(page, "Book venue").locator('[data-flag]')).toHaveCount(0);

  await row(page, "Review pricing").getByRole("button", { name: "Split into 2 items" }).click();
  await expect(page.getByTestId("item-row")).toHaveCount(4);

  await selectInNotes(page, "Lena will draft the FAQ");
  await page.getByRole("button", { name: "Add selected text as item" }).click();
  const lena = row(page, "Lena will draft the FAQ");
  await expect(lena).toContainText("Suggested: Lena");
  await expect(commit).toBeDisabled();
  await lena.getByLabel("Owner").selectOption({ label: "Lena" });

  await expect(commit).toBeEnabled();
  await commit.click();
  await expect(page).toHaveURL(/\/board\?meeting=/);
});

test("failed extraction keeps the notes and offers a retry", async ({ page }) => {
  const tag = uniqueTag();
  await pasteMeeting(page, `Fail ${tag}`, [`Notes ${tag}`, FAKE_FAILURE_MARKER]);
  await expect(page.getByRole("alert")).toContainText("Simulated extraction failure.");
  await expect(page.getByText("Your notes are saved.")).toBeVisible();
  await expect(page.getByRole("button", { name: "Retry extraction" })).toBeVisible();
  await expect(page.getByTestId("notes")).toContainText(`Notes ${tag}`);
});
```

- [ ] **Step 2: Run them and confirm they fail**

Run: `npm test -- tests/unit/notes/segments.test.ts && npm run e2e -- review.spec.ts`
Expected: the unit test FAILS because the module is missing, and the E2E test FAILS because the review page returns 404.

- [ ] **Step 3: Implement the pure helpers and labels**

`src/lib/notes/segments.ts`:

```ts
export interface Segment {
  start: number;
  end: number;
  text: string;
  itemIds: string[];
}

export function buildSegments(notes: string, ranges: Array<{ id: string; start: number; end: number }>): Segment[] {
  const valid = ranges.filter((r) => r.start >= 0 && r.end <= notes.length && r.start < r.end);
  const cuts = new Set<number>([0, notes.length]);
  for (const r of valid) {
    cuts.add(r.start);
    cuts.add(r.end);
  }
  const points = [...cuts].sort((a, b) => a - b);
  const segments: Segment[] = [];
  for (let i = 0; i < points.length - 1; i++) {
    const start = points[i];
    const end = points[i + 1];
    segments.push({
      start,
      end,
      text: notes.slice(start, end),
      itemIds: valid.filter((r) => r.start <= start && r.end >= end).map((r) => r.id),
    });
  }
  return segments;
}

export function selectionToRange(
  a: { segmentStart: number; offset: number },
  b: { segmentStart: number; offset: number },
): { start: number; end: number } | null {
  const x = a.segmentStart + a.offset;
  const y = b.segmentStart + b.offset;
  if (x === y) return null;
  return { start: Math.min(x, y), end: Math.max(x, y) };
}
```

`src/lib/flagLabels.ts`:

```ts
import type { Flag } from "./types";

export const FLAG_LABELS: Record<Flag, string> = {
  missing_owner: "Needs an owner",
  unknown_owner: "Owner not on the roster",
  multiple_owners: "Several owners",
  unparsed_due: "Couldn't read the due date",
  quote_not_found: "Not found in the notes: check it",
  possible_duplicate: "Possible duplicate",
};
```

Run: `npm test -- tests/unit/notes/segments.test.ts`
Expected: PASS.

- [ ] **Step 4: Implement the server actions**

`src/app/actions/review.ts`:

```ts
"use server";

import { redirect } from "next/navigation";
import { z } from "zod";
import { requireUser } from "@/lib/auth/requireUser";
import { dateLocale } from "@/lib/config";
import { getDb } from "@/lib/db/client";
import { getExtractor } from "@/lib/extraction";
import {
  addManualItem, commitMeeting, deleteDraftItem, runExtraction, splitDraftItem, updateDraftItem,
} from "@/lib/meetings/service";
import { runAction, type ActionResult } from "./result";

const Id = z.string().uuid();
const DraftPatch = z.object({
  text: z.string().optional(),
  ownerMemberId: z.string().uuid().nullable().optional(),
  dueDate: z.string().nullable().optional(),
});

export async function updateDraftItemAction(itemId: string, patch: z.input<typeof DraftPatch>): Promise<ActionResult> {
  await requireUser();
  return runAction(() => updateDraftItem(getDb(), Id.parse(itemId), DraftPatch.parse(patch)));
}

export async function splitDraftItemAction(itemId: string): Promise<ActionResult> {
  await requireUser();
  return runAction(() => splitDraftItem(getDb(), Id.parse(itemId)));
}

export async function addManualItemAction(meetingId: string, start: number, end: number): Promise<ActionResult> {
  await requireUser();
  return runAction(() => addManualItem(getDb(), Id.parse(meetingId), { start, end }));
}

export async function deleteDraftItemAction(itemId: string): Promise<ActionResult> {
  await requireUser();
  return runAction(() => deleteDraftItem(getDb(), Id.parse(itemId)));
}

export async function retryExtractionAction(meetingId: string): Promise<ActionResult> {
  await requireUser();
  return runAction(() => runExtraction(getDb(), Id.parse(meetingId), getExtractor(), dateLocale()));
}

export async function commitMeetingAction(meetingId: string): Promise<ActionResult> {
  const user = await requireUser();
  const id = Id.parse(meetingId);
  const result = await runAction(() => commitMeeting(getDb(), id, user.id));
  if (result.ok) redirect(`/board?meeting=${id}`);
  return result;
}
```

- [ ] **Step 5: Implement the shared components**

`src/app/components/FlagBadges.tsx`:

```tsx
import { FLAG_LABELS } from "@/lib/flagLabels";
import { isBlocking, type Flag } from "@/lib/types";

export function FlagBadges({ flags }: { flags: Flag[] }) {
  return (
    <>
      {flags.map((f) => (
        <span key={f} data-flag={f} className={isBlocking(f) ? "flag blocking" : "flag"}>
          {FLAG_LABELS[f]}
        </span>
      ))}
    </>
  );
}
```

`src/app/components/NotesPane.tsx`:

```tsx
"use client";

import { useEffect, useMemo, useRef, useState } from "react";
import { buildSegments, selectionToRange } from "@/lib/notes/segments";

type Range = { start: number; end: number };

export function NotesPane(props: {
  notes: string;
  ranges: Array<{ id: string } & Range>;
  activeItemId?: string | null;
  onHighlightClick?: (itemId: string) => void;
  onSelectRange?: (range: Range) => void;
}) {
  const { notes, ranges, activeItemId, onHighlightClick, onSelectRange } = props;
  const segments = useMemo(() => buildSegments(notes, ranges), [notes, ranges]);
  const ref = useRef<HTMLPreElement>(null);
  const [hint, setHint] = useState<string | null>(null);

  useEffect(() => {
    ref.current?.querySelector("mark.active")?.scrollIntoView({ block: "center" });
  }, [activeItemId]);

  function currentSelection(): Range | null {
    const sel = window.getSelection();
    if (!sel || sel.rangeCount === 0 || sel.isCollapsed) return null;
    const point = (node: Node | null, offset: number) => {
      if (!node || node.nodeType !== Node.TEXT_NODE) return null;
      const seg = node.parentElement?.closest<HTMLElement>("[data-seg-start]");
      if (!seg || !ref.current?.contains(seg)) return null;
      return { segmentStart: Number(seg.dataset.segStart), offset };
    };
    const a = point(sel.anchorNode, sel.anchorOffset);
    const b = point(sel.focusNode, sel.focusOffset);
    return a && b ? selectionToRange(a, b) : null;
  }

  return (
    <div className="stack">
      <pre ref={ref} className="notes" data-testid="notes">
        {segments.map((s) =>
          s.itemIds.length > 0 ? (
            <mark
              key={s.start}
              data-seg-start={s.start}
              className={activeItemId && s.itemIds.includes(activeItemId) ? "active" : undefined}
              onClick={() => onHighlightClick?.(s.itemIds[0])}
            >
              {s.text}
            </mark>
          ) : (
            <span key={s.start} data-seg-start={s.start}>
              {s.text}
            </span>
          ),
        )}
      </pre>
      {onSelectRange && (
        <div className="row">
          <button
            type="button"
            onMouseDown={(e) => e.preventDefault() /* keep the text selection */}
            onClick={() => {
              const range = currentSelection();
              if (!range) {
                setHint("Select the missed action item's text in the notes first.");
                return;
              }
              setHint(null);
              window.getSelection()?.removeAllRanges();
              onSelectRange(range);
            }}
          >
            Add selected text as item
          </button>
          {hint && <span className="muted">{hint}</span>}
        </div>
      )}
      <p className="muted">Highlighted text produced an item. Check the unhighlighted parts for anything missed.</p>
    </div>
  );
}
```

- [ ] **Step 6: Implement the review page, workspace and item row**

`src/app/meetings/[id]/review/page.tsx`:

```tsx
import { notFound, redirect } from "next/navigation";
import { z } from "zod";
import { requireUser } from "@/lib/auth/requireUser";
import { getDb } from "@/lib/db/client";
import { NotFoundError } from "@/lib/errors";
import { getMeetingWithItems } from "@/lib/meetings/service";
import { ReviewWorkspace } from "./ReviewWorkspace";

export default async function ReviewPage({ params }: { params: Promise<{ id: string }> }) {
  await requireUser();
  const { id } = await params;
  if (!z.string().uuid().safeParse(id).success) notFound();
  const data = await getMeetingWithItems(getDb(), id).catch((err) => {
    if (err instanceof NotFoundError) notFound();
    throw err;
  });
  if (data.meeting.status === "committed") redirect(`/meetings/${id}`);

  const { meeting } = data;
  return (
    <ReviewWorkspace
      meeting={{
        id: meeting.id,
        title: meeting.title,
        meetingDate: meeting.meetingDate,
        notesText: meeting.notesText,
        extractionState: meeting.extractionState,
        extractionError: meeting.extractionError,
      }}
      items={data.items.map((i) => ({
        id: i.id,
        text: i.text,
        ownerMemberId: i.ownerMemberId,
        ownerRaw: i.ownerRaw,
        ownerSuggestions: i.ownerSuggestions,
        dueDate: i.dueDate,
        dueRaw: i.dueRaw,
        sourceStart: i.sourceStart,
        sourceEnd: i.sourceEnd,
        flags: i.flags,
      }))}
      roster={data.roster}
    />
  );
}
```

`src/app/meetings/[id]/review/ReviewWorkspace.tsx`:

```tsx
"use client";

import { useRouter } from "next/navigation";
import { useMemo, useState, useTransition } from "react";
import { addManualItemAction, commitMeetingAction, retryExtractionAction } from "@/app/actions/review";
import { NotesPane } from "@/app/components/NotesPane";
import { isBlocking, type Flag, type RosterEntry } from "@/lib/types";
import { ItemRow, type ReviewItem } from "./ItemRow";

export function ReviewWorkspace(props: {
  meeting: {
    id: string;
    title: string;
    meetingDate: string;
    notesText: string;
    extractionState: "pending" | "done" | "failed";
    extractionError: string | null;
  };
  items: ReviewItem[];
  roster: RosterEntry[];
}) {
  const { meeting, items, roster } = props;
  const router = useRouter();
  const [activeItemId, setActiveItemId] = useState<string | null>(null);
  const [error, setError] = useState<string | null>(null);
  const [pending, startTransition] = useTransition();

  const ranges = useMemo(
    () =>
      items
        .filter((i) => i.sourceStart !== null && i.sourceEnd !== null)
        .map((i) => ({ id: i.id, start: i.sourceStart!, end: i.sourceEnd! })),
    [items],
  );
  const blockedCount = items.filter((i) => i.flags.some((f: Flag) => isBlocking(f))).length;
  const extractionOk = meeting.extractionState === "done";

  function run(action: () => Promise<{ ok: true } | { ok: false; error: string }>) {
    startTransition(async () => {
      const result = await action();
      setError(result.ok ? null : result.error);
      router.refresh();
    });
  }

  return (
    <div className="stack">
      <h1>Review: {meeting.title}</h1>
      <p className="muted">Meeting date {meeting.meetingDate}. Relative dates like “Friday” are worked out from this date.</p>

      {!extractionOk && (
        <div className="warning" role="alert">
          {meeting.extractionError ?? "Extraction didn't finish."} Your notes are saved.{" "}
          <button type="button" disabled={pending} onClick={() => run(() => retryExtractionAction(meeting.id))}>
            Retry extraction
          </button>
        </div>
      )}
      {error && (
        <p className="error" role="alert">
          {error}
        </p>
      )}

      <div className="review-grid">
        <NotesPane
          notes={meeting.notesText}
          ranges={ranges}
          activeItemId={activeItemId}
          onHighlightClick={setActiveItemId}
          onSelectRange={
            extractionOk ? (r) => run(() => addManualItemAction(meeting.id, r.start, r.end)) : undefined
          }
        />
        <div className="stack">
          {extractionOk && items.length === 0 && (
            <p>No action items found. Select text in the notes to add any that were missed, or add the meeting as is.</p>
          )}
          <ul className="items">
            {items.map((item) => (
              <ItemRow
                key={item.id}
                item={item}
                roster={roster}
                isActive={item.id === activeItemId}
                onFocus={() => setActiveItemId(item.id)}
                onChanged={() => router.refresh()}
              />
            ))}
          </ul>
          <div className="row">
            <button
              type="button"
              disabled={!extractionOk || blockedCount > 0 || pending}
              onClick={() => run(() => commitMeetingAction(meeting.id))}
            >
              Add to board
            </button>
            {blockedCount > 0 && (
              <span className="error">
                {blockedCount} {blockedCount === 1 ? "item needs" : "items need"} an owner
              </span>
            )}
          </div>
        </div>
      </div>
    </div>
  );
}
```

`src/app/meetings/[id]/review/ItemRow.tsx`:

```tsx
"use client";

import { useEffect, useState, useTransition } from "react";
import { deleteDraftItemAction, splitDraftItemAction, updateDraftItemAction } from "@/app/actions/review";
import { FlagBadges } from "@/app/components/FlagBadges";
import { isBlocking, type Flag, type RosterEntry } from "@/lib/types";

export interface ReviewItem {
  id: string;
  text: string;
  ownerMemberId: string | null;
  ownerRaw: string | null;
  ownerSuggestions: string[];
  dueDate: string | null;
  dueRaw: string | null;
  sourceStart: number | null;
  sourceEnd: number | null;
  flags: Flag[];
}

export function ItemRow(props: {
  item: ReviewItem;
  roster: RosterEntry[];
  isActive: boolean;
  onFocus: () => void;
  onChanged: () => void;
}) {
  const { item, roster, isActive, onFocus, onChanged } = props;
  const [text, setText] = useState(item.text);
  const [error, setError] = useState<string | null>(null);
  const [pending, startTransition] = useTransition();

  useEffect(() => setText(item.text), [item.text]);

  function run(action: () => Promise<{ ok: true } | { ok: false; error: string }>) {
    startTransition(async () => {
      const result = await action();
      setError(result.ok ? null : result.error);
      onChanged();
    });
  }

  const suggestions = item.ownerSuggestions
    .map((id) => roster.find((m) => m.id === id)?.displayName)
    .filter((n): n is string => Boolean(n));
  const blocked = item.flags.some(isBlocking);

  return (
    <li
      data-testid="item-row"
      data-item-text={item.text}
      className={[blocked ? "blocked" : "", isActive ? "active" : ""].join(" ").trim() || undefined}
      onFocus={onFocus}
    >
      <div className="stack">
        <input
          aria-label="Action item text"
          value={text}
          disabled={pending}
          onChange={(e) => setText(e.target.value)}
          onBlur={() => {
            if (text.trim() !== item.text) run(() => updateDraftItemAction(item.id, { text }));
          }}
        />
        <div className="row">
          <label>
            Owner{" "}
            <select
              aria-label="Owner"
              value={item.ownerMemberId ?? ""}
              disabled={pending}
              onChange={(e) => run(() => updateDraftItemAction(item.id, { ownerMemberId: e.target.value || null }))}
            >
              <option value="">Choose owner…</option>
              {roster.map((m) => (
                <option key={m.id} value={m.id}>
                  {m.displayName}
                </option>
              ))}
            </select>
          </label>
          {item.ownerRaw !== null && <span className="muted">Notes say: “{item.ownerRaw}”</span>}
          {!item.ownerMemberId && suggestions.length > 0 && (
            <span className="muted">Suggested: {suggestions.join(", ")}</span>
          )}
        </div>
        <div className="row">
          <label>
            Due{" "}
            <input
              type="date"
              aria-label="Due date"
              value={item.dueDate ?? ""}
              disabled={pending}
              onChange={(e) => run(() => updateDraftItemAction(item.id, { dueDate: e.target.value || null }))}
            />
          </label>
          {item.dueRaw && <span className="muted">Notes say: “{item.dueRaw}”</span>}
        </div>
        <div className="row">
          <FlagBadges flags={item.flags} />
        </div>
        <div className="row">
          {item.flags.includes("multiple_owners") && item.ownerSuggestions.length > 1 && (
            <button type="button" disabled={pending} onClick={() => run(() => splitDraftItemAction(item.id))}>
              Split into {item.ownerSuggestions.length} items
            </button>
          )}
          <button type="button" className="link" disabled={pending} onClick={() => run(() => deleteDraftItemAction(item.id))}>
            Delete
          </button>
        </div>
        {error && (
          <p className="error" role="alert">
            {error}
          </p>
        )}
      </div>
    </li>
  );
}
```

- [ ] **Step 7: Run the tests and confirm they pass**

Run: `npm run typecheck && npm run e2e -- review.spec.ts paste.spec.ts`
Expected: all PASS. The review E2E ends on `/board?meeting=…`, which returns 404 until Task 14. The test only checks the URL.

- [ ] **Step 8: Commit**

```bash
git add src/lib/notes/segments.ts src/lib/flagLabels.ts src/app/actions/review.ts src/app/components src/app/meetings tests/unit/notes/segments.test.ts tests/e2e/review.spec.ts
git commit -m "feat: review screen with flag resolution, split, add-from-selection and commit"
```

---

### Task 14: Board, item history and meeting notes view

**Files:**
- Create: `src/app/actions/board.ts`, `src/app/board/page.tsx`, `src/app/board/BoardTable.tsx`, `src/app/board/HistoryPanel.tsx`, `src/app/meetings/[id]/page.tsx`
- Test: `tests/e2e/board.spec.ts`

**Interfaces:**
- Consumes: items service and `describeEvent` (Task 9), `todayLocalIso`/`isOverdue`/`formatDue` (Task 9), `listDraftMeetings`/`getMeetingOrThrow`/`getMeetingWithItems` (Task 8), `getRoster` (Task 7), `NotesPane` (Task 13), `runAction` (Task 12).
- Produces:
  - `setDoneAction(itemId: string, done: boolean): Promise<ActionResult>`
  - `updateItemAction(itemId: string, patch: { text?: string; ownerMemberId?: string; dueDate?: string | null }): Promise<ActionResult>`
  - `getHistoryAction(itemId: string): Promise<Array<{ id: number; line: string; at: string }>>`
  - Board URL parameters: `?owner=<memberId>&meeting=<meetingId>&done=1`
  - Meeting notes view: `/meetings/<id>?item=<itemId>` (a committed meeting; a draft redirects to review)

- [ ] **Step 1: Write the failing test**

`tests/e2e/board.spec.ts`:

```ts
import { expect, test, type Page } from "@playwright/test";
import { pasteMeeting, uniqueTag } from "./helpers";

const boardRow = (page: Page, text: string) => page.locator(`[data-board-item="${text}"]`);

test("board shows committed items; owner changes and ticks are recorded", async ({ page }) => {
  const tag = uniqueTag();
  const ship = `Ship ${tag} release notes`;
  const roadmap = `Update ${tag} roadmap`;
  await pasteMeeting(page, `Board ${tag}`, [
    `- ACTION: ${ship} | owner: Tom | due: Friday`,
    `- ACTION: ${roadmap} | owner: Priya`,
  ]);
  await page.getByRole("button", { name: "Add to board" }).click();
  await expect(page).toHaveURL(/\/board\?meeting=/);

  await expect(boardRow(page, ship).getByLabel("Owner").locator("option:checked")).toHaveText("Tomás");
  await expect(boardRow(page, roadmap)).toContainText("No date");

  await boardRow(page, ship).getByLabel("Owner").selectOption({ label: "Ravi" });
  await expect(boardRow(page, ship).getByLabel("Owner").locator("option:checked")).toHaveText("Ravi");
  await boardRow(page, ship).getByRole("button", { name: "History" }).click();
  await expect(boardRow(page, ship).getByTestId("history")).toContainText("E2E Tester added this item");
  await expect(boardRow(page, ship).getByTestId("history")).toContainText("E2E Tester changed the owner from Tomás to Ravi");

  await boardRow(page, roadmap).getByRole("checkbox").check();
  await expect(boardRow(page, roadmap)).toHaveCount(0);

  await page.getByLabel("Show done (last 14 days)").check();
  await page.getByRole("button", { name: "Apply" }).click();
  await expect(boardRow(page, roadmap).getByRole("checkbox")).toBeChecked();
});

test("the notes link opens the meeting with the source highlighted", async ({ page }) => {
  const tag = uniqueTag();
  const text = `Email ${tag} vendor`;
  await pasteMeeting(page, `Notes view ${tag}`, [`Intro ${tag}`, `- ACTION: ${text} | owner: Dana`]);
  await page.getByRole("button", { name: "Add to board" }).click();
  await boardRow(page, text).getByRole("link", { name: /Notes view/ }).click();
  await expect(page).toHaveURL(/\/meetings\/[0-9a-f-]+\?item=/);
  await expect(page.locator("mark.active")).toContainText(`ACTION: ${text}`);
});
```

- [ ] **Step 2: Run it and confirm it fails**

Run: `npm run e2e -- board.spec.ts`
Expected: FAIL. `/board` returns 404.

- [ ] **Step 3: Implement the board actions**

`src/app/actions/board.ts`:

```ts
"use server";

import { z } from "zod";
import { requireUser } from "@/lib/auth/requireUser";
import { getDb } from "@/lib/db/client";
import { describeEvent } from "@/lib/items/describeEvent";
import { getItemHistory, setDone, updateItem } from "@/lib/items/service";
import { runAction, type ActionResult } from "./result";

const Id = z.string().uuid();
const BoardPatch = z.object({
  text: z.string().optional(),
  ownerMemberId: z.string().uuid().optional(),
  dueDate: z.string().nullable().optional(),
});

export async function setDoneAction(itemId: string, done: boolean): Promise<ActionResult> {
  const user = await requireUser();
  return runAction(() => setDone(getDb(), Id.parse(itemId), user.id, z.boolean().parse(done)));
}

export async function updateItemAction(itemId: string, patch: z.input<typeof BoardPatch>): Promise<ActionResult> {
  const user = await requireUser();
  return runAction(() => updateItem(getDb(), Id.parse(itemId), user.id, BoardPatch.parse(patch)));
}

export async function getHistoryAction(itemId: string): Promise<Array<{ id: number; line: string; at: string }>> {
  await requireUser();
  const events = await getItemHistory(getDb(), Id.parse(itemId));
  return events.map((e) => ({ id: e.id, line: `${e.actorName} ${describeEvent(e)}`, at: e.at.toISOString() }));
}
```

- [ ] **Step 4: Implement the board page and components**

`src/app/board/page.tsx`:

```tsx
import Link from "next/link";
import { z } from "zod";
import { requireUser } from "@/lib/auth/requireUser";
import { getDb } from "@/lib/db/client";
import { listBoard } from "@/lib/items/service";
import { getMeetingOrThrow, listDraftMeetings } from "@/lib/meetings/service";
import { getRoster } from "@/lib/roster/repository";
import { BoardTable } from "./BoardTable";

const uuidOrUndefined = (v: unknown) => (z.string().uuid().safeParse(v).success ? (v as string) : undefined);

export default async function BoardPage({
  searchParams,
}: {
  searchParams: Promise<{ owner?: string; meeting?: string; done?: string }>;
}) {
  await requireUser();
  const sp = await searchParams;
  const ownerId = uuidOrUndefined(sp.owner);
  const meetingId = uuidOrUndefined(sp.meeting);
  const showDone = sp.done === "1";
  const db = getDb();

  const [rows, roster, drafts, meeting] = await Promise.all([
    listBoard(db, {
      ownerId,
      meetingId,
      includeDoneSince: showDone ? new Date(Date.now() - 14 * 86_400_000) : undefined,
    }),
    getRoster(db),
    listDraftMeetings(db),
    meetingId ? getMeetingOrThrow(db, meetingId).catch(() => null) : Promise.resolve(null),
  ]);

  return (
    <div className="stack">
      <h1>Action items</h1>

      {drafts.length > 0 && (
        <div className="warning">
          Unfinished reviews:{" "}
          {drafts.map((d, i) => (
            <span key={d.id}>
              {i > 0 && ", "}
              <Link href={`/meetings/${d.id}/review`}>{d.title}</Link> ({d.meetingDate})
            </span>
          ))}
        </div>
      )}

      <form method="get" className="row">
        <label>
          Owner{" "}
          <select name="owner" defaultValue={ownerId ?? ""}>
            <option value="">Everyone</option>
            {roster.map((m) => (
              <option key={m.id} value={m.id}>
                {m.displayName}
              </option>
            ))}
          </select>
        </label>
        <label>
          <input type="checkbox" name="done" value="1" defaultChecked={showDone} /> Show done (last 14 days)
        </label>
        {meetingId && <input type="hidden" name="meeting" value={meetingId} />}
        <button type="submit">Apply</button>
        {meeting && (
          <span className="muted">
            Showing items from “{meeting.title}” · <Link href="/board">show all meetings</Link>
          </span>
        )}
      </form>

      {rows.length === 0 ? <p>No open action items.</p> : <BoardTable rows={rows} roster={roster} />}
    </div>
  );
}
```

`src/app/board/BoardTable.tsx`:

```tsx
"use client";

import Link from "next/link";
import { useRouter } from "next/navigation";
import { useEffect, useState, useTransition } from "react";
import { setDoneAction, updateItemAction } from "@/app/actions/board";
import { formatDue, isOverdue, todayLocalIso } from "@/lib/dates/display";
import type { BoardRow } from "@/lib/items/service";
import type { RosterEntry } from "@/lib/types";
import { HistoryPanel } from "./HistoryPanel";

export function BoardTable({ rows, roster }: { rows: BoardRow[]; roster: RosterEntry[] }) {
  const [today, setToday] = useState("");
  useEffect(() => setToday(todayLocalIso()), []);
  return (
    <table className="board">
      <thead>
        <tr>
          <th>Done</th>
          <th>Action item</th>
          <th>Owner</th>
          <th>Due</th>
          <th>Meeting</th>
          <th />
        </tr>
      </thead>
      <tbody>
        {rows.map((row) => (
          <BoardItemRow key={row.id} row={row} roster={roster} today={today} />
        ))}
      </tbody>
    </table>
  );
}

function BoardItemRow({ row, roster, today }: { row: BoardRow; roster: RosterEntry[]; today: string }) {
  const router = useRouter();
  const [text, setText] = useState(row.text);
  const [error, setError] = useState<string | null>(null);
  const [pending, startTransition] = useTransition();
  useEffect(() => setText(row.text), [row.text]);

  function run(action: () => Promise<{ ok: true } | { ok: false; error: string }>) {
    startTransition(async () => {
      const result = await action();
      setError(result.ok ? null : result.error);
      router.refresh();
    });
  }

  const overdue = row.status === "open" && today !== "" && isOverdue(row.dueDate, today);

  return (
    <tr data-board-item={row.text}>
      <td>
        <input
          type="checkbox"
          aria-label={`Mark “${row.text}” done`}
          checked={row.status === "done"}
          disabled={pending}
          onChange={(e) => run(() => setDoneAction(row.id, e.target.checked))}
        />
      </td>
      <td>
        <input
          aria-label="Action item text"
          value={text}
          disabled={pending}
          onChange={(e) => setText(e.target.value)}
          onBlur={() => {
            if (text.trim() !== row.text) run(() => updateItemAction(row.id, { text }));
          }}
        />
        {error && (
          <p className="error" role="alert">
            {error}
          </p>
        )}
      </td>
      <td>
        <select
          aria-label="Owner"
          value={row.ownerMemberId}
          disabled={pending}
          onChange={(e) => run(() => updateItemAction(row.id, { ownerMemberId: e.target.value }))}
        >
          {roster.map((m) => (
            <option key={m.id} value={m.id}>
              {m.displayName}
            </option>
          ))}
        </select>
      </td>
      <td>
        <div className={overdue ? "overdue" : undefined}>{formatDue(row.dueDate)}</div>
        <input
          type="date"
          aria-label="Due date"
          value={row.dueDate ?? ""}
          disabled={pending}
          onChange={(e) => run(() => updateItemAction(row.id, { dueDate: e.target.value || null }))}
        />
      </td>
      <td>
        <Link href={`/meetings/${row.meetingId}?item=${row.id}`}>{row.meetingTitle}</Link>
        <div className="muted">{row.meetingDate}</div>
      </td>
      <td>
        <HistoryPanel itemId={row.id} />
      </td>
    </tr>
  );
}
```

`src/app/board/HistoryPanel.tsx`:

```tsx
"use client";

import { useState, useTransition } from "react";
import { getHistoryAction } from "@/app/actions/board";

export function HistoryPanel({ itemId }: { itemId: string }) {
  const [entries, setEntries] = useState<Array<{ id: number; line: string; at: string }> | null>(null);
  const [pending, startTransition] = useTransition();

  function toggle() {
    if (entries) {
      setEntries(null);
      return;
    }
    startTransition(async () => setEntries(await getHistoryAction(itemId)));
  }

  return (
    <div>
      <button type="button" className="link" onClick={toggle} disabled={pending}>
        History
      </button>
      {entries && (
        <ul data-testid="history" className="muted">
          {entries.map((e) => (
            <li key={e.id}>
              {e.line} · {new Date(e.at).toLocaleString()}
            </li>
          ))}
        </ul>
      )}
    </div>
  );
}
```

`src/app/meetings/[id]/page.tsx`:

```tsx
import Link from "next/link";
import { notFound, redirect } from "next/navigation";
import { z } from "zod";
import { NotesPane } from "@/app/components/NotesPane";
import { requireUser } from "@/lib/auth/requireUser";
import { getDb } from "@/lib/db/client";
import { NotFoundError } from "@/lib/errors";
import { getMeetingWithItems } from "@/lib/meetings/service";

export default async function MeetingNotesPage({
  params,
  searchParams,
}: {
  params: Promise<{ id: string }>;
  searchParams: Promise<{ item?: string }>;
}) {
  await requireUser();
  const { id } = await params;
  const { item } = await searchParams;
  if (!z.string().uuid().safeParse(id).success) notFound();
  const data = await getMeetingWithItems(getDb(), id).catch((err) => {
    if (err instanceof NotFoundError) notFound();
    throw err;
  });
  if (data.meeting.status === "draft") redirect(`/meetings/${id}/review`);

  const ranges = data.items
    .filter((i) => i.sourceStart !== null && i.sourceEnd !== null)
    .map((i) => ({ id: i.id, start: i.sourceStart!, end: i.sourceEnd! }));

  return (
    <div className="stack">
      <h1>{data.meeting.title}</h1>
      <p className="muted">
        Meeting date {data.meeting.meetingDate} · <Link href={`/board?meeting=${id}`}>this meeting's items on the board</Link>
      </p>
      <NotesPane notes={data.meeting.notesText} ranges={ranges} activeItemId={item ?? null} />
    </div>
  );
}
```

- [ ] **Step 5: Run the tests and confirm they pass**

Run: `npm run typecheck && npm run e2e`
Expected: all E2E specs PASS (paste, review, board).

- [ ] **Step 6: Commit**

```bash
git add src/app/actions/board.ts src/app/board src/app/meetings/[id]/page.tsx tests/e2e/board.spec.ts
git commit -m "feat: shared board with inline edits, done/reopen, history and notes view"
```

---

### Task 15: Team page (alias editing)

**Files:**
- Create: `src/app/actions/team.ts`, `src/app/team/page.tsx`, `src/app/team/TeamEditor.tsx`
- Test: `tests/e2e/team.spec.ts`

**Interfaces:**
- Consumes: `updateAliases` (Task 10), `getRoster` (Task 7), `requireUser` (Task 11), E2E helpers (Task 12).
- Produces: `updateAliasesAction(memberId: string, aliasesText: string): Promise<{ ok: true; aliases: string[] } | { ok: false; error: string }>`. `aliasesText` is comma-separated.

- [ ] **Step 1: Write the failing test**

`tests/e2e/team.spec.ts`:

```ts
import { expect, test } from "@playwright/test";
import { pasteMeeting, uniqueTag } from "./helpers";

test("aliases: clashes are rejected, and a saved alias resolves future owners", async ({ page }) => {
  await page.goto("/team");
  const ravi = page.locator('[data-member="Ravi"]');

  await ravi.getByLabel("Aliases for Ravi").fill("tom");
  await ravi.getByRole("button", { name: "Save" }).click();
  await expect(ravi.getByRole("alert")).toHaveText("“tom” is already used by Tomás");

  await ravi.getByLabel("Aliases for Ravi").fill("RJ");
  await ravi.getByRole("button", { name: "Save" }).click();
  await expect(ravi.getByText("Saved")).toBeVisible();

  const tag = uniqueTag();
  await pasteMeeting(page, `Alias ${tag}`, [`- ACTION: Draft ${tag} memo | owner: RJ`]);
  const row = page.locator(`[data-item-text="Draft ${tag} memo"]`);
  await expect(row.getByLabel("Owner").locator("option:checked")).toHaveText("Ravi");
  await expect(row.locator("[data-flag]")).toHaveCount(0);
});
```

- [ ] **Step 2: Run it and confirm it fails**

Run: `npm run e2e -- team.spec.ts`
Expected: FAIL. `/team` returns 404.

- [ ] **Step 3: Implement**

`src/app/actions/team.ts`:

```ts
"use server";

import { revalidatePath } from "next/cache";
import { z } from "zod";
import { requireUser } from "@/lib/auth/requireUser";
import { getDb } from "@/lib/db/client";
import { NotFoundError } from "@/lib/errors";
import { updateAliases } from "@/lib/roster/service";

export async function updateAliasesAction(
  memberId: string,
  aliasesText: string,
): Promise<{ ok: true; aliases: string[] } | { ok: false; error: string }> {
  const user = await requireUser();
  const id = z.string().uuid().parse(memberId);
  const raw = z.string().max(1000).parse(aliasesText).split(",");
  try {
    const result = await updateAliases(getDb(), id, user.id, raw);
    if (result.ok) revalidatePath("/team");
    return result;
  } catch (err) {
    if (err instanceof NotFoundError) return { ok: false, error: err.message };
    throw err;
  }
}
```

`src/app/team/page.tsx`:

```tsx
import { requireUser } from "@/lib/auth/requireUser";
import { getDb } from "@/lib/db/client";
import { getRoster } from "@/lib/roster/repository";
import { TeamEditor } from "./TeamEditor";

export default async function TeamPage() {
  await requireUser();
  const roster = await getRoster(getDb());
  return (
    <div className="stack">
      <h1>Team</h1>
      <p className="muted">
        An owner in the notes is matched only if it's exactly a name or alias below (ignoring case and accents).
        Anything else is flagged for review. Alias changes affect future extractions only.
      </p>
      <ul className="items">
        {roster.map((m) => (
          <TeamEditor key={m.id} member={m} />
        ))}
      </ul>
    </div>
  );
}
```

`src/app/team/TeamEditor.tsx`:

```tsx
"use client";

import { useState, useTransition } from "react";
import { updateAliasesAction } from "@/app/actions/team";
import type { RosterEntry } from "@/lib/types";

export function TeamEditor({ member }: { member: RosterEntry }) {
  const [value, setValue] = useState(member.aliases.join(", "));
  const [status, setStatus] = useState<{ kind: "saved" } | { kind: "error"; message: string } | null>(null);
  const [pending, startTransition] = useTransition();

  function save() {
    startTransition(async () => {
      const result = await updateAliasesAction(member.id, value);
      if (result.ok) {
        setValue(result.aliases.join(", "));
        setStatus({ kind: "saved" });
      } else {
        setStatus({ kind: "error", message: result.error });
      }
    });
  }

  return (
    <li data-member={member.displayName} className="row">
      <strong style={{ minWidth: "6rem" }}>{member.displayName}</strong>
      <input
        aria-label={`Aliases for ${member.displayName}`}
        placeholder="e.g. tom, tommy"
        value={value}
        onChange={(e) => {
          setValue(e.target.value);
          setStatus(null);
        }}
      />
      <button type="button" onClick={save} disabled={pending}>
        Save
      </button>
      {status?.kind === "saved" && <span className="muted">Saved</span>}
      {status?.kind === "error" && (
        <span className="error" role="alert">
          {status.message}
        </span>
      )}
    </li>
  );
}
```

- [ ] **Step 4: Run the tests and confirm they pass**

Run: `npm run typecheck && npm run e2e`
Expected: all E2E specs PASS.

- [ ] **Step 5: Commit**

```bash
git add src/app/actions/team.ts src/app/team tests/e2e/team.spec.ts
git commit -m "feat: team page for editing roster aliases"
```

---

### Task 16: Extraction eval harness, README and launch checklist

**Files:**
- Create: `eval/score.ts`, `eval/run-eval.ts`, `eval/golden/README.md`, `eval/golden/synthetic-01.json`, `eval/golden/synthetic-02.json`, `README.md`
- Test: `tests/unit/eval/score.test.ts`

**Interfaces:**
- Consumes: `resolveOwner` (Task 2), `ExtractedItem` (Task 5), `createClaudeExtractorFromEnv` (Task 5), `RosterEntry` (Task 1), `config/roster.json`.
- Produces:
  - `interface ExpectedItem { match: string; owner: string | null }`. `match` is a case-insensitive phrase the extracted text must contain. `owner` is the roster display name, or `null` if the item must end up flagged.
  - `interface GoldenCase { name: string; meetingDate: string; notes: string; expected: ExpectedItem[] }`
  - `interface CaseScore { name: string; expectedCount: number; found: number; missed: string[]; extraCount: number; ownerCorrect: number; wrongOwner: Array<{ match: string; expected: string | null; got: string }>; flaggedInstead: string[] }`
  - `scoreCase(c: GoldenCase, extracted: ExtractedItem[], roster: RosterEntry[]): CaseScore`
  - `rosterFromConfig(entries: Array<{ displayName: string; aliases: string[] }>): RosterEntry[]` (ids are the display names)

`wrongOwner` counts an item assigned to the wrong person: the failure the spec rules out. `flaggedInstead` counts items that were flagged when an owner was expected. That's safe, but it costs the reviewer a click.

- [ ] **Step 1: Write the failing test**

`tests/unit/eval/score.test.ts`:

```ts
import { describe, expect, it } from "vitest";
import roster from "../../../config/roster.json";
import { rosterFromConfig, scoreCase, type GoldenCase } from "../../../eval/score";

const R = rosterFromConfig(roster);
const golden: GoldenCase = {
  name: "demo",
  meetingDate: "2026-09-30",
  notes: "irrelevant for scoring",
  expected: [
    { match: "deck", owner: "Tomás" },
    { match: "venue", owner: "Dana" },
    { match: "contract", owner: null },
    { match: "faq", owner: "Lena" },
  ],
};
const item = (text: string, owner: string | null) => ({ text, owner_mention: owner, due_mention: null, source_quote: text });

describe("scoreCase", () => {
  it("reports missed items, extras, wrong owners and flagged-instead", () => {
    const score = scoreCase(
      golden,
      [item("Send the deck", "Tom"), item("Book venue", "Ravi"), item("Check contract", "legal"), item("Order lunch", "Aisha"), item("Draft FAQ", "Lena K.")],
      R,
    );
    expect(score).toEqual({
      name: "demo",
      expectedCount: 4,
      found: 4,
      missed: [],
      extraCount: 1,
      ownerCorrect: 2,
      wrongOwner: [{ match: "venue", expected: "Dana", got: "Ravi" }],
      flaggedInstead: ["faq"],
    });
  });

  it("lists items that were not extracted", () => {
    const score = scoreCase(golden, [item("Send the deck", "Tom")], R);
    expect(score.found).toBe(1);
    expect(score.missed).toEqual(["venue", "contract", "faq"]);
  });
});
```

- [ ] **Step 2: Run it and confirm it fails**

Run: `npm test -- tests/unit/eval`
Expected: FAIL. `eval/score.ts` doesn't exist yet.

- [ ] **Step 3: Implement scoring and the runner**

`eval/score.ts`:

```ts
import type { ExtractedItem } from "../src/lib/extraction/schema";
import { resolveOwner } from "../src/lib/roster/resolveOwner";
import type { RosterEntry } from "../src/lib/types";

export interface ExpectedItem {
  match: string;
  owner: string | null;
}

export interface GoldenCase {
  name: string;
  meetingDate: string;
  notes: string;
  expected: ExpectedItem[];
}

export interface CaseScore {
  name: string;
  expectedCount: number;
  found: number;
  missed: string[];
  extraCount: number;
  ownerCorrect: number;
  wrongOwner: Array<{ match: string; expected: string | null; got: string }>;
  flaggedInstead: string[];
}

export function rosterFromConfig(entries: Array<{ displayName: string; aliases: string[] }>): RosterEntry[] {
  return entries.map((e) => ({ id: e.displayName, displayName: e.displayName, aliases: e.aliases }));
}

export function scoreCase(c: GoldenCase, extracted: ExtractedItem[], roster: RosterEntry[]): CaseScore {
  const used = new Set<number>();
  const missed: string[] = [];
  const wrongOwner: CaseScore["wrongOwner"] = [];
  const flaggedInstead: string[] = [];
  let ownerCorrect = 0;

  for (const exp of c.expected) {
    const idx = extracted.findIndex((it, i) => !used.has(i) && it.text.toLowerCase().includes(exp.match.toLowerCase()));
    if (idx === -1) {
      missed.push(exp.match);
      continue;
    }
    used.add(idx);
    const res = resolveOwner(extracted[idx].owner_mention, roster);
    const got = res.kind === "assigned" ? roster.find((m) => m.id === res.memberId)!.displayName : null;
    if (got === exp.owner) ownerCorrect++;
    else if (got === null) flaggedInstead.push(exp.match);
    else wrongOwner.push({ match: exp.match, expected: exp.owner, got });
  }

  return {
    name: c.name,
    expectedCount: c.expected.length,
    found: c.expected.length - missed.length,
    missed,
    extraCount: extracted.length - used.size,
    ownerCorrect,
    wrongOwner,
    flaggedInstead,
  };
}
```

`eval/run-eval.ts`:

```ts
import { readFileSync, readdirSync } from "node:fs";
import path from "node:path";
import roster from "../config/roster.json";
import { createClaudeExtractorFromEnv } from "../src/lib/extraction/claudeExtractor";
import { rosterFromConfig, scoreCase, type GoldenCase } from "./score";

// Calls the real Claude API once per golden file. Costs money; run on demand, not in CI.
async function main() {
  const dir = path.resolve("eval/golden");
  const files = readdirSync(dir).filter((f) => f.endsWith(".json")).sort();
  const extractor = createClaudeExtractorFromEnv();
  const r = rosterFromConfig(roster);
  let failed = false;

  for (const file of files) {
    const c = JSON.parse(readFileSync(path.join(dir, file), "utf8")) as GoldenCase;
    const s = scoreCase(c, await extractor.extract(c.notes), r);
    console.log(
      `${s.name}: found ${s.found}/${s.expectedCount}, extra ${s.extraCount}, owner correct ${s.ownerCorrect}, ` +
        `flagged instead ${s.flaggedInstead.length}, WRONG owner ${s.wrongOwner.length}`,
    );
    if (s.missed.length) console.log(`  missed: ${s.missed.join("; ")}`);
    if (s.wrongOwner.length) console.log(`  wrong owner: ${JSON.stringify(s.wrongOwner)}`);
    if (s.flaggedInstead.length) console.log(`  flagged instead: ${s.flaggedInstead.join("; ")}`);
    if (s.missed.length > 0 || s.wrongOwner.length > 0) failed = true;
  }

  console.log(failed ? "\nFAIL: some items were missed or assigned to the wrong person." : "\nPASS");
  process.exit(failed ? 1 : 0);
}

main().catch((err) => {
  console.error(err instanceof Error ? err.message : err);
  process.exit(1);
});
```

`eval/golden/synthetic-01.json`:

```json
{
  "name": "synthetic-01 weekly sync with recap",
  "meetingDate": "2026-09-30",
  "notes": "Weekly product sync\n\nAttendees: Priya, Tom, Dana, Ravi\n\n- Launch is still on track for Oct 14.\n- Tom will send the launch deck to legal by Friday.\n- Pricing page: Priya and Dana to review copy before EOW.\n- We decided to drop the beta banner.\n- Ravi to book the venue for the offsite.\n- Someone from legal should check the vendor contract.\n\nAction items:\n- Tom: launch deck to legal (Fri)\n- Ravi: venue\n",
  "expected": [
    { "match": "deck", "owner": "Tomás" },
    { "match": "pricing", "owner": null },
    { "match": "venue", "owner": "Ravi" },
    { "match": "contract", "owner": null }
  ]
}
```

`eval/golden/synthetic-02.json`:

```json
{
  "name": "synthetic-02 nicknames, no owners, no actions mixed in",
  "meetingDate": "2026-10-05",
  "notes": "Eng standup 5 Oct\r\n\r\nPK: finish the auth migration by Wednesday.\r\nMarcus is out next week.\r\nAisha will write the incident postmortem.\r\nNeed to update the on-call rota (no owner yet).\r\nLena mentioned the FAQ is outdated — she’ll draft a new one by 10/9.\r\nSarah shared the Q3 metrics; no follow-ups.\r\n",
  "expected": [
    { "match": "auth migration", "owner": "Priya" },
    { "match": "postmortem", "owner": "Aisha" },
    { "match": "on-call", "owner": null },
    { "match": "faq", "owner": "Lena" }
  ]
}
```

`eval/golden/README.md`:

````markdown
# Golden meeting notes

Each `*.json` file is one meeting:

```json
{
  "name": "short description",
  "meetingDate": "YYYY-MM-DD",
  "notes": "the pasted notes, verbatim",
  "expected": [{ "match": "a phrase the item text must contain", "owner": "Roster display name, or null if it must be flagged" }]
}
```

The two `synthetic-*` files only prove the harness works. **Before launch**, add 5–10 anonymized real meeting notes
from the team, with every action item listed under `expected`. Then run `npm run eval` (this calls the Claude API
and costs money). Launch requires no missed items and no wrong-person owners across the set. If the model misses
something, fix the prompt in `src/lib/extraction/prompt.ts` and keep the failing case here.
````

- [ ] **Step 4: Run the unit tests and confirm they pass**

Run: `npm test -- tests/unit/eval`
Expected: 2 PASS.

- [ ] **Step 5: Write the README**

`README.md`:

````markdown
# Meeting Action Items

Paste meeting notes, review the extracted action items (owner, due date), and track them on one shared board.
Design: `docs/superpowers/specs/2026-09-26-meeting-action-items-design.md`.

## Local development

```bash
cp .env.example .env.local        # set EXTRACTOR=fake to work without the Claude API
docker compose up -d postgres
npm install
npm run db:migrate && npm run db:seed
npm run dev
```

With real sign-in, you need Google OAuth credentials (see below). For a quick local look without them, add
`AUTH_TEST_BYPASS=1` to `.env.local`. It is refused when `NODE_ENV=production`.

## Tests

- `npm test`: unit and integration tests (PGlite in-process; no Docker needed)
- `npm run e2e`: Playwright against `next dev` with the fake extractor and a test user (needs `docker compose up -d postgres`)
- `npm run eval`: extraction quality against `eval/golden` using the **real** Claude API (costs money)

## Deploying

Any Node 20.9+ host plus managed Postgres 16 with encryption at rest, served over HTTPS.

1. Set the env vars from `.env.example`. **Do not** set `EXTRACTOR` or `AUTH_TEST_BYPASS`.
2. Run `npm run build`, then `DATABASE_URL=… npx tsx scripts/migrate.ts` and `npx tsx scripts/seed.ts` once. Then run `npm start`.

## Launch checklist

- [ ] Replace the `ALLOWED_DOMAIN` placeholder `ourcompany.com` with the real Google Workspace domain.
- [ ] In Google Cloud Console, create an OAuth client (web). Set the consent screen to **Internal** (Workspace only) and add the redirect URI `https://<host>/api/auth/callback/google`.
- [ ] Generate `AUTH_SECRET` with `npx auth secret`.
- [ ] Add 5–10 anonymized real meeting notes to `eval/golden/`, then run `npm run eval`. It must PASS (no missed items and no wrong owners).
- [ ] Check the roster aliases on the Team page (e.g. nicknames the team actually uses).
- [ ] Sign in with a personal Gmail account and confirm you land on "Access restricted".
````

- [ ] **Step 6: Full verification**

Run: `npm test && npm run typecheck && npm run build && npm run e2e`
Expected: every unit, integration and E2E test PASSES, and the build succeeds.

- [ ] **Step 7: Commit**

```bash
git add eval README.md tests/unit/eval
git commit -m "feat: extraction eval harness, README and launch checklist"
```

---

## Spec coverage map

| Spec section | Task(s) |
|---|---|
| §1 success criteria (completeness, correct owner, no retyping) | 5 (prompt biased to recall), 6, 13 (coverage highlights, add-from-selection), 16 (eval) |
| §2 architecture, config | 1, 5, 7, 11 |
| §3 units | 2–9 |
| §4 data model, constraint, audit rules | 7, 8, 9, 10 |
| §5.1 extraction | 5 |
| §5.2 owner resolution, aliases, split | 2, 8, 10, 13, 15 |
| §5.3 due dates | 3 |
| §5.4 quote location | 4 |
| §5.5 blocking/warning flags, possible_duplicate | 1, 6, 8, 13 |
| §6.1 sign-in | 11 |
| §6.2 paste, duplicate warning | 8, 12 |
| §6.3 review | 13 |
| §6.4 board, history, notes link | 9, 14 |
| §6.5 team | 10, 15 |
| §7 error handling | 5, 8, 12, 13 |
| §8 security | 11 (domain check, bypass guard), 5/8 (no notes in logs) |
| §9 testing strategy | every task; E2E in 12–15; eval in 16 |

