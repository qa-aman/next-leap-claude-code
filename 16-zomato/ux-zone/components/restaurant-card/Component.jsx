import "../../tokens.css";
import "../rating-chip/style.css";
import "../price-tag/style.css";
import "./style.css";
import RatingChip from "../rating-chip/Component.jsx";
import PriceTag from "../price-tag/Component.jsx";

/**
 * restaurant-card
 * @param {Object} props
 * @param {string} props.href
 * @param {string} props.imageSrc
 * @param {string} props.name
 * @param {number} props.rating
 * @param {string} props.cuisines
 * @param {number} props.costForTwo
 * @param {string} props.locality
 * @param {string} props.distance
 * @param {string} [props.offerLabel]
 * @param {string} [props.offerIconSrc]
 * @param {boolean} [props.promoted=false]
 */
export default function RestaurantCard({
  href, imageSrc, name, rating, cuisines, costForTwo, locality, distance,
  offerLabel, offerIconSrc, promoted = false,
}) {
  return (
    <a className="uxz-restaurant-card" href={href}>
      <div className="uxz-restaurant-card__media">
        {promoted && <span className="uxz-restaurant-card__promoted">Promoted</span>}
        <img className="uxz-restaurant-card__image" src={imageSrc} alt="" />
        {offerLabel && (
          <div className="uxz-restaurant-card__offer">
            {offerIconSrc && <img src={offerIconSrc} alt="" />}
            <span>{offerLabel}</span>
          </div>
        )}
      </div>
      <div className="uxz-restaurant-card__body">
        <div className="uxz-restaurant-card__row">
          <h4 className="uxz-restaurant-card__name">{name}</h4>
          <RatingChip value={rating} />
        </div>
        <p className="uxz-restaurant-card__cuisines">{cuisines}</p>
        <PriceTag amount={costForTwo} />
        <div className="uxz-restaurant-card__foot">
          <p className="uxz-restaurant-card__locality">{locality}</p>
          <p className="uxz-restaurant-card__distance">{distance}</p>
        </div>
      </div>
    </a>
  );
}
