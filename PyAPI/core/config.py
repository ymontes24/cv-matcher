import os
from dotenv import load_dotenv
from pydantic_settings import BaseSettings

load_dotenv()

class Settings(BaseSettings):
    # API
    API_HOST: str = os.getenv("API_HOST", "0.0.0.0")
    API_PORT: int = int(os.getenv("API_PORT", "8000"))
    
    # MongoDB
    MONGODB_URL: str = os.getenv("MONGODB_URL", "mongodb://root:root@localhost:27017")
    MONGODB_DB: str = os.getenv("MONGODB_DB", "cv_match")
    MONGODB_COLLECTION_CVS: str = os.getenv("MONGODB_COLLECTION_CVS", "cvs")
    MONGODB_COLLECTION_JOB_DESCRIPTIONS: str = os.getenv("MONGODB_COLLECTION_JOB_DESCRIPTIONS", "job_descriptions")
    
    # Embedding
    EMBEDDING_MODEL: str = os.getenv("EMBEDDING_MODEL", "all-MiniLM-L6-v2")
    CHUNK_SIZE: int = int(os.getenv("CHUNK_SIZE", "300"))
    CHUNK_OVERLAP: int = int(os.getenv("CHUNK_OVERLAP", "75"))
    
    # Aplicación
    APP_NAME: str = "CV Matcher"
    APP_VERSION: str = "0.1.0"
    APP_DESCRIPTION: str = "API para evaluar la compatibilidad entre descripciones de puestos y CVs"

settings = Settings()