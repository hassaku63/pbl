# coding: utf-8
"""
Tests for the star resource.
"""

import json
import unittest
from urllib.parse import parse_qs

from backlog.base import BacklogAPI
from tests import fake_http

API_ENDPOINT = "https://{space}.backlog.jp/api/v2/{uri}"


class TestStar(unittest.TestCase):
    def setUp(self):
        self.space = "space"
        self.api = BacklogAPI(self.space, "api_key")

    @fake_http.activate
    def test_add(self):
        # The API answers 204 No Content.
        cases = [
            ({"issueId": 1}, {"issueId": ["1"]}),
            ({"commentId": 2}, {"commentId": ["2"]}),
            ({"wikiId": 3}, {"wikiId": ["3"]}),
            ({"pullRequestId": 4}, {"pullRequestId": ["4"]}),
            ({"pullRequestCommentId": 5}, {"pullRequestCommentId": ["5"]}),
        ]
        for kwargs, form in cases:
            with self.subTest(kwargs=kwargs):
                fake_http.add(fake_http.POST, API_ENDPOINT.format(space=self.space, uri="stars"), body="", status=204)

                self.assertIsNone(self.api.star.add(**kwargs))

                req = fake_http.last_request()
                self.assertEqual("POST", req.method)
                self.assertEqual(form, parse_qs(req.body.decode()))

    def test_add_takes_exactly_one_target(self):
        for kwargs in ({}, {"issueId": 1, "wikiId": 2}):
            with self.subTest(kwargs=kwargs), self.assertRaises(ValueError):
                self.api.star.add(**kwargs)

    @fake_http.activate
    def test_delete(self):
        fake_http.add(fake_http.DELETE, API_ENDPOINT.format(space=self.space, uri="stars/9"), body="", status=204)

        self.assertIsNone(self.api.star.delete(9))
        self.assertEqual("DELETE", fake_http.last_request().method)

    @fake_http.activate
    def test_received(self):
        s = self.api.star
        cases = [
            ("list_received", lambda: s.list_received(1, minId=2, maxId=8, count=5, order="asc"), "users/1/stars",
             {"minId": ["2"], "maxId": ["8"], "count": ["5"], "order": ["asc"]}),
            ("list_received (defaults)", lambda: s.list_received(1), "users/1/stars", {}),
            ("count_received", lambda: s.count_received(1, since="2026-01-01", until="2026-12-31"), "users/1/stars/count",
             {"since": ["2026-01-01"], "until": ["2026-12-31"]}),
        ]
        for name, call, uri, query in cases:
            with self.subTest(name):
                fake_http.add(fake_http.GET, API_ENDPOINT.format(space=self.space, uri=uri), body=json.dumps({"called": name}))

                result = call()

                req = fake_http.last_request()
                self.assertEqual("GET", req.method)
                self.assertEqual("/api/v2/" + uri, req.path.split("?")[0])
                self.assertEqual(query, req.querystring)
                self.assertEqual({"called": name}, result)


if __name__ == "__main__":
    unittest.main()
