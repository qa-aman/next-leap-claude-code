/** rating-chip Tailwind variant. */
const bgByTier = {
  green: "bg-uxz-rating-green",
  yellow: "bg-uxz-rating-yellow",
  red: "bg-uxz-rating-red",
};
export default function RatingChip({ value, tier, starSrc }) {
  const resolved = tier || (value >= 4 ? "green" : value >= 3 ? "yellow" : "red");
  return (
    <span className={[
      "uxz-rating-chip inline-flex items-center gap-uxz-1 py-uxz-1 px-uxz-2 rounded-uxz-sm",
      "font-uxz-footer text-uxz-meta font-medium text-uxz-white",
      bgByTier[resolved],
    ].join(" ")}>
      {value}
      <img src={starSrc} alt="" className="w-[10px] h-[10px]" />
    </span>
  );
}
