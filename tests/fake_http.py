# coding: utf-8
"""
A tiny HTTP mock for the tests, without third-party dependencies.

It replaces ``backlog._http._open``, the function that actually sends a request, so everything
above it (URL, query string, form and multipart encoding, headers) is exercised for real.

The API mirrors the parts of the ``responses`` library the tests use::

    @fake_http.activate
    def test_something(self):
        fake_http.add(fake_http.GET, "https://space.backlog.jp/api/v2/users", body="[]")
        ...
        req = fake_http.last_request()
"""

import functools
import json
import urllib.error
from email.message import Message
from unittest import mock
from urllib.parse import parse_qs, urlsplit

GET = "GET"
POST = "POST"
PATCH = "PATCH"
DELETE = "DELETE"
PUT = "PUT"

_registry = []
calls = []


def _strip_query(url):
    parts = urlsplit(url)
    return "{}://{}{}".format(parts.scheme, parts.netloc, parts.path)


def add(method, url, body="", status=200, content_type="text/plain", headers=None, json_body=None):
    """
    Register a response. When several responses match a request, the most recently registered
    one is used. The query string of requests is ignored when matching.
    """
    if json_body is not None:
        body = json.dumps(json_body)
        content_type = "application/json"
    if isinstance(body, str):
        body = body.encode()
    _headers = Message()
    _headers["Content-Type"] = content_type
    for k, v in (headers or {}).items():
        _headers[k] = v
    _registry.append((method.upper(), _strip_query(url), status, _headers, body))


def _fake_open(req, timeout):
    recorded = RecordedRequest(req, timeout)
    calls.append(recorded)
    matches = [r for r in _registry if r[0] == recorded.method and r[1] == _strip_query(recorded.url)]
    if not matches:
        raise urllib.error.URLError("fake_http: no response registered for {} {}".format(recorded.method, recorded.url))
    _, _, status, headers, body = matches[-1]
    return status, headers, body, recorded.url


def activate(func):
    """
    Decorator that enables the fake for the duration of a test.
    """
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        _registry.clear()
        calls.clear()
        with mock.patch("backlog._http._open", _fake_open):
            try:
                return func(*args, **kwargs)
            finally:
                _registry.clear()
                calls.clear()
    return wrapper


class RecordedRequest(object):
    """
    A request captured by the fake, with convenient accessors for assertions.
    """

    def __init__(self, req, timeout):
        parts = urlsplit(req.full_url)
        self.url = req.full_url
        self.method = req.get_method()
        self.host = parts.hostname
        self.path = parts.path + ("?" + parts.query if parts.query else "")
        self.querystring = parse_qs(parts.query)
        self.timeout = timeout
        self.headers = Message()  # case-insensitive lookup
        for k, v in req.header_items():
            self.headers[k] = v
        self.body = req.data or b""


def last_request():
    """
    Return the last request sent while the fake is active.
    """
    return calls[-1]
