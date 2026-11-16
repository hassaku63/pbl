# coding: utf-8
"""
Tests for the recently viewed issues, projects and wiki pages of the user that owns the API key.
"""

import json
import unittest
from urllib.parse import parse_qs

from backlog.base import BacklogAPI
from tests import fake_http

API_ENDPOINT = "https://{space}.backlog.jp/api/v2/{uri}"


class TestRecentlyViewed(unittest.TestCase):
    def setUp(self):
        self.space = "space"
        self.api = BacklogAPI(self.space, "api_key")

    @fake_http.activate
    def test_requests(self):
        u = self.api.user
        cases = [
            ("list issues", lambda: u.list_recently_viewed_issues(order="asc", offset=10, count=5),
             "GET", "users/myself/recentlyViewedIssues", {"order": ["asc"], "offset": ["10"], "count": ["5"]}, {}),
            ("list issues (defaults)", lambda: u.list_recently_viewed_issues(),
             "GET", "users/myself/recentlyViewedIssues", {}, {}),
            ("add issue", lambda: u.add_recently_viewed_issue("TEST-1"),
             "POST", "users/myself/recentlyViewedIssues", {}, {"issueIdOrKey": ["TEST-1"]}),
            ("list projects", lambda: u.list_recently_viewed_projects(count=3),
             "GET", "users/myself/recentlyViewedProjects", {"count": ["3"]}, {}),
            ("list wikis", lambda: u.list_recently_viewed_wikis(offset=1),
             "GET", "users/myself/recentlyViewedWikis", {"offset": ["1"]}, {}),
            ("add wiki", lambda: u.add_recently_viewed_wiki(7),
             "POST", "users/myself/recentlyViewedWikis", {}, {"wikiId": ["7"]}),
        ]
        for name, call, method, uri, query, form in cases:
            with self.subTest(name):
                fake_http.add(method, API_ENDPOINT.format(space=self.space, uri=uri), body=json.dumps({"called": name}))

                result = call()

                req = fake_http.last_request()
                self.assertEqual(method, req.method)
                self.assertEqual("/api/v2/" + uri, req.path.split("?")[0])
                self.assertEqual(query, req.querystring)
                self.assertEqual(form, parse_qs(req.body.decode()))
                self.assertEqual({"called": name}, result)


if __name__ == "__main__":
    unittest.main()
