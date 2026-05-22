/** price-tag Tailwind variant. */
export default function PriceTag({ amount, suffix = "for two", currency = "₹" }) {
  const formatted = amount.toLocaleString("en-IN");
  return (
    <p className="uxz-price-tag m-0 font-uxz-footer text-uxz-card-meta font-light text-uxz-text-muted">
      {currency}{formatted} {suffix}
    </p>
  );
}
