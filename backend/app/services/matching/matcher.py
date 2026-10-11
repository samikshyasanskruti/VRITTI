from backend.app.services.matching.skill_matcher import compare_skills
from backend.app.services.matching.hybrid_ranker import hybrid_score
from backend.app.services.matching.semantic_matcher import semantic_scores


def _text(value):
    if value is None:
        return ""
    if isinstance(value, dict):
        return " ".join(_text(v) for v in value.values())
    if isinstance(value, (list, tuple, set)):
        return " ".join(_text(v) for v in value)
    return str(value)


def _coverage(skills):
    if not skills:
        return 0.0

    for key in ("required_coverage", "preferred_coverage"):
        if key in skills:
            try:
                value = float(skills[key])
                if value > 1:
                    value /= 100.0
                return max(0.0, min(1.0, value))
            except (TypeError, ValueError):
                pass

    return 0.0


def _normalize_skills(values):
    if not values:
        return []

    if isinstance(values, str):
        return [item.strip() for item in values.split(",") if item.strip()]

    if isinstance(values, list):
        return [
            item.get("name") or item.get("skill") or ""
            if isinstance(item, dict)
            else str(item)
            for item in values
            if item
        ]

    return []


def match_resume_to_jobs(
    profile: dict,
    resume_text: str,
    jobs: list[dict],
    top_k: int = 20,
) -> list[dict]:
    """Rank jobs using semantic similarity and skill coverage."""

    if not jobs:
        return []

    documents = [
        f"{job.get('title') or ''}\n"
        f"{job.get('description') or ''}\n"
        f"{job.get('required_skills') or ''}\n"
        f"{job.get('preferred_skills') or ''}"
        for job in jobs
    ]

    similarities = semantic_scores(resume_text, documents)
    candidate_skills = _normalize_skills(profile.get("skills"))
    projects_text = _text(profile.get("projects"))
    experience_text = _text(
        (profile.get("sections") or {}).get("experience", "")
        if isinstance(profile.get("sections"), dict)
        else profile.get("sections", "")
    )

    results = []

    for index, job in enumerate(jobs):
        required = _normalize_skills(job.get("required_skills"))
        preferred = _normalize_skills(job.get("preferred_skills"))

        skill_results = compare_skills(
            candidate_skills,
            required,
            preferred,
        )

        similarity = (
            float(similarities[index])
            if index < len(similarities)
            else 0.0
        )

        required_coverage = _coverage({
            "required_coverage": skill_results.get(
                "required_coverage", 0
            )
        })
        preferred_coverage = _coverage({
            "preferred_coverage": skill_results.get(
                "preferred_coverage", 0
            )
        })

        job_text = documents[index].lower()

        project_relevance = (
            sum(1 for skill in candidate_skills
                if skill.lower() in projects_text.lower())
            / max(len(candidate_skills), 1)
            if projects_text
            else 0.0
        )

        experience_relevance = (
            sum(1 for skill in required
                if skill.lower() in experience_text.lower())
            / max(len(required), 1)
            if required and experience_text
            else 0.0
        )

        score = hybrid_score(
            semantic_similarity=similarity,
            required_coverage=required_coverage,
            preferred_coverage=preferred_coverage,
            project_relevance=project_relevance,
            experience_relevance=experience_relevance,
        )

        results.append({
            "job_id": job.get("id"),
            "title": job.get("title"),
            "company": job.get("company"),
            "location": job.get("location"),
            "score": score,
            "score_type": "alignment score (not hiring probability)",
            "semantic_similarity": round(similarity * 100, 2),
            **skill_results,
            "project_relevance": round(project_relevance * 100, 2),
            "experience_relevance": round(experience_relevance * 100, 2),
            "explanation": _explain(skill_results),
        })

    results.sort(key=lambda item: item["score"], reverse=True)
    return results[:max(1, min(top_k, 100))]


def _explain(skills: dict) -> str:
    matched = skills.get("matched_skills", [])
    missing = skills.get("missing_skills", [])

    if not skills.get("required_skills_count") and not skills.get(
        "preferred_skills_count"
    ):
        return (
            "Ranked using semantic similarity. Job-specific skill "
            "requirements were not available for comparison."
        )

    explanation = []

    if matched:
        explanation.append(
            "Matched skills: " + ", ".join(matched[:8]) + "."
        )

    if missing:
        explanation.append(
            "Missing required skills: " + ", ".join(missing[:8]) + "."
        )

    if not missing:
        explanation.append("No detected required-skill gaps.")

    if not matched:
        explanation.append("No listed skills were detected in common.")

    return " ".join(explanation)