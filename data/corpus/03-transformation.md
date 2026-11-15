# Batch Data Processing Platform — Transformation

## Transformation Purpose and Inputs

The Transformation component of the Batch Data Processing Platform (BDPP) converts validated equipment inventory records into standardized output records.

Transformation occurs after Schema Validation and before Dataset Versioning.

Its purpose is to preserve accepted inventory information while applying deterministic processing rules that produce consistent outputs for downstream dataset creation and verification.

Transformation does not independently determine whether an input record is valid. It relies on the acceptance decisions established by Schema Validation.

## Eligible Records

Only inventory records accepted during Schema Validation are eligible for transformation.

A batch may contain both accepted and rejected records. When this occurs, Transformation processes the accepted records without reintroducing rejected records.

The following requirements apply:

- Every transformed record must originate from an accepted input record.
- Rejected input records must not appear in transformation outputs.
- Accepted-record ordering must be preserved.
- Transformation must not change the preceding validation decisions.

If a batch has no accepted records, there are no inventory records eligible for transformation.

Dataset Versioning separately determines whether the resulting output qualifies for creation of a dataset version.

## Inventory Field Preservation

Transformation preserves the validated inventory information associated with each accepted record.

The input inventory fields are:

| Field | Transformation responsibility |
|---|---|
| `equipment_id` | Preserve the validated equipment identifier |
| `category` | Preserve the validated equipment category |
| `quantity` | Preserve the validated quantity |
| `condition_code` | Preserve the validated condition code |
| `updated_at` | Normalize the timestamp to UTC while retaining its represented instant |

The transformation process does not redefine the meanings of inventory categories, condition codes, or quantities.

Transformation additionally derives `available_quantity` according to the established business rule.

The result is a standardized representation of an accepted inventory record.

## Timestamp Normalization

The input `updated_at` field represents the timestamp associated with an inventory record's update. The standardized output field is `updated_at_utc`.

Input validation requires a valid ISO 8601 timestamp containing an explicit UTC offset.

Transformation normalizes accepted `updated_at` timestamps to UTC.

Normalization preserves the instant represented by the original timestamp while expressing that instant in UTC.

For example:

- Input timestamp: `2026-11-12T08:30:00-06:00`
- Equivalent normalized timestamp: `2026-11-12T14:30:00Z`

These timestamps represent the same instant.

The original offset must not be interpreted as a change in the actual update time.

Timestamp normalization applies to accepted inventory records. It does not authorize otherwise invalid timestamp values to bypass Schema Validation.

## Derived Available Quantity

Transformation derives the field `available_quantity` from the validated `quantity` and `condition_code` values.

The calculation follows these rules:

1. When `condition_code` is `AVAILABLE`, `available_quantity` equals `quantity`.
2. When `condition_code` is `MAINTENANCE`, `available_quantity` equals zero.
3. When `condition_code` is `RETIRED`, `available_quantity` equals zero.

The resulting value indicates the quantity represented by the record that is considered available for lending.

### Illustrative examples

| `quantity` | `condition_code` | `available_quantity` |
|---:|---|---:|
| 5 | `AVAILABLE` | 5 |
| 3 | `MAINTENANCE` | 0 |
| 8 | `RETIRED` | 0 |
| 0 | `AVAILABLE` | 0 |

The calculation does not modify the original validated `quantity`.

For example, a maintenance record with `quantity` equal to 3 retains that quantity, even though its derived `available_quantity` equals zero.

The derived value is deterministic: the same valid quantity and condition code always produce the same available quantity.

## Record Ordering and Lineage

Transformation preserves the ordering of accepted records.

If accepted records appear in a particular sequence within the submitted batch, their transformed outputs retain that relative order.

Rejected records are excluded without changing the relative order of the remaining accepted records.

Each transformed output record includes `batch_id` and `source_id` to preserve the originating batch and source.

Relevant lineage information includes:

- `batch_id`: identifies the originating inventory batch.
- `source_id`: identifies the originating source.

Preserving this relationship allows downstream components to associate transformed inventory information with its input context.

Dataset Versioning is responsible for retaining the appropriate batch/source information in dataset version metadata.

Transformation does not independently create dataset version identifiers.

## Transformation Output Guarantees

Successful transformation of accepted records produces standardized inventory information with the following properties:

1. Every output record corresponds to an accepted input record.
2. Validated inventory values remain preserved, except for the specified timestamp representation normalization.
3. Record update timestamps represent the correct instants in UTC.
4. `available_quantity` follows the established condition-based calculation.
5. Batch/source lineage remains available.
6. Accepted-record ordering is preserved.
7. Rejected records are excluded.

Transformation does not determine whether a resulting dataset version satisfies output verification requirements.

Output Verification independently checks the relevant consistency properties after a dataset version candidate has been created.

Transformation also does not modify diagnostic reporting outcomes or establish policies for unexpected internal failure recovery.

These responsibilities remain outside the Transformation component's defined scope.