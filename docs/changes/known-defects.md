# Known defects

Verified against the schema and examples on 2026-11-19. Fixed as a dedicated
task (CLAUDE.md §4.3); remove each item when fixed and log it in `CHANGELOG.md`.

## Handled by the layout move (`repo-layout-0.5` branch)
| # | Defect | Where |
|---|---|---|
| L1 | Namespace `…/schema/0.1` to change to `…/schema/0.5` (schema and all examples) | all schema files, examples |
| L2 | Example 3 files use a different namespace, `http://www.pixm.aero/pixm/1.0` | `pixm_landing_exits.xml`, `pixm_departure_intersections.xml` |
| L3 | Example `schemaLocation`s point to `PIXM_Features.XSD` as if in the same folder; one uses a local GML path | all examples |
| L4 | Folder name contains `&` | `examples/Example 3 - Landing Exits & Departure Ints` |
| L5 | Feature file has an upper-case extension | `PIXM_Features.XSD` → `PIXM_Features.xsd` |
| L6 | README refers to `schemas/` instead of `schema/` | `README.md` |

## Schema (`known-defects` branch)
| # | Defect | Where | Needs CCB? |
|---|---|---|---|
| S1 | AIXM 5.1.1 imported (via a path outside the repo) for one type only; replace with a PIXM reference type and remove the import | `PIXM_Features`, property `aixmRunway` | Structure (open.md #6) |
| S2 | Abstract time-slice element named `AbstractPIXMTimeSliceType` (element with `Type` suffix); referenced by all 61 time-slice `substitutionGroup`s | `PIXM_AbstractGML_ObjectTypes`, `PIXM_Features` | No (0.x rename) |
| S3 | `Contamination` has a time-slice type but no feature type | `PIXM_Features` | Yes |
| S4 | Top-level element `PerformanceProfile` has no `substitutionGroup` | `PIXM_Features` | No |
| S5 | Property names starting with a capital: `V1VRChoice`, `V1VRRangeLimitChoice`, `V2VSChoice`, `V2VSRatio`, `V2VSValue`, `VerticalStructureTimeSlice`, `ClimbGradientComplianceCheck`, `VAppIncrements` | `PIXM_Features` | Casing of V-speed terms (open.md #3) |
| S6 | `uom` optional on all 14 measure types that have one; must be required | `PIXM_Measures` | No (decided, DEC-0001 #16) |
| S7 | No `uom` on `ValSlopeType`, `ValMagneticVariationType`, `ValMagneticVariationChangeType`, `ValRunwayEntryAngleType`; add (slope: new `UomSlopeType` with `PERCENT`; others: `UomAngleType`) | `PIXM_Measures`, `PIXM_UoM` | No (decided) |
| S8 | Dimensionless measures lack definitions stating "dimensionless" and range: `ValMuType`, `ValFrictionType`, `ValPCNType`, `ValPercentType` | `PIXM_Measures` | No |
| S9 | `ValFrictionType` and `ValMuType` may duplicate each other | `PIXM_Measures` | Yes, if merging |
| S10 | XSD primitives used directly on properties (94 uses, e.g. `takeoffRequestId` as `xs:string`) | `PIXM_Features` | Per case if type meaning changes |
| S11 | Property elements without explicit `minOccurs`/`maxOccurs` (74, mostly `timeSlice`) | `PIXM_Features` | No |
| S12 | Documentation almost absent (6 `xs:documentation` across all files) | all | No (fix on touch; bulk pass optional) |
| S13 | Feature types named `…Extension` that are not extensions | `AircraftConfigurationExtension`, `LandingAircraftConfigurationExtension` | Yes (open.md #7) |
| S14 | 69 properties mandatory (`minOccurs="1"`) against the optional-by-default principle | `PIXM_Features` | Yes (open.md #8) |

## Examples (`known-defects` branch)
| # | Defect | Where |
|---|---|---|
| E1 | 16 measure values without `uom` (`oeiASD`, `oeiTOD`, `oeiTOR`, `initialHalfWidth`, `maxHalfWidthAfterTurn`) | Example 1 response files; `zrh_phased_obstacles.xml` |
| E2 | Not well-formed: closing tag mismatch at line 111 | `examples/temporal_example.xml` |
| E3 | AIXM elements embedded directly in PIXM content (`aixm:runwayReferencePoint` etc.) | `pixm_departure_intersections.xml` |
| E4 | Headers lack the illustrative-data statement and PIXM version | all examples |
