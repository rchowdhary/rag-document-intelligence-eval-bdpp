from collections.abc import Sequence
from typing import Protocol

import numpy as np
from numpy.typing import NDArray

from rag_document_intelligence_eval.models import DocumentChunk


DEFAULT_EMBEDDING_MODEL_NAME = "BAAI/bge-small-en-v1.5"
QUERY_INSTRUCTION = "Represent this sentence for searching relevant passages: "


class EmbeddingModel(Protocol):
    def encode(
        self,
        sentences: str | list[str],
        *,
        convert_to_numpy: bool,
        normalize_embeddings: bool,
    ) -> NDArray[np.float32]:
        ...


def load_embedding_model(
    model_name: str = DEFAULT_EMBEDDING_MODEL_NAME,
    device: str = "cpu",
) -> EmbeddingModel:
    from sentence_transformers import SentenceTransformer

    return SentenceTransformer(model_name, device=device)


def embed_chunks(
    chunks: Sequence[DocumentChunk],
    model: EmbeddingModel,
) -> NDArray[np.float32]:
    if not chunks:
        raise ValueError("chunks must not be empty")

    texts = [chunk.text for chunk in chunks]

    embeddings = model.encode(
        texts,
        convert_to_numpy=True,
        normalize_embeddings=False,
    )

    result = np.asarray(embeddings, dtype=np.float32)

    if result.ndim != 2:
        raise ValueError("chunk embeddings must be a two-dimensional array")

    if result.shape[0] != len(chunks):
        raise ValueError(
            "chunk embedding count must match the number of input chunks"
        )

    return result


def embed_query(
    query: str,
    model: EmbeddingModel,
) -> NDArray[np.float32]:
    if not query.strip():
        raise ValueError("query must not be empty")

    instructed_query = f"{QUERY_INSTRUCTION}{query}"

    embedding = model.encode(
        instructed_query,
        convert_to_numpy=True,
        normalize_embeddings=False,
    )

    result = np.asarray(embedding, dtype=np.float32)

    if result.ndim != 1:
        raise ValueError("query embedding must be a one-dimensional array")

    return result
