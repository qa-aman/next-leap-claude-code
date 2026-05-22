import { cn } from "@/lib/cn";
import type { ButtonHTMLAttributes } from "react";

type Variant = "primary" | "secondary" | "ghost" | "danger";
type Size = "sm" | "md";

export function Button({
  variant = "secondary",
  size = "md",
  className,
  ...props
}: ButtonHTMLAttributes<HTMLButtonElement> & {
  variant?: Variant;
  size?: Size;
}) {
  const variants: Record<Variant, string> = {
    primary:
      "bg-gradient-to-b from-accent to-accent-hover text-white shadow-[0_1px_0_rgba(255,255,255,0.18)_inset,0_1px_2px_rgba(0,0,0,0.4),0_0_0_1px_rgba(139,109,255,0.4)] hover:shadow-glow-accent",
    secondary:
      "bg-bg-elevated text-fg border border-border hover:border-border-strong hover:bg-bg-subtle shadow-soft",
    ghost:
      "bg-bg-subtle text-fg border border-border hover:border-border-strong hover:bg-bg-elevated hover:text-fg",
    danger:
      "bg-gradient-to-b from-danger to-[#d8453d] text-white shadow-[0_1px_0_rgba(255,255,255,0.15)_inset,0_1px_2px_rgba(0,0,0,0.4)] hover:brightness-110",
  };
  const sizes: Record<Size, string> = {
    sm: "h-7 px-2.5 text-[12px]",
    md: "h-9 px-3.5 text-[13px]",
  };
  return (
    <button
      className={cn(
        "inline-flex items-center justify-center gap-1.5 rounded-md font-medium tracking-tight transition-all duration-150 disabled:opacity-50 disabled:cursor-not-allowed active:scale-[0.98] focus-visible:outline-offset-1",
        variants[variant],
        sizes[size],
        className
      )}
      {...props}
    />
  );
}
