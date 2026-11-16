# coding: utf-8
"""
Shared configuration, safety guards and a throttled client for the end-to-end tests.
See tests/e2e/README.md for the guidelines.
"""

import datetime
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
# Tier A (administrator operations, personal data, external side effects): local runs only.
ADMIN = os.environ.get("BACKLOG_E2E_ADMIN") == "1"
IN_CI = bool(os.environ.get("GITHUB_ACTIONS") or os.environ.get("CI"))

if ADMIN and IN_CI:
    raise RuntimeError(
        "BACKLOG_E2E_ADMIN must not be set in CI: tier A tests (administrator operations, personal data, "
        "external side effects) run only locally. See tests/e2e/README.md."
    )

CONFIGURED = bool(SPACE and API_KEY)

# Tier R: read-only.
requires_space = unittest.skipUnless(CONFIGURED, "BACKLOG_E2E_SPACE and BACKLOG_E2E_API_KEY are not set")
requires_project = unittest.skipUnless(CONFIGURED and PROJECT_KEY, "BACKLOG_E2E_PROJECT_KEY is not set")
# Tier W: creates resources in the test project and deletes them.
requires_write = unittest.skipUnless(CONFIGURED and PROJECT_KEY and WRITE, "BACKLOG_E2E_WRITE is not 1")
# Tier A: never in CI.
requires_local_admin = unittest.skipUnless(
    CONFIGURED and ADMIN and not IN_CI, "tier A: set BACKLOG_E2E_ADMIN=1 and run locally (never in CI)"
)

# Every resource a test creates is named with this prefix, so leftovers can be found and deleted.
PREFIX = "pbl-e2e-"
RUN_ID = os.environ.get("GITHUB_RUN_ID") or datetime.datetime.now(datetime.timezone.utc).strftime("%Y%m%d%H%M%S")
# Leftovers older than this are deleted by the cleanup tests (younger ones may belong to a run in progress).
LEFTOVER_AGE = datetime.timedelta(hours=1)


def resource_name(label):
    """
    Name for a resource created by a test, e.g. "pbl-e2e-123456-issue".
    """
    return "{}{}-{}".format(PREFIX, RUN_ID, label)


def is_previous_run(name):
    """
    Whether a resource name was created by another (earlier) run, for resources without a creation time.
    Runs never overlap in CI (the workflow uses a concurrency group).
    """
    return isinstance(name, str) and name.startswith(PREFIX) and not name.startswith("{}{}-".format(PREFIX, RUN_ID))


def is_leftover(name, created, now=None):
    """
    Whether a resource with this name and creation time ("2026-11-15T00:00:00Z") is an old e2e leftover.
    """
    if not isinstance(name, str) or not name.startswith(PREFIX) or not created:
        return False
    created_at = datetime.datetime.strptime(created, "%Y-%m-%dT%H:%M:%SZ").replace(tzinfo=datetime.timezone.utc)
    now = now or datetime.datetime.now(datetime.timezone.utc)
    return now - created_at > LEFTOVER_AGE


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
