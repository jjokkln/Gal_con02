"""
AI-based CV data extraction using OpenAI API
Supports PDF, DOCX, and image formats
"""

import base64
import io
import json
from typing import Dict, List, Any, Optional
import PyPDF2
from docx import Document
from PIL import Image
from openai import OpenAI
import httpx


class CVExtractor:
    def __init__(self, openai_api_key: str):
        # Create OpenAI client without proxies to avoid compatibility issues
        self.client = OpenAI(
            api_key=openai_api_key,
            http_client=httpx.Client()
        )
    
    async def extract_cv_data(self, file_bytes: bytes, file_type: str) -> Dict[str, Any]:
        """
        Extract structured data from CV file using OpenAI
        """
        try:
            # Extract text based on file type
            if file_type == "pdf":
                text = self._extract_pdf_text(file_bytes)
            elif file_type == "docx":
                text = self._extract_docx_text(file_bytes)
            elif file_type in ["jpg", "jpeg", "png"]:
                text = await self._extract_image_text(file_bytes)
            else:
                raise ValueError(f"Unsupported file type: {file_type}")
            
            # Use OpenAI to structure the data
            structured_data = await self._structure_with_openai(text)
            return structured_data
            
        except Exception as e:
            raise Exception(f"Error extracting CV data: {str(e)}")
    
    def _extract_pdf_text(self, file_bytes: bytes) -> str:
        """Extract text from PDF file"""
        try:
            pdf_file = io.BytesIO(file_bytes)
            pdf_reader = PyPDF2.PdfReader(pdf_file)
            text = ""
            for page in pdf_reader.pages:
                text += page.extract_text() + "\n"
            return text.strip()
        except Exception as e:
            raise Exception(f"Error reading PDF: {str(e)}")
    
    def _extract_docx_text(self, file_bytes: bytes) -> str:
        """Extract text from DOCX file"""
        try:
            doc_file = io.BytesIO(file_bytes)
            doc = Document(doc_file)
            text = ""
            for paragraph in doc.paragraphs:
                text += paragraph.text + "\n"
            return text.strip()
        except Exception as e:
            raise Exception(f"Error reading DOCX: {str(e)}")
    
    async def _extract_image_text(self, file_bytes: bytes) -> str:
        """Extract text from image using GPT-4 Vision"""
        try:
            # Convert image to base64
            base64_image = base64.b64encode(file_bytes).decode('utf-8')
            
            response = self.client.chat.completions.create(
                model="gpt-4-vision-preview",
                messages=[
                    {
                        "role": "user",
                        "content": [
                            {
                                "type": "text",
                                "text": "Extract all text from this CV image. Return only the raw text content, no formatting or analysis."
                            },
                            {
                                "type": "image_url",
                                "image_url": {
                                    "url": f"data:image/jpeg;base64,{base64_image}"
                                }
                            }
                        ]
                    }
                ],
                max_tokens=4000
            )
            
            return response.choices[0].message.content
        except Exception as e:
            raise Exception(f"Error extracting text from image: {str(e)}")
    
    async def _structure_with_openai(self, text: str) -> Dict[str, Any]:
        """Use OpenAI to structure the extracted text into CV data"""
        try:
            # Import extraction rules
            import sys
            import os
            sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..'))
            from resources.extraction_rules import EXTRACTION_USER_PROMPT, extract_city_from_address
            
            prompt = EXTRACTION_USER_PROMPT
            
            from resources.extraction_rules import EXTRACTION_SYSTEM_PROMPT
            
            response = self.client.chat.completions.create(
                model="gpt-4",
                messages=[
                    {"role": "system", "content": EXTRACTION_SYSTEM_PROMPT},
                    {"role": "user", "content": f"{prompt}\n\nCV Text:\n{text}"}
                ],
                temperature=0.1,
                max_tokens=3000
            )
            
            # Parse the JSON response
            json_text = response.choices[0].message.content.strip()
            # Remove any markdown formatting if present
            if json_text.startswith("```json"):
                json_text = json_text[7:]
            if json_text.endswith("```"):
                json_text = json_text[:-3]
            
            structured_data = json.loads(json_text)
            
            # Extract city from address if not already present
            if "personal" in structured_data and "address" in structured_data["personal"]:
                if not structured_data["personal"].get("city"):
                    structured_data["personal"]["city"] = extract_city_from_address(
                        structured_data["personal"]["address"]
                    )
            
            return structured_data
            
        except json.JSONDecodeError as e:
            raise Exception(f"Error parsing OpenAI response as JSON: {str(e)}")
        except Exception as e:
            raise Exception(f"Error structuring data with OpenAI: {str(e)}")


# Convenience function for direct usage
async def extract_cv_data(file_bytes: bytes, file_type: str, openai_api_key: str) -> Dict[str, Any]:
    """Extract CV data from file bytes"""
    extractor = CVExtractor(openai_api_key)
    return await extractor.extract_cv_data(file_bytes, file_type)
