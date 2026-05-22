import "../../tokens.css";
import "./style.css";

/**
 * collection-card
 * @param {Object} props
 * @param {string} props.href
 * @param {string} props.imgSrc
 * @param {string} props.title
 * @param {string} props.placesLabel - e.g. "82 Places"
 * @param {string} [props.chevronSrc="../../assets/icons/chevron-right.svg"]
 */
export default function CollectionCard({ href, imgSrc, title, placesLabel, chevronSrc = "../../assets/icons/chevron-right.svg" }) {
  return (
    <a className="uxz-collection-card" href={href}>
      <img className="uxz-collection-card__img" src={imgSrc} alt={title} />
      <div className="uxz-collection-card__overlay">
        <p className="uxz-collection-card__title">{title}</p>
        <div className="uxz-collection-card__meta">
          <span>{placesLabel}</span>
          <img src={chevronSrc} alt="" />
        </div>
      </div>
    </a>
  );
}
