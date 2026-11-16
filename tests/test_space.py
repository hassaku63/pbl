# coding: utf-8
"""
Tests for the space information methods of BacklogAPI.
"""

import json
import unittest

from backlog.base import BacklogAPI
from tests import fake_http

API_ENDPOINT = "https://{space}.backlog.jp/api/v2/{uri}"


class TestSpace(unittest.TestCase):
    def setUp(self):
        self.space = "space"
        self.api = BacklogAPI(self.space, "api_key")

    @fake_http.activate
    def test_json_requests(self):
        cases = [
            ("get_space", self.api.get_space, "space"),
            ("get_space_licence", self.api.get_space_licence, "space/licence"),
            ("get_space_notification", self.api.get_space_notification, "space/notification"),
        ]
        for name, call, uri in cases:
            with self.subTest(name):
                fake_http.add(fake_http.GET, API_ENDPOINT.format(space=self.space, uri=uri), body=json.dumps({"called": name}))

                self.assertEqual({"called": name}, call())

                req = fake_http.last_request()
                self.assertEqual("GET", req.method)
                self.assertEqual("/api/v2/" + uri, req.path.split("?")[0])

    @fake_http.activate
    def test_get_space_image(self):
        fake_http.add(fake_http.GET, API_ENDPOINT.format(space=self.space, uri="space/image"), body=b"\x89PNG",
                      content_type="application/octet-stream",
                      headers={"Content-Disposition": 'attachment;filename="logo_mark.png"'})

        self.assertEqual({"name": "logo_mark.png", "data": b"\x89PNG"}, self.api.get_space_image())

    def test_space_attribute_is_still_the_space_key(self):
        self.assertEqual("space", self.api.space)


if __name__ == "__main__":
    unittest.main()
