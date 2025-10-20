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
    
    def render_profile_html(self, data: Dict[str, Any], company: str = "galdora") -> str:
        """
        Render profile HTML based on extracted CV data and company
        """
        template_html = self._get_classic_template()
        template = Template(template_html)
        
        # Prepare data for template
        template_data = self._prepare_template_data(data, company)
        
        return template.render(**template_data)
    
    def _get_classic_template(self) -> str:
        """Get the Classic template HTML"""
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
            padding: 40px;
            text-align: center;
            position: relative;
        }
        
        .company-logo {
            max-height: 60px;
            margin-bottom: 20px;
        }
        
        .header h1 {
            font-size: 2.5em;
            margin-bottom: 10px;
            font-weight: 300;
        }
        
        .header .subtitle {
            font-size: 1.2em;
            opacity: 0.9;
        }
        
        .contact-info {
            display: flex;
            justify-content: center;
            gap: 30px;
            margin-top: 20px;
            flex-wrap: wrap;
        }
        
        .contact-item {
            display: flex;
            align-items: center;
            gap: 8px;
        }
        
        .main-content {
            padding: 40px;
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
        
        @media print {
            body { background: white; }
            .profile-container { box-shadow: none; }
        }
    </style>
</head>
<body>
    <div class="profile-container">
        <!-- Header Section -->
        <div class="header">
            {% if company_logo %}
            <img src="{{ company_logo }}" alt="{{ company_name }} Logo" class="company-logo">
            {% endif %}
            <h1>{{ personal.name }}</h1>
            {% if personal.summary %}
            <div class="subtitle">{{ personal.summary }}</div>
            {% endif %}
            
            <div class="contact-info">
                {% if personal.email %}
                <div class="contact-item">
                    <span>📧</span>
                    <span>{{ personal.email }}</span>
                </div>
                {% endif %}
                {% if personal.phone %}
                <div class="contact-item">
                    <span>📞</span>
                    <span>{{ personal.phone }}</span>
                </div>
                {% endif %}
                {% if personal.address %}
                <div class="contact-item">
                    <span>📍</span>
                    <span>{{ personal.address }}</span>
                </div>
                {% endif %}
                {% if personal.linkedin %}
                <div class="contact-item">
                    <span>💼</span>
                    <span>{{ personal.linkedin }}</span>
                </div>
                {% endif %}
            </div>
        </div>
        
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
                    {% if exp.description %}
                    <div class="item-description">{{ exp.description }}</div>
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
</body>
</html>
        """
    
    def _prepare_template_data(self, data: Dict[str, Any], company: str) -> Dict[str, Any]:
        """Prepare data for template rendering"""
        # Company-specific configurations
        company_configs = {
            "galdora": {
                "name": "Galdora",
                "logo": None,  # Will be added when logo files are available
                "colors": {
                    "primary": "#1e3a8a",  # Blue
                    "secondary": "#3b82f6"  # Light blue
                }
            },
            "bejob": {
                "name": "BeJob",
                "logo": None,  # Will be added when logo files are available
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
            "company_colors": config["colors"]
        }


# Convenience function for direct usage
def render_profile_html(data: Dict[str, Any], company: str = "galdora") -> str:
    """Render profile HTML from CV data"""
    renderer = TemplateRenderer()
    return renderer.render_profile_html(data, company)
