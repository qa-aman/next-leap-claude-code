import { Card, CardBody, CardHeader, CardTitle } from "@/components/ui/Card";

export function TldrCard({ tldr, durationMin, decisionsCount, actionsCount }: { tldr: string; durationMin: number; decisionsCount: number; actionsCount: number }) {
  return (
    <Card accent className="overflow-hidden">
      <CardHeader>
        <CardTitle className="flex items-center gap-2">
          <span className="relative grid h-6 w-6 place-items-center rounded-md bg-accent-subtle text-accent ring-1 ring-inset ring-accent/30">
            <SparkleIcon />
            <span className="absolute inset-0 rounded-md bg-accent/10 blur-md" />
          </span>
          <span className="text-gradient-accent">Quick recap</span>
        </CardTitle>
        <span className="font-mono text-2xs uppercase tracking-wider text-fg-subtle">AI summary</span>
      </CardHeader>
      <CardBody className="space-y-4 px-5 py-5">
        <p className="text-[15px] leading-[1.7] text-fg text-pretty">{tldr}</p>
        <div className="grid grid-cols-3 gap-3 border-t border-border-subtle pt-4">
          <Stat label="Duration" value={`${durationMin}m`} />
          <Stat label="Decisions" value={String(decisionsCount)} tone="accent" />
          <Stat label="Actions" value={String(actionsCount)} tone="success" />
        </div>
      </CardBody>
    </Card>
  );
}

function Stat({ label, value, tone = "neutral" }: { label: string; value: string; tone?: "neutral" | "accent" | "success" }) {
  const toneClass =
    tone === "accent" ? "text-accent" : tone === "success" ? "text-success" : "text-fg";
  return (
    <div className="space-y-1">
      <div className="text-2xs uppercase tracking-[0.16em] text-fg-subtle">{label}</div>
      <div className={`font-mono text-[22px] font-semibold tracking-tight nums ${toneClass}`}>{value}</div>
    </div>
  );
}

function SparkleIcon() {
  return (
    <svg width="13" height="13" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
      <path d="M9.937 15.5A2 2 0 0 0 8.5 14.063l-6.135-1.582a.5.5 0 0 1 0-.962L8.5 9.936A2 2 0 0 0 9.937 8.5l1.582-6.135a.5.5 0 0 1 .963 0L14.063 8.5A2 2 0 0 0 15.5 9.937l6.135 1.581a.5.5 0 0 1 0 .964L15.5 14.063a2 2 0 0 0-1.437 1.437l-1.582 6.135a.5.5 0 0 1-.963 0z" />
    </svg>
  );
}
