# Development Provenance

## 1. Purpose

This document records the development origin, engineering reuse boundaries, synthetic data provenance requirements, AI assistance, and publication controls for the public edition of **RAG Document Intelligence Evaluation**.

Its purpose is to support transparent attribution, reproducibility, and responsible publication.

This document is a development record, not a declaration that the repository has passed its final intellectual-property, licensing, security, or publication review.

## 2. Project Origin

The public edition is being developed from engineering work originally undertaken in a separate private project, *RAG Document Intelligence Evaluation*.

The original private project completed its planned v1.0.0 engineering scope, including document retrieval, evaluation, and failure analysis.

The public edition is a separate development effort intended to preserve appropriately reusable engineering work while replacing experimental materials whose publication provenance has not been sufficiently established.

The public edition must not be represented as an entirely independent implementation developed from scratch.

## 3. Original Private Project Preservation

The original private v1.0.0 repository and its 44-commit development history are retained separately.

The public edition uses a newly initialized Git repository with an independent history. The original 44 commits have not been imported.

The original private corpus, evaluation questions, and experimental findings are not automatically cleared for publication.

The separate sanitized historical preparation repository is not the source of the public edition's Git history.

Preservation of the original private project is a standing development requirement.

## 4. Replacement Synthetic Scenario

The original fictional service-level-objective (SLO) scenario has not been cleared for public release because its independent provenance has not been sufficiently established.

This precautionary determination does not establish that the original material infringed copyright, disclosed confidential information, or involved misconduct.

The approved replacement domain is an independently developed fictional batch-oriented data processing platform.

Planned documentation topics include:

- Data ingestion and input specifications.
- Schema validation.
- Data transformation.
- Version and change management.
- Verification and diagnostics.

The fictional platform serves as technical subject matter for evaluating document retrieval. The platform itself is not intended to be implemented.

The replacement material must not reproduce the original uncleared SLO procedure through renaming, paraphrasing, or superficial modification.

At the time of this initial record, the replacement scenario and corpus have not yet been developed.

## 5. Synthetic Material Provenance

New synthetic documents, evaluation questions, expected evidence, and scoring criteria must have documented origins.

Development records should identify:

- How fictional technical requirements were established.
- Which materials were newly authored.
- Whether external references or third-party materials were used.
- How potentially sensitive or uncleared content was excluded.
- How expected evidence and evaluation labels were verified.

The fictional documents must not contain employer-confidential information, proprietary operational procedures, internal business rules, or unauthorized third-party material.

Synthetic content must be identified as fictional. Its provenance must be established through documented development evidence, rather than through the synthetic label alone.

## 6. Engineering Component Reuse

The following existing engineering capabilities are candidates for selective reuse:

- Document loading.
- Text chunking.
- Embedding generation.
- Cosine-similarity retrieval.
- Evaluation infrastructure.
- Failure-analysis infrastructure.
- Relevant automated tests.

Reuse is subject to source review, appropriate rights clearance, compatibility checks, and necessary modifications.

A component's presence in the original private repository does not, by itself, authorize its inclusion in the public edition.

Reused components must be represented accurately as reused engineering work.

No engineering components had been copied into the new public-development workspace when this initial document was drafted.

## 7. AI Assistance and Human Review

The original project received substantial assistance from OpenAI's ChatGPT, including development planning, implementation guidance, debugging assistance, experimental interpretation, documentation, and troubleshooting.

The public-edition preparation has also received substantial ChatGPT assistance, including publication strategy evaluation, provenance review, and development planning.

Future AI-assisted contributions must be described accurately.

Human execution, code review, experimental verification, and independent understanding must not be claimed unless those activities actually occurred.

AI-generated content and suggested implementations remain subject to technical validation, provenance review, and applicable rights checks.

## 8. Evaluation and Experimental Integrity

The public edition is intended to evaluate document retrieval and supporting-evidence selection.

It must not be described as a complete retrieval-augmented answer-generation system unless that capability is actually implemented and verified.

Evaluation materials should support:

- Direct evidence retrieval.
- Version-sensitive retrieval.
- Cross-document evidence retrieval.
- Identification of correct supporting evidence among similar but inappropriate evidence.

Evaluation questions must have traceable expected evidence and defined scoring criteria.

New experiments must be executed against the replacement corpus.

Results from the original private v1.0.0 corpus must not be presented as experimental results from the public edition.

Observed retrieval failures must be reported based on actual experimental evidence rather than designed to reproduce earlier failure categories.

## 9. Dependencies, Licensing, and Third-Party Rights

External software dependencies, pretrained models, and other third-party components require appropriate licensing and usage review.

Dependency versions, applicable notices, attribution obligations, and relevant redistribution requirements must be documented before publication.

No public-edition license has been approved.

MIT licensing remains on hold pending appropriate review.

No third-party material should be included solely because it was accessible in the original project.

## 10. Security and Publication Controls

Before publication, the actual proposed public repository snapshot must undergo appropriate review for:

- Confidential or proprietary information.
- Personal information and credentials.
- Copyright and intellectual-property concerns.
- Third-party licensing and attribution.
- Synthetic corpus provenance.
- Source-code and documentation consistency.
- Experimental integrity and reproducibility.
- Security-sensitive material.
- Accurate development and AI-assistance disclosures.

Any unresolved material clearance concern must be investigated, remediated, or excluded before publication approval.

No review can guarantee the absence of all legal or technical risks.

## 11. Initial Development Status

As of November 10, 2026:

- Option B + D has been approved as the public-edition development strategy.
- The original private v1.0.0 project remains designated for preservation.
- A separate, initially empty development directory has been created.
- A new local Git repository has been initialized on `main`.
- The new repository has no commits.
- No original engineering components have been copied into the new repository.
- The replacement synthetic corpus has not been created.
- Fresh public-edition experiments have not been performed.
- No public-edition license has been approved.
- Publication has not been authorized.

Future development actions and clearance decisions should be recorded as they occur.

## 12. Publication Authorization

Development-strategy approval does not constitute publication authorization.

A separate affirmative publication decision is required after reviewing the actual proposed public-release snapshot.

Until then, the public edition remains a development project, and the original private repository must remain unchanged.

## 13. Development Update — November 12, 2026

This dated update records development work completed after the initial November 10, 2026 provenance snapshot in Section 11.

The earlier snapshot is retained as a historical record. Its statements about the initially empty repository, undeveloped corpus, and absence of experiments describe the project's status on November 10 and should not be interpreted as its current status.

This update does not supersede the publication requirements, rights restrictions, or authorization boundaries established in Sections 1–12.

### 13.1 Independent Public-Edition Development Status

As of November 12, 2026, the separate public-development repository contains an implementation of the fictional Batch Data Processing Platform (BDPP) document-retrieval evaluation.

The implemented experimental materials include:

- Six newly developed fictional Markdown specification documents.
- A deterministic corpus containing 47 unique document chunks.
- Two development evaluation datasets, V1 and V2, each containing 12 questions.
- Nine automated retrieval metrics addressing document, evidence-role, and chunk retrieval.
- Preserved V1 and V2 real-model retrieval-evaluation records.
- Automated tests and supporting engineering components.
- Evaluation methodology and results documentation.

The implementation uses the `BAAI/bge-small-en-v1.5` embedding model and cosine-similarity retrieval.

The public-development repository remains separate from the original private v1.0.0 project. The original 44-commit development history has not been imported, and the public-development repository has no commits as of this update.

The original private repository remains designated for preservation without modification.

### 13.2 Replacement Synthetic Scenario and Material Provenance

The replacement BDPP scenario was newly developed for the public edition as a fictional technical specification, with substantial assistance from ChatGPT and iterative human review.

The six corpus documents are:

1. `01-platform-overview.md`
2. `02-ingestion-validation.md`
3. `03-transformation.md`
4. `04-dataset-versioning.md`
5. `05-output-verification.md`
6. `06-diagnostics.md`

The specification addresses fictional ingestion rules, schema validation, transformation behavior, dataset-version creation, output verification, and diagnostic reporting.

The documents were designed to support retrieval questions involving direct evidence, overlapping requirements, and cross-component reasoning.

The original private project's uncleared SLO scenario was excluded from the replacement corpus design.

The new materials are intended to be independently developed synthetic experimental content, rather than a renamed or paraphrased reproduction of the original SLO scenario.

This development intention and the associated review process do not, by themselves, constitute a completed legal, copyright, confidentiality, or independent-provenance clearance.

The final proposed public-release snapshot must still be reviewed for unintended reuse of uncleared content and for employer, client, university, or other third-party material.

The user has described the project as independently undertaken educational work. That account is relevant development provenance, but it is not a substitute for final source and rights verification.

### 13.3 Engineering Component Reuse and Adaptation

The public edition selectively reuses or adapts engineering capabilities developed in the original private project.

The engineering work includes document loading, text chunking, embedding generation, cosine-similarity retrieval, evaluation logic, failure analysis, and relevant automated tests.

The public edition also introduces modifications and redesigns needed to support the independent BDPP corpus and its evidence annotations.

In particular, evaluation question structures and scoring logic were adapted to support explicit expected-document, expected-evidence-role, and expected-chunk annotations.

Engineering reuse must be distinguished from the creation of new synthetic experimental materials.

The public edition must not be described as an entirely new, independently written codebase developed without reference to the original private project.

The earlier engineering-component reuse assessment was preliminary. Its technical acceptance does not independently establish that every adapted file has completed final intellectual-property, licensing, attribution, or security review.

A final component-level review remains required before publication.

### 13.4 Evaluation Dataset Development

The first public-edition evaluation dataset contains 12 corpus-grounded questions.

A separate V2 dataset was prepared to address specific findings from the initial evaluation-design and failure-analysis review.

Only two question records changed:

**BDPP-002:** The designated expected documents, evidence roles, and chunks were revised to identify the governing Ingestion Validation and Dataset Versioning requirements more precisely. The question wording was unchanged.

**BDPP-007:** The question wording and human-readable gold-evidence annotation were revised to explicitly require cross-component evidence. Its designated documents, evidence roles, and expected chunks remained unchanged.

The remaining ten question records are identical between V1 and V2.

Both datasets remain preserved separately under schema version `1.1`.

The revised annotations are not retroactively applied to the original V1 baseline.

### 13.5 Experimental Execution, Preservation, and Integrity

The public edition underwent real-model retrieval evaluation using the replacement BDPP corpus.

The V1 baseline artifact is:

`data/evaluation/results/bdpp_development_baseline_2026-11-12.json`

The original V1 evaluation was executed locally. Its saved archival JSON record was subsequently reconstructed from verified console output without rerunning inference.

The reconstructed artifact preserves the original top-three rankings and cosine-similarity scores at the precision printed during execution.

The V2 artifact is:

`data/evaluation/results/bdpp_development_v2_2026-11-12.json`

V2 represents a direct real-model evaluation execution with the revised dataset.

Both experimental records contain retrieval outcomes for 12 questions and the nine automated evaluation metrics.

The results are preserved alongside their dataset fingerprints and supporting experiment metadata.

The numerical comparison must be interpreted cautiously because V1 and V2 differ in evaluation annotations and question wording.

The comparison does not isolate an embedding-model or retrieval-algorithm change and must not be characterized as proof of an independently improved retrieval model.

Complete Chunk Accuracy@3 remained 0.5833 in both evaluations.

Question-level analysis also preserved important distinctions between:

- Exact designated-source retrieval.
- Substantive answer sufficiency.
- Governing-source authority.

Automated retrieval metrics do not independently establish the latter two dimensions.

Earlier manual adjudications identified substantively useful alternative evidence in BDPP-003 and BDPP-012, while BDPP-011 retains a genuine unresolved retrieval failure.

These observations remain separate from the automated metric values.

Detailed numerical results and interpretation are documented in `docs/evaluation-results.md`.

### 13.6 Documentation and Review Activities

The following documentation files have been prepared, reviewed, and created in the public-development repository:

**`docs/evaluation-methodology.md`**

Documents the retrieval configuration, evaluation schema, nine metric definitions, three evaluation dimensions, failure-analysis methodology, and limitations.

**`docs/evaluation-results.md`**

Documents preserved V1/V2 experimental artifacts, aggregate metrics, question-level outcomes, failure analysis, reproducibility limitations, and artifact fingerprints.

Both documents were reviewed against the applicable source-code and experimental records before creation.

The original November 10 provenance record has been retained as a historical snapshot.

The root `README.md` remains to be prepared separately.

Documentation preparation does not constitute final publication approval.

### 13.7 AI Assistance and Human Verification

Substantial assistance from OpenAI's ChatGPT continued throughout public-edition development.

That assistance included:

- Fictional scenario design and specification drafting.
- Engineering architecture and code adaptation guidance.
- Development of evaluation schemas and scoring logic.
- Suggestions for automated tests and local verification procedures.
- Retrieval experiment planning and interpretation.
- Failure analysis and evidence adjudication support.
- Provenance analysis and documentation drafting.
- PowerShell commands for local inspection, verification, and controlled file creation.

The user reviewed proposed engineering and methodological decisions, executed local commands and experiments, examined resulting outputs, and explicitly authorized bounded repository modifications.

These activities should be described as human-directed, AI-assisted development and local verification.

They should not be represented as wholly unaided engineering work, independent scientific validation, or professional production deployment experience.

ChatGPT-assisted implementation and documentation remain subject to appropriate human technical review and final publication safeguards.

### 13.8 Outstanding Clearance and Publication Controls

As of this update, the public edition remains a local development project.

The following reviews are still required before public release:

- Final intellectual-property and copyright provenance review.
- Review of engineering-component reuse and required attribution.
- Review of software dependencies, pretrained-model licensing, and redistribution obligations.
- Security and sensitive-information inspection of the actual proposed repository snapshot.
- Verification that original uncleared materials and historical Git content have not been inadvertently included.
- Source-code, evaluation-artifact, and documentation consistency review.
- Final confirmation that public-facing descriptions accurately disclose ChatGPT assistance and experimental limitations.
- A separate affirmative decision concerning the repository's license and publication.

No public-edition license has been approved. MIT licensing remains on hold.

No commits, pushes, or public release have been authorized as of this dated update.

Any subsequent authorization must be explicit and limited to the action being approved.

The original private v1.0.0 repository remains outside the public-edition release scope.

## 14. Development Update — November 14, 2026: Repository Licensing Decision

### 14.1 Selected Licensing Policy

On November 14, 2026, the project maintainer selected a no-open-source-license approach for the proposed public edition of RAG Document Intelligence Evaluation.

The primary purpose of the proposed public repository is to demonstrate technical engineering work to prospective employers and other reviewers, rather than to authorize general reuse or redistribution.

No MIT, Apache-2.0, Creative Commons Attribution 4.0, or other open-source or open-content license has been approved for the repository's original project materials.

### 14.2 Historical Licensing Statements

Earlier statements that MIT licensing remained on hold are retained as part of the historical development record.

The November 14 decision supersedes those earlier proposals for the current repository licensing policy. It does not retroactively alter previous development records or establish that any particular material is exclusively owned or copyright-protected.

### 14.3 Rights and Publication Limitations

The absence of an open-source license does not eliminate applicable third-party licenses, statutory permissions, GitHub platform permissions, or other existing legal rights.

This licensing decision does not constitute final intellectual-property, copyright, contractual, confidentiality, security, attribution, or publication clearance.

The substantial ChatGPT-assistance disclosure, synthetic-material provenance requirements, evaluation-integrity disclosures, and historical reproducibility limitations remain applicable.

No repository publication, Git commit, remote configuration, push, or public release is authorized by this decision. A separate final review and explicit publication authorization remain required.
