import json
from dataclasses import replace

import pytest

from rag_document_intelligence_eval.evaluation import (
    EXPECTED_EVIDENCE_ROLE_MAPPING,
    load_retrieval_evaluation_set,
    document_recall_at_k,
    document_hit_at_k,
    document_reciprocal_rank,
    hit_rate_at_k,
    mean_document_recall_at_k,
    mean_reciprocal_rank,
    expected_document_retrieval_accuracy,
    expected_evidence_role_retrieval_accuracy,
    identify_retrieval_failures,
    categorize_retrieval_failures,
)

from rag_document_intelligence_eval.models import (
    DocumentChunk,
    DocumentMetadata,
    EvidenceRole,
    RetrievalEvaluationQuestion,
    RetrievalFailureCategory,
    RetrievalResult,
)


def make_question(
    question_id="BDPP-001",
    expected_documents=("05-output-verification.md",),
    expected_roles=("verification_requirements",),
):
    return RetrievalEvaluationQuestion(
        question_id=question_id,
        question_type="verification_failure",
        question="What happens when output verification fails?",
        expected_documents=expected_documents,
        expected_evidence_roles=expected_roles,
        gold_evidence=("FAILED_VERIFICATION",),
        competing_documents=("02-ingestion-validation.md",),
        evaluation_notes="Independent BDPP evaluation fixture.",
    )


def make_result(rank, document_id, filename, role, chunk_id):
    metadata = DocumentMetadata(
        document_id=document_id,
        filename=filename,
        title=document_id,
        evidence_role=role,
    )

    chunk = DocumentChunk(
        chunk_id=chunk_id,
        document_metadata=metadata,
        heading="Synthetic test heading",
        text="Independent BDPP test evidence.",
        chunk_index=0,
    )

    return RetrievalResult(
        rank=rank,
        score=1.0 - rank * 0.1,
        chunk=chunk,
    )


def sample_results():
    return (
        make_result(
            1, "ingestion_validation",
            "02-ingestion-validation.md",
            EvidenceRole.PROCESSING_REQUIREMENTS,
            "ingestion_validation::005",
        ),
        make_result(
            2, "output_verification",
            "05-output-verification.md",
            EvidenceRole.VERIFICATION_REQUIREMENTS,
            "output_verification::000",
        ),
        make_result(
            3, "diagnostics",
            "06-diagnostics.md",
            EvidenceRole.DIAGNOSTIC_REQUIREMENTS,
            "diagnostics::002",
        ),
    )


def test_bdpp_evidence_role_mapping():
    assert len(EXPECTED_EVIDENCE_ROLE_MAPPING) == 4

    for role in EvidenceRole:
        assert EXPECTED_EVIDENCE_ROLE_MAPPING[role.value] is role


def test_document_metrics_respect_rank_and_depth():
    question = make_question()
    results = sample_results()

    assert document_hit_at_k(question, results, 1) is False
    assert document_hit_at_k(question, results, 3) is True
    assert document_recall_at_k(question, results, 1) == 0.0
    assert document_recall_at_k(question, results, 3) == 1.0
    assert document_reciprocal_rank(question, results) == 0.5


def test_aggregate_document_metrics():
    first = make_question("BDPP-001")
    second = make_question(
        "BDPP-002",
        expected_documents=("06-diagnostics.md",),
        expected_roles=("diagnostic_requirements",),
    )

    results_by_id = {
        "BDPP-001": sample_results(),
        "BDPP-002": sample_results()[:1],
    }

    questions = (first, second)

    assert hit_rate_at_k(questions, results_by_id, 3) == 0.5
    assert mean_document_recall_at_k(
        questions, results_by_id, 3
    ) == 0.5
    assert mean_reciprocal_rank(
        questions, results_by_id
    ) == 0.25


def test_document_and_role_success_can_miss_gold_chunks():
    question = make_question()
    results = sample_results()
    results_by_id = {question.question_id: results}

    assert expected_document_retrieval_accuracy(
        (question,), results_by_id
    ) == 1.0

    assert expected_evidence_role_retrieval_accuracy(
        (question,), results_by_id
    ) == 1.0

    authoritative_chunks = {
        "output_verification::006",
        "output_verification::007",
    }

    retrieved_chunks = {
        result.chunk.chunk_id
        for result in results
    }

    assert authoritative_chunks.isdisjoint(retrieved_chunks)


def test_failure_identification_reports_missing_document_and_role():
    question = make_question()
    results = sample_results()[:1]

    failures = identify_retrieval_failures(
        (question,),
        {question.question_id: results},
    )

    assert len(failures) == 1
    assert failures[0].question_id == "BDPP-001"
    assert failures[0].missing_expected_documents == (
        "05-output-verification.md",
    )
    assert failures[0].missing_expected_evidence_roles == (
        "verification_requirements",
    )


def test_failure_categorization_detects_substitution_and_concentration():
    question = make_question()
    first = sample_results()[0]

    second = make_result(
        2, "ingestion_validation",
        "02-ingestion-validation.md",
        EvidenceRole.PROCESSING_REQUIREMENTS,
        "ingestion_validation::006",
    )

    categories = categorize_retrieval_failures(
        (question,),
        {question.question_id: (first, second)},
    )

    assert len(categories) == 1

    assert set(categories[0].categories) == {
        RetrievalFailureCategory.EVIDENCE_SOURCE_SUBSTITUTION,
        RetrievalFailureCategory.RETRIEVAL_SOURCE_CONCENTRATION,
    }


def test_document_metrics_reject_nonpositive_k():
    question = make_question()
    results = sample_results()

    with pytest.raises(ValueError):
        document_recall_at_k(question, results, 0)

    with pytest.raises(ValueError):
        document_hit_at_k(question, results, 0)


def test_bdpp_evaluation_set_loader(tmp_path):
    path = tmp_path / "bdpp_questions.json"

    data = {
        "schema_version": "1.0",
        "dataset_name": "independent_bdpp_test",
        "description": "Independent test fixture.",
        "source_specification": "data/corpus",
        "retrieval_depths": [1, 3],
        "questions": [
            {
                "question_id": "BDPP-001",
                "question_type": "verification_failure",
                "question": "What happens when verification fails?",
                "expected_documents": [
                    "05-output-verification.md"
                ],
                "expected_evidence_roles": [
                    "verification_requirements"
                ],
                "gold_evidence": ["FAILED_VERIFICATION"],
                "competing_documents": [
                    "02-ingestion-validation.md"
                ],
                "evaluation_notes": "Synthetic test question.",
            }
        ],
    }

    path.write_text(json.dumps(data), encoding="utf-8")

    evaluation_set = load_retrieval_evaluation_set(path)

    assert evaluation_set.dataset_name == "independent_bdpp_test"
    assert evaluation_set.retrieval_depths == (1, 3)
    assert len(evaluation_set.questions) == 1

    question = evaluation_set.questions[0]

    assert question.question_id == "BDPP-001"
    assert question.expected_evidence_roles == (
        "verification_requirements",
    )


def test_expected_chunks_default_preserves_compatibility():
    question = make_question()

    assert question.expected_chunks == ()


def test_evaluation_loader_preserves_expected_chunk_ids(tmp_path):
    path = tmp_path / "bdpp_chunk_questions.json"

    data = {
        "schema_version": "1.1",
        "dataset_name": "bdpp_chunk_evaluation",
        "description": "Independent chunk-level evaluation fixture.",
        "source_specification": "data/corpus",
        "retrieval_depths": [1, 3],
        "questions": [
            {
                "question_id": "BDPP-CHUNK-001",
                "question_type": "verification_failure",
                "question": "What happens when verification fails?",
                "expected_documents": [
                    "05-output-verification.md"
                ],
                "expected_evidence_roles": [
                    "verification_requirements"
                ],
                "expected_chunks": [
                    "output_verification::006",
                    "output_verification::007"
                ],
                "gold_evidence": [
                    "FAILED_VERIFICATION",
                    "Stored records remain unchanged"
                ],
                "competing_documents": [
                    "02-ingestion-validation.md"
                ],
                "evaluation_notes": "Authoritative BDPP evidence.",
            }
        ],
    }

    path.write_text(json.dumps(data), encoding="utf-8")

    evaluation_set = load_retrieval_evaluation_set(path)
    question = evaluation_set.questions[0]

    assert question.expected_chunks == (
        "output_verification::006",
        "output_verification::007",
    )


from rag_document_intelligence_eval.evaluation import (
    chunk_recall_at_k,
    chunk_hit_at_k,
    expected_chunk_retrieval_accuracy,
)


def make_chunk_question(question_id="BDPP-CHUNK-001"):
    return replace(
        make_question(question_id),
        expected_chunks=(
            "output_verification::006",
            "output_verification::007",
        ),
    )


def authoritative_chunk_results():
    return (
        make_result(
            1,
            "output_verification",
            "05-output-verification.md",
            EvidenceRole.VERIFICATION_REQUIREMENTS,
            "output_verification::006",
        ),
        make_result(
            2,
            "output_verification",
            "05-output-verification.md",
            EvidenceRole.VERIFICATION_REQUIREMENTS,
            "output_verification::007",
        ),
    )


def test_chunk_metrics_detect_missing_authoritative_evidence():
    question = make_chunk_question()
    results = sample_results()

    assert document_recall_at_k(question, results, 3) == 1.0
    assert chunk_recall_at_k(question, results, 3) == 0.0
    assert chunk_hit_at_k(question, results, 3) is False


def test_chunk_metrics_support_partial_and_complete_coverage():
    question = make_chunk_question()
    results = authoritative_chunk_results()

    assert chunk_recall_at_k(question, results, 1) == 0.5
    assert chunk_recall_at_k(question, results, 2) == 1.0

    assert chunk_hit_at_k(question, results, 1) is True
    assert chunk_hit_at_k(question, results, 2) is True


def test_duplicate_retrieved_chunks_do_not_increase_recall():
    question = make_chunk_question()
    first = authoritative_chunk_results()[0]

    duplicate = make_result(
        2,
        "output_verification",
        "05-output-verification.md",
        EvidenceRole.VERIFICATION_REQUIREMENTS,
        "output_verification::006",
    )

    assert chunk_recall_at_k(
        question,
        (first, duplicate),
        2,
    ) == 0.5


def test_chunk_metrics_validate_expected_chunks_and_depth():
    question = make_chunk_question()
    results = sample_results()

    with pytest.raises(ValueError):
        chunk_recall_at_k(question, results, 0)

    with pytest.raises(ValueError):
        chunk_hit_at_k(question, results, 0)

    question_without_chunks = make_question()

    with pytest.raises(ValueError):
        chunk_recall_at_k(question_without_chunks, results, 3)

    with pytest.raises(ValueError):
        chunk_hit_at_k(question_without_chunks, results, 3)


def test_expected_chunk_accuracy_calculates_complete_coverage():
    first = make_chunk_question("BDPP-CHUNK-001")
    second = make_chunk_question("BDPP-CHUNK-002")

    results_by_id = {
        first.question_id: authoritative_chunk_results(),
        second.question_id: sample_results(),
    }

    assert expected_chunk_retrieval_accuracy(
        (first, second),
        results_by_id,
    ) == 0.5


def test_expected_chunk_accuracy_rejects_missing_results():
    question = make_chunk_question()

    with pytest.raises(ValueError):
        expected_chunk_retrieval_accuracy(
            (question,),
            {},
        )


def test_expected_chunk_accuracy_rejects_empty_questions():
    with pytest.raises(ValueError):
        expected_chunk_retrieval_accuracy(
            (),
            {},
        )
