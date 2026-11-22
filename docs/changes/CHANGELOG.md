# PIXM change log

One line per change to the schema or examples. Format: `docs/process/ccb-process.md` §3.

## 0.5 (unreleased)

### 2026-11-20 — AIXM time-slice structure (DEC-0003)
- ADD     PIXM_Features: `…TimeSlicePropertyType` for all 61 features (contains one `…TimeSlice`). Compat: none.
- CHANGE  PIXM_Features: `timeSlice` on all 61 features `…TimeSliceType` → `…TimeSlicePropertyType`. Compat: breaking. Ref: DEC-0003.
- RENAME  PIXM_AbstractGML_ObjectTypes: element `AbstractPIXMTimeSliceType` → `AbstractPIXMTimeSlice`; all 61 `substitutionGroup`s updated. Compat: rename.
- CHANGE  PIXM_AbstractGML_ObjectTypes: `AbstractPIXMTimeSlice` added to substitution group `gml:AbstractTimeSlice`. Compat: none.
- DOC     PIXM_Features: definitions and explicit `minOccurs`/`maxOccurs` on the 61 `timeSlice` properties (fix on touch). Compat: none.

### 2026-11-20 — Repository layout and namespace 0.5
- CHANGE  all schema files: namespace `http://www.pixm.aero/schema/0.1` → `http://www.pixm.aero/schema/0.5`. Compat: breaking.
- CHANGE  all schema files: moved `schema/` → `schema/0.5/`; `PIXM_Features.XSD` and `PIXM_Codelists.XSD` → lower-case `.xsd`. Compat: none (file location only).
- CHANGE  PIXM_Features: AIXM 5.1.1 import `schemaLocation` → `https://aixm.aero/schema/5.1.1/AIXM_Features.xsd` (was a path outside the repo). Compat: none.
- FIX     examples (all): namespace → `…/schema/0.5` (Example 3 was `http://www.pixm.aero/pixm/1.0`). Compat: none.
- FIX     examples (all): `schemaLocation` → relative path to `schema/0.5/PIXM_Features.xsd`; added where missing (Example 2, Example 3); local GML path → official URL (`temporal_example.xml`). Compat: none.
- CHANGE  examples: folder `Example 3 - Landing Exits & Departure Ints` → `Example 3 - Landing Exits and Departure Ints`. Compat: none.

### 2026-11-19 — Governance baseline (DEC-0001)
- CHANGE  PIXM_DataTypes: `TextSettingBaseType` maxLength 80 added. Compat: breaking.
