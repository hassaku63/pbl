# coding: utf-8
"""
Tests for User.get_myself() and the watching resource.
"""

import json
import unittest
from urllib.parse import parse_qs

from backlog.base import BacklogAPI
from tests import fake_http

API_ENDPOINT = "https://{space}.backlog.jp/api/v2/{uri}"


class TestWatching(unittest.TestCase):
    def setUp(self):
        self.space = "space"
        self.api = BacklogAPI(self.space, "api_key")

    @fake_http.activate
    def test_requests(self):
        w = self.api.watching
        cases = [
            ("user.get_myself", lambda: self.api.user.get_myself(), "GET", "users/myself", {}, {}),
            ("list", lambda: w.list(1, order="asc", resourceAlreadyRead=False, **{"issueId[]": [10, 11]}),
             "GET", "users/1/watchings", {"order": ["asc"], "resourceAlreadyRead": ["false"], "issueId[]": ["10", "11"]}, {}),
            ("list (defaults)", lambda: w.list(1), "GET", "users/1/watchings", {}, {}),
            ("count", lambda: w.count(1, alreadyRead=True), "GET", "users/1/watchings/count", {"alreadyRead": ["true"]}, {}),
            ("get", lambda: w.get(5), "GET", "watchings/5", {}, {}),
            ("add", lambda: w.add("PRJ-1", note="check"), "POST", "watchings", {}, {"issueIdOrKey": ["PRJ-1"], "note": ["check"]}),
            ("add (no note)", lambda: w.add("PRJ-1"), "POST", "watchings", {}, {"issueIdOrKey": ["PRJ-1"]}),
            ("update", lambda: w.update(5, "new note"), "PATCH", "watchings/5", {}, {"note": ["new note"]}),
            ("delete", lambda: w.delete(5), "DELETE", "watchings/5", {}, {}),
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
    def test_mark_as_read(self):
        # The API answers 204 No Content.
        fake_http.add(fake_http.POST, API_ENDPOINT.format(space=self.space, uri="watchings/5/markAsRead"), body="", status=204)

        self.assertIsNone(self.api.watching.mark_as_read(5))
        self.assertEqual("POST", fake_http.last_request().method)


if __name__ == "__main__":
    unittest.main()
