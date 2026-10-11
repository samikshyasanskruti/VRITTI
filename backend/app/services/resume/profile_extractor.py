
import re


COMMON_SKILLS = [
    "python", "java", "javascript", "typescript", "sql", "c++", "c#",
    "matlab", "php", "kotlin", "swift", "ruby", "r programming",
    "machine learning", "deep learning", "artificial intelligence",
    "data science", "data analysis", "pandas", "numpy",
    "scikit-learn", "tensorflow", "keras", "pytorch", "opencv", "nlp",
    "natural language processing", "nltk", "spacy", "hugging face",
    "transformers", "computer vision", "power bi", "tableau", "excel",
    "statistics", "fastapi", "flask", "django", "spring boot",
    "rest api", "react", "node.js", "html", "css", "git", "github",
    "linux", "docker", "kubernetes", "aws", "azure", "google cloud",
    "spark", "databricks", "postgresql", "mysql", "mongodb", "sqlite",
    "faiss", "langchain", "generative ai", "llm", "communication",
    "project management", "jira", "figma", "flutter", "streamlit",
    "scipy", "matplotlib", "seaborn", "powerpoint", "excel",
    "agile", "scrum", "restful api", "fastapi", "langgraph",
]

HEADINGS = {
    "profile", "summary", "professional summary", "objective",
    "career objective", "about me", "about", "contact",
    "contact information", "personal details", "education",
    "experience", "work experience", "professional experience",
    "skills", "technical skills", "projects", "certifications",
    "certificates", "resume", "curriculum vitae", "cv",
    "internships", "achievements", "languages", "publications",
    "training", "courses", "technical summary",
}

NOT_A_NAME = re.compile(
    r"\b(resume|curriculum vitae|email|e-mail|phone|mobile|linkedin|"
    r"github|address|portfolio|profile|summary|objective)\b",
    re.IGNORECASE,
)

SECTION_ALIASES = {
    "education": [
        "education", "academic background", "educational qualification",
        "educational qualifications", "academics",
    ],
    "experience": [
        "experience", "work experience", "professional experience",
        "internships", "internship", "employment history",
    ],
    "projects": [
        "projects", "academic projects", "personal projects",
        "project experience",
    ],
    "certifications": [
        "certifications", "certificates", "courses", "training",
        "licenses",
    ],
    "achievements": [
        "achievements", "awards", "accomplishments",
    ],
}


def _guess_name(lines: list[str]) -> str | None:
    candidates = []

    for line in lines[:12]:
        cleaned = line.strip().strip("|").strip()

        if cleaned.lower().strip(": ") in HEADINGS:
            continue

        if len(cleaned) > 60 or re.search(r"[@\d]", cleaned):
            continue

        if NOT_A_NAME.search(cleaned):
            continue

        if len(cleaned.split()) > 5:
            continue

        candidates.append(cleaned)

    for line in candidates:
        if re.fullmatch(r"[A-Za-z.'\- ]+", line):
            words = line.split()
            if 2 <= len(words) <= 4:
                return line

    for line in candidates:
        if re.fullmatch(r"[A-Za-z.'\- ]+", line) and len(line.split()) <= 4:
            return line

    return None


def extract_skills(text: str) -> list[str]:
    """Extract skills explicitly mentioned in the resume."""
    if not text:
        return []

    normalized = text.lower()
    found = []

    for skill in COMMON_SKILLS:
        pattern = r"(?<!\w)" + re.escape(skill.lower()) + r"(?!\w)"
        if re.search(pattern, normalized):
            found.append(skill)

    return found


def extract_contact(text: str) -> dict:
    """Extract contact information from resume text."""
    email_match = re.search(
        r"\b[A-Z0-9._%+-]+@[A-Z0-9.-]+\.[A-Z]{2,}\b",
        text or "",
        re.IGNORECASE,
    )

    phone_match = re.search(
        r"(?<!\w)(?:\+?\d[\d\s().-]{7,}\d)(?!\w)",
        text or "",
    )

    lines = [
        line.strip()
        for line in (text or "").splitlines()
        if line.strip()
    ]

    return {
        "name": _guess_name(lines),
        "email": email_match.group(0) if email_match else None,
        "phone": phone_match.group(0).strip() if phone_match else None,
    }


def _normalize_heading(line: str) -> str:
    """Normalize common resume section headings."""
    return re.sub(r"[^a-z ]", "", line.lower()).strip()


def extract_sections(text: str) -> dict:
    """
    Extract text under recognized resume headings.
    The extracted content is taken from the resume, not invented.
    """
    sections = {name: [] for name in SECTION_ALIASES}
    current_section = None

    heading_lookup = {
        _normalize_heading(alias): section
        for section, aliases in SECTION_ALIASES.items()
        for alias in aliases
    }

    other_headings = {
        _normalize_heading(item)
        for item in HEADINGS
    }

    for line in (text or "").splitlines():
        cleaned = line.strip()

        if not cleaned:
            continue

        normalized = _normalize_heading(cleaned.rstrip(":"))

        if normalized in heading_lookup:
            current_section = heading_lookup[normalized]
            continue

        if normalized in other_headings:
            current_section = None
            continue

        # Ignore text outside a recognized section.
        if current_section:
            sections[current_section].append(cleaned)

    return {
        name: "\n".join(lines).strip()
        for name, lines in sections.items()
        if lines
    }


def extract_profile(text: str) -> dict:
    """Build a structured profile from extracted resume text."""
    text = text or ""
    contact = extract_contact(text)
    sections = extract_sections(text)

    return {
        "candidate": contact,
        "skills": extract_skills(text),
        "education": sections.get("education", ""),
        "experience": sections.get("experience", ""),
        "certifications": sections.get("certifications", ""),
        "projects": sections.get("projects", ""),
        "achievements": sections.get("achievements", ""),
        "text_length": len(text),
        "text": text,
    }
