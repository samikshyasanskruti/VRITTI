import re


def normalize_skills(values):
    if not values:
        return []

    if isinstance(values, str):
        return [s.strip().lower() for s in values.split(",") if s.strip()]

    if isinstance(values, list):
        return [
            str(
                item.get("name") or item.get("skill") or ""
                if isinstance(item, dict)
                else item
            ).strip().lower()
            for item in values
            if item
        ]

    return []


def compare_skills(candidate_skills, required_skills, preferred_skills):
    candidate = set(normalize_skills(candidate_skills))
    required = normalize_skills(required_skills)
    preferred = normalize_skills(preferred_skills)

    matched_required = [
        skill for skill in required if skill in candidate
    ]
    missing_required = [
        skill for skill in required if skill not in candidate
    ]
    matched_preferred = [
        skill for skill in preferred if skill in candidate
    ]

    required_coverage = (
        len(matched_required) / len(required)
        if required else 0.0
    )
    preferred_coverage = (
        len(matched_preferred) / len(preferred)
        if preferred else 0.0
    )

    return {
        "matched_skills": list(dict.fromkeys(
            matched_required + matched_preferred
        )),
        "missing_skills": list(dict.fromkeys(missing_required)),
        "required_skills_count": len(required),
        "preferred_skills_count": len(preferred),
        "required_coverage": required_coverage,
        "preferred_coverage": preferred_coverage,
    }