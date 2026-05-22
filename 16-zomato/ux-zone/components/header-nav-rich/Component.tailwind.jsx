/** header-nav-rich Tailwind variant. */
export default function HeaderNavRich({
  logoSrc, locationValue = "",
  searchPlaceholder = "Search for restaurant, cuisine or a dish",
  locationIconSrc, searchIconSrc, chevronSrc, showAuth = true,
}) {
  return (
    <header className="uxz-header-rich sticky top-0 z-50 bg-uxz-bg-page flex items-center gap-uxz-6 py-uxz-4 px-uxz-7 shadow-uxz-sm font-uxz-footer lg:px-uxz-5 lg:gap-uxz-4 md:px-uxz-4">
      <a className="shrink-0" href="/" aria-label="Zomato home"><img src={logoSrc} alt="Zomato" className="h-[32px] w-auto" /></a>
      <div className="flex-1 flex items-center gap-uxz-3 bg-uxz-bg-page border border-uxz-border-pill rounded-uxz-md py-uxz-2 px-uxz-4 shadow-uxz-sm md:flex-col md:items-stretch md:p-uxz-2">
        <div className="flex items-center gap-uxz-2 max-w-[360px] lg:max-w-[220px]">
          <img src={locationIconSrc} alt="" />
          <input type="text" defaultValue={locationValue} aria-label="Delivery location"
            className="border-0 outline-none bg-transparent text-uxz-meta text-uxz-text-card-title w-full placeholder:text-uxz-text-secondary" />
          <img src={chevronSrc} alt="" className="w-[12px] h-[12px]" />
        </div>
        <div className="w-px h-[24px] bg-uxz-border-pill md:hidden" />
        <div className="flex items-center gap-uxz-2 flex-1">
          <img src={searchIconSrc} alt="" />
          <input type="text" placeholder={searchPlaceholder} aria-label="Search"
            className="border-0 outline-none bg-transparent text-uxz-meta text-uxz-text-card-title w-full placeholder:text-uxz-text-secondary" />
        </div>
      </div>
      {showAuth && (
        <nav className="flex gap-uxz-6 md:hidden" aria-label="Account">
          <a href="#login" className="text-uxz-meta text-uxz-text-card-title no-underline hover:text-uxz-brand-red">Log in</a>
          <a href="#signup" className="text-uxz-meta text-uxz-text-card-title no-underline hover:text-uxz-brand-red">Sign up</a>
        </nav>
      )}
    </header>
  );
}
