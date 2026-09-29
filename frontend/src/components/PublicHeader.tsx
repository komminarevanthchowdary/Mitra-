"use client";

import Link from "next/link";
import { usePathname } from "next/navigation";
import { useState } from "react";
import { Brand } from "@/components/Brand";
import { Container } from "@/components/Container";
import { ArrowUpRight } from "@/components/Icons";

const links = [
  { href: "/services/", label: "Services" },
  { href: "/our-work/", label: "Our Work" },
  { href: "/quality/", label: "Quality" },
  { href: "/contact/", label: "Contact" },
];

export function PublicHeader() {
  const pathname = usePathname();
  const [open, setOpen] = useState(false);

  return (
    <header className="site-header">
      <Container className="header-inner">
        <Brand />
        <button
          type="button"
          className="menu-toggle"
          aria-expanded={open}
          aria-controls="primary-navigation"
          aria-label={open ? "Close navigation menu" : "Open navigation menu"}
          onClick={() => setOpen((value) => !value)}
        >
          <span /><span />
        </button>
        <nav id="primary-navigation" className={`primary-nav ${open ? "is-open" : ""}`} aria-label="Primary navigation">
          {links.map((link) => (
            <Link
              key={link.href}
              href={link.href}
              aria-current={pathname === link.href || `${pathname}/` === link.href ? "page" : undefined}
              onClick={() => setOpen(false)}
            >
              {link.label}
            </Link>
          ))}
          <Link className="nav-login" href="/login/" onClick={() => setOpen(false)}>
            Portal login <ArrowUpRight />
          </Link>
        </nav>
      </Container>
    </header>
  );
}
