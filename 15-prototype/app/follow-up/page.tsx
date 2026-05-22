"use client";
import { useState } from "react";
import { useStore } from "@/lib/store";
import { participants, followUpDrafts, liveMeeting, actionItems } from "@/lib/mock-data";
import { Button } from "@/components/ui/Button";
import { Card, CardBody, CardHeader, CardTitle } from "@/components/ui/Card";
import { Badge } from "@/components/ui/Badge";
import { RecipientPicker } from "@/ux-zone/follow-up/components/RecipientPicker/Component";
import { ToneSelector } from "@/ux-zone/follow-up/components/ToneSelector/Component";
import { EmailBodyEditor } from "@/ux-zone/follow-up/components/EmailBodyEditor/Component";

export default function FollowUpPage() {
  const {
    tone,
    setTone,
    draftSubject,
    draftBody,
    setDraftSubject,
    setDraftBody,
    recipients,
    toggleRecipient,
  } = useStore();
  const [sent, setSent] = useState(false);

  const sourceActions = actionItems.filter((a) => a.sourceMeetingId === liveMeeting.id);

  const regenerate = () => {
    const d = followUpDrafts[tone];
    setDraftSubject(d.subject);
    setDraftBody(d.body);
  };

  const send = () => {
    setSent(true);
    setTimeout(() => setSent(false), 2400);
  };

  return (
    <div className="grid gap-6 lg:grid-cols-[1fr_340px]">
      <div className="space-y-5">
        <div className="flex items-end justify-between gap-4 animate-slide-up">
          <div className="space-y-2">
            <div className="flex items-center gap-2 text-2xs uppercase tracking-[0.18em] text-fg-subtle">
              <span className="rounded border border-accent/30 bg-accent-subtle px-1.5 py-0.5 font-mono text-accent">AI draft</span>
              <span>From</span>
              <span className="font-mono text-fg-muted normal-case tracking-normal">{liveMeeting.title}</span>
            </div>
            <h1 className="text-[28px] font-semibold tracking-tight text-fg">Smart follow-up</h1>
          </div>
          <div className="flex items-center gap-2">
            <Button variant="ghost">Save draft</Button>
            <Button variant="primary" onClick={send}>
              Send to {recipients.length}
              <span className="opacity-80">→</span>
            </Button>
          </div>
        </div>

        <RecipientPicker
          available={participants.map((p) => ({ name: p.name, initials: p.initials }))}
          selected={recipients}
          onToggle={toggleRecipient}
        />

        <ToneSelector value={tone} onChange={setTone} />

        <EmailBodyEditor
          subject={draftSubject}
          body={draftBody}
          onSubjectChange={setDraftSubject}
          onBodyChange={setDraftBody}
          onRegenerate={regenerate}
        />

        {sent && (
          <div className="flex items-center gap-3 rounded-xl border border-success/40 bg-success-subtle px-4 py-3 text-sm text-success animate-slide-up shadow-soft">
            <span className="grid h-6 w-6 place-items-center rounded-full bg-success/20 ring-1 ring-success/40 text-success">
              <svg width="12" height="12" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="3" strokeLinecap="round" strokeLinejoin="round"><polyline points="20 6 9 17 4 12" /></svg>
            </span>
            <span>
              Sent to {recipients.length} recipient{recipients.length === 1 ? "" : "s"}.
              <span className="ml-1 text-success/70">(Demo, not actually sent.)</span>
            </span>
          </div>
        )}
      </div>

      <aside className="space-y-4">
        <Card accent>
          <CardHeader>
            <CardTitle className="flex items-center gap-2">
              <span className="h-1.5 w-1.5 rounded-full bg-accent" />
              Tied to action items
            </CardTitle>
            <span className="font-mono text-2xs uppercase tracking-wider text-fg-subtle">{sourceActions.length}</span>
          </CardHeader>
          <CardBody className="space-y-3">
            {sourceActions.map((a) => (
              <div key={a.id} className="space-y-1.5 border-l-2 border-accent/40 pl-3">
                <p className="text-[13px] leading-relaxed text-fg">{a.title}</p>
                <div className="flex items-center gap-2 text-xs text-fg-muted">
                  <Badge tone="accent">{a.assigneeName}</Badge>
                  <span className="font-mono nums text-fg-subtle">due {a.dueDate}</span>
                </div>
              </div>
            ))}
          </CardBody>
        </Card>
        <div className="rounded-xl border border-border-subtle bg-bg-inset bg-dots p-4 text-xs leading-relaxed text-fg-muted">
          <p className="mb-2 flex items-center gap-1.5 font-semibold uppercase tracking-wider text-fg">
            <span className="h-1.5 w-1.5 rounded-full bg-accent animate-pulse-dot" />
            Smart Follow-Up
          </p>
          <p className="mb-2 font-mono text-2xs uppercase tracking-wider text-fg-subtle">April 2026 launch</p>
          <p>
            Three tones at launch. More will be added based on post-launch usage data. The AI-drafted body always references the source meeting and its action items.
          </p>
        </div>
      </aside>
    </div>
  );
}
