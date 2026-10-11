
def prioritize_skill_gaps(
    missing_skills: list[str],
    required_skills: list[str] | None = None,
    preferred_skills: list[str] | None = None,
) -> list[dict]:
    """Prioritize missing skills based on supplied job requirements."""

    required_map = {
        str(skill).strip().lower(): str(skill).strip()
        for skill in (required_skills or [])
        if str(skill).strip()
    }

    preferred_map = {
        str(skill).strip().lower(): str(skill).strip()
        for skill in (preferred_skills or [])
        if str(skill).strip()
    }

    unique_gaps = {
        str(skill).strip().lower(): str(skill).strip()
        for skill in (missing_skills or [])
        if str(skill).strip()
    }

    priorities = []

    for key, skill in unique_gaps.items():
        if key in required_map:
            level = "High"
            reason = "Listed as a required job skill."
        elif key in preferred_map:
            level = "Medium"
            reason = "Listed as a preferred job skill."
        else:
            level = "Unclassified"
            reason = "No requirement priority was provided."

        priorities.append({
            "skill": skill,
            "priority": level,
            "reason": reason,
        })

    order = {"High": 0, "Medium": 1, "Unclassified": 2}
    priorities.sort(key=lambda item: order[item["priority"]])

    return priorities
