# PIXM tools

Python 3.12+. Install once: `pip install -r tools/requirements.txt`. Run from the repository root.

| Script | Purpose |
|---|---|
| `validate.py` | Authoritative validation: schema compiles, examples valid, schema lint, compared with the baseline |
| `fetch_schemas.py` | Downloads external schemas (GML, ISO 19139, AIXM) into `.schema-cache/` for offline validation |
| `schema_cache.py` | Shared helper: cache location and URL mapping |

## validate.py

```
python tools/validate.py                      # full run
python tools/validate.py examples/X/file.xml  # schema + lint + only these examples
python tools/validate.py --lint-only          # lint only (fast, no compilation)
python tools/validate.py --show-known         # also list findings already in the baseline
python tools/validate.py --prune-baseline     # remove baseline entries that no longer occur
python tools/validate.py --init-baseline      # create the baseline (only if none exists)
```

**Result:** `PASS` when every finding is in `lint-baseline.json`; `FAIL` (exit code 1)
when anything new appears. Fixed entries are reported; remove them with
`--prune-baseline` in the same change. Never add entries to the baseline without CCB
approval (CLAUDE.md §10).

Baseline keys contain the rule, file and message, but no line numbers, so
unrelated edits that move lines do not create new findings.

### External schemas
Schema `schemaLocation`s point to official online URLs. `validate.py` maps them to
`.schema-cache/` (and fetches the cache automatically if it is missing). Downloads
verify TLS with the `certifi` trust store.

### Checks

| Rule | Severity | What it checks |
|---|---|---|
| `SCHEMA` | error | `schema/0.5/PIXM_Features.xsd` and everything it includes/imports compiles |
| `FETCH` | error | An external schema could not be downloaded |
| `WELLFORMED` | error | A schema or example file is not well-formed XML |
| `EXAMPLE` | error | An example is not valid against the schema |
| `DOC` | warning | Named global type, property (local element) or enumeration literal has no `xs:documentation` |
| `NAME-TYPE` | warning | Type name is not UpperCamelCase ending in `Type` |
| `NAME-PROP` | warning | Property name is not lowerCamelCase |
| `NAME-LITERAL` | warning | Enumeration literal is not UPPER_SNAKE_CASE |
| `OCCURS` | warning | Property without explicit `minOccurs` and `maxOccurs` |
| `ANON` | warning | Property with an anonymous inline type |
| `PRIMITIVE` | warning | Property typed directly with an XSD primitive (`xs:string`, `xs:int`, …) |
| `PREFIX` | warning | Reference to a PIXM component without the `pixm:` prefix |
| `PAIR` | warning | Incomplete pattern: `Code/Val/Text…BaseType` without `…Type` (or the reverse); time-slice type without feature type or global elements; global element without `substitutionGroup` |
| `UNITS` | warning | Measure `uom` not `use="required"`; measure without `uom` not documented as dimensionless |

Lint applies to `schema/0.5/*.xsd` only. Anonymous member types inside `xs:union`
(the codelist pattern) are not flagged.
