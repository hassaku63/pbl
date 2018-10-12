# coding: utf-8

import unittest
import httpretty
import json
import tempfile
from requests import Response
from backlog.util import load_conf
from backlog.base import BacklogAPI

API_ENDPOINT = "https://{space}.backlog.jp/api/v2/{uri}"


class TestWiki(unittest.TestCase):
    def setUp(self):
        self.conf = load_conf("./conf.default.yml")["backlog"]
        self.api = BacklogAPI(self.conf["space"], self.conf["api_key"])
        self.space = self.conf["space"]
        self.api_key = self.conf["api_key"]

    @httpretty.activate
    def test_list_wiki(self):
        expects = [
            {
                "id": 112,
                "projectId": 103,
                "name": "Home",
                "tags": [
                    {
                        "id": 12,
                        "name": "議事録"
                    }
                ],
                "createdUser": {
                    "id": 1,
                    "userId": "admin",
                    "name": "admin",
                    "roleType": 1,
                    "lang": "ja",
                    "mailAddress": "eguchi@nulab.example"
                },
                "created": "2013-05-30T09:11:36Z",
                "updatedUser": {
                    "id": 1,
                    "userId": "admin",
                    "name": "admin",
                    "roleType": 1,
                    "lang": "ja",
                    "mailAddress": "eguchi@nulab.example"
                },
                "updated": "2013-05-30T09:11:36Z"
            }
        ]
        httpretty.register_uri(
            httpretty.GET,
            API_ENDPOINT.format(space=self.space ,uri="wikis"),
            body=json.dumps(expects)
        )
        wikis = self.api.wiki.list(projectIdOrKey=self.conf["default_project"])
        self.assertTrue(type(wikis) == list)

    def test_create_wiki(self):
        pass

    def test_get_wiki(self):
        pass

    def test_update_wiki(self):
        pass

    def test_delete_wiki(self):
        pass

    def test_add_attachment(self):
        pass

    @httpretty.activate
    def test_get_attachment(self):
        with tempfile.NamedTemporaryFile(delete=True) as tmp:
            # Set parameter and expects
            _wiki_id = 1234567890
            _attachment_id = 1234567890
            _uri = "wikis/{wiki_id}/attachments/{attachment_id}".format(
                wiki_id=_wiki_id,
                attachment_id=_attachment_id
            )
            _name = "test"
            _data = b"1234567890"
            tmp.file.write(_data)
            tmp.file.flush()
            tmp.file.seek(0)
            # expects = Response()
            # expects.status_code = 200
            # expects._content = tmp.file.read()
            expects = {
                "id": _attachment_id,
                "name": _name,
                "data": _data
            }

            # mock
            httpretty.register_uri(
                httpretty.GET,
                API_ENDPOINT.format(space=self.space, uri=_uri),
                # body=expects._content,
                body=tmp.file.read(),
                content_type="application/octet-stream"
            )

            # test
            resp = self.api.wiki.get_attachment(
                wikiId=_wiki_id,
                attachmentId=_attachment_id
            )

            self.assertEqual(expects, resp)

    def test_delete_attachment(self):
        pass


if __name__ == "__main__":
    unittest.main(warnings='ignore')