# coding: utf-8
"""
Tests for scripts/changelog_check.py, which keeps CHANGELOG.md consistent with VERSION.
"""

import contextlib
import importlib.util
import io
import os
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


if __name__ == "__main__":
    unittest.main()
