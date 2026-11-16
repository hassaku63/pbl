# coding: utf-8
"""
Tier R: read-only smoke tests. The implemented methods are accepted by the real API and return
the minimal structure each test needs. Assertions follow tests/e2e/README.md.
"""

import unittest

from backlog.base import BacklogError
from tests.e2e import assertions as check
from tests.e2e.support import PROJECT_KEY, client, requires_project, requires_space


@requires_space
class TestSpaceRead(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.api = client()

    def test_users(self):
        users = self.api.user.list()
        check.is_list(users, what="user.list()", min_length=1, item_keys=("id",))
        user = self.api.user.get(users[0]["id"])
        check.field_equals(user, "id", users[0]["id"], what="user.get()")

    def test_projects(self):
        check.is_list(self.api.project.list(), what="project.list()", item_keys=("id", "projectKey"))

    def test_myself_and_watchings(self):
        me = self.api.user.get_myself()
        check.field_type(me, "id", int, what="user.get_myself()")
        check.is_list(self.api.watching.list(me["id"], count=1), what="watching.list()")
        check.is_count(self.api.watching.count(me["id"]), what="watching.count()")

    def test_activities(self):
        activities = self.api.activity.list(count=1)
        check.is_list(activities, what="activity.list()", item_keys=("id", "type"))
        if activities:
            activity = self.api.activity.get(activities[0]["id"])
            check.field_equals(activity, "id", activities[0]["id"], what="activity.get()")
        me = self.api.user.get_myself()
        check.is_list(self.api.activity.list_user(me["id"], count=1), what="activity.list_user()", item_keys=("id",))

    def test_notifications(self):
        check.is_list(self.api.notification.list(count=1), what="notification.list()")
        check.is_count(self.api.notification.count(resourceAlreadyRead=False), what="notification.count()")

    def test_rate_limit(self):
        check.has_keys(self.api.get_rate_limit(), "rateLimit", what="get_rate_limit()")

    def test_priorities_and_resolutions(self):
        check.is_list(self.api.priority.list(), what="priority.list()", min_length=1, item_keys=("id", "name"))
        check.is_list(self.api.resolution.list(), what="resolution.list()", min_length=1, item_keys=("id", "name"))


@requires_project
class TestProjectRead(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.api = client()
        cls.project = cls.api.project.get(PROJECT_KEY)

    def test_project(self):
        check.field_equals(self.project, "projectKey", PROJECT_KEY, what="project.get()")
        check.field_type(self.project, "id", int, what="project.get()")

    def test_project_users(self):
        check.is_list(self.api.project.list_users(PROJECT_KEY), what="project.list_users()", min_length=1, item_keys=("id",))

    def test_issue_types(self):
        check.is_list(self.api.project.list_issue_types(PROJECT_KEY), what="project.list_issue_types()", min_length=1,
                      item_keys=("id", "name"))

    def test_statuses_and_versions(self):
        check.is_list(self.api.project.list_statuses(PROJECT_KEY), what="project.list_statuses()", min_length=1,
                      item_keys=("id", "name"))
        check.is_list(self.api.project.list_versions(PROJECT_KEY), what="project.list_versions()", item_keys=("id", "name"))

    def test_categories(self):
        check.is_list(self.api.category.list(PROJECT_KEY), what="category.list()", item_keys=("id", "name"))

    def test_custom_fields(self):
        check.is_list(self.api.custom_field.list(PROJECT_KEY), what="custom_field.list()", item_keys=("id", "typeId"))

    def test_activities(self):
        check.is_list(self.api.activity.list_project(PROJECT_KEY, count=1), what="activity.list_project()", item_keys=("id",))

    def test_issues(self):
        params = {"projectId[]": [self.project["id"]]}
        check.is_list(self.api.issue.list(count=1, **params), what="issue.list()", item_keys=("id", "issueKey"))
        check.is_count(self.api.issue.count(**params), what="issue.count()")

    def test_documents(self):
        check.is_list(self.api.document.list(projectId=self.project["id"], count=1), what="document.list()", item_keys=("id",))
        check.is_count(self.api.document.count(PROJECT_KEY), what="document.count()")

    def test_wikis(self):
        if not self.project.get("useWiki"):
            self.skipTest("Wiki is disabled in the project")
        check.is_list(self.api.wiki.list(PROJECT_KEY), what="wiki.list()", item_keys=("id", "name"))

    def test_git_repositories(self):
        if not self.project.get("useGit"):
            self.skipTest("Git is disabled in the project")
        try:
            repositories = self.api.git.list_git_repositories(PROJECT_KEY)
        except BacklogError as e:
            if '"code":2' in str(e).replace(" ", ""):
                self.skipTest("Git is not available in the plan (LicenceError)")
            raise
        check.is_list(repositories, what="git.list_git_repositories()", item_keys=("id", "name"))
