from fastapi import APIRouter, HTTPException, Query
from bson import ObjectId
from api.services.mathc_service import match_cv

router = APIRouter()

def is_valid_object_id(object_id: str) -> bool:
    """Check if the given string is a valid ObjectId."""
    return ObjectId.is_valid(object_id)

@router.get("/")
async def match_cv_job_id(
    jd_id: str = Query(..., description="The ID of the job description to match against."),
):
    if not is_valid_object_id(jd_id):
        raise HTTPException(status_code=400, detail="Invalid job description ID format.")
    
    try:
        matched_job_description = await match_cv(jd_id)
        
        if not matched_job_description:
            raise HTTPException(status_code=404, detail="No matching job description found.")
        
        return matched_job_description
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
