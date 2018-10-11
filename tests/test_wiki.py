# coding: utf-8

import unittest
from backlog.util import load_conf
from backlog.base import BacklogAPI


class TestWiki(unittest.TestCase):
    def setUp(self):
        self.conf = load_conf("./conf.yml")["backlog"]
        self.api = BacklogAPI(self.conf["space"], self.conf["api_key"])

    def test_list_wiki(self):
        wikis = self.api.wiki.list(projectIdOrKey=self.conf["default_project"])
        self.assertTrue(type(wikis) == list)
        print(wikis[0])

    def test_create_wiki(self):
        self.fail("not implemented")

    def test_get_wiki(self):
        self.fail("not implemented")

    def test_update_wiki(self):
        self.fail("not implemented")

    def test_delete_wiki(self):
        self.fail("not implemented")

    def test_get_attachment(self):
        self.fail("not implemented")

    def test_add_attachment(self):
        self.fail("not implemented")

    def test_get_attachment(self):
        wikis = self.api.wiki.list(projectIdOrKey=self.conf["default_project"])
        wiki = [ w for w in wikis if len(w["attachments"]) > 0 ][0]
        attachment = self.api.wiki.get_wiki_attachment(
            wikiId=wiki["id"],
            attachmentId=wiki["attachments"][0]["id"]
        )

        self.assertTrue(isinstance(attachment, dict))

    def test_delete_attachment(self):
        self.fail("not implemented")
