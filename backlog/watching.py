# coding: utf-8

from backlog._params import bool_params


class Watching(object):
    """
    Watching issues: https://developer.nulab.com/docs/backlog/api/2/get-watching-list/
    """

    def __init__(self, api) -> None:
        self.api = api

    def list(self, userId, **kwargs):
        """
        https://developer.nulab.com/docs/backlog/api/2/get-watching-list/

        :param userId: (int) user ID (see User.get_myself() for your own ID)
        :param kwargs: query parameters: order, sort ("created", "updated" or "issueUpdated"), count, offset,
            resourceAlreadyRead (bool), and **{"issueId[]": [...]}
        :return: list of watchings
        """
        _uri = "users/{user_id}/watchings".format(user_id=userId)

        resp = self.api.invoke_method("GET", _uri, query_param=bool_params(kwargs))

        return resp.json()

    def count(self, userId, resourceAlreadyRead=None, alreadyRead=None):
        """
        https://developer.nulab.com/docs/backlog/api/2/count-watching/

        :param userId: (int) user ID
        :param resourceAlreadyRead: (bool) Optional. count read (True) or unread (False) watched issues
        :param alreadyRead: (bool) Optional. count watchings read (True) or unread (False) since the user last checked.
            Takes precedence over resourceAlreadyRead.
        :return: {"count": int}
        """
        _uri = "users/{user_id}/watchings/count".format(user_id=userId)
        _query_param = bool_params({"resourceAlreadyRead": resourceAlreadyRead, "alreadyRead": alreadyRead})

        resp = self.api.invoke_method("GET", _uri, query_param=_query_param)

        return resp.json()

    def get(self, watchingId):
        """
        https://developer.nulab.com/docs/backlog/api/2/get-watching/

        :param watchingId: (int) watching ID
        :return: watching
        """
        resp = self.api.invoke_method("GET", "watchings/{watching_id}".format(watching_id=watchingId))

        return resp.json()

    def add(self, issueIdOrKey, note=None):
        """
        https://developer.nulab.com/docs/backlog/api/2/add-watching/

        :param issueIdOrKey: issue ID or issue key to watch
        :param note: (str) Optional. note
        :return: the added watching
        """
        resp = self.api.invoke_method("POST", "watchings", request_param={"issueIdOrKey": issueIdOrKey, "note": note})

        return resp.json()

    def update(self, watchingId, note):
        """
        https://developer.nulab.com/docs/backlog/api/2/update-watching/

        :param watchingId: (int) watching ID
        :param note: (str) new note
        :return: the updated watching
        """
        resp = self.api.invoke_method("PATCH", "watchings/{watching_id}".format(watching_id=watchingId), request_param={"note": note})

        return resp.json()

    def delete(self, watchingId):
        """
        https://developer.nulab.com/docs/backlog/api/2/delete-watching/

        :param watchingId: (int) watching ID
        :return: the deleted watching
        """
        resp = self.api.invoke_method("DELETE", "watchings/{watching_id}".format(watching_id=watchingId))

        return resp.json()

    def mark_as_read(self, watchingId):
        """
        https://developer.nulab.com/docs/backlog/api/2/mark-watching-as-read/

        :param watchingId: (int) watching ID
        """
        self.api.invoke_method("POST", "watchings/{watching_id}/markAsRead".format(watching_id=watchingId))
