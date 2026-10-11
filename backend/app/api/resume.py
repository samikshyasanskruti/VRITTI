
import json
import tempfile
from pathlib import Path

from fastapi import APIRouter, UploadFile, File, HTTPException, Depends
from sqlalchemy.orm import Session

from backend.app.database.database import get_db
from backend.app.models.database_models import Candidate, Resume
from backend.app.services.resume.resume_parser import parse_resume
from backend.app.config import MAX_UPLOAD_MB

router = APIRouter()

ALLOWED = {".pdf", ".docx", ".txt"}


def _parse_object(value):
    if isinstance(value, dict):
        return value

    if isinstance(value, str):
        try:
            parsed = json.loads(value)
            return parsed if isinstance(parsed, dict) else {}
        except (TypeError, ValueError):
            return {}

    return {}


@router.post("/upload")
async def upload_resume(
    file: UploadFile = File(...),
    db: Session = Depends(get_db),
):
    filename = Path(file.filename or "resume").name
    ext = Path(filename).suffix.lower()

    if ext not in ALLOWED:
        raise HTTPException(
            status_code=400,
            detail="Supported file types are PDF, DOCX and TXT.",
        )

    data = await file.read()

    if not data:
        raise HTTPException(
            status_code=400,
            detail="Uploaded file is empty.",
        )

    if len(data) > MAX_UPLOAD_MB * 1024 * 1024:
        raise HTTPException(
            status_code=413,
            detail=f"File exceeds {MAX_UPLOAD_MB} MB limit.",
        )

    temp = None

    try:
        with tempfile.NamedTemporaryFile(
            suffix=ext,
            delete=False,
        ) as handle:
            handle.write(data)
            temp = Path(handle.name)

        # The parser is responsible for extracting resume information.
        profile = parse_resume(temp)

        if not isinstance(profile, dict):
            raise ValueError("Resume parser returned an invalid profile.")

        resume_text = str(profile.get("text") or "").strip()

        if not resume_text:
            raise ValueError(
                "No extractable text found. Check the PDF or use a text-based PDF."
            )

        candidate_data = _parse_object(profile.get("candidate"))
        skills = profile.get("skills") or []

        candidate = Candidate(
            name=candidate_data.get("name"),
            email=candidate_data.get("email"),
            phone=candidate_data.get("phone"),
            skills_json=json.dumps(skills, ensure_ascii=False),
        )

        db.add(candidate)
        db.flush()

        resume = Resume(
            candidate_id=candidate.id,
            filename=filename,
            text=resume_text,
            profile_json=json.dumps(profile, ensure_ascii=False),
        )

        db.add(resume)
        db.commit()
        db.refresh(resume)

        # Return all structured fields except the full extracted text.
        public_profile = {
            key: value
            for key, value in profile.items()
            if key != "text"
        }

        return {
            "success": True,
            "resume_id": resume.id,
            "filename": filename,
            "text_length": len(resume_text),
            "profile": public_profile,
            "text_preview": resume_text[:1200],
        }

    except ValueError as exc:
        db.rollback()
        raise HTTPException(status_code=422, detail=str(exc)) from exc

    except Exception as exc:
        db.rollback()
        raise HTTPException(
            status_code=500,
            detail=f"Resume processing failed: {exc}",
        ) from exc

    finally:
        if temp:
            try:
                temp.unlink(missing_ok=True)
            except OSError:
                pass


@router.get("")
def list_resumes(
    limit: int = 50,
    db: Session = Depends(get_db),
):
    rows = (
        db.query(Resume)
        .order_by(Resume.id.desc())
        .limit(max(1, min(limit, 200)))
        .all()
    )

    return [
        {
            "id": row.id,
            "filename": row.filename,
            "text_length": len(row.text or ""),
            "profile": _parse_object(row.profile_json),
        }
        for row in rows
    ]


@router.get("/{resume_id}")
def get_resume_profile(
    resume_id: int,
    db: Session = Depends(get_db),
):
    row = db.get(Resume, resume_id)

    if not row:
        raise HTTPException(
            status_code=404,
            detail="Resume not found.",
        )

    return {
        "id": row.id,
        "filename": row.filename,
        "text_length": len(row.text or ""),
        "profile": _parse_object(row.profile_json),
    }
