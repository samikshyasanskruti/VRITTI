
import json
from pathlib import Path

from backend.app.config import PROJECT_ROOT
from backend.app.services.retrieval.faiss_engine import load_index

INDEX_DIR = PROJECT_ROOT / "vector_store" / "jobs"
INDEX_PATH = INDEX_DIR / "jobs.faiss"
METADATA_PATH = INDEX_DIR / "jobs_metadata.json"

# This must match the model used to create embeddings.npy.
MODEL_NAME = "sentence-transformers/all-MiniLM-L6-v2"


def load_job_index():
    if not INDEX_PATH.exists():
        raise FileNotFoundError(f"FAISS index missing: {INDEX_PATH}")

    if not METADATA_PATH.exists():
        raise FileNotFoundError(f"FAISS metadata missing: {METADATA_PATH}")

    with METADATA_PATH.open("r", encoding="utf-8") as file:
        records = json.load(file)

    if not isinstance(records, list):
        raise RuntimeError("Expected jobs_metadata.json to contain a JSON list.")

    index = load_index(INDEX_PATH)

    if index.ntotal != len(records):
        raise RuntimeError(
            f"FAISS index contains {index.ntotal} vectors but metadata "
            f"contains {len(records)} records. Rebuild the index."
        )

    return index, {
        "model_name": MODEL_NAME,
        "records": records,
    }
