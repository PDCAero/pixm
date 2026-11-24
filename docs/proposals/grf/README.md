# GRF runway condition reporting: prototype for CCB discussion

**Status: draft proposal, not normative.** Nothing here is part of PIXM 0.5. It
shows one possible implementation of the concept mapping "PIXM Concept Mapping -
GRF" (candidate PIXM v1.0) so the CCB can see what it would look like in XML.

The GRF model is an **alternative to**, not a replacement for, the existing
SCAP-equivalent `ContaminationDefinition`; it can be embedded in
`PerformanceRunway` or sent on its own.

## Files
| File | Contents |
|---|---|
| `PIXM_GRF_Proposal.xsd` | Draft schema: includes PIXM 0.5 and adds the GRF types. Uses `xs:redefine` only to show the new `PerformanceRunway` property; a real implementation would edit `PIXM_Features.xsd`. |
| `examples/grfRunwayConditionNotification-LSZH-28.xml` | A GRF report sent on its own (RWYCC 5/5/3). |
| `examples/performanceRunway-LSZH-28-SCAP-and-GRF.xml` | Both contamination models side by side on one performance runway. |
| `examples/runwayContaminationClearanceRequest-LSZH-28.xml` | An aircraft operator asks the aerodrome for at least RWYCC 5 and 45 m cleared width by 07:30 UTC. |

`tools/validate.py` does not check this folder. To validate by hand (from `tools/`):

    python -c "import xmlschema,schema_cache,glob; s=xmlschema.XMLSchema('../docs/proposals/grf/PIXM_GRF_Proposal.xsd',uri_mapper=schema_cache.uri_mapper); [print(p, s.is_valid(p)) for p in glob.glob('../docs/proposals/grf/examples/*.xml')]"

All three examples were valid on 2026-11-23.

## From the concept mapping to the prototype
| Concept mapping | Prototype | Notes |
|---|---|---|
| `BasicContaminationDefinition` (yellow) | existing `ContaminationDefinition`, unchanged | See question B8. |
| `GRFContaminationDefinition` (base class) | `GRFRunwayConditionReport` (report header) | Report-level fields (`observationTime`, `rcamVersionReference`) appear once; the report also carries `aerodromeDesignator` and `runwayDirectionDesignator`. |
| `RunwaySectionContamination` | `RunwaySectionContamination` (0..3 per report) | `section` (thirds), `runwayConditionCode`, `contaminant`, `depth`, `proportion`. |
| `RunwayContamination` | `RunwayContamination` (0..1 per report) | Cleared dimensions, ridges, further clearance; `clearedWidth` appears once. |
| `Ridge` (AIXM) | `Ridge` (PIXM block) | `side`, `distanceFromCenterline`, `height` (AIXM calls it `depth`). |
| `SurfaceContaminationLayer` (AIXM) | not used | GRF combined descriptors instead (question B3). |
| `frictionCoefficient` | not used | Question B5. |
| `PerformanceRunway.contamDefinition` | unchanged | |
| `grfOveralContamDefinition` + `grfAreaContamDefinition` | one property `grfRunwayConditionReport` | Question B1. |
| `RunwayContamClearanceRequest` | `RunwayContaminationClearanceRequest` | Built on `AbstractPIXMRequest`: `requestID`, `requesterID`, `timestamp` become the inherited `requestId`, `requesterId`, `requestTimestamp`; `airportID` becomes `aerodromeDesignator`. |
| `MinimumRunwayClearance` | `MinimumRunwayClearance` | `runwayEndId` becomes `runwayDirectionDesignator`; `minClearedWidth` becomes `minimumClearedWidth`. |

## Decided for the prototype (CCB, 2026-11-23)
- **A1 Naming:** `contam` is written `contamination`; `GRF` and `RCAM` stay abbreviated as accepted performance terms (glossary).
- **A2 Clearance request:** a request from an aircraft operator to an aerodrome to bring a runway to a minimum state; it inherits from the PIXM request base, with related fields renamed to match.
- **A3 Types:** existing PIXM types reused (`ValDepthType`, `ValPercentType`, `ValDistanceType`, `CodeRunwaySideType`, `DateTimeType`, `CodeYesNoType`, designator types).
- **A4:** `clearedWidth` appears once, on the whole-runway part.
- **A5:** runway sections are a closed list of thirds (FIRST, SECOND, THIRD) numbered from the threshold of the runway direction in use.
- **A6:** `Ridge` adapted as a PIXM block with `side`, `distanceFromCenterline`, `height`.

## Proposals for the CCB (shown in the prototype, not decided)
| # | Question | What the prototype does |
|---|---|---|
| B1 | Where GRF lives | One `GRFRunwayConditionReport` block, embedded in `PerformanceRunway` by one property and also sent alone as `GRFRunwayConditionNotification`. |
| B2 | Inheritance or composition | Composition: report header, whole-runway part, third sections. No base class. |
| B3 | Contaminant list | New closed `CodeGRFContaminant` with combined descriptors (e.g. `DRY_SNOW_ON_TOP_OF_ICE`); no layers. |
| B4 | RWYCC type | Closed codelist `CodeRunwayCondition` with literals 6 to 0, each defined. |
| B5 | Friction and braking action | Neither included in the GRF report. |
| B6 | SNOWTAM-era fields | `furtherClearanceTime`, `furtherTotalClearance`, `nextObservationTime`, `clearedLengthBegin` kept, for AIXM alignment. |
| B7 | Clearance request | No response message; any number (0..*) of runway entries; minimum RWYCC applies to every third. |
| B8 | GRF alongside SCAP | Both allowed on the same runway, both optional. |
| B9 | `rcamVersionReference` | A designator (e.g. `DOC9981-2020`); content to be agreed. |

Other open points:
- GRF situational awareness items (reduced runway length, drifting snow, loose sand, chemical treatment, taxiway and apron conditions) are not modeled. In scope?
- Is renaming `ContaminationDefinition` to `BasicContaminationDefinition` intended?
- The old model's `rcrValue` (a runway condition reading) could be confused with GRF's RCR (runway condition report).

## To verify before implementation
Marked `TODO(VERIFY)` in the draft; written from memory, to be checked against
ICAO PANS-AD (Doc 9981):
- RWYCC meanings (associated braking action for 6 to 0).
- The GRF contaminant list and which contaminants have a reported depth.
- Coverage steps (25, 50, 75, 100 percent).
- Whether AIXM 5.2 already models GRF (its schema was not found at `https://aixm.aero/schema/5.2/`).
