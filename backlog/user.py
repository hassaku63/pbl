# coding: utf-8


class User(object):
    def __init__(self, api):
        """

        :param api:
        """
        self.api = api

    def list(self):
        """
        https://developer.nulab.com/ja/docs/backlog/api/2/get-user-list/

        :return: Compliant with Backlog API specification
        """
        _uri = "users"
        _method = "GET"

        resp = self.api.invoke_method(_method, _uri)

        return resp.json()

    def get(self, userId):
        """
        https://developer.nulab.com/ja/docs/backlog/api/2/get-user/

        :param userId: (str or int) Required.
        :return: Compliant with Backlog API specification
        """
        _uri = "users/{user_id}".format(user_id=userId)
        _method = "GET"

        resp = self.api.invoke_method(_method, _uri)

        return resp.json()

    def add(self, userId, password, name, mailAddress, roleType):
        """
        https://developer.nulab.com/ja/docs/backlog/api/2/add-user/

        :param userId: (str) Required.
        :param password: (str) Required.
        :param name: (str) Required.
        :param mailAddress: (str) Required.
        :param roleType: (int) Required. administrator=1, general-user=2, reporter=3, viewer=4, guest-reporter=5, guest-viewer=6
        :return: Compliant with Backlog API specification
        """
        _uri = "users"
        _method = "POST"
        params = dict(
            userId=userId,
            passowrd=password,
            name=name,
            mailAddress=mailAddress,
            roleType=roleType
        )

        resp = self.api.invoke_method(_method, _uri, request_param=params)

        return resp.json()

    def update(self, userId, password, name, mailAddress, roleType):
        """
        https://developer.nulab.com/ja/docs/backlog/api/2/update-user/

        :param userId: (str) Required.
        :param password: (str) Optional.
        :param name: (str) Optional.
        :param mailAddress: (str) Optional.
        :param roleType: (str) Optional.
        :return: Compliant with Backlog API specification
        """
        _uri = "users/{user_id}".format(user_id=userId)
        _method = "PATCH"
        params = dict(
            userId=userId,
            passowrd=password,
            name=name,
            mailAddress=mailAddress,
            roleType=roleType
        )

        resp = self.api.invoke_method(_method, _uri, request_param=params)

        return resp.json()

    def delete(self, id):
        """
        https://developer.nulab.com/ja/docs/backlog/api/2/delete-user/

        :param id: (int) Required.
        :return: Compliant with Backlog API specification
        """
        _uri = "users/{id}".format(id=id)
        _method = "DELETE"

        resp = self.api.invoke_method(_method, _uri)

        return resp.json()
