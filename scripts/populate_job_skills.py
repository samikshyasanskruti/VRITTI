
import json
import re

from backend.app.database.database import SessionLocal
from backend.app.models.database_models import Job


SKILLS = [
    "python", "java", "javascript", "typescript", "sql", "c++", "c#",
    "machine learning", "deep learning", "artificial intelligence",
    "data science", "data analysis", "pandas", "numpy", "scikit-learn",
    "tensorflow", "pytorch", "keras", "nlp",
    "natural language processing", "computer vision", "opencv",
    "power bi", "tableau", "excel", "statistics",
    "fastapi", "flask", "django", "spring boot", "rest api",
    "react", "node.js", "html", "css", "git", "github",
    "linux", "docker", "kubernetes", "aws", "azure",
    "google cloud", "spark", "databricks", "postgresql",
    "mysql", "mongodb", "sqlite", "faiss", "langchain",
    "generative ai", "llm", "large language models",
    "communication", "project management", "jira",
    "data visualization", "etl", "airflow", "hadoop",
    "scipy", "matplotlib", "seaborn", "transformers",
    "hugging face", "data engineering", "cloud computing",
    "microservices", "agile", "scrum",
]


def extract_skills(text):
    if not text:
        return []

    text = text.lower()
    found = []

    for skill in SKILLS:
        pattern = r"(?<!\w)" + re.escape(skill) + r"(?!\w)"
        if re.search(pattern, text):
            found.append(skill)

    return found


def main():
    db = SessionLocal()
    scanned = 0
    updated = 0

    try:
        jobs = db.query(Job).yield_per(500)

        for job in jobs:
            scanned += 1
            description = job.description or ""

            detected = extract_skills(description)

            # Skip jobs without detected skills.
            if not detected:
                continue

            # These are detected description skills, not verified requirements.
            job.required_skills_json = json.dumps(detected)
            job.preferred_skills_json = json.dumps([])

            updated += 1

            if updated % 500 == 0:
                db.commit()
                print(f"Scanned {scanned}; updated {updated}")

        db.commit()

        print("\nSkill extraction completed.")
        print("Jobs scanned:", scanned)
        print("Jobs updated:", updated)
        print("Jobs without detected skills:", scanned - updated)

        for job in db.query(Job).filter(
            Job.required_skills_json != "[]"
        ).limit(5):
            print("\nJob:", job.title)
            print("Detected skills:", job.required_skills_json)

    except Exception:
        db.rollback()
        raise
    finally:
        db.close()


if __name__ == "__main__":
    main()
