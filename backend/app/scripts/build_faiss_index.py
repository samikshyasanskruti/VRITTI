
from pathlib import Path
import logging

import faiss
import numpy as np

ROOT = Path(__file__).resolve().parents[1]
OUTPUT_DIR = ROOT / "vector_store/jobs"
EMBEDDINGS_PATH = OUTPUT_DIR / "embeddings.npy"
INDEX_PATH = OUTPUT_DIR / "jobs.faiss"

logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")


def main():
    if not EMBEDDINGS_PATH.exists():
        raise FileNotFoundError(
            f"Embeddings not found: {EMBEDDINGS_PATH}. "
            "Run build_embeddings.py first."
        )

    embeddings = np.load(EMBEDDINGS_PATH, mmap_mode="r")

    if embeddings.ndim != 2 or embeddings.shape[0] == 0:
        raise ValueError("The embeddings file contains no valid vectors.")

    dimension = embeddings.shape[1]
    index = faiss.IndexFlatIP(dimension)

    # Add vectors in batches to avoid a large temporary memory allocation.
    batch_size = 10000
    for start in range(0, embeddings.shape[0], batch_size):
        batch = np.asarray(
            embeddings[start:start + batch_size],
            dtype=np.float32,
        )
        index.add(batch)

        logging.info(
            "Indexed %s / %s vectors",
            index.ntotal,
            embeddings.shape[0],
        )

    faiss.write_index(index, str(INDEX_PATH))

    logging.info("FAISS index saved to %s", INDEX_PATH)
    logging.info("Total indexed jobs: %s", index.ntotal)


if __name__ == "__main__":
    main()
