# coding: utf-8

import unittest
import httpretty
import json
from backlog.util import load_conf
from backlog.base import BacklogAPI

API_ENDPOINT = "https://{space}.backlog.jp/api/v2/{uri}"


class TestProject(unittest.TestCase):
    def setUp(self):
        self.conf = load_conf("./conf.default.yml")["backlog"]
        self.api = BacklogAPI(self.conf["space"], self.conf["api_key"])
        self.space = self.conf["space"]
        self.api_key = self.conf["api_key"]

    #
    # For Git Repository
    #
    @httpretty.activate
    def test_list_git_repositories(self):
        _project_id_or_key = 151
        _uri = "projects/{projectIdOrKey}/git/repositories".format(projectIdOrKey=_project_id_or_key)

        expects = [
            {
                "id": 1,
                "projectId": _project_id_or_key,
                "name": "app",
                "description": "",
                "hookUrl": None,
                "httpUrl": "https://xx.backlog.jp/git/BLG/app.git",
                "sshUrl": "xx@xx.git.backlog.jp:/BLG/app.git",
                "displayOrder": 0,
                "pushedAt": None,
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
            body=json.dumps(expects),
            match_querystring=True,
            status=200
        )

        resp = self.api.git.list_git_repositories(projectIdOrKey=_project_id_or_key)

        self.assertEqual(expects, resp)

    @httpretty.activate
    def test_get_git_repositories(self):
        pass

    #
    # For Pull Request
    #
    @httpretty.activate
    def test_list_pull_requests(self):
        pass

    @httpretty.activate
    def test_count_pull_requests(self):
        pass

    @httpretty.activate
    def test_add_pull_request(self):
        _project_id_or_key = 3
        _repository_id_or_key = 5
        _uri = "projects/{projectIdOrKey}/git/repositories/{repoIdOrName}/pullRequests".format(
            projectIdOrKey=_project_id_or_key,
            repoIdOrName=_repository_id_or_key
        )

        expects = {
            "id": 2,
            "projectId": _project_id_or_key,
            "repositoryId": _repository_id_or_key,
            "number": 1,
            "summary": "test",
            "description": "test data",
            "base": "master",
            "branch": "develop",
            "status": {
                "id": 1,
                "name": "Open"
            },
            "assignee": {
                "id": 5,
                "userId": "testuser2",
                "name": "testuser2",
                "roleType": 1,
                "lang": None,
                "mailAddress": "testuser2@nulab.test"
            },
            "issue": {
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
                        "archived": False
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
            },
            "baseCommit": None,
            "branchCommit": None,
            "closeAt": None,
            "mergeAt": None,
            "createdUser": {
                "id": 1,
                "userId": "admin",
                "name": "admin",
                "roleType": 1,
                "lang": "ja",
                "mailAddress": "eguchi@nulab.example"
            },
            "created": "2015-04-23T03:04:14Z",
            "updatedUser": {
                "id": 1,
                "userId": "admin",
                "name": "admin",
                "roleType": 1,
                "lang": "ja",
                "mailAddress": "eguchi@nulab.example"
            },
            "updated": "2015-04-23T03:04:14Z"
        }

        httpretty.register_uri(
            httpretty.POST,
            API_ENDPOINT.format(space=self.space, uri=_uri),
            body=json.dumps(expects),
            # match_querystring=True,
            status=200
        )

        resp = self.api.git.add_pull_request(
            projectIdOrKey=_project_id_or_key,
            repoIdOrName=_repository_id_or_key)

        self.assertEqual(expects, resp)

    @httpretty.activate
    def test_get_pull_requests(self):
        pass

    @httpretty.activate
    def test_update_pull_requests(self):
        pass

    @httpretty.activate
    def test_get_pull_request_comment(self):
        pass

    @httpretty.activate
    def test_add_pull_request_comment(self):
        _project_id_or_key = 3
        _repository_id_or_key = 5
        _number = 1
        _content = "test",
        _notified_user_ids = []
        _uri = "projects/{projectIdOrKey}/git/repositories/{repoIdOrName}/pullRequests/{number}/comments".format(
            projectIdOrKey=_project_id_or_key,
            repoIdOrName=_repository_id_or_key,
            number=_number
        )

        expects = {
            "id": 35,
            "content": "from api",
            "changeLog": [
                {
                    "field": "dependentIssue",
                    "newValue": "GIT-3",
                    "originalValue": None
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
            "created": "2015-05-14T01:53:38Z",
            "updated": "2015-05-14T01:53:38Z",
            "stars": [],
            "notifications": []
        }

        httpretty.register_uri(
            httpretty.POST,
            API_ENDPOINT.format(space=self.space, uri=_uri),
            body=json.dumps(expects),
            # match_querystring=True,
            status=200
        )

        resp = self.api.git.add_pull_request_comment(
            projectIdOrKey=_project_id_or_key,
            repoIdOrName=_repository_id_or_key,
            number=_number,
            content=_content,
            notifiedUserIds=_notified_user_ids
        )

        self.assertEqual(expects, resp)

    @httpretty.activate
    def test_count_pull_request_comments(self):
        pass

    @httpretty.activate
    def test_update_pull_request_comment(self):
        pass

    @httpretty.activate
    def test_list_pull_request_attachments(self):
        pass

    @httpretty.activate
    def test_get_pull_request_attachment(self):
        pass

    @httpretty.activate
    def test_delelte_pull_request_attachment(self):
        pass


if __name__ == "__main__":
    unittest.main(warnings='ignore')
