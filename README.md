# 🧪 Codex Playground – Experimentierumgebung für statische Seiten, APIs und Spiele

Willkommen im **Codex Playground** – einem flexiblen Projekt-Repository für das lokale Testen und Entwickeln von Frontend, Backend, APIs, DevOps-Tools und kleineren interaktiven Anwendungen mit Hilfe von Codex (KI).

## 📌 Zielsetzung

Dieses Repository dient als Testumgebung für:
- Schnelles Prototyping kleiner Web-Features
- Entwicklung und Integration einfacher APIs (z. B. Go, Flask, Node.js)
- Umsetzung einfacher interaktiver Web-Spiele
- Frontend-Design & dynamischer Content
- Testing & DevOps-Tools (Docker, VS Code DevContainer)
- Lokale Entwicklung und Hosting via Codex-Unterstützung

---

## 🔧 Projektmodule & Aufgaben

### 🌐 Statische Webinhalte
- [x] Landing Page mit HTML/CSS (Tailwind oder Bootstrap)
- [x] Dark-/Light-Mode Toggle via JavaScript
- [x] Dynamische Gallerie aus einem Verzeichnis (`/public/images`)
- [x] Markdown-Artikel als statische Seiten (`/content/*.md`)
- [ ] Kontaktformular (Frontend, optional Backend-Anbindung)
- [ ] Lokale Sprachumschaltung (Deutsch/Englisch)

### ⚙️ Backend-Entwicklung
- [x] REST-API mit einfachen Endpunkten (`/api/ping`, `/api/info`)
- [x] File Upload + File Serving über die API
- [x] Einfacher JSON-Datenspeicher (Dateibasiert)
- [x] Dummy-Login mit Session (Cookie oder Token-basiert)
- [x] Serverseitiger Markdown-Renderer

### 🎲 Interaktive Spiele (Frontend/Backend kombiniert)
- [x] Einfaches Schachspiel mit KI oder Zwei-Spieler-Logik
- [ ] Wizard (Stichspiel) als Spiel-Logik + Frontend
- [ ] Zufallsgeneriertes Puzzle oder Memory-Spiel
- [ ] Highscore-Logik & Spielstand-Speicherung

### 🧠 KI-freundliche Aufgaben für Codex
- [ ] Menü aus Ordnerstruktur generieren (`/content`)
- [ ] Theme-Konfiguration per JSON-Datei
- [x] API-Tests schreiben (`pytest`, `unittest`, `go test`)
- [ ] Farben, Icons oder Layout dynamisch generieren lassen
- [ ] API für „Fun Facts“ oder Zitate bauen

### 🐳 Docker & DevOps
- [x] Dockerfile für statischen Server (Nginx)
- [x] Dockerfile für API mit `docker-compose.yml`
- [x] `.devcontainer` für VS Code Remote Development
- [x] `Makefile` oder `Taskfile.yml` für lokale Automatisierung

### 🔐 Sicherheit & Access Control
- [x] Zugriffsbeschränkung für API-Endpunkte
- [x] Upload-Security: Dateitypprüfung, Limitierung
- [ ] Custom Error Pages (z. B. 404, 403)

---

## 🚀 Schnellstart (lokal)

```bash
git clone https://github.com/dein-user/codex-playground.git
cd codex-playground
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
# oder: docker compose up --build
```

### Docker Compose

Statt der lokalen Installation kann die Anwendung über Docker Compose gestartet werden:

```bash
docker compose up --build
```
Frontend steht dann auf <http://localhost:8080>, die API auf <http://localhost:5000> bereit.

### API starten

Nach der Installation der Abhängigkeiten kann die kleine Beispiel‑API
lokal mit folgendem Kommando gestartet werden:

```bash
python api/app.py
```

Die statische Seite erreichst du unter `http://localhost:5000/`.
Die Endpunkte sind anschließend unter `http://localhost:5000/api/*` verfügbar.

### Neue Endpunkte

- `GET /api/images` – listet Dateien aus `/public/images`
- `GET /articles/<name>` – rendert Markdown-Dateien aus `/content`
- `POST /api/login` – gibt bei korrekter Anmeldung ein Token zurück (`{"username": "admin", "password": "secret"}`)
- `POST /api/render` – erwartet JSON `{"text": "# Titel"}` und liefert gerendetes HTML zurück (Token benötigt)
- `POST /api/upload` – lädt eine Datei hoch
- `GET /api/files/<name>` – lädt hochgeladene Dateien herunter
- `GET /api/store` / `POST /api/store` – listet bzw. erstellt Datensätze
- `GET|PUT|DELETE /api/store/<id>` – Einzelzugriff auf Datensätze
- `GET /api/chess` – aktuellen Spielstand abrufen
- `POST /api/chess` – neuen Spielstand speichern

## 🖥️ Lokale Nutzung

Dieser Playground soll dir die komplette Kontrolle über deine Webanwendung geben.
Du kannst alle Features direkt auf deinem Laptop ausführen und über VS Code testen.
Im DevContainer läuft sowohl ein Webserver für statische Dateien als auch
(optional) eine API mit Hot-Reload. So entwickelst du ohne Umwege und siehst jede
Änderung sofort im Browser.

### Tipps für dein Setup
- VS Code mit Remote-Containers Erweiterung öffnen
- `docker compose up` startet Frontend und Backend
- lokale URL im Browser aufrufen, z.B. `http://localhost:8000`
- Anpassungen an HTML/CSS/JS werden automatisch geladen

## 🗂️ Projektübersicht

Mit diesem Repository kannst du Schritt für Schritt eine modulare Webanwendung
aufbauen. Kombiniere statische Seiten, kleine Spiele und APIs nach Belieben und
verwende Docker für eine einheitliche Entwicklungsumgebung. Schau auch in die
Datei `KANBAN.md`, um den aktuellen Stand der geplanten Aufgaben zu sehen.
