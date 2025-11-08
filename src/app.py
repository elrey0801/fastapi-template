# app.py

from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from config import *
# from router import *

from exception.global_exception_handler import configure_exception_handlers
from contextlib import asynccontextmanager
from fastapi.middleware.cors import CORSMiddleware

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup
    DBMySQL.connect()
    DBMySQL.Base.metadata.create_all(bind=DBMySQL._sync_engine)
    logger.info(f'App started successfully on port = {settings.PORT}, host = {settings.HOST}')
    
    yield  # App running
    
    # Shutdown
    logger.info('App shutting down')
    await DBMySQL.close()



app = FastAPI(title=settings.PROJECT_NAME, lifespan=lifespan, docs_url=None, redoc_url=None)
Logger.setup_logging()


origins = settings.ORIGINS.split(",") if settings.ORIGINS != "*" else ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

settings.print_settings()

# Include routers
# app.include_router(WordSetRouter.get_router())

# Mount static files for file serving
import os
from pathlib import Path

# Get the project root directory (parent of src)
# project_root = Path(__file__).parent.parent
# uploads_dir = os.getenv("UPLOADS_DIR", str(project_root / "uploads"))

# Ensure uploads directory exists
# Path(uploads_dir).mkdir(exist_ok=True, parents=True)

# app.mount("/uploads", StaticFiles(directory=uploads_dir), name="uploads")

configure_exception_handlers(app)

# Health check endpoint
@app.get("/health")
async def health_check():
    return {"status": "healthy", "message": "VocabApp Backend is running"}




