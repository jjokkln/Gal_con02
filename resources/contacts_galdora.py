"""
Ansprechpartner für Galdora
"""

GALDORA_CONTACTS = [
    {
        "id": "galdora_1",
        "name": "Alessandro Boehm",
        "role": "Recruiter",
        "email": "boehm@galdora.de",
        "phone": "01261 6212600",
        "image": None  # Optional: Pfad zu Profilbild
    },
    {
        "id": "galdora_2",
        "name": "Kai Fischer    ",
        "role": "Teamleitung Recruiting",
        "email": "fischer@galdora.de",
        "phone": "01261 6212601",
        "image": None
    },
    {
        "id": "galdora_3",
        "name": "Konrad Rusczyk",
        "role": "Recruiter",
        "email": "konrad@galdora.de",
        "phone": "01261 6212600",
        "image": None
    },
    {
        "id": "galdora_4",
        "name": "Melike Demirkol",
        "role": "Recruiter",
        "email": "demirkol@galdora.de",
        "phone": "01261 6212600",
        "image": None
    },
    {
        "id": "galdora_4",
        "name": "Salim Alizai",
        "role": "Geschäftsführung",
        "email": "gf@galdora.de",
        "phone": "01261 6212600",
        "image": None
    },    
]

def get_galdora_contacts():
    """Gibt Liste aller Galdora Ansprechpartner zurück"""
    return GALDORA_CONTACTS

def get_contact_by_id(contact_id: str):
    """Findet Ansprechpartner nach ID"""
    for contact in GALDORA_CONTACTS:
        if contact["id"] == contact_id:
            return contact
    return None

