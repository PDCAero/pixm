# DEC-0003: AIXM time-slice structure

- Date: 2026-11-20
- Status: Decided
- Affected elements: all 61 features in `PIXM_Features`; `AbstractPIXMTimeSlice` in `PIXM_AbstractGML_ObjectTypes`

## Context
PIXM features typed their `timeSlice` property directly as the time-slice type.
AIXM 5.1.1, which PIXM follows (DEC-0001), and all existing examples use a
property type that wraps a named time-slice element, following the GML
object/property alternation. The mismatch made every example invalid.

## Options considered
- Add AIXM-style `…TimeSlicePropertyType` wrappers to the schema.
- Keep the schema and remove the wrapper from every example.

## Decision
Add the wrappers to the schema. Each feature `X` gets `XTimeSlicePropertyType`
containing one `XTimeSlice`; `timeSlice` uses that type. The abstract time-slice
element is renamed `AbstractPIXMTimeSlice` and joins the `gml:AbstractTimeSlice`
substitution group.

## Rationale
Matches AIXM 5.1.1 and GML encoding conventions, so AIXM/GML-aware software and
the existing examples' structure work as expected.
