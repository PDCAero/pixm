# DEC-0002: Validation baseline holds lint warnings only

- Date: 2026-11-20
- Status: Decided
- Affected elements: `tools/validate.py`, `tools/lint-baseline.json`

## Context
The first full validation run found 2,004 lint warnings and 523 errors; every
example fails validation (known defects S15, E2, E5–E9). The baseline lets a run
pass while known legacy issues remain, failing only on new ones.

## Options considered
- Baseline both warnings and example errors, so validation passes until a change
  adds anything new.
- Baseline lint warnings only; errors always fail.

## Decision
Only lint warnings are recorded in the baseline. Errors (schema compilation,
well-formedness, example validity) are never baselined and always fail the run.

## Rationale
Invalid examples are real defects, not legacy style issues; they must stay
visible as failures until fixed by the known-defects work.
