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
        _uri = "test"

        # Status Pattern
        _http_statuses = [200, 201]

        for _status_code in _http_statuses:
            with self.subTest(status_code=_status_code):
                httpretty.register_uri(
                    httpretty.GET,
                    API_ENDPOINT.format(space=self.space, uri=_uri),
                    body=json.dumps(expects),
                    content_type="application/json",
                    status=_status_code
                )

                resp = self.api.invoke_method("GET", _uri)
                self.assertEqual(_status_code, resp.status_code)
                self.assertEqual(expects, resp.json())

        # Test 204(NO_CONTENT) Response
        #   NOTE: 204 response MUST NOT include a message-body.
        #   http://tools.ietf.org/search/rfc2616#section-10.2.5
        httpretty.register_uri(
            httpretty.GET,
            API_ENDPOINT.format(space=self.space, uri=_uri),
            content_type="application/json",
            status=204
        )

        resp = self.api.invoke_method("GET", _uri)
        self.assertEqual(204, resp.status_code)

    @httpretty.activate
    def test_invoke_post(self):
        expects = {
            "ok": True
        }
        _uri = "test"

        # Status Pattern
        _http_statuses = [200, 201]

        for _status_code in _http_statuses:
            with self.subTest(status_code=_status_code):
                httpretty.register_uri(
                    httpretty.POST,
                    API_ENDPOINT.format(space=self.space, uri=_uri),
                    body=json.dumps(expects),
                    content_type="application/json",
                    status=_status_code
                )

                resp = self.api.invoke_method("POST", _uri)
                self.assertEqual(_status_code, resp.status_code)
                self.assertEqual(expects, resp.json())

    @httpretty.activate
    def test_invoke_delete(self):
        expects = {
            "ok": True
        }
        _uri = "test"

        # Status 200
        httpretty.register_uri(
            httpretty.DELETE,
            API_ENDPOINT.format(space=self.space, uri=_uri),
            body=json.dumps(expects),
            content_type="application/json",
            status=200
        )

        resp = self.api.invoke_method("DELETE", _uri)
        self.assertEqual(200, resp.status_code)
        self.assertEqual(expects, resp.json())

    @httpretty.activate
    def test_invoke_patch(self):
        expects = {
            "ok": True
        }
        _uri = "test"

        # Status 200
        httpretty.register_uri(
            httpretty.PATCH,
            API_ENDPOINT.format(space=self.space, uri=_uri),
            body=json.dumps(expects),
            content_type="application/json",
            status=200
        )

        resp = self.api.invoke_method("PATCH", _uri)
        self.assertEqual(200, resp.status_code)
        self.assertEqual(expects, resp.json())


if __name__ == "__main__":
    unittest.main(warnings='ignore')