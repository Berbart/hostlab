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
- [ ] Landing Page mit HTML/CSS (Tailwind oder Bootstrap)
- [ ] Dark-/Light-Mode Toggle via JavaScript
- [ ] Dynamische Gallerie aus einem Verzeichnis (`/public/images`)
- [ ] Markdown-Artikel als statische Seiten (`/content/*.md`)
- [ ] Kontaktformular (Frontend, optional Backend-Anbindung)
- [ ] Lokale Sprachumschaltung (Deutsch/Englisch)

### ⚙️ Backend-Entwicklung
- [ ] REST-API mit einfachen Endpunkten (`/api/ping`, `/api/info`)
- [ ] File Upload + File Serving über die API
- [ ] Einfacher JSON-Datenspeicher (Dateibasiert)
- [ ] Dummy-Login mit Session (Cookie oder Token-basiert)
- [ ] Serverseitiger Markdown-Renderer

### 🎲 Interaktive Spiele (Frontend/Backend kombiniert)
- [ ] Einfaches Schachspiel mit KI oder Zwei-Spieler-Logik
- [ ] Wizard (Stichspiel) als Spiel-Logik + Frontend
- [ ] Zufallsgeneriertes Puzzle oder Memory-Spiel
- [ ] Highscore-Logik & Spielstand-Speicherung

### 🧠 KI-freundliche Aufgaben für Codex
- [ ] Menü aus Ordnerstruktur generieren (`/content`)
- [ ] Theme-Konfiguration per JSON-Datei
- [ ] API-Tests schreiben (`pytest`, `unittest`, `go test`)
- [ ] Farben, Icons oder Layout dynamisch generieren lassen
- [ ] API für „Fun Facts“ oder Zitate bauen

### 🐳 Docker & DevOps
- [ ] Dockerfile für statischen Server (Nginx)
- [ ] Dockerfile für API mit `docker-compose.yml`
- [ ] `.devcontainer` für VS Code Remote Development
- [ ] `Makefile` oder `Taskfile.yml` für lokale Automatisierung

### 🔐 Sicherheit & Access Control
- [ ] Zugriffsbeschränkung für API-Endpunkte
- [ ] Upload-Security: Dateitypprüfung, Limitierung
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

### API starten

Nach der Installation der Abhängigkeiten kann die kleine Beispiel‑API
lokal mit folgendem Kommando gestartet werden:

```bash
python api/app.py
```

Die Endpunkte sind anschließend unter `http://localhost:5000/api/*` verfügbar.

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
