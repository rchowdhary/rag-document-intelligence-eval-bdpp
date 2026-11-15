from pathlib import Path

from rag_document_intelligence_eval.corpus import CORPUS_DOCUMENTS
from rag_document_intelligence_eval.models import DocumentMetadata, SourceDocument


def load_document(
    corpus_directory: Path,
    metadata: DocumentMetadata,
) -> SourceDocument:
    """Load one UTF-8 document using its explicit corpus metadata."""
    path = corpus_directory / metadata.filename
    text = path.read_text(encoding="utf-8")

    return SourceDocument(
        path=path,
        metadata=metadata,
        text=text,
    )


def load_corpus(
    corpus_directory: Path,
) -> tuple[SourceDocument, ...]:
    """Load the configured corpus in deterministic metadata order."""
    validate_corpus_files(corpus_directory)

    return tuple(
        load_document(corpus_directory, metadata)
        for metadata in CORPUS_DOCUMENTS
    )


def validate_corpus_files(corpus_directory: Path) -> None:
    """Verify that every configured corpus document exists."""
    missing_filenames = [
        metadata.filename
        for metadata in CORPUS_DOCUMENTS
        if not (corpus_directory / metadata.filename).is_file()
    ]

    if missing_filenames:
        missing_list = ", ".join(missing_filenames)
        raise FileNotFoundError(
            f"Missing corpus document(s): {missing_list}"
        )
