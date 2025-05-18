from fastapi import APIRouter, HTTPException, Form
from typing import Optional
from core.config import settings
from api.models.job_description import JobDescriptionCreate, JobDescriptionResponse
from api.services.job_description_service import create_job_description

router = APIRouter()

@router.post("/", response_model=JobDescriptionResponse)
async def create_job_description_route(
    job_title: str = Form(...),
    job_description: str = Form(...),
    company_name: Optional[str] = Form(None),
    location: Optional[str] = Form(None),
    salary_range: Optional[str] = Form(None),
):
    try:
        if not all([job_title, job_description]):
            raise HTTPException(
                status_code=400,
                detail="Content must be provided."
            )

        job_description_data = JobDescriptionCreate(
            job_title=job_title,
            job_description=job_description,
            company_name=company_name,
            location=location,
            salary_range=salary_range
        )

        # Save the job description to the database
        job_description = await create_job_description(job_description_data)

        return JobDescriptionResponse(
            id=job_description.id,
            job_title=job_description.job_title,
            job_description=job_description.job_description,
            created_at=job_description.created_at,
            company_name=job_description.company_name,
            location=job_description.location,
            salary_range=job_description.salary_range
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))