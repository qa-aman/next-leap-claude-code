/** tab-bar Tailwind variant. */
export default function TabBar({ tabs = [], selectedId, onSelect }) {
  return (
    <div className="uxz-tab-bar flex gap-uxz-8 border-b border-uxz-border-pill md:gap-uxz-6 md:overflow-x-auto" role="tablist">
      {tabs.map((t) => {
        const isSel = t.id === selectedId;
        return (
          <button
            key={t.id}
            className={[
              "uxz-tab-bar__tab relative bg-transparent border-0 cursor-pointer py-uxz-4 font-uxz-footer",
              isSel ? "text-uxz-brand-red after:content-[''] after:absolute after:left-0 after:right-0 after:-bottom-px after:h-[3px] after:bg-uxz-brand-red after:rounded-uxz-pill"
                    : "text-uxz-text-muted hover:text-uxz-text-card-title",
            ].join(" ")}
            role="tab"
            aria-selected={isSel}
            onClick={() => onSelect && onSelect(t.id)}
          >
            <span className="text-uxz-h4 font-semibold md:text-[18px] md:leading-[24px]">{t.label}</span>
          </button>
        );
      })}
    </div>
  );
}
