import type { Metadata } from "next";
import { ContactForm } from "@/components/ContactForm";
import { Container } from "@/components/Container";
import { ArrowUpRight } from "@/components/Icons";
import { company } from "@/lib/content";

export const metadata: Metadata = {
  title: "Contact Us",
  description: "Contact Mitra Solar Enterprises in Tanuku, Andhra Pradesh about solar, battery and backup power options.",
};

function PinIcon() { return <svg viewBox="0 0 24 24" fill="none" aria-hidden="true"><path d="M19 10c0 5-7 11-7 11S5 15 5 10a7 7 0 1 1 14 0Z" stroke="currentColor" strokeWidth="1.6"/><circle cx="12" cy="10" r="2.2" stroke="currentColor" strokeWidth="1.6"/></svg>; }
function PhoneIcon() { return <svg viewBox="0 0 24 24" fill="none" aria-hidden="true"><path d="M7 3h3l1.5 4-2 1.5a15 15 0 0 0 6 6l1.5-2 4 1.5v3c0 1.1-.9 2-2 2C10.7 19 5 13.3 5 6c0-1.7.7-3 2-3Z" stroke="currentColor" strokeWidth="1.6" strokeLinejoin="round"/></svg>; }

export default function ContactPage() {
  const mapQuery = encodeURIComponent(company.address);
  return <>
    <section className="page-intro"><Container><span className="eyebrow"><i />Contact Us</span><h1>Let’s start with what you need.</h1><p>Share a few details and our team can follow up to understand your solar, storage or backup power requirement.</p></Container></section>
    <section className="page-body"><Container className="contact-layout">
      <div className="contact-details"><h2>A local conversation, at your pace.</h2><p>Reach out by phone or leave a note using the form. We’re based in Tanuku, Andhra Pradesh.</p>
        <div className="contact-item"><span className="contact-item-icon"><PhoneIcon /></span><div><small>Call us</small><a href={`tel:${company.phoneLink}`}>{company.phoneDisplay}</a></div></div>
        <div className="contact-item"><span className="contact-item-icon"><PinIcon /></span><div><small>Visit us</small><strong>{company.address}</strong></div></div>
        <div className="contact-map"><strong>Find us in Tanuku</strong><span>Velpur Road, Andhra Pradesh 534211</span><a href={`https://maps.google.com/?q=${mapQuery}`} target="_blank" rel="noreferrer">Open in Google Maps <ArrowUpRight style={{ display: "inline", width: 13, height: 13, verticalAlign: "middle" }} /></a></div>
      </div>
      <ContactForm />
    </Container></section>
  </>;
}
