from typing import List, Dict, Any, Optional
from bson import ObjectId
from db.mongodb import mongodb
from core.logging import app_logger
from api.models.documents import CVCreate, CV
from api.services.embedding_service import create_embeddings

async def create_cv(cv_data: CVCreate) -> CV:
    cv = CV(
        title=cv_data.title,
        content=cv_data.content,
        candidate_name=cv_data.candidate_name,
    )

    try:
        embeddings = await create_embeddings(cv.content)
        result = await mongodb.db['cvs'].insert_one(cv.dict())
        cv.id = str(result.inserted_id)
        app_logger.info(f"CV created with ID: {cv.id}")
        return cv
    except Exception as e:
        app_logger.error(f"Error creating CV: {e}")
        raise e