# coding: utf-8
"""
Tests for the project, user and team icons, and the administrators and teams of a project.
"""

import json
import unittest

from backlog.base import BacklogAPI
from tests import fake_http

API_ENDPOINT = "https://{space}.backlog.jp/api/v2/{uri}"


class TestIcons(unittest.TestCase):
    def setUp(self):
        self.space = "space"
        self.api = BacklogAPI(self.space, "api_key")

    @fake_http.activate
    def test_icons(self):
        cases = [
            ("project", lambda: self.api.project.get_image("TEST"), "projects/TEST/image", "logo_mark.png"),
            ("user", lambda: self.api.user.get_icon(12), "users/12/icon", "person_168.gif"),
            ("team", lambda: self.api.team.get_icon(3), "teams/3/icon", "team_168.gif"),
        ]
        for name, call, uri, filename in cases:
            with self.subTest(name):
                fake_http.add(fake_http.GET, API_ENDPOINT.format(space=self.space, uri=uri), body=b"GIF89a",
                              content_type="application/octet-stream",
                              headers={"Content-Disposition": 'attachment;filename="{}"'.format(filename)})

                self.assertEqual({"name": filename, "data": b"GIF89a"}, call())
                self.assertEqual("/api/v2/" + uri, fake_http.last_request().path.split("?")[0])


class TestProjectMembers(unittest.TestCase):
    def setUp(self):
        self.space = "space"
        self.api = BacklogAPI(self.space, "api_key")

    @fake_http.activate
    def test_requests(self):
        p = self.api.project
        cases = [
            ("list_administrators", lambda: p.list_administrators("TEST"), "projects/TEST/administrators"),
            ("list_teams", lambda: p.list_teams(1), "projects/1/teams"),
        ]
        for name, call, uri in cases:
            with self.subTest(name):
                fake_http.add(fake_http.GET, API_ENDPOINT.format(space=self.space, uri=uri), body=json.dumps([{"called": name}]))

                self.assertEqual([{"called": name}], call())

                req = fake_http.last_request()
                self.assertEqual("GET", req.method)
                self.assertEqual("/api/v2/" + uri, req.path.split("?")[0])


if __name__ == "__main__":
    unittest.main()
