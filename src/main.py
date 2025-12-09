import logging
import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager

## from src.api.routes import router as api_router

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)

@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Context manager to handle application startup and shutdown events.
    """
    logger.info("System is starting up. Initializing resources...")

    yield

    logger.info("System is shutting down. Cleaning up resources...")
def create_application() -> FastAPI:
    """
    Factory function to configure the FastAPI application.
    """
    application = FastAPI(
        title="Idea Forge",
        description="Backend service to generate project ideas based on user stack and level.",
        version="1.0.0",
        lifespan=lifespan
    )

    origins = ["*"]

    application.add_middleware(
        CORSMiddleware,
        allow_origins=origins,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
   
    # --- ARCHITECTURE CONNECTION POINT ---
    # Here we include the routes defined in the API layer.
    # The prefix "/api/v1" is a best practice for API versioning.
   # This means all endpoints will start with http://localhost:8000/api/v1/...
   # application.include_router(api_router, prefix="/api/v1")

    return application

app = create_application()

@app.get("/health")
async def health_check():
    """
    Simple health check endpoint.
    """
    return {"status": "active", "version": "1.0.0"}

if __name__ == "__main__":
    uvicorn.run("src.main:app", host="0.0.0.0", port=8000, reload=True)