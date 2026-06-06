#!/usr/bin/env python3
import os
import re

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(SCRIPT_DIR, "..", ".."))
OUTPUT_NAME = "SUMMARY.md"
OUTPUT = os.path.join(ROOT, OUTPUT_NAME)

IGNORE_DIRS = {
    ".git",
    ".agents",
    ".codex",
    "__pycache__",
    "_book",
    "node_modules",
    ".venv",
    "docs",
    "assets",
    "images",
}

TITLE_RE = re.compile(r"^\s*#\s+(.*)")


def natural_key(s):
    """
    Stable natural sort:
    01_xxx -> 1, xxx
    1-2    -> 1, 2
    10bit  -> 10, bit
    """
    key = []

    parts = re.split(r"[\-_\.]", s)
    for part in parts:
        subs = re.split(r"(\d+)", part)
        for item in subs:
            if item == "":
                continue
            if item.isdigit():
                key.append((0, int(item)))
            else:
                key.append((1, item.lower()))

    return key


def title_of(path):
    try:
        with open(path, "r", encoding="utf-8-sig") as f:
            for line in f:
                m = TITLE_RE.match(line)
                if m:
                    return m.group(1).strip()
    except OSError:
        pass

    return os.path.splitext(os.path.basename(path))[0]


def rel(path):
    return "./" + os.path.relpath(path, ROOT).replace("\\", "/")


def generate(dir_path, level, lines):
    entries = sorted(os.listdir(dir_path), key=natural_key)

    readme = None
    subdirs = []
    files = []

    for entry in entries:
        full = os.path.join(dir_path, entry)

        if os.path.isdir(full):
            if entry not in IGNORE_DIRS:
                subdirs.append(full)
            continue

        if entry.lower() == "readme.md":
            readme = full
        elif entry.endswith(".md") and entry != OUTPUT_NAME:
            files.append(full)

    # GitBook root: only the root README.md is listed as a root-level file.
    # Other markdown files in the repository root, such as AGENTS.md, are ignored.
    if os.path.abspath(dir_path) == ROOT:
        if readme:
            lines.append(f"- [{title_of(readme)}]({rel(readme)})")

        for sub in subdirs:
            generate(sub, 0, lines)
        return

    if readme:
        indent = "  " * level
        lines.append(f"{indent}- [{title_of(readme)}]({rel(readme)})")
        child_level = level + 1
    else:
        print(f"Warning: {dir_path} has no README.md")
        child_level = level

    for sub in subdirs:
        generate(sub, child_level, lines)

    for f in files:
        indent = "  " * child_level
        lines.append(f"{indent}- [{title_of(f)}]({rel(f)})")


def main():
    lines = ["# 目录\n"]
    generate(ROOT, 0, lines)

    with open(OUTPUT, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))

    print(f"{OUTPUT_NAME} generated.")


if __name__ == "__main__":
    main()
