# coding: utf-8

import requests
import os.path


class Attachment(object):
    def __init__(self, api):
        self.api = api

    def upload(self, filename):
        """
        https://developer.nulab-inc.com/ja/docs/backlog/api/2/post-attachment-file/

        :param filename: (str) Required. filename to upload
        :return: Compliant with Backlog API specification
        """
        if not os.path.exists(filename):
            raise FileNotFoundError(filename)

        with open(filename, "rb") as fp:
            _uri = "space/attachment"
            _method = "POST"
            _files = {
                os.path.basename(filename): fp
            }

            resp = self.api.invoke_method(_method, _uri, files=_files)

            return resp.json()
