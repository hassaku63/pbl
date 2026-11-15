# coding: utf-8

from backlog._params import bool_params
from backlog.wiki import _filename_from_response


class Document(object):
    """
    Documents: https://developer.nulab.com/docs/backlog/api/2/get-document-list/

    Document IDs are strings (e.g. "019d46599c2d7e19adfa562d5b9019a6").
    """

    def __init__(self, api) -> None:
        self.api = api

    def list(self, offset=0, projectId=None, keyword=None, sort=None, order=None, count=None):
        """
        https://developer.nulab.com/docs/backlog/api/2/get-document-list/

        :param offset: (int) where to start returning records from, default 0
        :param projectId: (int or list of int) Optional. project ID(s)
        :param keyword: (str) Optional. keyword
        :param sort: (str) Optional. "created" or "updated"
        :param order: (str) Optional. "asc" or "desc", default "desc"
        :param count: (int) Optional. number of records to retrieve (1-100), default 20
        :return: list of documents
        """
        _query_param = {
            "offset": offset,
            "projectId[]": projectId,
            "keyword": keyword,
            "sort": sort,
            "order": order,
            "count": count,
        }

        resp = self.api.invoke_method("GET", "documents", query_param=_query_param)

        return resp.json()

    def count(self, projectIdOrKey):
        """
        https://developer.nulab.com/docs/backlog/api/2/count-document/

        :param projectIdOrKey: project ID or project key
        :return: {"count": int}
        """
        resp = self.api.invoke_method("GET", "documents/count", query_param={"projectIdOrKey": projectIdOrKey})

        return resp.json()

    def tree(self, projectIdOrKey):
        """
        https://developer.nulab.com/docs/backlog/api/2/get-document-tree/

        :param projectIdOrKey: project ID or project key
        :return: the document tree of the project
        """
        resp = self.api.invoke_method("GET", "documents/tree", query_param={"projectIdOrKey": projectIdOrKey})

        return resp.json()

    def get(self, documentId):
        """
        https://developer.nulab.com/docs/backlog/api/2/get-document/

        :param documentId: (str) document ID
        :return: document
        """
        resp = self.api.invoke_method("GET", "documents/{document_id}".format(document_id=documentId))

        return resp.json()

    def add(self, projectId, title=None, content=None, emoji=None, parentId=None, addLast=None):
        """
        https://developer.nulab.com/docs/backlog/api/2/add-document/

        :param projectId: (int) project ID
        :param title: (str) Optional. title
        :param content: (str) Optional. content, parsed as Markdown
        :param emoji: (str) Optional. emoji shown alongside the title
        :param parentId: (str) Optional. ID of the parent document in the tree
        :param addLast: (bool) Optional. add as the last sibling instead of the first
        :return: the added document
        """
        _request_param = bool_params({
            "projectId": projectId,
            "title": title,
            "content": content,
            "emoji": emoji,
            "parentId": parentId,
            "addLast": addLast,
        })

        resp = self.api.invoke_method("POST", "documents", request_param=_request_param)

        return resp.json()

    def delete(self, documentId):
        """
        https://developer.nulab.com/docs/backlog/api/2/delete-document/

        Only administrators and project administrators can delete documents.

        :param documentId: (str) document ID
        :return: the deleted document
        """
        resp = self.api.invoke_method("DELETE", "documents/{document_id}".format(document_id=documentId))

        return resp.json()

    def get_attachment(self, documentId, attachmentId):
        """
        https://developer.nulab.com/docs/backlog/api/2/get-document-attachments/

        :param documentId: (str) document ID
        :param attachmentId: (int) attachment ID
        :return: dict with "id" (attachment ID), "name" (file name, or None if unknown) and "data" (bytes)
        """
        _uri = "documents/{document_id}/attachments/{attachment_id}".format(document_id=documentId, attachment_id=attachmentId)

        resp = self.api.invoke_method("GET", _uri)

        return {
            "id": attachmentId,
            "name": _filename_from_response(resp),
            "data": resp.content,
        }

    def list_comments(self, documentId):
        """
        https://developer.nulab.com/docs/backlog/api/2/get-document-comment/

        :param documentId: (str) document ID
        :return: list of comments
        """
        resp = self.api.invoke_method("GET", "documents/{document_id}/comments".format(document_id=documentId))

        return resp.json()

    def add_tags(self, documentId, tagNames):
        """
        https://developer.nulab.com/docs/backlog/api/2/add-document-tag/

        :param documentId: (str) document ID
        :param tagNames: (str or list of str) tag name(s) to add
        :return: list of tags
        """
        _uri = "documents/{document_id}/tags".format(document_id=documentId)

        resp = self.api.invoke_method("POST", _uri, request_param={"tagNames[]": tagNames})

        return resp.json()

    def remove_tags(self, documentId, tagNames):
        """
        https://developer.nulab.com/docs/backlog/api/2/remove-document-tag/

        :param documentId: (str) document ID
        :param tagNames: (str or list of str) tag name(s) to remove
        :return: the API response
        """
        _uri = "documents/{document_id}/tags".format(document_id=documentId)

        resp = self.api.invoke_method("DELETE", _uri, request_param={"tagNames[]": tagNames})

        return resp.json()
