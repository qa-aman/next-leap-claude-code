/** pull-quote Tailwind variant. */
export default function PullQuote({ children, attribution }) {
  return (
    <blockquote className="uxz-pullquote my-uxz-6 pl-uxz-7 pr-uxz-5 border-l-[4px] border-uxz-brand-red font-uxz-article">
      <p className="m-0 text-uxz-blockquote font-medium text-uxz-text-heading">
        <em className="italic font-light text-uxz-text-body text-uxz-body leading-[32.5px]">{children}</em>
        {attribution ? <> - {attribution}</> : null}
      </p>
    </blockquote>
  );
}
