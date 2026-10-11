
import re


def extract_years_experience(text: str) -> float | None:
    """Extract an explicitly stated number of years of experience."""
    if not text:
        return None

    patterns = [
        r"(\d+(?:\.\d+)?)\+?\s*(?:years|yrs)\s+(?:of\s+)?experience",
        r"experience\s*(?:of|:)?\s*(\d+(?:\.\d+)?)\+?\s*(?:years|yrs)",
    ]

    for pattern in patterns:
        match = re.search(pattern, text, re.IGNORECASE)
        if match:
            return float(match.group(1))

    return None


def compare_experience(
    resume_text: str,
    required_years: float | None,
) -> dict:
    candidate_years = extract_years_experience(resume_text)

    if required_years is None or candidate_years is None:
        return {
            "candidate_years_detected": candidate_years,
            "required_years": required_years,
            "experience_score": 0.0,
            "experience_assessed": False,
        }

    score = (
        1.0
        if required_years <= 0
        else min(candidate_years / required_years, 1.0)
    )

    return {
        "candidate_years_detected": candidate_years,
        "required_years": required_years,
        "experience_score": round(score, 4),
        "experience_assessed": True,
    }
