# coding: utf-8

import unittest
import httpretty
import json
from backlog.util import load_conf
from backlog.base import BacklogAPI

API_ENDPOINT = "https://{space}.backlog.jp/api/v2/{uri}"


class TestApi(unittest.TestCase):
    def setUp(self):
        self.conf = load_conf("./conf.default.yml")["backlog"]
        self.api = BacklogAPI(self.conf["space"], self.conf["api_key"])
        self.space = self.conf["space"]
        self.api_key = self.conf["api_key"]

    @httpretty.activate
    def test_invoke_get(self):
        expects = {
            "ok": True
        }
        URI = "test"

        httpretty.register_uri(
            httpretty.GET,
            API_ENDPOINT.format(space=self.space, uri=URI),
            body=json.dumps(expects),
            content_type="application/json",
            status=200
        )

        resp = self.api.invoke_method("GET", URI)
        self.assertEqual(expects, resp.json())

    @httpretty.activate
    def test_invoke_post(self):
        expects = {
            "ok": True
        }
        URI = "test"

        # Status 200
        httpretty.register_uri(
            httpretty.POST,
            API_ENDPOINT.format(space=self.space, uri=URI),
            body=json.dumps(expects),
            content_type="application/json",
            status=200
        )

        resp = self.api.invoke_method("POST", URI)
        self.assertEqual(200, resp.status_code)
        self.assertEqual(expects, resp.json())

        # status 201 (created)
        httpretty.register_uri(
            httpretty.POST,
            API_ENDPOINT.format(space=self.space, uri=URI),
            body=json.dumps(expects),
            content_type="application/json",
            status=201
        )

        resp = self.api.invoke_method("POST", URI)
        self.assertEqual(201, resp.status_code)
        self.assertEqual(expects, resp.json())


if __name__ == "__main__":
    unittest.main(warnings='ignore')