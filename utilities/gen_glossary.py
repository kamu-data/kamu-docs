#!/usr/bin/env python
import os
import re
import sys
import subprocess

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
        f"out side by side, but couldn't find path: {odf_tools_path}")

GLOSSARY_EXTRA_PATH = "content/glossary/extra.md"

IMAGES_DIR = "static/images/pages/glossary"
IMAGES_URL = "/images/pages/glossary/"

PAGE_HEADER = """---
# !!! THIS FILE IS AUTO-GENERATED - DO NOT MODIFY MANUALLY !!!
Title: Glossary
description: Definitions of commonly used terms in Open Data Fabric and Kamu projects
weight: 50
topLevelElement: true
categories: []
aliases:
---
"""


def id_of(name):
    return name.lower().replace(" ", "-")


if __name__ == "__main__":
    # Read the spec source
    with open(os.path.join(ODF_PATH, "src/open-data-fabric.md")) as f:
        spec = f.read()
    
    # Extract "Concepts" section
    section_name = "# Concepts and Components"
    following_section_name = "# Specification"

    start = spec.find(section_name)
    if start < 0:
        raise Exception(f"Unable to find section '{section_name}'")
    else:
        start = start + len(section_name)
    
    end = spec.find(following_section_name)
    if end < 0:
        raise Exception(f"Unable to find section '{following_section_name}'")

    section = spec[start:end].strip()

    # Read the extra glossary terms
    with open(GLOSSARY_EXTRA_PATH) as f:
        extra = f.read()

        # Strip YAML header
        extra = extra.split("---", 2)[-1].strip()
    
    # Combine ODF terms and extra
    section = f"""
# Open Data Fabric
{section}

{extra}"""

    # Substitute or glossary links with a styled version
    # Fix the rest of the links to point to the spec document
    terms = {
        m.group(1)
        for m in re.finditer(r"^###? (.+)", section, flags=re.MULTILINE)
    }
    term_links = {
        id_of(t)
        for t in terms
    }

    def sub_refs(m):
        t = m.group(1)
        url = m.group(2)
        if url in term_links:
            return f'{{{{<term "{t}" "{url}">}}}}'
        elif url.endswith("-schema") and url != "common-data-schema":
            t = t.strip('`')
            schema = url.removesuffix("-schema").removeprefix("#")
            return f'{{{{<schema "{t}" "{schema}">}}}}'
        elif url.startswith("reference-"):
            t = t.strip('`')
            schema = url.removeprefix("reference-")
            return f'{{{{<schema "{t}" "{schema}">}}}}'
        else:
            return f'[{t}]({{{{<relref "spec#{url}">}}}})'

    section = re.sub(r"\[([^]]+)\]\(#([^)]+)\)", sub_refs, section)

    # Clean up old images
    subprocess.run(
        f"mkdir -p {IMAGES_DIR}",
        shell=True,
        check=True,
    )
    subprocess.run(
        f"rm -f {IMAGES_DIR}/*",
        shell=True,
        check=True,
    )

    # Copy images and fix up URLs
    def sub_images(m):
        alt = m.group(1)
        file_name = os.path.basename(m.group(2))
        src_path = os.path.join(ODF_PATH, m.group(2))
        dst_path = os.path.join(IMAGES_DIR, file_name)
        subprocess.run(
            f'cp "{src_path}" "{dst_path}"',
            shell=True,
            check=True,
        )
        return f'{{{{<image filename="{IMAGES_URL}{file_name}" alt="{alt}">}}}}'

    section = re.sub(r"!\[(.+)\]\((.+)\)", sub_images, section)

    print(PAGE_HEADER)
    print(section)
