"use client";
import { useState } from "react";
import { meetings } from "@/lib/mock-data";
import { useRouter } from "next/navigation";
import { MeetingCard } from "@/ux-zone/pre-meeting/components/MeetingCard/Component";
import { AgendaPreviewPanel } from "@/ux-zone/pre-meeting/components/AgendaPreviewPanel/Component";

export default function PreMeetingPage() {
  const [expandedId, setExpandedId] = useState<string | null>(meetings[0].id);
  const router = useRouter();

  const grouped = groupByLabel(meetings);

  return (
    <div className="space-y-10">
      <header className="space-y-3">
        <div className="flex items-center gap-2 text-2xs uppercase tracking-[0.18em] text-fg-subtle">
          <span className="h-1 w-1 rounded-full bg-accent animate-pulse-dot" />
          <span className="font-mono">17-03-2026 · Workshop</span>
        </div>
        <div className="flex items-end justify-between gap-6">
          <div>
            <h1 className="text-[28px] font-semibold tracking-tight text-fg">Meetings</h1>
            <p className="mt-1.5 max-w-xl text-sm text-fg-muted">
              {meetings.length} upcoming today and this week. MeetFlow joins automatically when a meeting starts.
            </p>
          </div>
          <div className="hidden items-center gap-2 md:flex">
            <Stat label="Today" value={grouped.find((g) => g.label === "Today")?.items.length ?? 0} />
            <Stat label="This week" value={meetings.length} accent />
          </div>
        </div>
        <div className="divide-fade" />
      </header>

      {grouped.map(({ label, items }, idx) => (
        <section key={label} className="space-y-3 animate-slide-up" style={{ animationDelay: `${idx * 60}ms` }}>
          <div className="flex items-baseline gap-3">
            <h2 className="text-2xs font-semibold uppercase tracking-[0.18em] text-fg-subtle">{label}</h2>
            <span className="font-mono text-2xs text-fg-subtle">{items.length}</span>
            <div className="ml-2 h-px flex-1 bg-border-subtle" />
          </div>
          <div className="space-y-2">
            {items.map((m, i) => {
              const expanded = expandedId === m.id;
              return (
                <div key={m.id} className="animate-fade-in" style={{ animationDelay: `${i * 40}ms` }}>
                  <MeetingCard
                    meeting={m}
                    expanded={expanded}
                    onToggle={() => setExpandedId(expanded ? null : m.id)}
                    onJoin={() => router.push("/live")}
                  />
                  {expanded && (
                    <div className="-mt-1 rounded-b-xl border border-t-0 border-border-subtle surface-elevated overflow-hidden">
                      <AgendaPreviewPanel meeting={m} />
                    </div>
                  )}
                </div>
              );
            })}
          </div>
        </section>
      ))}
    </div>
  );
}

function Stat({ label, value, accent }: { label: string; value: number; accent?: boolean }) {
  return (
    <div className="flex items-center gap-2 rounded-md border border-border-subtle bg-bg-elevated px-2.5 py-1.5 shadow-soft">
      <span className="text-2xs uppercase tracking-wider text-fg-subtle">{label}</span>
      <span className={`font-mono text-sm font-semibold nums ${accent ? "text-accent" : "text-fg"}`}>{value}</span>
    </div>
  );
}

function groupByLabel(items: typeof meetings) {
  const today = "17-03-2026";
  const tomorrow = "18-03-2026";
  const groups = [
    { label: "Today", items: items.filter((m) => m.date === today) },
    { label: "Tomorrow", items: items.filter((m) => m.date === tomorrow) },
    { label: "Later this week", items: items.filter((m) => m.date !== today && m.date !== tomorrow) },
  ];
  return groups.filter((g) => g.items.length > 0);
}
