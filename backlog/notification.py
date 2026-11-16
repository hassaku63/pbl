# coding: utf-8

from backlog._params import bool_params
from backlog.pagination import id_range, iterate_by_id


class Notification(object):
    """
    Notifications of the user that owns the API key or access token:
    https://developer.nulab.com/docs/backlog/api/2/get-notification/
    """

    def __init__(self, api) -> None:
        self.api = api

    def list(self, minId=None, maxId=None, count=None, order=None, senderId=None):
        """
        https://developer.nulab.com/docs/backlog/api/2/get-notification/

        :param minId: (int) Optional. minimum notification ID
        :param maxId: (int) Optional. maximum notification ID
        :param count: (int) Optional. number of records to retrieve (1-100), default 20
        :param order: (str) Optional. "asc" or "desc"
        :param senderId: (int) Optional. only notifications from this user
        :return: list of notifications
        """
        _query_param = {"minId": minId, "maxId": maxId, "count": count, "order": order, "senderId": senderId}

        resp = self.api.invoke_method("GET", "notifications", query_param=_query_param)

        return resp.json()

    def iter(self, senderId=None, minId=None, maxId=None, order="desc", count=100):
        """
        Iterate over all notifications, newest first by default (minId/maxId paging).

        :param senderId: (int) Optional. only notifications from this user
        :return: iterator of notifications
        """
        return iterate_by_id(self.list, senderId=senderId, order=order, count=count, **id_range(minId, maxId))

    def count(self, resourceAlreadyRead=None, alreadyRead=None):
        """
        https://developer.nulab.com/docs/backlog/api/2/count-notification/

        :param resourceAlreadyRead: (bool) Optional. count read (True) or unread (False) notifications
        :param alreadyRead: (bool) Optional. count notifications read (True) or unread (False) since the user last checked
        :return: {"count": int}
        """
        _query_param = bool_params({"resourceAlreadyRead": resourceAlreadyRead, "alreadyRead": alreadyRead})

        resp = self.api.invoke_method("GET", "notifications/count", query_param=_query_param)

        return resp.json()

    def reset_unread_count(self):
        """
        https://developer.nulab.com/docs/backlog/api/2/reset-unread-notification-count/

        :return: {"count": int}
        """
        resp = self.api.invoke_method("POST", "notifications/markAsRead")

        return resp.json()

    def mark_as_read(self, id):
        """
        https://developer.nulab.com/docs/backlog/api/2/read-notification/

        :param id: (int) notification ID
        """
        self.api.invoke_method("POST", "notifications/{id}/markAsRead".format(id=id))
