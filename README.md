# RAG Document Intelligence Evaluation

**A development-stage retrieval-evaluation project using independently developed synthetic documentation for a fictional Batch Data Processing Platform (BDPP).**

This project investigates how effectively embedding-based retrieval identifies designated supporting documents, evidence roles, and specific source chunks when questions involve overlapping technical requirements.

The public-edition development work builds on reusable engineering components from an earlier private project while replacing its experimental corpus and questions with newly developed synthetic materials.

**Status:** Independent public edition in private release preparation. Internal licensing, intellectual-property, security, provenance, and publication-readiness reviews have been completed for the approved 31-file release candidate. Public publication remains on hold pending separate explicit authorization.

## 1. Project Overview

Technical documentation frequently distributes relevant information across multiple files. A retrieval system may identify a relevant document without retrieving the specific passage needed to answer a question.

This project examines such distinctions through a controlled synthetic documentation corpus.

It implements:

- Markdown document loading and deterministic chunking.
- Text embeddings using `BAAI/bge-small-en-v1.5`.
- Cosine-similarity top-k chunk retrieval.
- Document-level, evidence-role, and chunk-level evaluation.
- Retrieval failure identification and categorization.
- Preserved experimental records and question-level analysis.

The focus is **retrieval evaluation**, not generated-answer production.

The project does not implement or claim to evaluate a complete production retrieval-augmented generation (RAG) application.

## 2. Synthetic Documentation Corpus

The evaluation uses six fictional Markdown specifications describing a hypothetical batch-oriented inventory processing platform.

| Document | Subject |
|---|---|
| `01-platform-overview.md` | Platform context and processing stages |
| `02-ingestion-validation.md` | Ingestion, schema validation, and record acceptance |
| `03-transformation.md` | Record transformations and normalization |
| `04-dataset-versioning.md` | Dataset-version creation and included-record rules |
| `05-output-verification.md` | Output consistency and verification requirements |
| `06-diagnostics.md` | Processing outcomes and diagnostic reporting |

The corpus consists of **47 unique deterministic chunks**.

The documents intentionally contain related concepts and overlapping terminology, creating opportunities to examine whether retrieval identifies the appropriate governing evidence rather than merely a generally relevant passage.

The fictional platform is not a deployed software product. Its technical rules are synthetic experimental material.

Corpus files are located in `data/corpus/`.

## 3. Retrieval and Evaluation Architecture

The implemented retrieval workflow consists of the following conceptual stages:

**Document loading → Deterministic chunking → Embedding generation → Cosine-similarity ranking → Top-k retrieval → Evaluation and failure analysis**

The Python package is located under `src/rag_document_intelligence_eval/`.

| Module | Responsibility |
|---|---|
| `models.py` | Data models, metadata, evidence roles, and evaluation structures |
| `corpus.py` | Corpus-document definitions |
| `loader.py` | Document loading and corpus validation |
| `chunking.py` | Deterministic document chunking |
| `embeddings.py` | Embedding-model loading and embedding generation |
| `retrieval.py` | Cosine-similarity retrieval |
| `evaluation.py` | Retrieval metrics and failure analysis |

The project uses individual document chunks as retrieval units.

Each retrieved chunk retains metadata identifying its source document and evidence role.

The evaluations were recorded using CPU execution and top-three retrieval.

## 4. Evaluation Design

Two preserved development evaluation datasets are available:

| Dataset | File | Questions |
|---|---|---:|
| V1 | `data/evaluation/bdpp_retrieval_questions.json` | 12 |
| V2 | `data/evaluation/bdpp_retrieval_questions_v2.json` | 12 |

Both datasets use schema version `1.1`.

Each question includes designated expected documents, expected evidence roles, expected chunks, and human-readable gold-evidence annotations.

The project calculates nine automated retrieval metrics.

**Document-level metrics**

- Document Hit@1
- Document Hit@3
- Mean Document Recall@3
- Mean Reciprocal Rank
- Complete Document Accuracy@3

**Evidence-role metric**

- Evidence Role Accuracy@3

**Chunk-level metrics**

- Chunk Hit Rate@3
- Mean Chunk Recall@3
- Complete Chunk Accuracy@3

These metrics evaluate related but distinct retrieval properties.

For example, Complete Document Accuracy@3 requires all designated source documents to appear in the first three results, whereas Complete Chunk Accuracy@3 requires all designated chunk IDs.

Evidence Role Accuracy@3 measures complete expected-role coverage. It does not independently establish correct source authority.

The methodology distinguishes three evaluation dimensions:

1. Exact designated authoritative-source retrieval.
2. Substantive answer sufficiency.
3. Source authority.

The automated metrics do not independently establish substantive answer sufficiency or governing-source authority.

See [Evaluation Methodology](docs/evaluation-methodology.md) for definitions and limitations.

## 5. Experimental Results

Two development-stage real-model retrieval evaluations were preserved on November 12, 2026.

**V1** is an archival baseline reconstructed from verified original real-model console output without rerunning inference.

**V2** is a direct real-model execution using a revised evaluation dataset.

### Aggregate metrics

| Metric | V1 | V2 |
|---|---:|---:|
| Document Hit@1 | 0.6667 | 0.7500 |
| Document Hit@3 | 0.7500 | 0.8333 |
| Mean Document Recall@3 | 0.6667 | 0.7500 |
| Mean Reciprocal Rank | 0.6944 | 0.7778 |
| Complete Document Accuracy@3 | 0.5833 | 0.6667 |
| Evidence Role Accuracy@3 | 0.6667 | 0.7500 |
| Chunk Hit Rate@3 | 0.7500 | 0.8333 |
| Mean Chunk Recall@3 | 0.6667 | 0.7083 |
| Complete Chunk Accuracy@3 | 0.5833 | 0.5833 |

**Interpretation:** V2 has higher values for several designated-source metrics, but Complete Chunk Accuracy@3 remains unchanged at 0.5833.

These differences must not be interpreted as an isolated improvement to the embedding model or retrieval algorithm.

Only two question records changed between datasets:

**BDPP-002:** Gold-source annotations changed, but the question wording and retrieved rankings remained unchanged.

**BDPP-007:** Question wording changed to explicitly request cross-component evidence, producing different retrieval rankings.

The remaining ten question records were unchanged.

Consequently, V1/V2 numerical differences reflect a combination of annotation changes and query-dependent retrieval behavior, not a controlled retrieval-algorithm change.

See [Evaluation Results](docs/evaluation-results.md) for detailed comparisons, question-level outcomes, and artifact fingerprints.

## 6. Selected Retrieval Findings

The preserved results highlight several useful failure-analysis cases.

### BDPP-002 — Gold annotation revision

Revised annotations identify the governing Ingestion Validation and Dataset Versioning evidence.

The retrieval rankings do not change between V1 and V2.

V2 retrieves `dataset_versioning::001` but misses the other designated chunk, `ingestion_validation::006`.

This illustrates how evaluation annotations can change reported metrics without changing the retrieval behavior.

### BDPP-007 — Document coverage versus chunk coverage

The revised question explicitly requests evidence from Schema Validation and Dataset Versioning.

Both designated documents appear within the top three results.

However, exact designated-chunk recall remains 0.5 because `ingestion_validation::006` is not retrieved.

This demonstrates that retrieving the correct documents does not necessarily mean retrieving every required passage.

### BDPP-003 and BDPP-012 — Alternative evidence

Manual adjudication identified alternative retrieved evidence as substantively sufficient for these questions despite incomplete exact designated-source coverage.

These judgments are reported separately from the automated retrieval metrics.

### BDPP-011 — Unresolved retrieval failure

The designated Diagnostics evidence is absent from the top-three retrieval results.

This remains an unresolved retrieval failure in the preserved development evaluation.

The project retains such failures rather than modifying reporting to make all evaluated questions appear successful.

## 7. Repository Structure

The development repository contains the following principal directories and files:

| Path | Contents |
|---|---|
| `data/corpus/` | Six synthetic BDPP specification documents |
| `data/evaluation/` | V1 and V2 question datasets |
| `data/evaluation/results/` | Preserved V1 and V2 experimental JSON records |
| `src/rag_document_intelligence_eval/` | Python retrieval and evaluation implementation |
| `tests/` | Six Python test modules |
| `docs/evaluation-methodology.md` | Evaluation methodology and metric semantics |
| `docs/evaluation-results.md` | Results, comparisons, and failure analysis |
| `docs/provenance.md` | Development origin, reuse, AI assistance, and publication controls |
| `requirements.txt` | Direct runtime dependencies and audited development-environment versions |
| `requirements-dev.txt` | Development/test dependencies and reference to runtime requirements |
| `.gitignore` | Local environment, cache, and sensitive-file exclusions |

The test modules address chunking, corpus definitions, embeddings, evaluation, loading, and retrieval.

## 8. Execution and Reproducibility Status

The repository currently contains reusable Python modules, preserved experimental artifacts, and direct-dependency manifests.

The `requirements.txt` and `requirements-dev.txt` files record direct dependency versions observed in the audited Python 3.12.9 development environment. They do not constitute a complete transitive-dependency lockfile or reconstruct the exact historical experimental environment.

However, the inspected development snapshot does **not** yet contain:

- A packaged command-line interface or standalone experiment runner.
- A documented, independently verified clean-environment installation procedure.
- A validated one-command workflow for reproducing the complete saved experiments.

Accordingly, this README does not claim that a fresh installation or complete experiment reproduction has been independently verified.

The underlying retrieval and evaluation components have been exercised during local development, and their saved results are available for inspection.

The presence of unit-test modules and previously executed local experiments should not be interpreted as proof that the repository can currently be installed and reproduced without additional environment preparation.

The saved experiment records identify the embedding model, CPU device, retrieval method, corpus size, evaluation dataset, and top-three results.

They do not establish the exact embedding-model revision or all dependency versions.

Future reproducibility work may require a validated execution entry point, fuller environment pinning, and clean-environment testing before making stronger reproduction claims.

No new inference execution is required merely to inspect the preserved results.

## 9. Development Provenance and AI Assistance

The independent public edition was developed from engineering work originating in an earlier private version of RAG Document Intelligence Evaluation.

The original private project and its historical Git commits remain separate.

Reusable engineering components were selectively retained or adapted. The public edition must not be described as a wholly new implementation written from scratch without reference to the private project.

The replacement BDPP scenario, synthetic corpus, and development evaluation datasets were prepared separately for the public edition.

**Substantial assistance from OpenAI's ChatGPT** was involved in project planning, fictional specification drafting, implementation guidance, evaluation design, debugging, experimental interpretation, failure analysis, and documentation.

The user directed the development process, reviewed decisions, executed local commands and experiments, examined outputs, and authorized bounded modifications.

The work is appropriately characterized as human-directed, AI-assisted educational engineering and experimental evaluation.

It is not represented as wholly unaided engineering, independently validated research, or professional production deployment experience.

Additional provenance and rights reviews remain necessary before publication.

See [Development Provenance](docs/provenance.md).

## 10. Limitations

This project has several important limitations.

**Synthetic data:** The documents describe a fictional batch processing platform rather than a production system.

**Small evaluation size:** Each development evaluation contains only 12 questions.

**Corpus-grounded questions:** The evaluation is not blinded or independently constructed.

**Gold-source sensitivity:** Exact retrieval metrics depend on the designated documents and chunk annotations.

**No generated-answer evaluation:** The project does not measure factual correctness or faithfulness of generated RAG answers.

**No automatic substantive adjudication:** Automated metrics cannot independently establish whether retrieved passages sufficiently answer each question.

**No automatic source-authority verification:** Evidence-role matching does not prove the correct governing source was retrieved.

**Limited reproducibility metadata:** Exact model revision and all software dependency versions were not recorded.

**No production validation:** The experiments do not establish operational scalability, security, reliability, or production readiness.

**Comparison limitations:** The V1/V2 evaluations use revised annotations and question wording, so their aggregate differences are not attributable to an isolated algorithm change.

These limitations are material to the interpretation of the reported results.

## 11. Documentation

Additional technical documentation is available:

- [Evaluation Methodology](docs/evaluation-methodology.md) — Retrieval configuration, evaluation annotations, nine metric definitions, evidence dimensions, and methodological limitations.
- [Evaluation Results](docs/evaluation-results.md) — Preserved experimental outputs, aggregate and question-level results, failure analysis, and integrity fingerprints.
- [Development Provenance](docs/provenance.md) — Original project preservation, synthetic-material development, engineering-component reuse, AI assistance, and publication safeguards.

## 12. Publication and Licensing Status

This repository is currently an independent public-edition **development workspace**, not an authorized public release.

Before publication, the proposed repository snapshot requires final intellectual-property, copyright, provenance, dependency-licensing, security, attribution, and documentation-consistency reviews.

### Licensing and Reuse

**Licensing decision — November 14, 2026:** The proposed public edition is intended primarily for technical portfolio evaluation by prospective employers.

No open-source license is being offered for the project's source code, documentation, synthetic corpus, or evaluation artifacts at this time.

This README does not grant general permission to reuse, modify, or redistribute repository materials. Permissions arising under applicable law, GitHub's Terms of Service, or applicable third-party licenses remain unaffected.

This statement does not assert exclusive ownership or copyright protection over every repository component. Third-party rights, AI-assisted materials, and other applicable rights limitations remain subject to review.

The decision not to offer an open-source license does not constitute authorization to publish the repository or establish completion of intellectual-property, copyright, contractual, security, or other final release reviews.

See [Development Provenance](docs/provenance.md) for project origin, engineering reuse, substantial ChatGPT assistance, and publication safeguards.

No permission to publish or redistribute the repository should be inferred from this README.

A separate affirmative publication decision is required after the actual proposed release snapshot has been reviewed.
