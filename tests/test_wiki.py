# coding: utf-8

import unittest
import httpretty
import json
import tempfile
from uuid import uuid4
from backlog.base import BacklogAPI


API_ENDPOINT = "https://{space}.backlog.jp/api/v2/{uri}"


class TestWiki(unittest.TestCase):
    def setUp(self):
        self.space = 'space'
        self.api_key = 'api-key'
        self.api = BacklogAPI(self.space, self.api_key)
        self.default_project = "default_project_key"

    @httpretty.activate
    def test_list_wiki(self):
        _uri = "wikis"
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
            API_ENDPOINT.format(space=self.space, uri=_uri),
            body=json.dumps(expects)
        )
        wikis = self.api.wiki.list(projectIdOrKey=self.default_project)
        self.assertTrue(isinstance(wikis, list))

    @httpretty.activate
    def test_create_wiki(self):
        # Set parameter and expects
        _uri = "wikis"
        _project_id = 1
        _wiki_name = "SamplePage_{}".format(str(uuid4()))
        _wiki_content = "test content"
        _mail_notify = False
        expects = {
            "id": 1,
            "projectId": _project_id,
            "name": _wiki_name,
            "content": _wiki_content,
            "tags": [
                {
                    "id": 12,
                    "name": "議事録"
                }
            ],
            "attachments": [],
            "sharedFiles": [],
            "stars": [],
            "createdUser": {
                "id": 1,
                "userId": "admin",
                "name": "admin",
                "roleType": 1,
                "lang": "ja",
                "mailAddress": "eguchi@nulab.example"
            },
            "created": "2012-07-23T06:09:48Z",
            "updatedUser": {
                "id": 1,
                "userId": "admin",
                "name": "admin",
                "roleType": 1,
                "lang": "ja",
                "mailAddress": "eguchi@nulab.example"
            },
            "updated": "2012-07-23T06:09:48Z",
        }

        httpretty.register_uri(
            method=httpretty.POST,
            uri=API_ENDPOINT.format(space=self.space, uri=_uri),
            body=json.dumps(expects)
        )

        # test
        resp = self.api.wiki.create(
            projectId=_project_id,
            name=_wiki_name,
            content=_wiki_content,
            mailNotify="true" if _mail_notify else "false"
        )

        self.assertEqual(resp["projectId"], _project_id)
        self.assertEqual(resp["name"], _wiki_name)
        self.assertEqual(resp["content"], _wiki_content)

    @httpretty.activate
    def test_get_wiki(self):
        expects = {
            "id": 1,
            "projectId": 1,
            "name": "Home",
            "content": "test",
            "tags": [
                {
                    "id": 12,
                    "name": "議事録"
                }
            ],
            "attachments": [
                {
                    "id": 1,
                    "name": "test.json",
                    "size": 8857,
                    "createdUser": {
                        "id": 1,
                        "userId": "admin",
                        "name": "admin",
                        "roleType": 1,
                        "lang": "ja",
                        "mailAddress": "eguchi@nulab.example"
                    },
                    "created": "2014-01-06T11:10:45Z"
                },
            ],
            "sharedFiles": [
                {
                    "id": 454403,
                    "type": "file",
                    "dir": "/ユーザアイコン/",
                    "name": "01_サラリーマン.png",
                    "size": 2735,
                    "createdUser": {
                        "id": 5686,
                        "userId": "takada",
                        "name": "takada",
                        "roleType": 2,
                        "lang": "ja",
                        "mailAddress": "takada@nulab.example"
                    },
                    "created": "2009-02-27T03:26:15Z",
                    "updatedUser": {
                        "id": 5686,
                        "userId": "takada",
                        "name": "takada",
                        "roleType": 2,
                        "lang": "ja",
                        "mailAddress": "takada@nulab.example"
                    },
                    "updated": "2009-03-03T16:57:47Z"
                }
            ],
            "stars": [],
            "createdUser": {
                "id": 1,
                "userId": "admin",
                "name": "admin",
                "roleType": 1,
                "lang": "ja",
                "mailAddress": "eguchi@nulab.example"
            },
            "created": "2012-07-23T06:09:48Z",
            "updatedUser": {
                "id": 1,
                "userId": "admin",
                "name": "admin",
                "roleType": 1,
                "lang": "ja",
                "mailAddress": "eguchi@nulab.example"
            },
            "updated": "2012-07-23T06:09:48Z",
        }
        _wiki_id = 1
        _uri = "wikis/{wikiId}".format(
            wikiId=_wiki_id
        )

        httpretty.register_uri(
            httpretty.GET,
            API_ENDPOINT.format(space=self.space, uri=_uri),
            body=json.dumps(expects)
        )

        # test
        wiki = self.api.wiki.get(wikiId=_wiki_id)

        self.assertEqual(expects["id"], wiki["id"])
        self.assertEqual(expects["name"], wiki["name"])

    @httpretty.activate
    def test_update_wiki(self):
        expects = {
            "id": 1,
            "projectId": 1,
            "name": "Home",
            "content": "test",
            "tags": [
                {
                    "id": 12,
                    "name": "議事録"
                }
            ],
            "attachments": [
                {
                    "id": 1,
                    "name": "test.json",
                    "size": 8857,
                    "createdUser": {
                        "id": 1,
                        "userId": "admin",
                        "name": "admin",
                        "roleType": 1,
                        "lang": "ja",
                        "mailAddress": "eguchi@nulab.example"
                    },
                    "created": "2014-01-06T11:10:45Z"
                },
            ],
            "stars": [],
            "createdUser": {
                "id": 1,
                "userId": "admin",
                "name": "admin",
                "roleType": 1,
                "lang": "ja",
                "mailAddress": "eguchi@nulab.example"
            },
            "created": "2012-07-23T06:09:48Z",
            "updatedUser": {
                "id": 1,
                "userId": "admin",
                "name": "admin",
                "roleType": 1,
                "lang": "ja",
                "mailAddress": "eguchi@nulab.example"
            },
            "updated": "2012-07-23T06:09:48Z",
        }
        _wiki_id = expects["content"]
        _name = expects["name"]
        _content = expects["content"]
        _mail_notify = False
        _uri = "wikis/{wiki_id}".format(wiki_id=_wiki_id)

        httpretty.register_uri(
            httpretty.PATCH,
            API_ENDPOINT.format(space=self.space, uri=_uri),
            body=json.dumps(expects)
        )

        wiki = self.api.wiki.update(
            wikiId=_wiki_id,
            name=_name,
            content=_content,
            mailNotify=_mail_notify
        )

        self.assertEqual(expects["id"], wiki["id"])
        self.assertEqual(expects["name"], wiki["name"])
        self.assertEqual(expects["content"], wiki["content"])

    @httpretty.activate
    def test_delete_wiki(self):
        expects = {
            "id": 1,
            "projectId": 1,
            "name": "Home",
            "content": "test",
            "tags": [
                {
                    "id": 12,
                    "name": "議事録"
                }
            ],
            "attachments": [
                {
                    "id": 1,
                    "name": "test.json",
                    "size": 8857,
                    "createdUser": {
                        "id": 1,
                        "userId": "admin",
                        "name": "admin",
                        "roleType": 1,
                        "lang": "ja",
                        "mailAddress": "eguchi@nulab.example"
                    },
                    "created": "2014-01-06T11:10:45Z"
                }
            ],
            "sharedFiles": [
                {
                    "id": 454403,
                    "type": "file",
                    "dir": "/ユーザアイコン/",
                    "name": "01_サラリーマン.png",
                    "size": 2735,
                    "createdUser": {
                        "id": 5686,
                        "userId": "takada",
                        "name": "takada",
                        "roleType": 2,
                        "lang": "ja",
                        "mailAddress": "takada@nulab.example"
                    },
                    "created": "2009-02-27T03:26:15Z",
                    "updatedUser": {
                        "id": 5686,
                        "userId": "takada",
                        "name": "takada",
                        "roleType": 2,
                        "lang": "ja",
                        "mailAddress": "takada@nulab.example"
                    },
                    "updated": "2009-03-03T16:57:47Z"
                }
            ],
            "stars": [],
            "createdUser": {
                "id": 1,
                "userId": "admin",
                "name": "admin",
                "roleType": 1,
                "lang": "ja",
                "mailAddress": "eguchi@nulab.example"
            },
            "created": "2012-07-23T06:09:48Z",
            "updatedUser": {
                "id": 1,
                "userId": "admin",
                "name": "admin",
                "roleType": 1,
                "lang": "ja",
                "mailAddress": "eguchi@nulab.example"
            },
            "updated": "2012-07-23T06:09:48Z",
        }
        _wiki_id = expects["id"]
        _mail_notify = False
        _uri = "wikis/{wikiId}".format(
            wikiId=_wiki_id
        )

        httpretty.register_uri(
            httpretty.DELETE,
            API_ENDPOINT.format(space=self.space, uri=_uri),
            body=json.dumps(expects)
        )

        attachments = self.api.wiki.delete(_wiki_id, _mail_notify)

        # test
        self.assertEqual(attachments["id"], _wiki_id)

    @httpretty.activate
    def test_list_attachments(self):
        expects = [
            {
                "id": 1,
                "name": "IMGP0088.JPG",
                "size": 85079
            }
        ]
        _wiki_id = 1
        _uri = "wikis/{wikiId}/attachments".format(
            wikiId=_wiki_id
        )

        httpretty.register_uri(
            httpretty.GET,
            API_ENDPOINT.format(space=self.space, uri=_uri),
            body=json.dumps(expects)
        )

        attachments = self.api.wiki.list_attachments(_wiki_id)

        # test
        self.assertEqual(len(expects), len(attachments))
        self.assertEqual(expects[0]["id"], attachments[0]["id"])

    @httpretty.activate
    def test_add_attachment(self):
        _wiki_id = 1
        _attachment_id = 2
        _uri = "wikis/{wiki_id}/attachments".format(wiki_id=_wiki_id)
        expects = [
            {
                "id": _attachment_id,
                "name": "Duke.png",
                "size": 196186,
                "createdUser": {
                    "id": 1,
                    "userId": "admin",
                    "name": "admin",
                    "roleType": 1,
                    "lang": None,
                    "mailAddress": "eguchi@nulab.example"
                },
                "created": "2014-07-11T06:26:05Z"
            }
        ]

        httpretty.register_uri(
            httpretty.POST,
            API_ENDPOINT.format(space=self.space, uri=_uri),
            body=json.dumps(expects)
        )

        attachments = self.api.wiki.add_attachment(
            wikiId=_wiki_id,
            attachmentId=_attachment_id
        )

        self.assertEqual(expects[0]["id"], attachments[0]["id"])

    @httpretty.activate
    def test_get_attachment(self):
        with tempfile.NamedTemporaryFile(delete=True) as tmp:
            # Set parameter and expects
            _wiki_id = 1234567890
            _attachment_id = 1234567890
            _uri = "wikis/{wikiId}/attachments/{attachmentId}".format(
                wikiId=_wiki_id,
                attachmentId=_attachment_id
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
                body=tmp.file.read(),
                content_type="application/octet-stream"
            )

            # test
            resp = self.api.wiki.get_attachment(
                wikiId=_wiki_id,
                attachmentId=_attachment_id
            )

            self.assertEqual(expects, resp)

    @httpretty.activate
    def test_delete_attachment(self):
        expects = {
            "id": 2,
            "name": "Duke.png",
            "size": 196186,
            "createdUser": {
                "id": 1,
                "userId": "admin",
                "name": "admin",
                "roleType": 1,
                "lang": None,
                "mailAddress": "eguchi@nulab.example"
            },
            "created": "2014-07-11T06:26:05Z"
        }
        _wiki_id = 1
        _attachment_id = expects["id"]
        _uri = "wikis/{wiki_id}/attachments/{attachment_id}".format(
            wiki_id=_wiki_id,
            attachment_id=_attachment_id
        )

        httpretty.register_uri(
            httpretty.DELETE,
            API_ENDPOINT.format(space=self.space, uri=_uri),
            body=json.dumps(expects)
        )

        attachments = self.api.wiki.delete_attachment(
            wikiId=_wiki_id,
            attachmentId=_attachment_id
        )

        self.assertEqual(attachments["id"], _attachment_id)


if __name__ == "__main__":
    unittest.main(warnings='ignore')
