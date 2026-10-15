#!/usr/bin/env python
"""
Generates RFC pages from `rfcs/` directory of the ODF repository.
"""
import json
import os
import re

import odf

DST_DIR = "odf/rfcs"

INDEX_TITLE = "RFCs"
INDEX_INTRO = "Protocol design evolution proposals:\n"


def get_summary(text: str) -> str:
    m = re.search(r"^#+ Summary.*\n", text, flags=re.MULTILINE)
    if not m:
        raise Exception("Unable to find the summary section")
    end = re.search(r"^#", text[m.end():], flags=re.MULTILINE)
    end = m.end() + end.start() if end else len(text)
    return text[m.end():end].strip()


if __name__ == "__main__":
    src_dir = os.path.join(odf.ODF_PATH, "rfcs")
    os.makedirs(DST_DIR, exist_ok=True)

    file_names = sorted(
        fname
        for fname in os.listdir(src_dir)
        if re.fullmatch(r"\d{3}-.+\.md", fname) and fname != "000-template.md"
    )

    rfcs = []

    for fname in file_names:
        src_path = f"rfcs/{fname}"

        title, text = odf.split_title(odf.read(src_path).strip())
        text = odf.convert(src_path, text)

        with open(os.path.join(DST_DIR, fname), "w") as f:
            f.write(odf.page_header(title))
            f.write(text + "\n")

        rfcs.append((fname.removesuffix(".md"), title, get_summary(text)))

    # Write index
    with open(os.path.join(DST_DIR, "index.md"), "w") as f:
        f.write(odf.page_header(INDEX_TITLE))
        f.write(INDEX_INTRO)
        for name, title, _ in rfcs:
            f.write(f"- [{title}]({odf.RFCS_URL_PREFIX}{name})\n")

    # Update docs.json
    with open("docs.json") as f:
        cfg = json.load(f)

    group = cfg["navigation"]["tabs"][1]["groups"][0]
    assert group["group"] == "Open Data Fabric"
    rfcs_group = next(p for p in group["pages"] if isinstance(p, dict) and p.get("group") == "RFCs")
    rfcs_group["pages"] = [f"{odf.RFCS_URL_PREFIX}{name}" for name, _, _ in rfcs]

    with open("docs.json", "w") as f:
        json.dump(cfg, f, indent=2)
        f.write("\n")
