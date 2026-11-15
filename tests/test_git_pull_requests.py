# coding: utf-8
"""
Tests for the Git repository and pull request methods: the documented method, path, query string and body are sent.
"""

import json
import unittest
from urllib.parse import parse_qs

from backlog.base import BacklogAPI
from tests import fake_http

API_ENDPOINT = "https://{space}.backlog.jp/api/v2/{uri}"
PR = "projects/PRJ/git/repositories/repo/pullRequests/3"


class TestPullRequests(unittest.TestCase):
    def setUp(self):
        self.space = "space"
        self.api = BacklogAPI(self.space, "api_key")

    @fake_http.activate
    def test_requests(self):
        git = self.api.git
        cases = [
            ("get_git_repository", lambda: git.get_git_repository("PRJ", "repo"),
             "GET", "projects/PRJ/git/repositories/repo", {}, {}),
            ("get_pull_request", lambda: git.get_pull_request("PRJ", "repo", 3),
             "GET", PR, {}, {}),
            ("update_pull_request", lambda: git.update_pull_request(
                "PRJ", "repo", 3, summary="new", assigneeId=5, **{"notifiedUserId[]": [1, 2]}),
             "PATCH", PR, {}, {"summary": ["new"], "assigneeId": ["5"], "notifiedUserId[]": ["1", "2"]}),
            ("count_pull_requests", lambda: git.count_pull_requests("PRJ", "repo", **{"statusId[]": [1, 2]}),
             "GET", "projects/PRJ/git/repositories/repo/pullRequests/count", {"statusId[]": ["1", "2"]}, {}),
            ("list_pull_request_comments", lambda: git.list_pull_request_comments("PRJ", "repo", 3, count=5, order="asc"),
             "GET", PR + "/comments", {"count": ["5"], "order": ["asc"]}, {}),
            ("count_pull_request_comments", lambda: git.count_pull_request_comments("PRJ", "repo", 3),
             "GET", PR + "/comments/count", {}, {}),
            ("update_pull_request_comment", lambda: git.update_pull_request_comment("PRJ", "repo", 3, 9, "edited"),
             "PATCH", PR + "/comments/9", {}, {"content": ["edited"]}),
            ("list_pull_request_attachments", lambda: git.list_pull_request_attachments("PRJ", "repo", 3),
             "GET", PR + "/attachments", {}, {}),
            ("delete_pull_request_attachment", lambda: git.delete_pull_request_attachment("PRJ", "repo", 3, 7),
             "DELETE", PR + "/attachments/7", {}, {}),
        ]
        for name, call, method, uri, query, form in cases:
            with self.subTest(name):
                fake_http.add(method, API_ENDPOINT.format(space=self.space, uri=uri), body=json.dumps({"called": name}))

                result = call()

                req = fake_http.last_request()
                self.assertEqual(method, req.method)
                self.assertEqual("/api/v2/" + uri, req.path.split("?")[0])
                self.assertEqual(query, req.querystring)
                self.assertEqual(form, parse_qs(req.body.decode()))
                self.assertEqual({"called": name}, result)

    @fake_http.activate
    def test_get_pull_request_attachment(self):
        fake_http.add(
            fake_http.GET,
            API_ENDPOINT.format(space=self.space, uri=PR + "/attachments/7"),
            body=b"PK\x03\x04",
            content_type="application/zip",
            headers={"Content-Disposition": 'attachment; filename="logs.zip"'},
        )

        self.assertEqual(
            {"id": 7, "name": "logs.zip", "data": b"PK\x03\x04"},
            self.api.git.get_pull_request_attachment("PRJ", "repo", 3, 7),
        )


if __name__ == "__main__":
    unittest.main()
