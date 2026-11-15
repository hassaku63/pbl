# coding: utf-8
"""
Tests for the notification resource.
"""

import json
import unittest
from urllib.parse import parse_qs

from backlog._params import bool_params
from backlog.base import BacklogAPI
from tests import fake_http

API_ENDPOINT = "https://{space}.backlog.jp/api/v2/{uri}"


class TestNotification(unittest.TestCase):
    def setUp(self):
        self.space = "space"
        self.api = BacklogAPI(self.space, "api_key")

    @fake_http.activate
    def test_requests(self):
        n = self.api.notification
        cases = [
            ("list", lambda: n.list(count=10, order="asc", senderId=3),
             "GET", "notifications", {"count": ["10"], "order": ["asc"], "senderId": ["3"]}),
            ("list (defaults)", lambda: n.list(), "GET", "notifications", {}),
            ("count", lambda: n.count(resourceAlreadyRead=False), "GET", "notifications/count", {"resourceAlreadyRead": ["false"]}),
            ("count (alreadyRead)", lambda: n.count(alreadyRead=True), "GET", "notifications/count", {"alreadyRead": ["true"]}),
            ("reset_unread_count", lambda: n.reset_unread_count(), "POST", "notifications/markAsRead", {}),
        ]
        for name, call, method, uri, query in cases:
            with self.subTest(name):
                fake_http.add(method, API_ENDPOINT.format(space=self.space, uri=uri), body=json.dumps({"called": name}))

                result = call()

                req = fake_http.last_request()
                self.assertEqual(method, req.method)
                self.assertEqual("/api/v2/" + uri, req.path.split("?")[0])
                self.assertEqual(query, req.querystring)
                self.assertEqual({}, parse_qs(req.body.decode()))
                self.assertEqual({"called": name}, result)

    @fake_http.activate
    def test_mark_as_read(self):
        # The API answers 204 No Content.
        fake_http.add(fake_http.POST, API_ENDPOINT.format(space=self.space, uri="notifications/7/markAsRead"), body="", status=204)

        self.assertIsNone(self.api.notification.mark_as_read(7))
        self.assertEqual("POST", fake_http.last_request().method)


class TestBoolParams(unittest.TestCase):
    def test_bool_params(self):
        self.assertEqual({"a": "true", "b": "false", "c": None, "d": 1}, bool_params({"a": True, "b": False, "c": None, "d": 1}))


if __name__ == "__main__":
    unittest.main()
