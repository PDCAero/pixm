# DEC-0005: Departure intersections and landing exits

- Date: 2026-11-21
- Status: Decided
- Affected elements: new features `DepartureIntersection` and `LandingExit`; new
  blocks `DeclaredDistances`, `ElevatedPoint`, `RunwayReferencePoint`,
  `BearingStrength`, `UsageLimitation`; new codelists `CodeRunwayPointRole`,
  `CodeTirePressureCategory`, `CodePavementEvaluationMethod`,
  `CodeVerticalDatum`, `CodeRunwaySide`; planned status notifications in `PIXM_Messages`

## Context
The CCB proposed a data model for departure intersections and landing exits
(concept mapping "DepartureIntersection + LdgExit", 2026-11). Example 3 already
held LSZH data in an older, non-validating structure (known defects E3, E5).
The model referred to `aixm:RunwayCenterlinePoint` (AIXM 5.1.1 spells it
`RunwayCentrelinePoint`, and its roles lack `END_ROLLOUT`) and to `gml:Schedule`
(not defined in GML 3.2).

## Decisions
1. **Runway reference point:** adapt as a PIXM block (`RunwayReferencePoint`:
   designator, role, location), not an AIXM import or xlink. Role is a new closed
   codelist: the 13 AIXM 5.1.1 `CodeRunwayPointRole` literals plus `END_ROLLOUT`.
   Location is a PIXM `ElevatedPoint` block (GML point, elevation, vertical datum).
2. **Points:** `runwayReferencePoint`, `distanceReferencePoint`,
   `distanceReferenceLine` (departures) and `referencePoint` (exits) are different
   points; all are kept, each with its own definition.
3. **Availability and status:** no schedule property. Planned closures and
   restrictions are `TEMPDELTA` time slices of the feature (AIXM practice). The
   detailed status becomes a status notification in `PIXM_Messages` (pattern of
   DEC-0004), for both features, as a later step.
4. **Bearing strength:** a reusable `BearingStrength` block (ACN-PCN), reusing
   `ValPCNType`, `CodePavementBehaviourType` and `CodePavementSubgradeType`, with new
   closed codelists for tire pressure category and evaluation method. PCR may be
   added later.
5. **methodOfDetermination:** deferred until its values are agreed (`TODO(CCB)`).
6. **Text and sides:** `description` is an optional `pixm:TextNoteType` (free text
   approved for human-readable remarks only). `entryAccessSide` / `exitSide` use a
   new closed codelist `CodeRunwaySide` (LEFT, RIGHT, BOTH).
7. **Associations:** `DeclaredDistances`, `RunwayReferencePoint` and
   `UsageLimitation` are embedded blocks; `PerformanceRunway` is embedded as well
   (as elsewhere in the schema today). All optional (0..1).
8. **Examples:** Example 3 is converted to the new structure, keeping its values;
   the vertical datum NAVD88 (North American) is replaced by EGM_96 and labeled
   illustrative.
9. **Defaults accepted with the plan:** `CodeVerticalDatum` keeps the `OTHER:name`
   pattern (CCB exception to closed codelists, so national datums can be given);
   the LAHSO flag is named `landAndHoldShortPoint` (full words, no glossary entry);
   exit speeds are ground speeds; entry and exit angles use `ValAngleType`;
   `displacementFromFullLength` is measured along the runway centerline from the
   start of the takeoff run available (departures) or the threshold (exits) and is
   not negative.
10. **Naming:** full words are used instead of abbreviations in new names
    (`takeoffRunAvailable` rather than `tora`, `pavementClassificationNumber`
    rather than `pcn`); `runwayDirectionDesignator` and `aerodromeDesignator`
    follow DEC-0004; the limits shared by both features and the status
    notification are one `UsageLimitation` block (principle 6).

## Rationale
Adapting rather than importing keeps PIXM free of new AIXM dependencies (DEC-0001,
known defect S1) and allows `END_ROLLOUT`. Time slices express availability the
way AIXM does without a separate schedule model. Shared blocks avoid the
duplication the drawing shows between the two features and the status block.
