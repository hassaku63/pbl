# coding: utf-8

from backlog.wiki import _filename_from_response


class Issue(object):
    def __init__(self, api):
        """

        :param api:
        """
        self.api = api

    def list(self, **kwargs):
        """
        https://developer.nulab-inc.com/ja/docs/backlog/api/2/get-issue-list/

        :param kwargs: query parameter
        :return:
        """
        _uri = "issues"
        _method = "GET"

        resp = self.api.invoke_method(_method, _uri, query_param=kwargs)

        return resp.json()

    def count(self, **kwargs):
        """
        https://developer.nulab-inc.com/ja/docs/backlog/api/2/count-issue/

        :param kwargs:
        :return:
        """
        _uri = "issues/count"
        _method = "GET"

        resp = self.api.invoke_method(_method, _uri, query_param=kwargs)

        return resp.json()

    def create(self, **kwargs):
        """
        https://developer.nulab-inc.com/ja/docs/backlog/api/2/add-issue/

        :param kwargs:
        :return:
        """
        _uri = "issues"
        _method = "POST"

        resp = self.api.invoke_method(_method, _uri, request_param=kwargs)

        return resp.json()

    def get(self, issueIdOrKey):
        """
        https://developer.nulab-inc.com/ja/docs/backlog/api/2/get-issue/

        :param issueIdOrKey:
        :return:
        """
        _uri = "issues/{issue_id_or_key}".format(issue_id_or_key=issueIdOrKey)
        _method = "GET"

        resp = self.api.invoke_method(_method, _uri)

        return resp.json()

    def update(self, issueIdOrKey, **kwargs):
        """
        https://developer.nulab-inc.com/ja/docs/backlog/api/2/update-issue/

        :param issueIdOrKey:
        :param kwargs: issue param
        :return:
        """
        _uri = "issues/{issue_id_or_key}".format(issue_id_or_key=issueIdOrKey)
        _method = "PATCH"

        resp = self.api.invoke_method(_method, _uri, request_param=kwargs)

        return resp.json()

    def delete(self, issueIdOrKey):
        """
        https://developer.nulab-inc.com/ja/docs/backlog/api/2/delete-issue/

        :param issueIdOrKey:
        :return:
        """
        _uri = "issues/{issue_id_or_key}".format(issue_id_or_key=issueIdOrKey)
        _method = "DELETE"

        resp = self.api.invoke_method(_method, _uri)

        return resp.json()

    def get_comments(self, issueIdOrKey, minId=None, maxId=None, count=None, order=None):
        """
        https://developer.nulab.com/docs/backlog/api/2/get-comment-list/

        :param issueIdOrKey: Issue ID or Issue Key
        :param minId: (int) Optional. minimum comment ID
        :param maxId: (int) Optional. maximum comment ID
        :param count: (int) Optional. number of records to retrieve (1-100), default 20
        :param order: (str) Optional. "asc" or "desc", default "desc"
        :return: list of comments
        """
        _uri = "issues/{issue_id_or_key}/comments".format(issue_id_or_key=issueIdOrKey)
        _query_param = {"minId": minId, "maxId": maxId, "count": count, "order": order}

        resp = self.api.invoke_method("GET", _uri, query_param=_query_param)

        return resp.json()

    def add_comment(self, issueIdOrKey, content, notifiedUserId=None, attachmentId=None):
        """
        https://developer.nulab-inc.com/ja/docs/backlog/api/2/add-comment/

        :param issueIdOrKey:
        :param content:
        :param notifiedUserId:
        :param attachmentId:
        :return:
        """
        _uri = "issues/{issue_id_or_key}/comments".format(issue_id_or_key=issueIdOrKey)
        _method = "POST"
        _data = {
            "content": content
        }
        if notifiedUserId is not None:
            _data.update([("notifiedUserId[]", notifiedUserId)])
        if attachmentId is not None:
            _data.update([("attachmentId[]", attachmentId)])

        resp = self.api.invoke_method(_method, _uri, request_param=_data)

        return resp.json()

    def count_comments(self, issueIdOrKey):
        """
        https://developer.nulab.com/docs/backlog/api/2/count-comment/

        :param issueIdOrKey: Issue ID or Issue Key
        :return: {"count": int}
        """
        _uri = "issues/{issue_id_or_key}/comments/count".format(issue_id_or_key=issueIdOrKey)

        resp = self.api.invoke_method("GET", _uri)

        return resp.json()

    def get_comment(self, issueIdOrKey, commentId):
        """
        https://developer.nulab.com/docs/backlog/api/2/get-comment/

        :param issueIdOrKey: Issue ID or Issue Key
        :param commentId: (int) Comment ID
        :return: comment
        """
        resp = self.api.invoke_method("GET", self._comment_uri(issueIdOrKey, commentId))

        return resp.json()

    def update_comment(self, issueIdOrKey, commentId, content):
        """
        https://developer.nulab.com/docs/backlog/api/2/update-comment/

        :param issueIdOrKey: Issue ID or Issue Key
        :param commentId: (int) Comment ID
        :param content: (str) new content. Mention notation is available.
        :return: updated comment
        """
        resp = self.api.invoke_method("PATCH", self._comment_uri(issueIdOrKey, commentId), request_param={"content": content})

        return resp.json()

    def delete_comment(self, issueIdOrKey, commentId):
        """
        https://developer.nulab.com/docs/backlog/api/2/delete-comment/

        :param issueIdOrKey: Issue ID or Issue Key
        :param commentId: (int) Comment ID
        :return: deleted comment
        """
        resp = self.api.invoke_method("DELETE", self._comment_uri(issueIdOrKey, commentId))

        return resp.json()

    def get_comment_notifications(self, issueIdOrKey, commentId):
        """
        https://developer.nulab.com/docs/backlog/api/2/get-list-of-comment-notifications/

        :param issueIdOrKey: Issue ID or Issue Key
        :param commentId: (int) Comment ID
        :return: list of notifications
        """
        resp = self.api.invoke_method("GET", self._comment_uri(issueIdOrKey, commentId) + "/notifications")

        return resp.json()

    def add_comment_notification(self, issueIdOrKey, commentId, notifiedUserId):
        """
        https://developer.nulab.com/docs/backlog/api/2/add-comment-notification/

        :param issueIdOrKey: Issue ID or Issue Key
        :param commentId: (int) Comment ID
        :param notifiedUserId: (int or list of int) user ID(s) to notify
        :return: comment
        """
        resp = self.api.invoke_method(
            "POST",
            self._comment_uri(issueIdOrKey, commentId) + "/notifications",
            request_param={"notifiedUserId[]": notifiedUserId},
        )

        return resp.json()

    def list_issue_attachments(self, issueIdOrKey):
        """
        https://developer.nulab.com/docs/backlog/api/2/get-list-of-issue-attachments/

        :param issueIdOrKey: Issue ID or Issue Key
        :return: list of attachments
        """
        _uri = "issues/{issue_id_or_key}/attachments".format(issue_id_or_key=issueIdOrKey)

        resp = self.api.invoke_method("GET", _uri)

        return resp.json()

    def get_issue_attachment(self, issueIdOrKey, attachmentId):
        """
        https://developer.nulab.com/docs/backlog/api/2/get-issue-attachment/

        :param issueIdOrKey: Issue ID or Issue Key
        :param attachmentId: (int) Attachment file ID
        :return: dict with "id" (attachment ID), "name" (file name, or None if unknown) and "data" (bytes)
        """
        _uri = "issues/{issue_id_or_key}/attachments/{attachment_id}".format(issue_id_or_key=issueIdOrKey, attachment_id=attachmentId)

        resp = self.api.invoke_method("GET", _uri)

        return {
            "id": attachmentId,
            "name": _filename_from_response(resp),
            "data": resp.content,
        }

    # Kept for backward compatibility with the original (plural) name.
    get_issue_attachments = get_issue_attachment

    def delete_issue_attachment(self, issueIdOrKey, attachmentId):
        """
        https://developer.nulab.com/docs/backlog/api/2/delete-issue-attachment/

        :param issueIdOrKey: Issue ID or Issue Key
        :param attachmentId: (int) Attachment file ID
        :return: deleted attachment
        """
        _uri = "issues/{issue_id_or_key}/attachments/{attachment_id}".format(issue_id_or_key=issueIdOrKey, attachment_id=attachmentId)

        resp = self.api.invoke_method("DELETE", _uri)

        return resp.json()

    def list_issue_shared_files(self, issueIdOrKey):
        """
        https://developer.nulab.com/docs/backlog/api/2/get-list-of-linked-shared-files/

        :param issueIdOrKey: Issue ID or Issue Key
        :return: list of shared files
        """
        _uri = "issues/{issue_id_or_key}/sharedFiles".format(issue_id_or_key=issueIdOrKey)

        resp = self.api.invoke_method("GET", _uri)

        return resp.json()

    def link_issue_shared_files(self, issueIdOrKey, fileId):
        """
        https://developer.nulab.com/docs/backlog/api/2/link-shared-files-to-issue/

        :param issueIdOrKey: Issue ID or Issue Key
        :param fileId: (int or list of int) shared file ID(s)
        :return: list of linked shared files
        """
        _uri = "issues/{issue_id_or_key}/sharedFiles".format(issue_id_or_key=issueIdOrKey)

        resp = self.api.invoke_method("POST", _uri, request_param={"fileId[]": fileId})

        return resp.json()

    def unlink_issue_shared_file(self, issueIdOrKey, id):
        """
        https://developer.nulab.com/docs/backlog/api/2/remove-link-to-shared-file-from-issue/

        :param issueIdOrKey: Issue ID or Issue Key
        :param id: (int) shared file ID
        :return: the unlinked shared file
        """
        _uri = "issues/{issue_id_or_key}/sharedFiles/{id}".format(issue_id_or_key=issueIdOrKey, id=id)

        resp = self.api.invoke_method("DELETE", _uri)

        return resp.json()

    def list_participants(self, issueIdOrKey):
        """
        https://developer.nulab.com/docs/backlog/api/2/get-issue-participant-list/

        :param issueIdOrKey: Issue ID or Issue Key
        :return: list of users participating in the issue
        """
        _uri = "issues/{issue_id_or_key}/participants".format(issue_id_or_key=issueIdOrKey)

        resp = self.api.invoke_method("GET", _uri)

        return resp.json()

    def list_related_issues(self, issueIdOrKey):
        """
        https://developer.nulab.com/docs/backlog/api/2/get-list-of-related-issues/

        :param issueIdOrKey: Issue ID or Issue Key
        :return: list of related issues; each has a "type" field (currently always "RELATES")
        """
        _uri = "issues/{issue_id_or_key}/relatedIssues".format(issue_id_or_key=issueIdOrKey)

        resp = self.api.invoke_method("GET", _uri)

        return resp.json()

    def add_related_issue(self, issueIdOrKey, targetIssueId):
        """
        https://developer.nulab.com/docs/backlog/api/2/add-related-issue/

        Up to 50 related issues can be added per issue. Adding an existing relation is not an error.

        :param issueIdOrKey: Issue ID or Issue Key
        :param targetIssueId: (int) ID of the issue to relate
        :return: the issue
        """
        _uri = "issues/{issue_id_or_key}/relatedIssues".format(issue_id_or_key=issueIdOrKey)

        resp = self.api.invoke_method("POST", _uri, request_param={"targetIssueId": targetIssueId})

        return resp.json()

    def remove_related_issue(self, issueIdOrKey, relatedIssueId):
        """
        https://developer.nulab.com/docs/backlog/api/2/remove-related-issue/

        :param issueIdOrKey: Issue ID or Issue Key
        :param relatedIssueId: (int) ID of the related issue to remove
        :return: the issue
        """
        _uri = "issues/{issue_id_or_key}/relatedIssues/{related_issue_id}".format(
            issue_id_or_key=issueIdOrKey, related_issue_id=relatedIssueId
        )

        resp = self.api.invoke_method("DELETE", _uri)

        return resp.json()

    @staticmethod
    def _comment_uri(issueIdOrKey, commentId):
        return "issues/{issue_id_or_key}/comments/{comment_id}".format(issue_id_or_key=issueIdOrKey, comment_id=commentId)
