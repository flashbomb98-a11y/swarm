# Opsly — verbindliches Profilbild und Accountnamen (12.10.2026)

**Freigegebenes Muster:** dunkler Ink-Hintergrund, Lime-Raute, weißes „Opsly“. Die endgültige Quelle ist die vom Nutzer im Chat bestätigte quadratische Opsly-Logo-Grafik. **Das identische Bild** statt voneinander abweichender Logos verwenden. Gestaltungsregeln: [DESIGN_SYSTEM.md](DESIGN_SYSTEM.md).

## Zentral gespeicherte Bilddateien

Die quadratische Originalgrafik wurde aus dem bestätigten Design als echte Dateien erstellt und unverändert proportional skaliert. Alle Dateien liegen in der bestehenden persönlichen Opsly-Library:
- `/Opsly/Brand/Opsly_Profilbild_512.png`, Library-ID `libfile_0363295668188191ace3171b4c7ce930` (512 × 512, optimale Plattform-Quelle).
- `/Opsly/Brand/Opsly_Profilbild_256.png`, Library-ID `libfile_aff3a390cd088191856d9515d5d46ea8`.
- `/Opsly/Brand/Opsly_Profilbild_128.png`, Library-ID `libfile_86c951e4d92081919e6ad59832510fd6`.

Die 512er-Bilddatei wurde außerdem am 12.10.2026 über die **bereits verbundene Floot-Market-Plattform** hochgeladen. Öffentlicher Bildpfad (auf der Floot-Domain): `/_cdn/static/6b2c9875-6e45-4138-af88-c98ac2263499-Opsly_Profilbild_512.png`.
Floot Market-Projekt `909db142-453b-495b-9801-7b2a28ae3f14`: `iconUrl` wurde auf diese Asset-Datei gesetzt; **dieser Metadatenwechsel wird erst beim nächsten erfolgreichen Floot-Publish LIVE**. Vorher nicht als live oder global umbenannt ausgeben.

## Namen
- Sichtbare Dachmarke: exakt **Opsly**; nur bei spezifischem Support: „Opsly Sales“, „Opsly Business“, „Opsly Visual“ usw.
- Profilbild: **immer dieselbe Opsly-Grafik** (nicht für jede Produktsparte neu einfärben, keine fremden Schriftzüge).
- Account-Handle falls technisch möglich und freigegeben: `opsly` bevorzugt. Wenn dieser Handle vergeben ist, nur abgestimmte, möglichst einheitliche Alternative; NIEMALS behaupten, Umbenennung erledigt, bevor Plattform das bestätigt.
- Unternehmens-Kontaktemails technisch nicht umbenennen/löschen. Bestehende `opsly-sales@agentmail.to`, `opsly-business@agentmail.to`, `opsly-visual@agentmail.to` bleiben erreichbar, sichtbarer Anzeigename jeweils Opsly [Bereich].

## Fortschritt / Plattformfreigaben
| Ort | Öffentlich sichtbarer Name | Avatar | Status |
|---|---|---|---|
| Floot Opsly Market | Opsly Market / „Opsly“ | Gleiche Grafik hochgeladen; Projekt-`iconUrl` gesetzt | **Live-Publish noch prüfen**, Floot-Automation arbeitet seit 14:02 an priorisierten Shopfixes; nicht parallel am selben Code bauen |
| Render Standby | Opsly | Im Header bisher Opsly-Schriftmarke+Limezeichen; keine externe Profilfoto-Funktion | Live; Foto/Website-Favicon nur sinnvoll als zusätzliches eigenes Asset |
| Instagram | technischer Handle `@opslyco` | Änderung nicht verifiziert | Plattform-Profil-Editor nötig; Metricool kann Posts, aber keinen Profilfoto-/Handlewechsel |
| Pinterest | technischer Handle `@opslyshop` | Änderung nicht verifiziert | Plattform-Profil-Editor nötig; Metricool kann Posts, aber keinen Profilfoto-/Handlewechsel |
| Etsy Shop | Shop-Handle/Zugriff nicht verifiziert | Änderung nicht verifiziert | Etsy hat automatisierten Zugriff wegen ungewöhnlicher Aktivität blockiert; keine erneute automatisierte Login-/CAPTCHA-Umgehung. Anzeigenamen/Avatar erst mit legitimer Session ändern |
| Upwork | Benutzerkonto + Opsly Web Studio-Angebot | Änderung nicht verifiziert | Individuelle Upwork-Identitäts-/Profilregeln beachten. Nie persönliches Verifizierungsprofil als Unternehmen fälschen; Marke in Portfolio, Angeboten und ggf. Agenturprofil einsetzen |
| Stripe | Händleranzeige **„OplsyCo“** im Checkout nachweislich falsch | Änderung nicht verifiziert | Nur im autorisierten Stripe-Konto öffentlichen Anzeigenamen/Logo ändern, legale Firmendaten nur bei wahrheitsgemäßer Identität anpassen, kein neuer Checkout oder Account |
| Metricool | internes Brand-Label `opslyshop` | nicht die eigentliche IG-/Pinterest-Profilidentität | Label kann mit aktuell verbundenen Metricool-Tools nicht umbenannt werden; öffentliches Profil nicht durch internes Label verwechseln |

## Brand-Freigabe
Eine Plattform gilt **erst dann als einheitlich**, wenn (1) öffentlicher Anzeigename, (2) Profilbild, (3) Bio & Link, (4) Farben und Publikationen übereinstimmen, (5) Preise/Checkout plausibel sind, (6) Änderung dort live geprüft ist. Technische Handles werden als offen markiert, wenn die Plattform sie nicht freigibt.

**Geschäftsziel bleibt erster bezahlter Auftrag.** Für Style-/Avatar-Umbauten kein Floot-Tageskontingent aufbrauchen, das sichere Zahlungen/Auslieferung verdrängt. Keine bezahlten Upgrades, keine neuen Social-Accounts, keine Blockadeumgehung.


## Nachkontrolle 12.10.2026, nachmittags

- **Render Standby LIVE mit identischem Profilbild:** `opsly/standby-shop/index.html` wurde mit dem bereits genehmigten Opsly-Logo (128px aus originalem 512px-Avatar) im Seitenkopf und als Favicon versehen, Commit `a4fbdee490f0a5f889597d97741419a17fc8782f`. Der vorhandene Render-Service `srv-db6bkoqd0e5s73a4s22g` wurde EINMAL manuell aktualisiert (Deploy `dep-db6fju7lk1mc73d3bia0`, Status `live`). Externer GET ergab HTTP 200, sichtbares eingebettetes Markenavatar, sieben Opsly-Linien und sechs bestehende Etsy-Links. **Kein zweiter Dienst**.
- **Canva-Upload wirklich erfolgreich:** Exakt die genehmigte 512×512-Opsly-Grafik wurde als Canva-Medienasset `MAHXz9CTr7U` importiert, Name `Opsly – einheitliches Markenprofilbild 512`. Kein neues Canva-Abo oder Paid-Upgrade.
- **Metricool/Instagram-Pending-Post vom 15.10.2026:** Die alte helle Abbildung wurde durch ein neues dunkelblaues/limefarbenes Opsly-Web-Studio-Motiv ersetzt. Gespeicherter neuer Scheduled-Post-ID `394123318`, unveränderte UUID `-6061265053453366900`, weiterhin 10:00 Europe/Berlin, Bild `https://static.metricool.com/planner/202610/7220354-file-7936476088864345587.jpeg`. Text korrigiert: illustrative Markenillustration, keine Kundenreferenz. Preis 349 €, Kauf-URL und Lieferumfang unverändert.
- **Metricool/Pinterest-Pending-Pin vom 13.10.2026:** Die alte helle Grafik wurde durch dunkelblau/lime gestaltetes Opsly-Motiv ersetzt. Neuer Scheduled-ID `394123391`, UUID `2530073975614619770`, weiterhin 10:15 Europe/Berlin, Bild `https://static.metricool.com/planner/202610/7220354-file-2989432492091925101.jpeg`, Board `1141451536747632362` und Pin-Link `https://opsly-market.floot.app/#website-service` unverändert. Metricool-Nachprüfung bestätigte beide Medien und PENDING.
- **Instagram/Pinterest öffentliche Profil-Felder UNVERÄNDERT:** Technische Handles bleiben `@opslyco` und `@opslyshop`. Die aktuelle Metricool-Verbindung hat keinen Schreibzugriff auf Profilbild, Profilnamen, Bio oder Handle. Die Motive sind harmonisiert, NICHT die Accounts selber.
- **Upwork-Live-Kontoprüfung:** Das genehmigte Website-Angebot ist weiterhin online. Der Useraccount zeigt den verifizierten persönlichen Namen; es existiert kein Agenturprofil. Nicht den echten Personennamen/gesetzliche Identität heimlich durch „Opsly“ ersetzen. Opsly-Marke in Angebotsmaterialien verwenden. Öffentliche Profilbild-Änderung nicht belegt.
- **Stripe-Account-UI geprüft:** Das vorhandene Cloud-Browserprofil war NICHT bei Stripe angemeldet. Die zuvor live beobachtete falsche Händleranzeige `OplsyCo` lässt sich aus diesem Zugriff nicht legal korrigieren. Kein neuer Stripe-Account erstellt, keine fiktive Firmenidentität.
- **Kein Extern-Account als umbenannt oder mit Avatar aktualisiert zählen, solange der echte Plattform-Profilwechsel nicht verifiziert wurde.**
