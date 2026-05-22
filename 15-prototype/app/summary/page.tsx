"use client";
import { useRouter } from "next/navigation";
import { liveMeeting, summaryTldr, keyMoments, decisions, actionItems } from "@/lib/mock-data";
import { Card, CardBody, CardHeader, CardTitle } from "@/components/ui/Card";
import { Button } from "@/components/ui/Button";
import { Badge } from "@/components/ui/Badge";
import { Avatar } from "@/components/ui/Avatar";
import { TldrCard } from "@/ux-zone/post-summary/components/TldrCard/Component";
import { KeyMomentRow } from "@/ux-zone/post-summary/components/KeyMomentRow/Component";
import { ParticipantTalkTimeRow } from "@/ux-zone/post-summary/components/ParticipantTalkTimeRow/Component";

export default function SummaryPage() {
  const router = useRouter();
  const sourceActions = actionItems.filter((a) => a.sourceMeetingId === liveMeeting.id);

  return (
    <div className="space-y-7">
      <div className="flex items-end justify-between gap-4 animate-slide-up">
        <div className="space-y-2">
          <div className="flex items-center gap-2 text-2xs uppercase tracking-[0.18em] text-fg-subtle">
            <Badge tone="success" className="gap-1.5">
              <span className="h-1.5 w-1.5 rounded-full bg-success" /> Concluded
            </Badge>
            <span className="font-mono">{liveMeeting.date}</span>
            <span>·</span>
            <span className="font-mono">{liveMeeting.startTime} - {liveMeeting.endTime}</span>
          </div>
          <h1 className="text-[28px] font-semibold tracking-tight text-fg">{liveMeeting.title}</h1>
        </div>
        <Button variant="primary" onClick={() => router.push("/follow-up")}>
          Draft follow-up
          <span className="opacity-80">→</span>
        </Button>
      </div>

      <TldrCard
        tldr={summaryTldr}
        durationMin={liveMeeting.durationMin}
        decisionsCount={decisions.length}
        actionsCount={sourceActions.length}
      />

      <div className="grid gap-5 lg:grid-cols-2">
        <Card>
          <CardHeader>
            <CardTitle className="flex items-center gap-2">
              <span className="h-1.5 w-1.5 rounded-full bg-accent" />
              Key moments
            </CardTitle>
            <span className="font-mono text-2xs uppercase tracking-wider text-fg-subtle">{keyMoments.length}</span>
          </CardHeader>
          <CardBody className="px-2 py-2">
            <div className="space-y-0.5">
              {keyMoments.map((m) => (
                <KeyMomentRow key={m.id} moment={m} />
              ))}
            </div>
          </CardBody>
        </Card>

        <Card>
          <CardHeader>
            <CardTitle className="flex items-center gap-2">
              <span className="h-1.5 w-1.5 rounded-full bg-success" />
              Decisions
            </CardTitle>
            <span className="font-mono text-2xs uppercase tracking-wider text-fg-subtle">{decisions.length}</span>
          </CardHeader>
          <CardBody className="space-y-3">
            {decisions.map((d, i) => (
              <div
                key={d.id}
                className="group relative rounded-lg border border-border-subtle bg-bg-inset px-3 py-2.5 transition-colors hover:border-border"
              >
                <span className="absolute left-0 top-3 bottom-3 w-[2px] rounded-r bg-gradient-to-b from-success to-success/30" />
                <p className="pl-2 text-[13px] leading-relaxed text-fg">{d.text}</p>
                <div className="mt-1.5 pl-2 flex items-center gap-2 text-2xs uppercase tracking-wider text-fg-subtle">
                  <span>Owner</span>
                  <Badge tone="accent">{d.owner}</Badge>
                </div>
              </div>
            ))}
          </CardBody>
        </Card>
      </div>

      <Card>
        <CardHeader>
          <CardTitle className="flex items-center gap-2">
            <span className="h-1.5 w-1.5 rounded-full bg-warning" />
            Participants
          </CardTitle>
          <span className="font-mono text-2xs uppercase tracking-wider text-fg-subtle">Talk time</span>
        </CardHeader>
        <CardBody className="space-y-1">
          {liveMeeting.participants.map((p) => (
            <ParticipantTalkTimeRow key={p.id} participant={p} />
          ))}
        </CardBody>
      </Card>

      <Card>
        <CardHeader>
          <CardTitle className="flex items-center gap-2">
            <span className="h-1.5 w-1.5 rounded-full bg-accent" />
            Action items from this meeting
          </CardTitle>
          <Button size="sm" variant="ghost" onClick={() => router.push("/action-items")}>
            View all <span className="opacity-70">›</span>
          </Button>
        </CardHeader>
        <CardBody className="space-y-2">
          {sourceActions.map((a) => (
            <div key={a.id} className="group flex items-center justify-between gap-3 rounded-lg border border-border-subtle bg-bg-inset px-3 py-2.5 lift hover:border-border">
              <span className="flex min-w-0 items-center gap-2.5">
                <span className="h-1.5 w-1.5 shrink-0 rounded-full bg-fg-subtle group-hover:bg-accent transition-colors" />
                <span className="truncate text-[13px] text-fg">{a.title}</span>
              </span>
              <div className="flex items-center gap-2 text-xs text-fg-muted">
                <Avatar initials={a.assigneeName.split(" ").map((n) => n[0]).join("").slice(0, 2).toUpperCase()} size={18} />
                <span>{a.assigneeName}</span>
                <span className="text-fg-subtle">·</span>
                <span className="font-mono nums">{a.dueDate}</span>
              </div>
            </div>
          ))}
        </CardBody>
      </Card>
    </div>
  );
}
