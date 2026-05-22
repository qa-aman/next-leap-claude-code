import { Avatar } from "@/components/ui/Avatar";
import type { Participant } from "@/lib/mock-data";

export function ParticipantTalkTimeRow({ participant }: { participant: Participant }) {
  const pct = participant.talkTimePct ?? 0;
  return (
    <div className="flex items-center gap-3 py-2.5">
      <Avatar initials={participant.initials} size={30} />
      <div className="min-w-0 flex-1">
        <div className="flex items-center justify-between">
          <span className="truncate text-[13px] font-medium text-fg">{participant.name}</span>
          <div className="flex items-center gap-2.5 text-xs text-fg-muted">
            <span className="font-mono nums text-fg-subtle">{participant.wpm} wpm</span>
            <span className="font-mono nums w-9 text-right text-fg">{pct}%</span>
          </div>
        </div>
        <div className="relative mt-2 h-1.5 w-full overflow-hidden rounded-full bg-bg-inset ring-1 ring-inset ring-border-subtle">
          <div
            className="h-full rounded-full bg-gradient-to-r from-accent/80 to-accent shadow-[0_0_8px_rgba(139,109,255,0.4)] transition-[width] duration-700 ease-out"
            style={{ width: `${pct}%` }}
          />
        </div>
      </div>
    </div>
  );
}
