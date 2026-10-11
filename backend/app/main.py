
from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from backend.app.config import ALLOWED_ORIGINS
from backend.app.database.database import init_db

from backend.app.api import (
    health,
    resume,
    jobs,
    matching,
    recommendations,
    simulator,
    roadmap,
    recruiter,
)


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Initialize database tables when the backend starts.
    init_db()
    yield


app = FastAPI(
    title="CareerMatch AI API",
    version="1.0.0",
    description="Resume and job matching using real datasets.",
    lifespan=lifespan,
)

# CORS configuration for the frontend.
app.add_middleware(
    CORSMiddleware,
    allow_origins=ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Register all API routers.
app.include_router(
    health.router,
    prefix="/api/health",
    tags=["Health"],
)

app.include_router(
    resume.router,
    prefix="/api/resume",
    tags=["Resume"],
)

app.include_router(
    jobs.router,
    prefix="/api/jobs",
    tags=["Jobs"],
)

app.include_router(
    matching.router,
    prefix="/api/matching",
    tags=["Matching"],
)

app.include_router(
    recommendations.router,
    prefix="/api/recommendations",
    tags=["Recommendations"],
)

app.include_router(
    simulator.router,
    prefix="/api/simulator",
    tags=["Simulator"],
)

app.include_router(
    roadmap.router,
    prefix="/api/roadmap",
    tags=["Roadmap"],
)

app.include_router(
    recruiter.router,
    prefix="/api/recruiter",
    tags=["Recruiter"],
)


@app.get("/")
def root():
    return {
        "service": "CareerMatch AI",
        "status": "online",
        "docs": "/docs",
    }


@app.get("/health")
def health_check():
    return {
        "status": "healthy",
        "service": "CareerMatch AI",
    }
