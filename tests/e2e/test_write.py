# coding: utf-8
"""
Write round trip in the test project. Runs only with BACKLOG_E2E_WRITE=1, and deletes what it creates.
"""

import unittest

from tests.e2e.support import PROJECT_KEY, client, requires_write


@requires_write
class TestIssueRoundTrip(unittest.TestCase):
    def test_issue_and_comment_round_trip(self):
        api = client()
        project = api.project.get(PROJECT_KEY)
        issue_type = api.project.list_issue_types(PROJECT_KEY)[0]
        priority = api.priority.list()[-1]

        issue = api.issue.create(
            projectId=project["id"],
            summary="python-backlog e2e test (safe to delete)",
            issueTypeId=issue_type["id"],
            priorityId=priority["id"],
        )
        try:
            key = issue["issueKey"]
            self.assertEqual(issue["id"], api.issue.get(key)["id"])

            comment = api.issue.add_comment(key, "e2e comment")
            self.assertEqual("e2e comment", api.issue.get_comment(key, comment["id"])["content"])
            self.assertEqual("e2e comment (edited)", api.issue.update_comment(key, comment["id"], "e2e comment (edited)")["content"])
            self.assertIn(comment["id"], [c["id"] for c in api.issue.get_comments(key)])
            self.assertEqual(1, api.issue.count_comments(key)["count"])
            api.issue.delete_comment(key, comment["id"])
            self.assertEqual(0, api.issue.count_comments(key)["count"])
        finally:
            api.issue.delete(issue["issueKey"])
