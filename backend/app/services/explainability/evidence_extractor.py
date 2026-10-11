
import re


def extract_evidence(
    resume_text: str,
    skills: list[str],
) -> list[dict]:
    """Find text snippets supporting detected resume skills."""
    text = resume_text or ""
    evidence = []

    for skill in skills or []:
        skill_text = str(skill).strip()

        if not skill_text:
            continue

        match = re.search(
            re.escape(skill_text),
            text,
            flags=re.IGNORECASE,
        )

        if match:
            start = max(0, match.start() - 100)
            end = min(len(text), match.end() + 150)

            evidence.append({
                "skill": skill_text,
                "evidence": text[start:end].strip(),
                "found": True,
            })
        else:
            evidence.append({
                "skill": skill_text,
                "evidence": None,
                "found": False,
            })

    return evidence
