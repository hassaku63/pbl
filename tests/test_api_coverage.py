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


if __name__ == "__main__":
    unittest.main()
