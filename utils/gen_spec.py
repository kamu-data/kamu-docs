#!/usr/bin/env python
"""
Generates ODF specification pages from `specs/` directory of the ODF repository.

Specs are rendered into `odf/spec/{domain}/{spec}.md`, preserving the structure of the
source repository. The order of domains and specs in navigation follows the "Specs"
table of the overview document.
"""
import json
import os
import re
import shutil

import odf

DST_DIR = "odf/spec"
OVERVIEW = "specs/overview.md"


def list_specs() -> list[tuple[str, list[str]]]:
    """Returns domains and paths of their specs (relative to ODF root) in order of the overview table"""
    text = odf.read(OVERVIEW)
    domains: dict[str, list[str]] = {}
    for m in re.finditer(r"^\| ([^|]+?) \| \[[^\]]+\]\(([^)]+\.md)\) \|", text, flags=re.MULTILINE):
        domain, path = m.groups()
        domains.setdefault(domain, []).append(os.path.normpath(os.path.join("specs", path)))
    if not domains:
        raise Exception(f"Unable to find the list of specs in {OVERVIEW}")
    return list(domains.items())


def render(src_path: str, title: str = None):
    text = odf.read(src_path)
    doc_title, text = odf.split_title(text)
    text = odf.remove_section(text, "Table of Contents")
    text = odf.convert(src_path, text)

    page = src_path.removeprefix("specs/").removesuffix(".md")
    dst_path = os.path.join(DST_DIR, page + ".md")
    os.makedirs(os.path.dirname(dst_path), exist_ok=True)
    with open(dst_path, "w") as f:
        f.write(odf.page_header(title or doc_title))
        f.write(text.strip() + "\n")

    return odf.SPECS_URL_PREFIX + page


def update_navigation(overview_page: str, domains: list[tuple[str, list[str]]]):
    with open("docs.json") as f:
        cfg = json.load(f)

    group = cfg["navigation"]["tabs"][1]["groups"][0]
    assert group["group"] == "Open Data Fabric"

    spec_group = {
        "group": "Specification",
        "root": overview_page,
        "pages": [
            {"group": domain, "pages": pages}
            for domain, pages in domains
        ],
    }

    pages = group["pages"]
    for i, p in enumerate(pages):
        if p == "/odf/spec" or (isinstance(p, dict) and p.get("group") == "Specification"):
            pages[i] = spec_group
            break
    else:
        raise Exception("Unable to find the specification page in docs.json")

    with open("docs.json", "w") as f:
        json.dump(cfg, f, indent=2)
        f.write("\n")


if __name__ == "__main__":
    if os.path.exists(DST_DIR):
        shutil.rmtree(DST_DIR)

    overview_page = render(OVERVIEW, title="Overview")

    domains = [
        (domain, [render(path) for path in paths])
        for domain, paths in list_specs()
    ]

    update_navigation(overview_page, domains)
