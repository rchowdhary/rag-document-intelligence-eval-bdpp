from dataclasses import dataclass
from enum import Enum
from pathlib import Path


class EvidenceRole(str, Enum):
    PLATFORM_CONTEXT = "platform_context"
    PROCESSING_REQUIREMENTS = "processing_requirements"
    VERIFICATION_REQUIREMENTS = "verification_requirements"
    DIAGNOSTIC_REQUIREMENTS = "diagnostic_requirements"


@dataclass(frozen=True)
class DocumentMetadata:
    document_id: str
    filename: str
    title: str
    evidence_role: EvidenceRole


@dataclass(frozen=True)
class SourceDocument:
    path: Path
    metadata: DocumentMetadata
    text: str


@dataclass(frozen=True)
class DocumentChunk:
    chunk_id: str
    document_metadata: DocumentMetadata
    heading: str
    text: str
    chunk_index: int


@dataclass(frozen=True)
class RetrievalResult:
    rank: int
    score: float
    chunk: DocumentChunk


@dataclass(frozen=True)
class RetrievalEvaluationQuestion:
    question_id: str
    question_type: str
    question: str
    expected_documents: tuple[str, ...]
    expected_evidence_roles: tuple[str, ...]
    gold_evidence: tuple[str, ...]
    competing_documents: tuple[str, ...]
    evaluation_notes: str
    expected_chunks: tuple[str, ...] = ()


@dataclass(frozen=True)
class RetrievalFailure:
    question_id: str
    missing_expected_documents: tuple[str, ...]
    missing_expected_evidence_roles: tuple[str, ...]


class RetrievalFailureCategory(str, Enum):
    EVIDENCE_SOURCE_SUBSTITUTION = "evidence_source_substitution"
    RETRIEVAL_SOURCE_CONCENTRATION = "retrieval_source_concentration"


@dataclass(frozen=True)
class RetrievalFailureCategorization:
    question_id: str
    categories: tuple[RetrievalFailureCategory, ...]


@dataclass(frozen=True)
class RetrievalEvaluationSet:
    schema_version: str
    dataset_name: str
    description: str
    source_specification: str
    retrieval_depths: tuple[int, ...]
    questions: tuple[RetrievalEvaluationQuestion, ...]
