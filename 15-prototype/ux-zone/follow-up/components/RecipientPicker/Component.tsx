"use client";
import { useState } from "react";
import { Avatar } from "@/components/ui/Avatar";
import { cn } from "@/lib/cn";

export function RecipientPicker({
  available,
  selected,
  onToggle,
}: {
  available: { name: string; initials: string }[];
  selected: string[];
  onToggle: (name: string) => void;
}) {
  const [open, setOpen] = useState(false);
  const unselected = available.filter((a) => !selected.includes(a.name));

  return (
    <div className="space-y-1.5">
      <label className="block text-2xs font-semibold uppercase tracking-[0.16em] text-fg-subtle">
        To
      </label>
      <div className="flex flex-wrap items-center gap-1.5 rounded-xl border border-border-subtle surface-elevated px-2 py-2 shadow-soft transition-colors focus-within:border-accent/40">
        {selected.map((name) => {
          const p = available.find((a) => a.name === name);
          if (!p) return null;
          return (
            <button
              key={name}
              onClick={() => onToggle(name)}
              className="group inline-flex items-center gap-1.5 rounded-md border border-accent/30 bg-accent-subtle px-2 py-1 text-xs text-fg transition-all hover:border-accent/60 hover:bg-accent/15"
            >
              <Avatar initials={p.initials} size={16} />
              <span>{name}</span>
              <span className="text-fg-muted transition-colors group-hover:text-danger">×</span>
            </button>
          );
        })}
        <div className="relative">
          <button
            onClick={() => setOpen(!open)}
            className="rounded-md border border-dashed border-border px-2 py-1 text-xs text-fg-muted transition-colors hover:border-fg-subtle hover:bg-bg-subtle hover:text-fg"
          >
            + Add
          </button>
          {open && unselected.length > 0 && (
            <div className="absolute left-0 top-full z-20 mt-1.5 w-60 rounded-xl border border-border bg-bg-elevated p-1 shadow-pop animate-slide-up">
              {unselected.map((p) => (
                <button
                  key={p.name}
                  onClick={() => {
                    onToggle(p.name);
                    setOpen(false);
                  }}
                  className={cn(
                    "flex w-full items-center gap-2.5 rounded-md px-2 py-1.5 text-left text-sm text-fg",
                    "hover:bg-bg-subtle"
                  )}
                >
                  <Avatar initials={p.initials} size={22} />
                  <span>{p.name}</span>
                </button>
              ))}
            </div>
          )}
        </div>
      </div>
    </div>
  );
}
