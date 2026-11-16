# coding: utf-8
"""
Tests for the webhook resource.
"""

import json
import unittest
from urllib.parse import parse_qs

from backlog.base import BacklogAPI
from tests import fake_http

API_ENDPOINT = "https://{space}.backlog.jp/api/v2/{uri}"


class TestWebhook(unittest.TestCase):
    def setUp(self):
        self.space = "space"
        self.api = BacklogAPI(self.space, "api_key")

    @fake_http.activate
    def test_requests(self):
        w = self.api.webhook
        cases = [
            ("list", lambda: w.list("TEST"), "GET", "projects/TEST/webhooks", {}),
            ("add", lambda: w.add("TEST", "hook", "https://example.com/hook", description="d", activityTypeIds=[1, 2]),
             "POST", "projects/TEST/webhooks",
             {"name": ["hook"], "hookUrl": ["https://example.com/hook"], "description": ["d"], "activityTypeIds[]": ["1", "2"]}),
            ("add (all events)", lambda: w.add(1, "hook", "https://example.com/hook", allEvent=True),
             "POST", "projects/1/webhooks", {"name": ["hook"], "hookUrl": ["https://example.com/hook"], "allEvent": ["true"]}),
            ("get", lambda: w.get("TEST", 7), "GET", "projects/TEST/webhooks/7", {}),
            ("update", lambda: w.update("TEST", 7, name="renamed", allEvent=False),
             "PATCH", "projects/TEST/webhooks/7", {"name": ["renamed"], "allEvent": ["false"]}),
            ("delete", lambda: w.delete("TEST", 7), "DELETE", "projects/TEST/webhooks/7", {}),
        ]
        for name, call, method, uri, form in cases:
            with self.subTest(name):
                fake_http.add(method, API_ENDPOINT.format(space=self.space, uri=uri), body=json.dumps({"called": name}))

                result = call()

                req = fake_http.last_request()
                self.assertEqual(method, req.method)
                self.assertEqual("/api/v2/" + uri, req.path.split("?")[0])
                self.assertEqual(form, parse_qs(req.body.decode()))
                self.assertEqual({"called": name}, result)


if __name__ == "__main__":
    unittest.main()
