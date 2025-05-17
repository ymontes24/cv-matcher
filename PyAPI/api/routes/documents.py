from fastapi import APIRouter, HTTPException, UploadFile, File, Form, Depends
from typing import List, Optional
from core.config import settings
from utils.text_processing import extract_text_from_file
from api.models.documents import CVCreate, CVResponse
from api.services.document_service import create_cv

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
        
        cv_data = CVCreate(
            title=title,
            candidate_name=candidate_name,
            content=text if file else content
        )

        # Save the CV to the database
        cv = await create_cv(cv_data)

        return CVResponse(
            id=cv.id,
            title=cv.title,
            created_at=cv.created_at,
            candidate_name=cv.candidate_name
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))