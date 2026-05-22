import "../../tokens.css";
import "./style.css";

/**
 * tag-chip, plain-CSS variant.
 * Source: https://www.zomato.com/blog/sushi/ (article category label)
 *
 * @param {Object} props
 * @param {string} props.label             - The tag text. Source HTML: text node inside the chip span.
 * @param {"default"|"brand"} [props.variant="default"] - default = plain uppercase, brand = red pill.
 * @param {string} [props.className=""]    - Extra class names from the consumer.
 */
export default function TagChip({ label, variant = "default", className = "" }) {
  const cls = ["uxz-tag-chip", variant === "brand" ? "uxz-tag-chip--brand" : "", className]
    .filter(Boolean)
    .join(" ");
  return <span className={cls}>{label}</span>;
}
