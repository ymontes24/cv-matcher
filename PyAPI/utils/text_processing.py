import re
import io
from typing import List, Dict, Any
import docx2txt
import PyPDF2
from core.logging import app_logger
from core.config import settings

def extract_text_from_file(file_content: bytes, file_extension: str) -> str:

    try:
        file_extension = file_extension.lower()
        if file_extension == ".pdf":
            return clean_text(extratct_text_from_pdf(file_content))
        elif file_extension == ".docx":
            return clean_text(extract_text_from_docx(file_content))
        elif file_extension == ".txt":
            return clean_text(extract_text_from_txt(file_content))
        else:
            raise ValueError("Unsupported file format for PDF extraction.")
    except Exception as e:
        app_logger.error(f"Error extracting text from PDF: {e}")
        raise ValueError("Error extracting text from PDF.")
    
def extratct_text_from_pdf(file_content: bytes) -> str:
    try:
        pdf_file = io.BytesIO(file_content)
        reader = PyPDF2.PdfReader(pdf_file)
        text = ""
        for page in reader.pages:
            text += page.extract_text() + "\n"
        return text.strip()
    except Exception as e:
        app_logger.error(f"Error extracting text from PDF: {e}")
        raise ValueError("Error extracting text from PDF.")
    
def extract_text_from_docx(file_content: bytes) -> str:
    try:
        docx_file = io.BytesIO(file_content)
        text = docx2txt.process(docx_file)
        return text.strip()
    except Exception as e:
        app_logger.error(f"Error extracting text from DOCX: {e}")
        raise ValueError("Error extracting text from DOCX.")
    
def extract_text_from_txt(file_content: bytes) -> str:
    try:
        text = file_content.decode('utf-8')
        return text.strip()
    except Exception as e:
        app_logger.error(f"Error extracting text from TXT: {e}")
        raise ValueError("Error extracting text from TXT.")
    
def clean_text(text: str) -> str:
    """
    Limpia el texto eliminando caracteres especiales y espacios en blanco innecesarios
    """
    # Eliminar caracteres de control y espacios múltiples
    text = re.sub(r'[\x00-\x08\x0B\x0C\x0E-\x1F\x7F]', '', text)
    text = re.sub(r'\s+', ' ', text)
    
    # Eliminar espacios en blanco al principio y al final
    text = text.strip()
    
    return text