# coding: utf-8

from backlog.pagination import iterate_by_offset
from backlog.wiki import _filename_from_response


class Git(object):
    def __init__(self, api):
        """

        :param api:
        """
        self.api = api

    def list_git_repositories(self, projectIdOrKey):
        """
        https://developer.nulab-inc.com/ja/docs/backlog/api/2/get-list-of-git-repositories/

        :param projectIdOrKey: (str or int) Required
        :return:
        """
        _uri = "projects/{projectIdOrKey}/git/repositories".format(
            projectIdOrKey=projectIdOrKey
        )
        _method = "GET"

        resp = self.api.invoke_method(_method, _uri)

        return resp.json()

    def add_pull_request(self, projectIdOrKey, repoIdOrName, **kwargs):
        """
        https://developer.nulab-inc.com/ja/docs/backlog/api/2/add-pull-request/

        :param projectIdOrKey: (str or int) Requied.
        :param repoIdOrName: (str or int) Requied.
        :param kwargs: (dict) Optional. Other request parameter, compliant with Backlog API specification
        :return: Compliant with Backlog API specification
        """
        _uri = "projects/{projectIdOrKey}/git/repositories/{repoIdOrName}/pullRequests".format(
            projectIdOrKey=projectIdOrKey,
            repoIdOrName=repoIdOrName
        )
        _method = "POST"

        resp = self.api.invoke_method(_method, _uri, request_param=kwargs)

        return resp.json()

    def add_pull_request_comment(self, projectIdOrKey, repoIdOrName, number, content, notifiedUserIds=None):
        """
        https://developer.nulab-inc.com/ja/docs/backlog/api/2/add-pull-request-comment/

        :param projectIdOrKey: (str or int) Required.
        :param repoIdOrName: (str or int) Required.
        :param number: (str or int) Required. PR number
        :param content: (str) Required. comment string
        :param notifiedUserIds: (int or list of int) Optional.
        :return:
        """
        param = {
            "content": content,
            "notifiedUserId[]": notifiedUserIds if notifiedUserIds is not None else []
        }
        _uri = "projects/{projectIdOrKey}/git/repositories/{repoIdOrName}/pullRequests/{number}/comments".format(
            projectIdOrKey=projectIdOrKey,
            repoIdOrName=repoIdOrName,
            number=number
        )
        _method = "POST"

        resp = self.api.invoke_method(_method, _uri, request_param=param)

        return resp.json()

    def list_pull_requests(self, projectIdOrKey, repoIdOrName, **kwargs):
        """

        https://developer.nulab.com/ja/docs/backlog/api/2/get-pull-request-list/

        :param projectIdOrKey: (str or int) Required
        :param repoIdOrName: (str or int) Required
        :param kwargs: Optional. Query Parameters
        :return: Compliant with Backlog API specification
        """
        _uri = "projects/{projectIdOrKey}/git/repositories/{repoIdOrName}/pullRequests".format(
            projectIdOrKey=projectIdOrKey,
            repoIdOrName=repoIdOrName
        )
        _method = "GET"

        resp = self.api.invoke_method(_method, _uri, query_param=kwargs)

        return resp.json()

    def iter_pull_requests(self, projectIdOrKey, repoIdOrName, count=100, **kwargs):
        """
        Iterate over all pull requests of a repository that match the filters (offset/count paging).

        :param kwargs: filters as for list_pull_requests()
        :return: iterator of pull requests
        """
        return iterate_by_offset(self.list_pull_requests, projectIdOrKey, repoIdOrName, count=count, **kwargs)

    def get_git_repository(self, projectIdOrKey, repoIdOrName):
        """
        https://developer.nulab.com/docs/backlog/api/2/get-git-repository/

        :param projectIdOrKey: (str or int) Required.
        :param repoIdOrName: (str or int) Required.
        :return: Git repository
        """
        _uri = "projects/{projectIdOrKey}/git/repositories/{repoIdOrName}".format(
            projectIdOrKey=projectIdOrKey,
            repoIdOrName=repoIdOrName
        )

        resp = self.api.invoke_method("GET", _uri)

        return resp.json()

    def get_pull_request(self, projectIdOrKey, repoIdOrName, number):
        """
        https://developer.nulab.com/docs/backlog/api/2/get-pull-request/

        :param projectIdOrKey: (str or int) Required.
        :param repoIdOrName: (str or int) Required.
        :param number: (int) Required. pull request number
        :return: pull request
        """
        resp = self.api.invoke_method("GET", self._pull_request_uri(projectIdOrKey, repoIdOrName, number))

        return resp.json()

    def update_pull_request(self, projectIdOrKey, repoIdOrName, number, **kwargs):
        """
        https://developer.nulab.com/docs/backlog/api/2/update-pull-request/

        :param projectIdOrKey: (str or int) Required.
        :param repoIdOrName: (str or int) Required.
        :param number: (int) Required. pull request number
        :param kwargs: form parameters: summary, description, issueId, assigneeId, comment,
            and **{"notifiedUserId[]": [...]}
        :return: updated pull request
        """
        resp = self.api.invoke_method("PATCH", self._pull_request_uri(projectIdOrKey, repoIdOrName, number), request_param=kwargs)

        return resp.json()

    def count_pull_requests(self, projectIdOrKey, repoIdOrName, **kwargs):
        """
        https://developer.nulab.com/docs/backlog/api/2/get-number-of-pull-requests/

        :param projectIdOrKey: (str or int) Required.
        :param repoIdOrName: (str or int) Required.
        :param kwargs: query parameters, e.g. **{"statusId[]": [1], "assigneeId[]": [2]}
        :return: {"count": int}
        """
        _uri = "projects/{projectIdOrKey}/git/repositories/{repoIdOrName}/pullRequests/count".format(
            projectIdOrKey=projectIdOrKey,
            repoIdOrName=repoIdOrName
        )

        resp = self.api.invoke_method("GET", _uri, query_param=kwargs)

        return resp.json()

    def list_pull_request_comments(self, projectIdOrKey, repoIdOrName, number, minId=None, maxId=None, count=None, order=None):
        """
        https://developer.nulab.com/docs/backlog/api/2/get-pull-request-comment/

        :param projectIdOrKey: (str or int) Required.
        :param repoIdOrName: (str or int) Required.
        :param number: (int) Required. pull request number
        :param minId: (int) Optional. minimum comment ID
        :param maxId: (int) Optional. maximum comment ID
        :param count: (int) Optional. number of records to retrieve (1-100), default 20
        :param order: (str) Optional. "asc" or "desc", default "desc"
        :return: list of comments
        """
        _query_param = {"minId": minId, "maxId": maxId, "count": count, "order": order}

        resp = self.api.invoke_method(
            "GET", self._pull_request_uri(projectIdOrKey, repoIdOrName, number) + "/comments", query_param=_query_param
        )

        return resp.json()

    def count_pull_request_comments(self, projectIdOrKey, repoIdOrName, number):
        """
        https://developer.nulab.com/docs/backlog/api/2/get-number-of-pull-request-comments/

        :param projectIdOrKey: (str or int) Required.
        :param repoIdOrName: (str or int) Required.
        :param number: (int) Required. pull request number
        :return: {"count": int}
        """
        resp = self.api.invoke_method("GET", self._pull_request_uri(projectIdOrKey, repoIdOrName, number) + "/comments/count")

        return resp.json()

    def update_pull_request_comment(self, projectIdOrKey, repoIdOrName, number, commentId, content):
        """
        https://developer.nulab.com/docs/backlog/api/2/update-pull-request-comment-information/

        Only the author of a comment can update it.

        :param projectIdOrKey: (str or int) Required.
        :param repoIdOrName: (str or int) Required.
        :param number: (int) Required. pull request number
        :param commentId: (int) Required. comment ID
        :param content: (str) Required. new comment body
        :return: updated comment
        """
        resp = self.api.invoke_method(
            "PATCH",
            self._pull_request_uri(projectIdOrKey, repoIdOrName, number) + "/comments/{}".format(commentId),
            request_param={"content": content},
        )

        return resp.json()

    def list_pull_request_attachments(self, projectIdOrKey, repoIdOrName, number):
        """
        https://developer.nulab.com/docs/backlog/api/2/get-list-of-pull-request-attachment/

        :param projectIdOrKey: (str or int) Required.
        :param repoIdOrName: (str or int) Required.
        :param number: (int) Required. pull request number
        :return: list of attachments
        """
        resp = self.api.invoke_method("GET", self._pull_request_uri(projectIdOrKey, repoIdOrName, number) + "/attachments")

        return resp.json()

    def get_pull_request_attachment(self, projectIdOrKey, repoIdOrName, number, attachmentId):
        """
        https://developer.nulab.com/docs/backlog/api/2/download-pull-request-attachment/

        :param projectIdOrKey: (str or int) Required.
        :param repoIdOrName: (str or int) Required.
        :param number: (int) Required. pull request number
        :param attachmentId: (int) Required. attachment ID
        :return: dict with "id" (attachment ID), "name" (file name, or None if unknown) and "data" (bytes)
        """
        resp = self.api.invoke_method(
            "GET", self._pull_request_uri(projectIdOrKey, repoIdOrName, number) + "/attachments/{}".format(attachmentId)
        )

        return {
            "id": attachmentId,
            "name": _filename_from_response(resp),
            "data": resp.content,
        }

    def delete_pull_request_attachment(self, projectIdOrKey, repoIdOrName, number, attachmentId):
        """
        https://developer.nulab.com/docs/backlog/api/2/delete-pull-request-attachments/

        :param projectIdOrKey: (str or int) Required.
        :param repoIdOrName: (str or int) Required.
        :param number: (int) Required. pull request number
        :param attachmentId: (int) Required. attachment ID
        :return: deleted attachment
        """
        resp = self.api.invoke_method(
            "DELETE", self._pull_request_uri(projectIdOrKey, repoIdOrName, number) + "/attachments/{}".format(attachmentId)
        )

        return resp.json()

    @staticmethod
    def _pull_request_uri(projectIdOrKey, repoIdOrName, number):
        return "projects/{projectIdOrKey}/git/repositories/{repoIdOrName}/pullRequests/{number}".format(
            projectIdOrKey=projectIdOrKey,
            repoIdOrName=repoIdOrName,
            number=number
        )
