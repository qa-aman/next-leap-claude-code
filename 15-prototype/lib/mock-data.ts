// MeetFlow prototype mock data. All dates use DD-MM-YYYY format; workshop "today" is 17-03-2026.
// Numbers cited as MeetFlow stats trace to 03-product-knowledge/company.md or 04-strategy/product-vision.md.

export type Participant = {
  id: string;
  name: string;
  initials: string;
  talkTimePct?: number;
  wpm?: number;
};

export type Meeting = {
  id: string;
  title: string;
  date: string; // DD-MM-YYYY
  startTime: string; // HH:mm
  endTime: string;
  durationMin: number;
  participants: Participant[];
  recordingOn: boolean;
  status: "upcoming" | "live" | "completed";
  agenda: string[];
};

export type Confidence = "high" | "medium" | "low";

export type ActionItem = {
  id: string;
  title: string;
  assigneeId: string;
  assigneeName: string;
  dueDate: string; // DD-MM-YYYY
  confidence: Confidence;
  confidencePct: number;
  state: "needs-review" | "confirmed";
  sourceMeetingId: string;
  sourceMeetingTitle: string;
};

export type TranscriptLine = {
  id: string;
  speakerId: string;
  speakerName: string;
  timestamp: string; // mm:ss
  text: string;
};

export type KeyMoment = {
  id: string;
  timestamp: string;
  title: string;
};

export type Decision = {
  id: string;
  text: string;
  owner: string;
};

export const participants: Participant[] = [
  { id: "p1", name: "Aman Parmar", initials: "AP", talkTimePct: 42, wpm: 156 },
  { id: "p2", name: "Dana Rivera", initials: "DR", talkTimePct: 28, wpm: 142 },
  { id: "p3", name: "Aisha Patel", initials: "AI", talkTimePct: 18, wpm: 168 },
  { id: "p4", name: "Tomas Herrera", initials: "TH", talkTimePct: 12, wpm: 134 },
];

export const meetings: Meeting[] = [
  {
    id: "m1",
    title: "Pro churn deep-dive",
    date: "17-03-2026",
    startTime: "10:00",
    endTime: "10:45",
    durationMin: 45,
    participants: [participants[0], participants[1], participants[2]],
    recordingOn: true,
    status: "upcoming",
    agenda: [
      "Review Q4 2025 churn data (4.1% monthly)",
      "Map churn reasons to action item accuracy complaints",
      "Decide Smart Follow-Up scope cut for April launch",
    ],
  },
  {
    id: "m2",
    title: "Smart Follow-Up design review",
    date: "17-03-2026",
    startTime: "14:00",
    endTime: "14:30",
    durationMin: 30,
    participants: [participants[0], participants[2], participants[3]],
    recordingOn: true,
    status: "upcoming",
    agenda: [
      "Walk through the composer flow",
      "Tone selector: Concise / Warm / Direct",
      "Align on April launch readiness",
    ],
  },
  {
    id: "m3",
    title: "Q1 customer interview synthesis",
    date: "18-03-2026",
    startTime: "11:00",
    endTime: "12:00",
    durationMin: 60,
    participants: [participants[0], participants[1], participants[2], participants[3]],
    recordingOn: false,
    status: "upcoming",
    agenda: [
      "Top 3 frustrations from 4 power-user interviews",
      "Action items accuracy as North Star",
      "Synthesis output: 1-pager for stakeholder update",
    ],
  },
];

export const liveMeeting = meetings[1];

export const liveTranscript: TranscriptLine[] = [
  { id: "t1", speakerId: "p1", speakerName: "Aman Parmar", timestamp: "00:14", text: "Thanks for joining. Quick agenda: we walk the composer, lock the tone selector copy, and align on the April launch gate." },
  { id: "t2", speakerId: "p3", speakerName: "Aisha Patel", timestamp: "00:42", text: "On the composer, I want to flag that the subject line auto-fill is currently using meeting title verbatim. We should consider stripping prefixes like Re or Sync." },
  { id: "t3", speakerId: "p4", speakerName: "Tomas Herrera", timestamp: "01:08", text: "Agreed. For enterprise pilots we also need a setting to disable AI-drafted bodies entirely. Three of the three pilots asked." },
  { id: "t4", speakerId: "p1", speakerName: "Aman Parmar", timestamp: "01:35", text: "Good catch. Let's add an admin toggle as a follow-up, not blocking April. Aisha, can you own the subject cleanup?" },
  { id: "t5", speakerId: "p3", speakerName: "Aisha Patel", timestamp: "01:52", text: "Yes, I'll have the spec by Thursday." },
  { id: "t6", speakerId: "p1", speakerName: "Aman Parmar", timestamp: "02:15", text: "On tone: Concise, Warm, Direct. I want to ship with three and add more based on usage data." },
];

export const liveAiNotes: string[] = [
  "Subject line auto-fill needs cleanup of Re and Sync prefixes",
  "Enterprise pilots requested admin toggle to disable AI-drafted bodies",
  "April launch ships with three tones: Concise, Warm, Direct",
  "More tones to be added based on post-launch usage data",
];

export const summaryTldr =
  "The team reviewed the Smart Follow-Up composer and locked the tone selector to three options for April launch. Two follow-ups were captured: subject line cleanup and an enterprise admin toggle. No blockers raised.";

export const keyMoments: KeyMoment[] = [
  { id: "km1", timestamp: "00:42", title: "Subject auto-fill flagged as too literal" },
  { id: "km2", timestamp: "01:08", title: "Enterprise pilots ask for AI-draft disable toggle" },
  { id: "km3", timestamp: "01:35", title: "Aman commits admin toggle as non-blocking follow-up" },
  { id: "km4", timestamp: "02:15", title: "Tone scope locked: Concise / Warm / Direct" },
];

export const decisions: Decision[] = [
  { id: "d1", text: "Ship Smart Follow-Up in April with three tones (Concise / Warm / Direct)", owner: "Aman Parmar" },
  { id: "d2", text: "Subject line cleanup blocks April launch; spec by Thursday", owner: "Aisha Patel" },
  { id: "d3", text: "Admin toggle for AI-drafted bodies is post-launch, not blocking", owner: "Tomas Herrera" },
];

export const actionItems: ActionItem[] = [
  {
    id: "a1",
    title: "Spec subject line cleanup (strip Re / Sync prefixes)",
    assigneeId: "p3",
    assigneeName: "Aisha Patel",
    dueDate: "19-03-2026",
    confidence: "high",
    confidencePct: 94,
    state: "confirmed",
    sourceMeetingId: "m2",
    sourceMeetingTitle: "Smart Follow-Up design review",
  },
  {
    id: "a2",
    title: "Draft admin toggle requirements for enterprise pilots",
    assigneeId: "p4",
    assigneeName: "Tomas Herrera",
    dueDate: "24-03-2026",
    confidence: "high",
    confidencePct: 91,
    state: "confirmed",
    sourceMeetingId: "m2",
    sourceMeetingTitle: "Smart Follow-Up design review",
  },
  {
    id: "a3",
    title: "Lock April launch gate criteria in shared doc",
    assigneeId: "p1",
    assigneeName: "Aman Parmar",
    dueDate: "20-03-2026",
    confidence: "medium",
    confidencePct: 72,
    state: "needs-review",
    sourceMeetingId: "m2",
    sourceMeetingTitle: "Smart Follow-Up design review",
  },
  {
    id: "a4",
    title: "Pull Q4 churn cohort data sliced by Pro tier",
    assigneeId: "p2",
    assigneeName: "Dana Rivera",
    dueDate: "21-03-2026",
    confidence: "medium",
    confidencePct: 68,
    state: "needs-review",
    sourceMeetingId: "m1",
    sourceMeetingTitle: "Pro churn deep-dive",
  },
  {
    id: "a5",
    title: "Schedule follow-up with Notion AI competitive review",
    assigneeId: "p1",
    assigneeName: "Aman Parmar",
    dueDate: "25-03-2026",
    confidence: "low",
    confidencePct: 41,
    state: "needs-review",
    sourceMeetingId: "m1",
    sourceMeetingTitle: "Pro churn deep-dive",
  },
  {
    id: "a6",
    title: "Map interview themes to roadmap bets (NSM align)",
    assigneeId: "p3",
    assigneeName: "Aisha Patel",
    dueDate: "23-03-2026",
    confidence: "high",
    confidencePct: 88,
    state: "confirmed",
    sourceMeetingId: "m3",
    sourceMeetingTitle: "Q1 customer interview synthesis",
  },
  {
    id: "a7",
    title: "Investigate Granola Mac-native UX gap for prosumer segment",
    assigneeId: "p2",
    assigneeName: "Dana Rivera",
    dueDate: "27-03-2026",
    confidence: "low",
    confidencePct: 38,
    state: "needs-review",
    sourceMeetingId: "m3",
    sourceMeetingTitle: "Q1 customer interview synthesis",
  },
];

export const followUpDrafts: Record<"concise" | "warm" | "direct", { subject: string; body: string }> = {
  concise: {
    subject: "Recap: Smart Follow-Up design review",
    body: `Hi team,

Quick recap of today.

- Tone selector ships with three options: Concise, Warm, Direct.
- Aisha owns subject line cleanup spec by Thursday (19-03-2026).
- Tomas drafts admin toggle requirements by 24-03-2026.
- Aman locks April launch gate criteria by 20-03-2026.

April launch on track.

Aman`,
  },
  warm: {
    subject: "Great session today, here's the recap",
    body: `Hi team,

Thanks for a sharp 30 minutes today. We walked the Smart Follow-Up composer end to end and came out with a clean plan for April.

We agreed to ship with three tones (Concise, Warm, Direct) and revisit based on usage data once we are live. Aisha is going to own the subject line cleanup spec and have it ready by Thursday. Tomas will draft the admin toggle requirements that the enterprise pilots flagged, with a target of next Tuesday. I will lock the April launch gate criteria by Friday.

Really feeling good about where this is heading.

Aman`,
  },
  direct: {
    subject: "Smart Follow-Up: 3 owners, 3 dates, ship April",
    body: `Team,

Three things from today.

1. Aisha: subject cleanup spec, due 19-03-2026.
2. Tomas: admin toggle requirements, due 24-03-2026.
3. Aman: April launch gate criteria, due 20-03-2026.

Tone scope is locked at three: Concise, Warm, Direct. No further debate this sprint.

Ship in April.

Aman`,
  },
};
