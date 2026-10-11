from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session

from backend.app.api.matching import _run_matching
from backend.app.database.database import get_db
from backend.app.models.database_models import Resume

router = APIRouter()


@router.get("")
def recommendations(
    resume_id: int | None = Query(default=None, ge=1),
    top_k: int = Query(default=10, ge=1, le=100),
    db: Session = Depends(get_db),
):
    """
    Return job recommendations ranked against a saved resume.
    Uses the existing hybrid matching engine.
    """

    try:
        # Verify that a resume exists before matching.
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

        # Use the shared matching implementation.
        result = _run_matching(
            resume_id=resume.id,
            top_k=top_k,
            db=db,
        )

        matches = result.get("matches", [])

        return {
            "success": True,
            "resume_id": result.get("resume_id"),
            "count": len(matches),
            "recommendations": matches,
            "score_note": result.get(
                "score_note",
                "Alignment score, not probability of being hired.",
            ),
        }

    except HTTPException:
        raise
    except Exception as exc:
        raise HTTPException(
            status_code=500,
            detail=f"Failed to load recommendations: {exc}",
        ) from exc