# Batch Data Processing Platform — Dataset Versioning

## Dataset Versioning Purpose

The Dataset Versioning component of the Batch Data Processing Platform (BDPP) organizes transformed equipment inventory records into identifiable dataset versions.

Dataset Versioning operates after Transformation and before Output Verification.

Its responsibilities include determining whether transformed records are eligible for version creation, assigning unique version identifiers, retaining batch/source lineage, preserving immutable dataset contents, and maintaining version verification status.

A dataset version represents the transformed inventory records associated with one eligible input batch.

Dataset versions are not cumulative snapshots of previously processed batches.

## Version Creation Eligibility

Dataset Versioning receives the transformed records produced from an inventory batch.

A batch is eligible to create a dataset version candidate when at least one accepted inventory record has been successfully transformed.

The following rules apply:

1. An eligible batch creates exactly one dataset version candidate.
2. The candidate contains the transformed records associated with that batch.
3. No dataset version is created when zero transformed records are available.
4. A partially accepted batch may create a dataset version if at least one accepted record was transformed.
5. Rejected inventory records must not appear in the dataset version.

Version creation eligibility depends on the presence of transformed records rather than whether every submitted inventory record passed validation.

For example, a batch containing five inventory records may have three accepted records and two rejected records.

If the three accepted records are transformed, the batch is eligible to create one dataset version candidate containing those three transformed records.

The two rejected records do not belong to that dataset version.

If all five records are rejected, no transformed records are available and no dataset version is created.

## Version Identity and Metadata

Each dataset version has a unique identifier that distinguishes it from other versions.

The identifier supports unambiguous references to a particular version during output verification and diagnostic reporting.

Dataset version metadata retains the information needed to establish the version's origin and processing context.

This includes:

- A unique dataset version identifier.
- The originating `batch_id`.
- The originating `source_id`.
- A valid UTC `created_at` timestamp recording dataset version creation.
- Relevant inventory record counts.
- The dataset version's verification status.

Record-count information must accurately represent the records associated with the version.

The version's metadata supports downstream consistency checks and processing traceability.

A dataset version identifier is distinct from the originating batch identifier. Both support identification, but they refer to different concepts.

The original batch identifier identifies the submitted inventory batch, while the dataset version identifier identifies the dataset version created from its transformed records.

This conceptual specification requires unique version identifiers but does not prescribe a particular identifier-generation algorithm.

## Dataset Content and Immutability

A dataset version contains the standardized inventory records produced by Transformation.

These records retain the validated inventory information, normalized update timestamps, and derived available quantities established by the Transformation component.

The dataset records associated with a created version are immutable.

Immutability means that the version's dataset contents are not modified after creation.

Output Verification evaluates the dataset version against established requirements without changing its stored inventory records.

A verification failure does not authorize the verification process to rewrite, remove, or replace the version's records.

The version's verification status is tracked separately from the immutable dataset contents.

This distinction allows a version to move through its verification lifecycle without violating dataset-record immutability.

## Batch and Source Lineage

Every dataset version retains information connecting it to its originating inventory batch and source.

The primary lineage identifiers are:

- `batch_id`: identifies the inventory batch from which the version was created.
- `source_id`: identifies the source associated with that batch.

These identifiers establish the relationship between the original submission and the resulting dataset version.

The transformed records included in a version must correspond to records accepted from its originating batch.

The relative ordering of accepted records is preserved through Transformation and must remain consistent in the version's dataset contents.

Lineage information supports Output Verification, which checks whether the resulting dataset correctly corresponds to the accepted inventory information.

Lineage also supports Diagnostics and Processing Outcome Reporting by allowing processing results to be associated with the relevant batch and dataset version.

## Dataset Version Status Lifecycle

A newly created dataset version begins with the status:

`PENDING_VERIFICATION`

This status indicates that the dataset version has been created but has not yet received its final output verification result.

Output Verification evaluates the version and determines one of two final outcomes.

### VERIFIED

A version receives the status `VERIFIED` when it satisfies the applicable output verification requirements.

This indicates that the version passed the established output consistency checks.

### FAILED_VERIFICATION

A version receives the status `FAILED_VERIFICATION` when it fails one or more applicable output verification requirements.

The failed status identifies the verification outcome without requiring modification of the version's immutable dataset records.

### Permitted status transitions

The accepted version lifecycle permits the following transitions:

- `PENDING_VERIFICATION` → `VERIFIED`
- `PENDING_VERIFICATION` → `FAILED_VERIFICATION`

The two final states represent alternative outcomes.

The initial scenario does not define additional version status transitions or a separate remediation workflow.

Dataset version statuses are distinct from diagnostic reporting categories such as `VERSION_PENDING`, `VERSION_VERIFIED`, and `VERSION_FAILED`.

Diagnostic categories describe processing outcomes for reporting purposes. They do not replace the actual dataset version status values.

## Non-Cumulative Version Semantics

BDPP dataset versions represent independently processed inventory batches.

A new dataset version does not automatically include inventory records from previous dataset versions.

For example, suppose Batch A produces three transformed records and Batch B produces four transformed records.

If both batches are eligible, BDPP creates:

- One dataset version containing the three transformed records from Batch A.
- A separate dataset version containing the four transformed records from Batch B.

The second version does not automatically contain seven records.

This behavior distinguishes BDPP's per-batch dataset versioning from cumulative snapshot systems.

The initial versioning specification does not introduce historical aggregation, cross-version merging, or reconciliation of inventory records across batches.

Each version retains its own identity, lineage, dataset contents, and verification status.

## Relationship to Output Verification and Diagnostics

Dataset Versioning creates and maintains dataset version candidates according to the established eligibility and metadata requirements.

Output Verification subsequently determines whether a created version satisfies its consistency requirements.

Diagnostics reports relevant processing outcomes, including whether a dataset version was created and whether its verification succeeded or failed.

These components have separate responsibilities:

- Dataset Versioning creates identifiable, immutable dataset versions.
- Output Verification checks the correctness and consistency of those versions.
- Diagnostics reports the resulting processing and verification outcomes.

Dataset Versioning does not independently define the detailed verification checks or diagnostic reporting rules.

Those requirements are maintained in their respective technical documents.