# Writing PIXM examples

Rules are in CLAUDE.md §7; this guide covers how.

## Folder and file names
- One folder per scenario under `examples/`, e.g. `Example 3 - Landing Exits and Departure Ints`.
- Letters, digits, spaces and hyphens only in folder names.
- File names describe the message and variant, e.g. `takeoffRequest-28R-base.xml`.

## Header comment
Every example starts with a comment like:

```xml
<!--
  Purpose:   Takeoff request for runway 28R, baseline configuration.
  Scenario:  Example 1 - Airspace Coordination - Takeoff.
  PIXM:      0.5
  Exercises: TakeoffRequest, TakeoffRunwaySettings, TakeoffEnvironmentalSettings.
  Data:      Illustrative only, based on a real aerodrome. Not for operational use.
  Mapping:   (optional) legacy source fields → PIXM elements, e.g. TOLD card or SNOWTAM.
-->
```

## Content
- Use `uom` on every measure that has one.
- Use `nilReason` to show a deliberately absent value; never sentinel values.
- Keep at least one example that sends a single block on its own (e.g. only an
  aircraft configuration) to show the block is interpretable without a parent.
- When a value comes from a legacy or operational format (TOLD card, SNOWTAM),
  record the mapping in the header comment.

## schemaLocation
Point at the schema by a path relative to the example file (e.g.
`../../schema/0.5/PIXM_Features.xsd`) and at external schemas by their official
online URL. `tools/validate.py` resolves both.

## Validation
`python tools/validate.py examples/<folder>/<file>.xml`
