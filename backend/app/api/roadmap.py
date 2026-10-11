import json

from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from sqlalchemy.orm import Session

from backend.app.database.database import get_db
from backend.app.models.database_models import Resume, Job
from backend.app.services.matching.skill_matcher import compare_skills
from backend.app.services.roadmap.roadmap_generator import generate_roadmap

router = APIRouter()


class RoadmapRequest(BaseModel):
    resume_id: int
    job_id: int


def _parse_json_list(value):
    if not value:
        return []

    if isinstance(value, list):
        return value

    try:
        result = json.loads(value)
        return result if isinstance(result, list) else []
    except (TypeError, ValueError, json.JSONDecodeError):
        return []


def _parse_json_object(value):
    if not value:
        return {}

    if isinstance(value, dict):
        return value

    try:
        result = json.loads(value)
        return result if isinstance(result, dict) else {}
    except (TypeError, ValueError, json.JSONDecodeError):
        return {}


@router.post("")
def roadmap(
    payload: RoadmapRequest,
    db: Session = Depends(get_db),
):
    resume = db.get(Resume, payload.resume_id)
    job = db.get(Job, payload.job_id)

    if resume is None:
        raise HTTPException(status_code=404, detail="Resume not found.")

    if job is None:
        raise HTTPException(status_code=404, detail="Job not found.")

    profile = _parse_json_object(resume.profile_json)

    candidate_skills = profile.get("skills") or []
    required_skills = _parse_json_list(job.required_skills_json)
    preferred_skills = _parse_json_list(job.preferred_skills_json)

    # compare_skills requires candidate, required, and preferred skills.
    gap = compare_skills(
        candidate_skills,
        required_skills,
        preferred_skills,
    )

    missing_skills = gap.get("missing_skills", [])

    return {
        "resume_id": resume.id,
        "job_id": job.id,
        "job_title": job.title,
        "company": job.company,
        "matched_skills": gap.get("matched_skills", []),
        "missing_skills": missing_skills,
        "required_skills_count": gap.get("required_skills_count", 0),
        "required_coverage": gap.get("required_coverage", 0),
        "preferred_coverage": gap.get("preferred_coverage", 0),
        "roadmap": generate_roadmap(
    current_skills=candidate_skills,
    target_role=job.title or "Target Role",
    missing_skills=missing_skills,
),
    }