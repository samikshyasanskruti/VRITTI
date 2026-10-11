
import re


SECTION_PATTERNS = {
    "summary": r"^(professional\s+summary|summary|profile|objective)$",
    "education": r"^(education|academic\s+background|qualifications)$",
    "experience": r"^(experience|work\s+experience|employment\s+history)$",
    "skills": r"^(technical\s+skills|skills|core\s+competencies)$",
    "projects": r"^(projects|academic\s+projects|personal\s+projects)$",
    "certifications": r"^(certifications|certificates|licenses)$",
}


def detect_sections(text: str) -> dict[str, str]:
    """Split resume text using recognizable section headings."""
    sections = {}
    current_section = "other"
    buffer = []

    def save_buffer():
        content = "\n".join(buffer).strip()
        if content:
            sections[current_section] = (
                sections.get(current_section, "") + "\n" + content
            ).strip()

    for line in (text or "").splitlines():
        cleaned = line.strip().strip(":").strip()
        normalized = re.sub(r"\s+", " ", cleaned).lower()

        matched_section = None
        for section, pattern in SECTION_PATTERNS.items():
            if re.match(pattern, normalized, re.IGNORECASE):
                matched_section = section
                break

        if matched_section:
            save_buffer()
            current_section = matched_section
            buffer = []
        else:
            buffer.append(line)

    save_buffer()
    return sections
