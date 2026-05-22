/** footer Tailwind variant: same DOM, utility classes. */
export default function Footer({ logoSrc, columns = [], social = [], stores = [], legal = "" }) {
  return (
    <footer className="uxz-footer bg-uxz-bg-footer text-uxz-text-default font-uxz-footer py-uxz-8 px-uxz-6 md:px-uxz-4 md:py-uxz-7">
      <div className="uxz-footer__inner max-w-[1200px] mx-auto">
        {logoSrc && (
          <div className="uxz-footer__brand">
            <img src={logoSrc} alt="Zomato" className="h-[28px] w-auto mb-uxz-7" />
          </div>
        )}
        <div className="grid grid-cols-5 gap-uxz-7 lg:grid-cols-3 md:grid-cols-2 md:gap-uxz-6 [@media(max-width:360px)]:grid-cols-1">
          {columns.map((col, i) => (
            <div key={i}>
              <h3 className="m-0 mb-uxz-3 text-uxz-footer-h3 font-medium text-uxz-text-footer-heading uppercase tracking-[2px]">{col.title}</h3>
              <ul className="list-none m-0 p-0 flex flex-col gap-uxz-2">
                {col.links.map((l, j) => <li key={j}><a className="text-uxz-meta font-light text-uxz-text-muted hover:text-uxz-text-footer-heading no-underline" href={l.href}>{l.label}</a></li>)}
              </ul>
            </div>
          ))}
          {(social.length > 0 || stores.length > 0) && (
            <div>
              <h3 className="m-0 mb-uxz-3 text-uxz-footer-h3 font-medium text-uxz-text-footer-heading uppercase tracking-[2px]">Social Links</h3>
              <div className="flex gap-uxz-3 mb-uxz-4">
                {social.map((s, i) => <a key={i} href={s.href} aria-label={s.label}><img src={s.iconSrc} alt="" width={28} height={28} /></a>)}
              </div>
              <div className="flex flex-col gap-uxz-2">
                {stores.map((s, i) => <a key={i} href={s.href}><img src={s.src} alt={s.alt} className="h-[40px] w-auto" /></a>)}
              </div>
            </div>
          )}
        </div>
        {legal && <p className="uxz-footer__legal mt-uxz-8 text-uxz-copy font-light text-uxz-text-muted">{legal}</p>}
      </div>
    </footer>
  );
}
