
from backend.app.services.matching.skill_matcher import compare_skills
from backend.app.services.matching.hybrid_ranker import hybrid_score
from backend.app.services.matching.semantic_matcher import semantic_scores


def _text(value):
    """Convert nested profile data into searchable text."""
    if value is None:
        return ""

    if isinstance(value, dict):
        return " ".join(_text(v) for v in value.values())

    if isinstance(value, (list, tuple, set)):
        return " ".join(_text(v) for v in value)

    return str(value)


def _coverage(skills):
    """Normalize skill coverage to a ratio between 0 and 1."""
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
    """Normalize skill names from strings or structured lists."""
    if not values:
        return []

    if isinstance(values, str):
        values = [values]

    if isinstance(values, (list, tuple, set)):
        normalized = []

        for item in values:
            if isinstance(item, dict):
                skill = item.get("name") or item.get("skill") or ""
            else:
                skill = str(item) if item else ""

            skill = skill.strip()

            if skill:
                normalized.append(skill)

        return list(dict.fromkeys(normalized))

    return []


def _normalize_key(value):
    """Normalize section names for reliable lookup."""
    return " ".join(
        str(value).casefold().replace("_", " ").replace("-", " ").split()
    )


def _section_text(profile, *keys):
    """Read section text from detected sections or top-level profile fields."""
    sections = profile.get("sections") or {}

    if not isinstance(sections, dict):
        sections = {}

    normalized_sections = {
        _normalize_key(key): value
        for key, value in sections.items()
    }

    for key in keys:
        normalized_key = _normalize_key(key)

        # Prefer the detected section when it contains text.
        value = normalized_sections.get(normalized_key)
        if value:
            return _text(value)

        # Fall back to the structured top-level profile field.
        value = profile.get(key)
        if value:
            return _text(value)

        # Also support differently formatted top-level field names.
        for profile_key, profile_value in profile.items():
            if _normalize_key(profile_key) == normalized_key and profile_value:
                return _text(profile_value)

    return ""


def _skill_relevance(skills, text):
    """
    Calculate the fraction of detected job skills mentioned in a section.
    This is keyword overlap, not a semantic quality assessment.
    """
    if not skills or not text:
        return 0.0

    text = text.casefold()

    matched = sum(
        1
        for skill in skills
        if skill.casefold() in text
    )

    return matched / len(skills)


def match_resume_to_jobs(
    profile: dict,
    resume_text: str,
    jobs: list[dict],
    top_k: int = 20,
) -> list[dict]:
    """Rank jobs using semantic similarity and detected skill coverage."""

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

    projects_text = _section_text(
        profile,
        "projects",
        "project",
        "academic projects",
    )

    experience_text = _section_text(
        profile,
        "experience",
        "work experience",
        "employment",
        "professional experience",
        "internship",
        "internships",
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

        # Relevance is based on detected job skills mentioned in projects.
        project_relevance = _skill_relevance(
            required,
            projects_text,
        )

        # Relevance is based on detected job skills mentioned in experience.
        experience_relevance = _skill_relevance(
            required,
            experience_text,
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
            "experience_relevance": round(
                experience_relevance * 100, 2
            ),
            "explanation": _explain(skill_results),
        })

    results.sort(
        key=lambda item: item["score"],
        reverse=True,
    )

    return results[:max(1, min(top_k, 100))]


def _explain(skills: dict) -> str:
    """Explain detected skill overlap and gaps."""
    matched = skills.get("matched_skills", [])
    missing = skills.get("missing_skills", [])

    required_count = skills.get("required_skills_count", 0)
    preferred_count = skills.get("preferred_skills_count", 0)

    if not required_count and not preferred_count:
        return (
            "Ranked using semantic similarity. "
            "No detected job skills were available for comparison."
        )

    explanation = []

    if matched:
        explanation.append(
            "Matched detected skills: "
            + ", ".join(matched[:8]) + "."
        )

    if missing:
        explanation.append(
            "Other detected job skills not found in the resume: "
            + ", ".join(missing[:8]) + "."
        )

    if not missing:
        explanation.append(
            "All detected job skills were found in the resume."
        )

    if not matched:
        explanation.append(
            "No overlap was found among the detected skill lists."
        )

    return " ".join(explanation)
