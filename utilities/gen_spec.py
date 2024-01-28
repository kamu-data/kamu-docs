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

IMAGES_DIR = "static/images/pages/spec"
IMAGES_URL = "/images/pages/spec/"

PAGE_HEADER = """---
# !!! THIS FILE IS AUTO-GENERATED - DO NOT MODIFY MANUALLY !!!
Title: Open Data Fabric
linkTitle: Specification
description:
weight: 10
categories: []
---
"""


def id_of(name):
    return name.lower().replace(" ", "-")

def remove_section(spec, section_name, following_section_name=None):
    start = spec.find(section_name)
    if start < 0:
        raise Exception(f"Unable to find section '{section_name}'")
    
    if following_section_name is not None:
        end = spec.find(following_section_name)
        if end < 0:
            raise Exception(f"Unable to find section '{following_section_name}'")
    else:
        end = len(spec)

    return spec[:start].strip() + "\n\n" + spec[end:].strip()


if __name__ == "__main__":
    # Read the spec source
    with open(os.path.join(ODF_PATH, "src/open-data-fabric.md")) as f:
        text = f.read()
    
    # Remove title
    text = text.removeprefix("# Open Data Fabric").strip()

    text = remove_section(text, "# Table of Contents", "# Requirements")

    text = remove_section(text, "# Reference Information")
    
    # Fix up links
    def map_link(m):
        t = m.group(1)
        url = m.group(2)

        if url.startswith("/rfcs/"):
            rfc = url.removeprefix("/rfcs/")
            return f'[{t}]({{{{<relref "{rfc}">}}}})'
        elif url.startswith("#") and url.endswith("-schema") and url != "#common-data-schema":
            t = t.strip('`')
            schema = url.removesuffix("-schema").removeprefix("#")
            return f'{{{{<schema "{t}" "{schema}">}}}}'
        elif url.startswith("#reference-"):
            t = t.strip('`')
            schema = url.removeprefix("#reference-")
            return f'{{{{<schema "{t}" "{schema}">}}}}'
        else:
            return f'[{t}]({url})'

    text = re.sub(r"\[([^]]+)\]\(([^)]+)\)", map_link, text)

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

    text = re.sub(r"!\[(.+)\]\((.+)\)", sub_images, text)

    print(PAGE_HEADER)
    print(text)
