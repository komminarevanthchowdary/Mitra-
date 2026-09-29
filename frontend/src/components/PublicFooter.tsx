import Link from "next/link";
import { Brand } from "@/components/Brand";
import { Container } from "@/components/Container";
import { company } from "@/lib/content";

export function PublicFooter() {
  return (
    <footer className="site-footer">
      <Container>
        <div className="footer-main">
          <div className="footer-brand-block">
            <Brand />
            <p>Solar, storage and backup power conversations grounded in your needs.</p>
          </div>
          <div className="footer-links">
            <span className="footer-label">Explore</span>
            <Link href="/services/">Services</Link>
            <Link href="/our-work/">Our Work</Link>
            <Link href="/quality/">Quality</Link>
            <Link href="/contact/">Contact Us</Link>
          </div>
          <div className="footer-contact">
            <span className="footer-label">Visit or call</span>
            <a href={`tel:${company.phoneLink}`}>{company.phoneDisplay}</a>
            <p>{company.address}</p>
          </div>
        </div>
        <div className="footer-bottom">
          <span>© {new Date().getFullYear()} Mitra Solar Enterprises</span>
          <span>{company.location}</span>
        </div>
      </Container>
    </footer>
  );
}
