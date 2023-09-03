import unittest
import json
import httpretty
from backlog.base import BacklogAPI

API_ENDPOINT = "https://{space}.backlog.jp/api/v2/{path}"


class TestCategory(unittest.TestCase):
    def setUp(self) -> None:
        self.api = BacklogAPI("space", "api_key")
        self.space = "space"
        self.api_key = "api_key"
        self.project = "test-project"

    @httpretty.activate
    def test_list(self):
        expects = [
            {
                "id": 100,
                "projectId": 1,
                "name": "test-category",
                "displayOrder": 1
            },
        ]
        path = f"projects/{self.project}/categories"
        httpretty.register_uri(
            httpretty.GET,
            API_ENDPOINT.format(space=self.space, path=path),
            body=json.dumps(expects),
            content_type="application/json"
        )

        resp = self.api.category.list(self.project)
        self.assertEqual(expects, resp)

    @httpretty.activate
    def test_add(self):
        category = "test-category"
        expects = {
            "id": 100,
            "projectId": 1,
            "name": category,
            "displayOrder": 1
        }
        path = f"projects/{self.project}/categories"
        httpretty.register_uri(
            httpretty.POST,
            API_ENDPOINT.format(space=self.space, path=path),
            body=json.dumps(expects),
            content_type="application/json"
        )

        resp = self.api.category.add(self.project, category)
        self.assertEqual(expects, resp)

    @httpretty.activate
    def test_update(self):
        category_id = 100
        category = "updated-category"
        expects = {
            "id": category_id,
            "projectId": 1,
            "name": category,
            "displayOrder": 1
        }
        path = f"projects/{self.project}/categories/{category_id}"
        httpretty.register_uri(
            httpretty.PATCH,
            API_ENDPOINT.format(space=self.space, path=path),
            body=json.dumps(expects),
            content_type="application/json"
        )

        resp = self.api.category.update(self.project, category_id, category)
        self.assertEqual(expects, resp)

    @httpretty.activate
    def test_delete(self):
        category_id = 100
        category = "deleted-category"
        expects = {
            "id": category_id,
            "projectId": 1,
            "name": category,
            "displayOrder": 1
        }
        path = f"projects/{self.project}/categories/{category_id}"
        httpretty.register_uri(
            httpretty.DELETE,
            API_ENDPOINT.format(space=self.space, path=path),
            body=json.dumps(expects),
            content_type="application/json"
        )

        resp = self.api.category.delete(self.project, category_id)
        self.assertEqual(expects, resp)
