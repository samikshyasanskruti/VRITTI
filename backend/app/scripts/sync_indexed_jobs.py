
import sys
import json
import sqlite3
from pathlib import Path

# ============================================================
# 1. Set project root before importing backend modules
# ============================================================
ROOT = Path(__file__).resolve().parents[3]

if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from sqlalchemy import select

from backend.app.config import PROJECT_ROOT, DATABASE_PATH
from backend.app.database.database import SessionLocal, init_db
from backend.app.models.database_models import Job
from backend.app.services.skills.skill_extractor import extract_skills


# ============================================================
# 2. File paths and settings
# ============================================================
DATASET_DB = ROOT / "data" / "database" / "dataset.db"
METADATA_FILE = ROOT / "vector_store" / "jobs" / "jobs_metadata.json"
BATCH_SIZE = 1000


def serialize_skills(text):
    """Extract known skills and serialize them as a JSON list."""
    skills = extract_skills(text or "")
    return json.dumps(list(dict.fromkeys(skills)), ensure_ascii=False)


# ============================================================
# 3. Synchronize indexed jobs
# ============================================================
def main():
    print("=" * 65)
    print("Vritti - Job Synchronization with Skill Extraction")
    print("=" * 65)

    print("Project root:", ROOT)
    print("Configured root:", PROJECT_ROOT)
    print("Application database:", DATABASE_PATH)
    print("Source database:", DATASET_DB)
    print("Metadata file:", METADATA_FILE)

    if ROOT.resolve() != PROJECT_ROOT.resolve():
        raise RuntimeError(
            f"Project path mismatch.\n"
            f"Script root: {ROOT}\n"
            f"Configured root: {PROJECT_ROOT}"
        )

    if not DATASET_DB.exists():
        raise FileNotFoundError(
            f"Dataset database not found: {DATASET_DB}"
        )

    if not METADATA_FILE.exists():
        raise FileNotFoundError(
            f"Job metadata not found: {METADATA_FILE}"
        )

    with METADATA_FILE.open("r", encoding="utf-8") as file:
        records = json.load(file)

    if not isinstance(records, list):
        raise ValueError(
            "Expected jobs_metadata.json to contain a JSON list."
        )

    source_ids = list(dict.fromkeys(
        str(record["source_id"])
        for record in records
        if isinstance(record, dict)
        and record.get("source_id") is not None
    ))

    if not source_ids:
        raise ValueError("No valid source IDs found in job metadata.")

    print("Metadata records:", len(records))
    print("Unique source IDs:", len(source_ids))

    # Validate source database schema.
    with sqlite3.connect(str(DATASET_DB)) as source_db:
        tables = {
            row[0]
            for row in source_db.execute(
                "SELECT name FROM sqlite_master WHERE type='table'"
            ).fetchall()
        }

        if "dataset_jobs" not in tables:
            raise RuntimeError(
                "The dataset database does not contain dataset_jobs."
            )

        columns = {
            row[1]
            for row in source_db.execute(
                "PRAGMA table_info(dataset_jobs)"
            ).fetchall()
        }

        required_columns = {
            "source_id",
            "title",
            "company",
            "location",
            "description",
        }

        missing_columns = required_columns - columns

        if missing_columns:
            raise RuntimeError(
                f"dataset_jobs is missing columns: {missing_columns}"
            )

    init_db()
    db = SessionLocal()

    imported = 0
    updated = 0
    missing = 0
    skipped = 0
    jobs_with_detected_skills = 0
    detected_skill_total = 0

    try:
        allowed_fields = set(Job.__table__.columns.keys())

        for start in range(0, len(source_ids), BATCH_SIZE):
            batch_ids = source_ids[start:start + BATCH_SIZE]
            placeholders = ",".join("?" for _ in batch_ids)

            with sqlite3.connect(str(DATASET_DB)) as source_db:
                rows = source_db.execute(
                    f"""
                    SELECT
                        source_id,
                        title,
                        company,
                        location,
                        description
                    FROM dataset_jobs
                    WHERE source_id IN ({placeholders})
                    """,
                    batch_ids,
                ).fetchall()

            source_rows = {
                str(row[0]): row
                for row in rows
                if row[0] is not None
            }

            existing_jobs = db.execute(
                select(Job).where(Job.external_id.in_(batch_ids))
            ).scalars().all()

            existing_by_id = {
                str(job.external_id): job
                for job in existing_jobs
                if job.external_id is not None
            }

            for source_id in batch_ids:
                row = source_rows.get(source_id)

                if row is None:
                    missing += 1
                    continue

                _, title, company, location, description = row

                if not title:
                    skipped += 1
                    continue

                description = description or ""

                # Detect skills using the existing project taxonomy.
                # These are detected mentions, not verified mandatory
                # requirements from the employer.
                detected_skills = extract_skills(
                    f"{title}\n{description}"
                )

                if detected_skills:
                    jobs_with_detected_skills += 1
                    detected_skill_total += len(detected_skills)

                values = {
                    "external_id": source_id,
                    "title": title,
                    "company": company,
                    "location": location,
                    "description": description,
                    "required_skills_json": json.dumps(
                        detected_skills,
                        ensure_ascii=False,
                    ),
                    # The source does not reliably distinguish preferred
                    # skills, so do not invent them.
                    "preferred_skills_json": "[]",
                    "work_type": None,
                    "source_dataset": "dataset.db",
                }

                values = {
                    key: value
                    for key, value in values.items()
                    if key in allowed_fields
                }

                job = existing_by_id.get(source_id)

                if job is None:
                    db.add(Job(**values))
                    imported += 1
                else:
                    for key, value in values.items():
                        setattr(job, key, value)
                    updated += 1

            # Commit each batch to avoid a large transaction.
            db.commit()

            processed = min(
                start + len(batch_ids),
                len(source_ids),
            )

            print(
                f"Processed {processed:,}/{len(source_ids):,} "
                "indexed source IDs"
            )

        print("\n" + "=" * 65)
        print("Synchronization completed")
        print("=" * 65)
        print("New jobs imported:", imported)
        print("Existing jobs updated:", updated)
        print("Source IDs not found:", missing)
        print("Records skipped:", skipped)
        print("Jobs with detected skills:", jobs_with_detected_skills)
        print("Total detected skill mentions:", detected_skill_total)
        print(
            "Total jobs in application database:",
            db.query(Job).count(),
        )

    except Exception:
        db.rollback()
        raise

    finally:
        db.close()


if __name__ == "__main__":
    main()
