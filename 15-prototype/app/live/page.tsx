"use client";
import { useRouter } from "next/navigation";
import { liveMeeting, liveTranscript, liveAiNotes } from "@/lib/mock-data";
import { Avatar } from "@/components/ui/Avatar";
import { Card, CardBody } from "@/components/ui/Card";
import { TranscriptStream } from "@/ux-zone/live-meeting/components/TranscriptStream/Component";
import { AiNotesPanel } from "@/ux-zone/live-meeting/components/AiNotesPanel/Component";
import { RecordingControls } from "@/ux-zone/live-meeting/components/RecordingControls/Component";

export default function LiveMeetingPage() {
  const router = useRouter();

  return (
    <div className="space-y-5">
      <div className="space-y-2 animate-slide-up">
        <div className="flex items-center gap-2 text-2xs uppercase tracking-[0.18em] text-fg-subtle">
          <span className="relative flex h-1.5 w-1.5">
            <span className="absolute inset-0 rounded-full bg-danger animate-ping-ring" />
            <span className="relative h-1.5 w-1.5 rounded-full bg-danger" />
          </span>
          <span className="font-mono text-danger">Live</span>
          <span className="text-fg-subtle">·</span>
          <span className="font-mono">{liveMeeting.date}</span>
          <span className="text-fg-subtle">·</span>
          <span className="font-mono">started {liveMeeting.startTime}</span>
        </div>
        <h1 className="text-[28px] font-semibold tracking-tight text-fg">{liveMeeting.title}</h1>
      </div>

      <RecordingControls onEnd={() => router.push("/summary")} />

      <div className="grid gap-4 lg:grid-cols-[1fr_380px]">
        <Card>
          <CardBody>
            <div className="mb-3 flex items-center justify-between border-b border-border-subtle pb-3">
              <div className="flex items-center gap-2">
                <span className="text-[13px] font-semibold tracking-tight text-fg">Transcript</span>
                <span className="rounded border border-border-subtle bg-bg-inset px-1.5 py-0.5 font-mono text-[10px] text-fg-subtle">
                  EN · 96% accuracy
                </span>
              </div>
              <div className="flex -space-x-1.5">
                {liveMeeting.participants.map((p) => (
                  <Avatar key={p.id} initials={p.initials} size={22} className="ring-2 ring-bg-elevated" />
                ))}
              </div>
            </div>
            <TranscriptStream lines={liveTranscript} />
          </CardBody>
        </Card>

        <Card accent>
          <CardBody className="h-full">
            <AiNotesPanel notes={liveAiNotes} />
          </CardBody>
        </Card>
      </div>

      <div className="flex flex-wrap items-center gap-2 rounded-xl border border-border-subtle bg-bg-elevated px-3 py-2.5 shadow-soft">
        <span className="text-2xs uppercase tracking-[0.16em] text-fg-subtle">Speakers</span>
        {liveMeeting.participants.map((p) => (
          <span key={p.id} className="inline-flex items-center gap-1.5 rounded-md border border-border-subtle bg-bg-inset px-2 py-1 text-xs text-fg">
            <Avatar initials={p.initials} size={16} />
            {p.name}
          </span>
        ))}
      </div>
    </div>
  );
}
