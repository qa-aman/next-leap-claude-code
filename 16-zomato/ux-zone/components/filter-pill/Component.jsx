import "../../tokens.css";
import "./style.css";

/**
 * filter-pill
 * @param {Object} props
 * @param {string} props.label
 * @param {string} [props.iconSrc]   - Optional leading icon
 * @param {boolean} [props.pressed]
 * @param {(next: boolean) => void} [props.onToggle]
 */
export default function FilterPill({ label, iconSrc, pressed = false, onToggle }) {
  const cls = ["uxz-filter-pill", iconSrc ? "uxz-filter-pill--with-icon" : ""].filter(Boolean).join(" ");
  return (
    <button className={cls} aria-pressed={pressed} onClick={() => onToggle && onToggle(!pressed)}>
      {iconSrc && <img src={iconSrc} alt="" />}
      {label}
    </button>
  );
}
