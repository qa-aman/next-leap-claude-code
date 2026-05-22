import { cn } from "@/lib/cn";

const palette = [
  "bg-gradient-to-br from-[#8b6dff] to-[#5a3fd0] text-white",
  "bg-gradient-to-br from-[#3fb950] to-[#1f7a32] text-white",
  "bg-gradient-to-br from-[#e3b341] to-[#a87a1d] text-[#1a1308]",
  "bg-gradient-to-br from-[#f85149] to-[#a8302a] text-white",
  "bg-gradient-to-br from-[#4cc2ff] to-[#1a78b3] text-white",
  "bg-gradient-to-br from-[#ff7ab6] to-[#b03f78] text-white",
];

export function Avatar({ initials, size = 24, className }: { initials: string; size?: number; className?: string }) {
  const hash = initials.charCodeAt(0) + (initials.charCodeAt(1) || 0);
  const color = palette[hash % palette.length];
  return (
    <span
      className={cn(
        "inline-grid place-items-center rounded-full font-semibold leading-none ring-1 ring-inset ring-white/10 shadow-soft",
        color,
        className
      )}
      style={{ width: size, height: size, fontSize: size * 0.4, letterSpacing: "-0.02em" }}
    >
      {initials}
    </span>
  );
}
