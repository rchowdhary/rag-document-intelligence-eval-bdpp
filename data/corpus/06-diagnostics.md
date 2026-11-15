# Batch Data Processing Platform — Diagnostics and Processing Outcome Reporting

## Diagnostic Reporting Purpose

The Diagnostics and Processing Outcome Reporting component of the Batch Data Processing Platform (BDPP) provides traceable information about inventory batch processing and dataset verification outcomes.

Its purpose is to describe what occurred during processing without modifying the underlying processing results.

Diagnostic reporting covers:

- Batch-level validation outcomes.
- Individual inventory record acceptance and rejection.
- Accepted and rejected record counts.
- Dataset version creation results.
- Dataset version verification outcomes.
- Details of failed output verification.

The accepted diagnostic requirements are designated `DIA-01` through `DIA-08`.

Diagnostic reporting operates across the conceptual processing lifecycle. It uses information produced by other BDPP components rather than independently performing validation, transformation, or output verification.

## Batch Processing Outcome Categories

BDPP distinguishes input-processing outcomes from dataset-version verification outcomes.

The accepted diagnostic reporting categories are:

| Category | Meaning |
|---|---|
| `BATCH_REJECTED` | The submitted batch failed batch-level requirements and was rejected |
| `PARTIALLY_ACCEPTED` | The batch passed batch-level validation, with some records accepted and others rejected |
| `ALL_RECORDS_ACCEPTED` | The batch passed batch-level validation, and all submitted inventory records were accepted |
| `NO_VALID_RECORDS` | The batch passed batch-level validation, but no submitted inventory records were accepted |
| `VERSION_PENDING` | A dataset version was created and is awaiting output verification |
| `VERSION_VERIFIED` | A created dataset version passed output verification |
| `VERSION_FAILED` | A created dataset version failed output verification |

These categories describe different aspects of the processing lifecycle.

For example, `PARTIALLY_ACCEPTED` describes a batch's record-validation outcome, while `VERSION_VERIFIED` describes the verification outcome of a dataset version created from its accepted records.

Both categories can therefore apply to the processing history of the same batch.

Diagnostic reporting categories are distinct from dataset version status values.

The actual dataset version statuses are:

- `PENDING_VERIFICATION`
- `VERIFIED`
- `FAILED_VERIFICATION`

The reporting categories do not replace or redefine these statuses.

## Batch-Level Rejection Diagnostics

A batch-level validation failure causes the entire inventory batch to be rejected.

Diagnostic reporting must make the rejection outcome traceable to the submitted batch when identifying information is available.

Relevant diagnostic information includes:

- The batch identifier, when available.
- The fact that batch-level validation failed.
- The applicable batch-level validation requirement or rejection reason.
- The resulting batch-rejection outcome.

The diagnostic category for this situation is:

`BATCH_REJECTED`

For example, a batch containing an unsupported `schema_version` fails the applicable batch-level validation requirement.

The batch is rejected rather than having its inventory records individually accepted or rejected.

No transformed inventory records or dataset version are produced from that rejected batch.

Diagnostic reporting describes the rejection without changing the validation decision.

The specification does not require unavailable or invalid identifying information to be reconstructed or invented for diagnostic purposes.

## Record-Level Rejection Diagnostics

When a batch satisfies its batch-level requirements, Schema Validation evaluates individual inventory records.

A record failing one or more applicable validation requirements is rejected independently.

Diagnostic reporting must preserve enough information to distinguish record-level rejection from rejection of the entire batch.

Relevant record-level diagnostic information includes:

- The originating batch context.
- The affected record's identification or position when available.
- The applicable record-level validation failure or rejection reason.
- The record's rejected outcome.

For example, an inventory record with `quantity` equal to `-2` violates the nonnegative integer requirement.

That record is rejected.

Other records in the same batch remain independently eligible for acceptance if they satisfy their applicable validation requirements.

A record-level rejection does not automatically result in `BATCH_REJECTED`.

When a batch contains both accepted and rejected records, diagnostic reporting uses:

`PARTIALLY_ACCEPTED`

If no inventory records are accepted despite successful batch-level validation, the relevant category is:

`NO_VALID_RECORDS`

Diagnostic reporting records these outcomes without reconsidering or overriding the validation decisions.

## Accepted and Rejected Record Counts

For batches that proceed through individual record validation, diagnostic reporting provides accepted and rejected record counts.

These counts describe the results of Schema Validation.

For example, consider a batch containing five inventory records:

- Three records pass validation.
- Two records fail validation.

The diagnostic counts are:

| Measure | Count |
|---|---:|
| Submitted inventory records | 5 |
| Accepted records | 3 |
| Rejected records | 2 |

The batch's record-processing outcome is:

`PARTIALLY_ACCEPTED`

The three accepted records remain eligible for Transformation.

The two rejected records do not proceed to Transformation.

When every record passes validation, the diagnostic category is `ALL_RECORDS_ACCEPTED`.

When every record fails individual record validation, the diagnostic category is `NO_VALID_RECORDS`.

For batches rejected at the batch level, individual record acceptance and rejection counts are not assumed to have been evaluated.

Diagnostic reporting must not misrepresent an unevaluated individual record-validation result as a completed validation outcome.

## Dataset Version Creation Reporting

Diagnostic reporting includes the result of Dataset Versioning.

A dataset version candidate is created when an eligible batch produces at least one transformed inventory record.

Relevant reporting information includes:

- Whether a dataset version was created.
- The originating batch and source context.
- The created version's identifier, when applicable.
- The version's processing and verification status information.

When a dataset version is created, its initial status is:

`PENDING_VERIFICATION`

The corresponding diagnostic reporting category is:

`VERSION_PENDING`

A partially accepted batch can produce a dataset version candidate containing its transformed accepted records.

For example, a batch containing three accepted records and two rejected records may produce a dataset version containing three transformed records.

Diagnostic reporting can describe both the batch's partial acceptance and the resulting dataset version creation.

If no transformed records are available, Dataset Versioning creates no version candidate.

In that situation, diagnostic reporting must not claim that a dataset version was created.

No dataset version identifier or verification status is applicable when no version exists.

## Verification Failure Diagnostics

Output Verification evaluates created dataset versions against established consistency requirements.

The verification requirements are designated `VERF-01` through `VERF-08` and are defined in the Output Verification documentation.

A dataset version receives `VERIFIED` when all applicable checks pass.

The corresponding diagnostic reporting category is:

`VERSION_VERIFIED`

A dataset version receives `FAILED_VERIFICATION` when one or more applicable checks fail.

The corresponding diagnostic reporting category is:

`VERSION_FAILED`

Diagnostic reporting must provide traceable information about failed verification checks.

Relevant information includes:

- The affected dataset version.
- The verification failure outcome.
- The applicable failed verification requirement or requirements.
- Details sufficient to describe the detected inconsistency.

For example, suppose a dataset version declares a `record_count` of five but contains only four transformed records.

Output Verification detects the inconsistency under its record-count requirements.

The dataset version receives `FAILED_VERIFICATION`.

Diagnostic reporting identifies the failed verification outcome and the associated record-count inconsistency.

Diagnostics does not correct the count or modify the dataset contents.

## Diagnostic Traceability and Non-Mutation

Diagnostic information must remain associated with the relevant batch, record, or dataset version to the extent supported by the processing information available.

Traceability connects reported outcomes to the processing components responsible for those outcomes.

For example:

- Schema Validation determines whether an individual record is accepted or rejected.
- Transformation processes accepted records.
- Dataset Versioning determines whether a version candidate is created.
- Output Verification determines whether a created version passes verification.
- Diagnostics reports the corresponding results.

Diagnostic reporting is non-mutating.

It does not:

- Change batch-level validation decisions.
- Change record-level acceptance or rejection decisions.
- Add rejected records to transformation outputs.
- Modify immutable dataset records.
- Change the verification result determined by Output Verification.

The diagnostic requirements establish the information that must be reported, but do not prescribe a specific logging framework, database implementation, serialization format, or reporting interface.

Unexpected internal failure recovery remains outside the initial BDPP scenario scope.

## Relationship to Other Processing Components

Diagnostics depends on information established by earlier processing components.

Batch Ingestion provides the submitted input context.

Schema Validation establishes batch and record acceptance outcomes.

Transformation produces standardized inventory records from accepted inputs.

Dataset Versioning establishes dataset version creation results and version identity.

Output Verification determines whether created versions satisfy the output requirements.

Diagnostics consolidates and reports these outcomes while preserving their established meanings.

In particular, Diagnostics does not duplicate the responsibilities of Schema Validation or Output Verification.

Its responsibility is to provide clear, traceable descriptions of processing outcomes without modifying the underlying results.

This separation allows BDPP to distinguish processing decisions from the reporting of those decisions.