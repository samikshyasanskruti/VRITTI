
def explain_match(match: dict) -> dict:
    """Explain a match using its available scores and skill evidence."""
    matched = match.get("matched_skills") or []
    missing = match.get("missing_skills") or []
    score = match.get("score")

    reasons = []

    if matched:
        reasons.append(
            "Skills found in common: " + ", ".join(matched[:8]) + "."
        )

    if missing:
        reasons.append(
            "Potential required-skill gaps: "
            + ", ".join(missing[:8]) + "."
        )

    if not matched and not missing:
        reasons.append(
            "The ranking uses semantic similarity; explicit skill "
            "requirements are unavailable for comparison."
        )

    return {
        "job_title": match.get("title"),
        "company": match.get("company"),
        "alignment_score": score,
        "score_type": "alignment score, not hiring probability",
        "reasons": reasons,
    }
