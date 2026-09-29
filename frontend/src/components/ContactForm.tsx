"use client";

import { zodResolver } from "@hookform/resolvers/zod";
import { useState } from "react";
import { useForm } from "react-hook-form";
import { z } from "zod";
import { apiRequest } from "@/lib/api/client";

const enquirySchema = z.object({
  customer_name: z.string().trim().min(2, "Please enter your name.").max(120),
  mobile_number: z.string().trim().regex(/^[+\d][\d\s().-]{7,19}$/, "Enter a valid phone number."),
  email: z.union([z.literal(""), z.email("Enter a valid email address.").max(254)]).optional(),
  city: z.string().trim().min(2, "Please enter your city.").max(100),
  service_interest: z.string().min(1, "Choose a service area."),
  message: z.string().trim().min(10, "Please share a little more about your requirement.").max(2000),
  consent: z.boolean().refine((value) => value, { error: "Please confirm that we may contact you about this enquiry." }),
  website: z.string().max(200).optional(),
});

type EnquiryValues = z.infer<typeof enquirySchema>;

const serviceOptions = ["Solar panels", "Solar inverters", "Solar batteries", "Home inverters & UPS", "Inverter batteries", "Automotive or industrial batteries", "Not sure yet"];

export function ContactForm() {
  const [success, setSuccess] = useState(false);
  const { register, handleSubmit, reset, formState: { errors, isSubmitting } } = useForm<EnquiryValues>({
    resolver: zodResolver(enquirySchema),
    defaultValues: { customer_name: "", mobile_number: "", email: "", city: "", service_interest: "", message: "", consent: false, website: "" },
  });
  const [error, setError] = useState("");

  const submit = handleSubmit(async (values) => {
    setError("");
    setSuccess(false);
    try {
      await apiRequest<{ id: string }>("/contact", {
        method: "POST",
        body: JSON.stringify({ ...values, email: values.email || null }),
      });
      setSuccess(true);
      reset();
    } catch (caught) {
      setError(caught instanceof Error ? caught.message : "Your enquiry could not be sent. Please call us instead.");
    }
  });

  return <form className="contact-form" onSubmit={submit} noValidate>
    <h2>Send an enquiry</h2><p>We’ll use these details to respond to your request.</p>
    <div className="honeypot" aria-hidden="true"><label htmlFor="website">Leave this field empty</label><input id="website" tabIndex={-1} autoComplete="off" {...register("website")} /></div>
    <div className="form-grid">
      <div className="form-field"><label htmlFor="customer_name">Your name</label><input id="customer_name" autoComplete="name" placeholder="Name" {...register("customer_name")} />{errors.customer_name && <span className="field-error">{errors.customer_name.message}</span>}</div>
      <div className="form-field"><label htmlFor="mobile_number">Phone number</label><input id="mobile_number" type="tel" autoComplete="tel" placeholder="+91" {...register("mobile_number")} />{errors.mobile_number && <span className="field-error">{errors.mobile_number.message}</span>}</div>
      <div className="form-field"><label htmlFor="email">Email <span style={{ color: "#8b9790", fontWeight: 400 }}>(optional)</span></label><input id="email" type="email" autoComplete="email" placeholder="you@example.com" {...register("email")} />{errors.email && <span className="field-error">{errors.email.message}</span>}</div>
      <div className="form-field"><label htmlFor="city">City or town</label><input id="city" autoComplete="address-level2" placeholder="Your location" {...register("city")} />{errors.city && <span className="field-error">{errors.city.message}</span>}</div>
      <div className="form-field form-field-full"><label htmlFor="service_interest">What are you interested in?</label><select id="service_interest" {...register("service_interest")}><option value="">Choose an area</option>{serviceOptions.map((option) => <option key={option} value={option}>{option}</option>)}</select>{errors.service_interest && <span className="field-error">{errors.service_interest.message}</span>}</div>
      <div className="form-field form-field-full"><label htmlFor="message">Tell us a little more</label><textarea id="message" placeholder="What would you like help with?" {...register("message")} />{errors.message && <span className="field-error">{errors.message.message}</span>}</div>
    </div>
    <label className="form-consent"><input type="checkbox" {...register("consent")} /><span>I agree that Mitra Solar Enterprises may contact me about this enquiry. My details will be used to respond to this request.</span></label>
    {errors.consent && <span className="field-error">{errors.consent.message}</span>}
    {error && <p className="form-error" role="alert">{error}</p>}
    {success && <p className="form-success" role="status">Your enquiry has been received. Thank you for getting in touch.</p>}
    <button className="button button-dark form-submit" type="submit" disabled={isSubmitting}>{isSubmitting ? "Sending…" : "Send enquiry"}</button>
    <p className="form-fine-print">Please don’t include payment details or sensitive personal information.</p>
  </form>;
}
