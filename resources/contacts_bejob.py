"""
Ansprechpartner für BeJob
"""

BEJOB_CONTACTS = [
    {
        "id": "bejob_1",
        "name": "Lisa Hoffmann",
        "role": "Head of Recruiting",
        "email": "l.hoffmann@bejob.de",
        "phone": "+49 30 9876 5401",
        "image": None  # Optional: Pfad zu Profilbild
    },
    {
        "id": "bejob_2",
        "name": "Markus Klein",
        "role": "Senior Recruiter",
        "email": "m.klein@bejob.de",
        "phone": "+49 30 9876 5402",
        "image": None
    },
    {
        "id": "bejob_3",
        "name": "Julia Schneider",
        "role": "Talent Manager",
        "email": "j.schneider@bejob.de",
        "phone": "+49 30 9876 5403",
        "image": None
    },
    {
        "id": "bejob_4",
        "name": "Stefan Wagner",
        "role": "HR Consultant",
        "email": "s.wagner@bejob.de",
        "phone": "+49 30 9876 5404",
        "image": None
    }
]

def get_bejob_contacts():
    """Gibt Liste aller BeJob Ansprechpartner zurück"""
    return BEJOB_CONTACTS

def get_contact_by_id(contact_id: str):
    """Findet Ansprechpartner nach ID"""
    for contact in BEJOB_CONTACTS:
        if contact["id"] == contact_id:
            return contact
    return None

