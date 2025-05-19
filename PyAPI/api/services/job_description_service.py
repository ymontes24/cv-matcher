from bson import ObjectId
from db.mongodb import mongodb
from core.logging import app_logger
from api.models.job_description import JobDescriptionCreate, JobDescription, JobDescriptionResponse
from api.services.embedding_service import create_embeddings,insert_embeddings

async def create_job_description(job_description_data: JobDescriptionCreate) -> JobDescription:
    jd = JobDescription(
        job_title=job_description_data.job_title,
        job_description=job_description_data.job_description,
        company_name=job_description_data.company_name,
        location=job_description_data.location,
        salary_range=job_description_data.salary_range
    )

    try:
        result = await mongodb.db['job_descriptions'].insert_one(jd.dict())
        jd.id = str(result.inserted_id)
        app_logger.info(f"Job description created with ID: {jd.id}")
        
        app_logger.info("Creating embeddings...")
        embeddings = await create_embeddings(jd.job_description)
        app_logger.info("Embeddings created successfully.")

        app_logger.info("Inserting job description embeddings into the database...")
        await insert_embeddings(mongodb.db['job_description_embeddings'], jd.id, embeddings)
        app_logger.info("Job description embeddings inserted successfully.")

        return jd
    except Exception as e:
        app_logger.error(f"Error creating job description: {e}")
        raise e
    
async def get_job_description_by_id(job_description_id: str) -> JobDescriptionResponse:
    try:
        job_description = await mongodb.db['job_descriptions'].find_one({"_id": ObjectId(job_description_id)})
        if not job_description:
            app_logger.warning(f"Job description with ID {job_description_id} not found.")
            return None
        return JobDescriptionResponse(**job_description)
    except Exception as e:
        app_logger.error(f"Error retrieving job description: {e}")
        raise e