
def project_match_score(
    current_score: float,
    added_skills: list[str] | None = None,
    missing_skills: list[str] | None = None,
) -> dict:
    """
    Estimate a hypothetical score change.

    This is a heuristic scenario, not a trained prediction model.
    """
    current = max(0.0, min(100.0, float(current_score)))

    added = {
        str(skill).strip().lower()
        for skill in (added_skills or [])
        if str(skill).strip()
    }

    missing = {
        str(skill).strip().lower()
        for skill in (missing_skills or [])
        if str(skill).strip()
    }

    relevant_added = added & missing

    # Illustrative scenario: each addressed gap adds 3 points.
    projected = min(100.0, current + 3.0 * len(relevant_added))

    return {
        "current_score": round(current, 2),
        "projected_score": round(projected, 2),
        "estimated_change": round(projected - current, 2),
        "addressed_missing_skills": sorted(relevant_added),
        "is_heuristic": True,
        "warning": (
            "Illustrative estimate only. Actual job-match scores depend "
            "on the resume, job description, and ranking algorithm."
        ),
    }
