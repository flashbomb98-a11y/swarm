# Opsly Produkt-QA und Auslieferungsfreigabe – 12.10.2026

**Status: Produkt-Quelldateien in persönlicher Opsly-Library korrigiert; LIVE-SHOP-DOWNLOADS NOCH NICHT aktualisiert.** Das Floot-Kontingent ist bis 12.10.2026 12:00 UTC blockiert. Vor Verkaufsauslieferung die neuen ZIPs mit den alten Floot-Private-Produktdateien tauschen und bezahlte Download-Ausgabe ohne echte Zahlung testen.

## Visual – OBS Overlay
- Library-Pfad: `/Opsly/RevenueProducts/Opsly_Visual_Neon_Grid_Stream_Overlay_v1.zip`
- Library-ID: `libfile_a1d8a99f0fcc81919200c9b6d034a143`
- ZIP-SHA256: `e7093647ce7da2b29f5e4e82e7e9eb12bf7611a8ec5cf15aa7b68f54446f6b61`
- Root cause: `04_GAMEPLAY.html` hatte `.scene` mit undurchsichtigem CSS-Gradienten. In OBS als Overlay über einem Game Capture konnte dies das Spiel verdecken.
- Fix: Gameplay `class="scene gameplay"`, CSS `.scene.gameplay{background:transparent}`, Raster ausblenden, andere Szenen bleiben dunkel. Markenakzent `#C8FF3D`. ZIP entpackt und alle sechs Einträge auf Integrität geprüft; CSS/HTML-Selektoren geprüft. **Visueller Browser-Run im Container verweigert (ERR_BLOCKED_BY_ADMINISTRATOR)**; nicht als Echt-OBS-Integrationstest ausgeben.
- Live-Aufgabe: Ersatzdatei aus Library beziehen, Floot-Asset in private Produkte hochladen, zugehörigen Download-Pfad synchronisieren, Checkout/Entitlement und OBS-Praxischeck prüfen, dann erst live als repariert bewerben.

## Lab – TTRPG Campaign Continuity Console
- Library-Pfad: `/Opsly/RevenueProducts/Opsly_Lab_TTRPG_Campaign_Continuity_Console_v1.zip`
- Library-ID: `libfile_59d942ac5a0c81919ea3c057a76f1cb8`
- ZIP-SHA256: `d1f7b6641882c3aa0691b09c349066c914a9398b52c88d44976fb2b31a233ab3`
- Root cause: Eingefügtes JSON wurde ungeprüft zum gespeicherten `db`; beim anschließenden Rendern konnten falsche Datentypen das Tool lahmlegen und Daten überschreiben. Fehlerhaftes `localStorage`-JSON verhinderte den Start. Export-Object-URL wurde unmittelbar vor dem Download freigegeben.
- Fix: validiert fünf Kategorien und jeweils vier Textfelder, lehnt fehlerhafte Imports ohne Mutation ab, hat abgesicherte Lade-/Speichervorgänge, spätere Freigabe der Export-URL. `node --check` ist bestanden. ZIP-Integrität bestanden. Browser-E2E-Test wurde von Testumgebung gesperrt; bleibt offen.
- Live-Aufgabe: Ersatzdatei aus Library beziehen, Floot-Private-Download zuordnen, Browserimport/-export und Kaufdownload prüfen, bevor live als repariert ausgeben.

**Hinweise:** Library wurde am 12.10.2026 durch Upload-Overwrite erfolgreich aktualisiert (nicht nur lokale ZIPs erstellt). Keine Kundenbestellungen oder Umsatz durch diese Aktion. Neue Artikel NICHT anlegen, erst bestehende lieferfähig machen. 
