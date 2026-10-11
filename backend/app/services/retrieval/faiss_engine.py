
from pathlib import Path

import faiss
import numpy as np


def load_index(index_path: str | Path):
    path = Path(index_path)

    if not path.exists():
        raise FileNotFoundError(f"FAISS index not found: {path}")

    return faiss.read_index(str(path))


def search_index(index, query_vector, top_k: int = 20) -> list[tuple[int, float]]:
    """Search a FAISS inner-product index."""
    if top_k < 1:
        return []

    vector = np.asarray(query_vector, dtype=np.float32).reshape(1, -1)

    if vector.shape[1] != index.d:
        raise ValueError(
            f"Query vector dimension {vector.shape[1]} "
            f"does not match FAISS dimension {index.d}."
        )

    k = min(top_k, index.ntotal)

    if k == 0:
        return []

    scores, indices = index.search(vector, k)

    return [
        (int(idx), float(score))
        for idx, score in zip(indices[0], scores[0])
        if idx >= 0
    ]
