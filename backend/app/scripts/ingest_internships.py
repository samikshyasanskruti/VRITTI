
from pathlib import Path
import sqlite3
import logging
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
CSV_PATH = ROOT / "data/raw/internships/extracted/postings.csv"
DB_PATH = ROOT / "data/database/dataset.db"
CHUNK_SIZE = 2000

COLUMNS = [
    "job_id",
    "title",
    "company_name",
    "location",
    "description",
    "skills_desc",
    "job_posting_url",
]

logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")


def main():
    if not CSV_PATH.exists():
        raise FileNotFoundError(f"Job postings dataset not found: {CSV_PATH}")

    DB_PATH.parent.mkdir(parents=True, exist_ok=True)

    conn = sqlite3.connect(DB_PATH)
    try:
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

        total = 0
        for chunk in pd.read_csv(
            CSV_PATH,
            usecols=COLUMNS,
            chunksize=CHUNK_SIZE,
            dtype={"job_id": str},
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

            conn.executemany("""
                INSERT OR IGNORE INTO dataset_jobs
                (source_id, title, company, location,
                 description, skills_desc, source_url)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            """, rows)
            conn.commit()

            total += len(rows)
            logging.info("Processed %s job rows", total)

        count = conn.execute(
            "SELECT COUNT(*) FROM dataset_jobs"
        ).fetchone()[0]
        logging.info("Job ingestion complete. Database total: %s", count)

    finally:
        conn.close()


if __name__ == "__main__":
    main()
