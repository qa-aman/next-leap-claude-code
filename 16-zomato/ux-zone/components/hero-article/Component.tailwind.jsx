/** hero-article, Tailwind variant. */
export default function HeroArticle({ tag, title, author, date, readTime, heroSrc, heroAlt = "" }) {
  return (
    <section className="uxz-hero-article max-w-uxz-article mx-auto pt-uxz-9 px-uxz-6 pb-uxz-6 font-uxz-article">
      <span className="uxz-tag-chip inline-block font-uxz-article text-uxz-tag uppercase tracking-[1px] text-uxz-text-muted py-uxz-1 mb-uxz-3">{tag}</span>
      <h1 className="uxz-hero-article__title m-0 mb-uxz-6 text-uxz-h1 text-uxz-text-h1 font-medium tracking-[-0.5px]">{title}</h1>
      <div className="uxz-hero-article__meta flex flex-wrap gap-uxz-2 text-uxz-meta text-uxz-text-body font-light mb-uxz-6">
        <span>{author}</span><span className="text-uxz-text-muted">|</span>
        <span>{date}</span><span className="text-uxz-text-muted">|</span>
        <span>{readTime}</span>
      </div>
      <figure className="uxz-hero-article__media mt-uxz-6">
        <img src={heroSrc} alt={heroAlt} className="w-full" />
      </figure>
    </section>
  );
}
