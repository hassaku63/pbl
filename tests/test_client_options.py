# coding: utf-8
"""
Tests for BacklogAPI options: domain, OAuth access token and rate limit handling, and backlog.oauth.
"""

import io
import unittest
from unittest import mock
from urllib.parse import parse_qs, urlsplit

from backlog import oauth
from backlog.base import BacklogAPI, BacklogError, BacklogRateLimitError
from tests import fake_http


class TestDomain(unittest.TestCase):
    @fake_http.activate
    def test_domains(self):
        for domain in ["backlog.jp", "backlog.com", "backlogtool.com"]:
            with self.subTest(domain=domain):
                fake_http.add(fake_http.GET, "https://space.{}/api/v2/users".format(domain), body="[]")
                BacklogAPI("space", "key", domain=domain).user.list()
                self.assertEqual("space.{}".format(domain), fake_http.last_request().host)

    def test_default_domain(self):
        self.assertEqual("https://space.backlog.jp/api/v2/", BacklogAPI("space", "key").base_url)

    def test_invalid_domain(self):
        for domain in ["example.com", "backlog.com.evil.example", "", None]:
            with self.subTest(domain=domain):
                with self.assertRaises(ValueError):
                    BacklogAPI("space", "key", domain=domain)


class TestAccessToken(unittest.TestCase):
    @fake_http.activate
    def test_bearer_header(self):
        fake_http.add(fake_http.GET, "https://space.backlog.com/api/v2/users/myself", body="{}")
        api = BacklogAPI("space", access_token="TOKEN", domain="backlog.com")

        api.invoke_method("GET", "users/myself")

        req = fake_http.last_request()
        self.assertEqual("Bearer TOKEN", req.headers.get("Authorization"))
        self.assertIsNone(req.headers.get("Backlog-API-Key"))

    @fake_http.activate
    def test_set_access_token(self):
        fake_http.add(fake_http.GET, "https://space.backlog.jp/api/v2/users", body="[]")
        api = BacklogAPI("space", access_token="OLD")
        api.set_access_token("NEW")

        api.user.list()

        self.assertEqual("Bearer NEW", fake_http.last_request().headers.get("Authorization"))

    def test_api_key_and_access_token_are_exclusive(self):
        with self.assertRaises(ValueError):
            BacklogAPI("space", "key", access_token="TOKEN")
        with self.assertRaises(ValueError):
            BacklogAPI("space", "key").set_access_token("TOKEN")


class TestOAuth(unittest.TestCase):
    def test_authorization_url(self):
        url = oauth.authorization_url("space", "cid", "https://app.example/cb", state="xyz", domain="backlog.com")
        parts = urlsplit(url)
        self.assertEqual("https://space.backlog.com/OAuth2AccessRequest.action", "{}://{}{}".format(parts.scheme, parts.netloc, parts.path))
        self.assertEqual(
            {"response_type": ["code"], "client_id": ["cid"], "redirect_uri": ["https://app.example/cb"], "state": ["xyz"]},
            parse_qs(parts.query),
        )

    @fake_http.activate
    def test_request_access_token(self):
        fake_http.add(fake_http.POST, "https://space.backlog.jp/api/v2/oauth2/token", json_body={"access_token": "A", "refresh_token": "R"})

        token = oauth.request_access_token("space", "cid", "secret", "CODE", "https://app.example/cb")

        self.assertEqual({"access_token": "A", "refresh_token": "R"}, token)
        req = fake_http.last_request()
        self.assertEqual({
            "grant_type": ["authorization_code"], "code": ["CODE"], "redirect_uri": ["https://app.example/cb"],
            "client_id": ["cid"], "client_secret": ["secret"],
        }, parse_qs(req.body.decode()))
        self.assertNotIn("secret", req.url)

    @fake_http.activate
    def test_refresh_access_token(self):
        fake_http.add(fake_http.POST, "https://space.backlog.com/api/v2/oauth2/token", json_body={"access_token": "A2"})

        token = oauth.refresh_access_token("space", "cid", "secret", "R", domain="backlog.com")

        self.assertEqual("A2", token["access_token"])
        self.assertEqual(
            {"grant_type": ["refresh_token"], "client_id": ["cid"], "client_secret": ["secret"], "refresh_token": ["R"]},
            parse_qs(fake_http.last_request().body.decode()),
        )

    @fake_http.activate
    def test_token_error(self):
        fake_http.add(fake_http.POST, "https://space.backlog.jp/api/v2/oauth2/token", body='{"error":"invalid_grant"}', status=400)
        with self.assertRaises(BacklogError):
            oauth.refresh_access_token("space", "cid", "secret", "R")


class TestRateLimit(unittest.TestCase):
    URL = "https://space.backlog.jp/api/v2/users"

    def _limited(self, reset):
        return {"status": 429, "body": '{"errors":[]}',
                "headers": {"X-RateLimit-Limit": "600", "X-RateLimit-Remaining": "0", "X-RateLimit-Reset": str(reset)}}

    @fake_http.activate
    def test_raises_rate_limit_error_by_default(self):
        fake_http.add(fake_http.GET, self.URL, **self._limited(1000))

        with mock.patch("backlog.base.time.sleep") as sleep:
            with self.assertRaises(BacklogRateLimitError) as cm:
                BacklogAPI("space", "key").user.list()

        sleep.assert_not_called()
        self.assertIsInstance(cm.exception, BacklogError)
        self.assertEqual((600, 0, 1000), (cm.exception.limit, cm.exception.remaining, cm.exception.reset))
        self.assertEqual(1, len(fake_http.calls))

    @fake_http.activate
    def test_retries_after_reset(self):
        fake_http.add_sequence(fake_http.GET, self.URL, [self._limited(1010), {"body": "[]"}])

        with mock.patch("backlog.base.time.time", return_value=1000.0), mock.patch("backlog.base.time.sleep") as sleep:
            result = BacklogAPI("space", "key", rate_limit_retries=2).user.list()

        self.assertEqual([], result)
        sleep.assert_called_once_with(11.0)
        self.assertEqual(2, len(fake_http.calls))

    @fake_http.activate
    def test_does_not_wait_longer_than_max_wait(self):
        fake_http.add(fake_http.GET, self.URL, **self._limited(1100))

        with mock.patch("backlog.base.time.time", return_value=1000.0), mock.patch("backlog.base.time.sleep") as sleep:
            with self.assertRaises(BacklogRateLimitError):
                BacklogAPI("space", "key", rate_limit_retries=3, rate_limit_max_wait=60).user.list()

        sleep.assert_not_called()

    @fake_http.activate
    def test_gives_up_after_retries(self):
        fake_http.add(fake_http.GET, self.URL, **self._limited(1001))

        with mock.patch("backlog.base.time.time", return_value=1000.0), mock.patch("backlog.base.time.sleep") as sleep:
            with self.assertRaises(BacklogRateLimitError):
                BacklogAPI("space", "key", rate_limit_retries=2).user.list()

        self.assertEqual(2, sleep.call_count)
        self.assertEqual(3, len(fake_http.calls))

    @fake_http.activate
    def test_backoff_without_headers(self):
        fake_http.add_sequence(fake_http.GET, self.URL, [{"status": 429}, {"status": 429}, {"body": "[]"}])

        with mock.patch("backlog.base.time.sleep") as sleep:
            BacklogAPI("space", "key", rate_limit_retries=2).user.list()

        self.assertEqual([mock.call(1.0), mock.call(2.0)], sleep.call_args_list)

    @fake_http.activate
    def test_retry_resends_file_contents(self):
        url = "https://space.backlog.jp/api/v2/space/attachment"
        fake_http.add_sequence(fake_http.POST, url, [{"status": 429}, {"body": '{"id": 1}'}])
        f = io.BytesIO(b"hello")

        with mock.patch("backlog.base.time.sleep"):
            BacklogAPI("space", "key", rate_limit_retries=1).invoke_method("POST", "space/attachment", files={"file": ("a.txt", f)})

        self.assertIn(b"hello", fake_http.calls[0].body)
        self.assertIn(b"hello", fake_http.calls[1].body)

    def test_invalid_retries(self):
        with self.assertRaises(ValueError):
            BacklogAPI("space", "key", rate_limit_retries=-1)

    @fake_http.activate
    def test_get_rate_limit(self):
        fake_http.add(fake_http.GET, "https://space.backlog.jp/api/v2/rateLimit", json_body={"rateLimit": {"read": {"limit": 600}}})
        self.assertEqual({"rateLimit": {"read": {"limit": 600}}}, BacklogAPI("space", "key").get_rate_limit())


if __name__ == "__main__":
    unittest.main()
