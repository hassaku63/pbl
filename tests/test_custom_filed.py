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
                "id": 1,
                "projectId": 5,
                "typeId": 6,
                "name": "custom",
                "description": "",
                "required": False,
                "applicableIssueTypes": [],
                "allowAddItem": False,
                "items": [
                    {
                        "id": 1,
                        "name": "Windows 8",
                        "displayOrder": 0
                    },
                ]
            },
            {
                "id": 2,
                "typeId": 1,
                "name": "Attribute for Bug",
                "description": "",
                "required": False,
                "applicableIssueTypes": [1]
            },
        ]
        path = f"projects/{self.project}/customFields"
        httpretty.register_uri(
            httpretty.GET,
            API_ENDPOINT.format(space=self.space, path=path),
            body=json.dumps(expects),
            content_type="application/json"
        )

        resp = self.api.custom_field.list(self.project)
        self.assertEqual(expects, resp)

    @httpretty.activate
    def test_add_text_custom_field(self):
        project_key = "test-project"
        custom_field_name = "test-text-field"
        expects = {
            "id": 2,
            "projectId": 5,
            "typeId": 1,
            "name": custom_field_name,
            "description": "",
            "required": False,
            "applicableIssueTypes": [1],
        }
        path = f"projects/{self.project}/customFields"
        httpretty.register_uri(
            httpretty.POST,
            API_ENDPOINT.format(space=self.space, path=path),
            body=json.dumps(expects),
            content_type="application/json"
        )

        resp = self.api.custom_field.add_text_custom_field(
            projectIdOrKey=project_key,
            name=custom_field_name,
        )

        self.assertEqual(expects, resp)

    @httpretty.activate
    def test_add_sentence_custom_field(self):
        project_key = "test-project"
        custom_field_name = "test-sentence-field"
        expects = {
            "id": 2,
            "projectId": 5,
            "typeId": 1,
            "name": custom_field_name,
            "description": "",
            "required": False,
            "applicableIssueTypes": [1],
        }
        path = f"projects/{self.project}/customFields"
        httpretty.register_uri(
            httpretty.POST,
            API_ENDPOINT.format(space=self.space, path=path),
            body=json.dumps(expects),
            content_type="application/json"
        )

        resp = self.api.custom_field.add_sentence_custom_field(
            projectIdOrKey=project_key,
            name=custom_field_name,
        )

        self.assertEqual(expects, resp)

    @httpretty.activate
    def test_add_number_custom_field(self):
        project_key = "test-project"
        custom_field_name = "test-number-field"
        expects = {
            "id": 2,
            "projectId": 5,
            "typeId": 1,
            "name": custom_field_name,
            "description": "",
            "required": False,
            "applicableIssueTypes": [1],
        }
        path = f"projects/{self.project}/customFields"
        httpretty.register_uri(
            httpretty.POST,
            API_ENDPOINT.format(space=self.space, path=path),
            body=json.dumps(expects),
            content_type="application/json"
        )

        resp = self.api.custom_field.add_number_custom_field(
            projectIdOrKey=project_key,
            name=custom_field_name,
        )

        self.assertEqual(expects, resp)

    @httpretty.activate
    def test_add_date_custom_field(self):
        project_key = "test-project"
        custom_field_name = "test-date-field"
        expects = {
            "id": 2,
            "projectId": 5,
            "typeId": 1,
            "name": custom_field_name,
            "description": "",
            "required": False,
            "applicableIssueTypes": [1],
        }
        path = f"projects/{self.project}/customFields"
        httpretty.register_uri(
            httpretty.POST,
            API_ENDPOINT.format(space=self.space, path=path),
            body=json.dumps(expects),
            content_type="application/json"
        )

        resp = self.api.custom_field.add_date_custom_field(
            projectIdOrKey=project_key,
            name=custom_field_name,
        )

        self.assertEqual(expects, resp)

    @httpretty.activate
    def test_add_single_list_custom_field(self):
        project_key = "test-project"
        custom_field_name = "test-single-list-field"
        expects = {
            "id": 2,
            "projectId": 5,
            "typeId": 1,
            "name": custom_field_name,
            "description": "",
            "required": False,
            "applicableIssueTypes": [1],
        }
        path = f"projects/{self.project}/customFields"
        httpretty.register_uri(
            httpretty.POST,
            API_ENDPOINT.format(space=self.space, path=path),
            body=json.dumps(expects),
            content_type="application/json"
        )

        resp = self.api.custom_field.add_single_list_custom_field(
            projectIdOrKey=project_key,
            name=custom_field_name,
        )

        self.assertEqual(expects, resp)

    @httpretty.activate
    def test_add_multiple_list_custom_field(self):
        project_key = "test-project"
        custom_field_name = "test-multiple-list-field"
        expects = {
            "id": 2,
            "projectId": 5,
            "typeId": 1,
            "name": custom_field_name,
            "description": "",
            "required": False,
            "applicableIssueTypes": [1],
        }
        path = f"projects/{self.project}/customFields"
        httpretty.register_uri(
            httpretty.POST,
            API_ENDPOINT.format(space=self.space, path=path),
            body=json.dumps(expects),
            content_type="application/json"
        )

        resp = self.api.custom_field.add_multiple_list_custom_field(
            projectIdOrKey=project_key,
            name=custom_field_name,
        )

        self.assertEqual(expects, resp)

    @httpretty.activate
    def test_add_checkbox_custom_field(self):
        project_key = "test-project"
        custom_field_name = "test-checkbox-field"
        expects = {
            "id": 2,
            "projectId": 5,
            "typeId": 1,
            "name": custom_field_name,
            "description": "",
            "required": False,
            "applicableIssueTypes": [1],
        }
        path = f"projects/{self.project}/customFields"
        httpretty.register_uri(
            httpretty.POST,
            API_ENDPOINT.format(space=self.space, path=path),
            body=json.dumps(expects),
            content_type="application/json"
        )

        resp = self.api.custom_field.add_checkbox_custom_field(
            projectIdOrKey=project_key,
            name=custom_field_name,
        )
        self.assertEqual(expects, resp)

    @httpretty.activate
    def test_add_radio_custom_field(self):
        project_key = "test-project"
        custom_field_name = "test-radio-field"
        expects = {
            "id": 2,
            "projectId": 5,
            "typeId": 1,
            "name": custom_field_name,
            "description": "",
            "required": False,
            "items": [
                {
                    "id": 1,
                    "name": "Windows 8",
                    "displayOrder": 0
                },
            ],
            "applicableIssueTypes": [1],
        }
        path = f"projects/{self.project}/customFields"
        httpretty.register_uri(
            httpretty.POST,
            API_ENDPOINT.format(space=self.space, path=path),
            body=json.dumps(expects),
            content_type="application/json"
        )

        resp = self.api.custom_field.add_radio_custom_field(
            projectIdOrKey=project_key,
            name=custom_field_name,
            items=['Windows 8'],
        )

        self.assertEqual(expects, resp)

    # @httpretty.activate
    # def test_update(self):
    #     category_id = 100
    #     category = "updated-category"
    #     expects = {
    #         "id": category_id,
    #         "projectId": 1,
    #         "name": category,
    #         "displayOrder": 1
    #     }
    #     path = f"projects/{self.project}/categories/{category_id}"
    #     httpretty.register_uri(
    #         httpretty.PATCH,
    #         API_ENDPOINT.format(space=self.space, path=path),
    #         body=json.dumps(expects),
    #         content_type="application/json"
    #     )

    #     resp = self.api.category.update(self.project, category_id, category)
    #     self.assertEqual(expects, resp)

    # @httpretty.activate
    # def test_delete(self):
    #     category_id = 100
    #     category = "deleted-category"
    #     expects = {
    #         "id": category_id,
    #         "projectId": 1,
    #         "name": category,
    #         "displayOrder": 1
    #     }
    #     path = f"projects/{self.project}/categories/{category_id}"
    #     httpretty.register_uri(
    #         httpretty.DELETE,
    #         API_ENDPOINT.format(space=self.space, path=path),
    #         body=json.dumps(expects),
    #         content_type="application/json"
    #     )

    #     resp = self.api.category.delete(self.project, category_id)
    #     self.assertEqual(expects, resp)
