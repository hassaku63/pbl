# coding: utf-8
"""
Tests for adding, updating and deleting the statuses and versions/milestones of a project.
"""

import json
import unittest
from urllib.parse import parse_qs

from backlog.base import BacklogAPI
from tests import fake_http

API_ENDPOINT = "https://{space}.backlog.jp/api/v2/{uri}"


class TestProjectStatusesAndVersions(unittest.TestCase):
    def setUp(self):
        self.space = "space"
        self.api = BacklogAPI(self.space, "api_key")

    @fake_http.activate
    def test_requests(self):
        p = self.api.project
        cases = [
            ("add_status", lambda: p.add_status("TEST", "Review", "#3b9dbd"),
             "POST", "projects/TEST/statuses", {"name": ["Review"], "color": ["#3b9dbd"]}),
            ("update_status", lambda: p.update_status("TEST", 5, color="#393939"),
             "PATCH", "projects/TEST/statuses/5", {"color": ["#393939"]}),
            ("delete_status", lambda: p.delete_status("TEST", 5, substituteStatusId=1),
             "DELETE", "projects/TEST/statuses/5", {"substituteStatusId": ["1"]}),
            ("update_status_order", lambda: p.update_status_order("TEST", [1, 2, 5, 3, 4]),
             "PATCH", "projects/TEST/statuses/updateDisplayOrder", {"statusId[]": ["1", "2", "5", "3", "4"]}),
            ("add_version", lambda: p.add_version("TEST", "v1", startDate="2026-11-01", releaseDueDate="2026-11-30"),
             "POST", "projects/TEST/versions", {"name": ["v1"], "startDate": ["2026-11-01"], "releaseDueDate": ["2026-11-30"]}),
            ("add_version (name only)", lambda: p.add_version(1, "v1"), "POST", "projects/1/versions", {"name": ["v1"]}),
            ("update_version", lambda: p.update_version("TEST", 7, "v1", description="done", archived=True),
             "PATCH", "projects/TEST/versions/7", {"name": ["v1"], "description": ["done"], "archived": ["true"]}),
            ("update_version (unarchive)", lambda: p.update_version("TEST", 7, "v1", archived=False),
             "PATCH", "projects/TEST/versions/7", {"name": ["v1"], "archived": ["false"]}),
            ("delete_version", lambda: p.delete_version("TEST", 7), "DELETE", "projects/TEST/versions/7", {}),
        ]
        for name, call, method, uri, form in cases:
            with self.subTest(name):
                fake_http.add(method, API_ENDPOINT.format(space=self.space, uri=uri), body=json.dumps({"called": name}))

                result = call()

                req = fake_http.last_request()
                self.assertEqual(method, req.method)
                self.assertEqual("/api/v2/" + uri, req.path.split("?")[0])
                self.assertEqual({}, req.querystring)
                self.assertEqual(form, parse_qs(req.body.decode()))
                self.assertEqual({"called": name}, result)


if __name__ == "__main__":
    unittest.main()
