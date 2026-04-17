#!/usr/bin/env python3
"""Validate zugot recipe files.

Checks:
  1. TOML/CYML parse cleanly (using stdlib `tomllib`)
  2. `[package].name` matches the filename basename
  3. `sha256` is populated (empty values must have a `# TODO` comment nearby)
  4. Every `[depends].runtime` and `[depends].build` entry resolves to a
     package that exists in zugot itself OR in an optional bazaar tree
     passed via --check-against

Exit code: 0 on success, 1 on any failure.

Usage:
  scripts/validate_recipes.py                               # zugot-only check
  scripts/validate_recipes.py --check-against ../bazaar     # cross-check bazaar
"""

from __future__ import annotations

import argparse
import pathlib
import re
import sys
import tomllib


def extract_name(path: pathlib.Path) -> str | None:
    """Best-effort extraction of `[package].name` even if TOML parse fails."""
    try:
        with path.open("rb") as fh:
            return tomllib.load(fh).get("package", {}).get("name")
    except tomllib.TOMLDecodeError:
        text = path.read_text()
        m = re.search(r'^name\s*=\s*"([^"]+)"', text, re.M)
        return m.group(1) if m else None


def collect_names(root: pathlib.Path) -> set[str]:
    return {n for n in (extract_name(p) for p in root.rglob("*.cyml")) if n}


def check_recipe(path: pathlib.Path, provided: set[str]) -> list[str]:
    errors: list[str] = []
    rel = path

    # 1. Parse check
    try:
        with path.open("rb") as fh:
            data = tomllib.load(fh)
    except tomllib.TOMLDecodeError as e:
        errors.append(f"{rel}: TOML parse error: {e}")
        return errors  # can't check anything else

    pkg = data.get("package", {})
    name = pkg.get("name")
    source = data.get("source", {})

    # 2. Filename ↔ package.name
    stem = path.stem
    if name and name != stem:
        errors.append(f"{rel}: filename stem '{stem}' != [package].name '{name}'")

    # 3. SHA256 populated (unless there's a TODO comment in the file)
    sha = source.get("sha256")
    local = source.get("local", False)
    github_release = source.get("github_release")
    if sha is not None and not sha and not local:
        text = path.read_text()
        # Look for a TODO marker anywhere in the source block region
        if "# TODO" not in text and "# todo" not in text.lower():
            errors.append(f"{rel}: empty sha256 without a `# TODO` comment")

    # 4. Deps resolve
    depends = data.get("depends", {})
    for section in ("runtime", "build"):
        for dep in depends.get(section, []) or []:
            if dep == name:
                continue
            if dep not in provided:
                errors.append(f"{rel}: unresolved {section} dep '{dep}'")

    return errors


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--zugot", default=pathlib.Path(__file__).resolve().parent.parent,
        type=pathlib.Path, help="zugot recipe root (default: parent of scripts/)",
    )
    parser.add_argument(
        "--check-against", type=pathlib.Path,
        help="additional recipe root whose [package].name values also count as 'provided'",
    )
    args = parser.parse_args()

    zugot_root: pathlib.Path = args.zugot
    provided = collect_names(zugot_root)
    cross_root: pathlib.Path | None = args.check_against
    if cross_root is not None:
        provided |= collect_names(cross_root)

    # Which tree to validate? If --check-against is set, we validate the cross-ref
    # tree (bazaar against zugot). Otherwise we validate zugot itself.
    target = cross_root if cross_root is not None else zugot_root

    total_errors: list[str] = []
    for path in sorted(target.rglob("*.cyml")):
        # skip the index files inside .git, node_modules, etc.
        if any(part.startswith(".") for part in path.parts):
            continue
        total_errors.extend(check_recipe(path, provided))

    if total_errors:
        for err in total_errors:
            print(err)
        print(f"\n{len(total_errors)} problem(s) found", file=sys.stderr)
        return 1
    print(f"OK: all recipes in {target} validate clean", file=sys.stderr)
    return 0


if __name__ == "__main__":
    sys.exit(main())
