"""
Utilities shared by scripts that include content from the `open-data-fabric` repository.

The ODF repository is expected to be checked out side by side with this one.
"""
import os
import re
import shutil

from typing import Optional

ODF_URL = "https://github.com/open-data-fabric/open-data-fabric"
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

# Where images referenced by ODF documents are copied to, preserving their paths
# relative to the ODF repository root (e.g. `images/odf/specs/...`, `images/odf/rfcs/...`).
# Previously copied images are removed by the `docgen` target before regenerating.
IMAGES_DIR = "images/odf"

SPECS_URL_PREFIX = "/odf/spec/"
RFCS_URL_PREFIX = "/odf/rfcs/"
GLOSSARY_URL = "/general/glossary"
SCHEMAS_URL = "/odf/schemas"

# Schema contexts and directories that are not rendered on the schemas page
SCHEMAS_SKIP_CONTEXTS = {"legacy", "meta"}
SCHEMAS_SKIP_DIRS = {"meta"}

COMPONENTS_IMPORT = "import {Diagram, Term, Schema, YouTube, YouTubeList} from '/components/common.jsx'"

LINK_RE = re.compile(r"(!?)\[([^\]]*)\]\(([^)\s]+)\)")


def read(rel_path: str) -> str:
    with open(os.path.join(ODF_PATH, rel_path)) as f:
        return f.read()


def page_header(title: str, description: Optional[str] = None, extra: str = "") -> str:
    lines = [
        "---",
        "# !!! THIS FILE IS AUTO-GENERATED - DO NOT MODIFY MANUALLY !!!",
        f"title: \"{title}\"",
    ]
    if description:
        lines.append(f"description: \"{description}\"")
    if extra:
        lines.append(extra)
    lines += ["---", "", COMPONENTS_IMPORT, "", ""]
    return "\n".join(lines)


def split_title(text: str) -> tuple[str, str]:
    """Extracts the `# Title` line, returning the title and the remaining text"""
    m = re.match(r"# (.*)\n", text)
    if not m:
        raise Exception("Document has no title")
    title = m.group(1).replace("<!-- omit in toc -->", "").strip()
    return title, text[m.end():].strip()


def remove_section(text: str, heading: str) -> str:
    """Removes a `## Heading` section up to the next heading of the same or higher level"""
    m = re.search(rf"^(#+) {re.escape(heading)}.*\n", text, flags=re.MULTILINE)
    if not m:
        return text
    level = len(m.group(1))
    end = re.search(rf"^#{{1,{level}}} ", text[m.end():], flags=re.MULTILINE)
    end = m.end() + end.start() if end else len(text)
    return text[:m.start()] + text[end:]


def convert_comments(text: str) -> str:
    """Strips TOC markers and converts HTML comments into MDX comments"""
    text = re.sub(r"\s*<!-- omit in toc -->", "", text)
    return re.sub(r"<!--(.*?)-->", r"{/*\1*/}", text, flags=re.DOTALL)


def schema_anchor(name: str) -> str:
    """Anchor of a schema on the schemas page"""
    return name.lower()


def _github_url(target: str, fragment: str) -> str:
    kind = "tree" if os.path.isdir(os.path.join(ODF_PATH, target)) else "blob"
    return f"{ODF_URL}/{kind}/master/{target}{fragment}"


def _schema_name(target: str) -> Optional[str]:
    """Returns the name of a schema if it's rendered on the schemas page"""
    parts = target.split("/")
    if len(parts) < 4 or parts[0] != "schemas" or not target.endswith(".json"):
        return None
    if parts[1] in SCHEMAS_SKIP_CONTEXTS or any(p in SCHEMAS_SKIP_DIRS for p in parts[3:-1]):
        return None
    return os.path.splitext(parts[-1])[0]


def resolve(src_path: str, url: str) -> tuple[str, str]:
    """Resolves a link in the ODF document at `src_path` into a path relative to the ODF root and a fragment"""
    path, _, fragment = url.partition("#")
    fragment = f"#{fragment}" if fragment else ""
    if path.startswith("/"):
        target = path.lstrip("/")
    else:
        target = os.path.normpath(os.path.join(os.path.dirname(src_path), path))
    return target, fragment


def map_link(src_path: str, text: str, url: str) -> str:
    """Maps a link in an ODF document to the corresponding page of this site"""
    if url.startswith(("http://", "https://", "mailto:", "#")):
        return f"[{text}]({url})"

    target, fragment = resolve(src_path, url)

    if target == "specs/glossary.md":
        if fragment:
            return f'<Term t="{text}" id="{fragment[1:]}"/>'
        return f"[{text}]({GLOSSARY_URL})"

    if target == "specs/reference.md":
        if fragment.endswith("-schema"):
            name = fragment[1:].removesuffix("-schema")
            return f'<Schema t="{text.strip("`")}" id="{name}"/>'
        return f"[{text}]({SCHEMAS_URL})"

    if target.startswith("specs/") and target.endswith(".md"):
        page = target.removeprefix("specs/").removesuffix(".md")
        return f"[{text}]({SPECS_URL_PREFIX}{page}{fragment})"

    m = re.fullmatch(r"rfcs/(\d{3}-[^/]+)\.md", target)
    if m:
        return f"[{text}]({RFCS_URL_PREFIX}{m.group(1)}{fragment})"

    name = _schema_name(target)
    if name is not None:
        return f'<Schema t="{text.strip("`")}" id="{schema_anchor(name)}"/>'

    return f"[{text}]({_github_url(target, fragment)})"


def copy_image(src_path: str, url: str) -> str:
    """Copies an image referenced by an ODF document and returns its URL on this site"""
    if url.startswith(("http://", "https://")):
        return url
    target, _ = resolve(src_path, url)
    dst = os.path.join(IMAGES_DIR, target)
    os.makedirs(os.path.dirname(dst), exist_ok=True)
    shutil.copyfile(os.path.join(ODF_PATH, target), dst)
    return f"/{dst}"


def convert(src_path: str, text: str) -> str:
    """Converts an ODF markdown document into MDX suitable for this site"""
    text = convert_comments(text)

    def sub(m: re.Match[str]) -> str:
        is_image, label, url = m.groups()
        if is_image:
            return f'<Diagram src="{copy_image(src_path, url)}" alt="{label}"/>'
        return map_link(src_path, label, url)

    # Don't touch links inside fenced code blocks
    parts = re.split(r"(^```.*?^```)", text, flags=re.MULTILINE | re.DOTALL)
    return "".join(
        part if part.startswith("```") else LINK_RE.sub(sub, part)
        for part in parts
    )
