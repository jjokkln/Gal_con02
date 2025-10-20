# Changelog Version 1.1.0

## 🎯 Ziel
Verbesserung der Struktur, Datenschutz und Unternehmensauswahl

## 📅 Datum
20. Oktober 2025

---

## 🆕 Neue Funktionen

### 1. Zentrale Extraktion-Regeln
**Datei:** `resources/extraction_rules.py`

- Zentrale Verwaltung aller Parsing- und Extraktionslogiken
- OpenAI Prompts modular und wartbar
- Anonymisierungsfunktionen:
  - `anonymize_name()` - "Max Mustermann" → "Max M."
  - `extract_city_from_address()` - Extrahiert Stadt aus vollständiger Adresse
- Export Display Rules (was im Export gezeigt wird)
- Validierungsregeln für Felder

### 2. Ansprechpartner-Verwaltung
**Dateien:** 
- `resources/contacts_galdora.py`
- `resources/contacts_bejob.py`

Jedes Unternehmen hat jetzt eigene Ansprechpartner:
- **Galdora:** 4 Ansprechpartner (Dr. Sarah Schmidt, Michael Weber, Anna Müller, Thomas Fischer)
- **BeJob:** 4 Ansprechpartner (Lisa Hoffmann, Markus Klein, Julia Schneider, Stefan Wagner)

**Integration:**
- Ansprechpartner-Auswahl in Schritt 2 (Persönliche Daten)
- Dropdown mit Name und Rolle
- Anzeige von E-Mail und Telefon des Ansprechpartners

### 3. Sidebar entfernt - Unternehmensauswahl in Schritt 1
**Änderungen in:** `streamlit_app.py`

**Vorher:**
- Unternehmensauswahl in Sidebar
- Sidebar mit API Key Status

**Jetzt:**
- Sidebar komplett entfernt
- Unternehmensauswahl als erstes in Schritt 1
- Zwei große Buttons: "🔵 Galdora" und "🟢 BeJob"
- Logo-Anzeige nach Auswahl
- Upload-Optionen nur sichtbar nach Unternehmensauswahl

### 4. Datenschutz im Export
**Änderungen in:** `streamlit_app.py` - Funktion `prepare_export_data()`

**Im Export werden IMMER versteckt:**
- ❌ E-Mail-Adresse
- ❌ Telefonnummer
- ✅ Nur Wohnort (statt vollständige Adresse)

**Zusätzlich bei Anonymisierung:**
- Name wird zu Vorname + Anfangsbuchstabe
- Beispiel: "Max Mustermann" → "Max M."

### 5. Anonymisierungs-Checkbox in Schritt 3
**Änderungen in:** `streamlit_app.py` - Funktion `show_preview_and_export()`

- Neue Sektion "🔒 Datenschutz-Optionen"
- Checkbox: "Name anonymisieren"
- Info-Box zeigt alle Änderungen bei Aktivierung
- Wirkt sich auf Vorschau UND Export aus (PDF & DOCX)

---

## 🔧 Technische Änderungen

### Session State Erweiterung
```python
if 'selected_contact' not in st.session_state:
    st.session_state.selected_contact = None
if 'anonymize' not in st.session_state:
    st.session_state.anonymize = False
```

### Neue Funktion: `prepare_export_data()`
```python
def prepare_export_data(cv_data, anonymize=False):
    """
    Bereitet CV-Daten für Export vor mit Datenschutz-Optionen
    - Versteckt immer: E-Mail, Telefon
    - Zeigt nur Stadt (nicht vollständige Adresse)
    - Optional: Name anonymisieren
    """
```

### Extractor Anpassung
**Datei:** `backend/core/extractor.py`

- Verwendet jetzt `extraction_rules.py` für Prompts
- Extrahiert automatisch Stadt aus Adresse
- Fügt "city" Feld zu Personal Data hinzu

---

## 📊 User Flow (Neu)

### Schritt 1: Unternehmen & Upload
1. Nutzer wählt Unternehmen (Galdora oder BeJob)
2. Logo wird angezeigt
3. Upload-Optionen werden freigeschaltet
4. CV hochladen oder manuell eingeben

### Schritt 2: Daten bearbeiten
1. Tab "Persönlich": Kontaktdaten + **Ansprechpartner auswählen**
2. Tab "Berufserfahrung": Erfahrungen hinzufügen/bearbeiten
3. Tab "Ausbildung": Ausbildungen hinzufügen/bearbeiten
4. Tab "Fähigkeiten": Skills pflegen

### Schritt 3: Export
1. **Datenschutz-Option:** Anonymisierung aktivieren/deaktivieren
2. Vorschau generieren (berücksichtigt Anonymisierung)
3. Export als PDF oder DOCX

---

## 🎨 UI Verbesserungen

### Entfernte Elemente
- ❌ Komplette Sidebar
- ❌ API Key Eingabe in UI (nur noch .env)

### Neue Elemente
- ✅ Unternehmen-Auswahl-Buttons in Schritt 1
- ✅ Logo-Anzeige nach Unternehmensauswahl
- ✅ Ansprechpartner-Dropdown in Schritt 2
- ✅ Datenschutz-Checkbox in Schritt 3
- ✅ Info-Box für Anonymisierung
- ✅ "🔄 Neu starten" Button im Header

---

## 📁 Dateistruktur (Neu)

```
converter_01/
├── resources/                    # NEU
│   ├── extraction_rules.py      # Zentrale Extraktionsregeln
│   ├── contacts_galdora.py      # Galdora Ansprechpartner
│   ├── contacts_bejob.py        # BeJob Ansprechpartner
│   ├── galdoralogo.png          # Logo
│   └── bejoblogo.png            # Logo (optional)
├── backend/
│   ├── core/
│   │   ├── extractor.py         # GEÄNDERT: Verwendet extraction_rules
│   │   ├── template_renderer.py
│   │   └── exporters.py
│   └── app.py
├── streamlit_app.py             # GEÄNDERT: Alle 5 Aufgaben umgesetzt
├── .env
└── README.md
```

---

## 🧪 Test-Szenarien

### Szenario 1: Normaler Export (ohne Anonymisierung)
1. Unternehmen wählen
2. CV hochladen
3. Ansprechpartner wählen
4. Export ohne Anonymisierung
5. **Erwartet:** Name vollständig, aber E-Mail/Telefon versteckt, nur Stadt

### Szenario 2: Anonymisierter Export
1. Unternehmen wählen
2. CV hochladen
3. Ansprechpartner wählen
4. Anonymisierung aktivieren
5. Export
6. **Erwartet:** Name anonymisiert ("Max M."), E-Mail/Telefon versteckt, nur Stadt

### Szenario 3: Manuelle Eingabe
1. Unternehmen wählen
2. "Manuell eingeben" wählen
3. Alle Daten manuell eingeben
4. Stadt manuell eingeben
5. Ansprechpartner wählen
6. Export
7. **Erwartet:** Alle Daten wie eingegeben, Datenschutz-Regeln angewendet

---

## 🚀 Deployment Notes

### Neue Abhängigkeiten
Keine neuen Python-Packages erforderlich.

### Neue Dateien für Git
```bash
git add resources/extraction_rules.py
git add resources/contacts_galdora.py
git add resources/contacts_bejob.py
```

### Environment Variables
Keine Änderungen - `.env` bleibt gleich.

---

## 📝 Breaking Changes

### ⚠️ Wichtig für bestehende Nutzer:
1. **Sidebar entfernt:** Unternehmensauswahl muss in Schritt 1 erfolgen
2. **Session State:** Neue Felder `selected_contact` und `anonymize`
3. **Export-Format:** E-Mail und Telefon werden nicht mehr exportiert

---

## 🐛 Bug Fixes in dieser Version
- Stadt-Extraktion funktioniert jetzt korrekt
- Ansprechpartner-Import über sys.path.append
- Export verwendet deep copy um Original-Daten zu bewahren

---

## 📚 Dokumentation aktualisiert
- README.md (TODO: Muss noch aktualisiert werden)
- PROGRESS.md (TODO: Version 1.1.0 eintragen)
- Dieser CHANGELOG

---

## 🔮 Zukünftige Verbesserungen (Nice-to-have)
- [ ] Ansprechpartner mit Profilbildern
- [ ] Mehrsprachige Extraktion-Regeln
- [ ] Custom Anonymisierungs-Regeln
- [ ] Export-Template-Auswahl
- [ ] Drag & Drop für Logo-Upload

