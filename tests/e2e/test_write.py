# coding: utf-8
"""
Tier W: write round trips in the test project. Runs only with BACKLOG_E2E_WRITE=1, names every
resource with the e2e prefix and deletes what it creates. Assertions follow tests/e2e/README.md.
"""

import unittest

from tests.e2e import assertions as check
from tests.e2e.support import PROJECT_KEY, client, requires_write, resource_name


@requires_write
class TestIssueRoundTrip(unittest.TestCase):
    def test_issue_and_comment_round_trip(self):
        api = client()
        project = api.project.get(PROJECT_KEY)
        issue_type = api.project.list_issue_types(PROJECT_KEY)[0]
        priority = api.priority.list()[-1]
        summary = resource_name("issue")

        issue = api.issue.create(
            projectId=project["id"],
            summary=summary,
            issueTypeId=issue_type["id"],
            priorityId=priority["id"],
        )
        try:
            check.field_equals(issue, "summary", summary, what="issue.create()")
            check.has_keys(issue, "id", "issueKey", "status", "created", what="issue.create()")
            key = issue["issueKey"]
            check.field_equals(api.issue.get(key), "id", issue["id"], what="issue.get()")

            comment = api.issue.add_comment(key, "e2e comment")
            check.field_type(comment, "id", int, what="issue.add_comment()")
            check.field_equals(api.issue.get_comment(key, comment["id"]), "content", "e2e comment", what="issue.get_comment()")
            updated = api.issue.update_comment(key, comment["id"], "e2e comment (edited)")
            check.field_equals(updated, "content", "e2e comment (edited)", what="issue.update_comment()")
            check.contains_id(api.issue.get_comments(key), comment["id"], what="issue.get_comments()")
            check.is_count(api.issue.count_comments(key), what="issue.count_comments()", expected=1)
            api.issue.delete_comment(key, comment["id"])
            check.is_count(api.issue.count_comments(key), what="issue.count_comments()", expected=0)
        finally:
            api.issue.delete(issue["issueKey"])
