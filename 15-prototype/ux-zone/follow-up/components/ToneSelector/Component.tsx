"use client";
import { cn } from "@/lib/cn";
import type { Tone } from "@/lib/store";

const tones: { value: Tone; label: string; hint: string; icon: string }[] = [
  { value: "concise", label: "Concise", hint: "Bullets, minimum words", icon: "≡" },
  { value: "warm", label: "Warm", hint: "Friendly, conversational", icon: "*" },
  { value: "direct", label: "Direct", hint: "Sharp, owner + date first", icon: "→" },
];

export function ToneSelector({ value, onChange }: { value: Tone; onChange: (t: Tone) => void }) {
  return (
    <div className="space-y-1.5">
      <label className="block text-2xs font-semibold uppercase tracking-[0.16em] text-fg-subtle">
        Tone
      </label>
      <div className="grid grid-cols-3 gap-2">
        {tones.map((t) => {
          const active = value === t.value;
          return (
            <button
              key={t.value}
              onClick={() => onChange(t.value)}
              className={cn(
                "group relative overflow-hidden rounded-xl border px-3.5 py-3 text-left transition-all lift",
                active
                  ? "border-accent/50 surface-accent shadow-glow-accent"
                  : "border-border-subtle surface-elevated hover:border-border-strong"
              )}
            >
              {active && (
                <span className="pointer-events-none absolute -top-8 left-1/2 h-16 w-32 -translate-x-1/2 rounded-full bg-accent/20 blur-2xl" />
              )}
              <div className="relative flex items-start justify-between gap-2">
                <div>
                  <div className={cn(
                    "text-[13.5px] font-semibold tracking-tight transition-colors",
                    active ? "text-fg" : "text-fg"
                  )}>
                    {t.label}
                  </div>
                  <div className="mt-0.5 text-[11.5px] text-fg-muted">{t.hint}</div>
                </div>
                <span className={cn(
                  "font-mono text-sm transition-colors",
                  active ? "text-accent" : "text-fg-subtle group-hover:text-fg-muted"
                )}>
                  {t.icon}
                </span>
              </div>
            </button>
          );
        })}
      </div>
    </div>
  );
}
