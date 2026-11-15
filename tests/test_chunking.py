from pathlib import Path

from rag_document_intelligence_eval.chunking import chunk_document
from rag_document_intelligence_eval.loader import load_corpus
from rag_document_intelligence_eval.models import (
    DocumentMetadata,
    EvidenceRole,
    SourceDocument,
)


def make_test_document(text: str) -> SourceDocument:
    metadata = DocumentMetadata(
        document_id="test_document",
        filename="test_document.md",
        title="Test Document",
        evidence_role=EvidenceRole.PROCESSING_REQUIREMENTS,
    )

    return SourceDocument(
        path=Path("test_document.md"),
        metadata=metadata,
        text=text,
    )


def test_chunk_document_splits_on_level_two_headings() -> None:
    text = (
        "# Test Document\n"
        "\n"
        "Introductory text.\n"
        "\n"
        "## First Section\n"
        "\n"
        "First section text.\n"
        "\n"
        "### Nested Detail\n"
        "\n"
        "Nested detail text.\n"
        "\n"
        "## Second Section\n"
        "\n"
        "Second section text.\n"
    )

    document = make_test_document(text)
    chunks = chunk_document(document)

    assert len(chunks) == 2

    assert chunks[0].chunk_id == "test_document::000"
    assert chunks[0].chunk_index == 0
    assert chunks[0].heading == "First Section"
    assert chunks[0].document_metadata == document.metadata

    assert chunks[1].chunk_id == "test_document::001"
    assert chunks[1].chunk_index == 1
    assert chunks[1].heading == "Second Section"
    assert chunks[1].document_metadata == document.metadata

    first_text, separator, remainder = text.partition(
        "## Second Section\n"
    )

    assert separator
    assert chunks[0].text == first_text
    assert chunks[1].text == separator + remainder


def test_chunk_document_without_level_two_headings() -> None:
    document = make_test_document(
        "# Test Document\n\nIntroductory text only.\n"
    )

    assert chunk_document(document) == ()


def test_chunk_document_preserves_nested_headings() -> None:
    document = make_test_document(
        "# Test Document\n"
        "\n"
        "## Processing Requirements\n"
        "\n"
        "Processing summary.\n"
        "\n"
        "### Validation Details\n"
        "\n"
        "Validate the input records.\n"
    )

    chunks = chunk_document(document)

    assert len(chunks) == 1
    assert chunks[0].heading == "Processing Requirements"
    assert "### Validation Details\n" in chunks[0].text
    assert "Validate the input records.\n" in chunks[0].text


def test_chunk_document_produces_expected_bdpp_chunks() -> None:
    corpus_directory = (
        Path(__file__).resolve().parents[1] / "data" / "corpus"
    )

    documents = load_corpus(corpus_directory)

    expected_counts = {
        "platform_overview": 6,
        "ingestion_validation": 8,
        "transformation": 7,
        "dataset_versioning": 8,
        "output_verification": 9,
        "diagnostics": 9,
    }

    actual_counts = {
        document.metadata.document_id: len(chunk_document(document))
        for document in documents
    }

    assert actual_counts == expected_counts
    assert sum(actual_counts.values()) == 47


def test_chunk_document_determinism_and_attribution() -> None:
    corpus_directory = (
        Path(__file__).resolve().parents[1] / "data" / "corpus"
    )

    documents = load_corpus(corpus_directory)
    all_chunk_ids = []

    for document in documents:
        first_run = chunk_document(document)
        second_run = chunk_document(document)

        assert first_run == second_run

        for index, chunk in enumerate(first_run):
            assert chunk.chunk_index == index
            assert chunk.chunk_id == (
                f"{document.metadata.document_id}::{index:03d}"
            )
            assert chunk.document_metadata == document.metadata
            assert chunk.heading
            assert chunk.text

            all_chunk_ids.append(chunk.chunk_id)

    assert len(all_chunk_ids) == 47
    assert len(all_chunk_ids) == len(set(all_chunk_ids))
