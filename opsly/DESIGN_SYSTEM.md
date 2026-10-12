# Opsly · Verbindliches Designsystem (Version 1.0)

**Stand:** 12.10.2026. **Referenz:** die vom Nutzer bevorzugte dunkle, klare Opsly-Optik mit zusammenpassendem Lime-Akzent und ruhigen Karten. Diese Seite ist die **einzige Quelle** für öffentliche Farben, Gestaltungsregeln, Markenname und Sprache. Kein neues visuelles Sub-Branding pro Produktlinie.

## 1 · Unveränderliche Identität

- **Dachmarke auf allen öffentlichen Flächen: Opsly**, exakt O-p-s-l-y, ohne Co, Shop, Extras oder Schreibfehler. „OplsyCo“ im Live-Stripe-Checkout ist ein nachgewiesener BUG, keine alternative Marke.
- Produktlinien werden immer **Opsly Sales, Opsly Web Studio, Opsly Business, Opsly Tools, Opsly Visual, Opsly Audio, Opsly Lab** geschrieben.
- Bestehende technische IG/Pinterest-Handles `@opslyco` und `@opslyshop` sind KEINE Marketing-Namen; bis eine Profil-Umbenennung legitim möglich ist, sichtbaren Profil-/Anzeigenamen, Bio, Covers und Copy als **Opsly** ausgeben. Handle-Umbenennung nicht als erfolgt ausgeben, solange nicht überprüft.
- Für DACH-Webshop, DACH-Postings und deutschsprachigen Support: **Deutsch und „du“**, ruhig, klar, sachlich. Englisch nur für nachweislich internationale Käufer oder die bei internationalem Digitalmarkt notwendigen Produktbegriffe. Keine Mischung von Deutsch und Englisch innerhalb derselben Verkaufsseite ohne fachliche Begründung.
- Keine erfundenen Kundenlogos, Bewertungen, Testimonials oder Portfolio-Projekte. Fiktive Design-Mockups ausdrücklich so kennzeichnen.

## 2 · Verbindliche Farbwerte

| Zweck | HEX | Anwendungsregel |
|---|---|---|
| Haupt-Hintergrund | **`#111821`** | Vollflächiger dunkel-blaugrauer Ink-Ton |
| Karten/Navigation/Oberflächen | **`#25303C`** | Ruhige Schichtung vor dem Haupt-Hintergrund |
| Zwischenfläche/erhöhte Fläche | **`#1B262E`** | Sparsam für Hinweise und Sektionen |
| Rahmen/Trenner | **`#3C4A54`** | Dezent, nicht kontrastreicher als Inhalte |
| Primär-Akzent, Buttons, Highlight | **`#C8FF3D`** | Lime: höchstens ein dominanter CTA je Abschnitt |
| Haupttext | **`#F6F8F7`** | Headlines, Kernaussagen |
| Sekundärtext | **`#B9C6CA`** | Erläuterung, Preisdetails, Captions |
| Text auf Lime | **`#111821`** | Nie Weiß auf lime-grünen Buttons |

Verhältnis Lime/Ink ~15.15:1; Helltext/Karte ~12.57:1; Sekundärtext/Karte ~7.66:1, gemessen nach WCAG-Formel. Keine beliebigen violetten, roten oder türkisen Ersatz-Brandfarben. Statuswarnungen dürfen aus funktionalen Gründen abweichen; die sind nicht Teil des Brandings.

## 3 · Typografie und Layout
- Schriftstack: `Inter, ui-sans-serif, system-ui, -apple-system, "Segoe UI", sans-serif`; keine externen Pflicht-Webfonts. Sichtbar: kräftige Headlines 700–850, großzügiger Zeilenabstand im Fließtext, sauberes Letterspacing.
- Desktop max. Content-Breite **1120px**, mobil 20–24px Seitenabstand. Responsive 3/2/1-Karten-Grid.
- Primärbutton Lime, dunkle Schrift, Radius **12px** und Höhe min. **48px**; Sekundärbutton transparenter Ink-Rahmen. Fokus sichtbar mit Lime-Outline.
- Karten: Oberfläche `#25303C`, Rand `#3C4A54`, Radius **16px**; Innenabstand **20–24px**. Großzügige vertikale Abstände. Keine wilden Schatten, Glas-Effekte, überladene Farbverläufe oder animierte Pixel-Backgrounds auf Shopseiten.
- Brand-Signet: kleine limefarbene geometrische Markierung neben dem Schriftzug **Opsly** als konsistentes, ohne fremdes Unternehmenslogo verwendbares Wiedererkennungsmerkmal. Nicht auf fremde Plattform-UI (Stripe, Etsy, Instagram) als kontrollierbares UI-Element verlassen.
- Buttons/Links: eine klare Handlung je Karte (ansehen, anfragen oder kaufen). Nie eine „Jetzt kaufen“-Zusage, wenn Checkout-/Downloadpfad ungeprüft ist.
- Fotos/Mockups: dunkler ruhiger Hintergrund, ein Lime-Akzent, hochwertige typografische Hierarchie. Konkrete Verkaufsleistung im Motiv; keine Pseudo-Kundenreferenzen.

## 4 · Anwendungsorte / Kontrollliste

| Kanal | Stand / echte Lücke | Ausführung |
|---|---|---|
| Render Standby `opsly-standby-site.onrender.com` | Live, bisher nahe am Standard | CSS-Tokens exakt synchron halten; Etsy-Links und Kaufwege ohne Funktionsverlust |
| Floot Market `opsly-market.floot.app` | Live, Englisch und Web-Studio-lastig | Nach Build-Reset Hero/Karten in Deutsch, sieben Linien, exakt diese Farben, Shop-Preise; Checkout-Code/Dateien sicher prüfen |
| Stripe Checkout | LIVE-Checkout zeigt **OplsyCo** statt Opsly | Öffentlichen Händler-Anzeigenamen im berechtigten Stripe-Konto korrigieren; NICHT unberechtigt gesetzlichen Firmennamen ändern. Keine neue Stripe-Instanz |
| Etsy Opsly Business | Listingstatus wegen Etsy-Botblocker aktuell UNBEKANNT | Keine erzwungene Anmeldung; bestehende Cover/Vorlagen nach legitimer Etsy-Freigabe in Opsly-Palette angleichen, keine funktionalen XLSX-Stile blind überschreiben |
| Upwork Onepage-Service | Freigegeben, 9 Ansichten, 0 Orders | Haupt-Brand Opsly, gleiche Angebotssprache, Preis, Mockup und Lieferumfang; Profiländerungen nur bei berechtigtem Zugang |
| Instagram `@opslyco` | Veröffentlichte/scheduled Opsly Web Studio Posts deutsch; technischer Handle alt | Sichtbarer Profilname/Bio/Medienstandard Opsly, Farbschema dieser Tabelle; Username separat bei Plattform |
| Pinterest `@opslyshop` | Ein Beitrag geplant; technischer Handle alt | Anzeigename/Bio/Pin-Design Opsly, gleiche Farben und Copy; Username nicht als geändert melden |
| AgentMail | `opsly-sales@agentmail.to`, `opsly-business@agentmail.to`, `opsly-visual@agentmail.to` | Einheitliche sichtbare Signatur **Opsly · [Linie]**, gleiche Website/Preis im Angebot; kein „OpslyCo“ |
| Lieferdateien & Dokumente | Visual/Lab repariert, Online-Dateien noch offen | Cover, README, Lizenz, Startbild einheitlich; die eigentliche Funktionsgrafik darf produktgerecht sein, aber Dachmarke korrekt |

## 5 · Freigabegates (streng)
Vor jeder **neuen** öffentlichen Änderung: (1) ausgeschriebene Marke exakt Opsly, (2) genannte Palette/Typografie/Layouts, (3) sieben Lanes korrekt wo relevant, (4) Preis/Leistung/Lieferzeit wie realer Shop, (5) Links und Checkout/Dateilieferung funktionsfähig und vertrauenswürdig, (6) Sprachregel, (7) keine erfundenen Erfolge. Bei Fehler: **nicht mehr posten oder neuen Vertrieb auf den mangelhaften Kaufpfad lenken**; zuerst beheben oder ehrlich als Anfrage statt Sofortkauf deklarieren.

## 6 · Wartung ohne Chaos
Kein Neustart des Shops, kein zweites Produktinventar, keine getrennten Logos/Schriftwelten. Änderung an Designwerten zuerst hier, anschließend gebündelt auf aktiven Oberflächen aktualisieren. Jeden aktuellen Live-Stand nach Änderungen kontrollieren. Keine neuen bezahlten Tools, Credits, Domainkäufe oder Werbeschaltungen ohne Freigabe.
