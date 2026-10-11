
from pydantic import BaseModel, Field, ConfigDict


class JobBase(BaseModel):
    external_id: str | None = None
    title: str = Field(min_length=1, max_length=512)
    company: str | None = None
    location: str | None = None
    description: str = ""
    required_skills: list[str] = Field(default_factory=list)
    preferred_skills: list[str] = Field(default_factory=list)
    work_type: str | None = None
    source_dataset: str | None = None


class JobCreate(JobBase):
    pass


class JobResponse(JobBase):
    id: int

    model_config = ConfigDict(from_attributes=True)
