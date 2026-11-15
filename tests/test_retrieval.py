import numpy as np
import pytest

from rag_document_intelligence_eval.models import (
    DocumentChunk,
    DocumentMetadata,
    EvidenceRole,
)
from rag_document_intelligence_eval.retrieval import (
    retrieve_by_similarity,
)


def make_chunks(count=3):
    metadata = DocumentMetadata(
        document_id="test_document",
        filename="test.md",
        title="Test Document",
        evidence_role=EvidenceRole.PLATFORM_CONTEXT,
    )

    return [
        DocumentChunk(
            chunk_id=f"test_document::{index:03d}",
            document_metadata=metadata,
            heading=f"Section {index}",
            text=f"Chunk {index}",
            chunk_index=index,
        )
        for index in range(count)
    ]


def test_retrieve_ranks_by_cosine_similarity():
    chunks = make_chunks()

    embeddings = np.array(
        [[0.0, 5.0], [2.0, 0.0], [-9.0, 0.0]],
        dtype=np.float32,
    )
    query = np.array([10.0, 0.0], dtype=np.float32)

    results = retrieve_by_similarity(
        chunks, embeddings, query, top_k=3
    )

    assert [result.rank for result in results] == [1, 2, 3]
    assert [result.chunk for result in results] == [
        chunks[1], chunks[0], chunks[2]
    ]
    np.testing.assert_allclose(
        [result.score for result in results],
        [1.0, 0.0, -1.0],
        atol=1e-6,
    )


def test_retrieve_preserves_order_for_tied_scores():
    chunks = make_chunks()

    embeddings = np.array(
        [[1.0, 0.0], [2.0, 0.0], [0.0, 1.0]],
        dtype=np.float32,
    )
    query = np.array([1.0, 0.0], dtype=np.float32)

    results = retrieve_by_similarity(
        chunks, embeddings, query, top_k=2
    )

    assert [result.chunk for result in results] == [
        chunks[0], chunks[1]
    ]
    assert [result.rank for result in results] == [1, 2]


def test_retrieve_respects_top_k():
    chunks = make_chunks()

    embeddings = np.array(
        [[0.0, 1.0], [1.0, 0.0], [-1.0, 0.0]],
        dtype=np.float32,
    )
    query = np.array([1.0, 0.0], dtype=np.float32)

    results = retrieve_by_similarity(
        chunks, embeddings, query, top_k=1
    )

    assert len(results) == 1
    assert results[0].rank == 1
    assert results[0].chunk == chunks[1]


@pytest.mark.parametrize("top_k", [0, -1, 4])
def test_retrieve_rejects_invalid_top_k(top_k):
    chunks = make_chunks()
    embeddings = np.ones((3, 2), dtype=np.float32)
    query = np.ones(2, dtype=np.float32)

    with pytest.raises(ValueError, match="top_k"):
        retrieve_by_similarity(
            chunks, embeddings, query, top_k=top_k
        )


@pytest.mark.parametrize(
    "embeddings, query, expected_message",
    [
        (
            np.array([1.0, 0.0]),
            np.array([1.0, 0.0]),
            "two-dimensional",
        ),
        (
            np.array([[1.0, 0.0]]),
            np.array([1.0, 0.0]),
            "count must match",
        ),
        (
            np.ones((3, 2)),
            np.array([[1.0, 0.0]]),
            "one-dimensional",
        ),
        (
            np.ones((3, 2)),
            np.array([1.0, 0.0, 0.0]),
            "dimensions must match",
        ),
    ],
)
def test_retrieve_rejects_invalid_shapes(
    embeddings, query, expected_message
):
    chunks = make_chunks()

    with pytest.raises(ValueError, match=expected_message):
        retrieve_by_similarity(
            chunks, embeddings, query, top_k=2
        )


def test_retrieve_rejects_zero_norm_query():
    chunks = make_chunks()
    embeddings = np.ones((3, 2), dtype=np.float32)
    query = np.zeros(2, dtype=np.float32)

    with pytest.raises(ValueError, match="nonzero norm"):
        retrieve_by_similarity(
            chunks, embeddings, query, top_k=2
        )


def test_retrieve_rejects_zero_norm_chunk():
    chunks = make_chunks()
    embeddings = np.array(
        [[1.0, 0.0], [0.0, 0.0], [0.0, 1.0]],
        dtype=np.float32,
    )
    query = np.array([1.0, 0.0], dtype=np.float32)

    with pytest.raises(ValueError, match="nonzero norm"):
        retrieve_by_similarity(
            chunks, embeddings, query, top_k=2
        )
