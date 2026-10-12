# Opsly – unabhängige Standby-Verkaufsseite

## Zweck
Diese kostenlose, abgekoppelte, **statische** Seite ist eine Portabilitäts- und Kontakt-Reserve für den bestehenden Opsly Market. Sie ist **keine** vollwertige Zahlungsredundanz. Stand: 12.10.2026.

Quellcode: `opsly/standby-shop/index.html`. **Standby-Seite LIVE und überprüft seit 12.10.2026** unter https://opsly-standby-site.onrender.com/ (HTTP 200, alle sieben Produktlinien geprüft). Hauptshop weiterhin https://opsly-market.floot.app . Render Static Site ID `srv-db6bkoqd0e5s73a4s22g`, initialer Deploy `dep-db6bkpad0e5s73a4s3s0`, Status `live` am 12.10.2026 10:46 UTC. Workspace `tea-db0n9s8u01pc73b491d0` durch Nutzer bestätigt. `autoDeploy=no`: Änderungen am GitHub-Repo lösen bewusst keinen neuen Render-Build aus. Repository `https://github.com/flashbomb98-a11y/swarm`, Branch `master`, Build `test -f opsly/standby-shop/index.html && mkdir -p opsly-standby-public && cp opsly/standby-shop/index.html opsly-standby-public/index.html`, Publish path `opsly-standby-public`. Ausschließlich `index.html` wird in die öffentliche Standby-Site kopiert. Externer Live-Crawl meldete 200 und die erwarteten Kontaktlinks. **Keine zweite identische statische Site erstellen.**

## Was funktioniert
- Sieben Opsly-Linien im einheitlichen deutschen Markendesign #111821 / #C8FF3D.
- Statische Produkt- und Dienstleistungsinformation ohne Laufzeitserver, Framework, Webfont, Tracking-Script, Cookies oder externe Dienste.
- Kunden können uns mit ihrem Standard-E-Mail-Programm über `opsly-sales@agentmail.to` erreichen. Das Postfach ist über die bestehende AgentMail-Verbindung lesbar.
- Die CTA-Links führen zum bestehenden Floot-Hauptshop, soweit dieser läuft.
- `noindex` bis zu einer offiziellen Umschaltung, um Duplicate-Content gegen den Hauptshop zu vermeiden.

## Noch NICHT möglich
- Stripe-Zahlungen, Freischaltung digitaler Download-Dateien oder Bestellabwicklung auf der Standby-Domain.
- Direkter Weiterverkauf, falls Floot selbst nicht erreichbar ist.
- Automatisches DNS-Failover unter `opsly-market.floot.app`, weil das eine Floot-Subdomain ist.
- Das Repo darf KEINE Stripe-Zugangsdaten, live `sk_*`/Webhook-Secrets, personenbezogenen Bestellungen, privaten Kauf-ZIPs oder Kunden-Datensätze enthalten.

## Kostenfreie Deployment-Optionen
**Render:** Workspace `Opsly's workspace` ist vom Nutzer ausdrücklich bestätigt; das kostenlose **Static-Site-Projekt ist eingerichtet und live** (Details siehe oben). Kein zweites Projekt anlegen. Vor eventuellen späteren Deploys den Standby-Code und die veröffentlichten Paketpreise prüfen, dann manuell genau diesen Service deployen. Das Render-Static-Site-Angebot hat keine eigenen Compute-Instanzgebühren, verwendet aber monatliche gemeinsame Freikontingente für Bandbreite und Build-Minuten; bei Überschreitung können je nach hinterlegter Zahlungsmethode Nutzungsgebühren anfallen. Die Connector-Verbindung legt keine Rechnungs- oder Limitkonfiguration offen. Automatische Deployments bewusst aus, `noindex,nofollow`, nicht als öffentliche Hauptshop-Adresse bewerben. Keine kostenpflichtigen Planänderungen.

**Cloudflare Pages:** Noch nicht verbunden. Kostenloses statisches Pages-Projekt aus demselben GitHub-Pfad mit 500 kostenlosen Builds/Monat möglich; öffentliches Asset-Serving ist im statischen Free-Modell kostenlos. `root directory=opsly/standby-shop`, `build command` leer bzw. `exit 0`, `build output directory=.`. Vor Verbinden Account-/Projektlimits prüfen. Keine API-Tokens veröffentlichen.

**Nicht verwenden:** GitHub Pages (nicht als Online-Geschäfts-/E-Commerce-Site), Vercel Hobby (nicht für kommerzielle Nutzung); Railway und kostenpflichtige Render-Webservices nicht ohne Kostenprüfung.

## Reale Umschalt-Freigabe (nicht vorher von „Backup-Shop live“ sprechen)
1. Shop-Quellcode aus Floot in eine einzige versionierte GitHub-Codebasis übertragen und mit dieser Standby-Seite zusammenführen. Nicht zwei voneinander abweichende Kataloge dauerhaft pflegen.
2. Unabhängigen Checkout-Endpunkt mit Server-Secrets in geschütztem Runtime-Environment aufbauen; niemals im Frontend oder GitHub. Zahlungserfolg nur über Stripe mit echtem Signatur-/Session-Check akzeptieren.
3. Private Downloads und Bestellfreigabe nur an tatsächlich bezahlte Käufer liefern, kein öffentliches ZIP-Fallback.
4. Tests: Ausfall Hauptshop, Aufruf Standby, Anfrage per mailto, Produktlinks, unabhängiger Kaufweg, Fulfillment, Fehlzahlungen, doppelte Webhook-Events und Erstattung.
5. Umschaltung auf eine künftig unabhängig kontrollierte Domain; bei bestehender Floot-Subdomain gibt es keinen Anbieterwechsel der **gleichen URL**.
6. Erst nach diesen Gates `noindex` passend setzen, die Seite öffentlich bewerben und regelmäßigen Wiederherstellungstest einrichten.

## Qualität
`python3 opsly/standby-shop/validate.py` prüft die statische Seite lokal ohne zusätzliche Bibliotheken. Die Existenz des Quellcodes in GitHub ist **noch keine** Online-Veröffentlichung.
