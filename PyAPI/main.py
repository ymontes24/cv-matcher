from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from db.mongodb import connect_to_mongo, close_mongo_connection
from core.config import settings
from core.logging import app_logger
from contextlib import asynccontextmanager
from api.routes import documents

@asynccontextmanager
async def lifespan(app: FastAPI):
    """Manejador de ciclo de vida para startup y shutdown."""
    try:
        app_logger.info("Iniciando aplicación...")
        await connect_to_mongo()
        app_logger.info("Aplicación iniciada")
        yield  # Aquí corre la aplicación
    except Exception as e:
        app_logger.error(f"Error al iniciar la aplicación: {e}")
        raise HTTPException(status_code=500, detail="Error al iniciar la aplicación")
    finally:
        try:
            app_logger.info("Apagando aplicación...")
            await close_mongo_connection()
            app_logger.info("Aplicación apagada")
        except Exception as e:
            app_logger.error(f"Error al apagar la aplicación: {e}")
            # No se levanta excepción en shutdown para no bloquear cierre.

app = FastAPI(
    title=settings.APP_NAME,
    version=settings.APP_VERSION,
    description=settings.APP_DESCRIPTION,
    lifespan=lifespan,  # Aquí se registra el manejador
)

# Middleware para CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(documents.router, prefix="/api/documents", tags=["documents"])

@app.get("/api/health")
async def health():
    return {"status": "ok", "version": settings.APP_VERSION}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "app.main:app",
        host=settings.API_HOST,
        port=settings.API_PORT,
        reload=True
    )
