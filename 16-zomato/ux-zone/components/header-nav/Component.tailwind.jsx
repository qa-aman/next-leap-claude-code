/** header-nav, Tailwind variant. Requires ux-zone/adapters/tailwind.config.js. */
export default function HeaderNav({ logoSrc, href = "/", alt = "Zomato" }) {
  return (
    <header className="uxz-header-nav sticky top-0 z-50 bg-uxz-bg-page border-b border-uxz-border-muted h-[120px] flex items-center px-uxz-6 md:h-[72px] md:px-uxz-4">
      <a className="uxz-header-nav__brand inline-flex items-center" href={href} aria-label={`${alt} home`}>
        <img src={logoSrc} alt={alt} className="h-[26px] w-auto" />
      </a>
    </header>
  );
}
