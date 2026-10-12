# Opsly Produkt-QA und Auslieferungsfreigabe – 12.10.2026

**Status: Produkt-Quelldateien in persönlicher Opsly-Library korrigiert; LIVE-SHOP-DOWNLOADS NOCH NICHT aktualisiert.** Das Floot-Kontingent ist bis 12.10.2026 12:00 UTC blockiert. Vor Verkaufsauslieferung die neuen ZIPs mit den alten Floot-Private-Produktdateien tauschen und bezahlte Download-Ausgabe ohne echte Zahlung testen.

## Visual – OBS Overlay
- Library-Pfad: `/Opsly/RevenueProducts/Opsly_Visual_Neon_Grid_Stream_Overlay_v1.zip`
- Library-ID: `libfile_a1d8a99f0fcc81919200c9b6d034a143`
- ZIP-SHA256: `890a4f6c1076e06f9a5b2e0462842f3ffd33cd6b96ab28bfa28b4f9f21004c71`
- Root cause: `04_GAMEPLAY.html` hatte `.scene` mit undurchsichtigem CSS-Gradienten. In OBS als Overlay über einem Game Capture konnte dies das Spiel verdecken.
- Fix: Gameplay `class="scene gameplay"`, CSS `.scene.gameplay{background:transparent}`, Raster ausblenden, andere Szenen bleiben dunkel. Markenakzent `#C8FF3D`. ZIP entpackt und alle sechs Einträge auf Integrität geprüft; CSS/HTML-Selektoren geprüft. **Visueller Browser-Run im Container verweigert (ERR_BLOCKED_BY_ADMINISTRATOR)**; nicht als Echt-OBS-Integrationstest ausgeben.
- Live-Aufgabe: Ersatzdatei aus Library beziehen, Floot-Asset in private Produkte hochladen, zugehörigen Download-Pfad synchronisieren, Checkout/Entitlement und OBS-Praxischeck prüfen, dann erst live als repariert bewerben.

## Lab – TTRPG Campaign Continuity Console
- Library-Pfad: `/Opsly/RevenueProducts/Opsly_Lab_TTRPG_Campaign_Continuity_Console_v1.zip`
- Library-ID: `libfile_59d942ac5a0c81919ea3c057a76f1cb8`
- ZIP-SHA256: `981d61f304640d9c77389fcaad32ff3badad7f93b3c6ac73bf34b2b5fb2ab4b1`
- Root cause: Eingefügtes JSON wurde ungeprüft zum gespeicherten `db`; beim anschließenden Rendern konnten falsche Datentypen das Tool lahmlegen und Daten überschreiben. Fehlerhaftes `localStorage`-JSON verhinderte den Start. Export-Object-URL wurde unmittelbar vor dem Download freigegeben.
- Fix: validiert fünf Kategorien und jeweils vier Textfelder, lehnt fehlerhafte Imports ohne Mutation ab, hat abgesicherte Lade-/Speichervorgänge, spätere Freigabe der Export-URL. `node --check` ist bestanden. ZIP-Integrität bestanden. Browser-E2E-Test wurde von Testumgebung gesperrt; bleibt offen.
- Live-Aufgabe: Ersatzdatei aus Library beziehen, Floot-Private-Download zuordnen, Browserimport/-export und Kaufdownload prüfen, bevor live als repariert ausgeben.

**Hinweise:** Library wurde am 12.10.2026 durch Upload-Overwrite erfolgreich aktualisiert (nicht nur lokale ZIPs erstellt). Keine Kundenbestellungen oder Umsatz durch diese Aktion. Neue Artikel NICHT anlegen, erst bestehende lieferfähig machen. 

## Einheitsdesign nach Nutzerreferenz – neue finale Library-Version 12.10.2026
- **Dies sind die NEUEN gültigen SHA256-Werte oben.** Die beiden ZIPs wurden nach der ursprünglichen Sicherheitsreparatur als echte Produktdateien erneut gestaltet und unter **denselben bestehenden Library-IDs** überschrieben; alte SHA256 und zuvor erstellte ZIP-Kopien NICHT mehr zum Floot-Asset hochladen. Quelle: `opsly/DESIGN_SYSTEM.md`.
- **Visual:** `style.css` in Dark Ink `#111821`, Slate `#25303C`, Rand `#3C4A54`, Lime `#C8FF3D`, Helltext `#F6F8F7`, Muted `#B9C6CA`. OBS-Gameplay weiterhin transparent und Raster für Gameplay ausgeblendet. Vier Overlay-Szenen/Dateinamen unverändert. Alle Farbwerte im Code geprüft.
- **Lab:** Vollständige Benutzeroberfläche von Brown/Gold/Georgia auf dieselbe Opsly-Farbpalette, einheitliche Cards (16px), Lime-Buttons und System/Inter-Typografie umgestellt. **Datenspeicherung, Import-Validierung, Exportlogik, die fünf Datenkategorien und IDs wurden NICHT verändert**. Script nach Stiländerung mit `node --check` geprüft; ZIP-Integrität bestanden; sieben HEX-Werte passen Designstandard. Browser-Interaktion / OBS-Echt-Test noch **nicht** bestätigt.
- **WICHTIG:** Diese neuen Library-Versionen sind **noch nicht** die Floot-LIVE-Auslieferung. Nach Aktionsquota-Reset die jeweils aktuellen Library-ZIPs mit obigen Checksummen ins geschützte Floot-Asset-/Downloadsystem übertragen, Titel/Preis/Anleitungen synchronisieren, Zahlstatus und private Lieferung prüfen, einmal veröffentlichen. Bloß die Repo-/Library-Korrektur ist keine erfolgte Live-Shop-Reparatur.
