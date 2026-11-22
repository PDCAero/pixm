# Open CCB decisions

Questions awaiting the CCB. When one is decided, record it as a `DEC-NNNN`
file and remove it from this list.

| # | Question | Raised | Notes |
|---|---|---|---|
| 1 | Target AIRM version for traceability | 2026-11-19 | |
| 2 | Target FIXM and IWXXM versions for mappings | 2026-11-19 | |
| 3 | Initial list of accepted community terms and their casing (`docs/glossary/accepted-terms.md`) | 2026-11-19 | e.g. `vRef` vs `vref`, `vMCG` vs `vmcg` |
| 4 | Confirm namespace URI `http://www.pixm.aero/schema/0.5` (domain ownership and form) | 2026-11-19 | |
| 5 | UML tool and source format | 2026-11-19 | Deferred until UML work starts |
| 6 | Structure of the PIXM reference type replacing `aixm:RunwayDirectionPropertyType` | 2026-11-19 | Decided in principle (DEC-0001: port to PIXM); structure to approve on the `known-defects` branch |
| 7 | Rename `AircraftConfigurationExtension` / `LandingAircraftConfigurationExtension` (features, not extensions) | 2026-11-19 | |
| 8 | Review of properties currently mandatory (`minOccurs="1"`, 69 in `PIXM_Features`) against the optional-by-default principle | 2026-11-19 | Multiplicity changes need CCB approval |
| 9 | How PIXM time-slice interpretations are intended to be used | 2026-11-19 | For the modelling guide |
| 11 | Examples: replace the existing examples entirely with new compliant ones, or keep and fix them (known defect E9) | 2026-11-20 | Leaning to replace (CCB, 2026-11-20); to be decided on the examples task |
| 12 | Feature vs object: which PIXM concepts are time-sliced features and which are objects without time slices (static or embedded data)? | 2026-11-20 | All 62 types are features today; `AbstractPIXMObjectType` exists but is unused; ~60 properties embed whole features. Objects cannot be sent alone as GML features (principle 4). Includes the request/response/notification bases in `PIXM_Messages`, the interpretation of request time slices, and aligning `TakeoffRequest`/`LandingRequest` with those bases (DEC-0004). Separate task |
