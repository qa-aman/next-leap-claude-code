/** restaurant-card Tailwind variant. Composes inline rating-chip + price-tag. */
const tierBg = { green: "bg-uxz-rating-green", yellow: "bg-uxz-rating-yellow", red: "bg-uxz-rating-red" };
function tier(v) { return v >= 4 ? "green" : v >= 3 ? "yellow" : "red"; }

export default function RestaurantCard({
  href, imageSrc, name, rating, cuisines, costForTwo, locality, distance,
  offerLabel, offerIconSrc, starSrc, promoted = false,
}) {
  return (
    <a href={href} className="uxz-restaurant-card block w-[328px] no-underline font-uxz-footer text-uxz-text-card-title md:w-full md:max-w-[480px]">
      <div className="relative w-full aspect-[16/9] rounded-uxz-md overflow-hidden bg-uxz-border-muted">
        {promoted && <span className="absolute top-uxz-2 left-uxz-2 px-[6px] py-px bg-uxz-bg-promoted text-uxz-white text-[11px] leading-[16px] rounded-uxz-pill">Promoted</span>}
        <img src={imageSrc} alt="" className="w-full h-full object-cover block" />
        {offerLabel && (
          <div className="absolute bottom-uxz-2 left-uxz-2 flex items-center gap-uxz-2 py-uxz-1 px-uxz-2 bg-uxz-bg-page rounded-uxz-sm text-[12px] leading-[16px] font-medium text-uxz-brand-red">
            {offerIconSrc && <img src={offerIconSrc} alt="" className="w-[16px] h-[16px]" />}
            <span>{offerLabel}</span>
          </div>
        )}
      </div>
      <div className="pt-uxz-3">
        <div className="flex items-center justify-between gap-uxz-3 my-uxz-2">
          <h4 className="m-0 text-uxz-card-title font-medium text-uxz-text-card-title whitespace-nowrap overflow-hidden text-ellipsis">{name}</h4>
          <span className={["inline-flex items-center gap-uxz-1 py-uxz-1 px-uxz-2 rounded-uxz-sm text-uxz-meta font-medium text-uxz-white", tierBg[tier(rating)]].join(" ")}>
            {rating}
            <img src={starSrc} alt="" className="w-[10px] h-[10px]" />
          </span>
        </div>
        <p className="m-0 text-uxz-card-meta font-light text-uxz-text-muted whitespace-nowrap overflow-hidden text-ellipsis pb-uxz-1">{cuisines}</p>
        <p className="m-0 text-uxz-card-meta font-light text-uxz-text-muted">&#8377;{costForTwo.toLocaleString("en-IN")} for two</p>
        <div className="flex items-center justify-between pt-uxz-2 border-t border-dashed border-uxz-border-muted mt-uxz-2">
          <p className="m-0 text-uxz-card-meta font-light text-uxz-text-muted">{locality}</p>
          <p className="m-0 text-uxz-card-meta font-light text-uxz-text-muted">{distance}</p>
        </div>
      </div>
    </a>
  );
}
