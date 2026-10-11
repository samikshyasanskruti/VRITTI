
from pathlib import Path
import sqlite3
import logging
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
CSV_PATH = ROOT / "data/raw/resumes/extracted/Resume.csv"
DB_PATH = ROOT / "data/database/dataset.db"
CHUNK_SIZE = 1000

logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")


def main():
    if not CSV_PATH.exists():
        raise FileNotFoundError(f"Resume dataset not found: {CSV_PATH}")

    DB_PATH.parent.mkdir(parents=True, exist_ok=True)

    conn = sqlite3.connect(DB_PATH)
    try:
        conn.execute("""
            CREATE TABLE IF NOT EXISTS dataset_resumes (
                source_id TEXT PRIMARY KEY,
                category TEXT,
                resume_text TEXT NOT NULL
            )
        """)
        conn.commit()

        total = 0
        for chunk in pd.read_csv(
            CSV_PATH,
            usecols=["ID", "Resume_str", "Category"],
            chunksize=CHUNK_SIZE,
            dtype={"ID": str},
            on_bad_lines="warn",
        ):
            chunk = chunk.fillna("")
            rows = []

            for _, row in chunk.iterrows():
                source_id = str(row["ID"]).strip()
                resume_text = str(row["Resume_str"]).strip()

                if source_id and resume_text:
                    rows.append((
                        source_id,
                        str(row["Category"]).strip(),
                        resume_text,
                    ))

            conn.executemany("""
                INSERT OR IGNORE INTO dataset_resumes
                (source_id, category, resume_text)
                VALUES (?, ?, ?)
            """, rows)
            conn.commit()

            total += len(rows)
            logging.info("Processed %s resume rows", total)

        count = conn.execute(
            "SELECT COUNT(*) FROM dataset_resumes"
        ).fetchone()[0]
        logging.info("Resume ingestion complete. Database total: %s", count)

    finally:
        conn.close()


if __name__ == "__main__":
    main()