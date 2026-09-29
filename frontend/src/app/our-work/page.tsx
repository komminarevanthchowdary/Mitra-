import type { Metadata } from "next";
import { PageIntro } from "@/components/PageIntro";
import { Container } from "@/components/Container";
import { SunIcon } from "@/components/Icons";

export const metadata: Metadata = {
  title: "Our Work",
  description: "Project stories from Mitra Solar Enterprises in Tanuku and nearby areas.",
};

export default function OurWorkPage() {
  return <>
    <PageIntro eyebrow="Our Work" title="Thoughtful work, told with the details." description="This portfolio is being prepared. We’ll share project stories when the details are verified and approved for publication." />
    <section className="page-body"><Container>
      <div className="empty-work"><div><SunIcon /><h2>Project stories are on the way</h2><p>We are collecting project information and permissions before publishing examples. In the meantime, get in touch to discuss your own requirements.</p></div></div>
    </Container></section>
  </>;
}
