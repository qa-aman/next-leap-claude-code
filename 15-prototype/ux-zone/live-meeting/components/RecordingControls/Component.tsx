"use client";
import { useEffect, useState } from "react";
import { Button } from "@/components/ui/Button";

export function RecordingControls({ onEnd }: { onEnd: () => void }) {
  const [elapsed, setElapsed] = useState(154); // start at 02:34 for demo realism
  const [muted, setMuted] = useState(true);

  useEffect(() => {
    const id = setInterval(() => setElapsed((e) => e + 1), 1000);
    return () => clearInterval(id);
  }, []);

  const mm = String(Math.floor(elapsed / 60)).padStart(2, "0");
  const ss = String(elapsed % 60).padStart(2, "0");

  return (
    <div className="relative flex items-center justify-between overflow-hidden rounded-xl border border-border-subtle surface-elevated px-4 py-3 shadow-soft">
      <span className="pointer-events-none absolute inset-y-0 left-0 w-px bg-gradient-to-b from-transparent via-danger/60 to-transparent" />
      <div className="flex items-center gap-3">
        <span className="inline-flex items-center gap-2 rounded-md border border-danger/30 bg-danger-subtle px-2 py-1 text-xs font-medium text-danger">
          <span className="relative flex h-1.5 w-1.5">
            <span className="absolute inset-0 rounded-full bg-danger animate-ping-ring" />
            <span className="relative h-1.5 w-1.5 rounded-full bg-danger" />
          </span>
          Recording
        </span>
        <span className="font-mono text-[15px] font-semibold tabular-nums tracking-tight text-fg">{mm}:{ss}</span>
        {/* Mini audio waveform */}
        <span className="ml-1 flex items-end gap-0.5">
          {[3, 6, 4, 8, 5, 7, 4].map((h, i) => (
            <span
              key={i}
              className="w-0.5 rounded-full bg-accent/70"
              style={{
                height: `${h * 2}px`,
                animation: `pulse-dot 1.${(i % 5) + 1}s ease-in-out ${i * 80}ms infinite`,
              }}
            />
          ))}
        </span>
      </div>
      <div className="flex items-center gap-1.5">
        <Button size="sm" variant={muted ? "danger" : "secondary"} onClick={() => setMuted(!muted)}>
          {muted ? "Unmute" : "Mute"}
        </Button>
        <Button size="sm" variant="secondary">Share screen</Button>
        <Button size="sm" variant="secondary">Participants · 3</Button>
        <Button size="sm" variant="danger" onClick={onEnd}>End meeting</Button>
      </div>
    </div>
  );
}
