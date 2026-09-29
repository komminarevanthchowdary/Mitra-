import type { Metadata } from "next";
import Link from "next/link";
import { PageIntro } from "@/components/PageIntro";
import { Container } from "@/components/Container";
import { ServiceCard } from "@/components/ServiceCard";
import { ArrowRight } from "@/components/Icons";
import { services } from "@/lib/content";

export const metadata: Metadata = {
  title: "Services",
  description: "Explore solar, battery, inverter and UPS options with Mitra Solar Enterprises.",
};

export default function ServicesPage() {
  return <>
    <PageIntro eyebrow="Services" title="The right setup starts with the right conversation." description="Explore solar, storage and backup power options. We’ll first understand what you need, then talk through the details that matter for your property." />
    <section className="page-body"><Container>
      <div className="service-grid">{services.map((service) => <ServiceCard key={service.number} {...service} />)}</div>
      <div className="page-callout"><div><h2>Not sure where to begin?</h2><p>Tell us what you’re trying to solve and we’ll help you explore your options.</p></div><Link className="button button-primary" href="/contact/">Start a conversation <ArrowRight /></Link></div>
    </Container></section>
  </>;
}
