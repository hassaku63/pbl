# coding: utf-8

import unittest
from tests import fake_http

import json
from backlog.base import BacklogAPI, DEFAULT_TIMEOUT

API_ENDPOINT = "https://{space}.backlog.jp/api/v2/{uri}"


class TestApi(unittest.TestCase):
    def setUp(self):
        self.api = BacklogAPI("space", "api_key")
        self.space = "space"
        self.api_key = "api_key"

    @fake_http.activate
    def test_invoke_get(self):
        expects = {
            "ok": True
        }
        _uri = "test"

        # Status Pattern
        _http_statuses = [200, 201]

        for _status_code in _http_statuses:
            with self.subTest(status_code=_status_code):
                fake_http.add(
                    fake_http.GET,
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
        fake_http.add(
            fake_http.GET,
            API_ENDPOINT.format(space=self.space, uri=_uri),
            content_type="application/json",
            status=204
        )

        resp = self.api.invoke_method("GET", _uri)
        self.assertEqual(204, resp.status_code)

    @fake_http.activate
    def test_invoke_post(self):
        expects = {
            "ok": True
        }
        _uri = "test"

        # Status Pattern
        _http_statuses = [200, 201]

        for _status_code in _http_statuses:
            with self.subTest(status_code=_status_code):
                fake_http.add(
                    fake_http.POST,
                    API_ENDPOINT.format(space=self.space, uri=_uri),
                    body=json.dumps(expects),
                    content_type="application/json",
                    status=_status_code
                )

                resp = self.api.invoke_method("POST", _uri)
                self.assertEqual(_status_code, resp.status_code)
                self.assertEqual(expects, resp.json())

    @fake_http.activate
    def test_invoke_delete(self):
        expects = {
            "ok": True
        }
        _uri = "test"

        # Status 200
        fake_http.add(
            fake_http.DELETE,
            API_ENDPOINT.format(space=self.space, uri=_uri),
            body=json.dumps(expects),
            content_type="application/json",
            status=200
        )

        resp = self.api.invoke_method("DELETE", _uri)
        self.assertEqual(200, resp.status_code)
        self.assertEqual(expects, resp.json())

    @fake_http.activate
    def test_invoke_patch(self):
        expects = {
            "ok": True
        }
        _uri = "test"

        # Status 200
        fake_http.add(
            fake_http.PATCH,
            API_ENDPOINT.format(space=self.space, uri=_uri),
            body=json.dumps(expects),
            content_type="application/json",
            status=200
        )

        resp = self.api.invoke_method("PATCH", _uri)
        self.assertEqual(200, resp.status_code)
        self.assertEqual(expects, resp.json())

    @fake_http.activate
    def test_api_key_is_sent_in_header_not_query(self):
        for _method in ["GET", "POST", "DELETE", "PATCH"]:
            with self.subTest(method=_method):
                fake_http.add(
                    getattr(fake_http, _method),
                    API_ENDPOINT.format(space=self.space, uri="test"),
                    body="{}",
                    status=200
                )

                self.api.invoke_method(_method, "test")

                req = fake_http.last_request()
                self.assertEqual(self.api_key, req.headers.get("Backlog-API-Key"))
                self.assertNotIn("apiKey", req.querystring)
                self.assertNotIn(self.api_key, req.path)

    @fake_http.activate
    def test_api_key_does_not_leak_between_instances(self):
        """Regression: a shared mutable default argument used to keep the first instance's API key."""
        for _space in ["space-a", "space-b"]:
            fake_http.add(
                fake_http.GET,
                API_ENDPOINT.format(space=_space, uri="users"),
                body="[]",
                status=200
            )
        api_a = BacklogAPI("space-a", "KEY_A")
        api_b = BacklogAPI("space-b", "KEY_B")

        api_a.invoke_method("GET", "users")
        api_b.invoke_method("GET", "users")

        req = fake_http.last_request()
        self.assertEqual("space-b.backlog.jp", req.host)
        self.assertEqual("KEY_B", req.headers.get("Backlog-API-Key"))

    @fake_http.activate
    def test_caller_arguments_are_not_mutated(self):
        fake_http.add(
            fake_http.POST,
            API_ENDPOINT.format(space=self.space, uri="test"),
            body="{}",
            status=200
        )
        query_param = {"q": "1"}
        request_param = {"name": "x"}
        headers = {"X-Test": "1"}

        self.api.invoke_method("POST", "test", query_param=query_param, request_param=request_param, headers=headers)

        self.assertEqual({"q": "1"}, query_param)
        self.assertEqual({"name": "x"}, request_param)
        self.assertEqual({"X-Test": "1"}, headers)
        req = fake_http.last_request()
        self.assertEqual("1", req.headers.get("X-Test"))
        self.assertEqual(self.api_key, req.headers.get("Backlog-API-Key"))

    @fake_http.activate
    def test_timeout(self):
        fake_http.add(fake_http.GET, API_ENDPOINT.format(space=self.space, uri="test"), body="{}")

        self.api.invoke_method("GET", "test")
        self.assertEqual(DEFAULT_TIMEOUT, fake_http.last_request().timeout)

        BacklogAPI("space", "api_key", timeout=5).invoke_method("GET", "test")
        self.assertEqual(5, fake_http.last_request().timeout)

        self.api.invoke_method("GET", "test", timeout=1)
        self.assertEqual(1, fake_http.last_request().timeout)

    def test_invalid_space(self):
        for _space in ["", "evil.example.com/#", "space.backlog.com", "a b", "-space", None]:
            with self.subTest(space=_space):
                with self.assertRaises(ValueError):
                    BacklogAPI(_space, "api_key")

        for _space in ["space", "my-space", "Space01"]:
            with self.subTest(space=_space):
                BacklogAPI(_space, "api_key")


if __name__ == "__main__":
    unittest.main(warnings='ignore')
