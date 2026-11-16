# coding: utf-8

_TARGETS = ("issueId", "commentId", "wikiId", "pullRequestId", "pullRequestCommentId")


class Star(object):
    """
    Stars: https://developer.nulab.com/docs/backlog/api/2/add-star/

    The stars on a wiki page are listed by Wiki.list_stars(); stars on issues and comments are in
    their "stars" field.
    """

    def __init__(self, api) -> None:
        self.api = api

    def add(self, issueId=None, commentId=None, wikiId=None, pullRequestId=None, pullRequestCommentId=None):
        """
        https://developer.nulab.com/docs/backlog/api/2/add-star/

        Give a star to exactly one of: an issue, an issue comment, a wiki page, a pull request or a
        pull request comment (each by its numeric ID).

        :return: None (the API answers 204 No Content)
        """
        _request_param = {
            "issueId": issueId, "commentId": commentId, "wikiId": wikiId,
            "pullRequestId": pullRequestId, "pullRequestCommentId": pullRequestCommentId,
        }
        given = [k for k in _TARGETS if _request_param[k] is not None]
        if len(given) != 1:
            raise ValueError("Star.add() takes exactly one of: " + ", ".join(_TARGETS))

        self.api.invoke_method("POST", "stars", request_param={given[0]: _request_param[given[0]]})

    def delete(self, starId):
        """
        https://developer.nulab.com/docs/backlog/api/2/remove-star/

        :param starId: (int) star ID
        :return: None (the API answers 204 No Content)
        """
        self.api.invoke_method("DELETE", "stars/{star_id}".format(star_id=starId))

    def list_received(self, userId, minId=None, maxId=None, count=None, order=None):
        """
        https://developer.nulab.com/docs/backlog/api/2/get-received-star-list/

        :param userId: (int) user ID (see User.get_myself() for your own ID)
        :param minId: (int) Optional. minimum star ID
        :param maxId: (int) Optional. maximum star ID
        :param count: (int) Optional. number of records to retrieve (1-100), default 20
        :param order: (str) Optional. "asc" or "desc" (default)
        :return: list of stars the user received
        """
        _uri = "users/{user_id}/stars".format(user_id=userId)
        _query_param = {"minId": minId, "maxId": maxId, "count": count, "order": order}

        resp = self.api.invoke_method("GET", _uri, query_param=_query_param)

        return resp.json()

    def count_received(self, userId, since=None, until=None):
        """
        https://developer.nulab.com/docs/backlog/api/2/count-user-received-stars/

        :param userId: (int) user ID
        :param since: (str) Optional. only stars received on or after this date (yyyy-MM-dd)
        :param until: (str) Optional. only stars received on or before this date (yyyy-MM-dd)
        :return: {"count": int}
        """
        _uri = "users/{user_id}/stars/count".format(user_id=userId)

        resp = self.api.invoke_method("GET", _uri, query_param={"since": since, "until": until})

        return resp.json()
