# coding: utf-8
"""
Tests that assert what is actually sent to the Backlog API (method, query string and body),
not only how responses are parsed.
"""

import json
import os
import tempfile
import unittest
from urllib.parse import parse_qs

from tests import fake_http


from backlog.base import BacklogAPI

API_ENDPOINT = "https://{space}.backlog.jp/api/v2/{uri}"


def _form(req):
    return {k: v if len(v) > 1 else v[0] for k, v in parse_qs(req.body.decode()).items()}


class TestRequestParams(unittest.TestCase):
    def setUp(self):
        self.space = "space"
        self.api = BacklogAPI(self.space, "api_key")

    def _register(self, method, uri, body="{}", **kwargs):
        fake_http.add(
            method,
            API_ENDPOINT.format(space=self.space, uri=uri),
            body=body,
            content_type="application/json",
            **kwargs
        )

    @fake_http.activate
    def test_delete_sends_body(self):
        self._register(fake_http.DELETE, "projects/1/issueTypes/2")

        self.api.project.delete_issue_type(projectIdOrKey=1, id=2, substituteIssueTypeId=3)

        self.assertEqual({"substituteIssueTypeId": "3"}, _form(fake_http.last_request()))

    @fake_http.activate
    def test_wiki_delete_sends_mail_notify(self):
        self._register(fake_http.DELETE, "wikis/1")

        self.api.wiki.delete(wikiId=1, mailNotify=True)

        self.assertEqual({"mailNotify": "true"}, _form(fake_http.last_request()))

    @fake_http.activate
    def test_2xx_responses_are_success_for_delete_and_patch(self):
        for _method in [fake_http.DELETE, fake_http.PATCH]:
            with self.subTest(method=_method):
                self._register(_method, "test", status=202)
                resp = self.api.invoke_method(_method, "test")
                self.assertEqual(202, resp.status_code)

    @fake_http.activate
    def test_add_comment_sends_content_in_body(self):
        self._register(fake_http.POST, "issues/PRJ-1/comments")

        self.api.issue.add_comment("PRJ-1", "hello", notifiedUserId=10, attachmentId=20)

        req = fake_http.last_request()
        self.assertEqual({}, req.querystring)
        self.assertEqual(
            {"content": "hello", "notifiedUserId[]": "10", "attachmentId[]": "20"},
            _form(req)
        )

    @fake_http.activate
    def test_project_add_category_sends_name(self):
        self._register(fake_http.POST, "projects/1/categories")

        self.api.project.add_category(projectIdOrKey=1, name="dev")

        self.assertEqual({"name": "dev"}, _form(fake_http.last_request()))

    @fake_http.activate
    def test_project_update_category_sends_name(self):
        self._register(fake_http.PATCH, "projects/1/categories/2")

        self.api.project.update_category(projectIdOrKey=1, id=2, name="dev")

        self.assertEqual({"name": "dev"}, _form(fake_http.last_request()))

    @fake_http.activate
    def test_project_list_users_exclude_group_members(self):
        self._register(fake_http.GET, "projects/1/users", body="[]")

        for _flag, _expected in [(True, "true"), (False, "false")]:
            with self.subTest(excludeGroupMembers=_flag):
                self.api.project.list_users(1, excludeGroupMembers=_flag)
                self.assertEqual([_expected], fake_http.last_request().querystring["excludeGroupMembers"])

    @fake_http.activate
    def test_project_create_chart_enabled(self):
        self._register(fake_http.POST, "projects")

        for _kwargs in [{"chartEnabled": True}, {"chatEnabled": True}]:
            with self.subTest(**_kwargs):
                self.api.project.create(name="n", key="K", **_kwargs)
                self.assertEqual("true", _form(fake_http.last_request())["chartEnabled"])

        with self.assertRaises(ValueError):
            self.api.project.create(name="n", key="K", chartEnabled=True, chatEnabled=False)

    @fake_http.activate
    def test_user_add_sends_password(self):
        self._register(fake_http.POST, "users")

        self.api.user.add(userId="u", password="p", name="n", mailAddress="m@example.com", roleType=2)

        self.assertEqual(
            {"userId": "u", "password": "p", "name": "n", "mailAddress": "m@example.com", "roleType": "2"},
            _form(fake_http.last_request())
        )

    @fake_http.activate
    def test_user_update_sends_only_given_fields(self):
        self._register(fake_http.PATCH, "users/1")

        self.api.user.update(1, password="p")

        self.assertEqual({"password": "p"}, _form(fake_http.last_request()))

    @fake_http.activate
    def test_wiki_add_attachment_sends_attachment_id_array(self):
        self._register(fake_http.POST, "wikis/1/attachments", body="[]")

        for value, expected in [(2, ["2"]), ([2, 3], ["2", "3"])]:
            with self.subTest(attachmentId=value):
                self.api.wiki.add_attachment(wikiId=1, attachmentId=value)
                self.assertEqual({"attachmentId[]": expected}, parse_qs(fake_http.last_request().body.decode()))

    @fake_http.activate
    def test_wiki_get_attachment_name(self):
        _uri = "wikis/1/attachments/2"
        cases = [
            ("attachment;filename*=UTF-8''%E8%B3%87%E6%96%99.pdf", "資料.pdf"),
            ('attachment; filename="report.pdf"', "report.pdf"),
            (None, None),
        ]
        for _header, _expected in cases:
            with self.subTest(header=_header):
                _headers = {"Content-Disposition": _header} if _header else {}
                fake_http.add(
                    fake_http.GET,
                    API_ENDPOINT.format(space=self.space, uri=_uri),
                    body=b"data",
                    content_type="application/octet-stream",
                    headers=_headers
                )

                resp = self.api.wiki.get_attachment(wikiId=1, attachmentId=2)

                self.assertEqual(_expected, resp["name"])
                self.assertEqual(b"data", resp["data"])

    @fake_http.activate
    def test_attachment_upload_closes_file_and_sends_content_type(self):
        self._register(fake_http.POST, "space/attachment", body=json.dumps({"id": 1}))
        with tempfile.TemporaryDirectory() as d:
            _path = os.path.join(d, "a.txt")
            with open(_path, "w") as f:
                f.write("hello")

            with self.assertNoResourceWarning():
                self.api.attachment.upload(_path)

        body = fake_http.last_request().body
        self.assertIn(b'filename="a.txt"', body)
        self.assertIn(b"Content-Type: text/plain", body)

    def assertNoResourceWarning(self):
        test = self

        class _Ctx:
            def __enter__(self):
                import warnings
                import gc
                self._gc = gc
                self._cm = warnings.catch_warnings(record=True)
                self._w = self._cm.__enter__()
                warnings.simplefilter("always", ResourceWarning)
                return self

            def __exit__(self, *exc):
                self._gc.collect()
                self._cm.__exit__(*exc)
                test.assertEqual([], [w for w in self._w if issubclass(w.category, ResourceWarning)])
                return False

        return _Ctx()


if __name__ == "__main__":
    unittest.main()
