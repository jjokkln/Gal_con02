# CV2Profile - Quickstart Guide

## ⚡ In 3 Schritten starten

### 1. API Key einrichten
Öffne `.env` und füge deinen OpenAI API Key ein:
```bash
OPENAI_API_KEY=sk-your-actual-api-key-here
```

Keinen API Key? Hol dir einen auf [platform.openai.com](https://platform.openai.com)

### 2. App starten
```bash
./run.sh
```

### 3. Verwenden
Öffne im Browser: **http://localhost:8501**

## 🎯 Verwendung

### Option A: CV hochladen und analysieren
1. Wähle "Lebenslauf hochladen und analysieren"
2. Lade deinen CV hoch (PDF, DOCX, JPG, PNG)
3. Klicke "Lebenslauf analysieren"
4. Bearbeite die extrahierten Daten
5. Exportiere als PDF oder Word

### Option B: Manuell eingeben
1. Wähle "Manuell eingeben (ohne Upload)"
2. Klicke "Manuell starten"
3. Fülle alle Felder aus
4. Exportiere als PDF oder Word

## 🛑 Stoppen

```bash
./stop.sh
```

oder drücke `Ctrl+C` im Terminal

## 🔧 Troubleshooting

### App startet nicht
```bash
# Dependencies installieren
python3 -m pip install -r backend/requirements.txt

# Dann nochmal versuchen
./run.sh
```

### API Key Fehler
- Prüfe ob `.env` existiert
- Prüfe ob `OPENAI_API_KEY=sk-...` korrekt ist
- Starte App neu: `./stop.sh` dann `./run.sh`

### Port bereits belegt
```bash
# Beende alte Prozesse
./stop.sh

# Oder manuell
pkill -f streamlit
pkill -f uvicorn
```

## 📚 Weitere Infos

- Vollständige Dokumentation: `README.md`
- Setup-Guide: `SETUP.md`
- Fragen? Schau in die Logs im Terminal

---

**Das war's!** Viel Erfolg mit CV2Profile! 🚀

