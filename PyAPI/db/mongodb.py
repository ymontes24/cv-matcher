from motor.motor_asyncio import AsyncIOMotorClient
from core.config import settings
from core.logging import app_logger

class MongoDB:
    client: AsyncIOMotorClient = None
    db = None
    collection_cvs = None
    collection_job_descriptions = None

mongodb = MongoDB()

async def connect_to_mongo():
    """Establece la conexión con MongoDB"""
    app_logger.info("Conectando a MongoDB...")
    
    mongodb.client = AsyncIOMotorClient(settings.MONGODB_URL)
    mongodb.db = mongodb.client[settings.MONGODB_DB]
    mongodb.cvs_collection = mongodb.db[settings.MONGODB_COLLECTION_CVS]
    mongodb.job_descriptions_collection = mongodb.db[settings.MONGODB_COLLECTION_JOB_DESCRIPTIONS]
    
    app_logger.info("Conectado a MongoDB")

async def close_mongo_connection():
    """Cierra la conexión con MongoDB"""
    app_logger.info("Cerrando conexión con MongoDB...")
    if mongodb.client:
        mongodb.client.close()
    app_logger.info("Conexión con MongoDB cerrada")