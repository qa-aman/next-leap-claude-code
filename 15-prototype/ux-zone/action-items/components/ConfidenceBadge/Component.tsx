import { cn } from "@/lib/cn";
import type { Confidence } from "@/lib/mock-data";

const config: Record<Confidence, { label: string; classes: string; dot: string; bar: string }> = {
  high: {
    label: "High",
    classes: "bg-success-subtle text-success border-success/30",
    dot: "bg-success shadow-[0_0_6px_rgba(63,185,80,0.6)]",
    bar: "bg-success",
  },
  medium: {
    label: "Medium",
    classes: "bg-warning-subtle text-warning border-warning/30",
    dot: "bg-warning shadow-[0_0_6px_rgba(227,179,65,0.6)]",
    bar: "bg-warning",
  },
  low: {
    label: "Low",
    classes: "bg-danger-subtle text-danger border-danger/30",
    dot: "bg-danger shadow-[0_0_6px_rgba(248,81,73,0.6)]",
    bar: "bg-danger",
  },
};

export function ConfidenceBadge({
  confidence,
  pct,
  showPct = true,
}: {
  confidence: Confidence;
  pct: number;
  showPct?: boolean;
}) {
  const c = config[confidence];
  const segments = 5;
  const filled = Math.round((pct / 100) * segments);
  return (
    <span
      className={cn(
        "inline-flex items-center gap-1.5 rounded-md border px-1.5 py-0.5 text-[10.5px] font-medium tracking-wide",
        c.classes
      )}
      title={`${c.label} confidence: ${pct}%`}
    >
      <span className={cn("h-1.5 w-1.5 rounded-full", c.dot)} />
      <span>{c.label}</span>
      {showPct && (
        <span className="flex items-center gap-1">
          <span className="font-mono nums opacity-90">{pct}%</span>
          <span className="flex items-center gap-[2px]">
            {Array.from({ length: segments }).map((_, i) => (
              <span
                key={i}
                className={cn(
                  "h-2 w-[2px] rounded-sm",
                  i < filled ? c.bar : "bg-current opacity-20"
                )}
              />
            ))}
          </span>
        </span>
      )}
    </span>
  );
}
