import "../../tokens.css";
import "./style.css";

/**
 * breadcrumb
 * @param {Object} props
 * @param {Array<{label: string, href?: string}>} props.items - last item has no href, rendered as current
 */
export default function Breadcrumb({ items = [] }) {
  return (
    <nav className="uxz-breadcrumb" aria-label="Breadcrumb">
      {items.map((it, i) => {
        const isLast = i === items.length - 1;
        const sep = !isLast ? <span className="uxz-breadcrumb__sep">/</span> : null;
        if (isLast) return <span key={i} className="uxz-breadcrumb__current">{it.label}</span>;
        return <span key={i}><a href={it.href}>{it.label}</a>{sep}</span>;
      })}
    </nav>
  );
}
