# coding: utf-8

import unittest
import httpretty
import json
from backlog.util import load_conf
from backlog.base import BacklogAPI

API_ENDPOINT = "https://{space}.backlog.jp/api/v2/{uri}"


class TestUser(unittest.TestCase):
    def setUp(self):
        self.conf = load_conf("./conf.default.yml")["backlog"]
        self.api = BacklogAPI(self.conf["space"], self.conf["api_key"])
        self.space = self.conf["space"]
        self.api_key = self.conf["api_key"]

    @httpretty.activate
    def test_list(self):
        _uri = "users"

        expects = [
            {
                "id": 1,
                "userId": "admin",
                "name": "admin",
                "roleType": 1,
                "lang": "ja",
                "mailAddress": "eguchi@nulab.example"
            },
        ]

        httpretty.register_uri(
            httpretty.GET,
            API_ENDPOINT.format(space=self.space, uri=_uri),
            body=json.dumps(expects),
            status=200
        )

        resp = self.api.user.list()

        self.assertEqual(expects, resp)

    @httpretty.activate
    def test_get(self):
        _user_id = "1"
        _uri = "users/{user_id}".format(user_id=_user_id)

        expects = {
            "id": _user_id,
            "userId": "admin",
            "name": "admin",
            "roleType": 1,
            "lang": "ja",
            "mailAddress": "eguchi@nulab.example"
        }

        httpretty.register_uri(
            httpretty.GET,
            API_ENDPOINT.format(space=self.space, uri=_uri),
            body=json.dumps(expects),
            status=200
        )

        resp = self.api.user.get(userId=_user_id)

        self.assertEqual(expects, resp)

    @httpretty.activate
    def test_add(self):
        _user_id = "admin"
        _password = "hoge"
        _name = "admin"
        _mail_address = "eguchi@nulab.example"
        _role_type = 1
        _uri = "users"

        expects = {
            "id": 1,
            "userId": _user_id,
            "name": _name,
            "roleType": _role_type,
            "lang": "ja",
            "mailAddress": _mail_address
        }

        httpretty.register_uri(
            httpretty.POST,
            API_ENDPOINT.format(space=self.space, uri=_uri),
            body=json.dumps(expects),
            status=201
        )

        resp = self.api.user.add(
            userId=_user_id,
            password=_password,
            name=_name,
            mailAddress=_mail_address,
            roleType=_role_type
        )

        self.assertEqual(expects, resp)

    @httpretty.activate
    def test_update(self):
        _user_id = "admin"
        _password = "hoge"
        _name = "admin"
        _mail_address = "eguchi@nulab.example"
        _role_type = 1
        _uri = "users/{user_id}".format(user_id=_user_id)

        expects = {
            "id": 1,
            "userId": _user_id,
            "name": _name,
            "roleType": _role_type,
            "lang": "ja",
            "mailAddress": _mail_address
        }

        httpretty.register_uri(
            httpretty.PATCH,
            API_ENDPOINT.format(space=self.space, uri=_uri),
            body=json.dumps(expects),
            status=200
        )

        resp = self.api.user.update(
            userId=_user_id,
            password=_password,
            name=_name,
            mailAddress=_mail_address,
            roleType=_role_type
        )

        self.assertEqual(expects, resp)

    @httpretty.activate
    def test_delete(self):
        _id = "1"
        _uri = "users/{id}".format(id=_id)

        expects = {
            "id": _id,
            "userId": "admin",
            "name": "admin",
            "roleType": 1,
            "lang": "ja",
            "mailAddress": "eguchi@nulab.example"
        }

        httpretty.register_uri(
            httpretty.DELETE,
            API_ENDPOINT.format(space=self.space, uri=_uri),
            body=json.dumps(expects),
            status=200
        )

        resp = self.api.user.delete(id=_id)

        self.assertEqual(expects, resp)

    @httpretty.activate
    def test_get_own(self):
        pass


if __name__ == "__main__":
    unittest.main(warnings='ignore')
