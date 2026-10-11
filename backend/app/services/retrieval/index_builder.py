
import json
from pathlib import Path

import faiss
import numpy as np


def build_faiss_index(
    embeddings_path: str | Path,
    metadata_path: str | Path,
    index_path: str | Path,
) -> None:
    """Build a FAISS inner-product index from existing embeddings."""
    embeddings_path = Path(embeddings_path)
    metadata_path = Path(metadata_path)
    index_path = Path(index_path)

    if not embeddings_path.exists():
        raise FileNotFoundError(embeddings_path)

    if not metadata_path.exists():
        raise FileNotFoundError(metadata_path)

    with metadata_path.open("r", encoding="utf-8") as file:
        records = json.load(file)

    embeddings = np.load(embeddings_path, mmap_mode="r")

    if embeddings.ndim != 2:
        raise ValueError("Embeddings must be a 2D array.")

    if len(records) != embeddings.shape[0]:
        raise ValueError(
            f"Metadata count {len(records)} does not match "
            f"embedding count {embeddings.shape[0]}."
        )

    index = faiss.IndexFlatIP(embeddings.shape[1])

    batch_size = 10000
    for start in range(0, embeddings.shape[0], batch_size):
        index.add(
            np.asarray(
                embeddings[start:start + batch_size],
                dtype=np.float32,
            )
        )

    index_path.parent.mkdir(parents=True, exist_ok=True)
    faiss.write_index(index, str(index_path))

    print(f"Indexed {index.ntotal:,} records.")
    print(f"Saved index: {index_path}")
