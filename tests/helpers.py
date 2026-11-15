# coding: utf-8
"""
Test helpers on top of the `responses` library.
"""

from urllib.parse import parse_qs, urlsplit

import responses


class RecordedRequest(object):
    """
    A request captured by `responses`, with convenient accessors for assertions.
    """

    def __init__(self, prepared_request):
        self._request = prepared_request
        _url = urlsplit(prepared_request.url)
        self.url = prepared_request.url
        self.method = prepared_request.method
        self.host = _url.hostname
        self.path = _url.path + ("?" + _url.query if _url.query else "")
        self.querystring = parse_qs(_url.query)
        self.headers = prepared_request.headers
        _body = prepared_request.body
        if _body is None:
            _body = b""
        elif isinstance(_body, str):
            _body = _body.encode()
        self.body = _body


def last_request():
    """
    Return the last request sent while `responses` is active.
    """
    return RecordedRequest(responses.calls[-1].request)
