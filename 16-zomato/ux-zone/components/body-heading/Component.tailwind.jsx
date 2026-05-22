/** body-heading Tailwind variant: switches utility classes by level. */
const sizeByLevel = {
  2: "text-uxz-h2 font-semibold mt-uxz-8 mb-uxz-3 md:text-[28px] md:leading-[36px]",
  3: "text-uxz-h3 font-semibold mt-uxz-5 mb-uxz-3 md:text-[22px] md:leading-[30px]",
  4: "text-uxz-h4 font-semibold mt-uxz-4 mb-uxz-2",
};
export default function BodyHeading({ level, children, className = "" }) {
  const Tag = `h${level}`;
  const cls = [
    "uxz-h" + level,
    "font-uxz-article text-uxz-text-heading",
    sizeByLevel[level],
    className,
  ]
    .filter(Boolean)
    .join(" ");
  return <Tag className={cls}>{children}</Tag>;
}
