# CV2Profile Setup Anleitung

## 🔑 OpenAI API Key einrichten

### Option 1: In .env Datei (Empfohlen)

1. Öffne die `.env` Datei im Projekt-Hauptverzeichnis
2. Füge deinen OpenAI API Key ein:
   ```
   OPENAI_API_KEY=sk-your-api-key-here
   ```
3. Speichere die Datei
4. Starte die Streamlit App neu

### Option 2: Manuell in der App eingeben

1. Starte die Streamlit App
2. Gib deinen API Key in der Sidebar ein
3. Der Key wird nur für die aktuelle Session gespeichert

## 🚀 App starten

### Streamlit (Empfohlen für lokale Nutzung)

```bash
python3 run_streamlit.py
```

Dann öffne: `http://localhost:8501`

### FastAPI Backend + Next.js Frontend

```bash
# Terminal 1: Backend
python3 run_backend.py

# Terminal 2: Frontend
python3 run_frontend.py
```

## 📝 Verwendung

### Option 1: CV hochladen und analysieren

1. Wähle "Lebenslauf hochladen und analysieren"
2. Lade deinen CV hoch (PDF, DOCX, JPG, PNG)
3. Klicke "Lebenslauf analysieren"
4. Bearbeite die extrahierten Daten
5. Exportiere als PDF oder Word

### Option 2: Manuell eingeben

1. Wähle "Manuell eingeben (ohne Upload)"
2. Klicke "Manuell starten"
3. Fülle alle Felder aus
4. Exportiere als PDF oder Word

## 🔧 Troubleshooting

### API Key nicht gefunden

- Prüfe ob `.env` Datei existiert
- Prüfe ob OPENAI_API_KEY korrekt eingetragen ist
- Starte die App neu nach Änderungen

### Upload-Fehler

- Max. Dateigröße: 10MB
- Unterstützte Formate: PDF, DOCX, JPG, PNG
- Stelle sicher dass der OpenAI API Key gültig ist

### Export-Fehler

- Stelle sicher dass alle Pflichtfelder ausgefüllt sind
- Prüfe die Konsole für detaillierte Fehlermeldungen

