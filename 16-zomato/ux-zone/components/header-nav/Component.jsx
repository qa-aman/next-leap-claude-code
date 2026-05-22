import "../../tokens.css";
import "./style.css";

/**
 * header-nav, logo-only sticky header.
 * Source: zomato.com/blog/sushi/
 *
 * @param {Object} props
 * @param {string} [props.logoSrc="../../assets/images/b40b97e677bc7b2ca77c58c61db266fe1603954218.png"]
 * @param {string} [props.href="/"]
 * @param {string} [props.alt="Zomato"]
 */
export default function HeaderNav({
  logoSrc = "../../assets/images/b40b97e677bc7b2ca77c58c61db266fe1603954218.png",
  href = "/",
  alt = "Zomato",
}) {
  return (
    <header className="uxz-header-nav">
      <a className="uxz-header-nav__brand" href={href} aria-label={`${alt} home`}>
        <img src={logoSrc} alt={alt} width={120} height={26} />
      </a>
    </header>
  );
}
