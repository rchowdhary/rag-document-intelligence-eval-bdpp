import numpy as np
import pytest

from rag_document_intelligence_eval.embeddings import (
    QUERY_INSTRUCTION,
    embed_chunks,
    embed_query,
)
from rag_document_intelligence_eval.models import (
    DocumentChunk,
    DocumentMetadata,
    EvidenceRole,
)


class StubEmbeddingModel:
    def __init__(self, output):
        self.output = output
        self.calls = []

    def encode(
        self,
        sentences,
        *,
        convert_to_numpy,
        normalize_embeddings,
    ):
        self.calls.append(
            (sentences, convert_to_numpy, normalize_embeddings)
        )
        return self.output


def make_chunk(text, index):
    metadata = DocumentMetadata(
        document_id="test_document",
        filename="test.md",
        title="Test Document",
        evidence_role=EvidenceRole.PLATFORM_CONTEXT,
    )

    return DocumentChunk(
        chunk_id=f"test_document::{index:03d}",
        document_metadata=metadata,
        heading="Test Section",
        text=text,
        chunk_index=index,
    )


def test_embed_chunks_preserves_order_and_float32():
    chunks = [make_chunk("first", 0), make_chunk("second", 1)]
    model = StubEmbeddingModel([[1.0, 2.0], [3.0, 4.0]])

    result = embed_chunks(chunks, model)

    assert result.dtype == np.float32
    np.testing.assert_array_equal(
        result,
        np.array([[1.0, 2.0], [3.0, 4.0]], dtype=np.float32),
    )
    assert model.calls == [(["first", "second"], True, False)]


def test_embed_chunks_rejects_empty_input():
    model = StubEmbeddingModel([])

    with pytest.raises(ValueError, match="chunks must not be empty"):
        embed_chunks([], model)

    assert model.calls == []


@pytest.mark.parametrize(
    "invalid_output, expected_message",
    [
        ([1.0, 2.0], "two-dimensional"),
        ([[1.0, 2.0]], "count must match"),
    ],
)
def test_embed_chunks_rejects_invalid_output(
    invalid_output, expected_message
):
    chunks = [make_chunk("first", 0), make_chunk("second", 1)]
    model = StubEmbeddingModel(invalid_output)

    with pytest.raises(ValueError, match=expected_message):
        embed_chunks(chunks, model)


def test_embed_query_uses_bge_instruction():
    model = StubEmbeddingModel([1.0, 2.0, 3.0])

    result = embed_query("What happened?", model)

    assert result.shape == (3,)
    assert result.dtype == np.float32
    assert model.calls == [
        (
            QUERY_INSTRUCTION + "What happened?",
            True,
            False,
        )
    ]


def test_embed_query_rejects_blank_input():
    model = StubEmbeddingModel([])

    with pytest.raises(ValueError, match="query must not be empty"):
        embed_query("   ", model)

    assert model.calls == []


def test_embed_query_rejects_invalid_output_shape():
    model = StubEmbeddingModel([[1.0, 2.0]])

    with pytest.raises(ValueError, match="one-dimensional"):
        embed_query("test query", model)
