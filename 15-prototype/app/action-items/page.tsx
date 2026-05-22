"use client";
import { useMemo, useState } from "react";
import { actionItems as seedItems, type ActionItem } from "@/lib/mock-data";
import { useStore } from "@/lib/store";
import { ActionItemRow } from "@/ux-zone/action-items/components/ActionItemRow/Component";
import { FilterChips } from "@/ux-zone/action-items/components/FilterChips/Component";

export default function ActionItemsPage() {
  const { actionFilter, setActionFilter } = useStore();
  const [items, setItems] = useState<ActionItem[]>(seedItems);

  const counts = useMemo(
    () => ({
      all: items.length,
      high: items.filter((i) => i.confidence === "high").length,
      "needs-review": items.filter((i) => i.state === "needs-review").length,
    }),
    [items]
  );

  const filtered = useMemo(() => {
    if (actionFilter === "all") return items;
    if (actionFilter === "high") return items.filter((i) => i.confidence === "high");
    return items.filter((i) => i.state === "needs-review");
  }, [items, actionFilter]);

  const handleConfirm = (id: string) =>
    setItems((arr) => arr.map((i) => (i.id === id ? { ...i, state: "confirmed" } : i)));
  const handleReject = (id: string) => setItems((arr) => arr.filter((i) => i.id !== id));

  return (
    <div className="space-y-6">
      <header className="space-y-3 animate-slide-up">
        <div className="flex items-center gap-2 text-2xs uppercase tracking-[0.18em] text-fg-subtle">
          <span className="rounded border border-warning/30 bg-warning-subtle px-1.5 py-0.5 font-mono text-warning">In sprint</span>
          <span className="font-mono">17-03-2026 → 28-03-2026</span>
          <span>·</span>
          <span>Confidence Scoring v2</span>
        </div>
        <div className="flex items-end justify-between gap-4">
          <div>
            <h1 className="text-[28px] font-semibold tracking-tight text-fg">Action items</h1>
            <p className="mt-1.5 max-w-xl text-sm text-fg-muted">
              AI extracted these from your meetings. Anything below medium confidence needs your review before it ships to assignees.
            </p>
          </div>
          <FilterChips value={actionFilter} onChange={setActionFilter} counts={counts} />
        </div>
        <div className="divide-fade" />
      </header>

      {filtered.length === 0 ? (
        <div className="grid place-items-center rounded-xl border border-dashed border-border bg-bg-inset bg-dots px-6 py-20 text-center">
          <div className="space-y-2">
            <div className="mx-auto grid h-10 w-10 place-items-center rounded-full border border-border-subtle bg-bg-elevated text-success">
              <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2.5" strokeLinecap="round" strokeLinejoin="round"><polyline points="20 6 9 17 4 12" /></svg>
            </div>
            <p className="text-sm font-medium text-fg">All caught up.</p>
            <p className="text-xs text-fg-muted">Nothing in this filter needs your attention right now.</p>
          </div>
        </div>
      ) : (
        <div className="space-y-2">
          {filtered.map((i, idx) => (
            <div key={i.id} className="animate-fade-in" style={{ animationDelay: `${idx * 30}ms` }}>
              <ActionItemRow item={i} onConfirm={handleConfirm} onReject={handleReject} />
            </div>
          ))}
        </div>
      )}
    </div>
  );
}
