
def generate_match_explanation(
    resume_profile: dict,
    job: dict,
    match_result: dict,
) -> dict:
    """Generate an evidence-based explanation of a resume-job match."""

    resume_skills = resume_profile.get("skills") or []
    matched_skills = match_result.get("matched_skills") or []
    missing_skills = match_result.get("missing_skills") or []

    score = match_result.get("score")
    title = job.get("title") or "This role"
    company = job.get("company") or "the listed employer"

    reasons = []

    if matched_skills:
        reasons.append(
            "Skills detected in common: "
            + ", ".join(str(skill) for skill in matched_skills[:10])
            + "."
        )

    if missing_skills:
        reasons.append(
            "Potential skill gaps: "
            + ", ".join(str(skill) for skill in missing_skills[:10])
            + "."
        )

    if not matched_skills and not missing_skills:
        reasons.append(
            "No explicit skill comparison is available. "
            "Review the resume and job description manually."
        )

    if score is not None:
        reasons.append(
            f"Calculated alignment score: {score}. "
            "This is not a probability of being hired."
        )

    return {
        "job_title": title,
        "company": company,
        "resume_skills_detected": resume_skills,
        "matched_skills": matched_skills,
        "missing_skills": missing_skills,
        "explanation": " ".join(reasons),
    }


def generate_match_explanations(
    resume_profile: dict,
    matches: list[dict],
) -> list[dict]:
    """Generate explanations for multiple matched jobs."""

    explanations = []

    for match in matches:
        explanations.append(
            generate_match_explanation(
                resume_profile=resume_profile,
                job=match,
                match_result=match,
            )
        )

    return explanations
