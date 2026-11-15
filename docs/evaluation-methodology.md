# Evaluation Methodology

## 1. Purpose and Scope

This document describes the retrieval-evaluation methodology used in the independent public edition of **RAG Document Intelligence Evaluation**.

The project evaluates whether a retrieval system identifies designated source documents, evidence roles, and specific evidence chunks in a fictional Batch Data Processing Platform (BDPP) documentation corpus.

The evaluation is intended to support reproducible examination of retrieval behavior, error analysis, and methodological limitations.

It is a development-stage retrieval evaluation, not an independent production benchmark.

The project does not evaluate a complete retrieval-augmented generation system's answer generation or end-to-end answer correctness. Its automated retrieval metrics should not be interpreted as direct measurements of factual answer sufficiency, source authority, or production readiness.

## 2. Independent Synthetic Corpus

The public-edition corpus consists of six independently developed fictional Markdown documents describing a hypothetical batch data processing platform:

1. `01-platform-overview.md`
2. `02-ingestion-validation.md`
3. `03-transformation.md`
4. `04-dataset-versioning.md`
5. `05-output-verification.md`
6. `06-diagnostics.md`

The documents describe related but distinct platform responsibilities, including ingestion and validation, transformations, dataset-version creation, output verification, and diagnostic reporting.

The corpus is synthetic. Its platform specifications are educational experimental materials, not representations of an actual deployed production system.

The six documents produce **47 unique deterministic chunks** under the implemented corpus-loading and chunking configuration.

Each chunk is associated with a source document and a stable chunk identifier. The evaluation uses those identifiers to assess designated chunk retrieval.

### Evidence-role taxonomy

Source documents are assigned one of four evidence roles:

| Evidence role | Meaning |
|---|---|
| `platform_context` | General platform architecture and contextual information |
| `processing_requirements` | Requirements governing ingestion, transformation, and dataset versioning |
| `verification_requirements` | Requirements for verifying outputs and their consistency |
| `diagnostic_requirements` | Requirements for reporting diagnostic and processing outcomes |

Evidence roles provide a structured classification of retrieved documentation.

They are not independently validated measures of source authority or substantive answer sufficiency.

## 3. Retrieval Configuration

The evaluation uses the following retrieval components:

- **Embedding model:** `BAAI/bge-small-en-v1.5`
- **Retrieval method:** cosine similarity between question and document-chunk embeddings
- **Retrieval unit:** individual document chunk
- **Ranking:** descending retrieval similarity
- **Evaluated retrieval depths:** k = 1 and k = 3, as applicable to the metric
- **Corpus:** 47 chunks from the six-document synthetic BDPP specification

The retrieval implementation produces ranked chunk results containing source metadata and similarity scores.

Document-level metrics use the filename associated with each retrieved chunk. Evidence-role metrics use the source document's assigned evidence role. Chunk-level metrics use the retrieved chunk identifier.

The experimental comparison described in this documentation does not involve an isolated change to the embedding model, cosine-similarity ranking method, or underlying retrieval algorithm.

## 4. Evaluation Dataset Design

The project maintains two development-stage retrieval-evaluation datasets:

**V1 — Original development dataset**

`data/evaluation/bdpp_retrieval_questions.json`

**V2 — Revised development dataset**

`data/evaluation/bdpp_retrieval_questions_v2.json`

Both datasets use schema version `1.1` and contain 12 evaluation questions.

### Question annotations

Each question contains the following fields:

| Field | Purpose |
|---|---|
| `question_id` | Stable question identifier |
| `question_type` | Question classification |
| `question` | Query submitted to retrieval |
| `expected_documents` | Designated expected source filenames |
| `expected_evidence_roles` | Designated expected evidence-role labels |
| `expected_chunks` | Designated expected chunk identifiers |
| `gold_evidence` | Human-readable reference describing intended factual evidence |
| `competing_documents` | Other documents relevant to potential retrieval confusion |
| `evaluation_notes` | Supporting evaluation or adjudication notes |

### Annotation semantics

The evaluator uses `expected_documents` to calculate document-retrieval metrics and `expected_chunks` to calculate chunk-retrieval metrics.

For evidence-role coverage, the evaluator maps the labels in `expected_evidence_roles` to the implementation's evidence-role enumeration.

The `gold_evidence` field is retained as human-readable reference metadata. Although loaded into the evaluation-question object, its text is **not directly compared with retrieved passage text by the nine automated retrieval metrics**.

Consequently, achieving a high chunk-retrieval score does not necessarily demonstrate that the retrieved content provides a substantively sufficient answer.

Similarly, retrieval of an evidence-role label does not necessarily establish retrieval of the designated authoritative document or chunk.

### Development dataset limitations

The evaluation questions and annotations were developed using knowledge of the synthetic corpus.

The datasets are therefore development and diagnostic instruments rather than blinded, independently constructed benchmark sets.

The small number of questions limits the generalizability of aggregate results.

## 5. Quantitative Retrieval Metrics

The evaluation reports nine automated retrieval metrics.

All aggregate metrics are calculated across the evaluation questions, with each question contributing equally.

### 5.1 Document Hit@1

The fraction of questions for which at least one designated expected document appears among the first retrieved chunk.

A hit requires a retrieved chunk's source filename to match one of the question's `expected_documents`.

### 5.2 Document Hit@3

The fraction of questions for which at least one designated expected document appears among the first three retrieved chunks.

This is an any-match measure. It does not require all designated documents to be retrieved.

### 5.3 Mean Document Recall@3

For each question, document recall is calculated as:

`Number of distinct expected documents retrieved in the top 3 / Number of distinct expected documents`

The aggregate metric is the mean of these per-question recall values.

Repeated chunks from the same document do not increase distinct-document coverage.

### 5.4 Mean Reciprocal Rank (MRR)

For each question, reciprocal rank is calculated from the earliest-ranked retrieved chunk belonging to any designated expected document:

`Reciprocal Rank = 1 / Rank of first expected-document match`

If no expected document appears among the supplied retrieval results, reciprocal rank is zero.

MRR is the mean of these values across questions.

The implementation's `document_reciprocal_rank()` helper does not independently impose a fixed k limit. Its effective search depth depends on the ranked results supplied to it.

### 5.5 Complete Document Accuracy@3

The fraction of questions for which **all distinct designated expected documents** appear among the first three retrieved chunks.

A question contributes one successful outcome only when its document recall at k = 3 equals 1.0.

This is stricter than Document Hit@3.

### 5.6 Evidence Role Accuracy@3

The fraction of questions for which every designated expected evidence role is represented among the first three retrieved chunks.

For each question, the implementation computes sets of expected and retrieved roles and checks:

`Expected Roles ⊆ Retrieved Roles@3`

A question succeeds when the expected-role set is a subset of the retrieved-role set.

Additional retrieved roles do not cause failure.

The metric does not require exact matching of expected documents or chunks. A retrieved document with a matching role can satisfy the role condition even when the designated authoritative source is absent.

Therefore, this metric measures **complete designated evidence-role coverage**, not independent source-authority correctness.

### 5.7 Chunk Hit Rate@3

The fraction of questions for which at least one designated chunk identifier appears among the first three retrieved chunks.

The evaluator compares retrieved chunk IDs against `expected_chunks`.

This is an any-match measure.

### 5.8 Mean Chunk Recall@3

For each question, chunk recall is:

`Number of distinct expected chunks retrieved in the top 3 / Number of distinct expected chunks`

The aggregate metric is the mean of these per-question recall values.

A question with two expected chunks and only one matching retrieved chunk has chunk recall 0.5.

### 5.9 Complete Chunk Accuracy@3

The fraction of questions for which all distinct designated expected chunks appear among the first three retrieved chunks.

A question succeeds only when its chunk recall at k = 3 equals 1.0.

This measure is stricter than Chunk Hit Rate@3.

### Metric interpretation

Document, evidence-role, and chunk metrics evaluate different structural aspects of retrieval.

None of the nine automated metrics directly determines whether retrieved passages collectively provide a complete factual answer or whether the retrieved evidence is the most authoritative source for the question.

## 6. Three Evaluation Dimensions

The project distinguishes three evaluation dimensions.

### Dimension A — Exact designated authoritative-source retrieval

This dimension asks whether the retrieval system returns the specifically designated documents and chunks.

It is measured through automated document and chunk metrics using the expected-source annotations.

A failure in exact designated-source retrieval can occur even if the retrieved material contains some relevant information.

### Dimension B — Substantive answer sufficiency

This dimension asks whether the retrieved evidence contains enough factual information to answer the question as posed.

It requires examination of the actual source text and question requirements.

A retrieved passage may provide a sufficient answer even when it does not match the designated gold chunk.

Conversely, partial gold-source coverage may be insufficient when a question requires information from multiple components.

This dimension is not independently established by the automated metrics.

### Dimension C — Source authority

This dimension considers whether evidence comes from the component or document that governs the requirement being asked about.

A general platform overview may summarize a rule accurately while a more specialized component document provides the governing specification.

Retrieving relevant information from a summary source does not necessarily establish retrieval of the designated authoritative source.

Evidence-role classification provides useful structural information, but it cannot independently resolve source-authority judgments.

### Relationship among dimensions

These three dimensions must remain distinguishable in analysis and reporting.

An exact-source retrieval failure does not automatically prove substantive answer insufficiency.

A substantively useful alternative passage does not automatically satisfy designated-source retrieval.

Likewise, matching an evidence role does not establish that the correct governing document or chunk was retrieved.

## 7. Failure Analysis and Adjudication

Failure analysis examines question-level retrieval results, including ranked chunks, source documents, expected annotations, and relevant underlying text.

Adjudication distinguishes automated metric failures from evidence-sufficiency and authority assessments.

The preserved development evaluations include the following important cases.

### BDPP-002 — Revised authoritative-source annotations

The question asks when rejected records are excluded and under what condition a dataset-version candidate is created.

The revised V2 annotations designate:

- `ingestion_validation::006`
- `dataset_versioning::001`

These represent the governing requirements for rejection exclusion and version creation.

The question wording and retrieval rankings did not change between V1 and V2. The gold annotations changed to identify the more specific governing sources.

V2 retrieved one of the two designated chunks. The missing designated chunk was `ingestion_validation::006`.

The change in evaluation outcomes should therefore not be attributed to improved retrieval behavior.

### BDPP-007 — Revised cross-component question

V2 changes the question wording to explicitly request Schema Validation's definition of a partially accepted batch and Dataset Versioning's requirements for creating a version and determining included records.

The designated chunks remain:

- `ingestion_validation::006`
- `dataset_versioning::001`

The revised wording changes the retrieval rankings. Both designated documents appear within the evaluated retrieval set, but exact designated chunk coverage remains one of two.

The missing designated chunk is `ingestion_validation::006`.

This case demonstrates that document-level coverage and chunk-level coverage can differ, particularly for questions requiring evidence from multiple components.

### BDPP-003 and BDPP-012 — Alternative evidence

Earlier adjudication identified alternative retrieved Diagnostics evidence as substantively sufficient for these questions.

Those judgments should be preserved separately from exact designated-source scoring.

### BDPP-011 — Persistent retrieval failure

This question retains a genuine retrieval failure in the adjudicated development evaluation.

It must not be represented as resolved merely because other questions' annotations or wording were revised.

### Adjudication reporting

Question-level findings should distinguish:

- Designated source coverage.
- Substantive adequacy of retrieved evidence.
- Governing-source authority.

Adjudications are interpretive findings, not additional automatically calculated measures of answer quality.

## 8. Experimental Preservation and Comparison

The development evaluation preserves both its original baseline and revised experimental record.

### V1 baseline artifact

`data/evaluation/results/bdpp_development_baseline_2026-11-12.json`

The V1 baseline was reconstructed from previously verified original real-model console output.

It was not produced by rerunning inference during the preservation process.

### V2 experimental artifact

`data/evaluation/results/bdpp_development_v2_2026-11-12.json`

The V2 artifact records a direct real-model retrieval-evaluation execution using the revised evaluation dataset.

### Preservation rules

Both evaluation datasets and both saved result artifacts are retained.

The original V1 annotations and baseline results must not be silently replaced by V2 materials.

The comparison between V1 and V2 includes changes to question annotations and question wording, not an isolated modification to the retrieval model or ranking algorithm.

Specifically:

- BDPP-002 changes designated annotations while retaining identical question wording and retrieval rankings.
- BDPP-007 changes question wording and supporting gold-evidence text; its retrieval rankings also change.
- The remaining ten question records are unchanged.

Therefore, numerical differences between V1 and V2 must be interpreted as outcomes of a revised development evaluation design.

They must not be presented as proof that the embedding model or underlying retrieval algorithm improved.

The numerical metrics, comparative analysis, question-level outcomes, and associated caveats are documented separately in `docs/evaluation-results.md`.

## 9. Limitations

The following limitations apply to the reported evaluation.

**Synthetic corpus.** The six documents describe a fictional platform and do not reproduce real operational data or production requirements.

**Small evaluation set.** Twelve questions provide limited evidence about retrieval behavior beyond the evaluated corpus and query set.

**Development-stage design.** The evaluation questions and gold annotations were developed with knowledge of the corpus. Results are not equivalent to an independently blinded benchmark.

**Designated-source dependence.** Exact document and chunk metrics depend on the quality and interpretation of designated annotations.

**Alternative evidence.** Retrieved evidence can sometimes be substantively useful without matching the designated gold source.

**Evidence-role granularity.** Multiple documents may share the same evidence role. Role coverage is consequently less specific than exact document or chunk retrieval.

**No generated-answer evaluation.** The metrics do not assess the accuracy, completeness, or faithfulness of generated answers.

**No automatic authority adjudication.** The metrics do not independently determine which source governs a disputed or overlapping specification.

**Limited comparison interpretation.** V1/V2 differences combine annotation changes and revised question wording. They do not isolate a retrieval-system improvement.

**No production-readiness inference.** The results do not establish system reliability, scalability, security, or suitability for production deployment.

The limitations should accompany numerical results in portfolio materials and external descriptions.

## 10. Related Documentation

The intended public-edition documentation consists of:

- **`docs/evaluation-methodology.md`** — Evaluation design, metric definitions, evidence dimensions, and methodological limitations.
- **`docs/evaluation-results.md`** — Preserved V1/V2 results, quantitative comparisons, failure analysis, and interpretation.
- **`docs/provenance.md`** — Project origin, independent synthetic-material provenance, engineering-component reuse, and development history.
- **`README.md`** — Project overview, navigation, technical scope, experimental summary, and limitations.

The provenance documentation is responsible for accurately identifying engineering-component reuse from the original private project and disclosing substantial ChatGPT assistance.

The public edition must not be represented as a wholly unaided implementation or as production experience.

The original private v1.0.0 repository remains unchanged, and its historical Git commits are not imported into the independent public-edition repository.

Final intellectual-property, licensing, security, provenance, and publication-readiness reviews remain necessary before any public release.
