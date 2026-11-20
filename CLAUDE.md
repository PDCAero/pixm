# CLAUDE.md — Performance Information Exchange Model (PIXM)

This file tells Claude Code how to work on PIXM. Read it in full before creating or changing any schema, UML, example, or documentation file. When a rule here conflicts with a habit from another project, this file wins. When a rule here conflicts with an explicit instruction from the CCB (the project author), the CCB instruction wins — but say which rule is being overridden.

---

## 1. What PIXM is

PIXM is a SWIM-compatible information exchange model that standardises how **aircraft performance information — its inputs, its outputs, and the context needed to interpret them** — is exchanged among aviation stakeholders (operators, OEMs, EFB/performance-tool vendors, ANSPs, aerodrome operators, regulators).

It is a sibling of the established exchange models and should feel familiar to anyone who knows them:

| Model | Domain | Relevance to PIXM |
|---|---|---|
| **AIXM** (5.1.1 / 5.2) | Aeronautical information: aerodromes, runways, obstacles, surface contamination | Runway geometry, declared distances, runway condition (GRF/RCR), obstacles, elevation |
| **FIXM** (4.x Core) | Flight and flow information | Aircraft identification/type, masses, flight phases, departure/arrival aerodromes |
| **IWXXM / WXXM** | Meteorology | Wind, temperature, QNH, precipitation inputs |
| **AMXM** | Aerodrome mapping | Surface geometry where needed |
| **AIRM** | ATM Information Reference Model — the semantic reference all of the above trace to | PIXM must trace to it (see §9) |

### Deliverables (the four PIXM products)

1. **XML Schema (XSD)** — the normative core of the standard.
2. **UML logical model** — the source of truth for semantics; the XSD is derived from it.
3. **Example instance files** — valid against the XSD, realistic, and commented.
4. **Documentation** — primer, data dictionary, mapping/traceability reports, implementation guidance.

The UML, XSD, data dictionary and examples must never disagree. A change to one is not done until the others are updated (see §13).

---

## 2. How to work with the CCB (the user)

The user acts as the **PIXM Change Control Board (CCB)**. Claude proposes; the CCB decides.

**Always stop and ask the CCB before:**

- reusing, adapting, or ignoring a structure from AIXM, FIXM, IWXXM, or another standard (§8);
- deviating from the AIRM, or adding a concept the AIRM does not contain (§9);
- relaxing any of the core philosophies in §3 (e.g. using a code or external lookup instead of an enumeration);
- making a property mandatory (§3.5);
- renaming, removing, or changing the type or multiplicity of an existing released element (breaking change);
- adding a free-text or "OTHER" escape hatch.

**How to ask:** use a short, decision-ready format. For example:

> **CCB decision needed — runway condition input**
> PIXM needs per-third runway condition for landing performance. AIXM 5.2 has `RunwaySectionContamination` (runwayConditionCode, depth+uom, proportion, layer/type).
> Options:
> **(A) Reuse** — import the AIXM type by reference. Pros: zero mapping. Cons: drags in GML/AIXM feature model, time slices, AIXM codelists.
> **(B) Adapt** — define `pixm:RunwaySectionCondition` with the same semantics and AIXM-compatible enumeration literals, plus a documented mapping. Pros: standalone, simpler. Cons: a mapping to maintain.
> **(C) Ignore** — model independently.
> AIRM: corresponds to `<AIRM URN>` — no deviation for A or B.
> Recommendation: B.

Record each decision in `docs/decisions/` (see §14) so it is not re-asked.

If the CCB is not available (unattended run), do not guess on these items: implement the rest, leave a clearly marked `TODO(CCB):` note in the model/docs, and list the open decisions in the final summary.

---

## 3. Core PIXM philosophies (mandatory)

These eight principles define PIXM. Every element Claude adds must satisfy them, or carry a recorded CCB exception.

### 3.1 Semantically descriptive, human-readable names

- Names say what the thing *is*. By default use full words (`pressureAltitude`, not `pa`; `runwaySlope`, not `rwySlp`), and never use ad-hoc, vendor-specific, or tool-specific abbreviations.
- **Accepted community terms are allowed as names.** Where a term is generally understood across the aircraft performance and flight operations engineering community, use the common name rather than inventing a longer one. V-speeds are the prime example: `v1`, `vR`, `v2`, `vRef`, `vMCG`, `vMU` are preferred over `takeoffDecisionSpeed`, `rotationSpeed`, etc.
  - Test for "generally understood": the term has one meaning, is defined in regulatory, ICAO, or AFM material, and a performance or flight ops engineer would recognise it without a glossary.
  - The definition must still spell out the full term and cite its source, e.g. "V1 — the maximum speed in the takeoff at which the pilot must take the first action to stop the aeroplane within the accelerate-stop distance. [CS-Definitions / 14 CFR 1.2]".
  - Write the term in the casing convention of its position (lowerCamelCase for properties, UpperCamelCase for types), treating the abbreviation as one word: `vRef`, `CodeV2ScheduleType`.
  - Keep the approved list in `docs/glossary/accepted-terms.md`. If a term is not on the list and it's unclear whether it qualifies, ask the CCB and add it once decided.
- No overloaded generic names (`value`, `data`, `type1`, `param`, `info`) unless qualified by an unambiguous parent and only inside measure/value types.
- A name should make the **reference/datum** explicit where it matters: `pressureAltitude` vs `geometricAltitude`; `calibratedAirspeed` vs `trueAirspeed` vs `groundSpeed`; `outsideAirTemperature` vs `temperatureDeviationFromISA`; `grossMass` vs `zeroFuelMass`.
- Distinguish inputs, limits, and results in the name when the same quantity appears in more than one role: `actualTakeoffMass`, `maximumAllowableTakeoffMass`, `performanceLimitedTakeoffMass`.

### 3.2 Strong typing and enumeration over implicit meaning

- The model must contain the meaning needed to implement and understand each parameter. A receiver should not need an external table, ICD, or "tribal knowledge" to decode a value.
- Prefer **enumerations** for closed sets, **typed measures** for quantities (§3.3), **booleans modelled as clear two-value enumerations** where the "false" state is meaningful (see §6.4), and **structured sub-elements** over concatenated strings.
- Never encode multiple facts in one string that must be parsed (e.g. `"5/2/3"` for three RWYCCs, `"FLAPS15/AI-ON"`). Model each fact separately.
- Every enumeration literal carries its own definition in the UML and in the XSD `<xs:annotation>`.
- Constrain primitives with facets (ranges, patterns, lengths, fraction digits) wherever the domain allows (e.g. `runwayConditionCode` 0..6).
- **Exception:** where the CCB explicitly directs it (e.g. referencing an OEM-proprietary configuration code, an ICAO designator list, or an external code registry), an external code or open codelist may be used. Mark these with a `«codelist»` stereotype and a `CCB-EXCEPTION` note naming the authority that owns the list. Never introduce one on Claude's own initiative.

### 3.3 Engineering parameters carry their units

- Every physical quantity is a **measure type** with a mandatory `uom` attribute constrained to an enumeration of allowed units for that quantity: `MassType` (KG, LB, T), `SpeedType` (KT, KM_H, M_S, MACH handled separately), `DistanceType`, `AltitudeType`/`VerticalDistanceType` (FT, M, FL), `TemperatureType` (C, F, K), `PressureType` (HPA, IN_HG, MB), `AngleType`, `SlopeType`/`GradientType` (PERCENT), `DurationType`, etc.
- Never rely on a default or implied unit. Never name a unit into an element (`massKg`, `windKts`) — the unit lives in `uom`.
- Dimensionless quantities (ratios, coefficients, Mach number, percentages) still get an explicit type that states what they are (e.g. `MachNumberType`, `PercentageType`, `FrictionCoefficientType`).
- Where precision or source accuracy matters, allow an optional accuracy/resolution property on the measure type rather than inventing ad-hoc siblings.
- Follow the AIXM pattern for unit codelists (`Uom…Type`) where a matching AIXM unit list exists; flag any differences for the CCB (§8).

### 3.4 Elements have standalone meaning

- Any significant element (a configuration block, a runway condition, a takeoff result) should be sendable on its own and still be interpretable. It must carry — or be able to carry — enough context (identification, applicability, time of validity, reference datum, units) to mean something without its parent.
- Do not rely on sibling position, document order, or parent-only context to give meaning to a value. If an element only makes sense "because it sits under X", either move that context into the element as an optional property or reference X explicitly.
- Prefer self-describing references (identifier + type) over positional or index-based links.
- Definitions (UML notes / XSD annotations) must also stand alone — do not define a property by referring to another model element ("see above").

### 3.5 Everything optional unless the parent is meaningless without it

- Default multiplicity is **0..1** (or **0..\*** for lists).
- A property is **1..1 / mandatory only when its absence would make the parent meaningless**, e.g. `uom` on a measure, the `value` of a measure, the aircraft/registration identifier inside an `AircraftIdentification` block if that is the block's only purpose.
- Business-rule mandatoriness ("an EFB must send X for a landing calculation") belongs in **profiles / business rules** (Schematron or documented coding rules), not in the core XSD. This mirrors how AIXM separates the core model from data-set coding rules.
- Any proposal to make a property mandatory in the core schema must be raised with the CCB with the justification.
- Support explicit "value deliberately not provided" through a `nilReason`-style mechanism (§6.5) rather than magic values (`-1`, `9999`, `"NR"`).

### 3.6 Group parameters into reusable logical blocks

- Build reusable blocks once and use them across disciplines. Canonical examples:
  - `AircraftConfiguration` — flap/slat setting, landing gear, spoilers, anti-ice, bleeds/packs, thrust reverser availability, MEL/CDL items — reused by takeoff, climb-out, approach, landing, go-around.
  - `AircraftIdentification`, `AircraftMassAndBalance` (masses, CG), `EngineThrustSetting` (rating, derate, assumed/flex temperature).
  - `AtmosphericConditions` (OAT, QNH, wind components, ISA deviation), `RunwayCondition`, `RunwayGeometry`/`DeclaredDistances`, `Obstacle`.
  - `PerformanceCalculationProvenance` (tool, database/AFM revision, calculation method, time, operator policy applied).
- Discipline-specific classes (`TakeoffPerformanceRequest`, `LandingPerformanceResult`, …) should be thin compositions of these shared blocks plus discipline-specific properties.
- Before creating a new class, search the existing PIXM model for a block that already carries the meaning. Reuse it, or propose a generalisation; do not create a near-duplicate.
- Separate **inputs/conditions**, **constraints/limits**, and **results** into distinct blocks so they can be exchanged independently.

### 3.7 Highlight equivalent structures in existing standards — and ask

- For every new concept, check AIXM, FIXM, IWXXM, AMXM (and GML/ISO 19100 for geometry/time) for an equivalent.
- If one exists, present it to the CCB with the **Reuse / Adapt / Ignore** options (template in §2) before modelling. Include: the source element path, version, definition, type/units, and any semantic gap.
- If the CCB chooses *Adapt*, keep enumeration literals and definitions aligned with the source where possible and record the mapping in `docs/mappings/` (§8).

### 3.8 Follow the AIRM; flag every deviation or gap

- Each PIXM class, attribute, and enumeration literal should trace to an AIRM concept (semantic correspondence; §9).
- If the AIRM lacks the concept (very likely for many performance parameters — e.g. assumed temperature, V-speeds, climb gradient requirements, landing distance factors), **say so explicitly** and propose wording, so it can become an AIRM change request.
- If PIXM intentionally deviates from the AIRM definition, flag it to the CCB with the rationale and record it in the traceability report.

---

## 4. Best practices adopted from AIXM, FIXM and SWIM

These are derived from the AIXM UML-to-XSD mapping rules, the FIXM Modelling Best Practices and Development Guidelines, and the EUROCONTROL SWIM supporting material. They complement §3.

### 4.1 Content, not presentation
- PIXM models *what the information is*, not how it is displayed, printed on a TOLD card, or formatted in an ACARS uplink. Presentation formats are produced *from* PIXM, never stored *in* it.
- Legacy text formats (e.g. SNOWTAM text, ACARS performance messages) may be carried only as an optional, clearly labelled secondary representation alongside the structured data, and only with CCB approval.

### 4.2 Structured, never parsed
- No element should require receivers to decode text with custom logic.
- No generic name/value pair or "custom data" bags in the core. Stakeholder-specific needs go in extensions (§4.8). (FIXM removed name/value pairs for exactly this reason.)

### 4.3 Snapshot vs history
- A PIXM message represents the state of a request or result at a point in time. Do not model history (lists of prior calculations) unless a specific use case is endorsed by the CCB.
- Every message and every standalone block may carry the time(s) it applies to (`observationTime`, `calculationTime`, `validityPeriod`). Use ISO 8601 UTC `dateTime` only.

### 4.4 Reuse, don't redefine
- Where a concept is already defined by AIXM/FIXM/IWXXM, either import it or define a semantically equivalent element with a recorded mapping (§3.7). Never silently define a conflicting meaning for a term those models already use.
- Compatibility with ICAO provisions (Annex 6, Annex 14, PANS-AD Doc 9981 GRF, Doc 10064 Aeroplane Performance Manual, etc.) is *in meaning*, not necessarily in form.

### 4.5 Naming conventions (FIXM/AIXM style)
- **Classes, data types, packages:** UpperCamelCase (`AircraftConfiguration`). Data types end in `Type` (`MassType`, `CodeFlapSettingType`).
- **Attributes and association roles:** lowerCamelCase (`assumedTemperature`, `takeoffConfiguration`).
- **Enumeration literals:** UPPER_SNAKE_CASE, letters/digits/underscore only (`FULL_THRUST`, `DERATE_1`). Keep them short but unambiguous.
- **Characters:** letters, digits, underscore only. No hyphens, spaces, or diacritics.
- **Singular nouns** unless the element is explicitly a list; present tense.
- **Spelling:** follow ICAO/British spelling (`metre`, `aeroplane` in definitions; ask the CCB to confirm whether element names use ICAO "metre" or US "meter" if it ever matters in a name).
- Names unique within their scope; no reuse of a name with a different meaning anywhere in the model.
- Use AIXM's convention for coded types: `Code<Concept>Type` for enumerations/codelists, `Uom<Quantity>Type` for unit lists, `Value<Quantity>Type` for measures — **unless the CCB adopts a different PIXM convention**; record the choice in `docs/decisions/`.

### 4.6 Definitions and documentation
- Every package, class, attribute, association role, and enumeration literal has a definition. No exceptions.
- Definitions describe the element itself (not its container), are standalone (§3.4), and cite their origin in brackets: `[ICAO Annex 6]`, `[Doc 9981]`, `[AIXM 5.2]`, `[FIXM 4.3]`, `[AIRM]`, `[PIXM]`.
- Package documentation states the package theme, its role in the model, and any special rules.
- Define the datum, sign convention, and reference point for every engineering quantity (e.g. "positive = headwind", "measured from the runway threshold", "relative to ISA at the aerodrome pressure altitude").

### 4.7 UML conventions
- Stereotypes are limited to a small, documented set. Proposed set: `«feature»`/`«object»` (only if PIXM adopts the AIXM feature model — CCB decision), `«datatype»`, `«enumeration»`, `«codelist»` (CCB exception only), `«choice»`, `«deprecated»`.
- Use `«choice»` for "exactly one of" alternatives; each alternative is 0..1.
- Single inheritance only; abstract base classes are fine; avoid deep hierarchies.
- Ordered collections must be marked as ordered, and the ordering rule stated in the definition (e.g. runway thirds ordered from the threshold of the reported direction). Collections are unordered sets by default.
- Primitive types (`string`, `decimal`, `integer`, `boolean`, `dateTime`, `duration`) are used only inside base data types, never directly on domain classes. Domain attributes use PIXM data types.
- Keep one diagram per package, readable on one or two pages.
- Value constraints (range, pattern, fraction digits, length) are captured on the UML element so the XSD can be generated from them.

### 4.8 Core vs extension
- **Core** contains information that is broadly agreed across stakeholders and endorsed by the CCB.
- Provide a FIXM-style extension hook (`Extensible` base with `extension 0..*` of an abstract `Extension` type) on key classes, so stakeholders can add data without breaking core validation and receivers can ignore what they don't understand.
- Extensions use their own namespace and a distinguishing prefix, must not redefine core constraints, and should not depend on other extensions.

### 4.9 Versioning and deprecation
- Every UML element carries a tagged value for the PIXM version in which it was introduced.
- Never delete or rename a released element directly. Mark it `«deprecated»` with: rationale (change request reference), replacement path (or N/A), deprecation version, planned deletion version. The generated XSD carries the same information in `<xs:annotation><xs:appinfo>`.
- Schema namespace includes the major.minor version (e.g. `http://www.pixm.aero/schema/1.0` — confirm the URI with the CCB). Patch versions do not change the namespace.
- For each change, classify backward/forward compatibility in the AIXM change-proposal style (no mapping needed / mapping without loss / mapping with loss).

### 4.10 XSD mapping rules
- The XSD is generated from (or kept strictly in step with) the UML. Element names = UML names.
- Global complex types per class; elements for properties; XML attributes only for `uom`, `nilReason`, and similar metadata.
- Each enumeration becomes an `xs:simpleType` restriction with one `xs:enumeration` per literal, each with an `xs:annotation/xs:documentation` definition.
- Measures: `xs:simpleContent` extension of a decimal base with required `uom` attribute (and optional `nilReason`).
- Use `targetNamespace`, `elementFormDefault="qualified"`, and a consistent `pixm:` prefix.
- Keep the schema modular: e.g. `PIXM_DataTypes.xsd`, `PIXM_Common.xsd` (shared blocks), `PIXM_Takeoff.xsd`, `PIXM_Landing.xsd`, …, `PIXM_Message.xsd`.
- Business rules that XSD cannot express go into Schematron (`rules/`) with a rule ID, a plain-English description, and a severity.

---

## 5. Performance-domain modelling guidance

- **Request / result separation.** Model a calculation as: *conditions/inputs* → *method/provenance* → *results* (+ *limitations/assumptions*). Results must reference, or embed, the inputs they were computed from, so a result is auditable on its own.
- **Limiting factor is explicit.** When a result is limited (field length, climb, obstacle, tyre speed, brake energy, VMCG…), state the limiting factor as an enumeration, not in a remark.
- **Provenance.** Results should be able to carry: calculation tool and version, performance database/AFM revision, calculation method/standard (e.g. EASA/FAA certified vs advisory/operational), operator margins/factors applied, and calculation time.
- **Datum and reference conditions** must be explicit: pressure vs geometric altitude, QNH vs QFE, wind reported vs wind component along runway, runway slope sign, temperature in absolute vs ISA-relative terms.
- **Runway and surface condition** inputs should align with ICAO GRF (RWYCC per third, contaminant type/depth/coverage) — see the AIXM 5.2 RCR example in the project (`examples/aixm52/…`). Note: that example's GRF-specific element names are marked unverified against the published AIXM 5.2 XSD; check before relying on them.
- **Aircraft configuration** must be expressible both as standard enumerated states (flaps, gear, anti-ice) and, where the CCB permits, as OEM-specific settings via a documented codelist exception.

---

## 6. Data-type patterns

### 6.1 Measure type (template)
```xml
<xs:complexType name="MassType">
  <xs:annotation><xs:documentation>A mass with its unit of measurement. [PIXM]</xs:documentation></xs:annotation>
  <xs:simpleContent>
    <xs:extension base="xs:decimal">
      <xs:attribute name="uom" type="pixm:UomMassType" use="required"/>
      <xs:attribute name="nilReason" type="pixm:NilReasonType" use="optional"/>
    </xs:extension>
  </xs:simpleContent>
</xs:complexType>
```

### 6.2 Enumeration (template)
```xml
<xs:simpleType name="CodeLandingGearPositionType">
  <xs:annotation><xs:documentation>The position of the landing gear. [PIXM]</xs:documentation></xs:annotation>
  <xs:restriction base="xs:string">
    <xs:enumeration value="EXTENDED">
      <xs:annotation><xs:documentation>Landing gear down and locked.</xs:documentation></xs:annotation>
    </xs:enumeration>
    <xs:enumeration value="RETRACTED">
      <xs:annotation><xs:documentation>Landing gear up and locked.</xs:documentation></xs:annotation>
    </xs:enumeration>
  </xs:restriction>
</xs:simpleType>
```

### 6.3 "Other" values — CCB decision required
AIXM permits `OTHER:FREE_TEXT` in every codelist; FIXM prefers a `«choice»` between the enumeration and an `otherText` field and discourages OTHER/UNKNOWN literals. Both weaken philosophy §3.2. **Default for PIXM: closed enumerations with no OTHER.** Add an escape hatch only when the CCB approves it for a specific enumeration, and prefer the FIXM `«choice»` pattern.

### 6.4 Booleans
Prefer a two-value enumeration with explicit meanings (e.g. `CodeAntiIceStatusType = ON | OFF`) over `xs:boolean` when the "false" state carries operational meaning or a third state may appear later. Plain `xs:boolean` is acceptable for true yes/no flags with an unambiguous definition.

### 6.5 Missing / withheld values
Adopt a GML-style `nilReason` (`inapplicable`, `missing`, `template`, `unknown`, `withheld`, plus `other:<text>`) so a sender can state *why* a value is absent. Never use sentinel numbers or text such as `NR`, `N/A`, `-1`.

---

## 7. Example instance files

- Every new class or significant change gets (or updates) at least one example in `examples/`.
- Examples must **validate against the current XSD** (and Schematron, if present). Run validation before declaring the work done.
- Use realistic but clearly fictional data (fictitious aerodromes such as EADD "Donlon", fictitious registrations), and say so in a header comment.
- Header comment states: purpose, scenario, PIXM version, and which features it exercises.
- Include at least one **standalone-block** example (e.g. just an `AircraftConfiguration`) to demonstrate §3.4.
- Where a value maps from a legacy/operational format (TOLD card, SNOWTAM), include the mapping in the header comment, as in the AIXM RCR example.

---

## 8. Mapping to other standards

- Maintain `docs/mappings/<standard>-<version>.md` (e.g. `aixm-5.2.md`, `fixm-4.3.md`, `iwxxm-2023.md`) with columns: PIXM element | source element path | relationship (equivalent / broader / narrower / partial / none) | notes | CCB decision ref.
- When proposing reuse, cite the exact source version. Do not cite element names from memory as fact — verify against the published XSD/UML or flag as unverified.

---

## 9. AIRM traceability

- Maintain `docs/airm/semantic-correspondence.md` (or `.csv`) following the AIRM semantic-correspondence approach: PIXM element | AIRM URN (e.g. `urn:aero:airm:<version>:…`) | correspondence type (equivalent / specialisation / generalisation / partial / no correspondence) | rationale.
- Pure container/grouping elements do not need a direct correspondence but should be noted as such.
- For "no correspondence", record proposed AIRM wording — these become AIRM change-request candidates.
- Record the AIRM version used. Verify URNs against the published AIRM (airm.aero); never invent a URN — mark it `TODO(AIRM-URN)` instead.

---

## 10. Repository layout (proposed — confirm with CCB)

```
/CLAUDE.md
/uml/                     UML model (XMI / EA / PlantUML) and exported diagrams
/schema/1.0/              PIXM_*.xsd
/rules/                   Schematron business rules
/examples/                PIXM example instances (+ examples/aixm52/ reference material)
/docs/primer/             Introduction and concepts
/docs/data-dictionary/    Generated/maintained element definitions
/docs/mappings/           AIXM, FIXM, IWXXM mappings
/docs/airm/               AIRM semantic correspondence
/docs/decisions/          CCB decision records (ADR-style)
/docs/glossary/           Accepted community terms and abbreviations (§3.1)
/docs/changes/            Change proposals and release notes
/tools/                   Validation and generation scripts
```

---

## 11. Tooling and validation

- Validate every XSD for well-formedness and schema correctness (e.g. `xmllint --noout --schema …` or `lxml`) after every change.
- Validate every example against the schema; run Schematron where present.
- Check that every element and enumeration literal in the XSD has a non-empty `xs:documentation`.
- Check naming conventions automatically where practical (UpperCamelCase types, lowerCamelCase properties, UPPER_SNAKE literals).
- Do not claim validation passed without running it.

---

## 12. Things Claude must not do

- Invent AIXM/FIXM/IWXXM/AIRM element names, URNs, or code literals and present them as real. Verify or mark as unverified.
- Add free text, name/value bags, OTHER literals, or external code references without CCB approval.
- Embed units in names, or rely on implied units.
- Make properties mandatory without CCB approval.
- Make breaking changes to released elements without the deprecation process.
- Leave UML, XSD, examples, and documentation out of sync.

---

## 13. Definition of done for any model change

1. CCB decisions obtained for any item in §2's "always ask" list.
2. UML updated (class/attribute/literal, definition, multiplicity, constraints, version tag).
3. XSD updated and valid.
4. At least one example created/updated and valid.
5. Data dictionary updated.
6. Mapping table(s) and AIRM correspondence updated (or `TODO` recorded and reported).
7. Change log entry with compatibility classification (§4.9).
8. Summary to the CCB listing open questions and any `TODO(CCB)` / `TODO(AIRM-URN)` items.

---

## 14. Decision records

Store CCB decisions as `docs/decisions/NNNN-short-title.md` with: context, options considered, decision, rationale, date, affected elements. Check existing decisions before asking the CCB a question again.

### Open decisions to settle early
- PIXM namespace URI and version scheme.
- Whether PIXM adopts the AIXM GML feature/time-slice model or a lighter FIXM-style plain-XML model (affects reuse of AIXM types).
- Naming convention for coded/measure types (`Code…Type`/`Uom…Type`/`Value…Type` vs alternatives).
- Escape-hatch policy for enumerations (§6.3).
- `nilReason` adoption (§6.5).
- UML tool and source format (Enterprise Architect, XMI, PlantUML).
- Initial list of accepted community terms (§3.1) and their exact casing (e.g. `vRef` vs `vref`, `vMCG` vs `vmcg`).
- Target versions of reference standards (AIXM 5.2, FIXM 4.3, IWXXM, AIRM).

---

## 15. Key references

- AIXM UML-to-XSD mapping rules and data-type conventions — EUROCONTROL SWIM/AIXM Confluence (swim-eurocontrol.atlassian.net, space "AC")
- FIXM Core Modelling Best Practices (v4.1.0) and FIXM Development Guidelines v2 — fixm.aero
- FIXM Strategy (core vs extension criteria) — fixm.aero
- AIRM and semantic correspondence reports — airm.aero
- ICAO Annex 6, Annex 14, Annex 15; PANS-AD (Doc 9981, GRF); Doc 10064 (Aeroplane Performance Manual)