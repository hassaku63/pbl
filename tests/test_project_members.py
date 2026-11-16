# coding: utf-8
"""
Tests for adding and removing the users and teams of a project, and the team list of the space.
"""

import json
import unittest
from urllib.parse import parse_qs

from backlog.base import BacklogAPI
from tests import fake_http

API_ENDPOINT = "https://{space}.backlog.jp/api/v2/{uri}"


class TestProjectMembers(unittest.TestCase):
    def setUp(self):
        self.space = "space"
        self.api = BacklogAPI(self.space, "api_key")

    @fake_http.activate
    def test_requests(self):
        p = self.api.project
        cases = [
            ("add_user", lambda: p.add_user("TEST", 12), "POST", "projects/TEST/users", {}, {"userId": ["12"]}),
            ("delete_user", lambda: p.delete_user("TEST", 12), "DELETE", "projects/TEST/users", {}, {"userId": ["12"]}),
            ("add_team", lambda: p.add_team(1, 3), "POST", "projects/1/teams", {}, {"teamId": ["3"]}),
            ("delete_team", lambda: p.delete_team(1, 3), "DELETE", "projects/1/teams", {}, {"teamId": ["3"]}),
            ("team.list", lambda: self.api.team.list(order="asc", offset=20, count=10), "GET", "teams",
             {"order": ["asc"], "offset": ["20"], "count": ["10"]}, {}),
            ("team.list (defaults)", lambda: self.api.team.list(), "GET", "teams", {}, {}),
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


if __name__ == "__main__":
    unittest.main()
