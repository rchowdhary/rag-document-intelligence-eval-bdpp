# Batch Data Processing Platform — Output Verification

## Output Verification Purpose

The Output Verification component of the Batch Data Processing Platform (BDPP) evaluates created dataset versions against established output consistency requirements.

Output Verification operates after Dataset Versioning has created a dataset version candidate.

Its responsibilities include checking required version metadata, record counts, standardized record fields, normalized timestamps, derived quantities, batch/source lineage, and correspondence with accepted input records.

Output Verification determines whether a dataset version satisfies the applicable requirements without modifying its immutable dataset records.

## Verification Inputs and Preconditions

Output Verification receives a dataset version candidate created by Dataset Versioning.

Each eligible candidate begins with the status `PENDING_VERIFICATION`.

The dataset version contains:

- `version_id`
- `batch_id`
- `source_id`
- `created_at`
- `record_count`
- `status`
- `records`

The `records` collection contains the transformed inventory records associated with the originating batch.

Verification also requires access to the accepted input records and their validation outcomes when evaluating correspondence between the accepted inputs and transformed outputs.

The specification requires this comparison information to be available but does not prescribe its storage or retrieval implementation.

A batch producing zero transformed records does not create a dataset version candidate. Consequently, there is no dataset version to verify in that situation.

## Version Metadata Checks

### VERF-01 — Required Version Metadata

A dataset version must contain the required metadata established by Dataset Versioning.

Verification checks the presence and validity of the required version information, including:

- A unique `version_id`.
- The originating `batch_id`.
- The originating `source_id`.
- A valid UTC `created_at` timestamp.
- A declared `record_count`.
- A recognized version `status`.
- The associated `records` collection.

The version identifier must distinguish the candidate from other dataset versions.

The batch and source identifiers establish the version's originating inventory submission.

A dataset version with missing or invalid required metadata fails the applicable metadata verification check.

## Record Count and Field Checks

### VERF-02 — Record Count Consistency

The declared `record_count` must equal the number of transformed records contained in the dataset version.

For example, if a dataset version contains four transformed records, its declared `record_count` must equal four.

A version declaring five records while containing only four fails verification.

The declared count must reflect the version's actual transformed records rather than the total number of records originally submitted.

Rejected input records are not counted as transformed dataset records.

### VERF-03 — Required Standardized Output Fields

Every transformed inventory record must contain the standardized fields established by Transformation.

These fields are:

| Field | Purpose |
|---|---|
| `equipment_id` | Validated equipment identifier |
| `category` | Validated equipment category |
| `quantity` | Validated equipment quantity |
| `condition_code` | Validated equipment condition |
| `updated_at_utc` | Update timestamp normalized to UTC |
| `available_quantity` | Derived available inventory quantity |
| `batch_id` | Originating batch identifier |
| `source_id` | Originating source identifier |

A dataset version fails the applicable field check if a transformed record lacks a required standardized field.

The validation of accepted input values remains the responsibility of Schema Validation. Output Verification checks whether the established transformed-record structure is present and consistent.

## Timestamp and Derived Value Checks

### VERF-04 — Normalized UTC Timestamps

The `updated_at_utc` field in each transformed record must contain a valid UTC timestamp.

The standardized timestamp representation uses the UTC `Z` designation and preserves applicable fractional-second precision.

For example, an accepted input timestamp of:

`2026-11-12T08:30:00-06:00`

represents the same instant as the normalized output:

`2026-11-12T14:30:00Z`

Verification checks that the output timestamp is valid and correctly normalized while preserving the represented instant.

An incorrectly converted or invalid UTC timestamp fails the applicable verification check.

### VERF-05 — Derived Available Quantity

The transformed `available_quantity` must match the deterministic calculation established by Transformation.

The required behavior is:

- If `condition_code` is `AVAILABLE`, `available_quantity` equals `quantity`.
- If `condition_code` is `MAINTENANCE`, `available_quantity` equals zero.
- If `condition_code` is `RETIRED`, `available_quantity` equals zero.

For example, a transformed record with `quantity` equal to 6 and `condition_code` equal to `MAINTENANCE` must have `available_quantity` equal to zero.

The validated `quantity` remains 6.

If the output contains an incorrectly derived `available_quantity`, the dataset version fails this verification check.

Output Verification evaluates the derived result but does not modify it.

## Lineage and Record Correspondence Checks

### VERF-06 — Batch and Source Lineage

Every transformed inventory record must retain the originating batch and source identifiers.

The record-level `batch_id` and `source_id` values must match the corresponding identifiers in the dataset version metadata.

This ensures that records in a dataset version are associated with the version's originating inventory batch.

A record containing inconsistent batch/source identifiers fails the lineage verification check.

### VERF-07 — Accepted-Record Correspondence, Value Preservation, and Ordering

Every transformed output record must correspond to an inventory record accepted during Schema Validation.

Verification must establish that:

1. Each accepted input record has one corresponding transformed output record.
2. Rejected input records do not appear in the output.
3. Accepted records are not silently omitted.
4. Accepted records are not duplicated during transformation.
5. Required original inventory values are preserved, subject to the specified timestamp normalization.
6. The relative ordering of accepted records is preserved.

For example, consider an input batch containing four records in the following order:

- Record A — accepted
- Record B — rejected
- Record C — accepted
- Record D — accepted

The resulting transformed records must correspond to A, C, and D, in that relative order.

Record B must not appear in the transformed dataset.

Verification compares the transformed output against the accepted input records and their validation outcomes.

The comparison concerns record correspondence and transformation preservation. It does not introduce a new requirement that equipment identifiers be globally unique.

## Verification Outcomes

### VERF-08 — Final Verification Status

Output Verification determines a dataset version's final status from the results of the applicable verification checks.

A newly created dataset version begins with:

`PENDING_VERIFICATION`

After verification, the version transitions to one of two final statuses.

**VERIFIED**

The dataset version receives `VERIFIED` only when all applicable verification requirements pass.

**FAILED_VERIFICATION**

The dataset version receives `FAILED_VERIFICATION` when one or more applicable verification requirements fail.

The permitted transitions are:

- `PENDING_VERIFICATION` → `VERIFIED`
- `PENDING_VERIFICATION` → `FAILED_VERIFICATION`

The final status reflects the verification decision.

The initial BDPP design does not define automatic verification retries, additional status transitions, or a remediation workflow.

## Verification and Dataset Immutability

Output Verification must not modify the immutable dataset records belonging to a created version.

This restriction applies regardless of whether verification succeeds or fails.

Verification may determine and update the version's administrative status without changing its dataset contents.

If a dataset version fails verification, its stored records remain unchanged.

The verification failure can be reported by the Diagnostics and Processing Outcome Reporting component.

This preserves the distinction between evaluating dataset correctness and altering dataset contents.

## Relationship to Other Processing Components

Output Verification depends on requirements established by earlier BDPP components.

Schema Validation establishes which input records are accepted.

Transformation establishes standardized record values, UTC timestamp normalization, derived available quantities, record ordering, and lineage preservation.

Dataset Versioning creates the identifiable, immutable dataset version candidate.

Output Verification evaluates the candidate against these requirements and determines the final verification status.

Diagnostics and Processing Outcome Reporting provides information about verification results and failures.

Output Verification does not redefine input validation rules, transformation behavior, version creation eligibility, or diagnostic reporting categories.

These responsibilities remain assigned to their respective components.