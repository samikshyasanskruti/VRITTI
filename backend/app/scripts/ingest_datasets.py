
from pathlib import Path
import sqlite3
import logging

import pandas as pd

# ============================================================
# PATHS
# ============================================================
ROOT = Path(__file__).resolve().parents[1]

RESUME_CSV = ROOT / "data" / "raw" / "resume" / "extracted" / "Resume.csv"
JOBS_CSV = ROOT / "data" / "raw" / "internships" / "extracted" / "postings.csv"

DB_PATH = ROOT / "data" / "database" / "dataset.db"
CHUNK_SIZE = 2000

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s",
)


# ============================================================
# VALIDATE DATASETS
# ============================================================
def validate_files():
    if not RESUME_CSV.is_file():
        raise FileNotFoundError(
            f"Resume CSV not found: {RESUME_CSV}"
        )

    if not JOBS_CSV.is_file():
        raise FileNotFoundError(
            f"Job postings CSV not found: {JOBS_CSV}"
        )

    DB_PATH.parent.mkdir(parents=True, exist_ok=True)

    logging.info("Resume dataset: %s", RESUME_CSV)
    logging.info("Job dataset: %s", JOBS_CSV)
    logging.info("Database: %s", DB_PATH)


# ============================================================
# CREATE TABLES
# ============================================================
def create_tables(conn):
    conn.execute("""
        CREATE TABLE IF NOT EXISTS dataset_resumes (
            source_id TEXT PRIMARY KEY,
            category TEXT,
            resume_text TEXT NOT NULL
        )
    """)

    conn.execute("""
        CREATE TABLE IF NOT EXISTS dataset_jobs (
            source_id TEXT PRIMARY KEY,
            title TEXT,
            company TEXT,
            location TEXT,
            description TEXT,
            skills_desc TEXT,
            source_url TEXT
        )
    """)

    conn.commit()


# ============================================================
# INGEST RESUMES
# ============================================================
def ingest_resumes(conn):
    logging.info("Starting resume ingestion...")

    total_read = 0
    total_inserted = 0

    for chunk in pd.read_csv(
        RESUME_CSV,
        usecols=["ID", "Resume_str", "Category"],
        dtype={"ID": str},
        chunksize=CHUNK_SIZE,
        on_bad_lines="warn",
    ):
        chunk = chunk.fillna("")
        rows = []

        for _, row in chunk.iterrows():
            source_id = str(row["ID"]).strip()
            resume_text = str(row["Resume_str"]).strip()
            category = str(row["Category"]).strip()

            if not source_id or not resume_text:
                continue

            rows.append((source_id, category, resume_text))

        before = conn.total_changes

        conn.executemany("""
            INSERT OR IGNORE INTO dataset_resumes
            (source_id, category, resume_text)
            VALUES (?, ?, ?)
        """, rows)

        total_inserted += conn.total_changes - before
        total_read += len(chunk)
        conn.commit()

        logging.info(
            "Resume rows read: %s | New records inserted: %s",
            total_read,
            total_inserted,
        )

    count = conn.execute(
        "SELECT COUNT(*) FROM dataset_resumes"
    ).fetchone()[0]

    logging.info("Resume ingestion complete. Total stored: %s", count)


# ============================================================
# INGEST JOB POSTINGS
# ============================================================
def ingest_jobs(conn):
    logging.info("Starting job-posting ingestion...")

    columns = [
        "job_id",
        "title",
        "company_name",
        "location",
        "description",
        "skills_desc",
        "job_posting_url",
    ]

    total_read = 0
    total_inserted = 0

    for chunk in pd.read_csv(
        JOBS_CSV,
        usecols=columns,
        dtype={"job_id": str},
        chunksize=CHUNK_SIZE,
        on_bad_lines="warn",
    ):
        chunk = chunk.fillna("")
        rows = []

        for _, row in chunk.iterrows():
            source_id = str(row["job_id"]).strip()
            title = str(row["title"]).strip()
            description = str(row["description"]).strip()

            if not source_id or source_id.lower() == "nan":
                continue

            if not title and not description:
                continue

            rows.append((
                source_id,
                title,
                str(row["company_name"]).strip(),
                str(row["location"]).strip(),
                description,
                str(row["skills_desc"]).strip(),
                str(row["job_posting_url"]).strip(),
            ))

        before = conn.total_changes

        conn.executemany("""
            INSERT OR IGNORE INTO dataset_jobs
            (source_id, title, company, location,
             description, skills_desc, source_url)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        """, rows)

        total_inserted += conn.total_changes - before
        total_read += len(chunk)
        conn.commit()

        logging.info(
            "Job rows read: %s | New records inserted: %s",
            total_read,
            total_inserted,
        )

    count = conn.execute(
        "SELECT COUNT(*) FROM dataset_jobs"
    ).fetchone()[0]

    logging.info("Job ingestion complete. Total stored: %s", count)


# ============================================================
# MAIN
# ============================================================
def main():
    validate_files()

    with sqlite3.connect(DB_PATH) as conn:
        create_tables(conn)
        ingest_resumes(conn)
        ingest_jobs(conn)

        resume_count = conn.execute(
            "SELECT COUNT(*) FROM dataset_resumes"
        ).fetchone()[0]

        job_count = conn.execute(
            "SELECT COUNT(*) FROM dataset_jobs"
        ).fetchone()[0]

    logging.info("=" * 55)
    logging.info("DATASET INGESTION FINISHED")
    logging.info("Stored resumes: %s", resume_count)
    logging.info("Stored job postings: %s", job_count)
    logging.info("Database: %s", DB_PATH)
    logging.info("=" * 55)


if __name__ == "__main__":
    main()
