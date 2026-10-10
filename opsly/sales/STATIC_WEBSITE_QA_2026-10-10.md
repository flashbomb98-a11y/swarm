# Opsly — QA-Nachweis für einseitige Firmenwebseiten

**Prüfdatum:** 10.10.2026. **Gegenstand:** fiktives RAUMGRÜN-Muster und darauf aufbauender Auslieferungsprozess, **kein Kundenauftrag und keine Live-Kundenseite**.

## Welche Dateien wirklich geprüft wurden
- **Strukturprüfung** direkt auf der Repository-Fassung [raumgruen/index.html](../demo-webseiten/raumgruen/index.html), Git-Blob-SHA `6e83004ecb54d2674da3b4ecebba71cb6a61e357`, 28.472 Zeichen.
- **Interaktive Chromium-Tests** auf der früher exportierten und lokal gemounteten Musterdatei `/mnt/data/opsly-webseiten-muster/index.html` (28.586 Bytes). Diese Testkopie ist **nicht bytegleich** der GitHub-Fassung; daher ersetzen die Interaktionstests keinen abschließenden Test auf dem späteren Kundenartefakt.
- Keine neue Datenbank, kein Hosting oder Browser-Orchestrator eingerichtet. **Division Swarm** bleibt unverändert die Opsly-Laufzeit und der Buyer-Intent-Orchestrator.

## Prüfungen und tatsächliche Ergebnisse

| Prüfung | Ergebnis | Ausführung |
|---|---|---|
| Responsives Layout bei **1440 × 900**, **768 × 1024**, **390 × 844**, **320 × 568** | **OK**: Dokumentbreite entsprach jeweils dem Viewport, kein horizontales Dokument-Scrolling | Headless Chromium über Playwright, lokale HTML-Kopie via `page.set_content` |
| JavaScript-Konsole | **OK**: keine `pageerror`-Ausnahmen in den vier getesteten Viewports | Headless Chromium |
| Mobiles Menü auf 390 px | **OK**: `aria-expanded` wechselt `false → true`; sichtbarer Link; nach Klick `false` | Echtes Click-Event im Browser |
| Fiktives Anfrageformular | **OK als Demo**: ausgefüllte Testwerte erschienen in lokalem Vorschaudialog; kein Versand | Browserausführung |
| Escape-Taste im Dialog | **OK**: Vorschau schließt | Browserausführung |
| Interne Navigationslinks in der GitHub-Datei | **OK**: alle 9 `href="#..."`-Verweise besitzen passendes `id` | Statische Kontrolle an GitHub-Blob |
| Externe Asset-Abhängigkeiten | **Keine** externen Skript- und Stylesheet-Links in der GitHub-Fassung; eine Inline-CSS-/eine Inline-JS-Sektion, SVG-Grafiken | Statische Kontrolle |
| Formular-Sicherheit und Ehrlichkeit | **Kein echtes Anfrage-Backend**: Formular besitzt keine `action`, JavaScript verhindert `submit`, Demo-Hinweis sagt ausdrücklich: lokale Vorschau, kein Versand | GitHub-Fassung |
| Kleine optische Details auf 320 px | Bei zwei verschachtelten SVG-Elementen reichten Bounding-Boxes etwa 8 px rechts über den Rand, **ohne** horizontale Dokumentüberbreite. Vor Kundenübergabe visuell erneut prüfen | Headless Chromium |

**Nicht nachgewiesen:** öffentliche Demo ohne Drittanbieter-Interstitial, tatsächlicher E-Mail-Versand, Hosting, CMS, E-Commerce, Zahlungen, Suchmaschinenranking, vollständiger WCAG-Audit, Screenreader-Test, alle Browser-Engines oder Kunden-Abnahme.

## Verbindlicher Ablauf für jeden zukünftigen bezahlten Auftrag

1. **Kauf/Beauftragung tatsächlich verifizieren** (bei Upwork im Contract/Project-Catalog-Workroom; bei Direktkunden gesonderter schriftlicher Auftrag und vereinbarte Zahlung). Keine Produktion auf Basis einer bloßen DM.
2. **Scope bestätigen:** eine statische responsive Seite, bei Upwork maximal fünf Abschnitte und eine Revision, Kundentexte und Rechte nachweislich geklärt. Besondere Wünsche nur mit neuer schriftlicher Leistungsdefinition.
3. **Fiktionsschutz:** RAUMGRÜN-Inhalte, Namen, nicht echt belegbare Behauptungen und Konzeptkennzeichnung nicht versehentlich in eine Kundenwebseite kopieren; alle Kundeninhalte sorgfältig ersetzen.
4. **Kontaktfunktion:** das RAUMGRÜN-Demoformular ist **kein** lieferfähiges Echtkontaktformular. Bei Standardpaket stattdessen **funktionierenden `mailto:`-Link** oder Link zur bereits bestehenden Kontaktseite des Kunden umsetzen. Ein serverseitiges Formular nur bei separat vereinbartem Umfang, geeigneter Datenschutzprüfung und erfolgreichem Sende-/Fehlertest.
5. **Technische QA:** Titel und Beschreibung, `lang`, viewport, semantische Hierarchie, Bildrechte/Alternativtexte, CTA-Ziele, interne Anker, Tastaturbedienung, Escape/Fokus, 320/390/768/1440 px, JS-Konsole, mobile Navigation, Ladeverhalten und defekte Links.
6. **Datenschutz und Rechtstexte:** ausschließlich vom Kunden freigegebene Angaben verwenden, keine juristischen Texte als fertig geprüft ausgeben.
7. **Übergabe:** vollständige HTML/CSS/JS-Dateien und kurze README mit Grenzen; wenn Hosting nicht beauftragt ist, **nicht** behaupten, die Webseite sei live. Vorschau zeigen, konsolidierte Korrekturrunde umsetzen.
8. **Zahlung:** bei Upwork nur im Upwork-Vertragsraum einreichen und bezahlen lassen; reale Zahlungseingänge gesondert prüfen und dokumentieren.

## Reproduzierbarkeit
Die lokale Interaktionsprüfung nutzte Python Playwright mit System-Chromium (`/usr/bin/chromium`), nicht den fehlenden Playwright-Download-Browser. Das lokale `file://` war in der Laufzeit administrativ blockiert, weshalb die isolierte selbstenthaltene HTML-Vorlage per `page.set_content(html)` geladen wurde. Browserläufe sind **keine** automatisierte Prüfung einer live gehosteten Seite.

## Vertriebsstatus im Moment dieser Prüfung
Approved-Upwork-Produkt **Visible**, **1** Dashboard-Aufruf im 30-Tage-Fenster, **0** Bestellungen und **0** Upwork-Kundengespräche. Reddit-Benachrichtigungen **0**, Reddit-Chat mit `u/Visual_Lake5512` zeigt weiterhin nur unsere eigene Nachricht. **Keine neuen Käuferantworten oder Umsätze nachgewiesen.**

Aktuelle Bestandslinks:
- Upwork-Paket: https://www.upwork.com/services/product/development-it-a-modern-responsive-one-page-website-for-your-small-business-2109015259874676124
- Akquise- und Kontaktprotokoll: [FIRST_CUSTOMER_DISTRIBUTION.md](FIRST_CUSTOMER_DISTRIBUTION.md)
- Beauftragungs- und Auslieferungsregeln: [FIRST_PAID_ORDER_PLAYBOOK.md](FIRST_PAID_ORDER_PLAYBOOK.md)
