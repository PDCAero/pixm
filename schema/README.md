# PIXM schema files

Current version: **0.5** (pre-release). Namespace: `http://www.pixm.aero/schema/0.5`, prefix `pixm:`.
Schema files live in `schema/<version>/`.

Keep this file up to date whenever schema files are added, split, renamed or moved.

| File | Contents | Depends on |
|---|---|---|
| `PIXM_AbstractGML_ObjectTypes.xsd` | Abstract feature, time-slice, message, object and extension base types | GML 3.2, ISO 19139 gmd |
| `PIXM_Codelists.xsd` | `Code…BaseType` enumerations | — |
| `PIXM_DataTypes.xsd` | `Code…Type` / `Text…Type` wrappers with `nilReason` | Codelists, GML |
| `PIXM_UoM.xsd` | `Uom…Type` unit lists | — |
| `PIXM_Measures.xsd` | `Val…BaseType` / `Val…Type` measures with `uom` and `nilReason` | UoM, DataTypes, GML |
| `PIXM_Features.xsd` | All features and their time slices | All of the above (and, until removed, AIXM 5.1.1) |
| `PIXM_Messages.xsd` | Request, response and notification (unsolicited message) bases, and the simple runway status request, response and message | `PIXM_Features.xsd` |

## External schemas

| Namespace | Official location |
|---|---|
| GML 3.2 | `http://schemas.opengis.net/gml/3.2.1/gml.xsd` |
| ISO 19139 gmd | `http://schemas.opengis.net/iso/19139/20070417/gmd/gmd.xsd` |
| AIXM 5.1.1 | `https://aixm.aero/schema/5.1.1/AIXM_Features.xsd`: imported by `PIXM_Features.xsd` only, for `aixm:RunwayDirectionPropertyType` (scheduled for removal, see `docs/changes/known-defects.md`). |

For offline development, `python tools/fetch_schemas.py` caches these in `.schema-cache/` (git-ignored).
