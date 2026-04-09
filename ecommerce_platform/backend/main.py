"""
COMP7640 E-Commerce Platform - FastAPI Main Application
Uses a layered architecture:
  - Models: Data Model Layer (Pydantic)
  - Routes: Interface Layer (REST API)
  - Services: Business Logic Layer
  - DAO: Data Access Layer (Database)
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import logging

# Import routes
from routes import router

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Create FastAPI application
app = FastAPI(
    title="COMP7640 E-Commerce Platform API",
    description="Multi-vendor e-commerce platform REST API",
    version="2.0.0",
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Register routes
app.include_router(router)


# Startup and shutdown events
@app.on_event("startup")
async def startup():
    """Application startup event"""
    logger.info("E-Commerce Platform API starting up...")


@app.on_event("shutdown")
async def shutdown():
    """Application shutdown event"""
    logger.info("E-Commerce Platform API shutting down...")


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)