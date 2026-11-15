from rag_document_intelligence_eval.models import DocumentMetadata, EvidenceRole


CORPUS_DOCUMENTS: tuple[DocumentMetadata, ...] = (
    DocumentMetadata(
        document_id="platform_overview",
        filename="01-platform-overview.md",
        title="Batch Data Processing Platform — Overview",
        evidence_role=EvidenceRole.PLATFORM_CONTEXT,
    ),
    DocumentMetadata(
        document_id="ingestion_validation",
        filename="02-ingestion-validation.md",
        title="Batch Data Processing Platform — Ingestion and Validation",
        evidence_role=EvidenceRole.PROCESSING_REQUIREMENTS,
    ),
    DocumentMetadata(
        document_id="transformation",
        filename="03-transformation.md",
        title="Batch Data Processing Platform — Transformation",
        evidence_role=EvidenceRole.PROCESSING_REQUIREMENTS,
    ),
    DocumentMetadata(
        document_id="dataset_versioning",
        filename="04-dataset-versioning.md",
        title="Batch Data Processing Platform — Dataset Versioning",
        evidence_role=EvidenceRole.PROCESSING_REQUIREMENTS,
    ),
    DocumentMetadata(
        document_id="output_verification",
        filename="05-output-verification.md",
        title="Batch Data Processing Platform — Output Verification",
        evidence_role=EvidenceRole.VERIFICATION_REQUIREMENTS,
    ),
    DocumentMetadata(
        document_id="diagnostics",
        filename="06-diagnostics.md",
        title="Batch Data Processing Platform — Diagnostics and Processing Outcome Reporting",
        evidence_role=EvidenceRole.DIAGNOSTIC_REQUIREMENTS,
    ),
)


CORPUS_BY_FILENAME: dict[str, DocumentMetadata] = {
    document.filename: document for document in CORPUS_DOCUMENTS
}
