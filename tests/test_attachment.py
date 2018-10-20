# coding: utf-8

import unittest
import httpretty
import json
import os
import tempfile
import shutil
from backlog.util import load_conf
from backlog.base import BacklogAPI

API_ENDPOINT = "https://{space}.backlog.jp/api/v2/{uri}"


class TestAttachment(unittest.TestCase):
    def setUp(self):
        self.conf = load_conf("./conf.default.yml")["backlog"]
        self.api = BacklogAPI(self.conf["space"], self.conf["api_key"])
        self.space = self.conf["space"]
        self.api_key = self.conf["api_key"]

        # tempfile
        self.test_dir = tempfile.mkdtemp()
        self.test_fd, self.test_file = tempfile.mkstemp(dir=self.test_dir)
        self.test_data = b"1234567890"

        with open(self.test_fd, "wb") as fp:
            fp.write(self.test_data)

    @httpretty.activate
    def test_upload_attachment(self):
        _uri = "space/attachment"
        _filename = os.path.basename(self.test_file)
        expects = {
            "id": 1,
            "name": _filename,
            "size": 8857
        }
        httpretty.register_uri(
            httpretty.POST,
            API_ENDPOINT.format(space=self.space, uri=_uri),
            body=json.dumps(expects)
        )

        # test
        resp = self.api.attachment.upload(filename=self.test_file)
        self.assertTrue(expects, resp)

    @httpretty.activate
    def test_upload_attachment_file_not_found(self):
        _uri = "space/attachment"
        _filename = "not_exist_file.txt"

        with self.assertRaises(FileNotFoundError):
            resp = self.api.attachment.upload(filename=_filename)


if __name__ == "__main__":
    unittest.main(warnings='ignore')
