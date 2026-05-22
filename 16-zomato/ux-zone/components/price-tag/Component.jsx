import "../../tokens.css";
import "./style.css";

/**
 * price-tag
 * @param {Object} props
 * @param {number} props.amount     - Integer rupees, e.g. 3000
 * @param {string} [props.suffix="for two"]
 * @param {string} [props.currency="₹"]
 */
export default function PriceTag({ amount, suffix = "for two", currency = "₹" }) {
  const formatted = amount.toLocaleString("en-IN");
  return <p className="uxz-price-tag">{currency}{formatted} {suffix}</p>;
}
