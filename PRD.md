📋 CV2Profile Neuaufbau - Komplette Neuentwicklung

  🎯 Projektziel

  Entwurf eines Konvertierungstools für Profilvorlagen. Lebenslauf wird hochgeladen, fertige Profilvorlage nach den Anforderungen meiner UNternehmen kommen heraus. Funktioniert basierend auf KI Analyse

  📝 Anforderungen (Requirements)

  Userflow:

  1. Schritt 1: Startseite mit großem Logo + glasige
  Drag & Drop Fläche für CV-Upload
  2. Schritt 2: Datenbearbeitung (extrahierte Daten +
  Unternehmensauswahl + Drag & Drop Sortierung)
  3. Schritt 3: Export (PDF-Vorschau + PDF/Word
  Download, nur Classic Template)

  Technische Specs:

  - Max. Dateigröße: 10 MB
  - Unterstützte Formate: PDF, DOCX, JPEG, PNG
  - AI-Extraktion: OpenAI API
  - Templates: Nur Classic Template
  - Session: Temporär (nicht persistent)
  - Unternehmen: Galdora + BeJob (Auswahl in Schritt 2
  

  🎨 Frontend Komponenten Spezifikation

  1. Startseite (/)

  // Layout: Zentriertes Design mit Glasmorphism
  // Komponenten:
  
  - Unternehmensauswahl
  - Radio Buttons: Galdora / BeJob
  - Logo Preview des gewählten Unternehmens
  - Header mit CV2Profile Logo (groß)
  - Glasmorphic Card Container
  - Drag & Drop Zone (react-dropzone)
    - Akzeptierte Formate: .pdf, .docx, .jpg, .png
    - Max Size: 10MB
    - Upload Progress Bar
  - Footer mit Links

  // Styling: Glasmorphism Effekt
  - backdrop-blur-lg
  - bg-white/10
  - border border-white/20
  - Aktuelle Farbpalette beibehalten

  2. Datenbearbeitung (/edit)

  // Layout: 3-Abschnitte Grid (responsive)
  
  // 1. Abschnitt: Persönliche Daten
  - Name, Adresse, Kontakt
  - Profilbeschreibung (Textarea)

  // 2. Abschnitt: Berufserfahrung
  - Drag & Drop sortierbare Liste
  - Add/Edit/Delete Funktionen
  - Felder: Position, Unternehmen, Zeitraum,
  Beschreibung

  // 3. Abschnitt: Ausbildung & Weiterbildung  
  - Zwei separate Drag & Drop Listen
  - Gleiche CRUD Funktionen
  - Felder: Titel, Institution, Zeitraum, Details


  // Funktionen:
  - Auto-Save alle 5 Sekunden
  - Cross-Category Drag & Drop
  - Form Validation

  3. Export (/export)

Oben: PDF Preview:
  - Zoom Controls (50% - 300%)
  - Seitennavigation (falls mehrseitig)
  - Vollbild-Option

  // Unten: Export Optionen
  - PDF Download Button
  - Word Download Button
  - "Zurück bearbeiten" Link
  - Neue Profilvorlage erstellen

  // PDF Preview Features:
  - Responsive Design
  - Loading States
  - Error Handling