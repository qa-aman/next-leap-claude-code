"use client";
import { Avatar } from "@/components/ui/Avatar";
import { Badge } from "@/components/ui/Badge";
import { Button } from "@/components/ui/Button";
import { cn } from "@/lib/cn";
import type { ActionItem } from "@/lib/mock-data";
import { ConfidenceBadge } from "../ConfidenceBadge/Component";

export function ActionItemRow({
  item,
  onConfirm,
  onReject,
}: {
  item: ActionItem;
  onConfirm: (id: string) => void;
  onReject: (id: string) => void;
}) {
  const borderTone =
    item.state === "needs-review"
      ? "border-warning/30 hover:border-warning/50"
      : item.state === "confirmed"
      ? "border-success/20 hover:border-success/40"
      : "border-border-subtle hover:border-border-strong";

  const railTone =
    item.confidence === "high"
      ? "bg-gradient-to-b from-success to-success/30"
      : item.confidence === "medium"
      ? "bg-gradient-to-b from-warning to-warning/30"
      : "bg-gradient-to-b from-danger to-danger/30";

  return (
    <div
      className={cn(
        "group relative grid grid-cols-[1fr_auto] items-center gap-4 rounded-xl border surface-elevated px-5 py-4 lift shadow-soft",
        borderTone
      )}
    >
      <span className={cn("absolute inset-y-3 left-0 w-[2px] rounded-r", railTone)} />
      <div className="min-w-0 space-y-2 pl-1.5">
        <div className="flex flex-wrap items-center gap-2">
          <ConfidenceBadge confidence={item.confidence} pct={item.confidencePct} />
          {item.state === "needs-review" && <Badge tone="warning">Needs review</Badge>}
          {item.state === "confirmed" && <Badge tone="success">Confirmed</Badge>}
        </div>
        <p className="text-[14px] leading-relaxed text-fg text-pretty">{item.title}</p>
        <div className="flex flex-wrap items-center gap-x-3 gap-y-1 text-xs text-fg-muted">
          <span className="flex items-center gap-1.5">
            <Avatar initials={initials(item.assigneeName)} size={16} />
            <span className="text-fg">{item.assigneeName}</span>
          </span>
          <span className="text-fg-subtle">·</span>
          <span className="flex items-center gap-1 font-mono nums text-fg-muted">
            <span className="text-fg-subtle">due</span>
            {item.dueDate}
          </span>
          <span className="text-fg-subtle">·</span>
          <span className="truncate text-fg-subtle">from {item.sourceMeetingTitle}</span>
        </div>
      </div>
      <div className="flex items-center gap-2">
        {item.state === "needs-review" && (
          <>
            <Button size="sm" variant="ghost" onClick={() => onReject(item.id)}>
              Reject
            </Button>
            <Button size="sm" variant="primary" onClick={() => onConfirm(item.id)}>
              Confirm
            </Button>
          </>
        )}
        {item.state === "confirmed" && (
          <Button size="sm" variant="ghost">
            Edit
          </Button>
        )}
      </div>
    </div>
  );
}

function initials(name: string) {
  return name
    .split(" ")
    .map((n) => n[0])
    .join("")
    .slice(0, 2)
    .toUpperCase();
}
