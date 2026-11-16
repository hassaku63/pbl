# coding: utf-8

from backlog._params import bool_params


class Webhook(object):
    """
    Webhooks of a project: https://developer.nulab.com/docs/backlog/api/2/get-list-of-webhooks/

    These endpoints need administrator or project administrator rights.
    """

    def __init__(self, api) -> None:
        self.api = api

    @staticmethod
    def _params(name, description, hookUrl, allEvent, activityTypeIds):
        return bool_params({
            "name": name, "description": description, "hookUrl": hookUrl,
            "allEvent": allEvent, "activityTypeIds[]": activityTypeIds,
        })

    def list(self, projectIdOrKey):
        """
        https://developer.nulab.com/docs/backlog/api/2/get-list-of-webhooks/

        :param projectIdOrKey: Project ID or Project Key
        :return: list of the webhooks of the project
        """
        resp = self.api.invoke_method("GET", "projects/{project_id_or_key}/webhooks".format(project_id_or_key=projectIdOrKey))

        return resp.json()

    def add(self, projectIdOrKey, name, hookUrl, description=None, allEvent=None, activityTypeIds=None):
        """
        https://developer.nulab.com/docs/backlog/api/2/add-webhook/

        :param projectIdOrKey: Project ID or Project Key
        :param name: (str) webhook name
        :param hookUrl: (str) URL that Backlog sends the events to
        :param description: (str) Optional.
        :param allEvent: (bool) Optional. True to send all events
        :param activityTypeIds: (int or list of int) Optional. activity types to send (when allEvent is not True)
        :return: the added webhook
        """
        _request_param = self._params(name, description, hookUrl, allEvent, activityTypeIds)

        resp = self.api.invoke_method("POST", "projects/{project_id_or_key}/webhooks".format(project_id_or_key=projectIdOrKey),
                                      request_param=_request_param)

        return resp.json()

    def get(self, projectIdOrKey, webhookId):
        """
        https://developer.nulab.com/docs/backlog/api/2/get-webhook/

        :param projectIdOrKey: Project ID or Project Key
        :param webhookId: (int) webhook ID
        :return: the webhook
        """
        _uri = "projects/{project_id_or_key}/webhooks/{webhook_id}".format(project_id_or_key=projectIdOrKey, webhook_id=webhookId)

        resp = self.api.invoke_method("GET", _uri)

        return resp.json()

    def update(self, projectIdOrKey, webhookId, name=None, hookUrl=None, description=None, allEvent=None,
               activityTypeIds=None):
        """
        https://developer.nulab.com/docs/backlog/api/2/update-webhook/

        :param projectIdOrKey: Project ID or Project Key
        :param webhookId: (int) webhook ID
        :param name: (str) Optional.
        :param hookUrl: (str) Optional.
        :param description: (str) Optional.
        :param allEvent: (bool) Optional.
        :param activityTypeIds: (int or list of int) Optional.
        :return: the updated webhook
        """
        _uri = "projects/{project_id_or_key}/webhooks/{webhook_id}".format(project_id_or_key=projectIdOrKey, webhook_id=webhookId)
        _request_param = self._params(name, description, hookUrl, allEvent, activityTypeIds)

        resp = self.api.invoke_method("PATCH", _uri, request_param=_request_param)

        return resp.json()

    def delete(self, projectIdOrKey, webhookId):
        """
        https://developer.nulab.com/docs/backlog/api/2/delete-webhook/

        :param projectIdOrKey: Project ID or Project Key
        :param webhookId: (int) webhook ID
        :return: the deleted webhook
        """
        _uri = "projects/{project_id_or_key}/webhooks/{webhook_id}".format(project_id_or_key=projectIdOrKey, webhook_id=webhookId)

        resp = self.api.invoke_method("DELETE", _uri)

        return resp.json()
