"use client";
import { cn } from "@/lib/cn";
import type { ActionFilter } from "@/lib/store";

const filters: { value: ActionFilter; label: string }[] = [
  { value: "all", label: "All" },
  { value: "high", label: "High confidence" },
  { value: "needs-review", label: "Needs review" },
];

export function FilterChips({
  value,
  onChange,
  counts,
}: {
  value: ActionFilter;
  onChange: (v: ActionFilter) => void;
  counts: Record<ActionFilter, number>;
}) {
  return (
    <div className="inline-flex items-center gap-0.5 rounded-lg border border-border-subtle bg-bg-elevated p-1 shadow-soft">
      {filters.map((f) => {
        const active = value === f.value;
        return (
          <button
            key={f.value}
            onClick={() => onChange(f.value)}
            className={cn(
              "relative flex items-center gap-1.5 rounded-md px-2.5 py-1.5 text-xs font-medium transition-all",
              active
                ? "bg-bg-subtle text-fg shadow-soft"
                : "text-fg-muted hover:bg-bg-subtle/60 hover:text-fg"
            )}
          >
            {f.label}
            <span
              className={cn(
                "rounded px-1 font-mono text-[10px] tabular-nums",
                active ? "bg-accent-subtle text-accent" : "bg-bg-inset text-fg-subtle"
              )}
            >
              {counts[f.value]}
            </span>
          </button>
        );
      })}
    </div>
  );
}
