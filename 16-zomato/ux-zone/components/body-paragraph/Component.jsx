import "../../tokens.css";
import "./style.css";

/**
 * body-paragraph wrapper: renders `<article class="uxz-prose">` so any child p/strong/em/a inherits article prose styles.
 *
 * @param {{ children: any, className?: string }} props
 */
export default function Prose({ children, className = "" }) {
  return <article className={["uxz-prose", className].filter(Boolean).join(" ")}>{children}</article>;
}
