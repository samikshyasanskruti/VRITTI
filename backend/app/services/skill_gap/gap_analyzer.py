
def analyze_skill_gaps(
    candidate_skills: list[str],
    required_skills: list[str],
    preferred_skills: list[str] | None = None,
) -> dict:
    """Compare candidate skills with a job's supplied skill requirements."""

    candidate = {
        str(skill).strip().lower()
        for skill in (candidate_skills or [])
        if str(skill).strip()
    }

    required = {
        str(skill).strip()
        for skill in (required_skills or [])
        if str(skill).strip()
    }

    preferred = {
        str(skill).strip()
        for skill in (preferred_skills or [])
        if str(skill).strip()
    }

    matched_required = sorted(
        skill for skill in required if skill.lower() in candidate
    )
    missing_required = sorted(
        skill for skill in required if skill.lower() not in candidate
    )
    missing_preferred = sorted(
        skill for skill in preferred if skill.lower() not in candidate
    )

    coverage = (
        len(matched_required) / len(required)
        if required else None
    )

    return {
        "matched_required_skills": matched_required,
        "missing_required_skills": missing_required,
        "missing_preferred_skills": missing_preferred,
        "required_skill_coverage": (
            round(coverage * 100, 2)
            if coverage is not None else None
        ),
        "requirements_available": bool(required or preferred),
    }
