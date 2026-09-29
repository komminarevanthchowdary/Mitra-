import { Container } from "@/components/Container";

export function PageIntro({
  eyebrow,
  title,
  description,
}: {
  eyebrow: string;
  title: string;
  description: string;
}) {
  return (
    <section className="page-intro">
      <Container>
        <span className="eyebrow"><i />{eyebrow}</span>
        <h1>{title}</h1>
        <p>{description}</p>
      </Container>
    </section>
  );
}
