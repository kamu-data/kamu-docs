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
        f"out side by side, but couldn't find path: {ODF_PATH}")

PAGE_HEADER = """---
# !!! THIS FILE IS AUTO-GENERATED - DO NOT MODIFY MANUALLY !!!
Title: "{title}"
linkTitle: "{title}"
searchWeight: 0.5
categories: []
---

"""

INDEX_HEADER = """---
# !!! THIS FILE IS AUTO-GENERATED - DO NOT MODIFY MANUALLY !!!
Title: RFCs
linkTitle: RFCs
weight: 30
categories: []
aliases:
---

Protocol design evolution proposals:
"""


def get_summary(text):
    section_name = "## Summary"
    start = text.find(section_name)
    if start < 0:
        raise Exception(f"Unable to find section '## Summary'")
    
    start += len(section_name)
    
    end = text.find("##", start + 2)
    if end < 0:
        raise Exception(f"Unable to find section end")
    
    return text[start:end].strip()


if __name__ == "__main__":
    rfcs_dir = os.path.join(ODF_PATH, "rfcs")
    
    file_names = list(os.listdir(rfcs_dir))
    file_names.sort()

    summaries = []

    for fname in file_names:
        if fname == "000-template.md":
            continue

        src_path = os.path.join(rfcs_dir, fname)
        dst_path = os.path.join(sys.argv[1], fname)

        # Read the source
        with open(src_path) as f:
            text = f.read().strip()

        # Get title
        m = re.match(r"# (.*)", text)
        title = m.group(1)

        # Remove title
        text = text[len(m.group(0)):].strip()

        with open(dst_path, "w") as f:
            f.write(PAGE_HEADER.format(title=title))
            f.write(text)
        
        summaries.append((
            fname,
            title,
            get_summary(text)
        ))
    
    # Write index
    with open(os.path.join(sys.argv[1], "_index.md"), "w") as f:
        f.write(INDEX_HEADER)

        for fname, title, summary in summaries:
            f.write(f'- [{title}]({{{{<relref "{fname}">}}}})\n')
