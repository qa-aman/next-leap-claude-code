/** collection-card Tailwind variant. */
export default function CollectionCard({ href, imgSrc, title, placesLabel, chevronSrc }) {
  return (
    <a href={href} className="uxz-collection-card block relative w-[274px] h-[380px] rounded-uxz-md overflow-hidden no-underline text-uxz-white font-uxz-footer md:w-[220px] md:h-[300px]">
      <img src={imgSrc} alt={title} className="w-full h-full object-cover block" />
      <div className="absolute inset-x-0 bottom-0 p-uxz-4 px-uxz-5 bg-gradient-to-t from-black/65 to-transparent">
        <p className="m-0 mb-uxz-2 text-uxz-h4 font-semibold text-uxz-white">{title}</p>
        <div className="flex items-center gap-uxz-2 text-uxz-meta font-light text-uxz-white">
          <span>{placesLabel}</span>
          <img src={chevronSrc} alt="" className="w-[12px] h-[12px] invert" />
        </div>
      </div>
    </a>
  );
}
