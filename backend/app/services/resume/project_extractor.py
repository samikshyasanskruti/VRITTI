
from backend.app.services.resume.section_detector import detect_sections
from backend.app.services.resume.profile_extractor import extract_skills


def extract_projects(text: str) -> list[dict]:
    """Extract project entries from the Projects section of a resume."""
    sections = detect_sections(text)
    project_text = sections.get("projects", "")

    if not project_text:
        return []

    projects = []
    current_lines = []

    for line in project_text.splitlines():
        line = line.strip()

        if not line:
            if current_lines:
                projects.append("\n".join(current_lines))
                current_lines = []
            continue

        current_lines.append(line)

    if current_lines:
        projects.append("\n".join(current_lines))

    return [
        {
            "title": block.splitlines()[0][:200],
            "description": block,
            "skills": extract_skills(block),
        }
        for block in projects
        if block.strip()
    ]
