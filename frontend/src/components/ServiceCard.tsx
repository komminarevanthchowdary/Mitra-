import Link from "next/link";
import { ArrowUpRight, SunIcon } from "@/components/Icons";

export function ServiceCard({
  number,
  title,
  description,
  category,
}: {
  number: string;
  title: string;
  description: string;
  category: string;
}) {
  return (
    <article className="service-card">
      <div className="service-card-top">
        <span className="service-number">{number}</span>
        <span className="service-icon"><SunIcon /></span>
      </div>
      <span className="service-category">{category}</span>
      <h3>{title}</h3>
      <p>{description}</p>
      <Link href="/contact/" aria-label={`Ask us about ${title}`} className="service-link">
        Discuss this option <ArrowUpRight />
      </Link>
    </article>
  );
}
