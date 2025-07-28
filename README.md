# Kindle Dashboard

Dieses Script erstellt alle Stunde ein Dashboard png und lädt dieses auf Nextcloud hoch.
Dafür die .env mit den Daten der Nextcloud Instanz befüllen.
`docker compose build` ausführen und
`docker push registry.floxsite.de/kindle-dashboard:latest` zum hochladen.

Das Gegenstück an Code liegt dann auf dem Kindle und muss dementsprechend angepasst werden.
Dafür ein folgendes Repo auschecken.
Thanks to [pascalw](https://github.com/pascalw/kindle-dash)!
