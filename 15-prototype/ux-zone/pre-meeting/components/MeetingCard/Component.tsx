"use client";
import { Avatar } from "@/components/ui/Avatar";
import { Badge } from "@/components/ui/Badge";
import { Button } from "@/components/ui/Button";
import { cn } from "@/lib/cn";
import type { Meeting } from "@/lib/mock-data";

export function MeetingCard({
  meeting,
  expanded,
  onToggle,
  onJoin,
}: {
  meeting: Meeting;
  expanded: boolean;
  onToggle: () => void;
  onJoin: () => void;
}) {
  return (
    <div
      className={cn(
        "group relative rounded-xl border lift",
        expanded
          ? "border-accent/40 surface-accent shadow-glow-accent"
          : "border-border-subtle surface-elevated hover:border-border-strong"
      )}
    >
      {/* Left accent bar on hover/expand */}
      <span
        className={cn(
          "absolute inset-y-3 left-0 w-[2px] rounded-full transition-all duration-300",
          expanded ? "bg-accent shadow-glow-accent" : "bg-transparent group-hover:bg-accent/40"
        )}
      />
      <button
        onClick={onToggle}
        className="flex w-full items-center justify-between gap-4 px-4 py-3.5 text-left"
      >
        <div className="flex min-w-0 flex-1 items-center gap-4">
          <div className="grid w-[68px] shrink-0 place-items-center rounded-lg border border-border-subtle bg-bg-inset px-2 py-2 shadow-soft">
            <span className="font-mono text-[15px] font-semibold tracking-tight text-fg nums">{meeting.startTime}</span>
            <span className="mt-0.5 font-mono text-[10px] uppercase tracking-wider text-fg-subtle">{meeting.durationMin}min</span>
          </div>
          <div className="min-w-0 flex-1">
            <div className="flex items-center gap-2">
              <h3 className="truncate text-[14px] font-semibold tracking-tight text-fg">{meeting.title}</h3>
              {meeting.recordingOn && (
                <Badge tone="accent" className="gap-1.5">
                  <span className="relative flex h-1.5 w-1.5">
                    <span className="absolute inset-0 rounded-full bg-accent animate-ping-ring" />
                    <span className="relative h-1.5 w-1.5 rounded-full bg-accent" />
                  </span>
                  Recording on
                </Badge>
              )}
            </div>
            <div className="mt-1.5 flex items-center gap-2.5 text-xs text-fg-muted">
              <span className="font-mono nums">{meeting.date}</span>
              <span className="text-fg-subtle">·</span>
              <div className="flex -space-x-1.5">
                {meeting.participants.slice(0, 4).map((p) => (
                  <Avatar key={p.id} initials={p.initials} size={18} className="ring-2 ring-bg-elevated" />
                ))}
              </div>
              <span>{meeting.participants.length} attendees</span>
            </div>
          </div>
        </div>
        <div className="flex items-center gap-2">
          <span className={cn(
            "hidden text-fg-subtle transition-transform sm:inline",
            expanded ? "rotate-90 text-fg-muted" : "group-hover:text-fg-muted"
          )}>›</span>
          <Button
            variant={expanded ? "primary" : "secondary"}
            size="sm"
            onClick={(e) => {
              e.stopPropagation();
              onJoin();
            }}
          >
            Join with MeetFlow
          </Button>
        </div>
      </button>
    </div>
  );
}
