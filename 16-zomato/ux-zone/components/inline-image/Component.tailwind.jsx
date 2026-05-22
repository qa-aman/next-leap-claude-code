/** inline-image Tailwind variant. */
export default function InlineImage({ src, alt = "", caption }) {
  return (
    <figure className="uxz-figure my-uxz-6 font-uxz-article">
      <img src={src} alt={alt} className="w-full" />
      {caption && (
        <figcaption className="mt-uxz-3 text-center text-uxz-body font-light text-uxz-text-body italic md:text-[16px] md:leading-[24px]">
          {caption}
        </figcaption>
      )}
    </figure>
  );
}
