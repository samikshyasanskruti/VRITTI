
import json

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session

from backend.app.database.database import get_db
from backend.app.models.database_models import Job, Resume
from backend.app.services.matching.matcher import match_resume_to_jobs
from backend.app.services.retrieval.search import search_jobs


router = APIRouter()


def _parse_json_list(value):
    """Safely parse a JSON list stored in the database."""
    if not value:
        return []

    if isinstance(value, list):
        return value

    try:
        parsed = json.loads(value)
        return parsed if isinstance(parsed, list) else []
    except (TypeError, ValueError, json.JSONDecodeError):
        return []


def _run_matching(
    resume_id: int | None,
    top_k: int,
    db: Session,
):
    # 1. Get the requested resume, or the most recently uploaded resume.
    if resume_id is not None:
        resume = db.get(Resume, resume_id)
    else:
        resume = (
            db.query(Resume)
            .order_by(Resume.id.desc())
            .first()
        )

    if resume is None:
        raise HTTPException(
            status_code=404,
            detail="Resume not found. Upload a resume first.",
        )

    resume_text = (resume.text or "").strip()

    if not resume_text:
        raise HTTPException(
            status_code=422,
            detail="The selected resume contains no extractable text.",
        )

    # 2. Confirm the application database contains job postings.
    total_jobs = db.query(Job).count()

    if total_jobs == 0:
        raise HTTPException(
            status_code=404,
            detail=(
                "No jobs found in the application database. "
                "Run scripts/sync_indexed_jobs.py first."
            ),
        )

    # 3. Retrieve a semantic shortlist using the existing FAISS index.
    shortlist_size = min(top_k * 5, 200)

    try:
        shortlist = search_jobs(
            resume_text,
            top_k=shortlist_size,
        )
    except FileNotFoundError as exc:
        raise HTTPException(
            status_code=503,
            detail=f"FAISS index files are missing: {exc}",
        ) from exc
    except RuntimeError as exc:
        raise HTTPException(
            status_code=503,
            detail=f"FAISS index error: {exc}",
        ) from exc
    except Exception as exc:
        raise HTTPException(
            status_code=503,
            detail=f"Semantic job retrieval failed: {exc}",
        ) from exc

    if not shortlist:
        raise HTTPException(
            status_code=404,
            detail="FAISS did not return any matching job postings.",
        )

    # 4. Match FAISS source IDs to database external IDs.
    source_ids = list(dict.fromkeys(
        str(item["source_id"])
        for item in shortlist
        if item.get("source_id") is not None
    ))

    if not source_ids:
        raise HTTPException(
            status_code=503,
            detail=(
                "FAISS metadata has no source_id values. "
                "Check vector_store/jobs/jobs_metadata.json."
            ),
        )

    jobs = (
        db.query(Job)
        .filter(Job.external_id.in_(source_ids))
        .all()
    )

    jobs_by_external_id = {
        str(job.external_id): job
        for job in jobs
        if job.external_id is not None
    }

    # Preserve the FAISS retrieval order when building the shortlist.
    shortlist_jobs = []

    for item in shortlist:
        source_id = item.get("source_id")

        if source_id is None:
            continue

        job = jobs_by_external_id.get(str(source_id))

        if job is None:
            continue

        shortlist_jobs.append({
            "id": job.id,
            "title": job.title,
            "company": job.company,
            "location": job.location,
            "description": job.description or "",
            "required_skills": _parse_json_list(
                job.required_skills_json
            ),
            "preferred_skills": _parse_json_list(
                job.preferred_skills_json
            ),
        })

    if not shortlist_jobs:
        raise HTTPException(
            status_code=503,
            detail=(
                "FAISS returned postings, but none matched application "
                "database records. Verify source_id and external_id values."
            ),
        )

    # 5. Calculate alignment scores using the existing matching service.
    profile = _parse_json_object(resume.profile_json)

    try:
        results = match_resume_to_jobs(
            profile=profile,
            resume_text=resume_text,
            jobs=shortlist_jobs,
            top_k=top_k,
        )
    except Exception as exc:
        raise HTTPException(
            status_code=500,
            detail=f"Job ranking failed: {exc}",
        ) from exc

    return {
        "success": True,
        "resume_id": resume.id,
        "candidate_shortlist_count": len(shortlist_jobs),
        "total_postings_available": total_jobs,
        "count": len(results),
        "retrieval": (
            "Sentence Transformers embeddings + FAISS cosine similarity"
        ),
        "ranking": (
            "Semantic similarity + required-skill coverage"
        ),
        "score_note": (
            "Alignment score, not probability of being hired. "
            "Results depend on the information extracted from the resume "
            "and job descriptions."
        ),
        "matches": results,
    }


def _parse_json_object(value):
    """Safely parse a JSON object stored in the resume profile."""
    if not value:
        return {}

    if isinstance(value, dict):
        return value

    try:
        parsed = json.loads(value)
        return parsed if isinstance(parsed, dict) else {}
    except (TypeError, ValueError, json.JSONDecodeError):
        return {}


@router.post("/run")
def run_matching(
    resume_id: int | None = Query(default=None, ge=1),
    top_k: int = Query(default=20, ge=1, le=100),
    db: Session = Depends(get_db),
):
    return _run_matching(resume_id, top_k, db)


@router.get("/{resume_id}")
def get_matches(
    resume_id: int,
    top_k: int = Query(default=20, ge=1, le=100),
    db: Session = Depends(get_db),
):
    return _run_matching(resume_id, top_k, db)
