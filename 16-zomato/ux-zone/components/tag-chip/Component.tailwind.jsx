/**
 * tag-chip, Tailwind variant.
 * Requires the generated tailwind.config.js from ux-zone/adapters/.
 *
 * @param {Object} props
 * @param {string} props.label
 * @param {"default"|"brand"} [props.variant="default"]
 * @param {string} [props.className=""]
 */
export default function TagChip({ label, variant = "default", className = "" }) {
  const base =
    "uxz-tag-chip inline-block font-uxz-article text-uxz-tag uppercase tracking-[1px] " +
    "py-uxz-1 mb-uxz-3";
  const styles =
    variant === "brand"
      ? "text-uxz-bg-page bg-uxz-brand-red px-uxz-3 rounded-uxz-full ml-uxz-3"
      : "text-uxz-text-muted bg-transparent px-0";
  return <span className={[base, styles, className].filter(Boolean).join(" ")}>{label}</span>;
}
