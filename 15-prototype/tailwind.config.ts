import type { Config } from "tailwindcss";

const config: Config = {
  darkMode: "class",
  content: [
    "./app/**/*.{ts,tsx}",
    "./components/**/*.{ts,tsx}",
    "./lib/**/*.{ts,tsx}",
    "./ux-zone/**/*.{ts,tsx}",
  ],
  theme: {
    extend: {
      colors: {
        bg: {
          DEFAULT: "#08080a",
          elevated: "#101013",
          subtle: "#16161b",
          inset: "#0c0c0f",
        },
        border: {
          DEFAULT: "#22222a",
          subtle: "#1a1a20",
          strong: "#2e2e38",
        },
        fg: {
          DEFAULT: "#f1f1f4",
          muted: "#8b8b96",
          subtle: "#56565f",
        },
        accent: {
          DEFAULT: "#8b6dff",
          hover: "#7a5cff",
          subtle: "#1b1538",
          glow: "#8b6dff",
        },
        success: { DEFAULT: "#3fb950", subtle: "#0d2818" },
        warning: { DEFAULT: "#e3b341", subtle: "#2a2009" },
        danger: { DEFAULT: "#f85149", subtle: "#2d0f10" },
      },
      fontFamily: {
        sans: ["Inter", "system-ui", "sans-serif"],
        mono: ["JetBrains Mono", "ui-monospace", "monospace"],
      },
      fontSize: {
        "2xs": ["10px", { lineHeight: "14px", letterSpacing: "0.04em" }],
      },
      boxShadow: {
        "glow-accent": "0 0 0 1px rgba(139,109,255,0.35), 0 0 24px -4px rgba(139,109,255,0.35)",
        "soft": "0 1px 0 rgba(255,255,255,0.03) inset, 0 1px 2px rgba(0,0,0,0.4)",
        "pop": "0 10px 40px -10px rgba(0,0,0,0.6), 0 2px 6px rgba(0,0,0,0.4)",
      },
      keyframes: {
        "fade-in": {
          "0%": { opacity: "0", transform: "translateY(4px)" },
          "100%": { opacity: "1", transform: "translateY(0)" },
        },
        "slide-up": {
          "0%": { opacity: "0", transform: "translateY(8px)" },
          "100%": { opacity: "1", transform: "translateY(0)" },
        },
        "pulse-dot": {
          "0%, 100%": { opacity: "1", transform: "scale(1)" },
          "50%": { opacity: "0.55", transform: "scale(0.85)" },
        },
        "shimmer": {
          "0%": { backgroundPosition: "-200% 0" },
          "100%": { backgroundPosition: "200% 0" },
        },
        "ping-ring": {
          "0%": { transform: "scale(1)", opacity: "0.6" },
          "100%": { transform: "scale(2.4)", opacity: "0" },
        },
      },
      animation: {
        "fade-in": "fade-in 0.4s ease-out both",
        "slide-up": "slide-up 0.5s cubic-bezier(0.16, 1, 0.3, 1) both",
        "pulse-dot": "pulse-dot 1.6s ease-in-out infinite",
        "shimmer": "shimmer 2.4s linear infinite",
        "ping-ring": "ping-ring 1.8s cubic-bezier(0, 0, 0.2, 1) infinite",
      },
      backgroundImage: {
        "grid-fade":
          "radial-gradient(ellipse 80% 50% at 50% -10%, rgba(139,109,255,0.10), transparent 60%)",
        "dot-grid":
          "radial-gradient(circle, rgba(255,255,255,0.05) 1px, transparent 1px)",
      },
    },
  },
  plugins: [],
};
export default config;
