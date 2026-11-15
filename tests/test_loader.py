from pathlib import Path

from rag_document_intelligence_eval.corpus import CORPUS_DOCUMENTS
from rag_document_intelligence_eval.loader import (
    load_corpus,
    load_document,
    validate_corpus_files,
)


def test_load_document_reads_utf8_text(tmp_path: Path) -> None:
    metadata = CORPUS_DOCUMENTS[0]
    expected_text = "# BDPP Test\n\nRésumé: équipement disponible.\n"
    document_path = tmp_path / metadata.filename
    document_path.write_text(expected_text, encoding="utf-8")

    document = load_document(tmp_path, metadata)

    assert document.path == document_path
    assert document.metadata is metadata
    assert document.text == expected_text


def test_load_corpus_preserves_deterministic_corpus_order(
    tmp_path: Path,
) -> None:
    for index, metadata in enumerate(CORPUS_DOCUMENTS):
        document_path = tmp_path / metadata.filename
        document_path.write_text(
            f"# Test Document {index}\n",
            encoding="utf-8",
        )

    documents = load_corpus(tmp_path)

    assert len(documents) == len(CORPUS_DOCUMENTS)

    assert tuple(
        document.metadata for document in documents
    ) == tuple(CORPUS_DOCUMENTS)

    assert tuple(
        document.path.name for document in documents
    ) == tuple(
        metadata.filename for metadata in CORPUS_DOCUMENTS
    )


def test_validate_corpus_files_accepts_complete_corpus(
    tmp_path: Path,
) -> None:
    for metadata in CORPUS_DOCUMENTS:
        (tmp_path / metadata.filename).write_text(
            "# Test\n",
            encoding="utf-8",
        )

    validate_corpus_files(tmp_path)


def test_validate_corpus_files_reports_missing_documents(
    tmp_path: Path,
) -> None:
    for metadata in CORPUS_DOCUMENTS[:-2]:
        (tmp_path / metadata.filename).write_text(
            "# Test\n",
            encoding="utf-8",
        )

    try:
        validate_corpus_files(tmp_path)
    except FileNotFoundError as exc:
        message = str(exc)
    else:
        raise AssertionError("Expected FileNotFoundError")

    assert "05-output-verification.md" in message
    assert "06-diagnostics.md" in message


def test_load_corpus_validates_missing_documents_before_loading(
    tmp_path: Path,
) -> None:
    for metadata in CORPUS_DOCUMENTS[:-2]:
        (tmp_path / metadata.filename).write_text(
            "# Test\n",
            encoding="utf-8",
        )

    try:
        load_corpus(tmp_path)
    except FileNotFoundError as exc:
        message = str(exc)
    else:
        raise AssertionError("Expected FileNotFoundError")

    assert "05-output-verification.md" in message
    assert "06-diagnostics.md" in message


def test_load_corpus_loads_actual_bdpp_documents() -> None:
    corpus_directory = (
        Path(__file__).resolve().parents[1]
        / "data"
        / "corpus"
    )

    documents = load_corpus(corpus_directory)

    assert len(documents) == len(CORPUS_DOCUMENTS)

    assert tuple(
        document.metadata for document in documents
    ) == tuple(CORPUS_DOCUMENTS)

    assert all(document.path.is_file() for document in documents)
    assert all(document.text.strip() for document in documents)
