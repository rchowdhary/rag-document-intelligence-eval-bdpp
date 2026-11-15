import json
from pathlib import Path
from collections.abc import Mapping, Sequence

from rag_document_intelligence_eval.models import (
    EvidenceRole,
    RetrievalEvaluationQuestion,
    RetrievalEvaluationSet,
    RetrievalFailure,
    RetrievalFailureCategorization,
    RetrievalFailureCategory,
    RetrievalResult,
)

EXPECTED_EVIDENCE_ROLE_MAPPING = {
    "platform_context": EvidenceRole.PLATFORM_CONTEXT,
    "processing_requirements": EvidenceRole.PROCESSING_REQUIREMENTS,
    "verification_requirements": EvidenceRole.VERIFICATION_REQUIREMENTS,
    "diagnostic_requirements": EvidenceRole.DIAGNOSTIC_REQUIREMENTS,
}


def load_retrieval_evaluation_set(
    path: Path,
) -> RetrievalEvaluationSet:
    """Load a retrieval evaluation set from a UTF-8 JSON file."""
    data = json.loads(path.read_text(encoding="utf-8"))

    questions = tuple(
        RetrievalEvaluationQuestion(
            question_id=question["question_id"],
            question_type=question["question_type"],
            question=question["question"],
            expected_documents=tuple(
                question["expected_documents"]
            ),
            expected_evidence_roles=tuple(
                question["expected_evidence_roles"]
            ),
            gold_evidence=tuple(question["gold_evidence"]),
            competing_documents=tuple(
                question["competing_documents"]
            ),
            evaluation_notes=question["evaluation_notes"],
            expected_chunks=tuple(question.get("expected_chunks", ())),
        )
        for question in data["questions"]
    )

    return RetrievalEvaluationSet(
        schema_version=data["schema_version"],
        dataset_name=data["dataset_name"],
        description=data["description"],
        source_specification=data["source_specification"],
        retrieval_depths=tuple(data["retrieval_depths"]),
        questions=questions,
    )


def chunk_recall_at_k(
    question: RetrievalEvaluationQuestion,
    results: Sequence[RetrievalResult],
    k: int,
) -> float:
    """Calculate expected-chunk recall within the first k results."""
    if k <= 0:
        raise ValueError("k must be greater than zero")

    if not question.expected_chunks:
        raise ValueError(
            "question must define at least one expected chunk"
        )

    expected_chunks = set(question.expected_chunks)

    retrieved_chunks = {
        result.chunk.chunk_id
        for result in results[:k]
    }

    matched_chunks = expected_chunks & retrieved_chunks

    return len(matched_chunks) / len(expected_chunks)


def chunk_hit_at_k(
    question: RetrievalEvaluationQuestion,
    results: Sequence[RetrievalResult],
    k: int,
) -> bool:
    """Return whether an expected chunk appears in the first k results."""
    if k <= 0:
        raise ValueError("k must be greater than zero")

    if not question.expected_chunks:
        raise ValueError(
            "question must define at least one expected chunk"
        )

    expected_chunks = set(question.expected_chunks)

    return any(
        result.chunk.chunk_id in expected_chunks
        for result in results[:k]
    )


def expected_chunk_retrieval_accuracy(
    questions: Sequence[RetrievalEvaluationQuestion],
    results_by_question_id: Mapping[
        str,
        Sequence[RetrievalResult],
    ],
) -> float:
    """Calculate complete expected-chunk retrieval accuracy at k=3."""
    if not questions:
        raise ValueError(
            "questions must contain at least one evaluation question"
        )

    missing_question_ids = [
        question.question_id
        for question in questions
        if question.question_id not in results_by_question_id
    ]

    if missing_question_ids:
        raise ValueError(
            "retrieval results are missing for evaluation questions: "
            + ", ".join(missing_question_ids)
        )

    complete_coverage_count = sum(
        chunk_recall_at_k(
            question,
            results_by_question_id[question.question_id],
            k=3,
        ) == 1.0
        for question in questions
    )

    return complete_coverage_count / len(questions)


def document_recall_at_k(
    question: RetrievalEvaluationQuestion,
    results: Sequence[RetrievalResult],
    k: int,
) -> float:
    """Calculate expected-document recall within the first k results."""
    if k <= 0:
        raise ValueError("k must be greater than zero")

    if not question.expected_documents:
        raise ValueError(
            "question must define at least one expected document"
        )

    expected_documents = set(question.expected_documents)

    retrieved_documents = {
        result.chunk.document_metadata.filename
        for result in results[:k]
    }

    matched_documents = (
        expected_documents & retrieved_documents
    )

    return len(matched_documents) / len(expected_documents)


def document_hit_at_k(
    question: RetrievalEvaluationQuestion,
    results: Sequence[RetrievalResult],
    k: int,
) -> bool:
    """Return whether an expected document appears within the first k results."""
    if k <= 0:
        raise ValueError("k must be greater than zero")

    if not question.expected_documents:
        raise ValueError(
            "question must define at least one expected document"
        )

    expected_documents = set(question.expected_documents)

    return any(
        result.chunk.document_metadata.filename
        in expected_documents
        for result in results[:k]
    )


def document_reciprocal_rank(
    question: RetrievalEvaluationQuestion,
    results: Sequence[RetrievalResult],
) -> float:
    """Calculate reciprocal rank for the first expected document."""
    if not question.expected_documents:
        raise ValueError(
            "question must define at least one expected document"
        )

    expected_documents = set(question.expected_documents)

    matching_ranks = [
        result.rank
        for result in results
        if result.chunk.document_metadata.filename
        in expected_documents
    ]

    if not matching_ranks:
        return 0.0

    return 1.0 / min(matching_ranks)


def hit_rate_at_k(
    questions: Sequence[RetrievalEvaluationQuestion],
    results_by_question_id: Mapping[
        str,
        Sequence[RetrievalResult],
    ],
    k: int,
) -> float:
    """Calculate document hit rate across evaluation questions."""
    if k <= 0:
        raise ValueError("k must be greater than zero")

    if not questions:
        raise ValueError(
            "questions must contain at least one evaluation question"
        )

    missing_question_ids = [
        question.question_id
        for question in questions
        if question.question_id not in results_by_question_id
    ]

    if missing_question_ids:
        raise ValueError(
            "retrieval results are missing for evaluation questions: "
            + ", ".join(missing_question_ids)
        )

    hit_count = sum(
        document_hit_at_k(
            question,
            results_by_question_id[question.question_id],
            k,
        )
        for question in questions
    )

    return hit_count / len(questions)


def mean_document_recall_at_k(
    questions: Sequence[RetrievalEvaluationQuestion],
    results_by_question_id: Mapping[
        str,
        Sequence[RetrievalResult],
    ],
    k: int,
) -> float:
    """Calculate mean expected-document recall across evaluation questions."""
    if k <= 0:
        raise ValueError("k must be greater than zero")

    if not questions:
        raise ValueError(
            "questions must contain at least one evaluation question"
        )

    missing_question_ids = [
        question.question_id
        for question in questions
        if question.question_id not in results_by_question_id
    ]

    if missing_question_ids:
        raise ValueError(
            "retrieval results are missing for evaluation questions: "
            + ", ".join(missing_question_ids)
        )

    total_recall = sum(
        document_recall_at_k(
            question,
            results_by_question_id[question.question_id],
            k,
        )
        for question in questions
    )

    return total_recall / len(questions)


def mean_reciprocal_rank(
    questions: Sequence[RetrievalEvaluationQuestion],
    results_by_question_id: Mapping[
        str,
        Sequence[RetrievalResult],
    ],
) -> float:
    """Calculate mean reciprocal rank across evaluation questions."""
    if not questions:
        raise ValueError(
            "questions must contain at least one evaluation question"
        )

    missing_question_ids = [
        question.question_id
        for question in questions
        if question.question_id not in results_by_question_id
    ]

    if missing_question_ids:
        raise ValueError(
            "retrieval results are missing for evaluation questions: "
            + ", ".join(missing_question_ids)
        )

    total_reciprocal_rank = sum(
        document_reciprocal_rank(
            question,
            results_by_question_id[question.question_id],
        )
        for question in questions
    )

    return total_reciprocal_rank / len(questions)


def expected_document_retrieval_accuracy(
    questions: Sequence[RetrievalEvaluationQuestion],
    results_by_question_id: Mapping[
        str,
        Sequence[RetrievalResult],
    ],
) -> float:
    """Calculate complete expected-document retrieval accuracy at k=3."""
    if not questions:
        raise ValueError(
            "questions must contain at least one evaluation question"
        )

    missing_question_ids = [
        question.question_id
        for question in questions
        if question.question_id not in results_by_question_id
    ]

    if missing_question_ids:
        raise ValueError(
            "retrieval results are missing for evaluation questions: "
            + ", ".join(missing_question_ids)
        )

    complete_coverage_count = sum(
        document_recall_at_k(
            question,
            results_by_question_id[question.question_id],
            k=3,
        )
        == 1.0
        for question in questions
    )

    return complete_coverage_count / len(questions)


def expected_evidence_role_retrieval_accuracy(
    questions: Sequence[RetrievalEvaluationQuestion],
    results_by_question_id: Mapping[
        str,
        Sequence[RetrievalResult],
    ],
) -> float:
    """Calculate complete expected-evidence-role accuracy at k=3."""
    if not questions:
        raise ValueError(
            "questions must contain at least one evaluation question"
        )

    missing_question_ids = [
        question.question_id
        for question in questions
        if question.question_id not in results_by_question_id
    ]

    if missing_question_ids:
        raise ValueError(
            "retrieval results are missing for evaluation questions: "
            + ", ".join(missing_question_ids)
        )

    complete_coverage_count = 0

    for question in questions:
        expected_roles = {
            EXPECTED_EVIDENCE_ROLE_MAPPING[role]
            for role in question.expected_evidence_roles
        }

        retrieved_roles = {
            result.chunk.document_metadata.evidence_role
            for result in results_by_question_id[
                question.question_id
            ][:3]
        }

        if expected_roles.issubset(retrieved_roles):
            complete_coverage_count += 1

    return complete_coverage_count / len(questions)


def identify_retrieval_failures(
    questions: Sequence[RetrievalEvaluationQuestion],
    results_by_question_id: Mapping[
        str,
        Sequence[RetrievalResult],
    ],
) -> tuple[RetrievalFailure, ...]:
    """Identify incomplete document or evidence-role retrieval at k=3."""
    if not questions:
        raise ValueError(
            "questions must contain at least one evaluation question"
        )

    missing_question_ids = [
        question.question_id
        for question in questions
        if question.question_id not in results_by_question_id
    ]

    if missing_question_ids:
        raise ValueError(
            "retrieval results are missing for evaluation questions: "
            + ", ".join(missing_question_ids)
        )

    failures = []

    for question in questions:
        results = results_by_question_id[question.question_id][:3]

        retrieved_documents = {
            result.chunk.document_metadata.filename
            for result in results
        }

        retrieved_roles = {
            result.chunk.document_metadata.evidence_role
            for result in results
        }

        missing_expected_documents = tuple(
            document
            for document in question.expected_documents
            if document not in retrieved_documents
        )

        missing_expected_evidence_roles = tuple(
            role
            for role in question.expected_evidence_roles
            if EXPECTED_EVIDENCE_ROLE_MAPPING[role]
            not in retrieved_roles
        )

        if (
            missing_expected_documents
            or missing_expected_evidence_roles
        ):
            failures.append(
                RetrievalFailure(
                    question_id=question.question_id,
                    missing_expected_documents=(
                        missing_expected_documents
                    ),
                    missing_expected_evidence_roles=(
                        missing_expected_evidence_roles
                    ),
                )
            )

    return tuple(failures)


def categorize_retrieval_failures(
    questions: Sequence[RetrievalEvaluationQuestion],
    results_by_question_id: Mapping[
        str,
        Sequence[RetrievalResult],
    ],
) -> tuple[RetrievalFailureCategorization, ...]:
    """Categorize retrieval failures using observed top-3 patterns."""
    failures = identify_retrieval_failures(
        questions=questions,
        results_by_question_id=results_by_question_id,
    )

    questions_by_id = {
        question.question_id: question
        for question in questions
    }

    categorizations = []

    for failure in failures:
        question = questions_by_id[failure.question_id]
        results = results_by_question_id[
            failure.question_id
        ][:3]

        retrieved_documents = [
            result.chunk.document_metadata.filename
            for result in results
        ]

        categories = []

        if any(
            document in question.competing_documents
            for document in retrieved_documents
        ):
            categories.append(
                RetrievalFailureCategory.EVIDENCE_SOURCE_SUBSTITUTION
            )

        if len(retrieved_documents) != len(
            set(retrieved_documents)
        ):
            categories.append(
                RetrievalFailureCategory.RETRIEVAL_SOURCE_CONCENTRATION
            )

        categorizations.append(
            RetrievalFailureCategorization(
                question_id=failure.question_id,
                categories=tuple(categories),
            )
        )

    return tuple(categorizations)
