#!/usr/bin/env python
import os
import sys

# Locate `open-data-fabric` repo
ODF_URL = "https://github.com/open-data-fabric/open-data-fabric/"
ODF_PATH = os.path.normpath(
    os.path.join(
        os.path.dirname(__file__),
        "../../open-data-fabric"
    )
)
if not os.path.exists(ODF_PATH):
    raise Exception(
        f"Expecting to have `open-data-fabric` repository checked "
        f"out side by side, but couldn't find path: {ODF_PATH}")

# Import helpers
sys.path.append(os.path.join(ODF_PATH, "tools"))
import utils.schemas

ODF_SCHEMAS_PATH = os.path.join(ODF_PATH, "schemas")

PAGE_HEADER = """---
# !!! THIS FILE IS AUTO-GENERATED - DO NOT MODIFY MANUALLY !!!
Title: Reference
description: Schemas of common metadata objects
weight: 20
categories: []
aliases:
---

"""


class Ctx:
    def __init__(self, out, schemas, header_level, current_schema):
        self.out = out
        self.schemas = schemas
        self.header_level = header_level
        self.current_schema = current_schema

    def nest(self):
        return Ctx(
            out=self.out,
            schemas=self.schemas,
            header_level=self.header_level + 1,
            current_schema=self.current_schema,
        )

    def with_schema(self, schema):
        return Ctx(
            out=self.out,
            schemas=self.schemas,
            header_level=self.header_level,
            current_schema=schema,
        )

    def section_id(self, name):
        id = name.lower().replace(" ", "-")
        return f"reference-{id}"

    def schema_id(self, name):
        return name.lower().replace("::", "")


def render_type(ctx, sch):
    typ = sch.get("type")
    if typ == "array":
        items = render_type(ctx, sch["items"])
        typ = f"`array(`{items}`)`"
    elif typ is None:
        typ = sch["$ref"].split("/")[-1]
        typ = f"[`{typ}`](#{ctx.schema_id(typ)})"
    else:
        typ = f"`{typ}`"
    return typ.replace("``", "")


def render_format(sch):
    external_formats = {
        "flatbuffers": "https://flatbuffers.dev/",
        "date-time": "https://json-schema.org/draft/2019-09/json-schema-validation.html#rfc.section.7.3.1",
        "multihash": "https://github.com/multiformats/multihash",
        "multicodec": "https://github.com/multiformats/multicodec",
    }
    fmt = sch.get("format")
    if fmt is None:
        return ""
    elif fmt in external_formats:
        url = external_formats[fmt]
        return f"[`{fmt}`]({url})"
    elif fmt in ("dataset-id", "dataset-name", "dataset-alias", "dataset-ref", "dataset-ref-any"):
        return f"[`{fmt}`]({{{{<relref \"spec#dataset-identity\">}}}})"
    elif fmt in ("int32", "uint32", "int64", "uint64", "path", "regex", "url", "flatbuffers"):
        return f"`{fmt}`"
    else:
        raise Exception(f"Unknown format: {fmt}")


def render_union(ctx, sch, name):
    render_header(ctx, name, code=True)
    ctx.out.write(sch.get("description", ""))
    ctx.out.write("\n\n")

    rows = []
    for option in sch["oneOf"]:
        option_id = option["$ref"].split("/")[-1]

        if option["$ref"].startswith("#"):
            ename = name + "::" + option_id
        else:
            ename = option_id

        link = f"[`{ename}`](#{ctx.schema_id(ename)})"

        description = option.get("description", "")
        if not description:
            if option["$ref"].startswith("#"):
                description = sch["$defs"][option_id].get("description", "")
            else:
                description = ctx.schemas[option_id].schema.get("description", "")
        description = description.split("\n")[0]
        rows.append((link, description))

    render_table(
        ctx,
        header=["Union Type", "Description"],
        header_fmt=["---", "---"],
        rows=rows
    )
    ctx.out.write('\n')

    render_schema_links(ctx, name)

    ctx.out.write('\n')

    for dname, dsch in sch.get("$defs", {}).items():
        render_object(ctx, dsch, name + "::" + dname)
        ctx.out.write('\n')


def render_enum(ctx, sch, name):
    render_header(ctx, name, code=True)
    ctx.out.write(sch.get("description", ""))
    ctx.out.write("\n\n")

    render_table(
        ctx,
        header=["Enum Value"],
        header_fmt=[":---:"],
        rows=[(f"`{val}`",) for val in sch["enum"]]
    )
    ctx.out.write('\n')

    render_schema_links(ctx, name)


def render_table(ctx, header, header_fmt, rows):
    ctx.out.write("| " + " | ".join(header) + " |\n")
    ctx.out.write("| " + " | ".join(header_fmt) + " |\n")

    for values in rows:
        ctx.out.write("| " + " | ".join([
            v.replace("\n", "<br/>")
            for v in values
        ]) + " |\n")


def render_schema_links(ctx, name):
    rel_path = os.path.relpath(ctx.current_schema.path, ODF_SCHEMAS_PATH)
    ctx.out.write(
        f"[![JSON Schema](https://img.shields.io/badge/schema-JSON-orange)]"
        f"({ODF_URL}tree/master/schemas/{rel_path})\n")
    ctx.out.write(
        f"[![Flatbuffers Schema](https://img.shields.io/badge/schema-flatbuffers-blue)]"
        f"({ODF_URL}tree/master/schemas-generated/flatbuffers/opendatafabric.fbs)\n"
    )


def render_object(ctx, sch, name):
    render_header(ctx, name, code=True)
    ctx.out.write(sch.get("description", ""))
    ctx.out.write("\n\n")

    if sch["properties"]:
        render_table(
            ctx,
            header=["Property", "Type", "Required", "Format", "Description"],
            header_fmt=["---", "---", ":---:", ":---:", "---"],
            rows=[[
                f"`{pname}`",
                render_type(ctx, psch),
                "✔️" if pname in sch["required"] else "",
                render_format(psch),
                psch.get("description", "")
            ]
                for pname, psch in sch["properties"].items()
            ]
        )
        ctx.out.write("\n")

    render_schema_links(ctx, name)


def render_extensions(ctx, sch, name):
    render_header(ctx, name, code=True)
    ctx.out.write(sch.get("description", ""))
    ctx.out.write("\n")

    ctx.out.write("""
### Known Extensions

| Extension | Description |
| --- | --- |
| `opendatafabric.net/description` | Used for human readable schema field descriptions |
| `opendatafabric.net/type` | An extended set of logical types that ODF recommends but does not require every implementation to support |
| `opendatafabric.org/linkedObjects` | When attached to `AddData` event contains a summary of how many external objects were associated with a certain transaction as well as their size |
| `arrow.apache.org/bufferEncoding` | Used to accurately represent buffer encoding type when converting Arrow schema to ODF schema |
| `arrow.apache.org/dateEncoding` | Used to accurately represent date encoding type when converting Arrow schema to ODF schema |
| `arrow.apache.org/decimalEncoding` | Used to accurately represent decimal encoding type when converting Arrow schema to ODF schema |
""")
    
    ctx.out.write("""
### Known Extended Types

| Extended Type | Core Type | Description |
| --- | --- | --- |
| `Did` | `String` | Decentralized identifier `did:<method>:<id>` |
| `Multihash` | `String` | Hash in self-describing [multihash](https://github.com/multiformats/multihash) format |
| `ObjectLink` | `String` | Signifies that the value references an external object. The mandatory `linkType` property defines the type of the link (e.g. `Multihash`). |
""")
    
    ctx.out.write("\n")
    render_schema_links(ctx, name)


def render_schema(ctx, sch):
    if "patternProperties" in sch.schema:
        render_extensions(ctx, sch.schema, sch.name)
    elif sch.schema.get("type") == "object":
        render_object(ctx, sch.schema, sch.name)
    elif "oneOf" in sch.schema:
        render_union(ctx, sch.schema, sch.name)
    elif sch.schema.get("type") == "string" and "enum" in sch.schema:
        render_enum(ctx, sch.schema, sch.name)
    else:
        raise Exception(f"Unsupported type: {sch}")


def render_header(ctx, name, code=False):
    ctx.out.write("#" * ctx.header_level)
    if code:
        ctx.out.write(f" `{name}`\n")
    else:
        ctx.out.write(f" {name}\n")


def schemas_by_kind(schemas, kind, priority=()):
    filtered = [s for s in schemas.values() if s.kind == kind]
    filtered.sort(key=lambda x: x.name)

    for p in reversed(priority):
        for i in range(len(filtered)):
            if filtered[i].name == p:
                s = filtered.pop(i)
                filtered.insert(0, s)
                break

    return filtered


def render_all(ctx, schemas_dir):
    ctx.out.write(PAGE_HEADER)

    def render_section(ctx, name, kind, priority=()):
        render_header(ctx, name)
        for sch in schemas_by_kind(ctx.schemas, kind, priority):
            try:
                render_schema(ctx.nest().with_schema(sch), sch)
                ctx.out.write("\n")
            except Exception as ex:
                raise Exception(f"Failed to render schema: {sch.name}") from ex

    schemas = utils.schemas.read_schemas(schemas_dir)
    ctx.schemas = schemas

    render_section(ctx, "Manifests", "root", ["Manifest"])
    render_section(ctx, "Metadata Events", "metadata-event", ["MetadataEvent"])
    render_section(ctx, "Data Schema", "data-schema", ["DataSchema", "DataField"])
    render_section(ctx, "Engine Protocol", "engine-op")
    render_section(ctx, "Fragments", "fragment")


if __name__ == "__main__":
    ctx = Ctx(
        out=sys.stdout,
        schemas=None,
        header_level=1,
        current_schema=None,
    )

    render_all(ctx, ODF_SCHEMAS_PATH)
