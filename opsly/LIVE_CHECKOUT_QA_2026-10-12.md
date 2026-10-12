# Opsly — Live Checkout (ohne Zahlung) 12.10.2026

Quelle: öffentliche Produktionsseite https://opsly-market.floot.app/ . Der Test fand in einem echten Browser am 12.10.2026 nach 13:00 Europe/Berlin statt. **Keine Kreditkarten-/Kundendaten eingegeben, keine Zahlung ausgelöst**, keine echten Bestellungen erstellt.

## Belegbare Ergebnisse
1. HTML-Seite lädt mit HTTP 200; sichtbare acht Verkaufsbuttons: Web Studio, Sales 5er/100er/20er, Audio, Visual, Tools, Lab. Die Oberfläche ist englisch, was bei DACH-Kunden Reibung erzeugt.
2. Klick auf den fünften Button (Audio) **hat eine echte Stripe-hosted Checkout-Session** unter `https://checkout.stripe.com/c/pay/cs_live_...` geöffnet. Produkt `Opsly Audio — Neon UI Alerts`, Preis **5,90 €** im Checkout. Browser/IP wurde von Stripe als USD-Region erkannt: automatischer Alternativpreis **$6.86** und Währungsumrechnung inkl. angegebener 4%-Gebühr (US-Browser nicht als Nachweis für deutsches Default-Währungsverhalten interpretieren). Stripe-Seite sagt Live Mode, Testdaten nicht erlaubt.
3. Klick auf den ersten Verkaufsbutton (Web Studio) hat eine neue echte Checkout-Session geöffnet. Produkt `Opsly Web Studio — One-Page Business Website`, Preis **349,00 €**. Bei US-Browser-Region als Standard **$405.81** mit EUR-Auswahl. Produktumfang und Excludes zeigen sachlich stimmig.
4. **Sichtbarer Markenfehler im Stripe-Checkout: Händlername und Seitentitel `OplsyCo` (Tippfehler), nicht Opsly.** Der Fehler kommt von den Stripe-Händler-/Public-Display-Einstellungen, nicht vom Produktnamen. Dringend in offiziellem Stripe-Konto unter Public Business Information/Business Name prüfen und auf Opsly abgleichen; Firmen-/rechtlichen Namen nicht ohne Grundlage überschreiben. Keine Stripe-Zugangsdaten im Repo.
5. Stripe Checkout startfähig != zahlungsfähiges Geschäftsmodell bewiesen. Ob Merchant vollständig verifiziert ist, Zahlungen ausgezahlt werden, Checkout-Webhook signiert ist, erfolgreiche Bestellung privates Download-Entitlement liefert, Payment failures abgefangen werden, Refunds sicher verarbeitet werden, wurde **NICHT** bestätigt. Keine falsche Umsatzmeldung.
6. Weitere Produkt-Stripe-Buttons wurden nicht einzeln geprüft; ob sie funktionieren bleibt unbestätigt.

## Unmittelbare Maßnahmen
- Checkout-Händleranzeige auf exakte Dachmarke **Opsly** korrigieren, zuerst Account-Konfiguration verifizieren; Tippfehler in Branding beseitigen. Dies kann einen Account-Eigentümer-Eingriff erfordern, sofern kein befugter Stripe-Connector.
- Nach Floot-Aktionsquota-Reset 12:00 UTC Floot-Code für `endpoints/checkout_POST.ts`, `endpoints/order_GET.ts`, `helpers/productCatalog.tsx`, `pages/_index.tsx` lesen; tatsächliche Auth/fulfillment-/Delivery-Logik prüfen, ohne echte Zahlung.
- Bestehende reparierte private ZIP-Dateien Visual und Lab aus Library ersetzen, nicht nur Produkttexte ändern.
- Hauptshop sichtbaren deutschen DACH-Marketingstandard verbessern, alle sieben Linien berücksichtigen, saubere CTA + Support-Möglichkeit.
- Keinen neuen Stripe-Account oder zweiten Checkout auf Render anlegen; Render Standby bleibt reine Kontaktseite. Keine Ausgaben/Live-Testbuchungen ohne ausdrückliche Genehmigung.

## Aktive Käufergewinnung
Am 12.10.2026 wurde eine individuelle Antwort auf die öffentlich ausgeschriebene Freelance/Remote B2B Lead Generation Stelle von VNMT Solutions versendet, an **careers@vnmtsolutions.com**, vom bekannten AgentMail `opsly-sales@agentmail.to`, Betreff `VNMT freelance lead generation opening — Opsly research pilot`, messageId `<010001a12fc6189c-1adc87f9-d95d-4cd7-972c-fa2e0b57cd54-000000@email.amazonses.com>`; originäre Stellenausschreibung: https://www.linkedin.com/posts/diya-jethwani-456389421_hiring-leadgeneration-b2b-activity-7511317674849898496-vYqY (01.10.2026). Das Unternehmen wurde anhand von vnmtsolutions.com und LinkedIn verifiziert; explizite Bewerbungs-E-Mail in der Originalanzeige. Angeboten wurde ein bezahlter kleiner research-only Pilot mit Klärung, ob externe Services statt individueller Outbound-Freelancer akzeptiert werden. **Gesendet, aber nicht angenommener Auftrag / keine Zahlung**. Keine zweite Mail ohne inhaltliche Antwort oder legitime spätere einmalige Nachfrage.
