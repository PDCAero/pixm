# CCB process

How Claude raises questions to the PIXM Change Control Board (CCB), records
decisions, and keeps the change log. Rules: CLAUDE.md §2, §4.5, §14.

## 1. Raising a decision request

Short and decision-ready: what is needed, the options with pros and cons, the
AIRM position, and a recommendation.

> **CCB decision needed: runway condition input**
> PIXM needs per-third runway condition for landing performance. AIXM 5.2 has a
> runway-section contamination structure (runway condition code, depth + uom,
> proportion, layer type). `TODO(VERIFY)`: exact AIXM 5.2 element names.
> Options:
> **(A) Reuse**: import the AIXM type by reference. Pros: no mapping. Cons: brings in the AIXM schema dependency PIXM has removed.
> **(B) Adapt**: define a PIXM runway-section condition type with the same meaning and AIXM-compatible literals, plus a documented mapping. Pros: standalone. Cons: a mapping to maintain.
> **(C) Ignore**: model independently.
> AIRM: `TODO(AIRM-URN)`; no deviation for A or B.
> Recommendation: B.

Before asking, check `docs/decisions/` and `docs/decisions/open.md`.

## 2. Decision records

File: `docs/decisions/DEC-NNNN-short-title.md`, numbered in order.

```markdown
# DEC-NNNN: Short title

- Date: YYYY-MM-DD
- Status: Decided | Superseded by DEC-NNNN
- Affected elements: …

## Context
## Options considered
## Decision
## Rationale
```

When a decision answers an item in `open.md`, remove it from there.

## 3. Change log

`docs/changes/CHANGELOG.md`. Every change to the schema or examples is recorded
in the same change, one line per change, plain language, no narrative.

```markdown
## 0.5 (unreleased)

### 2026-11-20 — Known-defect fixes
- FIX     PIXM_Features: `V2VSRatio` → `v2VSRatio` (capitalisation). Compat: rename.
- CHANGE  PIXM_Measures: `ValDistanceType/@uom` optional → required. Compat: breaking.
- ADD     PIXM_Features: `RunwayDirectionReferenceType`. Compat: none.
- REMOVE  PIXM_Features: AIXM 5.1.1 import. Compat: breaking. Ref: DEC-0002.
- DOC     PIXM_Codelists: definitions added to `CodeAntiSkidSettingBaseType`. Compat: none.
```

Rules:
- **Tag**: `ADD`, `CHANGE`, `RENAME`, `FIX`, `REMOVE`, `DEPRECATE`, `DOC`.
  `FIX` covers typo/capitalisation renames and corrections that keep the meaning.
- **Location**: file (without extension) and element or type, in backticks.
- **What**: old → new where something changed.
- **Compat**: `none` (additive or documentation), `rename` (same meaning, new
  name), `breaking` (existing valid data may become invalid or change meaning).
  From 1.0, use the AIXM-style classification: no mapping needed / mapping
  without loss / mapping with loss.
- **Ref**: `DEC-NNNN` when a CCB decision applied.
- Fix-on-touch changes are logged like any other.
- Bulk mechanical changes may be one line with a count (e.g. `DOC PIXM_Codelists:
  definitions added to 12 codelists`), but never hide a breaking change in a bulk line.
- Group entries under the version being worked on, newest first, with a dated
  heading per step.
