# coding: utf-8
"""
Checks whether the endpoints behind User.add(), User.update() and User.delete() still exist.

They are no longer listed in the official API documentation. The probes never create, change or
delete a user: they send requests that cannot succeed (no parameters, or a nonexistent user ID),
and compare the error with the error for a path that does not exist at all.
"""

import json
import unittest

from tests.e2e import assertions as check
from tests.e2e.support import client, requires_space

UNKNOWN_PATH = "python-backlog-e2e-no-such-api"
NONEXISTENT_USER_ID = 0


@requires_space
class TestUserEndpointsExist(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.api = client()

    def _signature(self, method, uri):
        """
        Send a raw request and return (status, error code, error message) without raising.
        """
        resp = self.api.raw_request(method, uri)
        try:
            error = json.loads(resp.text)["errors"][0]
            return resp.status_code, error.get("code"), error.get("message")
        except (ValueError, KeyError, IndexError, TypeError):
            return resp.status_code, None, resp.text[:200]

    def _assert_exists(self, method, uri):
        unknown = self._signature(method, UNKNOWN_PATH)
        probe = self._signature(method, uri)
        # Only status codes and Backlog error codes are reported, never response bodies.
        check.is_true(
            unknown != probe,
            "{} {} responds like a nonexistent API (status {}, error code {})".format(method, uri, probe[0], probe[1]),
        )

    def test_method_can_tell_existing_endpoints_apart(self):
        # A documented endpoint must not look like an unknown path; otherwise the probes below prove nothing.
        self._assert_exists("GET", "users/{}".format(NONEXISTENT_USER_ID))

    def test_add_user_endpoint(self):
        self._assert_exists("POST", "users")

    def test_update_user_endpoint(self):
        self._assert_exists("PATCH", "users/{}".format(NONEXISTENT_USER_ID))

    def test_delete_user_endpoint(self):
        self._assert_exists("DELETE", "users/{}".format(NONEXISTENT_USER_ID))
