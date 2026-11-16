#!/usr/bin/env python3
# coding: utf-8
"""
Check that CHANGELOG.md is consistent with VERSION (used in CI).

A pull request that bumps VERSION must move the [Unreleased] entries of CHANGELOG.md to a section for the
new version (see "Releasing" in CONTRIBUTING.md). This script fails unless:

- the first section is "## [Unreleased]";
- the next section is "## [<VERSION>] - <YYYY-MM-DD>" and lists at least one change;
- versions are listed newest first, and their dates do not go backwards;
- every section has a link definition at the bottom, and [Unreleased] compares v<VERSION> with HEAD.

Usage:
    python scripts/changelog_check.py

Only the standard library is used.
"""

import datetime
import os
import re
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

_HEADING = re.compile(r"^## \[(?P<name>[^\]]+)\](?: - (?P<date>.+?))?\s*$")
_LINK = re.compile(r"^\[(?P<name>[^\]]+)\]: (?P<url>\S+)\s*$")
_VERSION = re.compile(r"^\d+\.\d+\.\d+$")


def _version_key(version):
    return tuple(int(part) for part in version.split("."))


def parse(text):
    """
    Return (sections, links): sections is a list of (name, date or None, body lines), links maps names to URLs.
    """
    sections, links = [], {}
    for line in text.splitlines():
        heading = _HEADING.match(line)
        link = _LINK.match(line)
        if heading:
            sections.append((heading.group("name"), heading.group("date"), []))
        elif link:
            links[link.group("name")] = link.group("url")
        elif sections:
            sections[-1][2].append(line)
    return sections, links


def _check_heading_dates(versions):
    problems = []
    for name, date, _ in versions:
        if not _VERSION.match(name):
            problems.append("section [{}] is not an X.Y.Z version".format(name))
            continue
        try:
            datetime.date.fromisoformat(date or "")
        except ValueError:
            problems.append("section [{}] needs a date: '## [{}] - YYYY-MM-DD'".format(name, name))
    return problems


def _check_order(versions):
    problems = []
    valid = [(name, date) for name, date, _ in versions if _VERSION.match(name)]
    for (newer, newer_date), (older, older_date) in zip(valid, valid[1:], strict=False):
        if _version_key(newer) <= _version_key(older):
            problems.append("versions must be listed newest first: [{}] comes before [{}]".format(newer, older))
        if newer_date and older_date and newer_date < older_date:
            problems.append("the date of [{}] is before the date of [{}]".format(newer, older))
    return problems


def check(text, version):
    """
    Return a list of problems; empty when CHANGELOG.md is consistent with the version in VERSION.
    """
    sections, links = parse(text)
    if not sections or sections[0][0] != "Unreleased":
        return ["the first section must be '## [Unreleased]'"]
    versions = sections[1:]
    if not versions or versions[0][0] != version:
        found = versions[0][0] if versions else "none"
        return ["VERSION is {} but the latest section of CHANGELOG.md is [{}]. In the pull request that bumps VERSION, "
                "move the [Unreleased] entries to '## [{}] - YYYY-MM-DD'.".format(version, found, version)]

    problems = []
    if not any(line.strip().startswith("- ") for line in versions[0][2]):
        problems.append("section [{}] lists no changes".format(version))
    problems += _check_heading_dates(versions)
    problems += _check_order(versions)
    for name in ["Unreleased"] + [name for name, _, _ in versions]:
        if name not in links:
            problems.append("missing link definition '[{}]: ...' at the bottom".format(name))
    unreleased = links.get("Unreleased", "")
    if unreleased and not unreleased.endswith("/compare/v{}...HEAD".format(version)):
        problems.append("the [Unreleased] link must compare v{}...HEAD".format(version))
    return problems


def main(argv):
    with open(os.path.join(ROOT, "VERSION"), encoding="utf-8") as f:
        version = f.read().strip()
    with open(os.path.join(ROOT, "CHANGELOG.md"), encoding="utf-8") as f:
        text = f.read()
    problems = check(text, version)
    if not problems:
        print("CHANGELOG.md is consistent with VERSION {}".format(version))
        return 0
    for problem in problems:
        print("::error file=CHANGELOG.md::{}".format(problem))
    return 1


if __name__ == "__main__":
    sys.exit(main(sys.argv))
