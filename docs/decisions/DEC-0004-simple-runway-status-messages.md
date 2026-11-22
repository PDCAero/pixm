# DEC-0004: Simple runway status messages

- Date: 2026-11-21
- Status: Decided
- Affected elements: `PIXM_Messages` (all types); `CodeAirportHeliportDesignatorBaseType` / `CodeAirportHeliportDesignatorType` in `PIXM_DataTypes`

## Context
`PIXM_Messages.xsd` and its examples were ported from the unmerged 0.1 branch
`simple-runway-status`. After the mechanical port (namespace 0.5, DEC-0003
wrappers), the content still used AIXM types, `xs:boolean`, `xs:dateTime`,
free text and an undefined integer code, and its abstract bases overlapped
open question #12 (feature vs object) and the existing `AbstractPIXMMessageType`.

## Options considered and decisions
1. **Designators.** Options: port to PIXM; xlink reference to AIXM features;
   keep the AIXM import. **Decided: port.** `runwayEndId` → `runwayDirectionDesignator`
   (`pixm:TextDesignatorType`, already in PIXM); `airportId` → `aerodromeDesignator`
   (new `pixm:CodeAirportHeliportDesignatorType`, copied from AIXM 5.1.1: 3–6
   upper-case letters or digits). `PIXM_Messages` no longer imports AIXM.
2. **Yes/no and timestamps.** Options: `CodeYesNoType` + `DateTimeType`; a
   per-operation status codelist; keep `xs:boolean`. **Decided: `CodeYesNoType`
   + `DateTimeType`** for `openLanding`, `openTakeoff`, `success`,
   `provideNextExpectedChange`, `requestTimestamp`, `responseTimestamp`, `timeInstant`.
3. **Errors and service status.** Options: closed codelists plus bounded text;
   reuse the `ErrorMessage` feature; keep as ported. **Decided: keep as ported.**
   `errorMessage` stays free text (`xs:string`) and `serviceStatusCode` stays an
   `xs:positiveInteger` whose values PIXM does not define (CCB exception to
   principles 2 and §6.2 primitives).
   The two resulting `PRIMITIVE` lint warnings were added to
   `tools/lint-baseline.json` (CCB approval, 2026-11-21).
4. **Framework.** Options: keep features and defer to #12; keep unchanged;
   resolve #12 first. **Decided: keep requests, responses and notifications as
   time-sliced features; their feature-vs-object status, the interpretation of
   request time slices, and alignment of `TakeoffRequest`/`LandingRequest` with
   these bases are part of open #12.** Bases renamed to AIXM style:
   `PIXMRequest` → `AbstractPIXMRequest`, `PIXMResponse` → `AbstractPIXMResponse`,
   and `PIXMMessage` → `AbstractPIXMNotification` (not `AbstractPIXMMessage`,
   which would clash with the existing message container `AbstractPIXMMessageType`).
   The concrete `SimpleRunwayStatusMessage` keeps its name.

## Rationale
Porting the designators follows DEC-0001 (port, do not reference AIXM) and avoids
growing the AIXM dependency that known defect S1 removes. `CodeYesNoType` and
`DateTimeType` follow principle 2 and §6.2 without changing meaning. Error and
status modeling and the request/response structure are deferred so the runway
status exchange can be used now without pre-empting #12.
