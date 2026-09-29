import Link from "next/link";
import { ArrowRight, ArrowUpRight, SunIcon } from "@/components/Icons";
import { Container } from "@/components/Container";
import { ServiceCard } from "@/components/ServiceCard";
import { company, processSteps, services } from "@/lib/content";

function SolarIllustration() {
  return (
    <div className="solar-visual" aria-label="Illustration of solar panels on a home roof" role="img">
      <svg viewBox="0 0 560 460" fill="none" xmlns="http://www.w3.org/2000/svg">
        <defs>
          <linearGradient id="roof" x1="145" y1="223" x2="449" y2="405" gradientUnits="userSpaceOnUse"><stop stopColor="#E5E6CC"/><stop offset="1" stopColor="#AEBB9E"/></linearGradient>
          <linearGradient id="panel" x1="206" y1="153" x2="372" y2="282" gradientUnits="userSpaceOnUse"><stop stopColor="#314F4B"/><stop offset="1" stopColor="#142E32"/></linearGradient>
          <linearGradient id="window" x1="322" y1="301" x2="382" y2="372" gradientUnits="userSpaceOnUse"><stop stopColor="#C4E8DA"/><stop offset="1" stopColor="#83B5A2"/></linearGradient>
        </defs>
        <circle cx="397" cy="99" r="48" fill="#D8ED6A" fillOpacity=".95"/>
        <circle cx="397" cy="99" r="66" stroke="#D8ED6A" strokeOpacity=".22"/>
        <path d="M80 340c66-52 116-71 177-76 58-5 124 10 224 66v78H80v-68Z" fill="#0C2F28" fillOpacity=".48"/>
        <path d="M141 252 311 143l169 109v161H141V252Z" fill="url(#roof)"/>
        <path d="m116 248 194-125 195 125-26 17-169-106-167 106-27-17Z" fill="#D7DDC7"/>
        <path d="M189 229 312 151l126 80-123 83-126-85Z" fill="url(#panel)" stroke="#D8ED6A" strokeOpacity=".85" strokeWidth="2"/>
        <path d="m250 191 126 80M278 173l126 80M218 210l126 81M250 229l122-79M282 250l121-78M312 272l123-79" stroke="#9BB0A2" strokeOpacity=".62" strokeWidth="1.4"/>
        <path d="M141 272 310 165l169 107" stroke="#87967E" strokeWidth="3"/>
        <path d="M163 288h101v125H163V288Z" fill="#F1F0DB"/>
        <path d="M178 302h70v111h-70V302Z" fill="#D7E2CE"/>
        <path d="M212 302v111m-34-55h70" stroke="#A2AE9C" strokeWidth="3"/>
        <path d="M295 300h103v113H295V300Z" fill="url(#window)"/>
        <path d="M346 300v113m-51-57h103" stroke="#EDF0DC" strokeWidth="4"/>
        <path d="M141 413h339" stroke="#85937C" strokeWidth="3"/>
        <path d="M89 417h402" stroke="#D8ED6A" strokeOpacity=".5" strokeWidth="2" strokeLinecap="round"/>
        <path d="m113 209 11-7m13-8 10-7m13-8 10-6m22-14 10-7m13-8 10-7" stroke="#D8ED6A" strokeWidth="2" strokeLinecap="round" opacity=".7"/>
      </svg>
    </div>
  );
}

export default function HomePage() {
  return (
    <>
      <section className="hero">
        <Container className="hero-inner">
          <div className="hero-copy">
            <span className="eyebrow"><i />Energy choices, made clearer</span>
            <h1>Make room for a <span>brighter</span> way forward.</h1>
            <p>Thoughtful solar, battery and backup power options for homes and businesses in and around Tanuku.</p>
            <div className="hero-actions">
              <Link className="button button-primary" href="/contact/">Talk through your needs <ArrowRight /></Link>
              <Link className="button button-outline" href="/services/">Explore services</Link>
            </div>
            <div className="hero-note">Local conversations in {company.location}</div>
          </div>
          <div className="hero-art">
            <div className="hero-orbit" aria-hidden="true" />
            <SolarIllustration />
            <div className="floating-note">
              <span className="floating-note-mark"><SunIcon /></span>
              <span><strong>Start with your needs</strong><small>Every conversation is different</small></span>
            </div>
          </div>
        </Container>
      </section>

      <section className="intro-strip">
        <Container className="intro-strip-inner">
          <p>From solar panels and batteries to inverters and UPS, we help you explore the options that fit your requirements.</p>
          <span className="location-tag"><SunIcon /> Tanuku, Andhra Pradesh</span>
        </Container>
      </section>

      <section className="section">
        <Container>
          <div className="section-heading">
            <div><span className="eyebrow"><i />What we can help with</span><h2>Power options for the way you live and work.</h2></div>
            <p>Begin with a conversation about your property and priorities. We can help you understand which products may suit your setup.</p>
          </div>
          <div className="service-grid">
            {services.slice(0, 3).map((service) => <ServiceCard key={service.number} {...service} />)}
          </div>
          <div style={{ marginTop: 25 }}><Link className="text-link" href="/services/">See all services <ArrowUpRight /></Link></div>
        </Container>
      </section>

      <section className="section process-section">
        <Container>
          <div className="section-heading">
            <div><span className="eyebrow"><i />A clear place to start</span><h2>Good decisions begin with good questions.</h2></div>
            <p>We keep the first steps straightforward, so you can make an informed choice at your own pace.</p>
          </div>
          <div className="process-grid">
            {processSteps.map((step) => <article className="process-step" key={step.number}>
              <div className="process-step-head"><span className="process-number">{step.number}</span></div>
              <h3>{step.title}</h3><p>{step.description}</p>
            </article>)}
          </div>
        </Container>
      </section>

      <section className="quality-band">
        <Container className="quality-band-inner">
          <div><span className="eyebrow"><i />The details matter</span><h2>Careful choices. Clear communication. Considered work.</h2><p>We take time to understand the requirement, explain the available options and plan the next step together.</p><div style={{ marginTop: 24 }}><Link className="button button-outline" href="/quality/">Our approach to quality <ArrowRight /></Link></div></div>
          <ul className="quality-list"><li>Understand the site and requirement <span>01</span></li><li>Discuss compatible options <span>02</span></li><li>Plan the work and next steps <span>03</span></li><li>Review details before completion <span>04</span></li></ul>
        </Container>
      </section>

      <section className="section">
        <Container>
          <div className="section-heading"><div><span className="eyebrow"><i />Our Work</span><h2>Real projects, shared with care.</h2></div><p>We are preparing this space for project stories that have been verified and approved to share.</p></div>
          <div className="work-preview">
            <span className="work-preview-mark"><SunIcon /></span>
            <div><span className="work-label">Project portfolio</span><h3>Stories are being prepared</h3><p>We’ll add project details here when verified information and permission to share are available.</p></div>
            <Link className="text-link" href="/our-work/">Visit Our Work <ArrowUpRight /></Link>
          </div>
        </Container>
      </section>

      <section className="cta-band">
        <Container className="cta-inner"><div><span className="eyebrow"><i />Let’s talk</span><h2>Tell us what you’re looking to power.</h2></div><Link className="button button-dark" href="/contact/">Get in touch <ArrowRight /></Link></Container>
      </section>
    </>
  );
}
