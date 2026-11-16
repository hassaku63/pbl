# coding: utf-8
"""
Tests for listing and downloading the shared files of a project.
"""

import unittest

from backlog.base import BacklogAPI
from tests import fake_http

API_ENDPOINT = "https://{space}.backlog.jp/api/v2/{uri}"


class TestSharedFile(unittest.TestCase):
    def setUp(self):
        self.space = "space"
        self.api = BacklogAPI(self.space, "api_key")

    @fake_http.activate
    def test_list_shared_files(self):
        cases = [
            ("root", {}, "projects/TEST/files/metadata/", {}),
            ("directory", {"path": "/docs/specs/", "order": "asc", "offset": 20, "count": 10},
             "projects/TEST/files/metadata/docs/specs", {"order": ["asc"], "offset": ["20"], "count": ["10"]}),
            ("non-ASCII directory", {"path": "資料"}, "projects/TEST/files/metadata/%E8%B3%87%E6%96%99", {}),
        ]
        for name, kwargs, uri, query in cases:
            with self.subTest(name):
                fake_http.add(fake_http.GET, API_ENDPOINT.format(space=self.space, uri=uri), json_body=[{"id": 1}])

                result = self.api.project.list_shared_files("TEST", **kwargs)

                req = fake_http.last_request()
                self.assertEqual("/api/v2/" + uri, req.path.split("?")[0])
                self.assertEqual(query, req.querystring)
                self.assertEqual([{"id": 1}], result)

    @fake_http.activate
    def test_get_shared_file(self):
        fake_http.add(fake_http.GET, API_ENDPOINT.format(space=self.space, uri="projects/TEST/files/825952"),
                      body=b"\x00\x01data", content_type="application/octet-stream",
                      headers={"Content-Disposition": 'attachment;filename="20091130.txt"'})

        result = self.api.project.get_shared_file("TEST", 825952)

        self.assertEqual({"id": 825952, "name": "20091130.txt", "data": b"\x00\x01data"}, result)
        self.assertEqual("GET", fake_http.last_request().method)


if __name__ == "__main__":
    unittest.main()
