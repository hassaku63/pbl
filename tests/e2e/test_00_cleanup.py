# coding: utf-8
"""
Delete resources left over by earlier runs (named with the e2e prefix). The module name sorts
first, so it runs before the other end-to-end tests. When a test creates a new kind of resource,
add it here.
"""

import unittest

from tests.e2e.support import PREFIX, PROJECT_KEY, client, is_leftover, is_previous_run, requires_write


@requires_write
class TestCleanupLeftovers(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.api = client()
        cls.project = cls.api.project.get(PROJECT_KEY)

    def test_issues(self):
        issues = self.api.issue.list(keyword=PREFIX, count=100, **{"projectId[]": [self.project["id"]]})
        for issue in issues:
            if is_leftover(issue.get("summary"), issue.get("created")):
                self.api.issue.delete(issue["issueKey"])

    def test_wikis(self):
        if not self.project.get("useWiki"):
            self.skipTest("Wiki is disabled in the project")
        for wiki in self.api.wiki.list(PROJECT_KEY):
            if is_leftover(wiki.get("name"), wiki.get("created")):
                self.api.wiki.delete(wiki["id"], mailNotify=False)

    def test_documents(self):
        for document in self.api.document.list(projectId=self.project["id"], keyword=PREFIX, count=100):
            if is_leftover(document.get("title"), document.get("created")):
                self.api.document.delete(document["id"])

    def test_categories(self):
        # Categories have no creation time: delete those named by an earlier run.
        for category in self.api.category.list(PROJECT_KEY):
            if is_previous_run(category.get("name")):
                self.api.category.delete(PROJECT_KEY, category["id"])
