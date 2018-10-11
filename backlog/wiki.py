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

    def get_wiki_attachment(self, wikiId, attachmentId):
        _uri = "wikis/{wiki_id}/attachments/{attachment_id}".format(wiki_id=wikiId, attachment_id=attachmentId)
        _method = "GET"

        resp = self.api.invoke_method(_method, _uri)

        return {
            os.path.basename(resp.content): resp.content
        }


