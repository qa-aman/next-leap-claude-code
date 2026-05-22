"use client";
import { useEffect, useState } from "react";

export function AiNotesPanel({ notes }: { notes: string[] }) {
  const [revealed, setRevealed] = useState(1);

  useEffect(() => {
    if (revealed >= notes.length) return;
    const t = setTimeout(() => setRevealed((r) => r + 1), 3500);
    return () => clearTimeout(t);
  }, [revealed, notes.length]);

  return (
    <div className="flex h-full flex-col">
      <div className="flex items-center justify-between border-b border-border-subtle pb-3">
        <div className="flex items-center gap-2">
          <span className="relative grid h-6 w-6 place-items-center rounded-md bg-accent-subtle text-accent ring-1 ring-inset ring-accent/30">
            <SparkleIcon />
            <span className="absolute inset-0 rounded-md bg-accent/10 blur-md" />
          </span>
          <span className="text-[13px] font-semibold tracking-tight text-gradient-accent">AI Notes</span>
        </div>
        <span className="rounded border border-accent/20 bg-accent-subtle px-1.5 py-0.5 font-mono text-[10px] uppercase tracking-wider text-accent/80">
          Live · {revealed}/{notes.length}
        </span>
      </div>
      <div className="mt-3 space-y-2 overflow-y-auto scrollbar-thin pr-1">
        {notes.slice(0, revealed).map((n, i) => (
          <div
            key={i}
            className="group relative rounded-lg border border-border-subtle bg-bg-inset px-3 py-2.5 text-[13px] leading-relaxed text-fg shadow-soft animate-slide-up"
            style={{ animationDelay: `${i * 60}ms` }}
          >
            <span className="absolute left-0 top-3 bottom-3 w-[2px] rounded-r bg-gradient-to-b from-accent to-accent/40" />
            <span className="pl-1.5 block text-pretty">{n}</span>
          </div>
        ))}
        {revealed < notes.length && (
          <div className="rounded-lg border border-dashed border-border bg-transparent px-3 py-2.5 text-xs text-fg-subtle">
            <span className="bg-shimmer bg-clip-text text-transparent animate-shimmer">AI is listening for the next note...</span>
          </div>
        )}
      </div>
      <div className="mt-3 border-t border-border-subtle pt-3">
        <button className="flex min-h-[36px] w-full items-center justify-between rounded-md border border-border bg-bg-subtle px-3 py-2 text-xs text-fg transition-colors hover:border-border-strong hover:bg-bg-elevated">
          <span>+ Add note manually</span>
          <kbd className="rounded border border-border bg-bg-inset px-1.5 py-0.5 font-mono text-[10px] text-fg-muted">⌘N</kbd>
        </button>
      </div>
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
