import { cn } from "@/lib/cn";

type Tone = "neutral" | "success" | "warning" | "danger" | "accent";

export function Badge({
  children,
  tone = "neutral",
  className,
}: {
  children: React.ReactNode;
  tone?: Tone;
  className?: string;
}) {
  const tones: Record<Tone, string> = {
    neutral: "bg-bg-subtle text-fg-muted border-border ring-1 ring-inset ring-white/[0.02]",
    success: "bg-success-subtle text-success border-success/30",
    warning: "bg-warning-subtle text-warning border-warning/30",
    danger: "bg-danger-subtle text-danger border-danger/30",
    accent: "bg-accent-subtle text-accent border-accent/30",
  };
  return (
    <span
      className={cn(
        "inline-flex items-center gap-1 rounded-md border px-1.5 py-0.5 text-[10.5px] font-medium tracking-wide",
        tones[tone],
        className
      )}
    >
      {children}
    </span>
  );
}
