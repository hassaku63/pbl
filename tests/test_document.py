# coding: utf-8
"""
Tests for the document resource.
"""

import json
import unittest
from urllib.parse import parse_qs

from backlog.base import BacklogAPI
from tests import fake_http

API_ENDPOINT = "https://{space}.backlog.jp/api/v2/{uri}"
DOC = "019d46599c2d7e19adfa562d5b9019a6"


class TestDocument(unittest.TestCase):
    def setUp(self):
        self.space = "space"
        self.api = BacklogAPI(self.space, "api_key")

    @fake_http.activate
    def test_requests(self):
        d = self.api.document
        cases = [
            ("list", lambda: d.list(projectId=[1, 2], keyword="spec", sort="updated", count=5),
             "GET", "documents", {"offset": ["0"], "projectId[]": ["1", "2"], "keyword": ["spec"], "sort": ["updated"], "count": ["5"]}, {}),
            ("list (offset, single project)", lambda: d.list(offset=20, projectId=1),
             "GET", "documents", {"offset": ["20"], "projectId[]": ["1"]}, {}),
            ("count", lambda: d.count("PRJ"), "GET", "documents/count", {"projectIdOrKey": ["PRJ"]}, {}),
            ("tree", lambda: d.tree("PRJ"), "GET", "documents/tree", {"projectIdOrKey": ["PRJ"]}, {}),
            ("get", lambda: d.get(DOC), "GET", "documents/" + DOC, {}, {}),
            ("add", lambda: d.add(1, title="Spec", content="# Spec", emoji="📄", parentId="p1", addLast=True),
             "POST", "documents", {},
             {"projectId": ["1"], "title": ["Spec"], "content": ["# Spec"], "emoji": ["📄"], "parentId": ["p1"], "addLast": ["true"]}),
            ("add (minimal)", lambda: d.add(1), "POST", "documents", {}, {"projectId": ["1"]}),
            ("delete", lambda: d.delete(DOC), "DELETE", "documents/" + DOC, {}, {}),
            ("list_comments", lambda: d.list_comments(DOC), "GET", "documents/{}/comments".format(DOC), {}, {}),
            ("add_tags", lambda: d.add_tags(DOC, ["a", "b"]), "POST", "documents/{}/tags".format(DOC), {}, {"tagNames[]": ["a", "b"]}),
            ("remove_tags", lambda: d.remove_tags(DOC, "a"), "DELETE", "documents/{}/tags".format(DOC), {}, {"tagNames[]": ["a"]}),
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

    @fake_http.activate
    def test_get_attachment(self):
        fake_http.add(
            fake_http.GET,
            API_ENDPOINT.format(space=self.space, uri="documents/{}/attachments/5".format(DOC)),
            body=b"\x89PNG",
            content_type="image/png",
            headers={"Content-Disposition": 'attachment; filename="diagram.png"'},
        )

        self.assertEqual({"id": 5, "name": "diagram.png", "data": b"\x89PNG"}, self.api.document.get_attachment(DOC, 5))


if __name__ == "__main__":
    unittest.main()
