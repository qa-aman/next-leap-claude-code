"use client";
import { Button } from "@/components/ui/Button";

export function EmailBodyEditor({
  subject,
  body,
  onSubjectChange,
  onBodyChange,
  onRegenerate,
}: {
  subject: string;
  body: string;
  onSubjectChange: (s: string) => void;
  onBodyChange: (s: string) => void;
  onRegenerate: () => void;
}) {
  const wordCount = body.trim().split(/\s+/).filter(Boolean).length;
  return (
    <div className="space-y-3">
      <div className="space-y-1.5">
        <label className="block text-2xs font-semibold uppercase tracking-[0.16em] text-fg-subtle">
          Subject
        </label>
        <input
          value={subject}
          onChange={(e) => onSubjectChange(e.target.value)}
          className="w-full rounded-xl border border-border-subtle surface-elevated px-3.5 py-2.5 text-[14px] font-medium text-fg shadow-soft outline-none transition-colors placeholder:text-fg-subtle focus:border-accent/50"
        />
      </div>
      <div className="space-y-1.5">
        <div className="flex items-center justify-between">
          <label className="block text-2xs font-semibold uppercase tracking-[0.16em] text-fg-subtle">
            Body · AI-drafted
          </label>
          <div className="flex items-center gap-2">
            <span className="font-mono text-2xs tracking-wider text-fg-subtle nums">{wordCount} words</span>
            <Button size="sm" variant="ghost" onClick={onRegenerate}>
              <span className="mr-0.5">↻</span> Regenerate
            </Button>
          </div>
        </div>
        <div className="relative overflow-hidden rounded-xl border border-border-subtle surface-elevated shadow-soft transition-colors focus-within:border-accent/50">
          <span className="pointer-events-none absolute inset-y-3 left-0 w-[2px] rounded-r bg-gradient-to-b from-accent/60 to-accent/10" />
          <textarea
            value={body}
            onChange={(e) => onBodyChange(e.target.value)}
            rows={14}
            className="w-full resize-none bg-transparent px-4 py-3.5 font-sans text-[13.5px] leading-[1.7] text-fg outline-none scrollbar-thin"
          />
        </div>
      </div>
    </div>
  );
}
