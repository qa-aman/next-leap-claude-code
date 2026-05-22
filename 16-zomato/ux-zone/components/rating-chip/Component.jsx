import "../../tokens.css";
import "./style.css";

/**
 * rating-chip
 * @param {Object} props
 * @param {number} props.value     - Numeric rating, e.g. 4.3
 * @param {"green"|"yellow"|"red"} [props.tier] - Manual tier override
 * @param {string} [props.starSrc="../../assets/icons/star-fill.svg"]
 */
export default function RatingChip({ value, tier, starSrc = "../../assets/icons/star-fill.svg" }) {
  const resolved = tier || (value >= 4 ? "green" : value >= 3 ? "yellow" : "red");
  return (
    <span className="uxz-rating-chip" data-tier={resolved}>
      {value}
      <img src={starSrc} alt="" />
    </span>
  );
}
