# coding: utf-8
"""
Tests for parameters added to older methods after comparing them with the API reference (0.19.0).
"""

import json
import unittest
from urllib.parse import parse_qs

from backlog.base import BacklogAPI
from tests import fake_http

API_ENDPOINT = "https://{space}.backlog.jp/api/v2/{uri}"


class TestAddedParameters(unittest.TestCase):
    def setUp(self):
        self.space = "space"
        self.api = BacklogAPI(self.space, "api_key")

    @fake_http.activate
    def test_requests(self):
        p = self.api.project
        cases = [
            ("project.create", lambda: p.create("P", "P", grandchildIssueEnabled=True, useDocument=False, useWiki=True),
             "POST", "projects", {}, {"name": ["P"], "key": ["P"], "grandchildIssueEnabled": ["true"],
                                      "useDocument": ["false"], "useWiki": ["true"]}),
            ("project.update", lambda: p.update("P", useDocument=True, archived=False),
             "PATCH", "projects/P", {}, {"useDocument": ["true"], "archived": ["false"]}),
            ("project.list (default)", lambda: p.list(), "GET", "projects", {"archived": ["false"], "all": ["false"]}, {}),
            ("project.list (all projects)", lambda: p.list(archived=None, all_=True), "GET", "projects", {"all": ["true"]}, {}),
            ("add_issue_type", lambda: p.add_issue_type("P", "Bug", "#990000", templateSummary="[Bug] ", templateDescription="Steps"),
             "POST", "projects/P/issueTypes", {},
             {"name": ["Bug"], "color": ["#990000"], "templateSummary": ["[Bug] "], "templateDescription": ["Steps"]}),
            ("add_issue_type (no template)", lambda: p.add_issue_type("P", "Bug", "#990000"),
             "POST", "projects/P/issueTypes", {}, {"name": ["Bug"], "color": ["#990000"]}),
            ("update_issue_type (template only)", lambda: p.update_issue_type("P", 3, templateSummary="x"),
             "PATCH", "projects/P/issueTypes/3", {}, {"templateSummary": ["x"]}),
            ("add_pull_request_comment", lambda: self.api.git.add_pull_request_comment("P", "repo", 1, "LGTM", attachmentId=[5, 6]),
             "POST", "projects/P/git/repositories/repo/pullRequests/1/comments", {},
             {"content": ["LGTM"], "attachmentId[]": ["5", "6"]}),
        ]
        for name, call, method, uri, query, form in cases:
            with self.subTest(name):
                fake_http.add(method, API_ENDPOINT.format(space=self.space, uri=uri), body=json.dumps({"called": name}))

                self.assertEqual({"called": name}, call())

                req = fake_http.last_request()
                self.assertEqual(method, req.method)
                self.assertEqual("/api/v2/" + uri, req.path.split("?")[0])
                self.assertEqual(query, req.querystring)
                self.assertEqual(form, parse_qs(req.body.decode(), keep_blank_values=True))


if __name__ == "__main__":
    unittest.main()
