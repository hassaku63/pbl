# coding: utf-8
"""
Read-only smoke tests: the implemented methods are accepted by the real API and return the expected shapes.
"""

import unittest

from backlog.base import BacklogError
from tests.e2e.support import PROJECT_KEY, client, requires_project, requires_space


@requires_space
class TestSpaceRead(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.api = client()

    def test_users(self):
        users = self.api.user.list()
        self.assertIsInstance(users, list)
        self.assertTrue(users)
        self.assertEqual(users[0]["id"], self.api.user.get(users[0]["id"])["id"])

    def test_projects(self):
        self.assertIsInstance(self.api.project.list(), list)

    def test_myself_and_watchings(self):
        me = self.api.user.get_myself()
        self.assertIn("id", me)
        self.assertIsInstance(self.api.watching.list(me["id"], count=1), list)
        self.assertIn("count", self.api.watching.count(me["id"]))

    def test_notifications(self):
        self.assertIsInstance(self.api.notification.list(count=1), list)
        self.assertIn("count", self.api.notification.count(resourceAlreadyRead=False))

    def test_rate_limit(self):
        self.assertIn("rateLimit", self.api.get_rate_limit())

    def test_priorities_and_resolutions(self):
        self.assertTrue(self.api.priority.list())
        self.assertTrue(self.api.resolution.list())


@requires_project
class TestProjectRead(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.api = client()
        cls.project = cls.api.project.get(PROJECT_KEY)

    def test_project(self):
        self.assertEqual(PROJECT_KEY, self.project["projectKey"])

    def test_project_users(self):
        self.assertIsInstance(self.api.project.list_users(PROJECT_KEY), list)

    def test_issue_types(self):
        self.assertTrue(self.api.project.list_issue_types(PROJECT_KEY))

    def test_statuses_and_versions(self):
        self.assertTrue(self.api.project.list_statuses(PROJECT_KEY))
        self.assertIsInstance(self.api.project.list_versions(PROJECT_KEY), list)

    def test_categories(self):
        self.assertIsInstance(self.api.category.list(PROJECT_KEY), list)

    def test_custom_fields(self):
        self.assertIsInstance(self.api.custom_field.list(PROJECT_KEY), list)

    def test_issues(self):
        params = {"projectId[]": [self.project["id"]]}
        self.assertIsInstance(self.api.issue.list(count=1, **params), list)
        self.assertIn("count", self.api.issue.count(**params))

    def test_wikis(self):
        if not self.project.get("useWiki"):
            self.skipTest("Wiki is disabled in the project")
        self.assertIsInstance(self.api.wiki.list(PROJECT_KEY), list)

    def test_git_repositories(self):
        if not self.project.get("useGit"):
            self.skipTest("Git is disabled in the project")
        try:
            self.assertIsInstance(self.api.git.list_git_repositories(PROJECT_KEY), list)
        except BacklogError as e:
            if '"code":2' in str(e).replace(" ", ""):
                self.skipTest("Git is not available in the plan (LicenceError)")
            raise
