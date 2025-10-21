"""
HTML template rendering for CV profiles
Supports Classic template with company-specific styling
"""

from typing import Dict, Any, List
from jinja2 import Template
import os


class TemplateRenderer:
    def __init__(self):
        self.template_dir = os.path.join(os.path.dirname(__file__), '..', 'templates')
    
    def render_profile_html(self, data: Dict[str, Any], company: str = "galdora", template_type: str = "modern") -> str:
        """
        Render profile HTML based on extracted CV data and company
        """
        if template_type == "classic":
            template_html = self._get_classic_template()
        else:
            template_html = self._get_modern_template()
        
        template = Template(template_html)
        
        # Prepare data for template
        template_data = self._prepare_template_data(data, company)
        
        return template.render(**template_data)
    
    def _get_modern_template(self) -> str:
        """Get the Modern template HTML"""
        return """
<!DOCTYPE html>
<html lang="de">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Profil - {{ personal.name }}</title>
    <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }
        
        body {
            font-family: 'Arial', sans-serif;
            line-height: 1.6;
            color: #333;
            background: #f8f9fa;
        }
        
        .profile-container {
            max-width: 210mm;
            margin: 0 auto;
            background: white;
            box-shadow: 0 0 20px rgba(0,0,0,0.1);
            min-height: 297mm;
        }
        
        .header {
            background: linear-gradient(135deg, {{ company_colors.primary }} 0%, {{ company_colors.secondary }} 100%);
            color: white;
            padding: 20px 40px;
            height: 40mm;
            display: flex;
            justify-content: space-between;
            align-items: center;
        }
        
        .header-left {
            flex: 1;
        }
        
        .header h1 {
            font-size: 2em;
            margin-bottom: 8px;
            font-weight: 600;
        }
        
        .header-info {
            display: flex;
            flex-direction: column;
            gap: 5px;
            font-size: 0.95em;
            margin-top: 8px;
        }
        
        .header-info span {
            white-space: nowrap;
        }
        
        .header-logo {
            max-height: 35mm;
            max-width: 80mm;
            object-fit: contain;
        }
        
        .profile-section {
            padding: 30px 40px;
            background: #f8f9fa;
            border-bottom: 2px solid {{ company_colors.primary }};
        }
        
        .summary-box {
            background: white;
            padding: 20px;
            border-radius: 8px;
            border-left: 4px solid {{ company_colors.primary }};
            margin-bottom: 20px;
            line-height: 1.6;
        }
        
        .contact-person {
            background: white;
            padding: 15px 20px;
            border-radius: 8px;
            display: flex;
            gap: 30px;
            flex-wrap: wrap;
            font-size: 0.9em;
        }
        
        .contact-person strong {
            color: {{ company_colors.primary }};
        }
        
        .main-content {
            padding: 40px;
            padding-bottom: 80px;
        }
        
        .section {
            margin-bottom: 40px;
        }
        
        .section-title {
            color: {{ company_colors.primary }};
            font-size: 1.4em;
            margin-bottom: 20px;
            padding-bottom: 10px;
            border-bottom: 2px solid {{ company_colors.primary }};
            font-weight: 600;
        }
        
        .experience-item, .education-item {
            margin-bottom: 25px;
            padding-left: 20px;
            border-left: 3px solid {{ company_colors.primary }};
            page-break-inside: avoid;
        }
        
        .item-header {
            display: flex;
            justify-content: space-between;
            align-items: flex-start;
            margin-bottom: 10px;
            flex-wrap: wrap;
        }
        
        .item-title {
            font-weight: 600;
            color: #2c3e50;
            font-size: 1.1em;
        }
        
        .item-company {
            color: {{ company_colors.primary }};
            font-weight: 500;
        }
        
        .item-dates {
            color: #666;
            font-size: 0.9em;
            white-space: nowrap;
        }
        
        .item-description {
            color: #555;
            line-height: 1.5;
        }
        
        .item-tasks {
            margin: 10px 0 0 20px;
            list-style: disc;
            color: #555;
        }
        
        .item-tasks li {
            margin-bottom: 5px;
            line-height: 1.6;
        }
        
        .skills-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
            gap: 15px;
        }
        
        .skill-item {
            background: #f8f9fa;
            padding: 10px 15px;
            border-radius: 5px;
            border-left: 4px solid {{ company_colors.primary }};
        }
        
        .summary {
            background: #f8f9fa;
            padding: 20px;
            border-radius: 8px;
            border-left: 4px solid {{ company_colors.primary }};
            font-style: italic;
            line-height: 1.6;
        }
        
        .certification-item {
            display: flex;
            justify-content: space-between;
            align-items: center;
            padding: 10px 0;
            border-bottom: 1px solid #eee;
        }
        
        .certification-item:last-child {
            border-bottom: none;
        }
        
        .cert-name {
            font-weight: 500;
            color: #2c3e50;
        }
        
        .cert-issuer {
            color: #666;
            font-size: 0.9em;
        }
        
        .cert-date {
            color: #666;
            font-size: 0.9em;
        }
        
        .page-footer {
            display: none;
        }
        
        @media print {
            body { 
                background: white; 
            }
            
            .profile-container { 
                box-shadow: none; 
                max-width: 100%;
                padding-bottom: 30mm;
            }
            
            .main-content {
                padding-bottom: 30mm;
            }
            
            .page-footer {
                display: block;
                position: fixed;
                bottom: 5mm;
                left: 0;
                right: 0;
                text-align: center;
                font-size: 9pt;
                color: #666;
                padding: 5mm 0;
                background: white;
            }
            
            .section {
                page-break-before: avoid;
            }
            
            .section-title {
                page-break-after: avoid;
                padding-top: 10mm;
            }
            
            .header + .profile-section + .main-content .section-title:first-child,
            .header + .main-content .section-title:first-child {
                padding-top: 0;
            }
            
            @page {
                size: A4;
                margin: 30mm 15mm 20mm 15mm;
            }
        }
    </style>
</head>
<body>
    <div class="profile-container">
        <!-- Header Section -->
        <div class="header">
            <div class="header-left">
                <h1>{{ personal.name }}</h1>
                <div class="header-info">
                    {% if personal.position %}<span>{{ personal.position }}</span>{% endif %}
                    {% if personal.city %}<span>📍 {{ personal.city }}</span>{% endif %}
                    {% if personal.birth_year %}<span>🎂 {{ personal.birth_year }}</span>{% endif %}
                </div>
            </div>
            {% if company_logo %}
            <img src="{{ company_logo }}" alt="{{ company_name }}" class="header-logo">
            {% endif %}
        </div>
        
        <!-- Profile Section (Summary + Contact Person) -->
        {% if show_summary or contact_person %}
        <div class="profile-section">
            {% if show_summary and personal.summary %}
            <div class="summary-box">
                <strong style="color: {{ company_colors.primary }}; display: block; margin-bottom: 10px;">Profil</strong>
                {{ personal.summary }}
            </div>
            {% endif %}
            
            {% if contact_person %}
            <div class="contact-person">
                <span><strong>Ansprechpartner:</strong> {{ contact_person.name }}</span>
                <span><strong>E-Mail:</strong> {{ contact_person.email }}</span>
                <span><strong>Tel:</strong> {{ contact_person.phone }}</span>
            </div>
            {% endif %}
        </div>
        {% endif %}
        
        <!-- Main Content -->
        <div class="main-content">
            <!-- Professional Experience -->
            {% if experience %}
            <div class="section">
                <h2 class="section-title">Berufserfahrung</h2>
                {% for exp in experience %}
                <div class="experience-item">
                    <div class="item-header">
                        <div>
                            <div class="item-title">{{ exp.position }}</div>
                            <div class="item-company">{{ exp.company }}</div>
                        </div>
                        <div class="item-dates">{{ exp.start_date }} - {{ exp.end_date }}</div>
                    </div>
                    {% if exp.tasks %}
                    <ul class="item-tasks">
                        {% for task in exp.tasks %}<li>{{ task }}</li>{% endfor %}
                    </ul>
                    {% endif %}
                </div>
                {% endfor %}
            </div>
            {% endif %}
            
            <!-- Education -->
            {% if education %}
            <div class="section">
                <h2 class="section-title">Ausbildung & Weiterbildung</h2>
                {% for edu in education %}
                <div class="education-item">
                    <div class="item-header">
                        <div>
                            <div class="item-title">{{ edu.degree }}</div>
                            <div class="item-company">{{ edu.institution }}</div>
                        </div>
                        <div class="item-dates">{{ edu.start_date }} - {{ edu.end_date }}</div>
                    </div>
                    {% if edu.description %}
                    <div class="item-description">{{ edu.description }}</div>
                    {% endif %}
                </div>
                {% endfor %}
            </div>
            {% endif %}
            
            <!-- Skills -->
            {% if skills %}
            <div class="section">
                <h2 class="section-title">Fähigkeiten & Kompetenzen</h2>
                <div class="skills-grid">
                    {% for skill in skills %}
                    <div class="skill-item">{{ skill }}</div>
                    {% endfor %}
                </div>
            </div>
            {% endif %}
            
            <!-- Certifications -->
            {% if certifications %}
            <div class="section">
                <h2 class="section-title">Zertifizierungen</h2>
                {% for cert in certifications %}
                <div class="certification-item">
                    <div>
                        <div class="cert-name">{{ cert.name }}</div>
                        <div class="cert-issuer">{{ cert.issuer }}</div>
                    </div>
                    <div class="cert-date">{{ cert.date }}</div>
                </div>
                {% endfor %}
            </div>
            {% endif %}
        </div>
    </div>
    
    <!-- Footer for print -->
    <div class="page-footer">
        Mail: info@galdora.de / Tel. 02161 6212600 / Adr. Volksgartenstraße 85-88 Mönchengladbach
    </div>
</body>
</html>
        """
    
    def _get_classic_template(self) -> str:
        """Get the Classic template HTML"""
        return """
<!DOCTYPE html>
<html lang="de">
<head>
    <meta charset="UTF-8">
    <title>Profil - {{ personal.name }}</title>
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }
        body { font-family: Arial, sans-serif; font-size: 11pt; line-height: 1.4; }
        .container { max-width: 210mm; margin: 0 auto; padding: 20mm 15mm; background: white; }
        
        .logo { max-width: 200px; margin-bottom: 30px; }
        h1 { font-size: 24pt; color: {{ company_colors.primary }}; margin-bottom: 5px; font-weight: 700; letter-spacing: -0.5px; }
        h2 { font-size: 14pt; margin-bottom: 15px; font-weight: 600; }
        
        .contact-box { background: #f5f5f5; padding: 15px; margin: 20px 0; border-left: 3px solid {{ company_colors.primary }}; }
        .contact-box strong { display: block; margin-bottom: 5px; }
        
        .info-grid { display: grid; grid-template-columns: auto 1fr; gap: 5px 15px; margin: 20px 0; }
        .info-grid strong { text-align: right; }
        
        .section { margin: 25px 0; page-break-inside: avoid; }
        .section h3 { font-size: 12pt; border-bottom: 1px solid #000; padding-bottom: 5px; margin-bottom: 15px; }
        
        .experience-item { display: grid; grid-template-columns: 150px 1fr; gap: 15px; margin-bottom: 20px; page-break-inside: avoid; }
        .experience-item .date { font-weight: bold; white-space: nowrap; }
        .experience-item .company { font-weight: bold; }
        .experience-item .position { font-style: italic; margin-bottom: 5px; }
        .experience-item ul { margin-left: 20px; }
        .experience-item li { margin-bottom: 3px; }
        
        .skills-grid { display: grid; grid-template-columns: repeat(auto-fit, minmax(180px, 1fr)); gap: 10px; }
        .skill-box { background: #f5f5f5; padding: 10px 15px; border-left: 3px solid {{ company_colors.primary }}; font-size: 10pt; }
        
        .page-footer { display: none; }
        
        @media print {
            .container { padding-bottom: 30mm; max-width: 100%; }
            .page-footer {
                display: block; position: fixed; bottom: 5mm; left: 0; right: 0;
                text-align: center; font-size: 9pt; color: #666; padding: 5mm 0; background: white;
            }
            .section { page-break-inside: avoid; }
            .section h3 { padding-top: 10mm; page-break-after: avoid; }
            .logo + h1 + h2 + .contact-box + .info-grid + .section h3,
            .logo + h1 + h2 + .info-grid + .section h3 { padding-top: 0; }
            @page { size: A4; margin: 30mm 15mm 20mm 15mm; }
        }
    </style>
</head>
<body>
    <div class="container">
        {% if company_logo %}<img src="{{ company_logo }}" class="logo">{% endif %}
        
        <h1>Profil</h1>
        <h2>{{ personal.name }}</h2>
        
        {% if contact_person %}
        <div class="contact-box">
            <strong>IHR ANSPRECHPARTNER</strong>
            {{ contact_person.name }}<br>
            Telefon: {{ contact_person.phone }}<br>
            E-Mail: {{ contact_person.email }}
        </div>
        {% endif %}
        
        <div class="info-grid">
            {% if personal.city %}<strong>Wohnort:</strong><span>{{ personal.city }}</span>{% endif %}
            {% if personal.birth_year %}<strong>Jahrgang:</strong><span>{{ personal.birth_year }}</span>{% endif %}
            {% if personal.position %}<strong>Position:</strong><span>{{ personal.position }}</span>{% endif %}
        </div>
        
        {% if show_summary and personal.summary %}
        <div class="section">
            <p>{{ personal.summary }}</p>
        </div>
        {% endif %}
        
        {% if experience %}
        <div class="section">
            <h3>Beruflicher Werdegang</h3>
            {% for exp in experience %}
            <div class="experience-item">
                <div class="date">{{ exp.start_date }} – {{ exp.end_date }}</div>
                <div>
                    <div class="company">{{ exp.company }}</div>
                    <div class="position">{{ exp.position }}</div>
                    {% if exp.tasks %}
                    <ul>
                        {% for task in exp.tasks %}<li>{{ task }}</li>{% endfor %}
                    </ul>
                    {% endif %}
                </div>
            </div>
            {% endfor %}
        </div>
        {% endif %}
        
        {% if education %}
        <div class="section">
            <h3>Ausbildung/ Weiterbildung</h3>
            {% for edu in education %}
            <div class="experience-item">
                <div class="date">{{ edu.start_date }} – {{ edu.end_date }}</div>
                <div>
                    <div class="company">{{ edu.degree }}</div>
                    <div class="position">{{ edu.institution }}</div>
                    {% if edu.description %}<p>{{ edu.description }}</p>{% endif %}
                </div>
            </div>
            {% endfor %}
        </div>
        {% endif %}
        
        {% if skills %}
        <div class="section">
            <h3>Fähigkeiten & Kompetenzen</h3>
            <div class="skills-grid">
                {% for skill in skills %}
                <div class="skill-box">{{ skill }}</div>
                {% endfor %}
            </div>
        </div>
        {% endif %}
    </div>
    
    <div class="page-footer">
        Mail: info@galdora.de / Tel. 02161 6212600 / Adr. Volksgartenstraße 85-88 Mönchengladbach
    </div>
</body>
</html>
        """
    
    def _prepare_template_data(self, data: Dict[str, Any], company: str) -> Dict[str, Any]:
        """Prepare data for template rendering"""
        import base64
        
        # Load logos as base64
        def get_logo_base64(filename):
            logo_path = os.path.join(os.path.dirname(__file__), '..', '..', 'ressources', filename)
            if os.path.exists(logo_path):
                with open(logo_path, 'rb') as f:
                    return f"data:image/png;base64,{base64.b64encode(f.read()).decode()}"
            return None
        
        # Company-specific configurations
        company_configs = {
            "galdora": {
                "name": "Galdora",
                "logo": get_logo_base64("galdoralogo.png"),
                "colors": {
                    "primary": "#1e3a8a",  # Blue
                    "secondary": "#3b82f6"  # Light blue
                }
            },
            "bejob": {
                "name": "BeJob",
                "logo": get_logo_base64("bejob-logo.png"),
                "colors": {
                    "primary": "#059669",  # Green
                    "secondary": "#10b981"  # Light green
                }
            }
        }
        
        config = company_configs.get(company.lower(), company_configs["galdora"])
        
        return {
            "personal": data.get("personal", {}),
            "experience": data.get("experience", []),
            "education": data.get("education", []),
            "skills": data.get("skills", []),
            "certifications": data.get("certifications", []),
            "company_name": config["name"],
            "company_logo": config["logo"],
            "company_colors": config["colors"],
            "show_summary": data.get("show_summary", True),
            "contact_person": data.get("contact_person", None)
        }


# Convenience function for direct usage
def render_profile_html(data: Dict[str, Any], company: str = "galdora", template_type: str = "modern") -> str:
    """Render profile HTML from CV data"""
    renderer = TemplateRenderer()
    return renderer.render_profile_html(data, company, template_type)
