from fastapi import APIRouter, HTTPException, UploadFile, File, Form, Depends
from typing import List, Optional
from core.config import settings
from utils.text_processing import extract_text_from_file
from api.models.documents import CVCreate

router = APIRouter()

@router.post("/cvs")
async def create_new_document(
    title: str = Form(...),
    candidate_name: str = Form(...),
    file: Optional[UploadFile] = File(None),
    content: Optional[str] = Form(None),
):
    try:
        if file is None and content is None:
            raise HTTPException(
                status_code=400,
                detail="Either file or content must be provided."
            )
        
        if file:
            file_content = await file.read()
            file_extension = file.filename.split('.')[-1]
            if file_extension not in ['pdf', 'docx', 'txt']:
                raise HTTPException(
                    status_code=400,
                    detail="Unsupported file format. Only PDF, DOCX, and TXT are allowed."
                )
            text = extract_text_from_file(file_content, f".{file_extension}")

        return {"filename": "example.txt", "message": text}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))