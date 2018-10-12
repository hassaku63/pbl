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

    def create(self, projectId, name, content, mailNotify=False):
        """
        https://developer.nulab-inc.com/ja/docs/backlog/api/2/add-wiki-page/

        :param projectId:
        :param name:
        :param content:
        :param mailNotify:
        :return:
        """
        raise NotImplementedError

    def get(self, wikiId):
        """
        https://developer.nulab-inc.com/ja/docs/backlog/api/2/get-wiki-page/

        :param wikiId:
        :return:
        """
        raise NotImplementedError

    def update(self, wikiId, name, content, mailNotify=False):
        """
        https://developer.nulab-inc.com/ja/docs/backlog/api/2/update-wiki-page/

        :param wikiId:
        :param name:
        :param content:
        :param mailNotify:
        :return:
        """
        raise NotImplementedError

    def delete(self, wikiId, mailNotify=False):
        """
        https://developer.nulab-inc.com/ja/docs/backlog/api/2/delete-wiki-page/

        :param wikiId:
        :param mailNotify:
        :return:
        """
        raise NotImplementedError


    def list_attachments(self, wikiId):
        """
        https://developer.nulab-inc.com/ja/docs/backlog/api/2/get-list-of-wiki-attachments/

        :param wikiId:
        :return:
        """
        raise NotImplementedError

    def add_attachment(self, wikiId, attachmentId):
        """
        https://developer.nulab-inc.com/ja/docs/backlog/api/2/attach-file-to-wiki/

        :param wikiId:
        :param attachmentId:
        :return:
        """
        raise NotImplementedError

    def get_attachment(self, wikiId, attachmentId):
        """

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
        raise NotImplementedError
