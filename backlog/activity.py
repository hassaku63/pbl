# coding: utf-8

from backlog.pagination import id_range, iterate_by_id


def _activity_query(activityTypeId, minId, maxId, count, order):
    return {"activityTypeId[]": activityTypeId, "minId": minId, "maxId": maxId, "count": count, "order": order}


class Activity(object):
    """
    Recent updates (activities) of the space, a project or a user:
    https://developer.nulab.com/docs/backlog/api/2/get-recent-updates/

    The list methods share these optional parameters:

    - activityTypeId: (int or list of int) activity types to return (1-51)
    - minId / maxId: (int) minimum / maximum activity ID
    - count: (int) number of records to retrieve (1-100), default 20
    - order: (str) "asc" or "desc" (default)
    """

    def __init__(self, api) -> None:
        self.api = api

    def list(self, activityTypeId=None, minId=None, maxId=None, count=None, order=None):
        """
        https://developer.nulab.com/docs/backlog/api/2/get-recent-updates/

        :return: list of recent updates in the space
        """
        _query_param = _activity_query(activityTypeId, minId, maxId, count, order)

        resp = self.api.invoke_method("GET", "space/activities", query_param=_query_param)

        return resp.json()

    def iter(self, activityTypeId=None, minId=None, maxId=None, order="desc", count=100):
        """
        Iterate over all recent updates in the space, newest first by default (minId/maxId paging).

        :return: iterator of activities
        """
        return iterate_by_id(self.list, activityTypeId=activityTypeId, order=order, count=count, **id_range(minId, maxId))

    def list_project(self, projectIdOrKey, activityTypeId=None, minId=None, maxId=None, count=None, order=None):
        """
        https://developer.nulab.com/docs/backlog/api/2/get-project-recent-updates/

        :param projectIdOrKey: Project ID or Project Key
        :return: list of recent updates in the project
        """
        _uri = "projects/{project_id_or_key}/activities".format(project_id_or_key=projectIdOrKey)
        _query_param = _activity_query(activityTypeId, minId, maxId, count, order)

        resp = self.api.invoke_method("GET", _uri, query_param=_query_param)

        return resp.json()

    def iter_project(self, projectIdOrKey, activityTypeId=None, minId=None, maxId=None, order="desc", count=100):
        """
        Iterate over all recent updates in the project, newest first by default.

        :param projectIdOrKey: Project ID or Project Key
        :return: iterator of activities
        """
        return iterate_by_id(self.list_project, projectIdOrKey, activityTypeId=activityTypeId, order=order, count=count,
                             **id_range(minId, maxId))

    def list_user(self, userId, activityTypeId=None, minId=None, maxId=None, count=None, order=None):
        """
        https://developer.nulab.com/docs/backlog/api/2/get-user-recent-updates/

        :param userId: (int) user ID (see User.get_myself() for your own ID)
        :return: list of the user's recent updates
        """
        _uri = "users/{user_id}/activities".format(user_id=userId)
        _query_param = _activity_query(activityTypeId, minId, maxId, count, order)

        resp = self.api.invoke_method("GET", _uri, query_param=_query_param)

        return resp.json()

    def iter_user(self, userId, activityTypeId=None, minId=None, maxId=None, order="desc", count=100):
        """
        Iterate over all recent updates of the user, newest first by default.

        :param userId: (int) user ID
        :return: iterator of activities
        """
        return iterate_by_id(self.list_user, userId, activityTypeId=activityTypeId, order=order, count=count,
                             **id_range(minId, maxId))

    def get(self, activityId):
        """
        https://developer.nulab.com/docs/backlog/api/2/get-activity/

        :param activityId: (int) activity ID
        :return: the activity
        """
        _uri = "activities/{activity_id}".format(activity_id=activityId)

        resp = self.api.invoke_method("GET", _uri)

        return resp.json()
