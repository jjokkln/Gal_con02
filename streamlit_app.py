"""
Streamlit app for CV2Profile
Single-page application with complete user flow
"""

import streamlit as st
import os
import tempfile
import uuid
from datetime import datetime
import base64
from io import BytesIO
import asyncio
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Import our core modules
import sys
sys.path.append('backend')
from core.extractor import extract_cv_data
from core.template_renderer import render_profile_html
from core.exporters import ProfileExporter

# Page configuration
st.set_page_config(
    page_title="CV2Profile",
    page_icon="📄",
    layout="wide",
    initial_sidebar_state="expanded"
)

def apply_theme_css(dark_mode=False):
    """Apply theme CSS based on dark_mode setting"""
    if dark_mode:
        # DARK MODE
        st.markdown("""
        <style>
            [data-testid="stAppViewContainer"] {
                background: linear-gradient(135deg, #1a1a2e 0%, #16213e 100%) !important;
            }
            
            .main {
                background: linear-gradient(135deg, #1a1a2e 0%, #16213e 100%) !important;
                color: #f0f0f0 !important;
            }
    
    /* Headers */
    .main-header {
        text-align: center;
        padding: 2rem 0;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white !important;
        border-radius: 10px;
        margin-bottom: 2rem;
    }
    
    .main-header h1, .main-header p {
        color: white !important;
    }
    
    .section-header {
        color: #667eea !important;
        border-bottom: 2px solid #667eea;
        padding-bottom: 0.5rem;
        margin: 1rem 0;
    }
    
    /* Text inputs and textareas */
    [data-baseweb="input"], [data-baseweb="textarea"] {
        background-color: #f8f9fa !important;
        color: #1e1e1e !important;
        border: 1px solid #dee2e6 !important;
    }
    
    /* Enhanced File Uploader with Drag & Drop Animation */
    [data-testid="stFileUploader"] {
        background: linear-gradient(135deg, rgba(102, 126, 234, 0.1) 0%, rgba(118, 75, 162, 0.1) 100%) !important;
        border: 3px dashed #667eea !important;
        border-radius: 16px !important;
        padding: 3rem !important;
        transition: all 0.3s ease !important;
        position: relative !important;
    }
    
    [data-testid="stFileUploader"]:hover {
        border-color: #764ba2 !important;
        background: linear-gradient(135deg, rgba(102, 126, 234, 0.2) 0%, rgba(118, 75, 162, 0.2) 100%) !important;
        transform: translateY(-2px) !important;
        box-shadow: 0 8px 24px rgba(102, 126, 234, 0.3) !important;
    }
    
    [data-testid="stFileUploader"]::before {
        content: "📁";
        font-size: 4rem;
        display: block;
        text-align: center;
        margin-bottom: 1rem;
        animation: bounce 2s infinite;
    }
    
    @keyframes bounce {
        0%, 100% { transform: translateY(0); }
        50% { transform: translateY(-10px); }
    }
    
    [data-testid="stFileUploader"] label {
        color: #667eea !important;
        font-size: 1.3rem !important;
        font-weight: 700 !important;
        text-align: center !important;
        display: block !important;
    }
    
    [data-testid="stFileUploader"] small {
        color: #6c757d !important;
        font-size: 1rem !important;
        display: block !important;
        text-align: center !important;
        margin-top: 0.5rem !important;
    }
    
    [data-testid="stFileUploader"]::before {
        content: "📁";
        font-size: 4rem;
        display: block;
        text-align: center;
        margin-bottom: 1rem;
        animation: bounce 2s infinite;
    }
    
    @keyframes bounce {
        0%, 100% { transform: translateY(0); }
        50% { transform: translateY(-10px); }
    }
    
    /* Buttons */
    .stButton button {
        background-color: #667eea !important;
        color: white !important;
        border: none !important;
        border-radius: 8px;
        padding: 0.5rem 1rem;
        font-weight: 500;
    }
    
    .stButton button:hover {
        background-color: #764ba2 !important;
    }
    
    /* Expanders - Modern Card Style */
    [data-testid="stExpander"] {
        background-color: white !important;
        border: none !important;
        border-radius: 12px !important;
        box-shadow: 0 2px 12px rgba(0,0,0,0.08) !important;
        margin-bottom: 1rem !important;
        transition: all 0.3s ease !important;
    }
    
    [data-testid="stExpander"]:hover {
        box-shadow: 0 4px 20px rgba(102, 126, 234, 0.15) !important;
        transform: translateY(-2px) !important;
    }
    
    /* Text color override */
    p, span, label, h1, h2, h3, h4, h5, h6 {
        color: #1e1e1e !important;
    }
            
            /* Markdown text */
            .stMarkdown {
                color: #1e1e1e !important;
            }
            
            /* Success/Info/Error boxes */
            .stAlert {
                background-color: #f8f9fa !important;
                color: #1e1e1e !important;
                border: 1px solid #dee2e6 !important;
            }
            
            /* Sidebar (if used) */
            [data-testid="stSidebar"] {
                background-color: #f8f9fa !important;
            }
        </style>
        """, unsafe_allow_html=True)

def toggle_theme():
    """Toggle between light and dark mode"""
    st.session_state.dark_mode = not st.session_state.dark_mode

def initialize_session_state():
    """Initialize session state variables"""
    if 'cv_data' not in st.session_state:
        st.session_state.cv_data = None
    if 'company' not in st.session_state:
        st.session_state.company = None  # Wird in Schritt 1 ausgewählt
    if 'session_id' not in st.session_state:
        st.session_state.session_id = str(uuid.uuid4())
    if 'extraction_complete' not in st.session_state:
        st.session_state.extraction_complete = False
    if 'selected_contact' not in st.session_state:
        st.session_state.selected_contact = None
    if 'anonymize' not in st.session_state:
        st.session_state.anonymize = False
    if 'template' not in st.session_state:
        st.session_state.template = "modern"  # Default template
    if 'current_edit_step' not in st.session_state:
        st.session_state.current_edit_step = 1  # 1=Personal, 2=Experience, 3=Education, 4=Skills, 5=Summary
    if 'dark_mode' not in st.session_state:
        st.session_state.dark_mode = False  # Default: Light Mode
    if 'export_options' not in st.session_state:
        st.session_state.export_options = {
            "limit_tasks": True  # Default: max 5 Aufgaben
        }
    if 'show_summary' not in st.session_state:
        st.session_state.show_summary = True

def month_year_picker(label, key, default_value=""):
    """Custom month/year picker"""
    col1, col2 = st.columns(2)
    
    months = ["01", "02", "03", "04", "05", "06", "07", "08", "09", "10", "11", "12"]
    years = [str(y) for y in range(2025, 1969, -1)]  # 2025 bis 1970
    
    # Parse default value if exists (format: MM/YYYY)
    default_month = "01"
    default_year = "2025"
    if default_value and "/" in default_value:
        parts = default_value.split("/")
        if len(parts) == 2:
            default_month = parts[0]
            default_year = parts[1]
    
    with col1:
        month = st.selectbox(
            f"{label} (Monat)",
            months,
            index=months.index(default_month) if default_month in months else 0,
            key=f"{key}_month"
        )
    
    with col2:
        year = st.selectbox(
            f"{label} (Jahr)",
            years,
            index=years.index(default_year) if default_year in years else 0,
            key=f"{key}_year"
        )
    
    return f"{month}/{year}"

def main():
    """Main application function"""
    initialize_session_state()
    
    # Apply theme CSS
    apply_theme_css(st.session_state.dark_mode)
    
    # Header with Theme Toggle
    col_header, col_theme = st.columns([9, 1])
    
    with col_header:
        st.markdown("""
        <div class="main-header">
            <h1>📄 CV2Profile</h1>
            <p>Konvertiere deinen Lebenslauf in eine professionelle Profilvorlage</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col_theme:
        if st.button("🌙" if not st.session_state.dark_mode else "☀️", 
                     key="theme_toggle",
                     help="Dark/Light Mode umschalten"):
            toggle_theme()
            st.rerun()
    
    # Reset button (ohne Sidebar)
    col1, col2, col3 = st.columns([1, 1, 8])
    with col1:
        if st.button("🔄 Neu starten"):
            st.session_state.cv_data = None
            st.session_state.extraction_complete = False
            st.session_state.company = None
            st.session_state.selected_contact = None
            st.session_state.anonymize = False
            st.session_state.current_edit_step = 1
            st.session_state.session_id = str(uuid.uuid4())
            st.session_state.show_summary = True
            st.rerun()
    
    # Main content area
    if not st.session_state.extraction_complete:
        show_upload_section()
    else:
        show_edit_section()

def show_upload_section():
    """Show file upload section with company selection"""
    st.markdown('<h2 class="section-header">📁 Schritt 1: Unternehmen auswählen & Lebenslauf hochladen</h2>', unsafe_allow_html=True)
    
    # Company Selection
    st.markdown("### 🏢 Wähle das Unternehmen")
    
    # Show company options with logos - Buttons nebeneinander auf gleicher Höhe
    col1, col2 = st.columns(2)
    
    with col1:
        # Show Galdora logo preview
        logo_galdora = "ressources/galdoralogo.png"
        if os.path.exists(logo_galdora):
            st.image(logo_galdora, width=200)
        else:
            st.write("🔵 **Galdora**")
    
    with col2:
        # Show BeJob logo preview
        logo_bejob = "ressources/bejob-logo.png"
        if os.path.exists(logo_bejob):
            st.image(logo_bejob, width=200)
        else:
            st.write("🟢 **BeJob**")
    
    # Buttons direkt nebeneinander auf gleicher Höhe
    col1, col2 = st.columns(2)
    with col1:
        if st.button("Galdora auswählen", key="btn_galdora", use_container_width=True, 
                     type="primary" if st.session_state.company == "galdora" else "secondary"):
            st.session_state.company = "galdora"
    
    with col2:
        if st.button("BeJob auswählen", key="btn_bejob", use_container_width=True,
                     type="primary" if st.session_state.company == "bejob" else "secondary"):
            st.session_state.company = "bejob"
    
    # Show selected company
    if st.session_state.company:
        st.success(f"✅ Ausgewähltes Unternehmen: **{'Galdora' if st.session_state.company == 'galdora' else 'BeJob'}**")
        st.markdown("---")
    
    # Only show upload options if company is selected
    if not st.session_state.company:
        st.info("👆 Bitte wähle zuerst ein Unternehmen aus.")
        return
    
    # Option to skip upload and enter manually
    st.markdown("### 📄 Lebenslauf hochladen oder manuell eingeben")
    upload_mode = st.radio(
        "Wähle eine Option:",
        ["Lebenslauf hochladen und analysieren", "Manuell eingeben (ohne Upload)"],
        help="Wähle ob du einen CV hochladen oder die Daten manuell eingeben möchtest"
    )
    
    if upload_mode == "Manuell eingeben (ohne Upload)":
        if st.button("📝 Manuell starten", type="primary"):
            # Create empty data structure
            st.session_state.cv_data = {
                "personal": {
                    "name": "",
                    "position": "",
                    "city": "",
                    "birth_year": "",
                    "availability": "",
                    "summary": "",
                    "photo": None,
                    "photo_filename": None
                },
                "experience": [],
                "education": [],
                "skills": [],
                "certifications": [],
                "languages": []
            }
            st.session_state.extraction_complete = True
            st.rerun()
        return
    
    # File upload - Enhanced Design with better messaging
    st.markdown("""
    <div style="text-align: center; margin: 2rem 0;">
        <h3 style="color: #667eea; margin-bottom: 1rem;">
            📄 Ziehe deinen Lebenslauf hierher oder klicke zum Durchsuchen
        </h3>
        <p style="color: #6c757d; font-size: 1.1rem;">
            Unterstützte Formate: PDF, DOCX, JPG, PNG (max. 10MB)
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    uploaded_file = st.file_uploader(
        "Datei hochladen:",
        type=['pdf', 'docx', 'jpg', 'png'],
        help="Drag & Drop oder durchsuchen",
        label_visibility="collapsed"
    )
    
    if uploaded_file is not None:
        # Validate file size
        if uploaded_file.size > 10 * 1024 * 1024:  # 10MB
            st.error("Datei ist zu groß! Maximum: 10MB")
            return
        
        # Show file info
        st.info(f"📄 Datei: {uploaded_file.name} ({uploaded_file.size:,} bytes)")
        
        # Extract button
        if st.button("🚀 Lebenslauf analysieren", type="primary"):
            if not os.getenv("OPENAI_API_KEY"):
                st.error("Bitte gib deinen OpenAI API Key in der Sidebar ein!")
                return
            
            with st.spinner("🤖 AI analysiert deinen Lebenslauf..."):
                try:
                    # Read file bytes
                    file_bytes = uploaded_file.read()
                    
                    # Determine file type
                    file_extension = uploaded_file.name.split(".")[-1].lower()
                    if file_extension == "pdf":
                        file_type = "pdf"
                    elif file_extension == "docx":
                        file_type = "docx"
                    elif file_extension in ["jpg", "jpeg"]:
                        file_type = "jpg"
                    elif file_extension == "png":
                        file_type = "png"
                    else:
                        st.error("Unsupported file type!")
                        return
                    
                    # Extract data using AI (run async function)
                    loop = asyncio.new_event_loop()
                    asyncio.set_event_loop(loop)
                    extracted_data = loop.run_until_complete(
                        extract_cv_data(file_bytes, file_type, os.getenv("OPENAI_API_KEY"))
                    )
                    loop.close()
                    
                    # Store in session state
                    st.session_state.cv_data = extracted_data
                    st.session_state.extraction_complete = True
                    
                    st.success("✅ Lebenslauf erfolgreich analysiert!")
                    st.rerun()
                    
                except Exception as e:
                    st.error(f"❌ Fehler bei der Analyse: {str(e)}")

def validate_current_step():
    """Validate the current step and return list of errors"""
    errors = []
    step = st.session_state.current_edit_step
    cv_data = st.session_state.cv_data
    
    if step == 1:  # Personal Data
        personal = cv_data.get("personal", {})
        if not personal.get("name") or personal.get("name").strip() == "":
            errors.append("Name ist ein Pflichtfeld")
        if not personal.get("city") or personal.get("city").strip() == "":
            errors.append("Stadt/Wohnort ist ein Pflichtfeld")
    
    elif step == 2:  # Experience
        experience = cv_data.get("experience", [])
        if len(experience) == 0:
            errors.append("Mindestens eine Berufserfahrung ist erforderlich")
        else:
            for i, exp in enumerate(experience):
                if not exp.get("position"):
                    errors.append(f"Position bei Berufserfahrung #{i+1} fehlt")
                if not exp.get("company"):
                    errors.append(f"Unternehmen bei Berufserfahrung #{i+1} fehlt")
    
    elif step == 3:  # Education & Skills
        education = cv_data.get("education", [])
        if len(education) > 0:
            for i, edu in enumerate(education):
                if not edu.get("degree"):
                    errors.append(f"Abschluss bei Ausbildung #{i+1} fehlt")
                if not edu.get("institution"):
                    errors.append(f"Institution bei Ausbildung #{i+1} fehlt")
    
    return errors

def show_progress_bar():
    """Show progress bar for current step"""
    step = st.session_state.current_edit_step
    total_steps = 4  # Personal, Experience, Education/Skills, Summary
    progress = (step - 1) / (total_steps - 1) if total_steps > 1 else 1.0
    
    # Step names
    step_names = {
        1: "👤 Persönliche Daten",
        2: "💼 Berufserfahrung",
        3: "🎓 Ausbildung & Fähigkeiten",
        4: "📋 Zusammenfassung & Export"
    }
    
    st.markdown(f"""
    <div style="background: linear-gradient(90deg, #667eea 0%, #764ba2 100%); 
                padding: 1.5rem; 
                border-radius: 12px; 
                color: white; 
                margin-bottom: 2rem;">
        <h3 style="margin: 0; color: white;">Schritt {step} von {total_steps}: {step_names.get(step, '')}</h3>
        <div style="background: rgba(255,255,255,0.3); 
                    border-radius: 10px; 
                    height: 12px; 
                    margin-top: 1rem; 
                    overflow: hidden;">
            <div style="background: white; 
                        height: 100%; 
                        width: {progress*100}%; 
                        border-radius: 10px; 
                        transition: width 0.3s ease;"></div>
        </div>
        <p style="margin: 0.5rem 0 0 0; font-size: 0.9rem; color: white;">
            {int(progress*100)}% abgeschlossen
        </p>
    </div>
    """, unsafe_allow_html=True)

def show_navigation_buttons():
    """Show navigation buttons with validation"""
    errors = validate_current_step()
    
    col1, col2, col3 = st.columns([1, 2, 1])
    
    with col1:
        if st.session_state.current_edit_step > 1:
            if st.button("← Zurück", key="nav_back", use_container_width=True):
                st.session_state.current_edit_step -= 1
                st.rerun()
    
    with col3:
        # Show errors if any
        if errors:
            st.button("Weiter →", key="nav_next", disabled=True, use_container_width=True)
        else:
            if st.session_state.current_edit_step < 4:
                if st.button("Weiter →", key="nav_next", type="primary", use_container_width=True):
                    st.session_state.current_edit_step += 1
                    st.rerun()
    
    # Show validation errors below buttons
    if errors:
        st.markdown("---")
        st.error("⚠️ **Bitte behebe folgende Fehler:**")
        for error in errors:
            st.warning(f"• {error}")

def show_edit_section():
    """Show data editing section with step-by-step navigation"""
    if not st.session_state.cv_data:
        st.error("Keine CV-Daten verfügbar!")
        return
    
    # Show progress bar
    show_progress_bar()
    
    # Show current step content
    step = st.session_state.current_edit_step
    
    if step == 1:
        edit_personal_data()
    elif step == 2:
        edit_experience_data()
    elif step == 3:
        # Combined Education & Skills & Languages
        edit_education_data()
        st.markdown("---")
        edit_skills_data()
        st.markdown("---")
        edit_languages_data()
    elif step == 4:
        show_summary_and_export()
    
    # Show navigation buttons
    st.markdown("---")
    show_navigation_buttons()

def edit_personal_data():
    """Edit personal information"""
    st.markdown('<h3 class="section-header">Persönliche Daten</h3>', unsafe_allow_html=True)
    
    st.markdown("""
    <div style="background: linear-gradient(135deg, #667eea15 0%, #764ba215 100%); 
                padding: 1rem; 
                border-radius: 12px; 
                border-left: 4px solid #667eea;
                margin-bottom: 1.5rem;">
        <p style="margin: 0; color: #1e1e1e;">
            📝 <b>Pflichtfelder:</b> Name und Stadt müssen ausgefüllt sein.
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    personal = st.session_state.cv_data.get("personal", {})
    
    # Personal data fields
    col1, col2 = st.columns(2)
    
    with col1:
        name = st.text_input("Name", value=personal.get("name", ""), help="Vollständiger Name des Kandidaten")
        position = st.text_input("Position", value=personal.get("position", ""), help="Gewünschte/Aktuelle Position")
    
    with col2:
        city = st.text_input("Stadt/Wohnort", value=personal.get("city", ""), help="Wird im Export angezeigt")
        birth_year = st.text_input("Geburtsjahr", value=personal.get("birth_year", ""),
                                  help="z.B. 1990", placeholder="1990")
        availability = st.text_input("Verfügbarkeit", value=personal.get("availability", ""),
                                    help="z.B. 'Ab sofort' oder 'ab 01.03.2024'",
                                    placeholder="Ab sofort / ab DD.MM.JJJJ")
    
    summary = st.text_area("Profilbeschreibung", value=personal.get("summary", ""), height=150, 
                          help="Kurze Zusammenfassung der Qualifikationen und Erfahrungen")
    
    # Profilbild Upload
    st.markdown("---")
    st.markdown("### 📸 Profilbild (Optional)")
    uploaded_photo = st.file_uploader(
        "Lade ein Profilbild hoch",
        type=['jpg', 'jpeg', 'png'],
        help="Quadratisches Bild empfohlen (max 2MB)",
        key="profile_photo_upload"
    )
    
    if uploaded_photo:
        # Validiere Dateigröße (2MB)
        if uploaded_photo.size > 2 * 1024 * 1024:
            st.error("Bild ist zu groß! Maximum: 2MB")
        else:
            # Bild in Base64 konvertieren für Session State
            photo_bytes = uploaded_photo.read()
            photo_base64 = base64.b64encode(photo_bytes).decode()
            st.session_state.cv_data["personal"]["photo"] = photo_base64
            st.session_state.cv_data["personal"]["photo_filename"] = uploaded_photo.name
            
            # Preview anzeigen
            col1, col2, col3 = st.columns([1, 1, 1])
            with col2:
                st.image(photo_bytes, width=150, caption="Profilbild Vorschau")
    elif st.session_state.cv_data["personal"].get("photo"):
        # Bereits hochgeladenes Bild anzeigen
        col1, col2, col3 = st.columns([1, 1, 1])
        with col2:
            photo_data = base64.b64decode(st.session_state.cv_data["personal"]["photo"])
            st.image(photo_data, width=150, caption="Aktuelles Profilbild")
            if st.button("🗑️ Bild entfernen", key="remove_photo"):
                st.session_state.cv_data["personal"]["photo"] = None
                st.session_state.cv_data["personal"]["photo_filename"] = None
                st.rerun()
    
    # Ansprechpartner Auswahl
    st.markdown("---")
    st.markdown("### 👤 Ansprechpartner auswählen")
    
    if st.session_state.company:
        try:
            sys.path.append('resources')
            if st.session_state.company == "galdora":
                from resources.contacts_galdora import get_galdora_contacts
                contacts = get_galdora_contacts()
            else:
                from resources.contacts_bejob import get_bejob_contacts
                contacts = get_bejob_contacts()
            
            contact_names = [f"{c['name']} ({c['role']})" for c in contacts]
            selected_index = st.selectbox(
                "Wähle einen Ansprechpartner für das Profil:",
                range(len(contact_names)),
                format_func=lambda i: contact_names[i]
            )
            
            st.session_state.selected_contact = contacts[selected_index]
            
            # Show selected contact info
            st.info(f"📧 {st.session_state.selected_contact['email']} | ☎️ {st.session_state.selected_contact['phone']}")
            
        except Exception as e:
            st.warning(f"Ansprechpartner konnten nicht geladen werden: {str(e)}")
    
    # Update session state - essential fields + position + availability
    # Preserve photo data if it exists
    photo_data = personal.get("photo")
    photo_filename = personal.get("photo_filename")
    
    st.session_state.cv_data["personal"] = {
        "name": name,
        "position": position,
        "city": city,
        "birth_year": birth_year,
        "availability": availability,
        "summary": summary,
        "photo": photo_data,
        "photo_filename": photo_filename
    }

def edit_experience_data():
    """Edit work experience with drag & drop"""
    st.markdown('<h3 class="section-header">Berufserfahrung</h3>', unsafe_allow_html=True)
    
    st.markdown("""
    <div style="background: linear-gradient(135deg, #667eea15 0%, #764ba215 100%); 
                padding: 1rem; 
                border-radius: 12px; 
                border-left: 4px solid #667eea;
                margin-bottom: 1.5rem;">
        <p style="margin: 0; color: #1e1e1e;">
            💼 <b>Tipp:</b> Mindestens eine Berufserfahrung mit Position und Unternehmen erforderlich.
            <br>⬆️⬇️ <b>Sortierung:</b> Nutze die Pfeiltasten um die Reihenfolge zu ändern.
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    # Initialize experience list if not exists
    if "experience" not in st.session_state.cv_data:
        st.session_state.cv_data["experience"] = []
    
    experience = st.session_state.cv_data["experience"]
    
    # Add new experience button
    add_exp = st.button("➕ Neue Berufserfahrung hinzufügen", key="add_exp_btn")
    if add_exp:
        st.session_state.cv_data["experience"].append({
            "position": "",
            "company": "",
            "start_date": "",
            "end_date": "",
            "tasks": [],
            "type": "experience"  # Track type for cross-category drag
        })
    
    st.markdown("---")
    
    # Edit existing experience
    for i, exp in enumerate(experience):
        with st.expander(f"💼 {exp.get('position', 'Neue Position')} bei {exp.get('company', 'Neues Unternehmen')}", expanded=False):
            col1, col2 = st.columns(2)
            
            with col1:
                position = st.text_input(f"Position {i+1}", value=exp.get("position", ""), key=f"pos_{i}")
                company = st.text_input(f"Unternehmen {i+1}", value=exp.get("company", ""), key=f"comp_{i}")
            
            with col2:
                start_date = month_year_picker(
                    "Start", 
                    f"exp_start_{i}", 
                    exp.get("start_date", "")
                )
                
                # End date mit "Heute" Option
                is_current = st.checkbox("Aktuell", key=f"exp_current_{i}", 
                                         value=(exp.get("end_date", "") == "Heute"))
                
                if is_current:
                    end_date = "Heute"
                else:
                    end_date = month_year_picker(
                        "Ende", 
                        f"exp_end_{i}", 
                        exp.get("end_date", "") if exp.get("end_date") != "Heute" else ""
                    )
            
            # Tasks as list (one per line)
            st.markdown("**Aufgaben** (eine pro Zeile - wird als Stichpunkte angezeigt):")
            
            # Get existing tasks or empty list
            existing_tasks = exp.get("tasks", [])
            if isinstance(existing_tasks, str):
                # If old format (description), convert to list
                existing_tasks = [existing_tasks] if existing_tasks else []
            
            tasks_text = st.text_area(
                f"Aufgaben {i+1}", 
                value="\n".join(existing_tasks),
                key=f"tasks_{i}",
                height=150,
                help="Jede Zeile wird als Stichpunkt (•) angezeigt",
                placeholder="• Aufgabe 1\n• Aufgabe 2\n• Aufgabe 3"
            )
            
            # Convert text to list (split by newlines, remove empty lines)
            tasks_list = [task.strip().lstrip('•').strip() for task in tasks_text.split("\n") if task.strip()]
            
            # Update experience
            experience[i] = {
                "position": position,
                "company": company,
                "start_date": start_date,
                "end_date": end_date,
                "tasks": tasks_list,
                "type": "experience"
            }
            
            # Show preview of bullet points
            if tasks_list:
                st.markdown("**Vorschau:**")
                for task in tasks_list:
                    st.markdown(f"• {task}")
            
            # Action buttons
            col_up, col_down, col_del, col_move = st.columns(4)
            
            with col_up:
                if i > 0:
                    if st.button(f"⬆️ Nach oben", key=f"up_exp_{i}"):
                        # Swap with previous
                        st.session_state.cv_data["experience"][i], st.session_state.cv_data["experience"][i-1] = \
                            st.session_state.cv_data["experience"][i-1], st.session_state.cv_data["experience"][i]
                        st.rerun()
            
            with col_down:
                if i < len(experience) - 1:
                    if st.button(f"⬇️ Nach unten", key=f"down_exp_{i}"):
                        # Swap with next
                        st.session_state.cv_data["experience"][i], st.session_state.cv_data["experience"][i+1] = \
                            st.session_state.cv_data["experience"][i+1], st.session_state.cv_data["experience"][i]
                        st.rerun()
            
            with col_del:
                if st.button(f"🗑️ Löschen", key=f"del_exp_{i}"):
                    st.session_state.cv_data["experience"].pop(i)
                    st.rerun()
            
            with col_move:
                if st.button(f"🔀 Zu Ausbildung", key=f"move_exp_{i}"):
                    # Move to education
                    item = st.session_state.cv_data["experience"].pop(i)
                    # Convert to education format
                    edu_item = {
                        "degree": item.get("position", ""),
                        "institution": item.get("company", ""),
                        "start_date": item.get("start_date", ""),
                        "end_date": item.get("end_date", ""),
                        "description": "\n".join(item.get("tasks", [])),
                        "type": "education"
                    }
                    if "education" not in st.session_state.cv_data:
                        st.session_state.cv_data["education"] = []
                    st.session_state.cv_data["education"].append(edu_item)
                    st.success(f"✅ '{item.get('position', 'Eintrag')}' wurde zu Ausbildung verschoben!")
                    st.rerun()
    
    # Update experience data in session state
    st.session_state.cv_data["experience"] = experience

def edit_education_data():
    """Edit education data with drag & drop"""
    st.markdown('<h3 class="section-header">Ausbildung & Weiterbildung</h3>', unsafe_allow_html=True)
    
    st.markdown("""
    <div style="background: linear-gradient(135deg, #667eea15 0%, #764ba215 100%); 
                padding: 1rem; 
                border-radius: 12px; 
                border-left: 4px solid #667eea;
                margin-bottom: 1.5rem;">
        <p style="margin: 0; color: #1e1e1e;">
            🎓 <b>Optional:</b> Füge Ausbildungen und Weiterbildungen hinzu um das Profil zu vervollständigen.
            <br>⬆️⬇️ <b>Sortierung:</b> Nutze die Pfeiltasten um die Reihenfolge zu ändern.
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    # Initialize education list if not exists
    if "education" not in st.session_state.cv_data:
        st.session_state.cv_data["education"] = []
    
    education = st.session_state.cv_data["education"]
    
    # Add new education button
    add_edu = st.button("➕ Neue Ausbildung hinzufügen", key="add_edu_btn")
    if add_edu:
        st.session_state.cv_data["education"].append({
            "degree": "",
            "institution": "",
            "start_date": "",
            "end_date": "",
            "description": "",
            "type": "education"
        })
    
    st.markdown("---")
    
    # Edit existing education
    for i, edu in enumerate(education):
        with st.expander(f"🎓 {edu.get('degree', 'Neuer Abschluss')} - {edu.get('institution', 'Neue Institution')}", expanded=False):
            col1, col2 = st.columns(2)
            
            with col1:
                degree = st.text_input(f"Abschluss {i+1}", value=edu.get("degree", ""), key=f"deg_{i}")
                institution = st.text_input(f"Institution {i+1}", value=edu.get("institution", ""), key=f"inst_{i}")
            
            with col2:
                start_date = month_year_picker(
                    "Start", 
                    f"edu_start_{i}", 
                    edu.get("start_date", "")
                )
                end_date = month_year_picker(
                    "Ende", 
                    f"edu_end_{i}", 
                    edu.get("end_date", "")
                )
            
            description = st.text_area(f"Beschreibung {i+1}", value=edu.get("description", ""), key=f"edu_desc_{i}")
            
            # Update education
            education[i] = {
                "degree": degree,
                "institution": institution,
                "start_date": start_date,
                "end_date": end_date,
                "description": description,
                "type": "education"
            }
            
            # Action buttons
            col_up, col_down, col_del, col_move = st.columns(4)
            
            with col_up:
                if i > 0:
                    if st.button(f"⬆️ Nach oben", key=f"up_edu_{i}"):
                        # Swap with previous
                        st.session_state.cv_data["education"][i], st.session_state.cv_data["education"][i-1] = \
                            st.session_state.cv_data["education"][i-1], st.session_state.cv_data["education"][i]
                        st.rerun()
            
            with col_down:
                if i < len(education) - 1:
                    if st.button(f"⬇️ Nach unten", key=f"down_edu_{i}"):
                        # Swap with next
                        st.session_state.cv_data["education"][i], st.session_state.cv_data["education"][i+1] = \
                            st.session_state.cv_data["education"][i+1], st.session_state.cv_data["education"][i]
                        st.rerun()
            
            with col_del:
                if st.button(f"🗑️ Löschen", key=f"del_edu_{i}"):
                    st.session_state.cv_data["education"].pop(i)
                    st.rerun()
            
            with col_move:
                if st.button(f"🔀 Zur Berufserfahrung", key=f"move_edu_{i}"):
                    # Move to experience
                    item = st.session_state.cv_data["education"].pop(i)
                    # Convert to experience format
                    exp_item = {
                        "position": item.get("degree", ""),
                        "company": item.get("institution", ""),
                        "start_date": item.get("start_date", ""),
                        "end_date": item.get("end_date", ""),
                        "tasks": [item.get("description", "")] if item.get("description") else [],
                        "type": "experience"
                    }
                    if "experience" not in st.session_state.cv_data:
                        st.session_state.cv_data["experience"] = []
                    st.session_state.cv_data["experience"].append(exp_item)
                    st.success(f"✅ '{item.get('degree', 'Eintrag')}' wurde zur Berufserfahrung verschoben!")
                    st.rerun()
    
    # Update education data in session state
    st.session_state.cv_data["education"] = education

def edit_skills_data():
    """Edit skills data"""
    st.markdown('<h3 class="section-header">Fähigkeiten & Kompetenzen</h3>', unsafe_allow_html=True)
    
    st.markdown("""
    <div style="background: linear-gradient(135deg, #667eea15 0%, #764ba215 100%); 
                padding: 1rem; 
                border-radius: 12px; 
                border-left: 4px solid #667eea;
                margin-bottom: 1.5rem;">
        <p style="margin: 0; color: #1e1e1e;">
            🛠️ <b>Tipp:</b> Jede Fähigkeit in eine neue Zeile (z.B. Python, React, SQL...).
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    skills = st.session_state.cv_data.get("skills", [])
    
    # Skills input
    skills_text = st.text_area(
        "Fähigkeiten (eine pro Zeile):",
        value="\n".join(skills),
        height=150,
        help="Gib jede Fähigkeit in eine neue Zeile ein"
    )
    
    # Update skills
    skills_list = [skill.strip() for skill in skills_text.split("\n") if skill.strip()]
    st.session_state.cv_data["skills"] = skills_list
    
    # Show current skills
    if skills_list:
        st.markdown("**Aktuelle Fähigkeiten:**")
        for skill in skills_list:
            st.markdown(f"• {skill}")

def edit_languages_data():
    """Edit languages with proficiency levels"""
    st.markdown('<h3 class="section-header">🌍 Sprachen</h3>', unsafe_allow_html=True)
    
    st.markdown("""
    <div style="background: linear-gradient(135deg, #667eea15 0%, #764ba215 100%); 
                padding: 1rem; 
                border-radius: 12px; 
                border-left: 4px solid #667eea;
                margin-bottom: 1.5rem;">
        <p style="margin: 0; color: #1e1e1e;">
            🗣️ <b>Tipp:</b> Füge Sprachen mit Kompetenzstufen hinzu (A1-C2 oder Beschreibung).
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    # Initialize languages list
    if "languages" not in st.session_state.cv_data:
        st.session_state.cv_data["languages"] = []
    
    languages = st.session_state.cv_data["languages"]
    
    # Add new language
    if st.button("➕ Neue Sprache hinzufügen", key="add_lang_btn"):
        st.session_state.cv_data["languages"].append({
            "name": "",
            "level": "A1",
            "type": "language"
        })
    
    st.markdown("---")
    
    # Edit existing languages
    for i, lang in enumerate(languages):
        with st.expander(f"🌍 {lang.get('name', 'Neue Sprache')}", expanded=False):
            col1, col2 = st.columns(2)
            
            with col1:
                name = st.text_input(
                    f"Sprache {i+1}",
                    value=lang.get("name", ""),
                    key=f"lang_name_{i}",
                    placeholder="z.B. Deutsch, Englisch, Französisch"
                )
            
            with col2:
                level = st.selectbox(
                    f"Kompetenzstufe {i+1}",
                    ["A1", "A2", "B1", "B2", "C1", "C2", "Muttersprache"],
                    index=["A1", "A2", "B1", "B2", "C1", "C2", "Muttersprache"].index(
                        lang.get("level", "A1")
                    ) if lang.get("level") in ["A1", "A2", "B1", "B2", "C1", "C2", "Muttersprache"] else 0,
                    key=f"lang_level_{i}",
                    help="GER (Gemeinsamer Europäischer Referenzrahmen)"
                )
            
            # Update language
            languages[i] = {
                "name": name,
                "level": level,
                "type": "language"
            }
            
            # Delete button
            if st.button(f"🗑️ Löschen", key=f"del_lang_{i}"):
                st.session_state.cv_data["languages"].pop(i)
                st.rerun()
    
    # Update languages in session state
    st.session_state.cv_data["languages"] = languages

def show_summary_and_export():
    """Show summary of all data and export options"""
    st.markdown('<h2 class="section-header">📋 Zusammenfassung & Export</h2>', unsafe_allow_html=True)
    
    st.info("🎉 **Fast geschafft!** Überprüfe alle Daten bevor du exportierst.")
    
    # Personal Data Summary with Header
    personal = st.session_state.cv_data.get("personal", {})
    
    # Header with Name and Position
    st.markdown(f"""
    <div style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); 
                padding: 2rem; 
                border-radius: 12px; 
                color: white; 
                text-align: center;
                margin-bottom: 2rem;">
        <h1 style="margin: 0; color: white; font-size: 2.5rem;">{personal.get('name', 'Name nicht angegeben')}</h1>
        <h3 style="margin: 0.5rem 0 0 0; color: white; font-weight: 400; font-size: 1.5rem;">{personal.get('position', 'Position nicht angegeben')}</h3>
    </div>
    """, unsafe_allow_html=True)
    
    # Personal Data Details
    st.markdown("---")
    col1, col2 = st.columns([4, 1])
    with col1:
        st.markdown("### 👤 Persönliche Daten")
    with col2:
        if st.button("✏️ Bearbeiten", key="edit_personal"):
            st.session_state.current_edit_step = 1
            st.rerun()
    
    col1, col2 = st.columns(2)
    with col1:
        st.write(f"**Stadt:** {personal.get('city', '-')}")
        st.write(f"**Geburtsjahr:** {personal.get('birth_year', '-')}")
        st.write(f"**Verfügbarkeit:** {personal.get('availability', '-')}")
    with col2:
        if personal.get("summary"):
            st.write(f"**Zusammenfassung:** {personal.get('summary')[:100]}...")
    
    # Experience Summary
    st.markdown("---")
    col1, col2 = st.columns([4, 1])
    with col1:
        st.markdown("### 💼 Berufserfahrung")
    with col2:
        if st.button("✏️ Bearbeiten", key="edit_experience"):
            st.session_state.current_edit_step = 2
            st.rerun()
    
    experience = st.session_state.cv_data.get("experience", [])
    if experience:
        st.write(f"**{len(experience)} Position(en)**")
        for i, exp in enumerate(experience):  # Show all
            st.write(f"• {exp.get('position', 'Unbekannt')} bei {exp.get('company', 'Unbekannt')} ({exp.get('start_date', '?')} - {exp.get('end_date', '?')})")
    else:
        st.write("Keine Berufserfahrung hinzugefügt")
    
    # Education Summary
    st.markdown("---")
    col1, col2 = st.columns([4, 1])
    with col1:
        st.markdown("### 🎓 Ausbildung & Fähigkeiten")
    with col2:
        if st.button("✏️ Bearbeiten", key="edit_education"):
            st.session_state.current_edit_step = 3
            st.rerun()
    
    education = st.session_state.cv_data.get("education", [])
    if education:
        st.write(f"**{len(education)} Abschluss/Abschlüsse**")
        for edu in education:  # Show all
            st.write(f"• {edu.get('degree', 'Unbekannt')} - {edu.get('institution', 'Unbekannt')}")
    else:
        st.write("Keine Ausbildung hinzugefügt")
    
    skills = st.session_state.cv_data.get("skills", [])
    if skills:
        st.write(f"**{len(skills)} Fähigkeit(en):** {', '.join(skills)}")
    
    # Export Options
    st.markdown("---")
    st.markdown("### 🎨 Export-Einstellungen")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("**Profilvorlage**")
        if st.button("📄 Modern", key="template_modern", use_container_width=True,
                     type="primary" if st.session_state.template == "modern" else "secondary"):
            st.session_state.template = "modern"
        if st.button("📋 Classic", key="template_classic", use_container_width=True,
                     type="primary" if st.session_state.template == "classic" else "secondary"):
            st.session_state.template = "classic"
        
        st.markdown("**Aufgaben-Anzeige**")
        limit_tasks = st.checkbox(
            "Max 5 Aufgaben pro Eintrag",
            value=st.session_state.export_options.get("limit_tasks", True),
            help="Begrenzt die Anzahl der Aufgaben-Stichpunkte im Export auf 5"
        )
        st.session_state.export_options["limit_tasks"] = limit_tasks
    
    with col2:
        st.markdown("**Datenschutz**")
        anonymize = st.checkbox(
            "Name anonymisieren",
            value=st.session_state.anonymize,
            help="z.B. 'Max M.' statt 'Max Mustermann'"
        )
        st.session_state.anonymize = anonymize

        st.markdown("**Export Optionen**")
        show_summary = st.checkbox(
            "Zusammenfassung einblenden",
            value=st.session_state.get("show_summary", True),
            help="Profilzusammenfassung im Export anzeigen"
        )
        st.session_state.show_summary = show_summary

        st.write(f"🏢 **Unternehmen:** {st.session_state.company.capitalize()}")

    # Languages Summary
    languages = st.session_state.cv_data.get("languages", [])
    if languages:
        st.markdown("---")
        col1, col2 = st.columns([4, 1])
        with col1:
            st.markdown("### 🌍 Sprachen")
        with col2:
            if st.button("✏️ Bearbeiten", key="edit_languages"):
                st.session_state.current_edit_step = 3 # Languages are part of step 3
                st.rerun()

        st.write(f"**{len(languages)} Sprache(n):**")
        for lang in languages: # Show all
            st.write(f"• {lang.get('name', 'Unbekannt')} - {lang.get('level', 'Unbekannt')}")

    # Preview Section
    st.markdown("---")
    st.markdown("### 👁️ Profilvorschau")
    
    if st.button("🔍 Vorschau generieren", type="secondary", use_container_width=True):
        try:
            # Prepare data for preview
            export_data = prepare_export_data(st.session_state.cv_data, st.session_state.anonymize)
            
            # Generate HTML preview
            html_content = render_profile_html(export_data, st.session_state.company)
            
            # Show preview in expandable section
            with st.expander("📄 HTML Vorschau", expanded=True):
                st.components.v1.html(html_content, height=800, scrolling=True)
            
            st.success("✅ Vorschau erfolgreich generiert!")
            
        except Exception as e:
            st.error(f"❌ Fehler beim Generieren der Vorschau: {str(e)}")
    
    # Export Buttons
    st.markdown("---")
    st.markdown("### 📥 Profil herunterladen")
    
    col1, col2 = st.columns(2)
    
    with col1:
        if st.button("📄 Als PDF speichern", type="primary", use_container_width=True):
            try:
                export_data = prepare_export_data(st.session_state.cv_data, st.session_state.anonymize)
                
                # Generate HTML (same as preview)
                html_content = render_profile_html(export_data, st.session_state.company)
                
                # Add print-friendly CSS
                exporter = ProfileExporter()
                html_for_print = exporter.html_to_pdf(html_content)
                
                # Show HTML in new page with print button
                st.markdown("---")
                st.success("✅ Profil bereit zum Drucken!")
                st.info("💡 **Anleitung:** Klicke unten auf 'Profil in neuem Tab öffnen', dann drücke `Cmd+P` (Mac) oder `Strg+P` (Windows) und wähle 'Als PDF speichern'.")
                
                # Create download for HTML
                st.download_button(
                    label="📄 Profil in neuem Tab öffnen",
                    data=html_for_print,
                    file_name=f"profile_{st.session_state.company}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.html",
                    mime="text/html",
                    use_container_width=True
                )
                
            except Exception as e:
                st.error(f"Fehler beim Export: {str(e)}")
    
    with col2:
        if st.button("📝 Als Word herunterladen", type="secondary", use_container_width=True):
            try:
                export_data = prepare_export_data(st.session_state.cv_data, st.session_state.anonymize)
                exporter = ProfileExporter()
                docx_bytes = exporter.generate_docx(export_data, st.session_state.company)
                
                st.download_button(
                    label="📥 Word herunterladen",
                    data=docx_bytes,
                    file_name=f"profile_{st.session_state.company}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.docx",
                    mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document",
                    use_container_width=True
                )
            except Exception as e:
                st.error(f"Fehler beim Word-Export: {str(e)}")

def show_preview_and_export():
    """Show preview and export options"""
    st.markdown('<h3 class="section-header">Vorschau & Export</h3>', unsafe_allow_html=True)
    
    # Template Selection
    st.markdown("### 🎨 Profilvorlage auswählen")
    col1, col2 = st.columns(2)
    
    with col1:
        if st.button("📄 Modern", key="template_modern", use_container_width=True,
                     type="primary" if st.session_state.template == "modern" else "secondary"):
            st.session_state.template = "modern"
    
    with col2:
        if st.button("📋 Classic", key="template_classic", use_container_width=True,
                     type="primary" if st.session_state.template == "classic" else "secondary"):
            st.session_state.template = "classic"
    
    st.success(f"✅ Ausgewählte Vorlage: **{st.session_state.template.capitalize()}**")
    
    st.markdown("---")
    
    # Anonymisierung Toggle
    st.markdown("### 🔒 Datenschutz-Optionen")
    anonymize = st.checkbox(
        "Name anonymisieren (z.B. 'Max M.' statt 'Max Mustermann')",
        value=st.session_state.anonymize,
        help="Aktiviere diese Option um den Namen im Export zu anonymisieren"
    )
    st.session_state.anonymize = anonymize
    
    if anonymize:
        st.info("ℹ️ Im Export werden folgende Daten angepasst:\n- Name wird anonymisiert (nur Vorname + Anfangsbuchstabe)\n- E-Mail und Telefon werden versteckt\n- Nur Wohnort wird angezeigt (nicht vollständige Adresse)")
    
    st.markdown("---")
    
    # Generate preview
    if st.button("👁️ Vorschau generieren", type="primary"):
        try:
            # Prepare data for export (with or without anonymization)
            export_data = prepare_export_data(st.session_state.cv_data, st.session_state.anonymize)
            
            html_content = render_profile_html(export_data, st.session_state.company)
            
            # Show preview in iframe
            st.markdown("### 📄 Profilvorschau")
            st.components.v1.html(html_content, height=800, scrolling=True)
            
        except Exception as e:
            st.error(f"Fehler beim Generieren der Vorschau: {str(e)}")
    
    # Export buttons
    st.markdown("### 📥 Export")
    
    col1, col2 = st.columns(2)
    
    with col1:
        if st.button("📄 Als PDF speichern", type="secondary"):
            try:
                # Prepare data for export (with or without anonymization)
                export_data = prepare_export_data(st.session_state.cv_data, st.session_state.anonymize)
                
                # Generate HTML (same as preview)
                html_content = render_profile_html(export_data, st.session_state.company)
                
                # Add print-friendly CSS
                exporter = ProfileExporter()
                html_for_print = exporter.html_to_pdf(html_content)
                
                st.success("✅ Profil bereit!")
                st.info("💡 Öffne die HTML-Datei und drücke Cmd+P / Strg+P zum Drucken als PDF.")
                
                st.download_button(
                    label="📄 HTML öffnen",
                    data=html_for_print,
                    file_name=f"profile_{st.session_state.company}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.html",
                    mime="text/html"
                )
                
            except Exception as e:
                st.error(f"Fehler beim Export: {str(e)}")
    
    with col2:
        if st.button("📝 Als Word herunterladen", type="secondary"):
            try:
                # Prepare data for export (with or without anonymization)
                export_data = prepare_export_data(st.session_state.cv_data, st.session_state.anonymize)
                
                exporter = ProfileExporter()
                docx_bytes = exporter.generate_docx(export_data, st.session_state.company)
                
                st.download_button(
                    label="Word herunterladen",
                    data=docx_bytes,
                    file_name=f"profile_{st.session_state.company}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.docx",
                    mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document"
                )
                
            except Exception as e:
                st.error(f"Fehler beim Word-Export: {str(e)}")

def prepare_export_data(cv_data, anonymize=False):
    """
    Prepare CV data for export with privacy/anonymization options
    According to EXPORT_DISPLAY_RULES:
    - Hide email and phone
    - Show only city (not full address)
    - Optionally anonymize name
    """
    import copy
    from resources.extraction_rules import anonymize_name, extract_city_from_address
    
    export_data = copy.deepcopy(cv_data)
    personal = export_data.get("personal", {})
    
    # Always hide email and phone in export (as per requirements)
    personal["email"] = ""
    personal["phone"] = ""
    
    # Show only city, not full address
    if personal.get("address") and not personal.get("city"):
        personal["city"] = extract_city_from_address(personal["address"])
    personal["address"] = personal.get("city", "")
    
    # Anonymize name if requested
    if anonymize and personal.get("name"):
        personal["name"] = anonymize_name(personal["name"])
    
    export_data["personal"] = personal
    
    # Add export options
    export_data["_export_options"] = {
        "limit_tasks": st.session_state.export_options.get("limit_tasks", True),
        "show_summary": st.session_state.get("show_summary", True)
    }
    
    return export_data

if __name__ == "__main__":
    main()
