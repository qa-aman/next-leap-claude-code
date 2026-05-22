"use client";
import { useEffect, useRef, useState } from "react";
import { Avatar } from "@/components/ui/Avatar";
import type { TranscriptLine } from "@/lib/mock-data";

const initialsFor = (name: string) =>
  name.split(" ").map((n) => n[0]).join("").slice(0, 2).toUpperCase();

export function TranscriptStream({ lines }: { lines: TranscriptLine[] }) {
  const [revealed, setRevealed] = useState(2);
  const scrollerRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    if (revealed >= lines.length) return;
    const t = setTimeout(() => setRevealed((r) => r + 1), 2200);
    return () => clearTimeout(t);
  }, [revealed, lines.length]);

  useEffect(() => {
    scrollerRef.current?.scrollTo({ top: scrollerRef.current.scrollHeight, behavior: "smooth" });
  }, [revealed]);

  return (
    <div
      ref={scrollerRef}
      className="relative h-[520px] overflow-y-auto scrollbar-thin px-1 pr-2"
    >
      {/* Top fade */}
      <div className="pointer-events-none sticky top-0 z-10 -mb-6 h-6 bg-gradient-to-b from-bg-elevated to-transparent" />
      <div className="relative space-y-5 pb-6">
        {/* Vertical timeline rail */}
        <span className="pointer-events-none absolute left-[13px] top-2 bottom-2 w-px bg-gradient-to-b from-transparent via-border to-transparent" />
        {lines.slice(0, revealed).map((line, i) => (
          <div
            key={line.id}
            className="relative flex gap-3 animate-fade-in"
            style={{ animationDelay: `${Math.min(i, 4) * 60}ms` }}
          >
            <Avatar initials={initialsFor(line.speakerName)} size={28} className="relative z-10 mt-0.5 shrink-0" />
            <div className="min-w-0 flex-1">
              <div className="flex items-baseline gap-2">
                <span className="text-[13px] font-semibold tracking-tight text-fg">{line.speakerName}</span>
                <span className="font-mono text-[11px] text-fg-subtle nums">{line.timestamp}</span>
              </div>
              <p className="mt-1 text-[13.5px] leading-[1.65] text-fg-muted text-pretty">{line.text}</p>
            </div>
          </div>
        ))}
        {revealed < lines.length && (
          <div className="relative flex items-center gap-2 pl-10 text-xs text-fg-subtle">
            <span className="flex gap-1">
              <span className="h-1.5 w-1.5 animate-pulse-dot rounded-full bg-accent" />
              <span className="h-1.5 w-1.5 animate-pulse-dot rounded-full bg-accent" style={{ animationDelay: "200ms" }} />
              <span className="h-1.5 w-1.5 animate-pulse-dot rounded-full bg-accent" style={{ animationDelay: "400ms" }} />
            </span>
            <span className="font-mono uppercase tracking-wider text-2xs">Listening</span>
          </div>
        )}
      </div>
      {/* Bottom fade */}
      <div className="pointer-events-none sticky bottom-0 -mt-6 h-6 bg-gradient-to-t from-bg-elevated to-transparent" />
    </div>
  );
}
