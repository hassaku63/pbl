# coding: utf-8

import os.path
import mimetypes


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

        _uri = "space/attachment"
        _method = "POST"
        _files = {
            'file': (os.path.basename(filename), open(filename, 'rb'), mimetypes.guess_type(filename))
        }

        resp = self.api.invoke_method(_method, _uri, files=_files)

        return resp.json()
