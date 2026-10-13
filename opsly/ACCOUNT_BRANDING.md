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

## Kontozugang-Prüfung am 12.10.2026, 20 Uhr
- Erneute READ-ONLY-Prüfung mit einem bereits vorhandenen gespeicherten Skyvern-Cloud-Browserprofil `bp_581979519349392896`, Workflow `wpid_584739309976735672` am 12.10.2026 ab 20:07 Europe/Berlin.
- Instagram `https://www.instagram.com/accounts/edit/`: Seite fordert LOGIN, `logged_in:false`, weder Edit Profile noch Avatarsteuerung sichtbar. Öffentliche technische Identität aus Metricool weiter `opslyco`. Kein automatischer Profilbild-/Name-Edit erlaubt oder bestätigt.
- Pinterest `https://www.pinterest.com/settings/edit-profile/`: öffentliche Willkommens-/Loginseite, `logged_in:false`, kein angemeldetes Konto oder Edit Profile sichtbar. Technischer Pinterest-Handle aus Metricool `opslyshop`. Kein Profilbild-/Name-Edit erlaubt oder bestätigt.
- Bereits aus früherer Prüfung: Etsy-Cloud-Login blockiert durch Sicherheitskontrolle; Upwork ist ein persönliches verifiziertes Nutzerkonto, nicht als Firmenkonto ausgeben; Stripe im bestehenden Cloud-Browserprofil nicht eingeloggt, Checkout-Merchant-Name weiterhin `OplsyCo`.
- **Konsequenz:** Beiden Profilen fehlt EINMALIGE berechtigte Kontoanmeldung in einer für den Agenten dauerhaft nutzbaren Sitzung; es wurde keine 2FA/CAPTCHA-Umgehung versucht. Die bereits geplanten Instagram/Pinterest-Motive sind visuell auf Opsly vereinheitlicht, aber NICHT die Profilseiten. Die Profiländerung hat deshalb bis zum menschlich freigegebenen Login den Status BLOCKIERT. Keine neuen Konten oder verzerrte Erfolgsberichte.
- Neue Nacht-Arbeitsautomation ist an zwei flexible Tageszeiten ca. 01:00/04:00 Europe/Berlin gebunden, zusätzlich zu anderen bereits aktiven Opsly-Vertriebs- und Sicherheitskontrollen. Nicht als dauerhafter ununterbrochener Prozess darstellen.


## Pinterest-/Instagram-Altbestand und neue Freigaben – 12.10.2026 ca. 20:30 Berlin

- Nutzer hat bestätigt, die NEUEN identischen Opsly-Profilbilder **selbst auf Instagram und Pinterest hochgeladen**. Dies als Nutzerbestätigung behandeln; der öffentliche Avatar konnte nicht unabhängig über API verifiziert werden. Alte technische Handles @opslyco / @opslyshop sind nicht als geändert bestätigt; Metricool-internes Markenlabel weiter opslyshop.
- Metricool Inventur am 12.10.2026: **13 bereits veröffentlichte Pinterest-Pins**, **6 bereits veröffentlichte Instagram-Beiträge**, je ein schon zuvor bestehender geplanter Pinterest-Pin 13.10. und geplanter IG-Post 15.10., beide im neuen Dunkel-Lime-Opsly-Design. Alte Pinterest-Pins sind übergewichtet mit Lager-/Excel-Vorlagen; mehrere Titel/Links zeigen noch `https://www.etsy.com/shop/OpslyCo`; alter IG-Reorder-Beitrag 05.10. nennt im Text `Etsy-Shop OpslyCo`. Nicht behaupten, dass diese alten veröffentlichten Einträge bereits geändert wurden.
- Laut offizieller Pinterest-Hilfe https://help.pinterest.com/en-gb/article/edit-or-delete-a-pin **kann der Medieninhalt nach Veröffentlichung NICHT ausgetauscht werden**, nur bestimmte Metadaten wie Titel, Beschreibung, Link und Board; für das neue Foto ein neuer Pin erforderlich, alte Pins nur über Pinterest selbst editieren/archivieren/löschen.
- Direktzugriff-Lage: Metricool bietet nur `getScheduledPosts` und `updateScheduledPost` für NOCH GEPLANTE Beiträge; keine Aktion für bereits veröffentlichte Bilder/Pin-Metadaten oder native Pinterest-Archivierung. Verfügbarer Skyvern-Browser aus älterem Profil war bei Pinterest/Instagram nicht angemeldet; der Benutzer-Login im lokalen Browser ist NICHT automatisch an dieses Tool verbunden. Opera-Browser-Connector meldet 'not connected', Remote Desktop Commander keine Geräte. **Keine unbefugten Logins, keine CAPTCHA-Umgehung, keine stillschweigend behaupteten Profiländerungen.**
- **NEUER geprüfter Pinterest-Kreativsatz:** sieben konkrete dunkle Opsly-Pinbilder (1000×1500), einheitlicher echter Markenavatar, #111821/#25303C/#C8FF3D, thematisch Lager-KPIs, Inventory Aging, Excess/No Demand, Reorder-Planner, Seller Margin Lab, B2B Fit-Check und Audio UI Alerts. Im Gespräch generierte Dateien als ZIP `/mnt/data/Opsly_Pinterest_Markenserie_2026-10.zip`, visuelles Vorschaublatt `/mnt/data/opsly_pinterest_preview.jpg`. Diese sind Gesprächs-Artefakte, **keine** automatische Live-Veröffentlichung aller sieben Motive; die verbleibenden fünf sind für zulässige spätere Ersetzungen verfügbar.
- **Tatsächlich NEU geplant und von Metricool als PENDING bestätigt:**
  - 16.10.2026 10:15 Europe/Berlin: **Opsly Tools – Margin Lab 6,90 €**, neue Bilddatei im einheitlichen Dark/Lime-Design, Metricool ID `394269740`, UUID `8665871943231817169`, Link https://opsly-market.floot.app/#direct-products.
  - 18.10.2026 10:15 Europe/Berlin: **Opsly Business – 3 Lager-KPIs**, einheitliche Grafik, Metricool ID `394269766`, UUID `3189852285208053424`, Link https://opsly-standby-site.onrender.com/#downloads.
- Beim dritten Medienupload meldete Floot das erreichte Tageslimit 100 Aktionen (Reset 13.10.2026 12:00 UTC); keinen endlosen Retry. Zwei vorhandene Bilder wurden zuvor als ÖFFENTLICHE Social-Media-Grafiken erfolgreich hochgeladen (keine privaten digitalen Produkt-ZIPs); der alte Security-Fall der öffentlich hochgeladenen Verkaufs-ZIP darf nie wieder passieren.
- **Freigaberegel:** Keine Serie von 13 Duplikatpins massenhaft neu posten. Erst bestehenden Pinterest-Zugang legitim verbinden, dann alte Bilder nach angemessener Abwägung archivieren/entfernen oder die Bilder als Historie belassen, problematische alten OpslyCo-Links/Texte editieren. Deletion ist irreversibel. Neue Pins mit korrekter Warenverfügbarkeit und geprüften Links nur zeitlich gestaffelt; bestehende 13.10., 16.10., 18.10. Pinntermine nicht doppeln.

## Social-Status 13.10.2026 – erste neue Marke veröffentlicht

- **Pinterest Web Studio 13.10. um 10:15 Europe/Berlin**: Metricool Post ID `394123391` (UUID `2530073975614619770`) liefert Status **PUBLISHED** nach Live-Recheck am 13.10. um 10:16. Gleiches Dark/Lime Opsly-Web-Studio-Motiv und korrektes Linkziel `https://opsly-market.floot.app/#website-service`; 349 EUR, fünf Abschnitte, eine Korrekturrunde. Publikation im Metricool-Konto bestätigt; kein unabhängiges externes Pinterest-Analytics-/Klicksignal behaupten.
- **Noch geplant, nicht erneut erstellen:** Instagram 15.10. 10:00 (`394123318`); Pinterest Tools 16.10. 10:15 (`394269740`); Pinterest Business 18.10. 10:15 (`394269766`).
- **Noch offen:** 13 alte Pinterest-Pins mit alten Bildern, fünf Links zu `OpslyCo`; bereits veröffentlichte Bilder nicht durch Metricool austauschbar. Kein unberechtigter Pinterest-Login oder Massenlöschen. Profilbilder IG/Pinterest vom Nutzer selbst als gewechselt gemeldet.
- **Vertriebssignal:** Auch ein veröffentlichter Post ist noch kein Kunde oder bezahlter Auftrag; Pinterest-Außenklicks weiterhin nicht neu bestätigt.
