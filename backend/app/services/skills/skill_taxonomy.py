
SKILL_TAXONOMY = {
    "programming": [
        "python", "java", "javascript", "typescript", "c++", "c#",
    ],
    "data_science": [
        "machine learning", "deep learning", "statistics",
        "pandas", "numpy", "scikit-learn",
    ],
    "ai_nlp": [
        "artificial intelligence", "natural language processing",
        "computer vision", "generative ai", "llm",
    ],
    "databases": [
        "sql", "mysql", "postgresql", "mongodb",
    ],
    "cloud_devops": [
        "aws", "azure", "google cloud", "docker", "kubernetes",
    ],
    "analytics": [
        "excel", "power bi", "tableau", "data analysis",
    ],
}


def get_skill_category(skill: str) -> str:
    normalized = str(skill or "").strip().lower()

    for category, skills in SKILL_TAXONOMY.items():
        if normalized in skills:
            return category

    return "other"
