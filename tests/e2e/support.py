# coding: utf-8
"""
Shared configuration and a throttled client for the end-to-end tests.
"""

import os
import time
import unittest

from backlog import _http
from backlog.base import BacklogAPI

SPACE = os.environ.get("BACKLOG_E2E_SPACE")
API_KEY = os.environ.get("BACKLOG_E2E_API_KEY")
DOMAIN = os.environ.get("BACKLOG_E2E_DOMAIN") or "backlog.jp"
PROJECT_KEY = os.environ.get("BACKLOG_E2E_PROJECT_KEY")
WRITE = os.environ.get("BACKLOG_E2E_WRITE") == "1"
INTERVAL = float(os.environ.get("BACKLOG_E2E_INTERVAL") or "1.0")

CONFIGURED = bool(SPACE and API_KEY)

requires_space = unittest.skipUnless(CONFIGURED, "BACKLOG_E2E_SPACE and BACKLOG_E2E_API_KEY are not set")
requires_project = unittest.skipUnless(CONFIGURED and PROJECT_KEY, "BACKLOG_E2E_PROJECT_KEY is not set")
requires_write = unittest.skipUnless(CONFIGURED and PROJECT_KEY and WRITE, "BACKLOG_E2E_WRITE is not 1")


_last_request = [0.0]


def throttle():
    """
    Wait until at least INTERVAL seconds have passed since the previous request of this test run.
    """
    wait = _last_request[0] + INTERVAL - time.monotonic()
    if wait > 0:
        time.sleep(wait)


class ThrottledBacklogAPI(BacklogAPI):
    """
    BacklogAPI that waits at least INTERVAL seconds between requests, and retries on 429.
    """

    def _send(self, *args, **kwargs):
        throttle()
        try:
            return super()._send(*args, **kwargs)
        finally:
            _last_request[0] = time.monotonic()

    def raw_request(self, method, uri):
        """
        Send an authenticated request and return the response for any status code (it never raises on 4xx/5xx).
        """
        throttle()
        try:
            return _http.request(method, self.base_url + uri, headers=self._build_headers(), timeout=self.timeout)
        finally:
            _last_request[0] = time.monotonic()


def client():
    return ThrottledBacklogAPI(SPACE, API_KEY, domain=DOMAIN, rate_limit_retries=2, rate_limit_max_wait=70)
