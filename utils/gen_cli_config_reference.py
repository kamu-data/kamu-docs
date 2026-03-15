#!/usr/bin/env python
import os

# Locate `kamu-cli` repo
KAMU_CLI_PATH = os.path.normpath(
    os.path.join(
        os.path.dirname(__file__),
        "../../kamu-cli"
    )
)
if not os.path.exists(KAMU_CLI_PATH):
    raise Exception(
        f"Expecting to have `kamu-cli` repository checked "
        f"out side by side, but couldn't find path: {KAMU_CLI_PATH}")

PAGE_HEADER = """---
# !!! THIS FILE IS AUTO-GENERATED - DO NOT MODIFY MANUALLY !!!
title: Config Reference
---
"""


# Hacky way to convert to MDX style
def md_to_mdx(text):
    lines = []
    for line in text.split("\n"):
        line = line.replace("{", "\\{").replace("<!--", "{/*").replace("-->", "*/}")
        lines.append(line)
    
    return "\n".join(lines)


if __name__ == "__main__":
    # Read the source
    with open(os.path.join(KAMU_CLI_PATH, "resources/config-reference.md")) as f:
        text = f.read()

    # Convert comments
    text = md_to_mdx(text)

    print(PAGE_HEADER)
    print(text)
