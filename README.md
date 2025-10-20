# 📄 CV2Profile - Lebenslauf zu Profilvorlage Converter

Ein AI-gestütztes Tool zur Konvertierung von Lebensläufen in professionelle Profilvorlagen für Galdora und BeJob.

[![Streamlit App](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://your-app-url.streamlit.app)

## 🎯 Features

✅ **AI-Extraktion**: Automatische Datenextraktion aus CV-Dateien mittels OpenAI GPT-4  
✅ **Multi-Format Support**: PDF, DOCX, JPG, PNG  
✅ **Step-by-Step Workflow**: Geführter 4-Schritte-Prozess  
✅ **Live-Validierung**: Sofortige Hinweise bei fehlenden Pflichtfeldern  
✅ **Drag & Sort**: Reihenfolge von Berufserfahrung und Ausbildung änderbar  
✅ **Cross-Category**: Verschieben zwischen Berufserfahrung ↔ Ausbildung  
✅ **Template-Auswahl**: Modern & Classic Vorlagen  
✅ **Anonymisierung**: Optional Name anonymisieren  
✅ **Export**: PDF & DOCX mit Firmenlogo  

## 🚀 Quick Start

### Lokale Installation

1. **Repository klonen**
```bash
git clone https://github.com/jjokkln/Gal_con02.git
cd Gal_con02
```

2. **Virtuelle Umgebung erstellen** (empfohlen)
```bash
python3 -m venv venv
source venv/bin/activate  # Linux/Mac
# oder
venv\Scripts\activate  # Windows
```

3. **Dependencies installieren**
```bash
pip install -r requirements.txt
```

4. **Umgebungsvariablen einrichten**
```bash
cp .env.example .env
# Bearbeite .env und füge deinen OpenAI API Key ein
```

5. **App starten**
```bash
streamlit run streamlit_app.py
```

Die App läuft dann auf: http://localhost:8501

### Alternativ: Start-Scripts verwenden

```bash
# App starten
./run.sh

# App stoppen
./stop.sh

# Nur Streamlit starten (kein Backend)
./start-streamlit-only.sh
```

## 🔑 OpenAI API Key Setup

### Lokal (Entwicklung)

1. Erstelle eine `.env` Datei im Projektverzeichnis:
```bash
OPENAI_API_KEY=sk-proj-dein-api-key-hier
```

2. Die App lädt den Key automatisch beim Start

### Streamlit Cloud (Production)

1. Gehe zu deiner App auf Streamlit Cloud
2. Klicke auf **Settings** → **Secrets**
3. Füge folgendes hinzu:
```toml
OPENAI_API_KEY = "sk-proj-dein-api-key-hier"
```
4. Speichern → App startet neu

**API Key erhalten:**
- Gehe zu [OpenAI Platform](https://platform.openai.com/api-keys)
- Erstelle einen neuen API Key
- Kopiere und füge ihn sicher ein

## 📋 User Flow

### Schritt 1: Unternehmen auswählen & CV hochladen
- Wähle **Galdora** oder **BeJob**
- Lade CV hoch (PDF, DOCX, Bild) **oder** gib Daten manuell ein
- AI analysiert automatisch

### Schritt 2: Berufserfahrung bearbeiten
- Überprüfe extrahierte Positionen
- **Pflichtfelder**: Position, Unternehmen
- Füge Aufgaben als Stichpunkte hinzu
- Sortiere mit ⬆️⬇️ Buttons
- Verschiebe zu Ausbildung mit 🔀

### Schritt 3: Ausbildung & Fähigkeiten
- Bearbeite Abschlüsse
- Füge Fähigkeiten hinzu
- Sortiere und verschiebe

### Schritt 4: Zusammenfassung & Export
- Überprüfe alle Daten
- Wähle Template (Modern/Classic)
- Optional: Name anonymisieren
- **Vorschau generieren**
- Download als **PDF** oder **Word**

## 📁 Projektstruktur

```
converter_01/
├── streamlit_app.py           # Hauptanwendung
├── backend/
│   ├── core/
│   │   ├── extractor.py       # AI-Extraktion
│   │   ├── template_renderer.py
│   │   └── exporters.py       # PDF/DOCX Export
│   └── app.py                 # FastAPI Backend (optional)
├── resources/
│   ├── extraction_rules.py    # AI Prompts & Regeln
│   ├── contacts_galdora.py    # Ansprechpartner Galdora
│   └── contacts_bejob.py      # Ansprechpartner BeJob
├── ressources/
│   ├── galdoralogo.png
│   └── bejob-logo.png
├── requirements.txt
├── .env.example
├── .streamlit/
│   └── config.toml
└── README.md
```

## 🛠️ Technologie-Stack

- **Frontend**: Streamlit 1.28.0
- **AI**: OpenAI GPT-4
- **PDF Processing**: PyPDF2, ReportLab
- **DOCX**: python-docx
- **Templating**: Jinja2

## 🎨 Design-Features

- **Fortschrittsbalken**: 4-Schritte-Anzeige mit %
- **Live-Validierung**: Pflichtfelder werden sofort geprüft
- **Modern Cards**: Hover-Effekte und Schatten
- **Gradient Header**: Lila (#667eea → #764ba2)
- **Responsive**: Funktioniert auf allen Geräten

## 🔒 Datenschutz

- Keine Datenbank - Daten nur im Session State
- Temporäre Dateien werden automatisch gelöscht
- Optional: Namens-Anonymisierung
- Email/Telefon werden im Export versteckt

## 📊 Deployment auf Streamlit Cloud

1. **Repository auf GitHub pushen** (bereits erledigt)
2. Gehe zu [share.streamlit.io](https://share.streamlit.io)
3. Klicke **New app**
4. Wähle dein Repository: `jjokkln/Gal_con02`
5. Main file: `streamlit_app.py`
6. Füge **Secrets** hinzu (OpenAI API Key)
7. Click **Deploy**!

## 📝 Dokumentation

- [UX_REDESIGN_PLAN.md](UX_REDESIGN_PLAN.md) - Technischer Plan
- [UX_FLOW_VISUAL.md](UX_FLOW_VISUAL.md) - Visueller Workflow
- [PRD.md](PRD.md) - Product Requirements
- [PROGRESS.md](PROGRESS.md) - Entwicklungsfortschritt

## 🐛 Troubleshooting

### "OpenAI API Key nicht gefunden"
- Prüfe ob `.env` Datei existiert und `OPENAI_API_KEY` gesetzt ist
- Für Streamlit Cloud: Prüfe Secrets in App Settings

### "Fehler beim PDF-Export"
- Stelle sicher dass alle Pflichtfelder ausgefüllt sind
- Prüfe ob `ressources/` Ordner die Logos enthält

### "Drag & Drop funktioniert nicht"
- Nutze die ⬆️⬇️ Buttons zum Sortieren
- Diese Lösung ist stabiler und funktioniert immer

## 🤝 Support

Bei Fragen oder Problemen:
- Erstelle ein Issue auf GitHub
- Kontaktiere den Administrator

## 📜 License

Proprietäres Projekt für Galdora und BeJob.

---

**Made with ❤️ using Streamlit & OpenAI GPT-4**
