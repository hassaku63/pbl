# coding: utf-8
"""
Tests for the lists used to look up IDs when adding or updating issues:
priorities, resolutions, project statuses and versions/milestones.
"""

import json
import unittest

from backlog.base import BacklogAPI
from tests import fake_http

API_ENDPOINT = "https://{space}.backlog.jp/api/v2/{uri}"


class TestReferenceData(unittest.TestCase):
    def setUp(self):
        self.space = "space"
        self.api = BacklogAPI(self.space, "api_key")

    @fake_http.activate
    def test_lists(self):
        cases = [
            ("priority.list", lambda: self.api.priority.list(), "priorities",
             [{"id": 2, "name": "High"}, {"id": 3, "name": "Normal"}, {"id": 4, "name": "Low"}]),
            ("resolution.list", lambda: self.api.resolution.list(), "resolutions",
             [{"id": 0, "name": "Fixed"}, {"id": 1, "name": "Won't Fix"}]),
            ("project.list_statuses", lambda: self.api.project.list_statuses("PRJ"), "projects/PRJ/statuses",
             [{"id": 1, "projectId": 1, "name": "Open", "color": "#ed8077", "displayOrder": 1000}]),
            ("project.list_versions", lambda: self.api.project.list_versions(1), "projects/1/versions",
             [{"id": 3, "projectId": 1, "name": "wait for release", "archived": False}]),
        ]
        for name, call, uri, expects in cases:
            with self.subTest(name):
                fake_http.add(fake_http.GET, API_ENDPOINT.format(space=self.space, uri=uri), body=json.dumps(expects))

                self.assertEqual(expects, call())

                req = fake_http.last_request()
                self.assertEqual("GET", req.method)
                self.assertEqual("/api/v2/" + uri, req.path)
                self.assertEqual(b"", req.body)


if __name__ == "__main__":
    unittest.main()
