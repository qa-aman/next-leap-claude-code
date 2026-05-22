"use client";
import Link from "next/link";
import { usePathname } from "next/navigation";
import { cn } from "@/lib/cn";

const nav = [
  { href: "/", label: "Meetings" },
  { href: "/live", label: "Live" },
  { href: "/summary", label: "Summary" },
  { href: "/action-items", label: "Action items" },
  { href: "/follow-up", label: "Follow-up" },
];

export function Header() {
  const pathname = usePathname();
  return (
    <header className="sticky top-0 z-20 border-b border-border-subtle bg-bg/70 backdrop-blur-xl">
      <div className="pointer-events-none absolute inset-x-0 -bottom-px h-px bg-gradient-to-r from-transparent via-accent/40 to-transparent opacity-60" />
      <div className="mx-auto flex max-w-6xl items-center justify-between px-6 py-3">
        <Link href="/" className="group flex items-center gap-2.5 text-fg">
          <span className="relative grid h-7 w-7 place-items-center rounded-md bg-gradient-to-br from-accent to-accent-hover text-white font-mono text-[11px] font-bold shadow-glow-accent">
            MF
            <span className="absolute inset-0 rounded-md ring-1 ring-inset ring-white/10" />
          </span>
          <span className="text-sm font-semibold tracking-tight">MeetFlow</span>
          <span className="ml-1.5 rounded-full border border-border bg-bg-subtle px-2 py-0.5 font-mono text-[10px] uppercase tracking-wider text-fg-muted">
            v0.1
          </span>
        </Link>
        <nav className="flex items-center gap-0.5 rounded-lg border border-border-subtle bg-bg-elevated/60 p-1 backdrop-blur">
          {nav.map((item) => {
            const active = pathname === item.href;
            return (
              <Link
                key={item.href}
                href={item.href}
                className={cn(
                  "relative rounded-md px-3 py-1.5 text-[13px] font-medium transition-all",
                  active
                    ? "bg-bg-subtle text-fg shadow-soft"
                    : "text-fg-muted hover:bg-bg-subtle/60 hover:text-fg"
                )}
              >
                {item.label}
                {active && (
                  <span className="absolute inset-x-3 -bottom-px h-px bg-gradient-to-r from-transparent via-accent to-transparent" />
                )}
              </Link>
            );
          })}
        </nav>
        <div className="flex items-center gap-2">
          <button className="hidden items-center gap-2 rounded-md border border-border-subtle bg-bg-elevated/60 px-2.5 py-1.5 text-xs text-fg-muted transition-colors hover:border-border hover:text-fg sm:inline-flex">
            <span>Search</span>
            <kbd className="rounded border border-border bg-bg-subtle px-1.5 py-0.5 font-mono text-[10px] text-fg-subtle">⌘K</kbd>
          </button>
          <div className="relative grid h-7 w-7 place-items-center rounded-full bg-gradient-to-br from-accent-subtle to-bg-subtle text-[11px] font-semibold text-fg ring-1 ring-border">
            AP
          </div>
        </div>
      </div>
    </header>
  );
}
