"""
Extraction Rules for CV2Profile
Zentrale Verwaltung aller Parsing- und Extraktionslogiken
"""

# OpenAI Extraction Prompt Template
EXTRACTION_SYSTEM_PROMPT = """
Du bist ein Experte für das Extrahieren und Strukturieren von Lebenslauf-Daten. 
Gib immer valides JSON zurück.
"""

EXTRACTION_USER_PROMPT = """
Extrahiere und strukturiere den folgenden Lebenslauf-Text in ein JSON-Format. 
Gib NUR valides JSON mit dieser exakten Struktur zurück:

  {
      "personal": {
          "name": "Vollständiger Name",
          "city": "Stadt",
          "summary": "Professionelle Zusammenfassung oder Zielsetzung"
      },
    "experience": [
        {
            "position": "Jobtitel",
            "company": "Firmenname",
            "start_date": "MM/YYYY",
            "end_date": "MM/YYYY oder Heute",
            "description": "Jobbeschreibung und Erfolge"
        }
    ],
    "education": [
        {
            "degree": "Abschlussname",
            "institution": "Universität/Schule",
            "start_date": "MM/YYYY",
            "end_date": "MM/YYYY",
            "description": "Zusätzliche Details"
        }
    ],
    "skills": [
        "Fähigkeit 1", "Fähigkeit 2", "Fähigkeit 3"
    ],
    "certifications": [
        {
            "name": "Zertifikatsname",
            "issuer": "Ausstellende Organisation",
            "date": "MM/YYYY"
        }
    ]
}

Wenn ein Feld nicht gefunden wird, verwende null oder ein leeres Array/String.
Extrahiere Daten im Format MM/YYYY.
Extrahiere die Stadt separat aus der Adresse ins 'city' Feld.
"""

# Field Validation Rules
REQUIRED_FIELDS = {
    "personal": ["name"],
    "experience": ["position", "company"],
    "education": ["degree", "institution"],
}

OPTIONAL_FIELDS = {
    "personal": ["email", "phone", "address", "city", "linkedin", "summary"],
    "experience": ["start_date", "end_date", "description"],
    "education": ["start_date", "end_date", "description"],
}

# Data Cleaning Rules
CLEANING_RULES = {
    "phone": {
        "remove_chars": [" ", "-", "(", ")", "/"],
        "format": "+49 XXX XXXXXX"
    },
    "email": {
        "lowercase": True,
        "trim": True
    },
    "dates": {
        "format": "MM/YYYY",
        "current_synonyms": ["Heute", "Present", "Aktuell", "Current"]
    }
}

# Privacy/Anonymization Rules
ANONYMIZATION_RULES = {
    "name": {
        "pattern": "first_initial_last",  # "Max Mustermann" -> "Max M."
        "placeholder": "Anonymisiert"
    },
    "email": {
        "hide": True,
        "placeholder": "[E-Mail versteckt]"
    },
    "phone": {
        "hide": True,
        "placeholder": "[Telefon versteckt]"
    },
    "address": {
        "show_city_only": True,  # Nur Stadt zeigen, nicht vollständige Adresse
    }
}

# Export Display Rules
EXPORT_DISPLAY_RULES = {
    "show_fields": {
        "personal": ["name", "city", "linkedin", "summary"],  # Kein email, phone
        "experience": ["position", "company", "start_date", "end_date", "description"],
        "education": ["degree", "institution", "start_date", "end_date", "description"],
        "skills": True,
        "certifications": True
    },
    "hide_fields": {
        "personal": ["email", "phone", "address"]  # Diese Felder nicht im Export zeigen
    }
}

def anonymize_name(full_name: str) -> str:
    """
    Anonymisiert einen Namen: 'Max Mustermann' -> 'Max M.'
    """
    if not full_name:
        return "Anonymisiert"
    
    parts = full_name.split()
    if len(parts) >= 2:
        return f"{parts[0]} {parts[-1][0]}."
    return full_name

def extract_city_from_address(address: str) -> str:
    """
    Extrahiert Stadt aus Adresse
    Beispiel: "Musterstraße 123, 12345 Berlin, Deutschland" -> "Berlin"
    """
    if not address:
        return ""
    
    # Simple Heuristik: Stadt ist oft nach PLZ (5 Ziffern)
    import re
    match = re.search(r'\d{5}\s+([^,]+)', address)
    if match:
        return match.group(1).strip()
    
    # Fallback: Nimm zweiten Teil nach Komma
    parts = address.split(',')
    if len(parts) >= 2:
        return parts[1].strip()
    
    return address.strip()

