from rag_document_intelligence_eval.corpus import (
    CORPUS_BY_FILENAME,
    CORPUS_DOCUMENTS,
)
from rag_document_intelligence_eval.models import EvidenceRole


def test_corpus_contains_expected_documents_in_deterministic_order() -> None:
    assert [document.filename for document in CORPUS_DOCUMENTS] == [
        "01-platform-overview.md",
        "02-ingestion-validation.md",
        "03-transformation.md",
        "04-dataset-versioning.md",
        "05-output-verification.md",
        "06-diagnostics.md",
    ]


def test_corpus_document_ids_are_unique() -> None:
    document_ids = [document.document_id for document in CORPUS_DOCUMENTS]

    assert len(document_ids) == len(set(document_ids))


def test_corpus_filenames_are_unique() -> None:
    filenames = [document.filename for document in CORPUS_DOCUMENTS]

    assert len(filenames) == len(set(filenames))


def test_filename_lookup_matches_corpus_metadata() -> None:
    assert len(CORPUS_BY_FILENAME) == len(CORPUS_DOCUMENTS)

    for document in CORPUS_DOCUMENTS:
        assert CORPUS_BY_FILENAME[document.filename] == document


def test_corpus_covers_expected_evidence_roles() -> None:
    assert {document.evidence_role for document in CORPUS_DOCUMENTS} == {
        EvidenceRole.PLATFORM_CONTEXT,
        EvidenceRole.PROCESSING_REQUIREMENTS,
        EvidenceRole.VERIFICATION_REQUIREMENTS,
        EvidenceRole.DIAGNOSTIC_REQUIREMENTS,
    }
