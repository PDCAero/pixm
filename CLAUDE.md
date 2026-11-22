# CLAUDE.md — Performance Information Exchange Model (PIXM)

Rules for Claude Code on this repository. Read in full before changing any
schema, example or documentation file. This file overrides habits from other
projects; an explicit CCB instruction overrides this file (say which rule is
being overridden).

## 1. What PIXM is
PIXM is a SWIM-compatible exchange model for **aircraft performance
information**: its inputs, its results, and the context needed to interpret
them, exchanged between operators, OEMs, EFB/performance-tool vendors, ANSPs,
aerodrome operators and regulators. It is a sibling of AIXM (aeronautical
data), FIXM (flight data) and IWXXM (meteorology), and traces to the AIRM.

Products: the **XSD** (normative, source of truth), **example instances**
(must validate), and **documentation** (guidelines, mappings, AIRM
traceability, change log). A UML model will later be generated from the XSD.
Schema, examples and documentation must never disagree; a change is not done
until all three agree (§13).

## 2. Working with the CCB
The user is the **PIXM Change Control Board (CCB)**. Claude proposes; the CCB
decides. Check `docs/decisions/` before asking. Do not re-ask a decided question.

**Always ask the CCB before:**
- reusing, adapting or ignoring a structure from AIXM, FIXM, IWXXM or another standard;
- deviating from the AIRM, or adding a concept the AIRM lacks;
- relaxing a core principle (§5), e.g. a code or external lookup instead of an enumeration;
- making a property mandatory;
- changing an element's meaning, type or multiplicity, or removing it (renames: see §4);
- adding free text, or `OTHER` to a new codelist;
- adding an extension hook to a feature.

**How to ask:** a short, decision-ready request with options (Reuse / Adapt /
Ignore, or similar), pros and cons, the AIRM position, and a recommendation.
Template: `docs/process/ccb-process.md`. Record each decision as
`docs/decisions/DEC-NNNN-short-title.md`.

**If the CCB is unavailable:** do not guess on these items. Do the rest, leave a
`TODO(CCB):` note at the spot, and list open decisions in the summary.

## 3. Current state of the repository
What already exists and what has been decided. Where another rule in this file
conflicts with this section, this section wins.

### 3.1 Status
- PIXM version: **0.5 (pre-release)**. Namespace: `http://www.pixm.aero/schema/0.5`, prefix `pixm:`.
- Until 1.0, breaking changes are permitted but every one is recorded in the
  change log (§4.5). The deprecation process (§6.4) applies from 1.0 onwards.

### 3.2 Settled decisions
| Topic | Decision |
|---|---|
| Model style | AIXM 5.1.1 pattern: GML 3.2 features with Feature + TimeSlice pairs. Migration to AIXM 5.2 is planned; do not add constructs that would block it. |
| Source of truth | The **XSD** is normative. UML is deferred and will later be generated from the XSD, so the XSD must stay regular (§3.4). |
| Type naming | AIXM style: `Code…BaseType` + `Code…Type` (codelists), `Val…BaseType` + `Val…Type` (measures), `Uom…Type` (unit lists), `Text…Type` (constrained text). |
| Units | A measure carries a **required** `uom` whenever the quantity can be expressed in more than one unit or scale. Only truly dimensionless quantities (coefficients, ratios, classification numbers) omit `uom`; their definition must say "dimensionless" and state the range or scale. A unit is never implied by convention alone. (Stricter than AIXM 5.1.1.) |
| Missing values | `gml:NilReasonEnumeration` via a `nilReason` attribute. |
| `OTHER` escape hatch | The `OTHER(:text)` pattern on existing codelists is grandfathered as CCB-approved. New codelists are closed unless the CCB approves an exception. |
| AIXM dependency | PIXM does not import the AIXM schema. Links to AIXM data use PIXM-defined reference types (xlink to the AIXM feature identifier). AIXM 5.2 migration is an alignment of meanings and mappings, not a schema dependency change. |
| Schema files | One feature file for now; a per-discipline split is revisited at 1.0 or the AIXM 5.2 migration. |
| External imports | Published schemas reference official online `schemaLocation`s so they stand alone for users. Local copies are for development only (§10). |
| Spelling | US spelling in names and definitions, unless it conflicts with an AIRM term. |

### 3.3 Schema files
What each schema file contains and depends on: `schema/README.md`. Keep that
file up to date whenever schema files are added, split, renamed or moved.

AIXM 5.1.1 is currently imported for one type only (`aixm:RunwayDirectionPropertyType`,
property `aixmRunway`). It is scheduled to be replaced by a PIXM reference type and
the import removed (see known defects).

### 3.4 Patterns that must stay regular (for future UML generation)
- No anonymous (inline) types; every type is named and global.
- Every feature `X` follows the AIXM 5.1.1 pattern: element `X` + `XType`
  (extends `AbstractPIXMFeatureType`, with a `timeSlice` property of type
  `XTimeSlicePropertyType`), `XTimeSlicePropertyType` (contains one
  `XTimeSlice` element), and element `XTimeSlice` + `XTimeSliceType`. `X`
  substitutes for `pixm:AbstractPIXMFeature`; `XTimeSlice` for
  `pixm:AbstractPIXMTimeSlice`.
- Every codelist has its `Code…BaseType` / `Code…Type` pair; every measure has
  its `Val…BaseType` / `Val…Type` pair.
- `minOccurs` / `maxOccurs` are always stated explicitly.
- Definitions go only in `xs:annotation/xs:documentation`; version and
  deprecation metadata only in `xs:annotation/xs:appinfo`.
- Every reference to a PIXM type uses the `pixm:` prefix.

### 3.5 Known defects
Recorded in `docs/changes/known-defects.md`. Fixing them is the first task
after this file's adoption, before new model functionality.

## 4. Legacy and transition policy
Much of the existing schema and examples predate this file. This section says
how the rules apply to that content.

### 4.1 Fix on touch
- When Claude changes an element (type, property, enumeration, example block)
  for any reason, it also brings **that element** into line with this file:
  definition, naming, `pixm:` prefixes, explicit `minOccurs`/`maxOccurs`,
  required `uom`, regular patterns (§3.4).
- "That element" means the type or property being changed and anything it
  directly declares — not sibling types, other codelists, or the rest of the file.
- Claude does not sweep unrelated content. Wider clean-up happens only as a
  dedicated, CCB-approved change.
- Every fix-on-touch change is listed separately in the change summary
  ("also brought into line: …").

### 4.2 What fix-on-touch does not do
- It never removes a grandfathered `OTHER(:text)` pattern (§3.2).
- **During 0.x**, it may correct typos and capitalisation in element and type
  names without asking (e.g. `sesgmentLength` → `segmentLength`), provided the
  meaning is unchanged. Every such rename is logged (§4.5) and all examples
  using the name are updated in the same change.
- **From 1.0**, any rename needs CCB approval and follows the deprecation
  process (§6.4).
- It never changes an element's meaning, type or multiplicity, or removes an
  element, without CCB approval (§2).
- If bringing an element into line would itself need a CCB decision, Claude
  leaves it, adds a `TODO(CCB):` note, and reports it.

### 4.3 Known defects
- Items in `docs/changes/known-defects.md` are fixed as a dedicated task, not
  piecemeal by fix-on-touch, unless the defect is in the element being changed.
- When a defect is fixed, it is removed from that list and recorded in the change log.

### 4.4 Examples
- Existing examples are brought into line when the schema they exercise
  changes, or when the example itself is edited.
- An example that no longer validates after a schema change is fixed in the
  same change, never left broken.

### 4.5 Change log
Every change to the schema or examples is recorded in `docs/changes/CHANGELOG.md`
in the same change: one line per change, written for CCB review.

    - FIX     PIXM_Features: `sesgmentLength` → `segmentLength` (typo). Compat: rename.

Tag (`ADD`, `CHANGE`, `RENAME`, `FIX`, `REMOVE`, `DEPRECATE`, `DOC`), file and
element, old → new, `Compat:` (`none` / `rename` / `breaking`), and `Ref:`
`DEC-NNNN` when a CCB decision applied. Never hide a breaking change inside a
bulk line. Full format: `docs/process/ccb-process.md`.

## 5. Core principles
Every element Claude adds or changes must satisfy these, or carry a recorded
CCB exception. Rationale and examples: `docs/guidelines/modelling-guide.md`.

1. **Descriptive names.** Full words, no ad-hoc or vendor abbreviations
   (`pressureAltitude`, not `pa`). Accepted community terms such as V-speeds
   (`v1`, `vR`, `v2`, `vRef`, `vMCG`) are allowed if listed in
   `docs/glossary/accepted-terms.md`; ask the CCB before adding one. Make the
   datum explicit (`pressureAltitude` vs `geometricAltitude`) and the role
   explicit (`actualTakeoffMass` vs `maximumAllowableTakeoffMass`). No bare
   generic names (`value`, `data`, `info`).
2. **Meaning lives in the model.** A receiver must not need an external table
   or ICD to decode a value. Use enumerations for closed sets, measures for
   quantities, and structured elements, never one string carrying several
   facts (`"5/2/3"`). Constrain values with facets (ranges, patterns). Yes/no
   and on/off use `CodeYesNoType` / `CodeOnOffType`, not `xs:boolean`.
   External or open codelists only by CCB exception, naming the authority.
3. **Units are explicit.** Follow the units rule (§3.2). Never put a unit in
   a name (`massKg`).
4. **Elements stand alone.** A significant block (configuration, runway
   condition, result) must be interpretable without its parent: it carries,
   or can carry, its identification, applicability, time and datum.
   No meaning from sibling position or document order. Definitions must not
   refer to other elements ("see above").
5. **Optional by default.** `minOccurs="0"` unless the parent is meaningless
   without the property. Mandatory-for-a-use-case rules go in Schematron
   business rules, not the core schema. Missing values use `nilReason`, never
   sentinel values (`-1`, `9999`, `NR`).
6. **Reusable blocks.** Build shared blocks once (aircraft configuration,
   identification, mass and balance, thrust setting, atmospheric conditions,
   runway condition, provenance) and compose discipline types from them.
   Search for an existing block before creating one; no near-duplicates.
   Keep inputs, limits and results in separate blocks.
7. **Check other standards first.** For each new concept, look for an
   equivalent in AIXM, FIXM, IWXXM, AMXM and GML/ISO 19100, and bring it to
   the CCB as Reuse / Adapt / Ignore before modelling (§2).
8. **Trace to the AIRM.** Each type, property and literal should trace to an
   AIRM concept. Say explicitly when the AIRM has no equivalent and propose
   wording; flag any intentional deviation to the CCB.
9. **Content, not presentation.** Model what the information is, not how it
   is displayed (TOLD card, ACARS text). Legacy text formats only as an
   optional, labelled secondary representation, with CCB approval. No
   name/value pairs or "custom data" bags in the core; use extensions (§6.3).
10. **Document everything.** Every type, property and literal has an
    `xs:documentation` definition that describes the element itself, states
    datum, sign convention and reference point for quantities, and ends with
    its source: `[ICAO Annex 6]`, `[Doc 9981]`, `[AIXM 5.1.1]`, `[FIXM 4.3]`,
    `[AIRM]`, `[PIXM]`.

## 6. Conventions

### 6.1 Naming
- Types: UpperCamelCase ending in `Type`. Properties: lowerCamelCase.
  Enumeration literals: UPPER_SNAKE_CASE. Letters, digits and underscore only.
- Type families: as in §3.2 (`Code…`, `Val…`, `Uom…`, `Text…`); features as in §3.4.
- Singular nouns unless the property is a list. Names are unique; never reuse
  a name with a different meaning.
- US spelling (`meter`, `airplane`, `optimization`) unless it conflicts with an
  AIRM term, in which case follow the AIRM.

### 6.2 XSD structure
- `elementFormDefault="qualified"`; namespace and prefix as in §3.1.
- Every type is named and global. Properties are elements; XML attributes are
  used only for `uom`, `nilReason` and similar metadata.
- Domain properties use PIXM types, never XSD primitives (`xs:int`,
  `xs:string`) directly. Primitives appear only inside `…BaseType` definitions.
- Each enumeration literal has its own `xs:documentation`.
- Use `xs:choice` for "exactly one of" alternatives.
- Collections are unordered unless the definition states the ordering rule
  (e.g. runway thirds from the threshold).
- Rules XSD cannot express go in Schematron under `rules/`, each with an ID,
  a plain-English description and a severity.
- Templates: `docs/guidelines/xsd-patterns.md`.

### 6.3 Extensions
- Stakeholder-specific data goes in extensions, not the core. Extensions
  derive from `pixm:AbstractExtensionType`, use their own namespace and prefix,
  must not redefine core constraints, and must not depend on other extensions.
- Extension hooks (`extension`, 0..*) are added to a feature only when a
  stakeholder need is identified, and only with CCB approval (§2).

### 6.4 Versioning
- 0.x: see §3.1 and §4. From 1.0: never delete or rename a released element
  directly; mark it deprecated in `xs:appinfo` with the change reference,
  replacement, deprecation version and planned removal version.
- Every change is logged with a compatibility class (§4.5).

## 7. Examples
How to write examples (header format, scenarios, mappings):
`docs/guidelines/examples-guide.md`.

- Every new type or significant change gets at least one example under
  `examples/`, and every example must pass `tools/validate.py` (§10).
- Real aerodromes and data may be used if the header comment states the data
  is illustrative and not for operational use. Otherwise use clearly
  fictional data.
- Each example starts with a header comment: purpose, scenario, PIXM version,
  features exercised, and the illustrative-data statement where relevant.
- Example folders have descriptive names using letters, digits, spaces and
  hyphens only.
- Keep at least one example that sends a block on its own (e.g. only an
  aircraft configuration) to demonstrate principle 4 (§5).

## 8. Traceability to other standards and the AIRM
Procedures and table formats: `docs/process/traceability.md`.

- Mappings to other standards live in `docs/mappings/<standard>-<version>.md`
  (e.g. `aixm-5.1.1.md`); AIRM correspondence in
  `docs/airm/semantic-correspondence.md`.
- Never present an AIXM/FIXM/IWXXM/AIRM element name, URN or code literal
  from memory as fact. Verify it against the published source, or mark it
  `TODO(VERIFY)`; for AIRM URNs use `TODO(AIRM-URN)`.
- During 0.x, missing mapping or AIRM entries may be left as TODOs (§13), but
  must be listed in the change summary.

## 9. Repository layout
    CLAUDE.md
    schema/0.5/          PIXM_*.xsd (current version)
    rules/               Schematron business rules
    examples/            Example instances, one folder per scenario
    tools/               validate.py, fetch_schemas.py, lint baseline, README
    docs/guidelines/     Modelling guide, XSD patterns, examples guide, references
    docs/process/        CCB process, change log format, traceability procedures
    docs/decisions/      CCB decision records (DEC-NNNN-*.md) and open.md
    docs/changes/        CHANGELOG.md, known-defects.md
    docs/mappings/       Mappings to AIXM, FIXM, IWXXM
    docs/airm/           AIRM semantic correspondence
    docs/glossary/       Accepted community terms (§5 principle 1)
    .schema-cache/       Local copies of external schemas (git-ignored)

## 10. Commands and validation
The authoritative check is `tools/validate.py`. "Validation passed" means it
exited with no errors and no warnings beyond the baseline.

| Task | Command |
|---|---|
| Install dependencies | `pip install -r tools/requirements.txt` |
| Fetch/refresh external schema cache | `python tools/fetch_schemas.py` |
| Validate schema + all examples + lint | `python tools/validate.py` |
| Validate one example | `python tools/validate.py examples/<path>.xml` |
| Lint only | `python tools/validate.py --lint-only` |

- Run from the repository root (Python 3.12, `xmlschema`, `lxml`).
- Never commit a local path in a `schemaLocation`. `validate.py` maps the
  official URLs to `.schema-cache/` when present and falls back to the network.
- `validate.py` checks: schema compiles; every example is valid; lint of
  documentation, naming, `pixm:` prefixes, explicit occurrences, regular
  patterns (§3.4) and the units rule. Details: `tools/README.md`.
- Lint warnings are compared with `tools/lint-baseline.json` (known legacy
  issues). A change **fails** if it adds any warning not in the baseline.
  When a change fixes baseline warnings, Claude removes them from the
  baseline in the same change. Claude never adds baseline entries; only the
  CCB can approve that.

## 11. Git workflow
The CCB owns all commits. Claude edits files; it does not change git state.

### 11.1 Permitted commands
- **May** run read-only git commands: `status`, `diff`, `log`, `show`, `blame`.
- **Must not** stage, commit, amend, push, pull, merge, rebase, stash, reset,
  checkout, create or switch branches, or open pull requests, unless the CCB
  explicitly asks for that specific action.

### 11.2 Branches and scope
- All changes are made on a branch created for that task, which corresponds to
  an item in the GitHub project. Claude does not create or switch branches.
- Before starting, run `git branch --show-current` and `git status`, and confirm
  the branch matches the task. If it does not, or if there are uncommitted
  changes in files the task will touch, stop and ask.
- Make only the changes that belong to the current branch's task. If a problem
  or needed change outside that task is found, do not make it: describe it and
  ask the CCB to create a separate branch. Small related findings may be
  recorded in `docs/changes/known-defects.md` if that file is in scope.
- Each step is one logical change that can be committed on its own. Do not mix
  structural moves, defect fixes, and new model content.

### 11.3 File handling
- Preserve each file's existing encoding (UTF-8) and line endings.
- Move files normally (not `git mv`) and list old → new paths in the summary.
- Do not create scratch or temporary files in the repository (it is synced via
  OneDrive); use a temporary directory outside it.

### 11.4 End-of-step summary
1. **Files changed** (added / modified / moved / deleted).
2. **Change log lines** added in this step (§4.5).
3. **Validation result**: errors, warnings, and change versus the baseline (§10).
4. **Open items**: `TODO(CCB)`, `TODO(AIRM-URN)`, `TODO(VERIFY)`, and questions.
5. **Suggested commit message**: one summary line plus a short body.

## 12. Never
- Present unverified external names, URNs or code literals as real (§8).
- Add free text, name/value bags, `OTHER` on a new codelist, or external code
  references without CCB approval.
- Put a unit in a name, or imply a unit by convention.
- Make a property mandatory without CCB approval.
- Rename or remove anything except as allowed by §4.2 (0.x) or §6.4 (1.0+).
- Leave schema, examples and documentation disagreeing.
- Claim validation passed without running `tools/validate.py`.
- Change git state (§11).

## 13. Definition of done (0.x)
1. CCB decisions obtained for every §2 item, and recorded in `docs/decisions/`.
2. Schema changed, with `xs:documentation` on every added or touched element.
3. At least one example added or updated for the change.
4. `tools/validate.py` passes with no warnings beyond the baseline.
5. `docs/changes/CHANGELOG.md` updated (§4.5).
6. Mapping, AIRM and glossary entries added, or listed as TODOs.
7. End-of-step summary given (§11.4).

## 14. Decisions
- Decision records: `docs/decisions/DEC-NNNN-short-title.md` with context,
  options, decision, rationale, date and affected elements.
- Open questions awaiting the CCB: `docs/decisions/open.md`.
- Check both before asking the CCB anything.

## Read this when…
| When you are… | Read first |
|---|---|
| Adding or changing a type, property or codelist | `docs/guidelines/xsd-patterns.md` |
| Modelling a new concept | `docs/guidelines/modelling-guide.md` |
| Proposing reuse of another standard, or touching the AIRM | `docs/process/traceability.md` |
| Raising a CCB question, recording a decision, or writing the change log | `docs/process/ccb-process.md` |
| Writing or editing an example | `docs/guidelines/examples-guide.md` |
| Looking up an external standard | `docs/guidelines/references.md` |
