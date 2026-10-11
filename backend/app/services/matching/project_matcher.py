
def match_projects_to_resume(
    resume_profile: dict,
    projects: list[dict],
    top_k: int = 10,
) -> list[dict]:
    """Rank projects using skills detected in the resume."""

    candidate_skills = {
        str(skill).strip().lower()
        for skill in (resume_profile.get("skills") or [])
        if str(skill).strip()
    }

    results = []

    for project in projects:
        project_skills = {
            str(skill).strip().lower()
            for skill in (project.get("skills") or [])
            if str(skill).strip()
        }

        matched = sorted(candidate_skills & project_skills)
        missing = sorted(project_skills - candidate_skills)

        coverage = (
            len(matched) / len(project_skills)
            if project_skills else 0.0
        )

        results.append({
            "project_id": project.get("id"),
            "title": project.get("title"),
            "description": project.get("description"),
            "matched_skills": matched,
            "missing_skills": missing,
            "score": round(coverage * 100, 2),
            "score_type": "project skill coverage",
        })

    results.sort(key=lambda item: item["score"], reverse=True)

    return results[:max(1, min(top_k, 50))]
