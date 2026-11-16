#!/usr/bin/env python3
# coding: utf-8
"""
Check that CHANGELOG.md is consistent with VERSION (used in CI).

A pull request that bumps VERSION must move the [Unreleased] entries of CHANGELOG.md to a section for the
new version (see "Releasing" in CONTRIBUTING.md). This script fails unless:

- the first section is "## [Unreleased]";
- the next section is "## [<VERSION>] - <YYYY-MM-DD>" and lists at least one change;
- versions are listed newest first, and their dates do not go backwards;
- every section has a link definition at the bottom, and [Unreleased] compares v<VERSION> with HEAD;
- every pull request merged into master for this release is accounted for: its link appears in the
  [<VERSION>] section or in the "## Internal" section. The pull requests are read from the git history
  (merge commits "Merge pull request #N" and squash commits "... (#N)") between the tag of the previous
  version and the tag of VERSION, or HEAD when that tag does not exist yet (a pending release). Pull
  requests that only change VERSION and CHANGELOG.md (release pull requests) are exempt. This part needs
  the git history and tags (in CI: actions/checkout with fetch-depth: 0); without them it is skipped
  with a warning.

Usage:
    python scripts/changelog_check.py          # the check (used in CI)
    python scripts/changelog_check.py pulls    # list the pull requests merged since the latest release tag

Only the standard library is used.
"""

import datetime
import os
import re
import subprocess
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

_HEADING = re.compile(r"^## \[(?P<name>[^\]]+)\](?: - (?P<date>.+?))?\s*$")
_LINK = re.compile(r"^\[(?P<name>[^\]]+)\]: (?P<url>\S+)\s*$")
_VERSION = re.compile(r"^\d+\.\d+\.\d+$")
_MERGE_SUBJECT = re.compile(r"^Merge pull request #(\d+)\b")
_SQUASH_SUBJECT = re.compile(r"\(#(\d+)\)\s*$")
_PR_LINK = re.compile(r"/pull/(\d+)\b")
_INTERNAL = re.compile(r"^## Internal[ \t]*$(?P<body>.*?)(?=^## |^\[[^\]]+\]: |\Z)", re.M | re.S)
# Files a release pull request changes; a pull request that changes nothing else needs no changelog entry.
RELEASE_ONLY_FILES = frozenset(["VERSION", "CHANGELOG.md"])


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


def _git(*args):
    return subprocess.run(["git"] + list(args), cwd=ROOT, capture_output=True, text=True, check=True).stdout


def merged_pull_requests(since, until="HEAD", git=_git):
    """
    Return {pull request number: set of changed files} for the pull requests merged into the first-parent
    history between the revisions since (exclusive) and until.
    """
    pulls = {}
    log = git("log", "--first-parent", "--format=%H%x00%P%x00%s", "{}..{}".format(since, until))
    for line in log.splitlines():
        sha, parents, subject = line.split("\x00", 2)
        match = _MERGE_SUBJECT.match(subject) or _SQUASH_SUBJECT.search(subject)
        if not match:
            continue
        first_parent = parents.split()[0] if parents.split() else None
        files = git("diff", "--name-only", first_parent, sha).split() if first_parent else []
        pulls[int(match.group(1))] = set(files)
    return pulls


def release_range(text, version, git=_git):
    """
    Return (since, until) revisions of the pull requests that belong to the [version] section, or None with a
    reason when they cannot be determined.
    """
    sections, _ = parse(text)
    versions = [name for name, _, _ in sections[1:]]
    if len(versions) < 2 or versions[0] != version:
        return None, "no previous version in CHANGELOG.md"

    def tag_exists(tag):
        try:
            git("rev-parse", "--verify", "--quiet", "refs/tags/" + tag)
            return True
        except subprocess.CalledProcessError:
            return False

    since = "v" + versions[1]
    if not tag_exists(since):
        return None, "tag {} not found (fetch the git history with tags, e.g. fetch-depth: 0)".format(since)
    until = "v" + version if tag_exists("v" + version) else "HEAD"
    return (since, until), None


def coverage_problems(text, version, pulls):
    """
    Return a problem for each pull request that is neither linked in the [version] section or the Internal
    section nor a release-only pull request.
    """
    sections, _ = parse(text)
    body = "\n".join(next((lines for name, _, lines in sections if name == version), []))
    internal = _INTERNAL.search(text)
    mentioned = {int(n) for n in _PR_LINK.findall(body + (internal.group("body") if internal else ""))}
    problems = []
    for number, files in sorted(pulls.items()):
        if number in mentioned or (files and files <= RELEASE_ONLY_FILES):
            continue
        problems.append("pull request #{} was merged for {} but is not in the [{}] section or the Internal section. "
                        "Describe it (see .claude/skills/release/SKILL.md) or, if package users do not notice it, "
                        "list it under Internal.".format(number, version, version))
    return problems


def list_pulls(git=_git):
    """
    Print the pull requests merged since the latest release tag reachable from HEAD, for writing the changelog.
    """
    since = git("describe", "--tags", "--abbrev=0", "--match", "v[0-9]*", "HEAD").strip()
    pulls = merged_pull_requests(since, "HEAD", git=git)
    print("Pull requests merged since {} (newest first):".format(since))
    for number, files in sorted(pulls.items(), reverse=True):
        note = "  (release only: no entry needed)" if files and files <= RELEASE_ONLY_FILES else ""
        print("#{}{}  {}".format(number, note, " ".join(sorted(files))))
    if not pulls:
        print("(none)")
    return 0


def main(argv):
    if argv[1:2] == ["pulls"]:
        return list_pulls()
    with open(os.path.join(ROOT, "VERSION"), encoding="utf-8") as f:
        version = f.read().strip()
    with open(os.path.join(ROOT, "CHANGELOG.md"), encoding="utf-8") as f:
        text = f.read()
    problems = check(text, version)
    if not problems:
        try:
            revisions, reason = release_range(text, version)
            if revisions:
                problems += coverage_problems(text, version, merged_pull_requests(*revisions))
                print("Checked the pull requests merged in {}..{}".format(*revisions))
            else:
                print("::warning file=CHANGELOG.md::Skipped the pull request check: {}".format(reason))
        except (OSError, subprocess.CalledProcessError) as e:
            print("::warning file=CHANGELOG.md::Skipped the pull request check: git failed ({})".format(type(e).__name__))
    if not problems:
        print("CHANGELOG.md is consistent with VERSION {}".format(version))
        return 0
    for problem in problems:
        print("::error file=CHANGELOG.md::{}".format(problem))
    return 1


if __name__ == "__main__":
    sys.exit(main(sys.argv))
