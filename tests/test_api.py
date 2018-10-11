# coding: utf-8

import unittest
from backlog.util import load_conf
from backlog.base import BacklogAPI

class TestApi(unittest.TestCase):
    def setUp(self):
        self.conf = load_conf("./conf.yml")["backlog"]
        self.api = BacklogAPI(self.conf["space"], self.conf["api_key"])

    def test_invoke_get(self):
        resp = self.api.invoke_method("GET", "wikis", query_param=dict(projectIdOrKey=self.conf["default_project"]))
        resp = resp.json()
        self.assertTrue(type(resp), list)
        self.assertTrue("id" in resp[0].keys())

if __name__ == "__main__":
    unittest.main()