# coding: utf-8
"""
Tests for the standard library HTTP client (backlog._http) and the transport behavior of BacklogAPI.

The integration tests talk to a local HTTP server, so they exercise urllib for real.
"""

import json
import ssl
import threading
import unittest
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from unittest import mock
from urllib.parse import parse_qs, urlsplit

from backlog import _http
from backlog.base import BacklogAPI, BacklogConnectionError, BacklogError
from tests import fake_http

API_ENDPOINT = "https://{space}.backlog.jp/api/v2/{uri}"


class _Handler(BaseHTTPRequestHandler):
    def log_message(self, *args):
        pass

    def _reply(self):
        length = int(self.headers.get("Content-Length") or 0)
        body = self.rfile.read(length) if length else b""
        path = urlsplit(self.path)
        if path.path == "/redirect":
            self.send_response(302)
            self.send_header("Location", "http://example.invalid/stolen")
            self.end_headers()
            return
        status = int(parse_qs(path.query).get("status", ["200"])[0])
        payload = json.dumps({
            "method": self.command,
            "path": path.path,
            "query": parse_qs(path.query),
            "body": body.decode("latin-1"),
            "content_type": self.headers.get("Content-Type"),
            "api_key": self.headers.get("Backlog-API-Key"),
        }).encode()
        self.send_response(status)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(payload)))
        self.end_headers()
        self.wfile.write(payload)

    do_GET = do_POST = do_PATCH = do_DELETE = _reply


class TestHttpClientIntegration(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.server = ThreadingHTTPServer(("127.0.0.1", 0), _Handler)
        cls.thread = threading.Thread(target=cls.server.serve_forever, daemon=True)
        cls.thread.start()
        cls.base = "http://127.0.0.1:{}".format(cls.server.server_address[1])
        # Do not send localhost traffic through any proxy configured in the environment.
        cls.env = mock.patch.dict("os.environ", {"no_proxy": "127.0.0.1", "NO_PROXY": "127.0.0.1"})
        cls.env.start()
        _http._opener = None

    @classmethod
    def tearDownClass(cls):
        cls.server.shutdown()
        cls.server.server_close()
        cls.env.stop()
        _http._opener = None

    def test_get_with_query_and_headers(self):
        resp = _http.request("GET", self.base + "/api", params={"a": 1, "b[]": [1, 2], "skip": None},
                             headers={"Backlog-API-Key": "key"}, timeout=5)

        self.assertEqual(200, resp.status_code)
        self.assertTrue(resp.ok)
        data = resp.json()
        self.assertEqual("GET", data["method"])
        self.assertEqual({"a": ["1"], "b[]": ["1", "2"]}, data["query"])
        self.assertEqual("key", data["api_key"])
        self.assertEqual("", data["body"])

    def test_form_body_for_post_patch_delete(self):
        for method in ["POST", "PATCH", "DELETE"]:
            with self.subTest(method=method):
                resp = _http.request(method, self.base + "/api", data={"name": "n", "flag": True, "ids[]": [1, 2]}, timeout=5)
                data = resp.json()
                self.assertEqual(method, data["method"])
                self.assertEqual("application/x-www-form-urlencoded", data["content_type"])
                self.assertEqual({"name": ["n"], "flag": ["True"], "ids[]": ["1", "2"]}, parse_qs(data["body"]))

    def test_multipart_body(self):
        resp = _http.request("POST", self.base + "/api", files={"file": ("a.txt", b"hello", "text/plain")}, timeout=5)
        data = resp.json()
        self.assertTrue(data["content_type"].startswith("multipart/form-data; boundary="))
        self.assertIn('Content-Disposition: form-data; name="file"; filename="a.txt"', data["body"])
        self.assertIn("Content-Type: text/plain\r\n\r\nhello\r\n", data["body"])

    def test_error_status_returns_response(self):
        resp = _http.request("GET", self.base + "/api?status=404", timeout=5)
        self.assertEqual(404, resp.status_code)
        self.assertFalse(resp.ok)
        self.assertEqual("/api", resp.json()["path"])

    def test_redirect_is_not_followed(self):
        resp = _http.request("GET", self.base + "/redirect", headers={"Backlog-API-Key": "key"}, timeout=5)
        self.assertEqual(302, resp.status_code)

    def test_connection_error(self):
        with self.assertRaises(OSError):
            _http.request("GET", "http://127.0.0.1:1/unreachable", timeout=5)


class TestSSLContext(unittest.TestCase):
    def test_verifies_certificates(self):
        context = _http._ssl_context()
        self.assertTrue(context.check_hostname)
        self.assertEqual(ssl.CERT_REQUIRED, context.verify_mode)

    def test_loads_requests_ca_bundle(self):
        with mock.patch.dict("os.environ", {"REQUESTS_CA_BUNDLE": "/nonexistent/ca.pem", "CURL_CA_BUNDLE": ""}):
            with self.assertRaises(OSError):
                _http._ssl_context()


class TestResponse(unittest.TestCase):
    def test_text_uses_charset(self):
        resp = _http.Response(200, {"Content-Type": "text/plain; charset=shift_jis"}, "テスト".encode("shift_jis"), "u")
        self.assertEqual("テスト", resp.text)

    def test_text_defaults_to_utf8(self):
        resp = _http.Response(200, {}, "テスト".encode(), "u")
        self.assertEqual("テスト", resp.text)

    def test_json(self):
        resp = _http.Response(200, {"Content-Type": "application/json"}, b'{"a": 1}', "u")
        self.assertEqual({"a": 1}, resp.json())


class TestBacklogAPITransport(unittest.TestCase):
    def setUp(self):
        self.api = BacklogAPI("space", "api_key")

    def test_unsupported_kwargs(self):
        with self.assertRaises(TypeError) as cm:
            self.api.invoke_method("GET", "users", verify=False)
        self.assertIn("verify", str(cm.exception))

    @fake_http.activate
    def test_connection_error_is_wrapped(self):
        # Nothing registered: the fake raises URLError like a failed connection.
        with self.assertRaises(BacklogConnectionError) as cm:
            self.api.invoke_method("GET", "users")
        self.assertIsInstance(cm.exception, BacklogError)
        self.assertNotIn("api_key", str(cm.exception))

    @fake_http.activate
    def test_non_2xx_raises_backlog_error(self):
        fake_http.add(fake_http.GET, API_ENDPOINT.format(space="space", uri="users"), body='{"errors": []}', status=401)
        with self.assertRaises(BacklogError) as cm:
            self.api.invoke_method("GET", "users")
        self.assertIn("401", str(cm.exception))

    @fake_http.activate
    def test_get_does_not_send_body(self):
        fake_http.add(fake_http.GET, API_ENDPOINT.format(space="space", uri="users"), body="[]")
        self.api.invoke_method("GET", "users", request_param={"x": 1})
        self.assertEqual(b"", fake_http.last_request().body)


if __name__ == "__main__":
    unittest.main()
