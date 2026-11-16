# coding: utf-8
"""
Tier W: create -> read -> update -> delete round trips in the test project. Runs only with
BACKLOG_E2E_WRITE=1, names every resource with resource_name() and deletes what it creates in
finally. Assertions follow tests/e2e/README.md.

The API key's user needs to be an administrator of the test project (not of the space) for
documents, categories, versions and statuses.
"""

import os
import tempfile
import unittest

from tests.e2e import assertions as check
from tests.e2e.support import PROJECT_KEY, client, requires_write, resource_name


@requires_write
class TestIssueRoundTrip(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.api = client()
        cls.project = cls.api.project.get(PROJECT_KEY)
        cls.issue_type = cls.api.project.list_issue_types(PROJECT_KEY)[0]
        cls.priority = cls.api.priority.list()[-1]

    def _create_issue(self, label):
        summary = resource_name(label)
        issue = self.api.issue.create(
            projectId=self.project["id"],
            summary=summary,
            issueTypeId=self.issue_type["id"],
            priorityId=self.priority["id"],
        )
        check.field_equals(issue, "summary", summary, what="issue.create()")
        check.has_keys(issue, "id", "issueKey", "status", "created", what="issue.create()")
        return issue

    def test_issue_and_comment_round_trip(self):
        issue = self._create_issue("issue")
        try:
            key = issue["issueKey"]
            check.field_equals(self.api.issue.get(key), "id", issue["id"], what="issue.get()")
            updated = self.api.issue.update(key, description="updated by the e2e test")
            check.field_equals(updated, "description", "updated by the e2e test", what="issue.update()")

            comment = self.api.issue.add_comment(key, "e2e comment")
            check.field_type(comment, "id", int, what="issue.add_comment()")
            check.field_equals(self.api.issue.get_comment(key, comment["id"]), "content", "e2e comment", what="issue.get_comment()")
            edited = self.api.issue.update_comment(key, comment["id"], "e2e comment (edited)")
            check.field_equals(edited, "content", "e2e comment (edited)", what="issue.update_comment()")
            check.contains_id(self.api.issue.get_comments(key), comment["id"], what="issue.get_comments()")
            check.is_count(self.api.issue.count_comments(key), what="issue.count_comments()", expected=1)
            self.api.issue.delete_comment(key, comment["id"])
            check.is_count(self.api.issue.count_comments(key), what="issue.count_comments()", expected=0)
            check.is_list(self.api.issue.list_participants(key), what="issue.list_participants()", min_length=1, item_keys=("id",))
        finally:
            self.api.issue.delete(issue["issueKey"])

    def test_recently_viewed_issue(self):
        issue = self._create_issue("viewed")
        try:
            added = self.api.user.add_recently_viewed_issue(issue["issueKey"])
            check.field_equals(added, "id", issue["id"], what="user.add_recently_viewed_issue()")
            viewed = [item["issue"]["id"] for item in self.api.user.list_recently_viewed_issues(count=20)]
            check.is_true(issue["id"] in viewed, "user.list_recently_viewed_issues() does not contain the issue")
        finally:
            self.api.issue.delete(issue["issueKey"])

    def test_shared_file_links(self):
        # Shared files cannot be uploaded through the API: use one that already exists in the project.
        if not self.project.get("useFileSharing"):
            self.skipTest("File sharing is disabled in the project")
        files = [e for e in self.api.project.list_shared_files(PROJECT_KEY, count=100) if e.get("type") == "file"]
        if not files:
            self.skipTest("The project has no shared file in its root directory")
        file_id = files[0]["id"]
        issue = self._create_issue("shared-file")
        try:
            check.is_list(self.api.issue.link_issue_shared_files(issue["issueKey"], [file_id]),
                          what="issue.link_issue_shared_files()", min_length=1)
            check.contains_id(self.api.issue.list_issue_shared_files(issue["issueKey"]), file_id,
                              what="issue.list_issue_shared_files()")
            self.api.issue.unlink_issue_shared_file(issue["issueKey"], file_id)
        finally:
            self.api.issue.delete(issue["issueKey"])

    def test_star(self):
        issue = self._create_issue("star")
        try:
            check.is_true(self.api.star.add(issueId=issue["id"]) is None, "star.add() did not return None")
            stars = self.api.issue.get(issue["issueKey"]).get("stars")
            check.is_list(stars, what="issue.get()['stars']", min_length=1, item_keys=("id",))
            self.api.star.delete(stars[-1]["id"])
            check.is_list(self.api.issue.get(issue["issueKey"]).get("stars"), what="issue.get()['stars']")
        finally:
            self.api.issue.delete(issue["issueKey"])

    def test_related_issues_and_watching(self):
        issue = self._create_issue("issue-a")
        try:
            other = self._create_issue("issue-b")
            try:
                key = issue["issueKey"]
                self.api.issue.add_related_issue(key, other["id"])
                check.contains_id(self.api.issue.list_related_issues(key), other["id"], what="issue.list_related_issues()")
                self.api.issue.remove_related_issue(key, other["id"])
                related = self.api.issue.list_related_issues(key)
                check.is_true(other["id"] not in [i.get("id") for i in related], "the related issue was not removed")

                watching = self.api.watching.add(key, note=resource_name("watching"))
                try:
                    check.field_type(watching, "id", int, what="watching.add()")
                    check.field_equals(self.api.watching.get(watching["id"]), "id", watching["id"], what="watching.get()")
                    note = resource_name("watching-edited")
                    check.field_equals(self.api.watching.update(watching["id"], note), "note", note, what="watching.update()")
                finally:
                    self.api.watching.delete(watching["id"])
            finally:
                self.api.issue.delete(other["issueKey"])
        finally:
            self.api.issue.delete(issue["issueKey"])


@requires_write
class TestWikiRoundTrip(unittest.TestCase):
    def test_wiki_with_attachment(self):
        api = client()
        project = api.project.get(PROJECT_KEY)
        if not project.get("useWiki"):
            self.skipTest("Wiki is disabled in the project")

        name = resource_name("wiki")
        wiki = api.wiki.create(project["id"], name, "created by the e2e test", mailNotify=False)
        try:
            check.field_equals(wiki, "name", name, what="wiki.create()")
            check.has_keys(wiki, "id", "created", what="wiki.create()")
            updated = api.wiki.update(wiki["id"], name, "updated by the e2e test", mailNotify=False)
            check.field_equals(updated, "content", "updated by the e2e test", what="wiki.update()")
            check.field_equals(api.user.add_recently_viewed_wiki(wiki["id"]), "id", wiki["id"], what="user.add_recently_viewed_wiki()")
            if project.get("useFileSharing"):
                files = [e for e in api.project.list_shared_files(PROJECT_KEY, count=100) if e.get("type") == "file"]
                if files:
                    api.wiki.link_shared_files(wiki["id"], [files[0]["id"]])
                    check.contains_id(api.wiki.list_shared_files(wiki["id"]), files[0]["id"], what="wiki.list_shared_files()")
                    api.wiki.unlink_shared_file(wiki["id"], files[0]["id"])
            check.is_list(api.wiki.list_history(wiki["id"]), what="wiki.list_history()", min_length=1, item_keys=("version",))
            check.is_list(api.wiki.list(PROJECT_KEY, keyword=name), what="wiki.list(keyword)", min_length=1)

            data = b"python-backlog e2e attachment\n"
            with tempfile.TemporaryDirectory() as d:
                path = os.path.join(d, resource_name("attachment") + ".txt")
                with open(path, "wb") as f:
                    f.write(data)
                uploaded = api.attachment.upload(path)
            check.field_type(uploaded, "id", int, what="attachment.upload()")

            attached = api.wiki.add_attachment(wiki["id"], uploaded["id"])
            check.is_list(attached, what="wiki.add_attachment()", min_length=1, item_keys=("id",))
            attachment_id = attached[0]["id"]
            check.contains_id(api.wiki.list_attachments(wiki["id"]), attachment_id, what="wiki.list_attachments()")
            downloaded = api.wiki.get_attachment(wiki["id"], attachment_id)
            check.field_equals(downloaded, "data", data, what="wiki.get_attachment()")
            api.wiki.delete_attachment(wiki["id"], attachment_id)
        finally:
            api.wiki.delete(wiki["id"], mailNotify=False)


@requires_write
class TestDocumentRoundTrip(unittest.TestCase):
    def test_document_with_tags(self):
        api = client()
        project = api.project.get(PROJECT_KEY)
        title = resource_name("document")

        document = api.document.add(project["id"], title=title, content="# created by the e2e test")
        try:
            check.field_equals(document, "title", title, what="document.add()")
            check.has_keys(document, "id", "created", what="document.add()")
            check.field_equals(api.document.get(document["id"]), "title", title, what="document.get()")

            tag = resource_name("tag")
            check.is_list(api.document.add_tags(document["id"], [tag]), what="document.add_tags()", item_keys=("id", "name"))
            api.document.remove_tags(document["id"], [tag])
            tags = api.document.get(document["id"]).get("tags") or []
            check.is_true(tag not in [t.get("name") for t in tags], "the tag was not removed")
        finally:
            api.document.delete(document["id"])


@requires_write
class TestCategoryRoundTrip(unittest.TestCase):
    def test_category(self):
        api = client()
        name = resource_name("category")

        category = api.category.add(PROJECT_KEY, name)
        try:
            check.field_equals(category, "name", name, what="category.add()")
            check.field_type(category, "id", int, what="category.add()")
            renamed = resource_name("category-renamed")
            check.field_equals(api.category.update(PROJECT_KEY, category["id"], renamed), "name", renamed, what="category.update()")
            check.contains_id(api.category.list(PROJECT_KEY), category["id"], what="category.list()")
        finally:
            api.category.delete(PROJECT_KEY, category["id"])


@requires_write
class TestVersionAndStatusRoundTrip(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.api = client()

    def test_version(self):
        name = resource_name("version")
        version = self.api.project.add_version(PROJECT_KEY, name, startDate="2026-01-01", releaseDueDate="2026-12-31")
        try:
            check.field_equals(version, "name", name, what="project.add_version()")
            check.field_type(version, "id", int, what="project.add_version()")
            updated = self.api.project.update_version(PROJECT_KEY, version["id"], name, description="e2e", archived=True)
            check.field_equals(updated, "archived", True, what="project.update_version()")
            check.field_equals(updated, "description", "e2e", what="project.update_version()")
            check.contains_id(self.api.project.list_versions(PROJECT_KEY), version["id"], what="project.list_versions()")
        finally:
            self.api.project.delete_version(PROJECT_KEY, version["id"])

    def test_status(self):
        statuses = self.api.project.list_statuses(PROJECT_KEY)
        check.is_list(statuses, what="project.list_statuses()", min_length=1, item_keys=("id",))
        substitute = statuses[0]["id"]
        name = resource_name("status")

        status = self.api.project.add_status(PROJECT_KEY, name, "#3b9dbd")
        try:
            check.field_equals(status, "name", name, what="project.add_status()")
            check.field_type(status, "id", int, what="project.add_status()")
            updated = self.api.project.update_status(PROJECT_KEY, status["id"], color="#393939")
            check.field_equals(updated, "color", "#393939", what="project.update_status()")
            check.contains_id(self.api.project.list_statuses(PROJECT_KEY), status["id"], what="project.list_statuses()")
        finally:
            self.api.project.delete_status(PROJECT_KEY, status["id"], substituteStatusId=substitute)
