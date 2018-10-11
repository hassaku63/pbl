# coding: utf-8

import requests
import os.path

class Attachment(object):
    """
    tes
    """
    def __init__(self, api):
        self.api = api

    def upload(self, filename):
        """
        https://developer.nulab-inc.com/ja/docs/backlog/api/2/post-attachment-file/

        :param filename:
        :return: dict object has keys id, name, size
        """
        if os.path.exists(filename):
            raise FileNotFoundError(filename)

            # api.invoke("POST", )
