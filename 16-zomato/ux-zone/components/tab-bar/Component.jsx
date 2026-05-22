import "../../tokens.css";
import "./style.css";

/**
 * tab-bar
 * @param {Object} props
 * @param {Array<{id: string, label: string}>} props.tabs
 * @param {string} props.selectedId
 * @param {(id: string) => void} [props.onSelect]
 */
export default function TabBar({ tabs = [], selectedId, onSelect }) {
  return (
    <div className="uxz-tab-bar" role="tablist">
      {tabs.map((t) => (
        <button
          key={t.id}
          className="uxz-tab-bar__tab"
          role="tab"
          aria-selected={t.id === selectedId}
          onClick={() => onSelect && onSelect(t.id)}
        >
          <span className="uxz-tab-bar__label">{t.label}</span>
        </button>
      ))}
    </div>
  );
}
