import json
import re

from sqlalchemy.orm import Session

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
    "power bi", "tableau", "scipy", "matplotlib",
    "seaborn", "transformers", "hugging face",
    "data engineering", "cloud computing", "restful api",
    "microservices", "agile", "scrum", "linux",
]


def extract_skills(text):
    if not text:
        return []

    text = text.lower()
    found = []

    for skill in SKILLS:
        pattern = r"(?<!\w)" + re.escape(skill.lower()) + r"(?!\w)"

        if re.search(pattern, text):
            found.append(skill)

    return list(dict.fromkeys(found))


def main():
    db: Session = SessionLocal()

    scanned = 0
    updated = 0
    errors = 0

    try:
        jobs = db.query(Job).yield_per(500)

        for job in jobs:
            scanned += 1

            description = job.description or ""
            required = extract_skills(description)

            # Existing job descriptions are the source of truth.
            # These are detected skills, not verified employer requirements.
            preferred = []

            if not required:
                continue

            job.required_skills_json = json.dumps(
                required,
                ensure_ascii=False,
            )
            job.preferred_skills_json = json.dumps(
                preferred,
                ensure_ascii=False,
            )

            updated += 1

            if updated % 1000 == 0:
                db.commit()
                print(f"Scanned: {scanned}, updated: {updated}")

        db.commit()

        print("\nJob skill extraction completed.")
        print("Jobs scanned:", scanned)
        print("Jobs updated:", updated)
        print("Jobs without detected skills:", scanned - updated)

        print("\nSample updated jobs:")
        samples = (
            db.query(Job)
            .filter(Job.required_skills_json != "[]")
            .limit(5)
            .all()
        )

        for job in samples:
            print("\nJob:", job.title)
            print("Detected skills:", job.required_skills_json)

    except Exception:
        db.rollback()
        raise

    finally:
        db.close()


if __name__ == "__main__":
    main()