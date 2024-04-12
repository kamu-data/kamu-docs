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
Title: CLI Reference
description:
weight: 100
categories: []
---
"""

if __name__ == "__main__":
    # Read the source
    with open(os.path.join(KAMU_CLI_PATH, "resources/cli-reference.md")) as f:
        text = f.read()

    print(PAGE_HEADER)
    print(text)
