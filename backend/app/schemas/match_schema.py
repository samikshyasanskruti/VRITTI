
from pydantic import BaseModel, Field


class MatchRequest(BaseModel):
    resume_id: int | None = Field(default=None, ge=1)
    top_k: int = Field(default=20, ge=1, le=100)


class JobMatchResult(BaseModel):
    job_id: int | None = None
    title: str | None = None
    company: str | None = None
    location: str | None = None
    score: float = Field(ge=0, le=100)
    score_type: str = "alignment score (not hiring probability)"
    semantic_similarity: float | None = None
    matched_skills: list[str] = Field(default_factory=list)
    missing_skills: list[str] = Field(default_factory=list)
    explanation: str = ""


class MatchResponse(BaseModel):
    success: bool = True
    resume_id: int
    candidate_shortlist_count: int
    total_postings_available: int
    count: int
    retrieval: str
    ranking: str
    score_note: str
    matches: list[JobMatchResult] = Field(default_factory=list)
