/** body-paragraph Tailwind wrapper. Children use raw <p>/<strong>/<em>/<a>; outer class applies prose styles. */
export default function Prose({ children, className = "" }) {
  return (
    <article
      className={[
        "uxz-prose max-w-uxz-article mx-auto px-uxz-6 font-uxz-article text-uxz-text-body",
        "[&_p]:my-uxz-5 [&_p]:text-uxz-body [&_p]:font-light [&_p]:text-uxz-text-body",
        "[&_strong]:text-uxz-text-heading [&_strong]:font-medium",
        "[&_em]:italic [&_em]:text-uxz-text-body",
        "[&_a]:text-uxz-link [&_a]:no-underline hover:[&_a]:underline",
        className,
      ]
        .filter(Boolean)
        .join(" ")}
    >
      {children}
    </article>
  );
}
