# coding: utf-8

import unittest
import httpretty
import json
from backlog.util import load_conf
from backlog.base import BacklogAPI

API_ENDPOINT = "https://{space}.backlog.jp/api/v2/{uri}"


class TestAttachment(unittest.TestCase):
    def setUp(self):
        self.conf = load_conf("./conf.default.yml")["backlog"]
        self.api = BacklogAPI(self.conf["space"], self.conf["api_key"])
        self.space = self.conf["space"]
        self.api_key = self.conf["api_key"]

    def test_upload_attachment(self):
        pass


if __name__ == "__main__":
    unittest.main(warnings='ignore')
