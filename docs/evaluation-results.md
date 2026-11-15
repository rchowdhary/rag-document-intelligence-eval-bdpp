# Evaluation Results

## 1. Purpose and Scope

This document presents the preserved V1 and V2 development-stage retrieval-evaluation results for the independent public edition of **RAG Document Intelligence Evaluation**.

The evaluations use an independently developed fictional Batch Data Processing Platform (BDPP) documentation corpus.

The purpose of this comparison is to examine designated-source retrieval performance, identify retrieval failures, and document how revised evaluation annotations and question wording affect the reported results.

**The V1/V2 comparison is not an isolated experiment demonstrating an improvement to the retrieval model or algorithm.**

Metric definitions and evaluation-design limitations are described in `docs/evaluation-methodology.md`.

## 2. Experimental Configuration

Both evaluations used the following recorded configuration:

| Property | Value |
|---|---|
| Embedding model identifier | `BAAI/bge-small-en-v1.5` |
| Execution device | CPU |
| Retrieval method | Cosine similarity |
| Retrieval depth | Top 3 chunks |
| Synthetic corpus | 6 Markdown documents |
| Corpus size | 47 deterministic chunks |
| Evaluation questions | 12 per dataset |
| Evaluation schema version | 1.1 |
| Evaluation date | November 12, 2026 |

The model identifier is recorded, but the experiment artifacts do not establish the exact downloaded model revision or embedding-library package versions.

The retrieval evaluations do not include generated-answer evaluation, response-quality scoring, or production deployment testing.

## 3. Preserved Experimental Artifacts

### 3.1 V1 — Original development baseline

**Artifact:**

`data/evaluation/results/bdpp_development_baseline_2026-11-12.json`

**Dataset:**

`data/evaluation/bdpp_retrieval_questions.json`

The original real-model retrieval evaluation was executed locally during Step 19C.10J.

Its archival JSON record was subsequently reconstructed from verified original console output without rerunning model inference.

The record preserves the original top-three retrieval rankings, chunk IDs, reported cosine similarities, source fingerprints, and evaluation metrics.

Cosine-similarity scores in this reconstructed record are preserved at the six-decimal precision printed during the original execution.

The artifact includes both reported four-decimal aggregate metrics and recomputed aggregate metrics.

It must not be described as a newly executed inference run.

### 3.2 V2 — Revised development evaluation

**Artifact:**

`data/evaluation/results/bdpp_development_v2_2026-11-12.json`

**Dataset:**

`data/evaluation/bdpp_retrieval_questions_v2.json`

V2 was executed directly with the revised evaluation dataset during Step 19C.10N.6.

Its saved artifact records the retrieval results, top-three rankings, document metadata, evidence roles, cosine-similarity values, aggregate metrics, and input fingerprints.

Both datasets contain 12 questions. Only BDPP-002 and BDPP-007 have revised question records.

The six synthetic corpus documents are preserved across the evaluations.

## 4. Aggregate Retrieval Results

The following table reports V1 and V2 retrieval metrics rounded to four decimal places.

The difference column is calculated from the underlying metric values rather than by subtracting the displayed rounded values.

| Metric | V1 | V2 | Difference |
|---|---:|---:|---:|
| Document Hit@1 | 0.6667 | 0.7500 | +0.0833 |
| Document Hit@3 | 0.7500 | 0.8333 | +0.0833 |
| Mean Document Recall@3 | 0.6667 | 0.7500 | +0.0833 |
| Mean Reciprocal Rank | 0.6944 | 0.7778 | +0.0833 |
| Complete Document Accuracy@3 | 0.5833 | 0.6667 | +0.0833 |
| Evidence Role Accuracy@3 | 0.6667 | 0.7500 | +0.0833 |
| Chunk Hit Rate@3 | 0.7500 | 0.8333 | +0.0833 |
| Mean Chunk Recall@3 | 0.6667 | 0.7083 | +0.0417 |
| Complete Chunk Accuracy@3 | 0.5833 | 0.5833 | 0.0000 |

### 4.1 Document-level results

V2 records designated-document hits at rank 1 for 9 of 12 questions, compared with 8 of 12 under V1.

At rank 3, at least one expected document is retrieved for 10 of 12 V2 questions, compared with 9 of 12 V1 questions.

Complete designated-document coverage at rank 3 occurs for 8 of 12 V2 questions, compared with 7 of 12 V1 questions.

These numerical differences include changes to gold-source annotations and query wording.

They must not be interpreted as evidence of an isolated retrieval-algorithm improvement.

### 4.2 Evidence-role results

Complete expected evidence-role coverage occurs for 9 of 12 V2 questions, compared with 8 of 12 V1 questions.

Evidence Role Accuracy@3 requires every expected role to appear among the first three retrieved chunks.

It does not require exact designated documents or chunks to be retrieved and does not independently establish source authority.

### 4.3 Chunk-level results

At least one designated chunk is retrieved for 10 of 12 V2 questions, compared with 9 of 12 V1 questions.

Mean Chunk Recall@3 changes from 0.6667 to 0.7083.

However, **Complete Chunk Accuracy@3 remains 0.5833 in both evaluations**, corresponding to 7 of 12 questions with complete designated-chunk coverage.

Thus, the recorded V2 evaluation does not show an increase in the number of questions for which every designated chunk was retrieved.

## 5. Question-Level Retrieval Outcomes

The following table summarizes exact designated-document and designated-chunk recall within the top three retrieved results.

Each value represents the fraction of that question's designated sources retrieved. A value of 1.0 indicates complete coverage.

| Question | V1 document | V2 document | V1 chunk | V2 chunk |
|---|---:|---:|---:|---:|
| BDPP-001 | 1.0 | 1.0 | 1.0 | 1.0 |
| BDPP-002 | 0.0 | 0.5 | 0.0 | 0.5 |
| BDPP-003 | 0.0 | 0.0 | 0.0 | 0.0 |
| BDPP-004 | 1.0 | 1.0 | 1.0 | 1.0 |
| BDPP-005 | 1.0 | 1.0 | 1.0 | 1.0 |
| BDPP-006 | 1.0 | 1.0 | 1.0 | 1.0 |
| BDPP-007 | 0.5 | 1.0 | 0.5 | 0.5 |
| BDPP-008 | 1.0 | 1.0 | 1.0 | 1.0 |
| BDPP-009 | 1.0 | 1.0 | 1.0 | 1.0 |
| BDPP-010 | 1.0 | 1.0 | 1.0 | 1.0 |
| BDPP-011 | 0.0 | 0.0 | 0.0 | 0.0 |
| BDPP-012 | 0.5 | 0.5 | 0.5 | 0.5 |

These values describe exact annotation coverage, not automatic judgments about whether the retrieved passages are substantively sufficient answers.

For BDPP-010, the designated chunk `output_verification::005` appears at rank 3, so the question achieves complete top-three coverage despite the first two retrieved chunks coming from Transformation.

## 6. Focused Failure Analysis

### 6.1 BDPP-002 — Revised authoritative-source annotations

**Question:** When are rejected records excluded, and under what condition is a dataset-version candidate created?

The V1 dataset designated:

- `platform_overview::003`
- `ingestion_validation::006`

The revised V2 dataset designates:

- `ingestion_validation::006`
- `dataset_versioning::001`

V2 also changes the designated documents and evidence-role annotations to reflect the more specific governing sources.

The question wording remains unchanged.

**Preserved retrieval ranking in both evaluations:**

| Rank | Retrieved chunk |
|---|---|
| 1 | `dataset_versioning::001` |
| 2 | `output_verification::001` |
| 3 | `diagnostics::005` |

Under V1 annotations, neither designated chunk was retrieved.

Under V2 annotations, one of two designated chunks was retrieved, giving chunk recall 0.5.

The missing designated chunk is `ingestion_validation::006`.

The change in measured outcomes comes from revising the evaluation annotations, not from a changed retrieval ranking.

The retrieved dataset-versioning evidence does not itself demonstrate retrieval of the separate governing ingestion-validation requirement.

### 6.2 BDPP-007 — Revised cross-component question

The original V1 question asked whether a partially accepted batch could create a dataset version and which records were included.

The V2 question explicitly requests:

- Schema Validation's definition of a partially accepted batch.
- Dataset Versioning's separate requirements for version creation and included records.

Both versions designate:

- `ingestion_validation::006`
- `dataset_versioning::001`

**V1 retrieved chunks:**

| Rank | Retrieved chunk |
|---|---|
| 1 | `dataset_versioning::001` |
| 2 | `output_verification::001` |
| 3 | `diagnostics::005` |

**V2 retrieved chunks:**

| Rank | Retrieved chunk |
|---|---|
| 1 | `ingestion_validation::005` |
| 2 | `dataset_versioning::001` |
| 3 | `output_verification::001` |

The revised query causes a different retrieval ranking.

V2 retrieves both designated documents: Ingestion Validation and Dataset Versioning.

However, it does not retrieve `ingestion_validation::006`, which remains one of the two designated gold chunks.

Accordingly:

- V2 designated-document recall is 1.0.
- V2 designated-chunk recall is 0.5.
- Complete Chunk Accuracy@3 remains unsuccessful for this question.

The retrieval of `ingestion_validation::005` is not interchangeable with retrieval of `ingestion_validation::006` for exact gold-chunk scoring.

This case demonstrates why document-level and chunk-level coverage must be reported separately.

### 6.3 BDPP-003 — Alternative Diagnostics evidence

The question concerns the consequences of submitting a batch with an unsupported schema version.

The designated chunks are:

- `ingestion_validation::004`
- `ingestion_validation::005`

The preserved top-three retrieval results instead contain:

- `diagnostics::002`
- `platform_overview::002`
- `platform_overview::003`

Neither designated chunk is retrieved.

Earlier manual adjudication identified alternative Diagnostics evidence as substantively sufficient for the question.

This assessment is separate from exact designated-source scoring.

The automated metrics continue to record the designated-source retrieval failure.

### 6.4 BDPP-011 — Persistent retrieval failure

The question asks whether `PARTIALLY_ACCEPTED` and `VERSION_VERIFIED` can both describe the processing history of one batch.

The designated chunk is:

`diagnostics::001`

The preserved top-three retrieval results contain:

1. `output_verification::001`
2. `ingestion_validation::006`
3. `output_verification::005`

The designated Diagnostics chunk and document are absent.

Earlier adjudication identified this as a genuine unresolved retrieval failure.

Neither V2's revised annotations for other questions nor its aggregate metric differences resolve this case.

### 6.5 BDPP-012 — Alternative evidence and incomplete designated coverage

The question asks how dataset status and diagnostic reporting differ when verification fails.

The designated chunks are:

- `output_verification::006`
- `diagnostics::006`

The preserved top-three results contain:

1. `diagnostics::006`
2. `dataset_versioning::005`
3. `diagnostics::005`

Only one designated chunk is retrieved.

The required Output Verification document and verification evidence role are absent from the retrieved top three.

Earlier manual adjudication found alternative retrieved evidence substantively sufficient.

Nevertheless, exact designated-document and chunk coverage remain incomplete, and complete expected-role coverage is not achieved.

This illustrates the difference between substantive evidence adjudication and automated designated-source retrieval scoring.

## 7. Interpretation of the V1/V2 Comparison

The evaluations must be interpreted as a comparison between two related development evaluation designs.

There are two different types of revision.

**BDPP-002 — Annotation revision**

The question and retrieval rankings are unchanged, while designated gold documents, roles, and chunks are revised.

Any associated metric difference reflects the revised target annotations.

**BDPP-007 — Query revision**

The revised question wording explicitly requires cross-component evidence.

The retrieval rankings change, and designated-document coverage increases, but exact designated-chunk coverage remains incomplete.

The remaining ten evaluation question records are unchanged.

Consequently, the aggregate differences combine annotation effects and changes in retrieval behavior induced by different question wording.

They do not isolate changes to the embedding model, chunking algorithm, similarity computation, or retrieval-ranking implementation.

The comparison also does not establish statistical generalizability beyond this small development question set.

## 8. Evaluation Dimensions and Adjudication

The project distinguishes three dimensions when interpreting its results.

**A. Exact designated authoritative-source retrieval**

Whether retrieved documents or chunks match the explicitly designated gold annotations.

This is the principal focus of the automated document-level and chunk-level metrics.

**B. Substantive answer sufficiency**

Whether retrieved evidence contains sufficient information to answer the actual question.

The nine automated retrieval metrics do not independently measure this dimension.

**C. Source authority**

Whether retrieved evidence comes from the component or specification that governs the requirement.

Evidence-role labels provide structural categories but cannot independently establish governing-source authority.

Manual adjudications for cases such as BDPP-003 and BDPP-012 should therefore not be silently converted into automated retrieval successes.

Likewise, the unresolved BDPP-011 retrieval failure must remain visible.

## 9. Limitations and Reproducibility

### 9.1 Synthetic and development-stage evaluation

The corpus contains six fictional documents and 47 deterministic chunks.

The evaluation contains only 12 corpus-grounded questions and is not blinded.

No claim of broad retrieval-system generalizability is supported by these experiments alone.

### 9.2 Metric limitations

The metrics measure designated source and evidence-role coverage, including ranking and completeness.

They do not automatically evaluate generated-answer faithfulness, factual sufficiency, or source authority.

### 9.3 Baseline reconstruction

The V1 baseline artifact was reconstructed from verified real-model console output.

Its reported cosine-similarity scores are rounded to six decimal places.

The artifact should not be represented as a fresh inference execution or a full-precision archive of the original embedding outputs.

### 9.4 Environment limitations

The saved records identify the embedding model, CPU device, cosine-similarity retrieval, corpus size, and retrieval depth.

They do not establish the exact embedding-model revision or all dependency package versions.

Reproducing a run under a different environment may not generate identical numerical scores or rankings.

### 9.5 Experimental preservation

The preserved datasets and result artifacts are retained as separate V1 and V2 records.

Their SHA-256 fingerprints provide integrity references, not proof of external publication rights or independently validated scientific reproducibility.

### 9.6 Publication limitations

This project represents educational and independently developed experimental work.

It does not establish professional production deployment experience.

Final intellectual-property, licensing, security, provenance, and publication-readiness reviews remain outstanding.

## 10. Artifact Integrity References

The following SHA-256 fingerprints identify the preserved experimental artifacts.

| Artifact | SHA-256 |
|---|---|
| V1 evaluation dataset | `4e8e1bb9ed9fa732b9dcdab21a677555c5f8a4122c62bbb515f937c9cf133448` |
| V2 evaluation dataset | `affba62b62294eda0d4cea2da24571d6c1ed20438c66d1d39b430951aaca69e6` |
| V1 baseline result | `26bf055712d984fa0d206adac1b0bc220ae55004424e642d89fc2deb1002d3cc` |
| V2 direct-execution result | `3284eecbe7e5aedf4e66c1f02f88310ce8f9a9d48ba510868c90675e07507b20` |

These fingerprints were confirmed during the read-only artifact-integrity inspection.

## 11. Related Documentation

- `docs/evaluation-methodology.md` — Quantitative metric definitions, evaluation-design assumptions, evidence dimensions, and methodological limitations.
- `docs/provenance.md` — Project origins, engineering-component reuse, independent synthetic-material development, and substantial ChatGPT assistance disclosure.
- `README.md` — Public-edition project overview and navigation, to be prepared after the detailed documentation.

The original private v1.0.0 repository remains unchanged. Its historical commits are not imported into the independent public-development repository.

No public release is authorized by the preparation of these evaluation results.
