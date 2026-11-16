# coding: utf-8
"""
Delete resources left over by earlier runs (named with the e2e prefix and older than an hour).
The module name sorts first, so it runs before the other end-to-end tests.
"""

import unittest

from tests.e2e.support import PREFIX, PROJECT_KEY, client, is_leftover, requires_write


@requires_write
class TestCleanupLeftovers(unittest.TestCase):
    def test_delete_leftover_issues(self):
        api = client()
        project = api.project.get(PROJECT_KEY)
        issues = api.issue.list(keyword=PREFIX, count=100, **{"projectId[]": [project["id"]]})
        for issue in issues:
            if is_leftover(issue.get("summary"), issue.get("created")):
                api.issue.delete(issue["issueKey"])
