import "../../tokens.css";
import "../body-paragraph/style.css";
import "./style.css";

/**
 * body-heading, h2/h3/h4 in article context.
 *
 * @param {Object} props
 * @param {2|3|4} props.level
 * @param {string} props.children
 * @param {string} [props.className=""]
 */
export default function BodyHeading({ level, children, className = "" }) {
  const Tag = `h${level}`;
  const cls = ["uxz-h" + level, className].filter(Boolean).join(" ");
  return <Tag className={cls}>{children}</Tag>;
}
