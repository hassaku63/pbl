# coding: utf-8
"""
Tests for updating custom fields and the items of list type custom fields.
"""

import json
import unittest
from urllib.parse import parse_qs

from backlog.base import BacklogAPI
from tests import fake_http

API_ENDPOINT = "https://{space}.backlog.jp/api/v2/{uri}"


class TestCustomFieldUpdate(unittest.TestCase):
    def setUp(self):
        self.space = "space"
        self.api = BacklogAPI(self.space, "api_key")

    @fake_http.activate
    def test_requests(self):
        c = self.api.custom_field
        cases = [
            ("update", lambda: c.update("TEST", 5, name="Severity", applicableIssueTypes=[1, 2], required=True),
             "PATCH", "projects/TEST/customFields/5",
             {"name": ["Severity"], "applicableIssueTypes[]": ["1", "2"], "required": ["true"]}),
            ("update (list field)", lambda: c.update("TEST", 5, items=["a", "b"], allowAddItem=False),
             "PATCH", "projects/TEST/customFields/5", {"items[]": ["a", "b"], "allowAddItem": ["false"]}),
            ("update (number field)", lambda: c.update(1, 6, min=0, max=10, unit="pt"),
             "PATCH", "projects/1/customFields/6", {"min": ["0"], "max": ["10"], "unit": ["pt"]}),
            ("add_list_item", lambda: c.add_list_item("TEST", 5, "High"),
             "POST", "projects/TEST/customFields/5/items", {"name": ["High"]}),
            ("update_list_item", lambda: c.update_list_item("TEST", 5, 9, "Highest"),
             "PATCH", "projects/TEST/customFields/5/items/9", {"name": ["Highest"]}),
            ("delete_list_item", lambda: c.delete_list_item("TEST", 5, 9),
             "DELETE", "projects/TEST/customFields/5/items/9", {}),
        ]
        for name, call, method, uri, form in cases:
            with self.subTest(name):
                fake_http.add(method, API_ENDPOINT.format(space=self.space, uri=uri), body=json.dumps({"called": name}))

                result = call()

                req = fake_http.last_request()
                self.assertEqual(method, req.method)
                self.assertEqual("/api/v2/" + uri, req.path.split("?")[0])
                self.assertEqual(form, parse_qs(req.body.decode()))
                self.assertEqual({"called": name}, result)


if __name__ == "__main__":
    unittest.main()
