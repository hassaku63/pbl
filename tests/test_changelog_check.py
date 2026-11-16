# coding: utf-8
"""
Tests for scripts/changelog_check.py, which keeps CHANGELOG.md consistent with VERSION.
"""

import contextlib
import importlib.util
import io
import os
import subprocess
import textwrap
import unittest

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
_spec = importlib.util.spec_from_file_location("changelog_check", os.path.join(ROOT, "scripts", "changelog_check.py"))
changelog_check = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(changelog_check)

VALID = textwrap.dedent("""\
    # Changelog

    ## [Unreleased]

    ## [0.2.0] - 2026-11-16

    ### Added

    - Something new ([#2](https://example.com/2)).

    ## [0.1.0] - 2026-11-15

    ### Fixed

    - A bug.

    [Unreleased]: https://github.com/hassaku63/pbl/compare/v0.2.0...HEAD
    [0.2.0]: https://github.com/hassaku63/pbl/compare/v0.1.0...v0.2.0
    [0.1.0]: https://github.com/hassaku63/pbl/compare/v0.0.9...v0.1.0
""")


class TestChangelogCheck(unittest.TestCase):
    def test_valid(self):
        self.assertEqual([], changelog_check.check(VALID, "0.2.0"))

    def test_version_bumped_without_changelog_section(self):
        problems = changelog_check.check(VALID, "0.3.0")
        self.assertEqual(1, len(problems))
        self.assertIn("VERSION is 0.3.0 but the latest section of CHANGELOG.md is [0.2.0]", problems[0])

    def test_entries_left_in_unreleased(self):
        text = VALID.replace("## [0.2.0] - 2026-11-16\n\n### Added\n\n- Something new ([#2](https://example.com/2)).\n", "## [0.2.0] - 2026-11-16\n")
        self.assertIn("section [0.2.0] lists no changes", changelog_check.check(text, "0.2.0"))

    def test_unreleased_must_come_first(self):
        text = VALID.replace("## [Unreleased]\n\n", "")
        self.assertEqual(["the first section must be '## [Unreleased]'"], changelog_check.check(text, "0.2.0"))

    def test_missing_or_invalid_date(self):
        for heading in ("## [0.2.0]", "## [0.2.0] - 16 Nov 2026"):
            with self.subTest(heading=heading):
                text = VALID.replace("## [0.2.0] - 2026-11-16", heading)
                self.assertIn("section [0.2.0] needs a date: '## [0.2.0] - YYYY-MM-DD'", changelog_check.check(text, "0.2.0"))

    def test_order_and_dates(self):
        text = VALID.replace("## [0.1.0] - 2026-11-15", "## [0.1.0] - 2026-11-17")
        self.assertIn("the date of [0.2.0] is before the date of [0.1.0]", changelog_check.check(text, "0.2.0"))
        text = VALID.replace("## [0.1.0] - 2026-11-15", "## [0.3.0] - 2026-11-15").replace("[0.1.0]:", "[0.3.0]:")
        self.assertIn("versions must be listed newest first: [0.2.0] comes before [0.3.0]", changelog_check.check(text, "0.2.0"))

    def test_links(self):
        text = VALID.replace("[0.1.0]: https://github.com/hassaku63/pbl/compare/v0.0.9...v0.1.0\n", "")
        self.assertIn("missing link definition '[0.1.0]: ...' at the bottom", changelog_check.check(text, "0.2.0"))
        text = VALID.replace("compare/v0.2.0...HEAD", "compare/v0.1.0...HEAD")
        self.assertIn("the [Unreleased] link must compare v0.2.0...HEAD", changelog_check.check(text, "0.2.0"))

    def test_repository_changelog_is_consistent_with_version(self):
        with contextlib.redirect_stdout(io.StringIO()) as out:
            self.assertEqual(0, changelog_check.main(["changelog_check.py"]))
        self.assertIn("is consistent with VERSION", out.getvalue())


COVERED = textwrap.dedent("""\
    # Changelog

    ## [Unreleased]

    ## [0.2.0] - 2026-11-16

    ### Added

    - Something new ([#12](https://github.com/hassaku63/pbl/pull/12)).

    ## [0.1.0] - 2026-11-15

    ### Fixed

    - A bug ([#5](https://github.com/hassaku63/pbl/pull/5)).

    ## Internal

    CI changes ([#11](https://github.com/hassaku63/pbl/pull/11)).

    [Unreleased]: https://github.com/hassaku63/pbl/compare/v0.2.0...HEAD
    [0.2.0]: https://github.com/hassaku63/pbl/compare/v0.1.0...v0.2.0
    [0.1.0]: https://github.com/hassaku63/pbl/compare/v0.0.9...v0.1.0
""")


class FakeGit(object):
    """
    Answers the git commands used by changelog_check from a fixed history.
    """

    def __init__(self, tags, log, diffs):
        self.tags, self.log, self.diffs, self.calls = tags, log, diffs, []

    def __call__(self, *args):
        self.calls.append(args)
        if args[:3] == ("rev-parse", "--verify", "--quiet"):
            if args[3].replace("refs/tags/", "") not in self.tags:
                raise subprocess.CalledProcessError(1, "git")
            return "sha\n"
        if args[0] == "log":
            return "".join("{}\x00{}\x00{}\n".format(sha, parents, subject) for sha, parents, subject in self.log)
        if args[0] == "diff":
            return "\n".join(self.diffs[args[3]])
        raise AssertionError(args)


HISTORY = [
    ("c4", "c3 x4", "Merge pull request #13 from fork/release"),
    ("c3", "c2", "Fix the docs of Issue.get (#12)"),
    ("c2", "c1 x2", "Merge pull request #11 from fork/ci"),
    ("c1", "c0", "Merge branch 'master' into topic"),
]
DIFFS = {"c4": ["VERSION", "CHANGELOG.md"], "c3": ["backlog/issue.py"], "c2": [".github/workflows/jobs.yml"],
         "c1": ["backlog/x.py"]}


class TestPullRequestCoverage(unittest.TestCase):
    def test_merged_pull_requests(self):
        git = FakeGit({"v0.1.0"}, HISTORY, DIFFS)

        pulls = changelog_check.merged_pull_requests("v0.1.0", "HEAD", git=git)

        self.assertEqual({13: {"VERSION", "CHANGELOG.md"}, 12: {"backlog/issue.py"}, 11: {".github/workflows/jobs.yml"}}, pulls)
        self.assertEqual(("log", "--first-parent", "--format=%H%x00%P%x00%s", "v0.1.0..HEAD"), git.calls[0])

    def test_release_range(self):
        pending = FakeGit({"v0.1.0"}, [], {})
        self.assertEqual((("v0.1.0", "HEAD"), None), changelog_check.release_range(COVERED, "0.2.0", git=pending))
        released = FakeGit({"v0.1.0", "v0.2.0"}, [], {})
        self.assertEqual((("v0.1.0", "v0.2.0"), None), changelog_check.release_range(COVERED, "0.2.0", git=released))
        untagged = FakeGit(set(), [], {})
        revisions, reason = changelog_check.release_range(COVERED, "0.2.0", git=untagged)
        self.assertIsNone(revisions)
        self.assertIn("tag v0.1.0 not found", reason)

    def test_every_pull_request_is_in_the_section_or_internal(self):
        pulls = {13: {"VERSION", "CHANGELOG.md"}, 12: {"backlog/issue.py"}, 11: {".github/workflows/jobs.yml"}}
        self.assertEqual([], changelog_check.coverage_problems(COVERED, "0.2.0", pulls))

    def test_missing_pull_request(self):
        pulls = {14: {"backlog/issue.py"}, 5: {"backlog/x.py"}}
        problems = changelog_check.coverage_problems(COVERED, "0.2.0", pulls)
        # #5 is linked only in the older [0.1.0] section, which does not count for 0.2.0.
        self.assertEqual(2, len(problems))
        self.assertIn("pull request #5 was merged for 0.2.0 but is not in the [0.2.0] section", problems[0])
        self.assertIn("pull request #14", problems[1])

    def test_list_pulls(self):
        git = FakeGit({"v0.1.0"}, HISTORY, DIFFS)
        real = git.__call__

        def fake(*args):
            if args[0] == "describe":
                return "v0.1.0\n"
            return real(*args)

        with contextlib.redirect_stdout(io.StringIO()) as out:
            self.assertEqual(0, changelog_check.list_pulls(git=fake))
        lines = out.getvalue().splitlines()
        self.assertEqual("Pull requests merged since v0.1.0 (newest first):", lines[0])
        self.assertEqual("#13  (release only: no entry needed)  CHANGELOG.md VERSION", lines[1])
        self.assertEqual("#12  backlog/issue.py", lines[2])

    def test_release_only_pull_requests_are_exempt(self):
        for files in ({"VERSION"}, {"CHANGELOG.md"}, {"VERSION", "CHANGELOG.md"}):
            with self.subTest(files=files):
                self.assertEqual([], changelog_check.coverage_problems(COVERED, "0.2.0", {20: set(files)}))
        self.assertEqual(1, len(changelog_check.coverage_problems(COVERED, "0.2.0", {20: {"VERSION", "README.md"}})))


if __name__ == "__main__":
    unittest.main()
