
import re


SKILLS = [
    "Python", "Java", "JavaScript", "TypeScript", "SQL", "C++", "C#",
    "Machine Learning", "Deep Learning", "Artificial Intelligence",
    "Natural Language Processing", "Data Science", "Data Analysis",
    "Statistics", "Pandas", "NumPy", "Scikit-learn", "TensorFlow",
    "PyTorch", "Power BI", "Tableau", "Excel", "AWS", "Azure",
    "Google Cloud", "Docker", "Kubernetes", "Git", "FastAPI", "Flask",
    "Django", "React", "Node.js", "PostgreSQL", "MySQL", "MongoDB",
    "Apache Spark", "Databricks", "Airflow", "ETL", "Communication",
    "Project Management", "Leadership", "Adobe Photoshop", "Illustrator",
    "InDesign", "Canva", "Google Analytics", "Marketing",
    "Graphic Design", "Microsoft Office", "Customer Service", "Sales",
]


def extract_required_skills(description: str) -> list[str]:
    if not description:
        return []

    found = []
    for skill in SKILLS:
        pattern = r"(?<!\w)" + re.escape(skill) + r"(?!\w)"
        if re.search(pattern, description, re.IGNORECASE):
            found.append(skill)

    return found


def extract_requirements(description: str) -> list[str]:
    if not description:
        return []

    text = re.sub(r"\s+", " ", description).strip()

    # Find an explicit qualifications heading, if one exists.
    heading = re.search(
        r"\b(?:what experience do i need to have|"
        r"what experience do i need|requirements|"
        r"required qualifications|minimum qualifications|"
        r"qualifications|what you'll need|what you will need|"
        r"skills and qualifications|experience and skills)\s*[:?]?\s*",
        text,
        re.IGNORECASE,
    )

    if heading:
        text = text[heading.end():]
    else:
        # Without a heading, do not classify the entire description
        # as requirements. Look only for explicit qualification phrases.
        sentences = re.split(r"(?<=[.!?])\s+", text)
        text = " ".join(
            sentence for sentence in sentences
            if re.search(
                r"\b(must have|required|minimum of|"
                r"bachelor|master|degree required|"
                r"years of experience|years experience|"
                r"proficient in|knowledge of|certification required)\b",
                sentence,
                re.IGNORECASE,
            )
        )

    # Remove sections following qualifications.
    text = re.split(
        r"\b(?:what benefits do i receive|benefits|"
        r"equal opportunity employer|job type|salary|"
        r"expected hours|work location|schedule)\b",
        text,
        maxsplit=1,
        flags=re.IGNORECASE,
    )[0]

    sentences = re.split(r"(?<=[.!?])\s+", text)
    results = []

    for sentence in sentences:
        sentence = sentence.strip(" -•\t")
        if not sentence:
            continue

        if re.search(
            r"\b(required|must have|minimum|bachelor|master|degree|"
            r"experience|proficient|knowledge of|familiarity with|"
            r"certification|preferred|qualification)\b",
            sentence,
            re.IGNORECASE,
        ) and not re.search(
            r"\b(equal opportunity|qualified applicants|"
            r"without regard to|benefits|salary)\b",
            sentence,
            re.IGNORECASE,
        ):
            results.append(sentence)

    return list(dict.fromkeys(results))
