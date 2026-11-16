# coding: utf-8
"""
Tests for scripts/api_coverage.py, the generator of docs/API_COVERAGE.md.
"""

import contextlib
import importlib.util
import io
import os
import tempfile
import textwrap
import unittest
from unittest import mock

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
_spec = importlib.util.spec_from_file_location("api_coverage", os.path.join(ROOT, "scripts", "api_coverage.py"))
api_coverage = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(api_coverage)

SAMPLE = textwrap.dedent('''
    class Sample(object):
        def literal(self):
            return self.api.invoke_method("GET", "space")

        def variables(self, key):
            _uri = "projects/{key}/statuses".format(key=key)
            _method = "GET"
            return self.api.invoke_method(_method, _uri)

        def fstring(self, key, id):
            return self.api.invoke_method("PATCH", f"projects/{key}/versions/{id}")

        def helper(self, key, id):
            return self.api.invoke_method("DELETE", self._uri(key, id) + "/notifications")

        @staticmethod
        def _uri(key, id):
            return "issues/{key}/comments/{id}".format(key=key, id=id)

        def unresolvable(self, uri):
            return self.api.invoke_method("GET", uri)
''')


class TestImplementedEndpoints(unittest.TestCase):
    def test_uri_forms(self):
        with tempfile.TemporaryDirectory() as d:
            with open(os.path.join(d, "sample.py"), "w") as f:
                f.write(SAMPLE)
            found = api_coverage.implemented_endpoints(d)

        self.assertEqual({
            ("GET", "space"): ["Sample.literal"],
            ("GET", "projects/*/statuses"): ["Sample.variables"],
            ("PATCH", "projects/*/versions/*"): ["Sample.fstring"],
            ("DELETE", "issues/*/comments/*/notifications"): ["Sample.helper"],
        }, found)

    def test_normalize(self):
        self.assertEqual("issues/*/comments", api_coverage.normalize("/api/v2/issues/:issueIdOrKey/comments"))
        self.assertEqual("issues/*/comments", api_coverage.normalize("issues/{issue_id_or_key}/comments"))


class TestCoverageDocument(unittest.TestCase):
    def test_committed_document_is_up_to_date(self):
        with contextlib.redirect_stdout(io.StringIO()):
            self.assertEqual(0, api_coverage.main(["api_coverage.py", "check"]))

    def test_check_fails_when_document_is_stale(self):
        with tempfile.NamedTemporaryFile("w", suffix=".md", delete=False) as f:
            f.write("# stale\n")
        try:
            with mock.patch.object(api_coverage, "COVERAGE_MD", f.name), contextlib.redirect_stdout(io.StringIO()) as out:
                self.assertEqual(1, api_coverage.main(["api_coverage.py", "check"]))
            self.assertIn("out of date", out.getvalue())
        finally:
            os.unlink(f.name)


DEPRECATION_SAMPLE = textwrap.dedent('''
    import warnings


    def _warn_removed(name):
        warnings.warn(name, DeprecationWarning)


    class Sample(object):
        def marked(self):
            """
            .. deprecated:: 1.0
            """
            return self.api.invoke_method("POST", "users")

        def warns(self):
            warnings.warn("old", DeprecationWarning, stacklevel=2)
            return self.api.invoke_method("GET", "groups")

        def helper(self, id):
            _warn_removed("helper")
            return self.api.invoke_method("DELETE", "users/{id}".format(id=id))

        def plain(self, key):
            return self.api.invoke_method("GET", "projects/{key}/groups".format(key=key))

        def other_warning(self):
            warnings.warn("not a deprecation", UserWarning)
            return self.api.invoke_method("GET", "statuses")
''')

REMOVED = [
    {"method": "POST", "path": "/api/v2/users", "title": "Add User", "note": "gone", "confirmed_on": "2026-11-16"},
    {"method": "GET", "path": "/api/v2/groups", "title": "Get List of Groups", "removed_in": "2.113.3",
     "removed_on": "2025-09-11", "replacement": "GET /api/v2/teams", "announcement": "https://example.com/notice",
     "changelog": "https://example.com/changelog", "confirmed_on": "2026-11-16"},
    {"method": "DELETE", "path": "/api/v2/users/:userId", "title": "Delete User", "note": "gone", "confirmed_on": "2026-11-16"},
    {"method": "GET", "path": "/api/v2/projects/:projectIdOrKey/groups", "title": "Get Project Group List",
     "removed_in": "2.113.3", "confirmed_on": "2026-11-16"},
    {"method": "GET", "path": "/api/v2/statuses", "title": "Get Status List", "removed_in": "2.113.3", "confirmed_on": "2026-11-16"},
]


class TestRemovedEndpoints(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        with tempfile.TemporaryDirectory() as d:
            with open(os.path.join(d, "sample.py"), "w") as f:
                f.write(DEPRECATION_SAMPLE)
            cls.implemented = api_coverage.implemented_endpoints(d)
            cls.deprecated = api_coverage.deprecated_methods(d)
        cls.snapshot = {"index": "https://example.com/", "index_last_accessed": "2026-11-16", "removed": REMOVED,
                        "endpoints": [{"method": "GET", "path": "/api/v2/space", "title": "Get Space",
                                       "url": "https://developer.nulab.com/docs/backlog/api/2/get-space/",
                                       "last_accessed": "2026-11-16"}]}

    def test_deprecated_methods(self):
        self.assertEqual({"Sample.marked", "Sample.warns", "Sample.helper"}, self.deprecated)

    def test_violations_are_calls_to_removed_endpoints_from_methods_that_are_not_deprecated(self):
        self.assertEqual([
            "GET /api/v2/projects/:projectIdOrKey/groups: Sample.plain",
            "GET /api/v2/statuses: Sample.other_warning",
        ], api_coverage.removed_endpoint_violations(self.snapshot, self.implemented, self.deprecated))

    def test_render_lists_removed_endpoints_and_not_as_undocumented(self):
        text = api_coverage.render(self.snapshot, self.implemented, self.deprecated)

        self.assertNotIn("not in the official API reference", text)
        self.assertIn("## Removed endpoints", text)
        self.assertIn("| POST | `users` | Add User | Removed from the reference (confirmed 2026-11-16) | — | `Sample.marked()` (deprecated) |", text)
        self.assertIn("| GET | `groups` | [Get List of Groups](https://example.com/notice) | "
                      "[2.113.3 (2025-09-11)](https://example.com/changelog) | `GET teams` | `Sample.warns()` (deprecated) |", text)
        self.assertIn("| GET | `statuses` | Get Status List | 2.113.3 | — | `Sample.other_warning()` |", text)
        self.assertIn("- Add User, Delete User: gone", text)

    def test_main_fails_on_violations(self):
        with mock.patch.object(api_coverage, "implemented_endpoints", return_value=self.implemented), \
                mock.patch.object(api_coverage, "deprecated_methods", return_value=self.deprecated), \
                mock.patch.object(api_coverage, "_load_snapshot", return_value=self.snapshot), \
                contextlib.redirect_stdout(io.StringIO()) as out:
            self.assertEqual(1, api_coverage.main(["api_coverage.py", "check"]))
        self.assertIn("::error::GET /api/v2/statuses: Sample.other_warning calls an endpoint that Backlog removed", out.getvalue())

    def test_package_calls_no_removed_endpoint_unless_deprecated(self):
        snapshot = api_coverage._load_snapshot()
        self.assertTrue(snapshot["removed"])
        self.assertEqual([], api_coverage.removed_endpoint_violations(
            snapshot, api_coverage.implemented_endpoints(), api_coverage.deprecated_methods()))
        self.assertTrue({"User.add", "User.update", "User.delete"} <= api_coverage.deprecated_methods())


class TestEndpointList(unittest.TestCase):
    def _load(self, data):
        import json
        with tempfile.NamedTemporaryFile("w", suffix=".json", delete=False) as f:
            json.dump(data, f)
        try:
            with mock.patch.object(api_coverage, "ENDPOINTS_JSON", f.name):
                return api_coverage._load_snapshot()
        finally:
            os.unlink(f.name)

    def test_valid(self):
        entry = {"method": "GET", "path": "/api/v2/space", "title": "Get Space",
                 "url": "https://developer.nulab.com/docs/backlog/api/2/get-space/", "last_accessed": "2026-11-15"}
        self.assertEqual([entry], self._load({"index": "x", "index_last_accessed": "2026-11-15", "endpoints": [entry]})["endpoints"])

    def test_invalid(self):
        bad = {"method": "FETCH", "path": "space", "title": "t", "url": "https://example.com/", "last_accessed": "Nov 15"}
        with self.assertRaises(SystemExit) as cm:
            self._load({"index": "x", "index_last_accessed": "2026-11-15", "endpoints": [bad, {"method": "GET"}]})
        message = str(cm.exception)
        for expected in ["invalid method", "must start with /api/v2/", "developer.nulab.com", "YYYY-MM-DD", "missing"]:
            self.assertIn(expected, message)

    def test_invalid_removed_entries(self):
        current = {"method": "GET", "path": "/api/v2/space", "title": "Get Space",
                   "url": "https://developer.nulab.com/docs/backlog/api/2/get-space/", "last_accessed": "2026-11-15"}
        removed = [
            {"method": "GET", "path": "/api/v2/space", "title": "dup", "note": "n", "confirmed_on": "2026-11-16"},
            {"method": "GET", "path": "/api/v2/groups", "title": "no reason", "confirmed_on": "2026-11-16"},
            {"method": "GET", "path": "/api/v2/statuses", "title": "bad", "removed_in": "2.113.3",
             "removed_on": "Sep 2025", "announcement": "http://example.com", "confirmed_on": "2026-11-16"},
            {"method": "GET", "path": "/api/v2/x"},
        ]
        with self.assertRaises(SystemExit) as cm:
            self._load({"index": "x", "index_last_accessed": "2026-11-15", "endpoints": [current], "removed": removed})
        message = str(cm.exception)
        for expected in ["also listed as a current endpoint", "give removed_in", "removed_on must be a YYYY-MM-DD",
                         "announcement must be an https URL", "removed[3] is missing title, confirmed_on"]:
            self.assertIn(expected, message)


if __name__ == "__main__":
    unittest.main()
