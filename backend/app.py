"""
FastAPI backend for CV2Profile application
Handles file upload, AI extraction, and export functionality
"""

import os
import uuid
import tempfile
import shutil
from datetime import datetime, timedelta
from typing import Dict, Any, Optional
from fastapi import FastAPI, UploadFile, File, HTTPException, Form
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse, HTMLResponse
from fastapi.staticfiles import StaticFiles
import uvicorn
from dotenv import load_dotenv

from core.extractor import extract_cv_data
from core.template_renderer import render_profile_html
from core.exporters import ProfileExporter

# Load environment variables
load_dotenv()

app = FastAPI(title="CV2Profile API", version="1.0.0")

# CORS middleware for frontend integration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Configure appropriately for production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# In-memory session storage (replace with Redis in production)
sessions: Dict[str, Dict[str, Any]] = {}

# Cleanup old sessions every hour
def cleanup_sessions():
    """Remove sessions older than 1 hour"""
    current_time = datetime.now()
    expired_sessions = []
    
    for session_id, session_data in sessions.items():
        if current_time - session_data.get("created_at", current_time) > timedelta(hours=1):
            expired_sessions.append(session_id)
    
    for session_id in expired_sessions:
        # Clean up temporary files
        if "temp_file" in sessions[session_id]:
            temp_file = sessions[session_id]["temp_file"]
            if os.path.exists(temp_file):
                os.remove(temp_file)
        del sessions[session_id]

@app.on_event("startup")
async def startup_event():
    """Initialize application"""
    # Create necessary directories
    os.makedirs("temp", exist_ok=True)
    os.makedirs("static", exist_ok=True)

@app.get("/")
async def root():
    """Health check endpoint"""
    return {"message": "CV2Profile API is running", "version": "1.0.0"}

@app.post("/api/upload")
async def upload_cv(
    file: UploadFile = File(...),
    company: str = Form("galdora")
):
    """
    Upload CV file and extract data using AI
    """
    try:
        # Validate file type
        allowed_types = ["application/pdf", "application/vnd.openxmlformats-officedocument.wordprocessingml.document", 
                        "image/jpeg", "image/png"]
        if file.content_type not in allowed_types:
            raise HTTPException(status_code=400, detail="Unsupported file type")
        
        # Validate file size (10MB max)
        file_bytes = await file.read()
        if len(file_bytes) > 10 * 1024 * 1024:
            raise HTTPException(status_code=400, detail="File too large (max 10MB)")
        
        # Get OpenAI API key
        openai_key = os.getenv("OPENAI_API_KEY")
        if not openai_key:
            raise HTTPException(status_code=500, detail="OpenAI API key not configured")
        
        # Determine file type
        file_extension = file.filename.split(".")[-1].lower()
        if file_extension == "pdf":
            file_type = "pdf"
        elif file_extension == "docx":
            file_type = "docx"
        elif file_extension in ["jpg", "jpeg"]:
            file_type = "jpg"
        elif file_extension == "png":
            file_type = "png"
        else:
            raise HTTPException(status_code=400, detail="Unsupported file extension")
        
        # Extract CV data using AI
        extracted_data = await extract_cv_data(file_bytes, file_type, openai_key)
        
        # Create session
        session_id = str(uuid.uuid4())
        
        # Save file temporarily
        temp_file = f"temp/{session_id}_{file.filename}"
        with open(temp_file, "wb") as f:
            f.write(file_bytes)
        
        # Store session data
        sessions[session_id] = {
            "id": session_id,
            "company": company,
            "original_filename": file.filename,
            "extracted_data": extracted_data,
            "created_at": datetime.now(),
            "temp_file": temp_file
        }
        
        # Cleanup old sessions
        cleanup_sessions()
        
        return {
            "session_id": session_id,
            "extracted_data": extracted_data,
            "company": company,
            "message": "CV uploaded and processed successfully"
        }
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error processing file: {str(e)}")

@app.get("/api/session/{session_id}")
async def get_session(session_id: str):
    """
    Get session data
    """
    if session_id not in sessions:
        raise HTTPException(status_code=404, detail="Session not found")
    
    session_data = sessions[session_id]
    return {
        "session_id": session_id,
        "company": session_data["company"],
        "extracted_data": session_data["extracted_data"],
        "created_at": session_data["created_at"].isoformat()
    }

@app.put("/api/session/{session_id}")
async def update_session(
    session_id: str,
    extracted_data: Dict[str, Any]
):
    """
    Update session data (for editing)
    """
    if session_id not in sessions:
        raise HTTPException(status_code=404, detail="Session not found")
    
    sessions[session_id]["extracted_data"] = extracted_data
    return {"message": "Session updated successfully"}

@app.post("/api/generate-preview/{session_id}")
async def generate_preview(session_id: str):
    """
    Generate HTML preview for the profile
    """
    if session_id not in sessions:
        raise HTTPException(status_code=404, detail="Session not found")
    
    session_data = sessions[session_id]
    extracted_data = session_data["extracted_data"]
    company = session_data["company"]
    
    try:
        html_content = render_profile_html(extracted_data, company)
        return HTMLResponse(content=html_content)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error generating preview: {str(e)}")

@app.post("/api/export/pdf/{session_id}")
async def export_pdf(session_id: str):
    """
    Export profile as PDF
    """
    if session_id not in sessions:
        raise HTTPException(status_code=404, detail="Session not found")
    
    session_data = sessions[session_id]
    extracted_data = session_data["extracted_data"]
    company = session_data["company"]
    
    try:
        # Generate PDF directly from data
        exporter = ProfileExporter()
        pdf_bytes = exporter.generate_pdf_from_data(extracted_data, company)
        
        # Save temporary PDF
        temp_pdf = f"temp/{session_id}_profile.pdf"
        with open(temp_pdf, "wb") as f:
            f.write(pdf_bytes)
        
        return FileResponse(
            temp_pdf,
            media_type="application/pdf",
            filename=f"profile_{company}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf"
        )
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error generating PDF: {str(e)}")

@app.post("/api/export/docx/{session_id}")
async def export_docx(session_id: str):
    """
    Export profile as DOCX
    """
    if session_id not in sessions:
        raise HTTPException(status_code=404, detail="Session not found")
    
    session_data = sessions[session_id]
    extracted_data = session_data["extracted_data"]
    company = session_data["company"]
    
    try:
        # Generate DOCX
        exporter = ProfileExporter()
        docx_bytes = exporter.generate_docx(extracted_data, company)
        
        # Save temporary DOCX
        temp_docx = f"temp/{session_id}_profile.docx"
        with open(temp_docx, "wb") as f:
            f.write(docx_bytes)
        
        return FileResponse(
            temp_docx,
            media_type="application/vnd.openxmlformats-officedocument.wordprocessingml.document",
            filename=f"profile_{company}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.docx"
        )
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error generating DOCX: {str(e)}")

@app.delete("/api/session/{session_id}")
async def delete_session(session_id: str):
    """
    Delete session and cleanup files
    """
    if session_id not in sessions:
        raise HTTPException(status_code=404, detail="Session not found")
    
    session_data = sessions[session_id]
    
    # Clean up temporary files
    if "temp_file" in session_data and os.path.exists(session_data["temp_file"]):
        os.remove(session_data["temp_file"])
    
    # Remove session
    del sessions[session_id]
    
    return {"message": "Session deleted successfully"}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
