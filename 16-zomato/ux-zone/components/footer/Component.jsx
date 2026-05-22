import "../../tokens.css";
import "./style.css";

/**
 * footer, 5-column site footer.
 * Source: zomato.com/blog/sushi/ footer.
 *
 * @param {Object} props
 * @param {string} [props.logoSrc]
 * @param {Array<{title: string, links: Array<{label: string, href: string}>}>} [props.columns]
 * @param {Array<{href: string, iconSrc: string, label: string}>} [props.social]
 * @param {Array<{href: string, src: string, alt: string}>} [props.stores]
 * @param {string} [props.legal]
 */
export default function Footer({ logoSrc, columns = [], social = [], stores = [], legal = "" }) {
  return (
    <footer className="uxz-footer">
      <div className="uxz-footer__inner">
        {logoSrc && <div className="uxz-footer__brand"><img src={logoSrc} alt="Zomato" /></div>}
        <div className="uxz-footer__cols">
          {columns.map((col, i) => (
            <div className="uxz-footer__col" key={i}>
              <h3>{col.title}</h3>
              <ul>{col.links.map((l, j) => <li key={j}><a href={l.href}>{l.label}</a></li>)}</ul>
            </div>
          ))}
          {(social.length > 0 || stores.length > 0) && (
            <div className="uxz-footer__col">
              <h3>Social Links</h3>
              <div className="uxz-footer__social">
                {social.map((s, i) => <a key={i} href={s.href} aria-label={s.label}><img src={s.iconSrc} alt="" width={28} height={28} /></a>)}
              </div>
              <div className="uxz-footer__stores">
                {stores.map((s, i) => <a key={i} href={s.href}><img src={s.src} alt={s.alt} width={136} /></a>)}
              </div>
            </div>
          )}
        </div>
        {legal && <p className="uxz-footer__legal">{legal}</p>}
      </div>
    </footer>
  );
}
