# PIXM modelling guide

Background, rationale and worked guidance behind the rules in CLAUDE.md. Read it
when modelling a new concept. Where this guide and CLAUDE.md disagree, CLAUDE.md wins.

## 1. Related exchange models

| Model | Domain | Relevance to PIXM |
|---|---|---|
| AIXM (5.1.1, 5.2) | Aeronautical information: aerodromes, runways, obstacles, surface contamination | Runway geometry, declared distances, runway condition (GRF/RCR), obstacles, elevation |
| FIXM (4.x Core) | Flight and flow information | Aircraft identification/type, masses, flight phases, departure/arrival aerodromes |
| IWXXM / WXXM | Meteorology | Wind, temperature, QNH, precipitation inputs |
| AMXM | Aerodrome mapping | Surface geometry where needed |
| AIRM | ATM Information Reference Model | The semantic reference PIXM traces to |

## 2. Core principles: rationale and examples

### 2.1 Descriptive names and accepted community terms
- A term qualifies as "generally understood" when it has one meaning, is defined
  in regulatory, ICAO or AFM material, and a performance or flight operations
  engineer would recognise it without a glossary.
- Its definition still spells out the full term and cites the source, e.g.
  "V1: the maximum speed in the takeoff at which the pilot must take the first
  action to stop the airplane within the accelerate-stop distance.
  [14 CFR 1.2 / CS-Definitions]".
- Casing follows position, treating the abbreviation as one word: `vRef`
  (property), `CodeV2ScheduleType` (type).
- Make the reference explicit: `calibratedAirspeed` vs `trueAirspeed` vs
  `groundSpeed`; `outsideAirTemperature` vs `temperatureDeviationFromISA`;
  `grossMass` vs `zeroFuelMass`.
- Distinguish roles where the same quantity appears more than once:
  `actualTakeoffMass`, `maximumAllowableTakeoffMass`, `performanceLimitedTakeoffMass`.

### 2.2 Meaning lives in the model
- Never `"5/2/3"` for three runway condition codes or `"FLAPS15/AI-ON"` for a
  configuration: model each fact separately.
- Constrain primitives with facets wherever the domain allows (e.g. runway
  condition code 0–6).
- External codelist exceptions are marked in the definition with the owning
  authority and a reference to the CCB decision.

### 2.3 Units
- Where precision or source accuracy matters, add an optional accuracy or
  resolution property to the measure rather than ad-hoc sibling elements.
- Where an AIXM unit list exists for the same quantity, keep literals aligned
  and record any difference in `docs/mappings/`.

### 2.4 Standalone elements
- Prefer self-describing references (identifier + type) over positional or
  index-based links.

### 2.5 Reusable blocks
Candidate shared blocks:
- Aircraft configuration: flap/slat setting, landing gear, spoilers, anti-ice,
  bleeds/packs, thrust reverser availability, MEL/CDL items.
- Aircraft identification; mass and balance (masses, CG); engine thrust setting
  (rating, derate, assumed/flex temperature).
- Atmospheric conditions (OAT, QNH, wind components, ISA deviation); runway
  condition; runway geometry / declared distances; obstacle.
- Calculation provenance (tool, database/AFM revision, method, time, operator
  policy applied).

### 2.6 Core vs extension
- Core holds information broadly agreed across stakeholders and endorsed by the CCB.
- FIXM removed name/value pairs from its core because they defeat validation
  and shared meaning; PIXM follows the same reasoning.

## 3. Time and history
- PIXM uses AIXM-style time slices to state when information applies.
- A message represents the state of a request or result at a point in time; do
  not model history (lists of prior calculations) unless the CCB endorses a use case.
- Times are ISO 8601 `dateTime` in UTC.
- `TODO(CCB)`: document how PIXM time-slice interpretations (baseline,
  temporary, etc.) are intended to be used.

## 4. Compatibility with ICAO provisions
Compatibility with ICAO provisions (Annex 6, Annex 14, PANS-AD Doc 9981 GRF,
Doc 10064 Aeroplane Performance Manual) is in meaning, not necessarily in form.

## 5. Guidance for performance calculations (applies to that area only)
- Model a calculation as inputs/conditions → method/provenance → results
  (+ limitations/assumptions). A result references or embeds the inputs it was
  computed from, so it can be audited on its own.
- A limited result states its limiting factor as an enumeration (field length,
  climb, obstacle, tire speed, brake energy, VMCG…), never in a remark.
- Results can carry provenance: tool and version, performance database or AFM
  revision, calculation method (certified vs advisory), operator margins
  applied, calculation time.
- Datum and reference are explicit: pressure vs geometric altitude, QNH vs QFE,
  reported wind vs runway component, slope sign, absolute vs ISA-relative temperature.
- Runway condition aligns with ICAO GRF (RWYCC per third, contaminant type,
  depth, coverage) [Doc 9981].
- Aircraft configuration uses enumerated standard states; OEM-specific settings
  only through a CCB-approved codelist exception.

## 6. Future UML model
UML is deferred (CLAUDE.md §3.2). When it is introduced:

### 6.1 Generating UML from the XSD
1. Write a PIXM-specific converter (Python, XSD → PlantUML or XMI) that folds
   the regular patterns: Feature + TimeSlice → one «feature» class;
   `Code…BaseType` + `Code…Type` → one «enumeration»/«codelist»;
   `Val…Type` → «datatype» with `uom`; `minOccurs`/`maxOccurs` → multiplicity;
   `xs:documentation` → definition.
2. Alternatively import the XSD into a modelling tool (Enterprise Architect,
   Cameo) and clean up the result manually.
3. Once UML exists, generate an XSD from it (e.g. ShapeChange) and compare with
   the hand-written XSD to prove equivalence before making UML the source of truth.

### 6.2 UML conventions to adopt
- Small documented stereotype set: «feature», «object», «datatype»,
  «enumeration», «codelist» (CCB exception only), «choice», «deprecated».
- «choice» for exactly-one-of alternatives; each alternative 0..1.
- Single inheritance; abstract base classes allowed; shallow hierarchies.
- Ordered collections marked ordered, with the ordering rule in the definition.
- Primitives only inside base data types.
- One diagram per package, readable on one or two pages.
- Value constraints captured on the UML element so the XSD can be generated.
- Each element carries a tagged value for the PIXM version that introduced it.
