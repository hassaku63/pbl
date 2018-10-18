import unittest
import json
import httpretty
from backlog.util import load_conf
from backlog.base import BacklogAPI

API_ENDPOINT = "https://{space}.backlog.jp/api/v2/{uri}"


class TestIssue(unittest.TestCase):
    def setUp(self):
        self.conf = load_conf("./conf.default.yml")["backlog"]
        self.api = BacklogAPI(self.conf["space"], self.conf["api_key"])
        self.space = self.conf["space"]
        self.api_key = self.conf["api_key"]

    @httpretty.activate
    def test_list(self):
        # Set parameter and expects
        _uri = "issues"
        _project_id = 1
        expects = [
            {
                "id": 1,
                "projectId": 1,
                "issueKey": "BLG-1",
                "keyId": 1,
                "issueType": {
                    "id": 2,
                    "projectId" :1,
                    "name": "タスク",
                    "color": "#7ea800",
                    "displayOrder": 0
                },
                "summary": "first issue",
                "description": "",
                "resolutions": None,
                "priority": {
                    "id": 3,
                    "name": "中"
                },
                "status": {
                    "id": 1,
                    "name": "未対応"
                },
                "assignee": {
                    "id": 2,
                    "name": "eguchi",
                    "roleType" :2,
                    "lang": None,
                    "mailAddress": "eguchi@nulab.example"
                },
                "category": [],
                "versions": [],
                "milestone": [
                    {
                        "id": 30,
                        "projectId": 1,
                        "name": "wait for release",
                        "description": "",
                        "startDate": None,
                        "releaseDueDate": None,
                        "archived": False,
                        "displayOrder": 0
                    }
                ],
                "startDate": None,
                "dueDate": None,
                "estimatedHours": None,
                "actualHours": None,
                "parentIssueId": None,
                "createdUser": {
                    "id": 1,
                    "userId": "admin",
                    "name": "admin",
                    "roleType": 1,
                    "lang": "ja",
                    "mailAddress": "eguchi@nulab.example"
                },
                "created": "2012-07-23T06:10:15Z",
                "updatedUser": {
                    "id": 1,
                    "userId": "admin",
                    "name": "admin",
                    "roleType": 1,
                    "lang": "ja",
                    "mailAddress": "eguchi@nulab.example"
                },
                "updated": "2013-02-07T08:09:49Z",
                "customFields": [],
                "attachments": [
                    {
                        "id": 1,
                        "name": "IMGP0088.JPG",
                        "size": 85079
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
                            "roleType":2,
                            "lang":"ja",
                            "mailAddress":"takada@nulab.example"
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
                        "updated":"2009-03-03T16:57:47Z"
                    }
                ],
                "stars": [
                    {
                        "id": 10,
                        "comment": None,
                        "url": "https://xx.backlog.jp/view/BLG-1",
                        "title": "[BLG-1] first issue | 課題の表示 - Backlog",
                        "presenter": {
                            "id": 2,
                            "userId": "eguchi",
                            "name": "eguchi",
                            "roleType": 2,
                            "lang": "ja",
                            "mailAddress": "eguchi@nulab.example"
                        },
                        "created":"2013-07-08T10:24:28Z"
                    }
                ]
            }
        ]

        httpretty.register_uri(
            httpretty.GET,
            API_ENDPOINT.format(space=self.space, uri=_uri),
            body=json.dumps(expects),
            status=200
        )

        # test
        resp = self.api.issue.list(projectId=_project_id)

        self.assertEqual(len(expects), 1)
        self.assertEqual(expects[0]["id"], 1)
        self.assertEqual(expects[0]["projectId"], _project_id)

    @httpretty.activate
    def test_count(self):
        _uri = "issues/count"
        expects = {
            "count": 43
        }

        httpretty.register_uri(
            httpretty.GET,
            API_ENDPOINT.format(space=self.space, uri=_uri),
            body=json.dumps(expects),
            status=200
        )

        # test
        resp = self.api.issue.count()

        self.assertEqual(expects["count"], resp["count"])

    @httpretty.activate
    def test_create(self):
        # Set parameter and expects
        _uri = "issues"
        _project_id = 1
        _summary = "first issue"
        _issue_type_id = 2
        _priority_id = 3
        expects = {
            "id": 1,
            "projectId": _project_id,
            "issueKey": "BLG-1",
            "keyId": 1,
            "issueType": {
                "id": _issue_type_id,
                "projectId" :1,
                "name": "タスク",
                "color": "#7ea800",
                "displayOrder": 0
            },
            "summary": _summary,
            "description": "",
            "resolutions": None,
            "priority": {
                "id": _priority_id,
                "name": "中"
            },
            "status": {
                "id": 1,
                "name": "未対応"
            },
            "assignee": {
                "id": 2,
                "userId": "eguchi",
                "name": "eguchi",
                "roleType": 2,
                "lang": None,
                "mailAddress": "eguchi@nulab.example"
            },
            "category": [],
            "versions": [],
            "milestone": [
                {
                    "id": 30,
                    "projectId": 1,
                    "name": "wait for release",
                    "description": "",
                    "startDate": None,
                    "releaseDueDate": None,
                    "archived": False,
                    "displayOrder": 0
                }
            ],
            "startDate": None,
            "dueDate": None,
            "estimatedHours": None,
            "actualHours": None,
            "parentIssueId": None,
            "createdUser": {
                "id": 1,
                "userId": "admin",
                "name": "admin",
                "roleType": 1,
                "lang": "ja",
                "mailAddress": "eguchi@nulab.example"
            },
            "created": "2012-07-23T06:10:15Z",
            "updatedUser": {
                "id": 1,
                "userId": "admin",
                "name": "admin",
                "roleType": 1,
                "lang": "ja",
                "mailAddress": "eguchi@nulab.example"
            },
            "updated": "2012-07-23T06:10:15Z",
            "customFields": [],
            "attachments": [
                {
                    "id": 1,
                    "name": "IMGP0088.JPG",
                    "size": 85079
                }
            ],
            "sharedFiles": [],
            "stars": []
        }

        httpretty.register_uri(
            httpretty.POST,
            API_ENDPOINT.format(space=self.space, uri=_uri),
            body=json.dumps(expects),
            status=201  # Created response
        )

        # test
        resp = self.api.issue.create(
            projectId=_project_id,
            summary=_summary,
            issueTypeId=_issue_type_id,
            priorityId=_priority_id
        )

        self.assertEqual(expects["projectId"], _project_id)
        self.assertEqual(expects["summary"], _summary)
        self.assertEqual(expects["issueType"]["id"], _issue_type_id)
        self.assertEqual(expects["priority"]["id"], _priority_id)

    @httpretty.activate
    def test_get(self):
        _issue_key = "BLG-1"
        _uri = "issues/{issue_id_or_key}".format(issue_id_or_key=_issue_key)
        expects = {
            "id": 1,
            "projectId": 1,
            "issueKey": _issue_key,
            "keyId": 1,
            "issueType": {
                "id": 2,
                "projectId" :1,
                "name": "タスク",
                "color": "#7ea800",
                "displayOrder": 0
            },
            "summary": "first issue",
            "description": "",
            "resolutions": None,
            "priority": {
                "id": 3,
                "name": "中"
            },
            "status": {
                "id": 1,
                "name": "未対応"
            },
            "assignee": {
                "id": 2,
                "name": "eguchi",
                "roleType" :2,
                "lang": None,
                "mailAddress": "eguchi@nulab.example"
            },
            "category": [],
            "versions": [],
            "milestone": [
                {
                    "id": 30,
                    "projectId": 1,
                    "name": "wait for release",
                    "description": "",
                    "startDate": None,
                    "releaseDueDate": None,
                    "archived": False,
                    "displayOrder": 0
                }
            ],
            "startDate": None,
            "dueDate": None,
            "estimatedHours": None,
            "actualHours": None,
            "parentIssueId": None,
            "createdUser": {
                "id": 1,
                "userId": "admin",
                "name": "admin",
                "roleType": 1,
                "lang": "ja",
                "mailAddress": "eguchi@nulab.example"
            },
            "created": "2012-07-23T06:10:15Z",
            "updatedUser": {
                "id": 1,
                "userId": "admin",
                "name": "admin",
                "roleType": 1,
                "lang": "ja",
                "mailAddress": "eguchi@nulab.example"
            },
            "updated": "2013-02-07T08:09:49Z",
            "customFields": [],
            "attachments": [
                {
                    "id": 1,
                    "name": "IMGP0088.JPG",
                    "size": 85079
                }
            ],
            "sharedFiles": [],
            "stars": [
                {
                    "id": 10,
                    "comment": None,
                    "url": "https://xx.backlog.jp/view/BLG-1",
                    "title": "[BLG-1] first issue | 課題の表示 - Backlog",
                    "presenter": {
                        "id": 2,
                        "userId": "eguchi",
                        "name": "eguchi",
                        "roleType": 2,
                        "lang": "ja",
                        "mailAddress": "eguchi@nulab.example"
                    },
                    "created":"2013-07-08T10:24:28Z"
                }
            ]
        }

        httpretty.register_uri(
            httpretty.GET,
            API_ENDPOINT.format(space=self.space, uri=_uri),
            body=json.dumps(expects),
            status=200
        )

        resp = self.api.issue.get(issueIdOrKey=_issue_key)

        self.assertEqual(expects["issueKey"], resp["issueKey"])

    @httpretty.activate
    def test_update(self):
        _issue_key = "BLG-1"
        _uri = "issues/{issue_id_or_key}".format(issue_id_or_key=_issue_key)
        expects = { 
            "id": 1,
            "projectId": 1,
            "issueKey": _issue_key,
            "keyId": 1,
            "issueType": {
                "id": 2,
                "projectId": 1,
                "name": "タスク",
                "color": "#7ea800",
                "displayOrder": 0
            },
            "summary": "first issue",
            "description": "",
            "resolutions": None,
            "priority": {
                "id": 3,
                "name": "中"
            },
            "status": {
                "id": 1,
                "name": "未対応"
            },
            "assignee": {
                "id": 2,
                "name": "eguchi",
                "roleType": 2,
                "lang": None,
                "mailAddress": "eguchi@nulab.example"
            },
            "category": [],
            "versions": [],
            "milestone": [
                {
                    "id": 30,
                    "projectId": 1,
                    "name": "wait for release",
                    "description": "",
                    "startDate": None,
                    "releaseDueDate": None,
                    "archived": False,
                    "displayOrder": 0
                }
            ],
            "startDate": None,
            "dueDate": None,
            "estimatedHours": None,
            "actualHours": None,
            "parentIssueId": None,
            "createdUser": {
                "id": 1,
                "userId": "admin",
                "name": "admin",
                "roleType": 1,
                "lang": "ja",
                "mailAddress": "eguchi@nulab.example"
            },
            "created": "2012-07-23T06:10:15Z",
            "updatedUser": {
                "id": 1,
                "userId": "admin",
                "name": "admin",
                "roleType": 1,
                "lang": "ja",
                "mailAddress": "eguchi@nulab.example"
            },
            "updated": "2013-02-07T08:09:49Z",
            "customFields": [],
            "attachments": [
                {
                    "id": 1,
                    "name": "IMGP0088.JPG",
                    "size": 85079
                }
            ],
            "sharedFiles": [],
            "stars": [
                {
                    "id": 10,
                    "comment": None,
                    "url": "https://xx.backlog.jp/view/BLG-1",
                    "title": "[BLG-1] first issue | 課題の表示 - Backlog",
                    "presenter": {
                        "id": 2,
                        "userId": "eguchi",
                        "name": "eguchi",
                        "roleType": 2,
                        "lang": "ja",
                        "mailAddress": "eguchi@nulab.example"
                    },
                    "created":"2013-07-08T10:24:28Z"
                }
            ]
        }

        httpretty.register_uri(
            httpretty.PATCH,
            API_ENDPOINT.format(space=self.space, uri=_uri),
            body=json.dumps(expects),
            status=200
        )

        resp = self.api.issue.update(issueIdOrKey=_issue_key)

        self.assertEqual(expects["issueKey"], resp["issueKey"])

    def test_delete(self):
        pass

    def test_get_comments(self):
        pass

    def test_add_comment(self):
        pass

    def test_count_comments(self):
        pass

    def test_get_comment(self):
        pass

    def test_update_comment(self):
        pass

    def test_get_comment_notifications(self):
        pass

    def test_add_comment_notifycation(self):
        pass

    def test_list_issue_attachments(self):
        pass

    def test_get_issue_attachments(self):
        pass

    def test_delete_issue_attachment(self):
        pass

    def test_list_issue_shared_files(self):
        pass

    def test_link_issue_shared_files(self):
        pass

    def test_unlink_issue_shared_file(self):
        pass
