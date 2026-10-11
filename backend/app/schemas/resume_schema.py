
from pydantic import BaseModel, Field


class ResumeUploadResponse(BaseModel):
    success: bool = True
    resume_id: int
    filename: str
    text_length: int
    profile: dict = Field(default_factory=dict)
    text_preview: str = ""


class ResumeSummary(BaseModel):
    id: int
    filename: str
    text_length: int
    profile: dict = Field(default_factory=dict)
