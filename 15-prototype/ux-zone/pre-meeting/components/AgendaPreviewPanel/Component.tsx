"use client";
import { Avatar } from "@/components/ui/Avatar";
import type { Meeting } from "@/lib/mock-data";

export function AgendaPreviewPanel({ meeting }: { meeting: Meeting }) {
  return (
    <div className="border-t border-border-subtle bg-bg-inset bg-dots px-5 py-5 animate-fade-in">
      <div className="grid gap-8 md:grid-cols-[1fr_240px]">
        <div>
          <h4 className="mb-3 flex items-center gap-2 text-2xs font-semibold uppercase tracking-[0.16em] text-fg-subtle">
            <span className="h-px w-4 bg-fg-subtle" /> Agenda
          </h4>
          <ol className="space-y-2.5">
            {meeting.agenda.map((item, i) => (
              <li key={i} className="flex items-start gap-3 text-[13px] leading-relaxed text-fg">
                <span className="mt-0.5 grid h-5 w-5 shrink-0 place-items-center rounded border border-border-subtle bg-bg-elevated font-mono text-[10px] text-fg-muted">
                  {i + 1}
                </span>
                <span>{item}</span>
              </li>
            ))}
          </ol>
        </div>
        <div>
          <h4 className="mb-3 flex items-center gap-2 text-2xs font-semibold uppercase tracking-[0.16em] text-fg-subtle">
            <span className="h-px w-4 bg-fg-subtle" /> Attendees
          </h4>
          <ul className="space-y-2">
            {meeting.participants.map((p) => (
              <li key={p.id} className="flex items-center gap-2.5 text-[13px] text-fg">
                <Avatar initials={p.initials} size={22} />
                <span className="truncate">{p.name}</span>
              </li>
            ))}
          </ul>
        </div>
      </div>
    </div>
  );
}
