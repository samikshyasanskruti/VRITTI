import re
from typing import Any


def _normalize(value: Any) -> str:
    """Convert text or structured values into normalized searchable text."""
    if value is None:
        return ""

    if isinstance(value, dict):
        return " ".join(
            f"{_normalize(key)} {_normalize(item)}"
            for key, item in value.items()
        )

    if isinstance(value, (list, tuple, set)):
        return " ".join(_normalize(item) for item in value)

    return re.sub(r"\s+", " ", str(value).lower()).strip()


def _coverage(candidate_text: str, target_text: str) -> float:
    """Estimate keyword coverage between candidate and job requirements."""
    if not target_text:
        return 0.0

    terms = set(re.findall(r"\b[a-zA-Z][a-zA-Z0-9+#.]*\b", target_text))
    ignored = {
        "and", "the", "for", "with", "from", "this", "that",
        "have", "has", "will", "you", "your", "our", "are",
        "job", "work", "years", "year", "using", "including",
    }
    terms = {term for term in terms if term not in ignored}

    if not terms:
        return 0.0

    present = sum(1 for term in terms if re.search(
        r"(?<!\w)" + re.escape(term) + r"(?!\w)",
        candidate_text,
    ))

    return present / len(terms)


def _skill_coverage(value: Any) -> float:
    """Normalize skill coverage supplied as a ratio or percentage."""
    if value is None:
        return 0.0

    try:
        number = float(value)
    except (TypeError, ValueError):
        return 0.0

    if number > 1:
        number /= 100.0

    return max(0.0, min(1.0, number))


def hybrid_score(
    semantic_similarity: float,
    required_coverage: float,
    preferred_coverage: float,
    project_relevance: float = 0.0,
    experience_relevance: float = 0.0,
) -> float:
    """
    Calculate a hybrid resume-to-job alignment score.

    Weights:
      Semantic relevance:  35%
      Required skills:     30%
      Preferred skills:    10%
      Project relevance:   15%
      Experience relevance: 10%

    All inputs may be ratios (0-1) or percentages (0-100).
    Returns a percentage score between 0 and 100.
    """
    components = {
        "semantic": _skill_coverage(semantic_similarity),
        "required": _skill_coverage(required_coverage),
        "preferred": _skill_coverage(preferred_coverage),
        "projects": _skill_coverage(project_relevance),
        "experience": _skill_coverage(experience_relevance),
    }

    weights = {
        "semantic": 0.35,
        "required": 0.30,
        "preferred": 0.10,
        "projects": 0.15,
        "experience": 0.10,
    }

    score = sum(
        components[name] * weight
        for name, weight in weights.items()
    )

    return round(max(0.0, min(100.0, score * 100)), 2)


def calculate_project_relevance(
    profile: dict,
    job_description: str,
) -> float:
    """Estimate project relevance from the candidate's extracted projects."""
    projects = profile.get("projects") or []
    candidate_projects = _normalize(projects)
    job_text = _normalize(job_description)

    if not candidate_projects or not job_text:
        return 0.0

    return _coverage(candidate_projects, job_text)


def calculate_experience_relevance(
    profile: dict,
    job_description: str,
) -> float:
    """Estimate experience relevance from extracted work experience."""
    sections = profile.get("sections") or {}

    if isinstance(sections, dict):
        experience = (
            sections.get("experience")
            or sections.get("work experience")
            or sections.get("work_experience")
            or sections.get("employment")
            or ""
        )
    else:
        experience = sections

    experience_text = _normalize(experience)
    job_text = _normalize(job_description)

    if not experience_text or not job_text:
        return 0.0

    return _coverage(experience_text, job_text)