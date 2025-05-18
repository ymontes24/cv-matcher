from typing import List, Dict, Any, Optional
from bson import ObjectId
from db.mongodb import mongodb
from core.logging import app_logger
from api.models.documents import CVCreate, CV
from api.services.embedding_service import create_embeddings,insert_cv_embeddings

async def create_cv(cv_data: CVCreate) -> CV:
    cv = CV(
        title=cv_data.title,
        content=cv_data.content,
        candidate_name=cv_data.candidate_name,
    )

    try:
        result = await mongodb.db['cvs'].insert_one(cv.dict())
        cv.id = str(result.inserted_id)
        app_logger.info(f"CV created with ID: {cv.id}")

        app_logger.info("Creating embeddings...")
        embeddings = await create_embeddings(cv.content)
        app_logger.info("Embeddings created successfully.")

        app_logger.info("Inserting CV embeddings into the database...")
        await insert_cv_embeddings(mongodb.db['cv_embeddings'], cv.id, embeddings)
        app_logger.info("CV embeddings inserted successfully.")
        
        return cv
    except Exception as e:
        app_logger.error(f"Error creating CV: {e}")
        raise e