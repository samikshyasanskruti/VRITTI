
from pydantic import BaseModel, EmailStr, Field, ConfigDict


class CandidateBase(BaseModel):
    name: str | None = Field(default=None, max_length=255)
    email: EmailStr | None = None
    phone: str | None = Field(default=None, max_length=80)
    location: str | None = Field(default=None, max_length=255)
    skills: list[str] = Field(default_factory=list)


class CandidateCreate(CandidateBase):
    pass


class CandidateResponse(CandidateBase):
    id: int

    model_config = ConfigDict(from_attributes=True)
