"use client";
import { create } from "zustand";
import { followUpDrafts, type Confidence } from "./mock-data";

type ActionFilter = "all" | "high" | "needs-review";
type Tone = "concise" | "warm" | "direct";

type State = {
  selectedMeetingId: string | null;
  setSelectedMeetingId: (id: string | null) => void;

  actionFilter: ActionFilter;
  setActionFilter: (f: ActionFilter) => void;

  tone: Tone;
  setTone: (t: Tone) => void;

  draftSubject: string;
  draftBody: string;
  recipients: string[];
  setDraftSubject: (s: string) => void;
  setDraftBody: (s: string) => void;
  toggleRecipient: (name: string) => void;
};

export const useStore = create<State>((set) => ({
  selectedMeetingId: null,
  setSelectedMeetingId: (id) => set({ selectedMeetingId: id }),

  actionFilter: "all",
  setActionFilter: (f) => set({ actionFilter: f }),

  tone: "concise",
  setTone: (t) =>
    set({
      tone: t,
      draftSubject: followUpDrafts[t].subject,
      draftBody: followUpDrafts[t].body,
    }),

  draftSubject: followUpDrafts.concise.subject,
  draftBody: followUpDrafts.concise.body,
  recipients: ["Aisha Patel", "Tomas Herrera"],
  setDraftSubject: (s) => set({ draftSubject: s }),
  setDraftBody: (s) => set({ draftBody: s }),
  toggleRecipient: (name) =>
    set((s) => ({
      recipients: s.recipients.includes(name)
        ? s.recipients.filter((r) => r !== name)
        : [...s.recipients, name],
    })),
}));

export type { ActionFilter, Tone, Confidence };
