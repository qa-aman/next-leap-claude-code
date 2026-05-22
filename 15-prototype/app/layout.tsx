import type { Metadata } from "next";
import "./globals.css";
import { Header } from "@/components/Header";

export const metadata: Metadata = {
  title: "MeetFlow Prototype",
  description: "AI Intelligence pillar - prototype demo",
};

export default function RootLayout({ children }: { children: React.ReactNode }) {
  return (
    <html lang="en" className="dark">
      <body className="min-h-screen bg-bg text-fg font-sans antialiased selection:bg-accent/30">
        <Header />
        <main className="mx-auto max-w-6xl px-6 py-10 animate-fade-in">{children}</main>
      </body>
    </html>
  );
}
