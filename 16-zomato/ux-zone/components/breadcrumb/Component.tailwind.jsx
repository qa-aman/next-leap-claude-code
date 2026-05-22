/** breadcrumb Tailwind variant. */
export default function Breadcrumb({ items = [] }) {
  return (
    <nav className="uxz-breadcrumb flex items-center flex-wrap gap-uxz-2 font-uxz-footer text-uxz-meta font-light text-uxz-text-secondary py-uxz-3" aria-label="Breadcrumb">
      {items.map((it, i) => {
        const isLast = i === items.length - 1;
        if (isLast) return <span key={i} className="text-uxz-text-card-title font-normal">{it.label}</span>;
        return (
          <span key={i} className="flex items-center gap-uxz-2">
            <a href={it.href} className="text-uxz-text-secondary no-underline hover:text-uxz-text-card-title">{it.label}</a>
            <span className="text-uxz-text-secondary">/</span>
          </span>
        );
      })}
    </nav>
  );
}
