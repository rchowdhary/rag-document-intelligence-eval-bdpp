# Batch Data Processing Platform — Ingestion and Validation

## Input Format and Batch Structure

The Batch Data Processing Platform (BDPP) receives synthetic equipment inventory information as structured JSON batches.

Each batch contains identifying metadata and an array of inventory records. The ingestion and validation components establish whether the submitted information satisfies the platform's input requirements.

Ingestion is responsible for receiving submitted batches. Schema Validation evaluates the batch structure and individual inventory records.

The initial supported input schema version is `1.0`.

## Inventory Batch Fields

Each Inventory Batch contains five required fields.

| Field | Description |
|---|---|
| `batch_id` | Identifier associated with the submitted inventory batch |
| `source_id` | Identifier of the inventory batch's source |
| `submitted_at` | Timestamp representing when the batch was submitted |
| `schema_version` | Version of the input schema used by the batch |
| `records` | Array of inventory records submitted for processing |

The `batch_id` and `source_id` values must be nonempty strings.

The `submitted_at` field must contain a valid ISO 8601 timestamp with an explicit UTC offset.

The `schema_version` field must identify a supported input schema version. Initially, BDPP supports `1.0`.

The `records` field must contain a nonempty array.

## Inventory Record Fields

Each inventory record contains five required fields.

| Field | Description |
|---|---|
| `equipment_id` | Identifier of the equipment represented by the record |
| `category` | Equipment category |
| `quantity` | Recorded equipment quantity |
| `condition_code` | Recorded equipment condition |
| `updated_at` | Timestamp associated with the inventory record's update |

The `equipment_id` value must be a nonempty string.

The supported equipment categories are:

- `LAPTOP`
- `MONITOR`
- `PROJECTOR`

The supported condition codes are:

- `AVAILABLE`
- `MAINTENANCE`
- `RETIRED`

The `quantity` field must contain a nonnegative integer. Boolean values are not valid quantities, even in programming environments where booleans can behave as integers.

The `updated_at` field must contain a valid ISO 8601 timestamp with an explicit UTC offset.

## Batch Ingestion Responsibilities

Batch Ingestion receives submitted inventory data and establishes the input available for validation.

The accepted ingestion requirements are designated `ING-01` through `ING-05`.

Together, these requirements establish that:

1. The submitted input is a structured JSON inventory batch.
2. The batch envelope contains the required batch-level fields.
3. Inventory records are supplied through the `records` array.
4. The submitted batch identifier is associated with processing information when available.
5. A submission whose batch envelope cannot be interpreted sufficiently for processing is rejected rather than forwarded as valid input.

Ingestion does not independently determine whether individual inventory records satisfy their schema constraints.

That responsibility belongs to Schema Validation.

## Schema Validation Rules

Schema Validation applies requirements at two levels:

- Batch-level validation determines whether the submitted batch is eligible for individual record processing.
- Record-level validation determines which inventory records within an eligible batch are accepted or rejected.

These levels have different rejection consequences.

### Batch-level validation

The accepted batch-level rules are designated `VAL-B01` through `VAL-B05`.

| Rule | Requirement |
|---|---|
| `VAL-B01` | `batch_id` must be a nonempty string |
| `VAL-B02` | `source_id` must be a nonempty string |
| `VAL-B03` | `submitted_at` must be a valid ISO 8601 timestamp with an explicit UTC offset |
| `VAL-B04` | `schema_version` must identify a supported version, initially `1.0` |
| `VAL-B05` | `records` must be a nonempty array |

All required batch-level fields must be present.

A batch failing any applicable batch-level requirement is rejected as a whole.

### Record-level validation

The accepted record-level rules are designated `VAL-R01` through `VAL-R06`.

| Rule | Requirement |
|---|---|
| `VAL-R01` | `equipment_id` must be a nonempty string |
| `VAL-R02` | `category` must identify a supported equipment category |
| `VAL-R03` | `quantity` must be a nonnegative integer, excluding Boolean values |
| `VAL-R04` | `condition_code` must identify a supported condition code |
| `VAL-R05` | `updated_at` must be a valid ISO 8601 timestamp with an explicit UTC offset |
| `VAL-R06` | All five required inventory record fields must be present |

Record-level validation is performed only when the containing batch satisfies batch-level validation.

Each inventory record is evaluated independently against its applicable requirements.

## Batch-Level Rejection

A batch-level validation failure rejects the entire batch.

When batch-level validation fails:

- The batch is classified as rejected.
- Its inventory records do not proceed through individual record acceptance and transformation.
- No dataset version is created from that rejected batch.

A batch cannot become partially accepted when the batch itself fails the required batch-level validation checks.

Batch rejection information is made available for diagnostic reporting.

## Record-Level Rejection and Partial Acceptance

When a batch passes batch-level validation, BDPP evaluates its inventory records individually.

A record satisfying all applicable record-level requirements is accepted.

A record failing one or more applicable requirements is rejected.

Rejecting one record does not automatically reject other records within the same valid batch.

This supports three relevant record-processing situations:

**All records accepted**

Every submitted inventory record satisfies the applicable record-level requirements.

**Partially accepted batch**

At least one inventory record is accepted and at least one is rejected.

Accepted records remain eligible for downstream transformation. Rejected records do not proceed.

**No valid records**

The batch passes batch-level validation, but none of its inventory records satisfy the record-level requirements.

No records are eligible for transformation in this situation.

These distinctions allow BDPP to retain valid input data without treating every record-level validation failure as a failure of the entire batch.

## Validation Results and Downstream Eligibility

Validation establishes which records can enter the Transformation component.

The relevant validation results are:

- Batch rejected
- Record accepted
- Record rejected

Only accepted inventory records are eligible for transformation.

A partially accepted batch may produce transformed records and subsequently create a dataset version candidate.

If no records are accepted, no transformed inventory records are produced and no dataset version is created.

Validation rejection details and accepted/rejected record counts are available to the Diagnostics and Processing Outcome Reporting component.

Validation does not determine whether a subsequently created dataset version satisfies output verification requirements.

That determination belongs to Output Verification.

The initial ingestion and validation specification does not introduce additional policies for duplicate equipment identifiers, unspecified input fields, timestamp relationships between records, or unexpected internal failure recovery. These topics are not assigned new behavior by this document.