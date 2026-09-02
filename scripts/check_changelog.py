#!/usr/bin/env python3
"""Validate changelog structure and extract a version's release notes."""

from __future__ import annotations

import argparse
import re
import subprocess
import sys
from pathlib import Path

CHANGELOG = Path("CHANGELOG.md")
UNRELEASED_HEADER = "## [Unreleased]"
VERSION_RE = re.compile(r"^## \[(?P<version>\d+\.\d+\.\d+)\] - \d{4}-\d{2}-\d{2}$")
RELEASE_RELEVANT_PATHS = ("linux-vconsole.toml", "README.md", "images/")


def fail(message: str) -> None:
    print(f"changelog check failed: {message}", file=sys.stderr)
    raise SystemExit(1)


def read_changelog() -> list[str]:
    if not CHANGELOG.is_file():
        fail("CHANGELOG.md is required")

    lines = CHANGELOG.read_text(encoding="utf-8").splitlines()
    if UNRELEASED_HEADER not in lines:
        fail("CHANGELOG.md must contain '## [Unreleased]'")

    headers = [line for line in lines if line.startswith("## [")]
    if not headers or headers[0] != UNRELEASED_HEADER:
        fail("'## [Unreleased]' must be the first version heading")

    versions: set[str] = set()
    for header in headers[1:]:
        match = VERSION_RE.fullmatch(header)
        if match is None:
            fail(f"invalid version heading: {header!r}")
        version = match.group("version")
        if version in versions:
            fail(f"duplicate version heading: {version}")
        versions.add(version)

    return lines


def changed_paths(base: str) -> set[str]:
    if not base or set(base) == {"0"}:
        return set()

    result = subprocess.run(
        ["git", "diff", "--name-only", base, "HEAD"],
        check=False,
        capture_output=True,
        text=True,
    )
    if result.returncode != 0:
        fail(f"could not compare against {base}: {result.stderr.strip()}")
    return set(filter(None, result.stdout.splitlines()))


def check_changelog_updated(base: str) -> None:
    paths = changed_paths(base)
    affects_release = any(
        path == relevant or path.startswith(relevant)
        for path in paths
        for relevant in RELEASE_RELEVANT_PATHS
    )
    if affects_release and "CHANGELOG.md" not in paths:
        fail("release-relevant changes must update CHANGELOG.md")


def notes_for_version(lines: list[str], tag: str) -> str:
    version = tag.removeprefix("v")
    if not re.fullmatch(r"\d+\.\d+\.\d+", version):
        fail(f"release tag must use vX.Y.Z, got {tag!r}")

    target = f"## [{version}]"
    start = next((index for index, line in enumerate(lines) if line.startswith(target)), None)
    if start is None:
        fail(f"no changelog section exists for {version}")

    end = next(
        (index for index in range(start + 1, len(lines)) if lines[index].startswith("## [")),
        len(lines),
    )
    notes = "\n".join(lines[start + 1 : end]).strip()
    if not notes:
        fail(f"changelog section {version} has no release notes")
    return notes + "\n"


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--base", help="commit to compare with HEAD")
    parser.add_argument("--release-version", help="vX.Y.Z tag to extract")
    parser.add_argument("--output", type=Path, help="file for extracted release notes")
    args = parser.parse_args()

    lines = read_changelog()
    if args.base:
        check_changelog_updated(args.base)

    if args.release_version:
        if args.output is None:
            fail("--output is required with --release-version")
        args.output.write_text(notes_for_version(lines, args.release_version), encoding="utf-8")
    elif args.output is not None:
        fail("--output requires --release-version")


if __name__ == "__main__":
    main()
