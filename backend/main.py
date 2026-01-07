from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from contextlib import asynccontextmanager
from database import engine, Base
from config import settings


from routers import (
    auth_router,
    datasets_router,
    query_router,
    charts_router,
    reports_router,
    dashboard_router
)
from app.api import export
from app.api import sharing

# Create database tables
@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup
    Base.metadata.create_all(bind=engine)
    yield
    # Shutdown
    pass

# Initialize FastAPI app
app = FastAPI(
    title=settings.PROJECT_NAME,
    description="BI Analytics Platform - Power BI-like data analysis and visualization",
    version="1.0.0",
    lifespan=lifespan
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(auth_router)
app.include_router(datasets_router)
app.include_router(query_router)
app.include_router(charts_router)
app.include_router(reports_router)
app.include_router(dashboard_router)
app.include_router(export.router)
app.include_router(sharing.router)

# Root endpoint
@app.get("/")
def root():
    return {
        "message": "BI Analytics Platform API",
        "version": "1.0.0",
        "docs": "/docs"
    }

# Health check endpoint
@app.get("/health")
def health_check():
    return {"status": "healthy"}

