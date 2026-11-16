# coding: utf-8
"""
Tests for backlog.pagination and the iter...() methods built on it.
"""

import json
import unittest

from backlog.base import BacklogAPI
from backlog.pagination import id_range, iterate_by_id, iterate_by_offset
from tests import fake_http

ITEMS = [{"id": i} for i in range(1, 251)]  # ids 1..250


def offset_api(calls):
    def fetch(*args, offset=0, count=20, **kwargs):
        calls.append(dict(kwargs, args=args, offset=offset, count=count))
        return ITEMS[offset:offset + count]
    return fetch


def id_api(calls, inclusive):
    """
    A minId/maxId list endpoint; inclusive decides whether minId/maxId include the boundary item.
    """
    def fetch(*args, minId=None, maxId=None, count=20, order="desc", **kwargs):
        calls.append(dict(kwargs, args=args, minId=minId, maxId=maxId, count=count, order=order))
        items = ITEMS
        if minId is not None:
            items = [i for i in items if (i["id"] >= minId if inclusive else i["id"] > minId)]
        if maxId is not None:
            items = [i for i in items if (i["id"] <= maxId if inclusive else i["id"] < maxId)]
        items = sorted(items, key=lambda i: i["id"], reverse=(order == "desc"))
        return items[:count]
    return fetch


class TestIterateByOffset(unittest.TestCase):
    def test_all_pages(self):
        calls = []
        result = list(iterate_by_offset(offset_api(calls), "KEY", count=100, keyword="x"))

        self.assertEqual(ITEMS, result)
        self.assertEqual([0, 100, 200], [c["offset"] for c in calls])
        self.assertTrue(all(c["count"] == 100 and c["keyword"] == "x" and c["args"] == ("KEY",) for c in calls))

    def test_exact_multiple_needs_one_empty_page(self):
        calls = []
        result = list(iterate_by_offset(offset_api(calls), count=50))
        self.assertEqual(250, len(result))
        self.assertEqual([0, 50, 100, 150, 200, 250], [c["offset"] for c in calls])

    def test_is_lazy(self):
        calls = []
        iterator = iterate_by_offset(offset_api(calls), count=100)
        self.assertEqual([], calls)
        next(iterator)
        self.assertEqual(1, len(calls))


class TestIterateById(unittest.TestCase):
    def test_desc_and_asc_with_both_boundary_semantics(self):
        for inclusive in (True, False):
            for order in ("desc", "asc"):
                with self.subTest(inclusive=inclusive, order=order):
                    calls = []
                    result = list(iterate_by_id(id_api(calls, inclusive), count=100, order=order))
                    expected = sorted(ITEMS, key=lambda i: i["id"], reverse=(order == "desc"))
                    self.assertEqual(expected, result)

    def test_range(self):
        calls = []
        result = list(iterate_by_id(id_api(calls, True), count=10, order="asc", **id_range(minId=5, maxId=30)))
        self.assertEqual(list(range(5, 31)), [i["id"] for i in result])
        self.assertTrue(all(c["maxId"] == 30 for c in calls))

    def test_invalid_order(self):
        with self.assertRaises(ValueError):
            next(iterate_by_id(id_api([], True), order="newest"))

    def test_stops_without_progress(self):
        calls = []

        def stuck(**kwargs):
            calls.append(kwargs)
            return [{"id": 7}]

        self.assertEqual([{"id": 7}], list(iterate_by_id(stuck, count=1)))
        self.assertEqual(2, len(calls))

    def test_id_range(self):
        self.assertEqual({}, id_range())
        self.assertEqual({"minId": 1}, id_range(minId=1))
        self.assertEqual({"minId": 0, "maxId": 9}, id_range(0, 9))


class TestIterMethods(unittest.TestCase):
    def setUp(self):
        self.api = BacklogAPI("space", "key")

    @fake_http.activate
    def test_issue_iter(self):
        url = "https://space.backlog.jp/api/v2/issues"
        fake_http.add_sequence(fake_http.GET, url, [
            {"body": json.dumps(ITEMS[:100])}, {"body": json.dumps(ITEMS[100:103])}])

        result = list(self.api.issue.iter(**{"projectId[]": [1], "keyword": "bug"}))

        self.assertEqual(ITEMS[:103], result)
        queries = [c.querystring for c in fake_http.calls]
        self.assertEqual([["0"], ["100"]], [q["offset"] for q in queries])
        self.assertTrue(all(q["count"] == ["100"] and q["projectId[]"] == ["1"] and q["keyword"] == ["bug"] for q in queries))

    @fake_http.activate
    def test_activity_iter(self):
        url = "https://space.backlog.jp/api/v2/space/activities"
        newest = sorted(ITEMS, key=lambda i: i["id"], reverse=True)
        fake_http.add_sequence(fake_http.GET, url, [
            {"body": json.dumps(newest[:100])}, {"body": json.dumps(newest[99:150])}])

        result = list(self.api.activity.iter(activityTypeId=[1, 2]))

        self.assertEqual(newest[:150], result)
        queries = [c.querystring for c in fake_http.calls]
        self.assertNotIn("maxId", queries[0])
        self.assertEqual(["151"], queries[1]["maxId"])
        self.assertTrue(all(q["order"] == ["desc"] and q["activityTypeId[]"] == ["1", "2"] for q in queries))

    @fake_http.activate
    def test_other_iter_methods_request_the_right_endpoint(self):
        cases = [
            (lambda: self.api.issue.iter_comments("TEST-1"), "issues/TEST-1/comments", {"order": ["asc"]}),
            (lambda: self.api.activity.iter_project("TEST"), "projects/TEST/activities", {"order": ["desc"]}),
            (lambda: self.api.activity.iter_user(3), "users/3/activities", {"order": ["desc"]}),
            (lambda: self.api.notification.iter(senderId=4), "notifications", {"senderId": ["4"]}),
            (lambda: self.api.star.iter_received(3, minId=10), "users/3/stars", {"minId": ["10"]}),
            (lambda: self.api.wiki.iter_history(5), "wikis/5/history", {"order": ["desc"]}),
            (lambda: self.api.document.iter(projectId=[1]), "documents", {"offset": ["0"], "projectId[]": ["1"]}),
            (lambda: self.api.git.iter_pull_requests("TEST", "repo"), "projects/TEST/git/repositories/repo/pullRequests",
             {"offset": ["0"]}),
            (lambda: self.api.watching.iter(3, resourceAlreadyRead=False), "users/3/watchings",
             {"offset": ["0"], "resourceAlreadyRead": ["false"]}),
        ]
        for call, uri, expected in cases:
            with self.subTest(uri=uri):
                fake_http.add(fake_http.GET, "https://space.backlog.jp/api/v2/" + uri, body="[]")

                self.assertEqual([], list(call()))

                req = fake_http.last_request()
                self.assertEqual("/api/v2/" + uri, req.path.split("?")[0])
                self.assertEqual(["100"], req.querystring["count"])
                for key, value in expected.items():
                    self.assertEqual(value, req.querystring[key], key)


if __name__ == "__main__":
    unittest.main()
