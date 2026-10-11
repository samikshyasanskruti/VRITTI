
from pydantic import BaseModel, Field


class RecommendationRequest(BaseModel):
    resume_id: int | None = Field(default=None, ge=1)
    top_k: int = Field(default=10, ge=1, le=100)


class CareerRecommendation(BaseModel):
    career_title: str
    company_example: str | None = None
    matching_jobs_in_results: int = 0
    resume_skills: list[str] = Field(default_factory=list)
    reason: str = ""


class InternshipRecommendation(BaseModel):
    job_id: int | None = None
    title: str
    company: str | None = None
    location: str | None = None
    score: float | None = None
    matched_skills: list[str] = Field(default_factory=list)
    description: str = ""
    source: str = "Retrieved job posting"
