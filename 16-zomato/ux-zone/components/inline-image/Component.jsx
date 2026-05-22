import "../../tokens.css";
import "../body-paragraph/style.css";
import "./style.css";

/**
 * inline-image, full-width figure with italic caption.
 *
 * @param {Object} props
 * @param {string} props.src
 * @param {string} [props.alt=""]
 * @param {string|JSX.Element} [props.caption] - Pass an italic string or full <em>/<strong> markup.
 */
export default function InlineImage({ src, alt = "", caption }) {
  return (
    <figure className="uxz-figure">
      <img src={src} alt={alt} />
      {caption && (
        <figcaption>
          <em>{caption}</em>
        </figcaption>
      )}
    </figure>
  );
}
