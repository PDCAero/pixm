# Known defects

Verified against the schema and examples on 2026-11-19. Fixed as a dedicated
task (CLAUDE.md §4.3); remove each item when fixed and log it in `CHANGELOG.md`.

## Schema (`known-defects` branch)
| # | Defect | Where | Needs CCB? |
|---|---|---|---|
| S1 | AIXM 5.1.1 imported for one type only; replace with a PIXM reference type and remove the import | `PIXM_Features`, property `aixmRunway` | Structure (open.md #6) |
| S3 | Naming mismatch: feature `ContaminationDefinition` has time slice `ContaminationTimeSlice` (pattern expects `ContaminationDefinitionTimeSlice`) | `PIXM_Features` | Yes (which name to keep) |
| S4 | Top-level element `PerformanceProfile` has no `substitutionGroup` | `PIXM_Features` | No |
| S5 | Property names starting with a capital: `V1VRChoice`, `V1VRRangeLimitChoice`, `V2VSChoice`, `V2VSRatio`, `V2VSValue`, `VerticalStructureTimeSlice`, `ClimbGradientComplianceCheck`, `VAppIncrements` | `PIXM_Features` | Casing of V-speed terms (open.md #3) |
| S6 | `uom` optional on all 14 measure types that have one; must be required | `PIXM_Measures` | No (decided, DEC-0001 #16) |
| S7 | No `uom` on `ValSlopeType`, `ValMagneticVariationType`, `ValMagneticVariationChangeType`, `ValRunwayEntryAngleType`; add (slope: new `UomSlopeType` with `PERCENT`; others: `UomAngleType`) | `PIXM_Measures`, `PIXM_UoM` | No (decided) |
| S8 | Dimensionless measures lack definitions stating "dimensionless" and range: `ValMuType`, `ValFrictionType`, `ValPCNType`, `ValPercentType` | `PIXM_Measures` | No |
| S9 | `ValFrictionType` and `ValMuType` may duplicate each other | `PIXM_Measures` | Yes, if merging |
| S10 | XSD primitives used directly on properties (94 uses, e.g. `takeoffRequestId` as `xs:string`) | `PIXM_Features` | Per case if type meaning changes |
| S11 | Property elements without explicit `minOccurs`/`maxOccurs` (89 lint warnings) | `PIXM_Features`, `PIXM_AbstractGML_ObjectTypes`, `PIXM_DataTypes` | No |
| S12 | Documentation largely absent (1,627 `DOC` lint warnings) | all | No (fix on touch; bulk pass optional) |
| S13 | Feature types named `…Extension` that are not extensions | `AircraftConfigurationExtension`, `LandingAircraftConfigurationExtension` | Yes (open.md #7) |
| S14 | 69 properties mandatory (`minOccurs="1"`) against the optional-by-default principle | `PIXM_Features` | Yes (open.md #8) |

## Examples (`known-defects` branch)
| # | Defect | Where |
|---|---|---|
| E1 | 16 measure values without `uom` (`oeiASD`, `oeiTOD`, `oeiTOR`, `initialHalfWidth`, `maxHalfWidthAfterTurn`) | Example 1 response files; `zrh_phased_obstacles.xml` |
| E2 | Not well-formed: closing tag mismatch at line 111 | `examples/temporal_example.xml` |
| E3 | AIXM elements embedded directly in PIXM content (`aixm:runwayReferencePoint` etc.) | `pixm_departure_intersections.xml` |
| E4 | Headers lack the illustrative-data statement and PIXM version | all examples |
| E5 | Uses features `LandingExit` and `DepartureIntersection`, which do not exist in the schema | `examples/Example 3 - Landing Exits and Departure Ints/` |
| E6 | `gml:id` values contain colons (`urn:uuid:obs-…`); `gml:id` must be an NCName | Example 1 `takeoffRequest-28R_*.xml`, `takeoffRequest_01R_*.xml` |
| E7 | Feature properties placed directly on the feature (no time slice), and time slices / `obstacleSet` placed directly in `gml:featureMember` | `zrh_phased_obstacles.xml`; `obstacleSet` in Example 1 requests |
| E8 | Time slices have no `pixm:interpretation`, which the schema requires | all examples |
| E9 | All 20 examples fail validation (1,014 errors on 2026-11-20, after the time-slice fix let validation reach the content). About 750 are elements the schema does not define (e.g. `contextUsage`, `identifier`, `geometry`, `speedName`, `position`, `description`); about 120 are nested blocks in an older style (e.g. `aircraftConfigurationTimeSlice`); 75 are properties out of sequence order; the rest are E5–E8 and invalid values | `python tools/validate.py`; open.md #11 |
