export const company = {
  name: "Mitra Solar Enterprises",
  location: "Tanuku, Andhra Pradesh",
  phoneDisplay: "+91 84604 06769",
  phoneLink: "+918460406769",
  address:
    "Shop No 5, 30-1-1/3, Near Surya Residency, Mukkamaala Vaari Street, Velpur Road, Tanuku - 534211, Andhra Pradesh",
} as const;

export const services = [
  {
    number: "01",
    title: "Solar panel systems",
    description:
      "Explore solar panel options for your home or business, with a conversation shaped around your site and energy needs.",
    category: "Solar",
  },
  {
    number: "02",
    title: "Solar inverters",
    description:
      "Find an inverter solution designed to work with the panels, battery needs and electrical setup you have in mind.",
    category: "Solar",
  },
  {
    number: "03",
    title: "Solar batteries",
    description:
      "Discuss storage options and how a battery may fit into your solar energy plans.",
    category: "Storage",
  },
  {
    number: "04",
    title: "Home inverters & UPS",
    description:
      "Compare home inverter and UPS options for everyday backup requirements.",
    category: "Backup power",
  },
  {
    number: "05",
    title: "Inverter batteries",
    description:
      "Get help considering battery options for a new or existing inverter setup.",
    category: "Storage",
  },
  {
    number: "06",
    title: "Automotive & industrial batteries",
    description:
      "Talk through battery requirements for automotive and industrial applications.",
    category: "Batteries",
  },
] as const;

export const processSteps = [
  {
    number: "01",
    title: "Tell us what you need",
    description: "Share a little about your property, priorities and energy use.",
  },
  {
    number: "02",
    title: "Discuss the options",
    description: "Review suitable products and the details that affect your setup.",
  },
  {
    number: "03",
    title: "Plan the next step",
    description: "Agree on the right way forward for your home or business.",
  },
] as const;
