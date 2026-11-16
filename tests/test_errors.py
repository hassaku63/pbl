# coding: utf-8
"""
Tests for the exceptions raised on error responses.
"""

import json
import unittest

from backlog import oauth
from backlog.base import (
    BacklogAPI,
    BacklogAPIError,
    BacklogBadRequestError,
    BacklogError,
    BacklogErrorCode,
    BacklogForbiddenError,
    BacklogNotFoundError,
    BacklogRateLimitError,
    BacklogServerError,
    BacklogUnauthorizedError,
)
from tests import fake_http

URL = "https://space.backlog.jp/api/v2/projects/TEST"


def _body(message, code):
    return json.dumps({"errors": [{"message": message, "code": code, "moreInfo": ""}]})


class TestErrorClasses(unittest.TestCase):
    def setUp(self):
        self.api = BacklogAPI("space", "key")

    @fake_http.activate
    def test_status_codes(self):
        cases = [
            (400, BacklogBadRequestError, 7),
            (401, BacklogUnauthorizedError, 11),
            (403, BacklogForbiddenError, 5),
            (404, BacklogNotFoundError, 6),
            (429, BacklogRateLimitError, 13),
            (500, BacklogServerError, 1),
            (503, BacklogServerError, 1),
            (409, BacklogAPIError, 7),
        ]
        for status, cls, code in cases:
            with self.subTest(status=status):
                fake_http.add(fake_http.GET, URL, status=status, json_body=json.loads(_body("Oops.", code)))

                with self.assertRaises(cls) as cm:
                    self.api.project.get("TEST")

                error = cm.exception
                self.assertIs(type(error), cls)
                self.assertIsInstance(error, BacklogAPIError)
                self.assertIsInstance(error, BacklogError)
                self.assertEqual(status, error.status_code)
                self.assertEqual(BacklogErrorCode(code), error.code)
                self.assertEqual("Oops.", error.error_message)
                self.assertEqual([{"message": "Oops.", "code": code, "moreInfo": ""}], error.errors)
                self.assertEqual(status, error.response.status_code)

    @fake_http.activate
    def test_message_keeps_the_historical_format(self):
        body = _body("No project.", 6)
        fake_http.add(fake_http.GET, URL, status=404, body=body, content_type="application/json")

        with self.assertRaises(BacklogNotFoundError) as cm:
            self.api.project.get("TEST")

        self.assertEqual("Http response 404: " + body, str(cm.exception))
        self.assertIs(BacklogErrorCode.NO_RESOURCE_ERROR, cm.exception.code)

    @fake_http.activate
    def test_body_without_errors(self):
        for body in ["", "<html>Bad gateway</html>", '{"error": "x"}', '{"errors": "x"}', "[1, 2]"]:
            with self.subTest(body=body):
                fake_http.add(fake_http.GET, URL, status=502, body=body)

                with self.assertRaises(BacklogServerError) as cm:
                    self.api.project.get("TEST")

                self.assertEqual([], cm.exception.errors)
                self.assertIsNone(cm.exception.code)
                self.assertIsNone(cm.exception.error_message)

    @fake_http.activate
    def test_unknown_error_code_is_kept_as_is(self):
        fake_http.add(fake_http.GET, URL, status=400, body=_body("New.", 99))

        with self.assertRaises(BacklogBadRequestError) as cm:
            self.api.project.get("TEST")

        self.assertEqual(99, cm.exception.code)

    @fake_http.activate
    def test_oauth_token_errors(self):
        fake_http.add(fake_http.POST, "https://space.backlog.jp/api/v2/oauth2/token", body='{"error":"invalid_grant"}', status=400)

        with self.assertRaises(BacklogBadRequestError) as cm:
            oauth.refresh_access_token("space", "cid", "secret", "R")

        self.assertEqual(400, cm.exception.status_code)
        self.assertEqual([], cm.exception.errors)

    def test_old_import_paths_still_work(self):
        from backlog import base, errors
        for name in ("BacklogError", "BacklogConnectionError", "BacklogRateLimitError"):
            with self.subTest(name=name):
                self.assertIs(getattr(errors, name), getattr(base, name))


if __name__ == "__main__":
    unittest.main()
