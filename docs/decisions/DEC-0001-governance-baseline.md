# DEC-0001: Governance baseline for CLAUDE.md

- Date: 2026-11-19
- Status: Decided
- Affected elements: CLAUDE.md; whole schema (conventions); examples; repository layout

## Context
A new CLAUDE.md was written as if PIXM were a new model, but the repository
already contains a v0.x schema with established patterns. Several rules
conflicted with the existing schema. The CCB reviewed each conflict.

## Decisions
| # | Topic | Decision |
|---|---|---|
| 1 | Model style | AIXM 5.1.1 GML feature/time-slice model is settled; migration to AIXM 5.2 planned. |
| 2 | Source of truth | XSD is normative; UML deferred and later generated from the XSD. |
| 3 | Legacy content | Fix on touch. During 0.x, typo/capitalisation renames allowed without asking; from 1.0 all renames need CCB approval. |
| 4 | Type naming | Keep AIXM style: `Code…BaseType`/`Code…Type`, `Val…BaseType`/`Val…Type`, `Uom…Type`, `Text…Type`. |
| 5 | Missing values | `gml:NilReasonEnumeration`. |
| 6 | `OTHER` | All existing `OTHER(:text)` codelist patterns grandfathered; new codelists closed by default. |
| 7 | Version | 0.5 pre-release; breaking changes allowed and logged until 1.0. Namespace changes to `http://www.pixm.aero/schema/0.5`; schema folder `schema/0.5/`. |
| 8 | Schema files | Keep a single feature file for now; revisit split at 1.0 or AIXM 5.2 migration. |
| 9 | Layout | Adopt the full repository layout in CLAUDE.md §9 (excluding `uml/`, `docs/primer/`, `docs/data-dictionary/` until needed). |
| 10 | External imports | Published schemas use official online `schemaLocation`s; local cache for development only. |
| 11 | Validation | `tools/validate.py` (Python, xmlschema) is authoritative; a change fails only if it adds lint warnings beyond the recorded baseline. |
| 12 | Examples | Real aerodromes allowed with an illustrative-data statement; folder names without `&`; namespaces and paths fixed. |
| 13 | Definition of done (0.x) | CCB decisions, valid XSD, documentation, validating example, change log; mappings/AIRM/glossary may be TODOs. |
| 14 | Git | Claude edits only; the CCB commits. Work happens on a task branch; unrelated changes need a separate branch. |
| 15 | Known defects | Fixed as the first task after CLAUDE.md adoption and the layout move. |
| 16 | Units | `uom` required whenever a quantity can be expressed in more than one unit or scale; only dimensionless quantities omit it. |
| 17 | AIXM dependency | Port the single AIXM type used (`aixm:RunwayDirectionPropertyType`) to a PIXM reference type and remove the AIXM import. |
| 18 | Spelling | US spelling unless in conflict with an AIRM term. |
| 19 | Extensions | Extension hooks added to a feature only when a stakeholder need is identified, with CCB approval. |
| 20 | CLAUDE.md scope | Performance-calculation guidance is not a general rule (PIXM will be wider); kept in the modelling guide only. |

## Rationale
Align the working instructions with the schema as it exists, keep pre-release
flexibility while making every change reviewable, and keep CLAUDE.md to rules
needed on every task.
