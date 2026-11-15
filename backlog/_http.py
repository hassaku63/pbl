# coding: utf-8
"""
Minimal HTTP client built on the standard library (urllib).

python-backlog has no runtime dependencies. This module implements the small subset of HTTP
features the Backlog API needs: query strings, form-encoded and multipart bodies, custom
headers, timeouts and JSON responses.
"""

import json
import os
import ssl
import urllib.error
import urllib.parse
import urllib.request
import uuid
from email.message import Message


class Response(object):
    """
    HTTP response returned by :meth:`backlog.base.BaseAPI.invoke_method`.

    It provides the attributes of ``requests.Response`` that are commonly used with this library.
    """

    def __init__(self, status_code, headers, content, url):
        self.status_code = status_code
        self.headers = headers
        self.content = content
        self.url = url

    @property
    def ok(self):
        return 200 <= self.status_code < 400

    @property
    def encoding(self):
        _message = Message()
        _message["Content-Type"] = self.headers.get("Content-Type", "")
        return _message.get_content_charset() or "utf-8"

    @property
    def text(self):
        return self.content.decode(self.encoding, errors="replace")

    def json(self):
        return json.loads(self.text)

    def __repr__(self):
        return "<Response [{}]>".format(self.status_code)


def _items(params):
    """
    Flatten a parameter dict into (key, value) string pairs, like requests does:
    None values are skipped and list/tuple values become repeated keys.
    """
    pairs = []
    for key, value in (params or {}).items():
        values = value if isinstance(value, (list, tuple)) else [value]
        for v in values:
            if v is None:
                continue
            if isinstance(v, bytes):
                v = v.decode()
            pairs.append((str(key), str(v)))
    return pairs


def encode_query(url, params):
    pairs = _items(params)
    if not pairs:
        return url
    return url + ("&" if "?" in url else "?") + urllib.parse.urlencode(pairs)


def encode_form(data):
    pairs = _items(data)
    if not pairs:
        return None
    return urllib.parse.urlencode(pairs).encode()


def encode_multipart(data, files):
    """
    Encode form fields and files as multipart/form-data.

    :param files: dict of field name to ``(filename, fileobj_or_bytes[, content_type])``
    :return: (body, content_type)
    """
    boundary = uuid.uuid4().hex
    lines = []
    for key, value in _items(data):
        lines += [
            "--{}".format(boundary).encode(),
            'Content-Disposition: form-data; name="{}"'.format(_quote(key)).encode(),
            b"",
            value.encode(),
        ]
    for key, spec in files.items():
        filename, content = spec[0], spec[1]
        content_type = (spec[2] if len(spec) > 2 else None) or "application/octet-stream"
        if hasattr(content, "read"):
            content = content.read()
        if isinstance(content, str):
            content = content.encode()
        lines += [
            "--{}".format(boundary).encode(),
            'Content-Disposition: form-data; name="{}"; filename="{}"'.format(_quote(key), _quote(filename)).encode(),
            "Content-Type: {}".format(content_type).encode(),
            b"",
            content,
        ]
    lines += ["--{}--".format(boundary).encode(), b""]
    return b"\r\n".join(lines), "multipart/form-data; boundary={}".format(boundary)


def _quote(value):
    return str(value).replace("\\", "\\\\").replace('"', '\\"').replace("\r", "").replace("\n", "")


class _NoRedirectHandler(urllib.request.HTTPRedirectHandler):
    """
    Do not follow redirects. The Backlog API does not redirect, and following a redirect would
    forward the API key header to wherever the redirect points.
    """

    def redirect_request(self, req, fp, code, msg, headers, newurl):
        return None


def _ssl_context():
    """
    Build the TLS context.

    The system trust store is used as the standard library does (it also honors SSL_CERT_FILE and
    SSL_CERT_DIR, so CAs added to the OS, such as those of corporate proxies, keep working).
    CA bundles that requests users may rely on are added on top of it:

    - the file in REQUESTS_CA_BUNDLE or CURL_CA_BUNDLE, if set;
    - certifi's bundle, if certifi is installed (helps on systems without a usable trust store).
    """
    context = ssl.create_default_context()
    for name in ("REQUESTS_CA_BUNDLE", "CURL_CA_BUNDLE"):
        path = os.environ.get(name)
        if not path:
            continue
        if os.path.isdir(path):
            context.load_verify_locations(capath=path)
        else:
            context.load_verify_locations(cafile=path)
    try:
        import certifi
    except ImportError:
        pass
    else:
        context.load_verify_locations(cafile=certifi.where())
    return context


_opener = None


def _get_opener():
    global _opener
    if _opener is None:
        _opener = urllib.request.build_opener(
            urllib.request.HTTPSHandler(context=_ssl_context()),
            _NoRedirectHandler(),
        )
    return _opener


def _open(req, timeout):
    """
    Send the request. Returns (status, headers, body, url) for every HTTP status code.
    """
    try:
        with _get_opener().open(req, timeout=timeout) as resp:
            return resp.status, resp.headers, resp.read(), resp.url
    except urllib.error.HTTPError as e:
        with e:
            return e.code, e.headers, e.read(), e.url


def request(method, url, params=None, data=None, headers=None, files=None, timeout=None):
    """
    Send an HTTP request and return a :class:`Response`.

    Network errors raise ``OSError`` subclasses (``urllib.error.URLError``, ``TimeoutError``, ...).
    """
    _headers = dict(headers or {})
    body = None
    if files:
        body, _headers["Content-Type"] = encode_multipart(data, files)
    elif method.upper() != "GET":
        body = encode_form(data)
        if body is not None:
            _headers["Content-Type"] = "application/x-www-form-urlencoded"

    req = urllib.request.Request(encode_query(url, params), data=body, headers=_headers, method=method.upper())
    status, response_headers, content, response_url = _open(req, timeout)
    return Response(status, response_headers, content, response_url)
