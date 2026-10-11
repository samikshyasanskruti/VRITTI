
from pathlib import Path
import json
import sqlite3
import logging

import numpy as np
from sentence_transformers import SentenceTransformer

# ============================================================
# CONFIGURATION
# ============================================================
ROOT = Path(__file__).resolve().parents[1]

DB_PATH = ROOT / "data" / "database" / "dataset.db"
OUTPUT_DIR = ROOT / "vector_store" / "jobs"

EMBEDDINGS_PATH = OUTPUT_DIR / "embeddings.npy"
METADATA_PATH = OUTPUT_DIR / "jobs_metadata.json"

MODEL_NAME = "sentence-transformers/all-MiniLM-L6-v2"

MAX_JOBS = 50_000
BATCH_SIZE = 64

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s",
)


# ============================================================
# LOAD REAL JOB POSTINGS
# ============================================================
def load_jobs():
    if not DB_PATH.exists():
        raise FileNotFoundError(
            f"Database not found: {DB_PATH}. "
            "Run scripts/ingest_datasets.py first."
        )

    with sqlite3.connect(DB_PATH) as conn:
        rows = conn.execute(
            """
            SELECT source_id, title, company, location,
                   description, skills_desc, source_url
            FROM dataset_jobs
            ORDER BY source_id
            LIMIT ?
            """,
            (MAX_JOBS,),
        ).fetchall()

    if not rows:
        raise RuntimeError(
            "No jobs found in dataset_jobs. "
            "Run scripts/ingest_datasets.py first."
        )

    texts = []
    metadata = []

    for source_id, title, company, location, description, skills, url in rows:
        text = (
            f"Title: {title or ''}\n"
            f"Company: {company or ''}\n"
            f"Location: {location or ''}\n"
            f"Description: {description or ''}\n"
            f"Skills: {skills or ''}"
        ).strip()

        if not text:
            continue

        texts.append(text)
        metadata.append(
            {
                "source_id": str(source_id),
                "title": title or "",
                "company": company or "",
                "location": location or "",
                "description": description or "",
                "skills_desc": skills or "",
                "source_url": url or "",
            }
        )

    return texts, metadata


# ============================================================
# GENERATE EMBEDDINGS
# ============================================================
def main():
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    texts, metadata = load_jobs()
    total = len(texts)

    logging.info("Target: up to %s real job postings", MAX_JOBS)
    logging.info("Jobs selected: %s", total)

    model = SentenceTransformer(MODEL_NAME)
    embedding_batches = []

    for start in range(0, total, BATCH_SIZE):
        end = min(start + BATCH_SIZE, total)

        vectors = model.encode(
            texts[start:end],
            batch_size=BATCH_SIZE,
            convert_to_numpy=True,
            normalize_embeddings=True,
            show_progress_bar=False,
        )

        embedding_batches.append(
            np.asarray(vectors, dtype=np.float32)
        )

        logging.info(
            "Embedded %s / %s job postings",
            end,
            total,
        )

    if not embedding_batches:
        raise RuntimeError("No embeddings were generated.")

    embeddings = np.concatenate(embedding_batches, axis=0)

    if embeddings.shape[0] != len(metadata):
        raise RuntimeError(
            "Embedding count does not match metadata count."
        )

    np.save(EMBEDDINGS_PATH, embeddings)

    with open(METADATA_PATH, "w", encoding="utf-8") as file:
        json.dump(metadata, file, ensure_ascii=False)

    logging.info("=" * 55)
    logging.info("EMBEDDING GENERATION COMPLETED")
    logging.info("Jobs embedded: %s", embeddings.shape[0])
    logging.info("Vector dimensions: %s", embeddings.shape[1])
    logging.info("Embeddings saved: %s", EMBEDDINGS_PATH)
    logging.info("Metadata saved: %s", METADATA_PATH)
    logging.info("=" * 55)


if __name__ == "__main__":
    main()
