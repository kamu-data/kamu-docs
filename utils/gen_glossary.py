#!/usr/bin/env python
"""
Generates the glossary page by combining the ODF glossary (`specs/glossary.md`)
with Kamu-specific terms from `utils/glossary-extra.md`.
"""
import re

import odf

SRC_PATH = "specs/glossary.md"
GLOSSARY_EXTRA_PATH = "utils/glossary-extra.md"

PAGE_TITLE = "Glossary"
PAGE_DESCRIPTION = "Definitions of commonly used terms in Open Data Fabric and Kamu projects"


if __name__ == "__main__":
    _, odf_terms = odf.split_title(odf.read(SRC_PATH))
    odf_terms = odf.remove_section(odf_terms, "Table of Contents")

    # Drop the intro paragraph - glossary entries start from the first heading
    odf_terms = odf_terms[odf_terms.index("\n## ") + 1:]

    # Links to terms within the glossary itself are styled as terms
    odf_terms = re.sub(
        r"(?<!!)\[([^\]]+)\]\(#([^)]+)\)",
        lambda m: f'<Term t="{m.group(1)}" id="{m.group(2)}"/>',
        odf_terms,
    )
    odf_terms = odf.convert(SRC_PATH, odf_terms)

    # Read the extra glossary terms, stripping the YAML header
    with open(GLOSSARY_EXTRA_PATH) as f:
        extra = f.read().split("---", 2)[-1].strip()

    print(odf.page_header(PAGE_TITLE, PAGE_DESCRIPTION, extra="icon: arrow-down-a-z"))
    print("# Open Data Fabric\n")
    print(odf_terms.strip())
    print()
    print(extra)
