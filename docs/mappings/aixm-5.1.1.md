# Mapping: PIXM 0.5 ↔ AIXM 5.1.1

Procedure: `docs/process/traceability.md` §2. Source element paths verified
against the AIXM 5.1.1 XSD (`https://aixm.aero/schema/5.1.1/`) on 2026-11-21.
PIXM does not import these AIXM types; it adapts them (DEC-0001, DEC-0004, DEC-0005).

## Designators (DEC-0004)
| PIXM element | Source element path | Relationship | Notes | Decision |
|---|---|---|---|---|
| `pixm:CodeAirportHeliportDesignatorType` | `aixm:CodeAirportHeliportDesignatorType` | equivalent | Same facets (3–6 upper-case letters or digits). | DEC-0004 |
| `pixm:…/aerodromeDesignator` | `aixm:AirportHeliportTimeSlice/aixm:designator` | equivalent | Carried as a designator, not a reference to the AIXM feature. | DEC-0004 |
| `pixm:…/runwayDirectionDesignator` | `aixm:RunwayDirectionTimeSlice/aixm:designator` | equivalent | `pixm:TextDesignatorType` has the same facets as `aixm:TextDesignatorType`. | DEC-0004 |

## Runway reference points (DEC-0005)
| PIXM element | Source element path | Relationship | Notes | Decision |
|---|---|---|---|---|
| `pixm:RunwayReferencePoint` | `aixm:RunwayCentrelinePoint` | partial | Embedded data block, not a feature; no `onRunway`, `associatedDeclaredDistance`, `navaidEquipment` or `annotation`. | DEC-0005 |
| `pixm:RunwayReferencePoint/designator` | `aixm:RunwayCentrelinePointTimeSlice/aixm:designator` | equivalent | | DEC-0005 |
| `pixm:RunwayReferencePoint/role` | `aixm:RunwayCentrelinePointTimeSlice/aixm:role` | broader | See codelist row. | DEC-0005 |
| `pixm:CodeRunwayPointRoleType` | `aixm:CodeRunwayPointRoleType` | broader | All 13 AIXM literals plus `END_ROLLOUT`; closed (no `OTHER`). | DEC-0005 |
| `pixm:RunwayReferencePoint/location` | `aixm:RunwayCentrelinePointTimeSlice/aixm:location` | partial | See `ElevatedPoint`. | DEC-0005 |
| `pixm:ElevatedPoint` | `aixm:ElevatedPoint` | partial | Data block with a `gml:Point` property instead of a `gml:PointType` subtype; no `geoidUndulation` or `verticalAccuracy`. | DEC-0005 |
| `pixm:ElevatedPoint/elevation` | `aixm:ElevatedPoint/aixm:elevation` | equivalent | | DEC-0005 |
| `pixm:ElevatedPoint/verticalDatum` | `aixm:ElevatedPoint/aixm:verticalDatum` | equivalent | | DEC-0005 |
| `pixm:CodeVerticalDatumType` | `aixm:CodeVerticalDatumType` | equivalent | Same literals and `OTHER` pattern (CCB exception). | DEC-0005 |

## Declared distances (DEC-0005)
| PIXM element | Source element path | Relationship | Notes | Decision |
|---|---|---|---|---|
| `pixm:DeclaredDistances` | `aixm:RunwayDeclaredDistance` | partial | AIXM: one object per distance with `type` (`aixm:CodeDeclaredDistanceType`) and `declaredValue/distance`; PIXM: one block with four named distances, no accuracy. | DEC-0005 |
| `pixm:DeclaredDistances/takeoffRunAvailable` | `aixm:RunwayDeclaredDistance` with `type` = `TORA` | equivalent | | DEC-0005 |
| `pixm:DeclaredDistances/takeoffDistanceAvailable` | `aixm:RunwayDeclaredDistance` with `type` = `TODA` | equivalent | | DEC-0005 |
| `pixm:DeclaredDistances/accelerateStopDistanceAvailable` | `aixm:RunwayDeclaredDistance` with `type` = `ASDA` | equivalent | | DEC-0005 |
| `pixm:DeclaredDistances/landingDistanceAvailable` | `aixm:RunwayDeclaredDistance` with `type` = `LDA` | equivalent | | DEC-0005 |

## Bearing strength (DEC-0005)
| PIXM element | Source element path | Relationship | Notes | Decision |
|---|---|---|---|---|
| `pixm:BearingStrength` | `aixm:SurfaceCharacteristics` (PCN properties) | partial | PCN properties only; no composition, preparation, condition, LCN or SIWL. | DEC-0005 |
| `pixm:BearingStrength/pavementClassificationNumber` | `aixm:SurfaceCharacteristics/aixm:classPCN` | equivalent | | DEC-0005 |
| `pixm:BearingStrength/pavementType` | `aixm:SurfaceCharacteristics/aixm:pavementTypePCN` | equivalent | Reuses `pixm:CodePavementBehaviourType` (RIGID, FLEXIBLE = `aixm:CodePCNPavementType`). | DEC-0005 |
| `pixm:BearingStrength/subgradeCategory` | `aixm:SurfaceCharacteristics/aixm:pavementSubgradePCN` | equivalent | Reuses `pixm:CodePavementSubgradeType` (A–D = `aixm:CodePCNSubgradeType`). | DEC-0005 |
| `pixm:BearingStrength/maximumTirePressure` | `aixm:SurfaceCharacteristics/aixm:maxTyrePressurePCN` | equivalent | `pixm:CodeTirePressureCategoryType` = `aixm:CodePCNTyrePressureType` (W, X, Y, Z), closed. | DEC-0005 |
| `pixm:BearingStrength/evaluationMethod` | `aixm:SurfaceCharacteristics/aixm:evaluationMethodPCN` | equivalent | `pixm:CodePavementEvaluationMethodType` = `aixm:CodePCNMethodType` (TECH, ACFT), closed. | DEC-0005 |

## No AIXM equivalent
| PIXM element | Source element path | Relationship | Notes | Decision |
|---|---|---|---|---|
| `pixm:DepartureIntersection` | — | none | Nearest AIXM concepts: `aixm:RunwayCentrelinePoint` with role `START_RUN`, `aixm:TaxiHoldingPosition`. | DEC-0005 |
| `pixm:LandingExit` | — | none | Nearest AIXM concept: `aixm:RunwayCentrelinePoint`; no exit role in AIXM 5.1.1. | DEC-0005 |
| `pixm:AbstractRunwayAccessPointStatus` (`closed`, `active`, `restriction`) | — | none | Availability in AIXM is modeled with `aixm:ManoeuvringAreaAvailability` and time slices; correspondence TODO(VERIFY). | DEC-0005 |
| `pixm:UsageLimitation`, `pixm:CodeRunwaySideType` | — | none | | DEC-0005 |
