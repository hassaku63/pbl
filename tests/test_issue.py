import unittest
import json
from urllib.parse import parse_qs
from tests import fake_http
from backlog.base import BacklogAPI

API_ENDPOINT = "https://{space}.backlog.jp/api/v2/{uri}"


class TestIssue(unittest.TestCase):
    def setUp(self):
        self.api = BacklogAPI("space", "api_key")
        self.space = "space"
        self.api_key = "api_key"

    @fake_http.activate
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
                        "created": "2013-07-08T10:24:28Z"
                    }
                ]
            }
        ]

        fake_http.add(
            fake_http.GET,
            API_ENDPOINT.format(space=self.space, uri=_uri),
            body=json.dumps(expects),
            status=200
        )

        # test
        resp = self.api.issue.list(projectId=_project_id)

        self.assertEqual(len(resp), 1)
        self.assertEqual(resp[0]["id"], 1)
        self.assertEqual(resp[0]["projectId"], _project_id)

    @fake_http.activate
    def test_count(self):
        _uri = "issues/count"
        expects = {
            "count": 43
        }

        fake_http.add(
            fake_http.GET,
            API_ENDPOINT.format(space=self.space, uri=_uri),
            body=json.dumps(expects),
            status=200
        )

        # test
        resp = self.api.issue.count()

        self.assertEqual(expects["count"], resp["count"])

    @fake_http.activate
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
                "projectId": 1,
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

        fake_http.add(
            fake_http.POST,
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

        self.assertEqual(resp["projectId"], _project_id)
        self.assertEqual(resp["summary"], _summary)
        self.assertEqual(resp["issueType"]["id"], _issue_type_id)
        self.assertEqual(resp["priority"]["id"], _priority_id)

    @fake_http.activate
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
                    "created": "2013-07-08T10:24:28Z"
                }
            ]
        }

        fake_http.add(
            fake_http.GET,
            API_ENDPOINT.format(space=self.space, uri=_uri),
            body=json.dumps(expects),
            status=200
        )

        resp = self.api.issue.get(issueIdOrKey=_issue_key)

        self.assertEqual(expects["issueKey"], resp["issueKey"])

    @fake_http.activate
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
                    "created": "2013-07-08T10:24:28Z"
                }
            ]
        }

        fake_http.add(
            fake_http.PATCH,
            API_ENDPOINT.format(space=self.space, uri=_uri),
            body=json.dumps(expects),
            status=200
        )

        resp = self.api.issue.update(issueIdOrKey=_issue_key)

        self.assertEqual(expects["issueKey"], resp["issueKey"])

    @fake_http.activate
    def test_delete(self):
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
                    "created": "2013-07-08T10:24:28Z"
                }
            ]
        }

        fake_http.add(
            fake_http.DELETE,
            API_ENDPOINT.format(space=self.space, uri=_uri),
            body=json.dumps(expects),
            status=200
        )

        resp = self.api.issue.delete(issueIdOrKey=_issue_key)

        self.assertEqual(expects["issueKey"], resp["issueKey"])

    @fake_http.activate
    def test_add_comment(self):
        _issue_key = "BLG-1"
        _uri = "issues/{issue_id_or_key}/comments".format(issue_id_or_key=_issue_key)
        expects = {
            "id": 6586,
            "content": "test comment",
            "changeLog": None,
            "createdUser": {
                "id": 1,
                "userId": "admin",
                "name": "admin",
                "roleType": 1,
                "lang": "ja",
                "mailAddress": "eguchi@nulab.example"
            },
            "created": "2013-08-05T06:15:06Z",
            "updated": "2013-08-05T06:15:06Z",
            "stars": [],
            "notifications": [],
        }

        fake_http.add(
            fake_http.POST,
            API_ENDPOINT.format(space=self.space, uri=_uri),
            body=json.dumps(expects),
            status=201,
        )

        resp = self.api.issue.add_comment(
            issueIdOrKey=_issue_key,
            content='test comment',
            notifiedUserId=[],
            attachmentId=[])

        self.assertEqual('test comment', resp["content"])

    @fake_http.activate
    def test_comment_attachment_and_shared_file_apis(self):
        """
        Each call sends the documented method, path, query string and form body,
        and returns the decoded JSON response.
        """
        base = "issues/BLG-1"
        cases = [
            ("get_comments", lambda: self.api.issue.get_comments("BLG-1", minId=1, count=10, order="asc"),
             "GET", base + "/comments", {"minId": ["1"], "count": ["10"], "order": ["asc"]}, {}),
            ("get_comments (defaults)", lambda: self.api.issue.get_comments("BLG-1"),
             "GET", base + "/comments", {}, {}),
            ("count_comments", lambda: self.api.issue.count_comments("BLG-1"),
             "GET", base + "/comments/count", {}, {}),
            ("get_comment", lambda: self.api.issue.get_comment("BLG-1", 10),
             "GET", base + "/comments/10", {}, {}),
            ("update_comment", lambda: self.api.issue.update_comment("BLG-1", 10, "new text"),
             "PATCH", base + "/comments/10", {}, {"content": ["new text"]}),
            ("delete_comment", lambda: self.api.issue.delete_comment("BLG-1", 10),
             "DELETE", base + "/comments/10", {}, {}),
            ("get_comment_notifications", lambda: self.api.issue.get_comment_notifications("BLG-1", 10),
             "GET", base + "/comments/10/notifications", {}, {}),
            ("add_comment_notification", lambda: self.api.issue.add_comment_notification("BLG-1", 10, [1, 2]),
             "POST", base + "/comments/10/notifications", {}, {"notifiedUserId[]": ["1", "2"]}),
            ("list_issue_attachments", lambda: self.api.issue.list_issue_attachments("BLG-1"),
             "GET", base + "/attachments", {}, {}),
            ("delete_issue_attachment", lambda: self.api.issue.delete_issue_attachment("BLG-1", 8),
             "DELETE", base + "/attachments/8", {}, {}),
            ("list_issue_shared_files", lambda: self.api.issue.list_issue_shared_files("BLG-1"),
             "GET", base + "/sharedFiles", {}, {}),
            ("link_issue_shared_files", lambda: self.api.issue.link_issue_shared_files("BLG-1", [3, 4]),
             "POST", base + "/sharedFiles", {}, {"fileId[]": ["3", "4"]}),
            ("link_issue_shared_files (single)", lambda: self.api.issue.link_issue_shared_files("BLG-1", 3),
             "POST", base + "/sharedFiles", {}, {"fileId[]": ["3"]}),
            ("unlink_issue_shared_file", lambda: self.api.issue.unlink_issue_shared_file("BLG-1", 3),
             "DELETE", base + "/sharedFiles/3", {}, {}),
            ("list_participants", lambda: self.api.issue.list_participants("BLG-1"),
             "GET", base + "/participants", {}, {}),
            ("list_related_issues", lambda: self.api.issue.list_related_issues("BLG-1"),
             "GET", base + "/relatedIssues", {}, {}),
            ("add_related_issue", lambda: self.api.issue.add_related_issue("BLG-1", 42),
             "POST", base + "/relatedIssues", {}, {"targetIssueId": ["42"]}),
            ("remove_related_issue", lambda: self.api.issue.remove_related_issue("BLG-1", 42),
             "DELETE", base + "/relatedIssues/42", {}, {}),
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
    def test_get_issue_attachment(self):
        fake_http.add(
            fake_http.GET,
            API_ENDPOINT.format(space=self.space, uri="issues/BLG-1/attachments/8"),
            body=b"\x89PNG",
            content_type="image/png",
            headers={"Content-Disposition": "attachment;filename*=UTF-8''%E5%9B%B3.png"},
        )

        for method in [self.api.issue.get_issue_attachment, self.api.issue.get_issue_attachments]:
            with self.subTest(method=method.__name__):
                self.assertEqual({"id": 8, "name": "図.png", "data": b"\x89PNG"}, method("BLG-1", 8))
