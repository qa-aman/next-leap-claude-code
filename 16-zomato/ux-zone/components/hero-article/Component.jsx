import "../../tokens.css";
import "../tag-chip/style.css";
import "./style.css";

/**
 * hero-article, plain-CSS variant.
 * Source: zomato.com/blog/sushi/ article hero block.
 *
 * @param {Object} props
 * @param {string} props.tag      - Category label, e.g. "technology"
 * @param {string} props.title    - h1 text
 * @param {string} props.author
 * @param {string} props.date     - DD-MM-YYYY string
 * @param {string} props.readTime - e.g. "6 mins read"
 * @param {string} props.heroSrc  - Hero image URL
 * @param {string} [props.heroAlt=""]
 */
export default function HeroArticle({ tag, title, author, date, readTime, heroSrc, heroAlt = "" }) {
  return (
    <section className="uxz-hero-article">
      <span className="uxz-tag-chip">{tag}</span>
      <h1 className="uxz-hero-article__title">{title}</h1>
      <div className="uxz-hero-article__meta">
        <span className="uxz-hero-article__author">{author}</span>
        <span className="uxz-hero-article__sep">|</span>
        <span className="uxz-hero-article__date">{date}</span>
        <span className="uxz-hero-article__sep">|</span>
        <span className="uxz-hero-article__read">{readTime}</span>
      </div>
      <figure className="uxz-hero-article__media">
        <img src={heroSrc} alt={heroAlt} />
      </figure>
    </section>
  );
}
