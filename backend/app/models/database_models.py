
from datetime import datetime

from sqlalchemy import (
    Column,
    Integer,
    String,
    Text,
    Float,
    DateTime,
    ForeignKey,
    Index,
)

from backend.app.database.database import Base


class Candidate(Base):
    __tablename__ = "candidates"

    id = Column(Integer, primary_key=True)
    name = Column(String(255), nullable=True)
    email = Column(String(255), nullable=True, index=True)
    phone = Column(String(80), nullable=True)
    location = Column(String(255), nullable=True)
    skills_json = Column(Text, nullable=False, default="[]")
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)


class Resume(Base):
    __tablename__ = "resumes"

    id = Column(Integer, primary_key=True)
    candidate_id = Column(
        Integer, ForeignKey("candidates.id"), nullable=True, index=True
    )
    filename = Column(String(512), nullable=False)
    text = Column(Text, nullable=False, default="")
    profile_json = Column(Text, nullable=False, default="{}")
    source_dataset = Column(String(255), nullable=True)
    source_id = Column(String(255), nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)


class Job(Base):
    __tablename__ = "jobs"

    id = Column(Integer, primary_key=True)
    external_id = Column(String(255), nullable=True, index=True)
    title = Column(String(512), nullable=False)
    company = Column(String(512), nullable=True)
    location = Column(String(512), nullable=True)
    description = Column(Text, nullable=False, default="")
    required_skills_json = Column(Text, nullable=False, default="[]")
    preferred_skills_json = Column(Text, nullable=False, default="[]")
    work_type = Column(String(255), nullable=True)
    source_dataset = Column(String(255), nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)


class Skill(Base):
    __tablename__ = "skills"

    id = Column(Integer, primary_key=True)
    name = Column(String(255), unique=True, nullable=False)
    category = Column(String(100), nullable=True)


class Match(Base):
    __tablename__ = "matches"

    id = Column(Integer, primary_key=True)
    resume_id = Column(
        Integer, ForeignKey("resumes.id"), nullable=False, index=True
    )
    job_id = Column(
        Integer, ForeignKey("jobs.id"), nullable=False, index=True
    )
    score = Column(Float, nullable=False)
    details_json = Column(Text, nullable=False, default="{}")
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)


class Project(Base):
    __tablename__ = "projects"

    id = Column(Integer, primary_key=True)
    title = Column(String(512), nullable=False)
    description = Column(Text, nullable=False, default="")
    skills_json = Column(Text, nullable=False, default="[]")
    source_dataset = Column(String(255), nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)


Index("ix_jobs_title_company", Job.title, Job.company)
