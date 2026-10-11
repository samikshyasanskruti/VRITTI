import json
from sqlalchemy import select, func
from backend.app.models.database_models import Candidate, Resume, Job, Match

def json_load(value, default=None):
    try:
        return json.loads(value) if value else (default if default is not None else [])
    except (ValueError, TypeError):
        return default if default is not None else []

def resume_to_dict(resume, candidate=None):
    profile = json_load(resume.profile_json, {})
    return {"id": resume.id, "filename": resume.filename, "text_length": len(resume.text or ""),
            "profile": profile, "created_at": resume.created_at.isoformat() if resume.created_at else None,
            "candidate_id": resume.candidate_id}

def get_resume(db, resume_id):
    return db.get(Resume, resume_id)

def latest_resume(db):
    return db.scalar(select(Resume).order_by(Resume.id.desc()).limit(1))

def list_jobs(db, limit=50, offset=0, q=None):
    stmt = select(Job).order_by(Job.id).offset(offset).limit(limit)
    if q:
        pattern = f"%{q}%"
        stmt = select(Job).where((Job.title.ilike(pattern)) | (Job.company.ilike(pattern)) | (Job.description.ilike(pattern))).order_by(Job.id).offset(offset).limit(limit)
    return list(db.scalars(stmt))

def counts(db):
    return {"resumes": db.scalar(select(func.count()).select_from(Resume)) or 0,
            "jobs": db.scalar(select(func.count()).select_from(Job)) or 0,
            "candidates": db.scalar(select(func.count()).select_from(Candidate)) or 0}
