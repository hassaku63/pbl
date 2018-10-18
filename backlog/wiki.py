# coding: utf-8

import os.path


class Wiki(object):
    def __init__(self, api):
        """

        :param api:
        """
        self.api = api

    def list(self, projectIdOrKey):
        """

        :param projectIdOrKey:
        :return:
        """
        _uri = "wikis"
        _method = "GET"

        resp = self.api.invoke_method(_method, _uri, query_param=dict(projectIdOrKey=projectIdOrKey))

        return resp.json()

    def create(self, projectId, name, content, mailNotify):
        """
        https://developer.nulab-inc.com/ja/docs/backlog/api/2/add-wiki-page/

        :param projectId: int: project id
        :param name: str: wiki page name
        :param content: str: page content
        :param mailNotify: bool: notification
        :return:
        """
        _uri = "wikis"
        _method = "POST"
        _request_param = {
            "projectId": projectId,
            "name": name,
            "content": content,
            "mailNotify": "true" if mailNotify else "false"
        }

        resp = self.api.invoke_method(_method, _uri, request_param=_request_param)

        return resp.json()

    def get(self, wikiId):
        """
        https://developer.nulab-inc.com/ja/docs/backlog/api/2/get-wiki-page/

        :param wikiId:
        :return:
        """
        _uri = "wikis/{wiki_id}".format(wiki_id=wikiId)
        _method = "GET"
        resp = self.api.invoke_method(_method, _uri)

        return resp.json()

    def update(self, wikiId, name, content, mailNotify=False):
        """
        https://developer.nulab-inc.com/ja/docs/backlog/api/2/update-wiki-page/

        :param wikiId:
        :param name:
        :param content:
        :param mailNotify:
        :return:
        """
        _uri = "wikis/{wiki_id}".format(wiki_id=wikiId)
        _method = "PATCH"
        _request_param = {
            "name": name,
            "content": content,
            "mainNotify": "true" if mailNotify else "false"
        }

        resp = self.api.invoke_method(_method, _uri, request_param=_request_param)

        return resp.json()

    def delete(self, wikiId, mailNotify=False):
        """
        https://developer.nulab-inc.com/ja/docs/backlog/api/2/delete-wiki-page/

        :param wikiId:
        :param mailNotify:
        :return:
        """
        _uri = "wikis/{wiki_id}".format(wiki_id=wikiId)
        _method = "DELETE"
        _mail_notify = mailNotify
        _request_param = {
            "mailNotify": "true" if _mail_notify else "false"
        }

        resp = self.api.invoke_method(_method, _uri, request_param=_request_param)

        return resp.json()

    def list_attachments(self, wikiId):
        """
        https://developer.nulab-inc.com/ja/docs/backlog/api/2/get-list-of-wiki-attachments/

        :param wikiId:
        :return:
        """
        _uri = "wikis/{wiki_id}/attachments".format(wiki_id=wikiId)
        _method = "GET"

        resp = self.api.invoke_method(_method, _uri)

        return resp.json()

    def add_attachment(self, wikiId, attachmentId):
        """
        https://developer.nulab-inc.com/ja/docs/backlog/api/2/attach-file-to-wiki/

        :param wikiId:
        :param attachmentId:
        :return:
        """
        _uri = "wikis/{wiki_id}/attachments".format(wiki_id=wikiId)
        _method = "POST"
        _request_param = {
            "attachmentId": attachmentId
        }

        resp = self.api.invoke_method(_method, _uri, request_param=_request_param)

        return resp.json()

    def get_attachment(self, wikiId, attachmentId):
        """
        https://developer.nulab-inc.com/ja/docs/backlog/api/2/get-wiki-page-attachment

        :param wikiId:
        :param attachmentId:
        :return: bytes object. NOT json.
        """
        _uri = "wikis/{wiki_id}/attachments/{attachment_id}".format(wiki_id=wikiId, attachment_id=attachmentId)
        _method = "GET"

        resp = self.api.invoke_method(_method, _uri)

        return {
            "id": attachmentId,
            "name": "test",
            "data": resp.content
        }

    def delete_attachment(self, wikiId, attachmentId):
        """
        https://developer.nulab-inc.com/ja/docs/backlog/api/2/remove-wiki-attachment/

        :param wikiId:
        :param attachmentId:
        :return:
        """
        _uri = "wikis/{wiki_id}/attachments/{attachment_id}".format(
            wiki_id=wikiId,
            attachment_id=attachmentId
        )
        _method = "DELETE"

        resp = self.api.invoke_method(_method, _uri)

        return resp.json()