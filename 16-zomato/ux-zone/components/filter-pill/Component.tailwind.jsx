/** filter-pill Tailwind variant. */
export default function FilterPill({ label, iconSrc, pressed = false, onToggle }) {
  const base =
    "uxz-filter-pill inline-flex items-center gap-uxz-2 py-uxz-2 px-uxz-4 rounded-uxz-full " +
    "font-uxz-footer text-uxz-pill cursor-pointer transition-shadow duration-100";
  const styles = pressed
    ? "bg-uxz-text-card-title text-uxz-bg-page border border-uxz-text-card-title"
    : "bg-uxz-bg-page text-uxz-text-card-title border border-uxz-border-pill hover:shadow-uxz-sm";
  const focus = "focus-visible:outline focus-visible:outline-2 focus-visible:outline-uxz-link focus-visible:outline-offset-2";
  return (
    <button
      className={[base, styles, focus, iconSrc ? "pl-uxz-3" : ""].filter(Boolean).join(" ")}
      aria-pressed={pressed}
      onClick={() => onToggle && onToggle(!pressed)}
    >
      {iconSrc && <img src={iconSrc} alt="" className="w-[14px] h-[14px]" />}
      {label}
    </button>
  );
}
