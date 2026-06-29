"""
BlockState FastAPI Backend
Main application entry point with system enforcer logic
"""

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
import logging
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Import routers
from routes import enforcer, workflows, sessions, system, categorization

# Lifespan context manager for startup/shutdown
@asynccontextmanager
async def lifespan(app: FastAPI):
    """Handle startup and shutdown events"""
    logger.info("BlockState Backend Starting...")
    yield
    logger.info("BlockState Backend Shutting Down...")

# Create FastAPI application
app = FastAPI(
    title="BlockState API",
    description="System enforcer backend for BlockState productivity application",
    version="1.0.0",
    lifespan=lifespan
)

# Configure CORS to allow React frontend communication
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://localhost:5173", "*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(enforcer.router, prefix="/api/enforcer", tags=["enforcer"])
app.include_router(workflows.router, prefix="/api/workflows", tags=["workflows"])
app.include_router(sessions.router, prefix="/api/sessions", tags=["sessions"])
app.include_router(system.router, prefix="/api/system", tags=["system"])
app.include_router(categorization.router, prefix="/api/categorization", tags=["categorization"])

# Health check endpoint
@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "service": "BlockState Backend",
        "version": "1.0.0"
    }

# Root endpoint
@app.get("/")
async def root():
    """Root endpoint with API documentation"""
    return {
        "message": "BlockState API",
        "docs": "/docs",
        "version": "1.0.0"
    }

if __name__ == "__main__":
    import uvicorn
    
    # Get configuration from environment
    host = os.getenv("BACKEND_HOST", "0.0.0.0")
    port = int(os.getenv("BACKEND_PORT", 8000))
    
    logger.info(f"Starting BlockState Backend on {host}:{port}")
    
    uvicorn.run(
        "main:app",
        host=host,
        port=port,
        reload=True,
        log_level="info"
    )
