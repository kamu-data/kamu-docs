#!/usr/bin/env python
import os
import sys
import json

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

ODF_SCHEMAS_PATH = os.path.join(ODF_PATH, "schemas")

# Contexts to skip entirely
SKIP_CONTEXTS = {"legacy", "metaschemas"}

PAGE_HEADER = """---
# !!! THIS FILE IS AUTO-GENERATED - DO NOT MODIFY MANUALLY !!!
title: Schemas
description: Schemas of common metadata objects
---

import {Diagram, Term, Schema, YouTube, YouTubeList} from '/components/common.jsx'

"""

# Human-readable titles for contexts
CONTEXT_TITLES = {
    "auth": "Auth",
    "config": "Config",
    "data": "Data",
    "dataset": "Dataset",
    "engine": "Engine",
    "event": "Event",
    "flow": "Flow",
    "resource": "Resource",
    "sink": "Sink",
    "source": "Source",
    "storage": "Storage",
    "task": "Task",
}


class Schema:
    def __init__(self, name, schema, path, context, version):
        self.name = name
        self.schema = schema
        self.path = path
        self.context = context
        self.version = version


class Ctx:
    def __init__(self, out, schemas_by_name, header_level, current_schema):
        self.out = out
        self.schemas_by_name = schemas_by_name
        self.header_level = header_level
        self.current_schema = current_schema

    def nest(self):
        return Ctx(
            out=self.out,
            schemas_by_name=self.schemas_by_name,
            header_level=self.header_level + 1,
            current_schema=self.current_schema,
        )

    def with_schema(self, schema):
        return Ctx(
            out=self.out,
            schemas_by_name=self.schemas_by_name,
            header_level=self.header_level,
            current_schema=schema,
        )

    def schema_id(self, name):
        return name.lower().replace("::", "")


def read_all_schemas(schemas_dir):
    """Read all schemas from context/version subdirectories, skipping excluded contexts."""
    schemas_by_name = {}
    schemas_by_context = {}

    for context in sorted(os.listdir(schemas_dir)):
        if context in SKIP_CONTEXTS:
            continue
        context_path = os.path.join(schemas_dir, context)
        if not os.path.isdir(context_path):
            continue

        schemas_by_context[context] = []

        for version in sorted(os.listdir(context_path)):
            version_path = os.path.join(context_path, version)
            if not os.path.isdir(version_path):
                continue

            for fname in sorted(os.listdir(version_path)):
                if not fname.endswith(".json"):
                    continue
                path = os.path.join(version_path, fname)
                with open(path) as f:
                    sch = json.load(f)
                name = os.path.splitext(fname)[0]
                schema = Schema(name=name, schema=sch, path=path, context=context, version=version)
                schemas_by_name[name] = schema
                schemas_by_context[context].append(schema)

    return schemas_by_name, schemas_by_context


def render_type(ctx, psch):
    """Render a property's type as a markdown string."""
    typ = psch.get("type")
    ref = psch.get("$ref")

    if typ == "array":
        items = render_type(ctx, psch["items"])
        return f"`array(`{items}`)`".replace("``", "")
    elif ref is not None:
        type_name = ref.split("/")[-1]
        return f"[`{type_name}`](#{ctx.schema_id(type_name)})"
    elif typ is not None:
        return f"`{typ}`"
    else:
        # Fallback for complex inline schemas (e.g. oneOf without $ref)
        return "`object`"


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
    elif fmt in (
        "int8", "int16", "int32", "int64",
        "uint8", "uint16", "uint32", "uint64",
        "float32", "float64",
        "path", "regex", "url", "uri",
        "date-time", "duration", "byte-size", "email",
        "resource-id", "resource-name", "type-uri", "type-ref",
        "account-id", "account-name",
        "dataset-id", "dataset-name", "dataset-alias", "dataset-ref", "dataset-ref-any",
        "did", "struct-or-string", "union-or-string", "fragment",
    ):
        return f"`{fmt}`"
    else:
        raise Exception(f"Unknown format: {fmt}")


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


def render_header(ctx, name, code=False):
    ctx.out.write("#" * ctx.header_level)
    if code:
        ctx.out.write(f" `{name}`\n")
    else:
        ctx.out.write(f" {name}\n")


def render_object(ctx, sch, name):
    render_header(ctx, name, code=True)
    ctx.out.write(sch.get("description", ""))
    ctx.out.write("\n\n")

    required = sch.get("required", [])
    properties = sch.get("properties", {})
    if properties:
        render_table(
            ctx,
            header=["Property", "Type", "Required", "Format", "Description"],
            header_fmt=["---", "---", ":---:", ":---:", "---"],
            rows=[[
                f"`{pname}`",
                render_type(ctx, psch),
                "✔️" if pname in required else "",
                render_format(psch),
                psch.get("description", "") + (
                    "\n\nDefault: `{}`".format(psch.get("default"))
                    if psch.get("default")
                    else ""
                )
            ]
                for pname, psch in properties.items()
            ]
        )
        ctx.out.write("\n")

    render_schema_links(ctx, name)


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


def render_union(ctx, sch, name):
    render_header(ctx, name, code=True)
    ctx.out.write(sch.get("description", ""))
    ctx.out.write("\n\n")

    options = list(sch["oneOf"])

    # Short-form unions have a leading string option - skip it
    if sch.get("format") == "union-or-string":
        options = [o for o in options if o.get("type") != "string"]

    rows = []
    for option in options:
        # New format: allOf with [kind-discriminator, $ref]
        if "allOf" in option:
            all_of = option["allOf"]
            ref_entry = next((e for e in all_of if "$ref" in e), None)
            if ref_entry is None:
                continue
            ref = ref_entry["$ref"]
            variant_name = ref.split("/")[-1]

            if ref.startswith("#"):
                ename = name + "::" + variant_name
                description = sch.get("$defs", {}).get(variant_name, {}).get("description", "")
            else:
                ename = variant_name
                description = ctx.schemas_by_name.get(variant_name, Schema(variant_name, {}, "", "", "")).schema.get("description", "")

            description = description.split("\n")[0]
            link = f"[`{ename}`](#{ctx.schema_id(ename)})"
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

    # Render inline $defs as sub-schemas
    for dname, dsch in sch.get("$defs", {}).items():
        render_object(ctx, dsch, name + "::" + dname)
        ctx.out.write('\n')


def render_struct_or_string(ctx, sch, name):
    """Render a struct-or-string schema: show the object variant's properties."""
    obj_variant = next(
        (o for o in sch["oneOf"] if o.get("type") == "object"),
        None
    )
    if obj_variant:
        render_object(ctx, obj_variant, name)
    else:
        render_object(ctx, sch, name)


def render_map(ctx, sch, name):
    render_header(ctx, name, code=True)
    ctx.out.write(sch.get("description", ""))
    ctx.out.write("\n\n")
    ctx.out.write("_Map of string keys to arbitrary values._\n\n")
    render_schema_links(ctx, name)


def render_scalar(ctx, sch, name):
    """Render a simple scalar schema (boolean, null, integer, etc.)."""
    render_header(ctx, name, code=True)
    ctx.out.write(sch.get("description", ""))
    ctx.out.write("\n\n")
    typ = sch.get("type", "any")
    ctx.out.write(f"_Type: `{typ}`_\n\n")
    render_schema_links(ctx, name)


def render_schema(ctx, sch):
    s = sch.schema
    name = sch.name

    if "patternProperties" in s:
        render_map(ctx, s, name)
    elif s.get("format") == "struct-or-string":
        render_struct_or_string(ctx, s, name)
    elif s.get("type") == "object":
        render_object(ctx, s, name)
    elif "oneOf" in s:
        render_union(ctx, s, name)
    elif s.get("type") == "string" and "enum" in s:
        render_enum(ctx, s, name)
    elif s.get("type") in ("boolean", "null", "integer", "number"):
        render_scalar(ctx, s, name)
    else:
        raise Exception(f"Unsupported schema shape: {name}")


def render_all(ctx, schemas_dir):
    ctx.out.write(PAGE_HEADER)

    schemas_by_name, schemas_by_context = read_all_schemas(schemas_dir)
    ctx.schemas_by_name = schemas_by_name

    for context, schemas in schemas_by_context.items():
        title = CONTEXT_TITLES.get(context, context.title())
        render_header(ctx, title)

        for sch in schemas:
            try:
                render_schema(ctx.nest().with_schema(sch), sch)
                ctx.out.write("\n")
            except Exception as ex:
                raise Exception(f"Failed to render schema: {sch.name}") from ex


if __name__ == "__main__":
    ctx = Ctx(
        out=sys.stdout,
        schemas_by_name=None,
        header_level=1,
        current_schema=None,
    )

    render_all(ctx, ODF_SCHEMAS_PATH)
