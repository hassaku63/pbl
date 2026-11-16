# coding: utf-8
"""
Tests for the wiki page count, tags, history, stars and shared files.
"""

import json
import unittest
from urllib.parse import parse_qs

from backlog.base import BacklogAPI
from tests import fake_http

API_ENDPOINT = "https://{space}.backlog.jp/api/v2/{uri}"


class TestWikiMore(unittest.TestCase):
    def setUp(self):
        self.space = "space"
        self.api = BacklogAPI(self.space, "api_key")

    @fake_http.activate
    def test_requests(self):
        w = self.api.wiki
        cases = [
            ("list (keyword)", lambda: w.list("TEST", keyword="spec"),
             "GET", "wikis", {"projectIdOrKey": ["TEST"], "keyword": ["spec"]}, {}),
            ("list", lambda: w.list("TEST"), "GET", "wikis", {"projectIdOrKey": ["TEST"]}, {}),
            ("count", lambda: w.count("TEST"), "GET", "wikis/count", {"projectIdOrKey": ["TEST"]}, {}),
            ("list_tags", lambda: w.list_tags(1), "GET", "wikis/tags", {"projectIdOrKey": ["1"]}, {}),
            ("list_history", lambda: w.list_history(3, minId=1, count=5, order="asc"),
             "GET", "wikis/3/history", {"minId": ["1"], "count": ["5"], "order": ["asc"]}, {}),
            ("list_stars", lambda: w.list_stars(3), "GET", "wikis/3/stars", {}, {}),
            ("list_shared_files", lambda: w.list_shared_files(3), "GET", "wikis/3/sharedFiles", {}, {}),
            ("link_shared_files", lambda: w.link_shared_files(3, [10, 11]),
             "POST", "wikis/3/sharedFiles", {}, {"fileId[]": ["10", "11"]}),
            ("link_shared_files (one)", lambda: w.link_shared_files(3, 10),
             "POST", "wikis/3/sharedFiles", {}, {"fileId[]": ["10"]}),
            ("unlink_shared_file", lambda: w.unlink_shared_file(3, 10), "DELETE", "wikis/3/sharedFiles/10", {}, {}),
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
