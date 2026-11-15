from collections.abc import Sequence

import numpy as np
from numpy.typing import NDArray

from rag_document_intelligence_eval.models import (
    DocumentChunk,
    RetrievalResult,
)


def retrieve_by_similarity(
    chunks: Sequence[DocumentChunk],
    chunk_embeddings: NDArray[np.float32],
    query_embedding: NDArray[np.float32],
    top_k: int = 3,
) -> list[RetrievalResult]:
    if top_k <= 0:
        raise ValueError("top_k must be greater than zero")

    if top_k > len(chunks):
        raise ValueError("top_k must not exceed the number of chunks")

    if chunk_embeddings.ndim != 2:
        raise ValueError(
            "chunk embeddings must be a two-dimensional array"
        )

    if chunk_embeddings.shape[0] != len(chunks):
        raise ValueError(
            "chunk embedding count must match the number of chunks"
        )

    if query_embedding.ndim != 1:
        raise ValueError(
            "query embedding must be a one-dimensional array"
        )

    if chunk_embeddings.shape[1] != query_embedding.shape[0]:
        raise ValueError(
            "chunk and query embedding dimensions must match"
        )

    query_norm = np.linalg.norm(query_embedding)

    if query_norm == 0.0:
        raise ValueError("query embedding must have nonzero norm")

    chunk_norms = np.linalg.norm(chunk_embeddings, axis=1)

    if np.any(chunk_norms == 0.0):
        raise ValueError("chunk embeddings must have nonzero norm")

    scores = (
        chunk_embeddings @ query_embedding
    ) / (chunk_norms * query_norm)

    ranked_indexes = np.argsort(-scores, kind="stable")[:top_k]

    return [
        RetrievalResult(
            rank=rank,
            score=float(scores[index]),
            chunk=chunks[index],
        )
        for rank, index in enumerate(ranked_indexes, start=1)
    ]
