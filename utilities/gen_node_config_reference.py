#!/usr/bin/env python
import os

# Locate `kamu-node` repo
KAMU_NODE_PATH = os.path.normpath(
    os.path.join(
        os.path.dirname(__file__),
        "../../kamu-node"
    )
)
if not os.path.exists(KAMU_NODE_PATH):
    raise Exception(
        f"Expecting to have `kamu-node` repository checked "
        f"out side by side, but couldn't find path: {KAMU_NODE_PATH}")

PAGE_HEADER = """---
# !!! THIS FILE IS AUTO-GENERATED - DO NOT MODIFY MANUALLY !!!
Title: Config Reference
description:
weight: 110
categories: []
---
"""

if __name__ == "__main__":
    # Read the source
    with open(os.path.join(KAMU_NODE_PATH, "resources/api-server/config.md")) as f:
        text = f.read()

    print(PAGE_HEADER)
    print(text)
