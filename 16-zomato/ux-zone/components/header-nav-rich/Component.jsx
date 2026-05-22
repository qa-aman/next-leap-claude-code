import "../../tokens.css";
import "./style.css";

/**
 * header-nav-rich
 * @param {Object} props
 * @param {string} props.logoSrc
 * @param {string} [props.locationValue=""]
 * @param {string} [props.searchPlaceholder="Search for restaurant, cuisine or a dish"]
 * @param {string} [props.locationIconSrc="../../assets/icons/location.svg"]
 * @param {string} [props.searchIconSrc="../../assets/icons/search.svg"]
 * @param {string} [props.chevronSrc="../../assets/icons/chevron-down.svg"]
 * @param {boolean} [props.showAuth=true]
 */
export default function HeaderNavRich({
  logoSrc,
  locationValue = "",
  searchPlaceholder = "Search for restaurant, cuisine or a dish",
  locationIconSrc = "../../assets/icons/location.svg",
  searchIconSrc = "../../assets/icons/search.svg",
  chevronSrc = "../../assets/icons/chevron-down.svg",
  showAuth = true,
}) {
  return (
    <header className="uxz-header-rich">
      <a className="uxz-header-rich__brand" href="/" aria-label="Zomato home">
        <img src={logoSrc} alt="Zomato" height={32} />
      </a>
      <div className="uxz-header-rich__search">
        <div className="uxz-header-rich__location">
          <img src={locationIconSrc} alt="" />
          <input type="text" defaultValue={locationValue} aria-label="Delivery location" />
          <img className="uxz-header-rich__chev" src={chevronSrc} alt="" />
        </div>
        <div className="uxz-header-rich__divider" />
        <div className="uxz-header-rich__query">
          <img src={searchIconSrc} alt="" />
          <input type="text" placeholder={searchPlaceholder} aria-label="Search" />
        </div>
      </div>
      {showAuth && (
        <nav className="uxz-header-rich__auth" aria-label="Account">
          <a href="#login">Log in</a>
          <a href="#signup">Sign up</a>
        </nav>
      )}
    </header>
  );
}
