
from pydantic import BaseModel, Field


class SkillGapRequest(BaseModel):
    resume_id: int = Field(ge=1)
    job_id: int = Field(ge=1)


class SkillGapResponse(BaseModel):
    matched_required_skills: list[str] = Field(default_factory=list)
    missing_required_skills: list[str] = Field(default_factory=list)
    missing_preferred_skills: list[str] = Field(default_factory=list)
    required_skill_coverage: float | None = None
    requirements_available: bool = False
