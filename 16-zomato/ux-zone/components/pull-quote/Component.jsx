import "../../tokens.css";
import "../body-paragraph/style.css";
import "./style.css";

/**
 * pull-quote, blockquote with brand-red left border.
 *
 * @param {{ children: any, attribution?: string }} props
 */
export default function PullQuote({ children, attribution }) {
  return (
    <blockquote className="uxz-pullquote">
      <p>
        <em>{children}</em>
        {attribution ? <> - {attribution}</> : null}
      </p>
    </blockquote>
  );
}
