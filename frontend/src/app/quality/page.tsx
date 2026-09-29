import type { Metadata } from "next";
import { PageIntro } from "@/components/PageIntro";
import { Container } from "@/components/Container";

export const metadata: Metadata = {
  title: "Quality",
  description: "How Mitra Solar Enterprises approaches product selection, planning and installation conversations.",
};

const steps = [
  { title: "Listen and understand", copy: "We start by learning about the property, how power is used and what you want the system to do." },
  { title: "Discuss suitable options", copy: "We explain the product choices and practical considerations that relate to your stated requirement." },
  { title: "Plan the work", copy: "Before work begins, we align on the scope, site details and the next steps for the project." },
  { title: "Review the details", copy: "We make time to go through the setup and answer questions as the work is completed." },
];

export default function QualityPage() {
  return <>
    <PageIntro eyebrow="Quality" title="A considered approach, from first discussion to follow-through." description="Good work starts with understanding the requirement and being clear about what happens next. Here is the approach we bring to each conversation." />
    <section className="page-body"><Container className="quality-grid">
      <aside className="quality-aside"><span className="eyebrow" style={{ color: "var(--lime)" }}><i />How we work</span><h2>Clarity is part of the service.</h2><p>Every property and requirement is different. We take care to discuss the relevant details without making assumptions about your setup.</p></aside>
      <div className="quality-steps">{steps.map((step, index) => <article className="quality-row" key={step.title}><span className="quality-row-num">0{index + 1}</span><div><h3>{step.title}</h3><p>{step.copy}</p></div></article>)}</div>
    </Container></section>
  </>;
}
