# coding: utf-8
"""
Tests for the activity (recent updates) resource.
"""

import json
import unittest
from urllib.parse import parse_qs

from backlog.base import BacklogAPI
from tests import fake_http

API_ENDPOINT = "https://{space}.backlog.jp/api/v2/{uri}"


class TestActivity(unittest.TestCase):
    def setUp(self):
        self.space = "space"
        self.api = BacklogAPI(self.space, "api_key")

    @fake_http.activate
    def test_requests(self):
        a = self.api.activity
        cases = [
            ("list", lambda: a.list(activityTypeId=[1, 2], minId=5, maxId=9, count=10, order="asc"),
             "space/activities",
             {"activityTypeId[]": ["1", "2"], "minId": ["5"], "maxId": ["9"], "count": ["10"], "order": ["asc"]}),
            ("list (defaults)", lambda: a.list(), "space/activities", {}),
            ("list_project", lambda: a.list_project("TEST", activityTypeId=3), "projects/TEST/activities",
             {"activityTypeId[]": ["3"]}),
            ("list_user", lambda: a.list_user(12, count=5), "users/12/activities", {"count": ["5"]}),
            ("get", lambda: a.get(345), "activities/345", {}),
        ]
        for name, call, uri, query in cases:
            with self.subTest(name):
                fake_http.add(fake_http.GET, API_ENDPOINT.format(space=self.space, uri=uri), body=json.dumps({"called": name}))

                result = call()

                req = fake_http.last_request()
                self.assertEqual("GET", req.method)
                self.assertEqual("/api/v2/" + uri, req.path.split("?")[0])
                self.assertEqual(query, req.querystring)
                self.assertEqual({}, parse_qs(req.body.decode()))
                self.assertEqual({"called": name}, result)


if __name__ == "__main__":
    unittest.main()
