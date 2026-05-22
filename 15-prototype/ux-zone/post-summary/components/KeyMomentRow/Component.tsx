"use client";
import type { KeyMoment } from "@/lib/mock-data";

export function KeyMomentRow({ moment }: { moment: KeyMoment }) {
  return (
    <button className="group flex w-full items-center gap-3 rounded-lg border border-transparent px-3 py-2.5 text-left transition-all hover:border-border-subtle hover:bg-bg-inset focus-visible:border-accent/60 focus-visible:bg-bg-inset">
      <span className="grid h-8 w-14 shrink-0 place-items-center rounded-md border border-border-subtle bg-bg-inset font-mono text-[12px] font-semibold tabular-nums text-fg-muted shadow-soft transition-colors group-hover:border-accent/40 group-hover:text-accent">
        {moment.timestamp}
      </span>
      <span className="flex-1 text-[13px] leading-relaxed text-fg group-hover:text-fg">{moment.title}</span>
      <span className="font-mono text-fg-subtle transition-all group-hover:translate-x-0.5 group-hover:text-accent">›</span>
    </button>
  );
}
