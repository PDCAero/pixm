# Traceability to other standards and the AIRM

Rules: CLAUDE.md §5 (principles 7–8) and §8.

## 1. Checking other standards
For every new concept, look for an equivalent in AIXM, FIXM, IWXXM, AMXM, and
GML / ISO 19100 for geometry and time. If one exists, raise a Reuse / Adapt /
Ignore request (`ccb-process.md`) including: source element path, version,
definition, type/units, and any gap in meaning.

If the CCB chooses **Adapt**, keep literals and definitions aligned with the
source where possible and record the mapping.

Never cite an external element name, URN or literal from memory as fact. Verify
it against the published XSD/UML/documentation, or mark it `TODO(VERIFY)`.

## 2. Mapping tables
File: `docs/mappings/<standard>-<version>.md`, e.g. `aixm-5.1.1.md`, `fixm-4.3.md`.

| PIXM element | Source element path | Relationship | Notes | Decision |
|---|---|---|---|---|
| `pixm:…` | `aixm:…` | equivalent / broader / narrower / partial / none | … | DEC-NNNN |

## 3. AIRM semantic correspondence
File: `docs/airm/semantic-correspondence.md`. Record the AIRM version used at the top.

| PIXM element | AIRM URN | Correspondence | Rationale |
|---|---|---|---|
| `pixm:…` | `urn:aero:airm:<version>:…` | equivalent / specialisation / generalisation / partial / no correspondence | … |

- Pure container or grouping elements need no direct correspondence; note them as such.
- For "no correspondence", record proposed AIRM wording; these are AIRM change-request candidates.
- Verify URNs against the published AIRM (airm.aero). Never invent one; use `TODO(AIRM-URN)`.
- Intentional deviations from an AIRM definition are flagged to the CCB and recorded here with the rationale.

## 4. During 0.x
Missing mapping or AIRM entries may be left as TODOs, but each change summary
lists them.
