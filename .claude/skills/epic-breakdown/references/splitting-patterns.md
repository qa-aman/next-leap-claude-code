# Splitting Patterns — Detailed Examples

## 1. Workflow Steps

Split by sequential steps in the user journey.

**Example — Content Creation:**
- SE-001: Create Item (select type, enter content)
- SE-002: Add Media (images, audio)
- SE-003: Set Rules (scoring, validation)
- SE-004: Preview & Validate
- SE-005: Publish

**Use when:** Feature has a clear multi-step flow. **Avoid when:** Steps are tightly coupled.

## 2. Business Rules

Split by individual business rules or validations.

**Example — Reward Earning:**
- SE-001: Core earning (complete task -> earn reward)
- SE-002: Inventory cap (max rewards held)
- SE-003: Expiry logic (time-based expiry)
- SE-004: Usage limits (per-period caps)

**Use when:** Complex validation logic. **Avoid when:** Rules are simple and interdependent.

## 3. Data Variations

Split by different data types or input formats.

**Example — Content Import:**
- SE-001: Import from CSV
- SE-002: Import from Excel
- SE-003: Import from JSON/API

**Use when:** Multiple input formats. **Avoid when:** Formats share 90%+ logic.

## 4. Platform Differences

Split by platform.

**Example — Offline Sync:**
- SE-001: Web (online-only baseline)
- SE-002: Tablet (offline with local storage)
- SE-003: Mobile (reduced UI, offline-capable)

**Use when:** Feature works differently across platforms. **Avoid when:** Differences are only CSS.

## 5. Operations (CRUD)

Split by Create, Read, Update, Delete.

**Example — Dashboard:**
- SE-001: View data (Read)
- SE-002: Create custom groups (Create)
- SE-003: Update assignments (Update)
- SE-004: Archive old items (Delete/soft-delete)

**Use when:** Standard data management. **Avoid when:** Feature is single operation.

## 6. Spike/Research

Separate unknowns into research spikes.

**Example — Third-Party Integration:**
- SE-001: Spike — evaluate providers (2 points)
- SE-002: Spike — prototype latency test (2 points)
- SE-003: Build — integrate selected provider (5 points)

**Use when:** Technical unknowns exist. **Avoid when:** Technology is well-understood.

## 7. Performance

Separate performance optimization from functionality.

**Example — Dashboard Loading:**
- SE-001: Build with basic queries (functional)
- SE-002: Add caching layer for sub-200ms load (performance)
- SE-003: Add lazy loading for large datasets (performance)

**Use when:** Feature has specific NFR targets. **Avoid when:** Performance is adequate.

## 8. Persona Variations

Split by user role.

**Example — Notifications:**
- SE-001: End-user notifications (actions, reminders)
- SE-002: Manager notifications (reports, alerts)
- SE-003: Admin notifications (system analytics)

**Use when:** Different personas have different needs. **Avoid when:** All share same experience.

## 9. Happy Path vs Edge Cases

Ship happy path first, then edge/error/empty.

**Example — Feature Activation:**
- SE-001: Happy path — activate online, resources available (3 points)
- SE-002: Edge — offline activation with sync (5 points)
- SE-003: Edge — usage limit handling (2 points)
- SE-004: Error — activation failure recovery (3 points)
- SE-005: Empty — no resources available state (1 point)

**Use when:** Feature can deliver value with just happy path. **Avoid when:** Edge cases are the core value.
