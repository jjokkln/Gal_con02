# 🚀 Streamlit Cloud Deployment Guide

## Voraussetzungen

✅ GitHub Account  
✅ Streamlit Cloud Account ([share.streamlit.io](https://share.streamlit.io))  
✅ OpenAI API Key ([platform.openai.com](https://platform.openai.com/api-keys))  

---

## Schritt-für-Schritt Anleitung

### 1. Repository auf GitHub

**Bereits erledigt!** ✅

Repository URL: [https://github.com/jjokkln/Gal_con02.git](https://github.com/jjokkln/Gal_con02.git)

### 2. Streamlit Cloud Setup

1. **Gehe zu [share.streamlit.io](https://share.streamlit.io)**
2. **Sign in** mit deinem GitHub Account
3. Klicke auf **"New app"** (oder **"Deploy an app"**)

### 3. App Konfiguration

Fülle die Felder aus:

```
Repository: jjokkln/Gal_con02
Branch: main (oder master)
Main file path: streamlit_app.py
App URL: [dein-wunsch-name] (z.B. cv2profile-galdora)
```

### 4. Secrets einrichten (WICHTIG!)

Bevor du auf "Deploy" klickst:

1. Scrolle nach unten zu **"Advanced settings"**
2. Klicke auf **"Secrets"**
3. Füge folgendes ein:

```toml
OPENAI_API_KEY = "sk-proj-DEIN-ECHTER-API-KEY-HIER"
```

**Beispiel:**
```toml
OPENAI_API_KEY = "sk-proj-abc123def456ghi789..."
```

⚠️ **WICHTIG:** 
- Verwende ECHTE Anführungszeichen: `"` (nicht `"` oder `"`)
- Keine Leerzeichen vor/nach dem `=`
- Der Key muss mit `sk-` beginnen

### 5. Deployment starten

1. Klicke auf **"Deploy!"**
2. Warte 2-5 Minuten
3. Die App startet automatisch

### 6. Überprüfen

Wenn die App läuft:

✅ **Test 1:** Öffne die App-URL  
✅ **Test 2:** Wähle ein Unternehmen  
✅ **Test 3:** Lade einen Test-CV hoch  
✅ **Test 4:** Überprüfe ob AI-Analyse funktioniert  
✅ **Test 5:** Exportiere als PDF  

---

## 🔧 Troubleshooting

### Problem: "OpenAI API Key nicht gefunden"

**Lösung:**
1. Gehe zu App Settings (⚙️ oben rechts)
2. Klicke auf **"Secrets"** im linken Menü
3. Überprüfe ob `OPENAI_API_KEY` korrekt gesetzt ist
4. Format: `OPENAI_API_KEY = "sk-proj-..."`
5. **Reboot app** (unten rechts)

### Problem: "App startet nicht"

**Lösung:**
1. Überprüfe **Logs** (unten rechts "Manage app" → "Logs")
2. Häufige Fehler:
   - Fehlende Dependencies → Prüfe `requirements.txt`
   - Python Version → Streamlit Cloud nutzt Python 3.9+
   - Fehlende Dateien → Prüfe ob alle Dateien gepusht wurden

### Problem: "Import Error: streamlit_sortables"

**Lösung:**
- Bereits behoben! ✅
- Wir nutzen keine externe Drag & Drop Library mehr
- Falls der Fehler auftritt: `git pull` und erneut deployen

### Problem: "Logos werden nicht angezeigt"

**Lösung:**
1. Prüfe ob `ressources/` Ordner existiert
2. Prüfe ob `galdoralogo.png` und `bejob-logo.png` vorhanden sind
3. Pfade in Code überprüfen (sollten relativ sein)

---

## 📊 App verwalten

### App neu starten

1. Gehe zu [share.streamlit.io](https://share.streamlit.io)
2. Finde deine App
3. Klicke auf **"⋮"** (drei Punkte)
4. Wähle **"Reboot app"**

### Secrets ändern

1. App öffnen → **"⚙️ Settings"**
2. **"Secrets"** im linken Menü
3. Bearbeiten und **"Save"**
4. App startet automatisch neu

### Logs anschauen

1. App öffnen → **"Manage app"** (unten rechts)
2. **"Logs"** Tab
3. Zeigt Fehler und Warnungen

### App löschen

1. [share.streamlit.io](https://share.streamlit.io)
2. Finde deine App
3. **"⋮"** → **"Delete app"**

---

## 🔐 Sicherheit

### API Key Schutz

✅ **Niemals** API Keys im Code!  
✅ **Niemals** API Keys in Git committen!  
✅ **Immer** Streamlit Secrets verwenden!  

### .env Datei

Die `.env` Datei ist in `.gitignore`:
- Wird **NICHT** auf GitHub gepusht
- Nur für lokale Entwicklung
- Für Production: **Streamlit Secrets** nutzen!

---

## 📈 Performance Optimierung

### Empfehlungen für Streamlit Cloud

1. **Caching nutzen**: `@st.cache_data` wo möglich
2. **Session State**: Nur notwendige Daten speichern
3. **File Size**: CV-Uploads auf 10MB limitiert (bereits implementiert)
4. **API Calls**: Minimieren durch lokale Validierung

### Resource Limits (Free Tier)

- **Memory**: 1GB RAM
- **CPU**: Shared
- **Sleep**: App schläft nach 7 Tagen Inaktivität

Unser Tool ist optimiert und bleibt unter diesen Limits! ✅

---

## 🔄 Updates deployen

### Methode 1: Git Push (Auto-Deploy)

```bash
# Änderungen machen
git add .
git commit -m "Beschreibung der Änderung"
git push origin main
```

Streamlit Cloud deployed automatisch! 🚀

### Methode 2: Manueller Redeploy

1. [share.streamlit.io](https://share.streamlit.io)
2. Deine App → **"⋮"**
3. **"Reboot app"**

---

## 📞 Support

### Streamlit Community

- [Forum](https://discuss.streamlit.io/)
- [Docs](https://docs.streamlit.io/)
- [GitHub](https://github.com/streamlit/streamlit)

### OpenAI Support

- [Platform Docs](https://platform.openai.com/docs)
- [API Status](https://status.openai.com/)
- [Community](https://community.openai.com/)

---

## ✅ Deployment Checklist

Vor dem Deployment:

- [ ] `.env.example` erstellt mit Anleitung
- [ ] `.gitignore` enthält `.env` und Secrets
- [ ] `requirements.txt` vollständig und aktuell
- [ ] `README.md` mit Setup-Anleitung
- [ ] Alle Dateien auf GitHub gepusht
- [ ] OpenAI API Key bereit
- [ ] Streamlit Cloud Account erstellt

Während des Deployments:

- [ ] Repository verbunden
- [ ] `streamlit_app.py` als Main File
- [ ] Secrets korrekt eingegeben
- [ ] Deploy gestartet

Nach dem Deployment:

- [ ] App-URL funktioniert
- [ ] AI-Analyse funktioniert
- [ ] PDF/DOCX Export funktioniert
- [ ] Firmenlogos werden angezeigt
- [ ] Alle 4 Schritte durchlaufen

---

**🎉 Fertig! Deine App ist live!**

Teile die App-URL mit deinem Team:
```
https://[dein-app-name].streamlit.app
```

