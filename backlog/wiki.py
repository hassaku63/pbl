# coding: utf-8

from email.message import Message


def _filename_from_response(resp):
    """
    Extract the file name from the Content-Disposition header (supports RFC 6266 filename*).

    :return: file name, or None if the header does not contain one
    """
    _content_disposition = resp.headers.get("Content-Disposition")
    if not _content_disposition:
        return None
    _message = Message()
    _message["Content-Disposition"] = _content_disposition
    return _message.get_filename()


class Wiki(object):
    def __init__(self, api):
        """

        :param api:
        """
        self.api = api

    def list(self, projectIdOrKey, keyword=None):
        """
        https://developer.nulab.com/docs/backlog/api/2/get-wiki-page-list/

        :param projectIdOrKey: Project ID or Project Key
        :param keyword: (str) Optional. only pages that contain the keyword
        :return: list of wiki pages
        """
        _uri = "wikis"
        _method = "GET"

        resp = self.api.invoke_method(_method, _uri, query_param=dict(projectIdOrKey=projectIdOrKey, keyword=keyword))

        return resp.json()

    def count(self, projectIdOrKey):
        """
        https://developer.nulab.com/docs/backlog/api/2/count-wiki-page/

        :param projectIdOrKey: Project ID or Project Key
        :return: {"count": int}
        """
        resp = self.api.invoke_method("GET", "wikis/count", query_param={"projectIdOrKey": projectIdOrKey})

        return resp.json()

    def list_tags(self, projectIdOrKey):
        """
        https://developer.nulab.com/docs/backlog/api/2/get-wiki-page-tag-list/

        :param projectIdOrKey: Project ID or Project Key
        :return: list of the wiki page tags in the project
        """
        resp = self.api.invoke_method("GET", "wikis/tags", query_param={"projectIdOrKey": projectIdOrKey})

        return resp.json()

    def create(self, projectId, name, content, mailNotify=False):
        """
        https://developer.nulab-inc.com/ja/docs/backlog/api/2/add-wiki-page/

        :param projectId: (int) Required. project id
        :param name: (str) Required. wiki page name
        :param content: (str) Required. page content
        :param mailNotify: (bool) Optional. mail notification flag
        :return: Compliant with Backlog API specification
        """
        _uri = "wikis"
        _method = "POST"
        _request_param = {
            "projectId": projectId,
            "name": name,
            "content": content,
            "mailNotify": "true" if mailNotify else "false"
        }

        resp = self.api.invoke_method(_method, _uri, request_param=_request_param)

        return resp.json()

    def get(self, wikiId):
        """
        https://developer.nulab-inc.com/ja/docs/backlog/api/2/get-wiki-page/

        :param wikiId: (int) Required wiki id
        :return: Compliant with Backlog API specification
        """
        _uri = "wikis/{wiki_id}".format(wiki_id=wikiId)
        _method = "GET"
        resp = self.api.invoke_method(_method, _uri)

        return resp.json()

    def update(self, wikiId, name, content, mailNotify=False):
        """
        https://developer.nulab-inc.com/ja/docs/backlog/api/2/update-wiki-page/

        :param wikiId: (int) Required. wiki id
        :param name: (str) Required. wiki name
        :param content: (str) Required. content string
        :param mailNotify: (bool) Optional. mail notification falg.
        :return: Compliant with Backlog API specification
        """
        _uri = "wikis/{wiki_id}".format(wiki_id=wikiId)
        _method = "PATCH"
        _request_param = {
            "name": name,
            "content": content,
            "mailNotify": "true" if mailNotify else "false"
        }

        resp = self.api.invoke_method(_method, _uri, request_param=_request_param)

        return resp.json()

    def delete(self, wikiId, mailNotify=False):
        """
        https://developer.nulab-inc.com/ja/docs/backlog/api/2/delete-wiki-page/

        :param wikiId: (int) Required. wiki id
        :param mailNotify: (bool) Optional. mail notification flag
        :return: Compliant with Backlog API specification
        """
        _uri = "wikis/{wiki_id}".format(wiki_id=wikiId)
        _method = "DELETE"
        _mail_notify = mailNotify
        _request_param = {
            "mailNotify": "true" if _mail_notify else "false"
        }

        resp = self.api.invoke_method(_method, _uri, request_param=_request_param)

        return resp.json()

    def list_attachments(self, wikiId):
        """
        https://developer.nulab-inc.com/ja/docs/backlog/api/2/get-list-of-wiki-attachments/

        :param wikiId: (int) Required. wiki id
        :return: Compliant with Backlog API specification
        """
        _uri = "wikis/{wiki_id}/attachments".format(wiki_id=wikiId)
        _method = "GET"

        resp = self.api.invoke_method(_method, _uri)

        return resp.json()

    def add_attachment(self, wikiId, attachmentId):
        """
        https://developer.nulab.com/docs/backlog/api/2/attach-file-to-wiki/

        :param wikiId: (int) Required. wiki id
        :param attachmentId: (int or list of int) Required. attachment ID(s) returned by Attachment.upload()
        :return: Compliant with Backlog API specification
        """
        _uri = "wikis/{wiki_id}/attachments".format(wiki_id=wikiId)
        _method = "POST"
        _request_param = {
            "attachmentId[]": attachmentId
        }

        resp = self.api.invoke_method(_method, _uri, request_param=_request_param)

        return resp.json()

    def get_attachment(self, wikiId, attachmentId):
        """
        https://developer.nulab-inc.com/ja/docs/backlog/api/2/get-wiki-page-attachment

        :param wikiId: (int) Required. wiki id
        :param attachmentId: (int) Required. attachment id
        :return: dict object. This object contains values.
            "id" as attachment id, "name" as attachment name, and "data" as binary content.
        """
        _uri = "wikis/{wiki_id}/attachments/{attachment_id}".format(wiki_id=wikiId, attachment_id=attachmentId)
        _method = "GET"

        resp = self.api.invoke_method(_method, _uri)

        return {
            "id": attachmentId,
            "name": _filename_from_response(resp),
            "data": resp.content
        }

    def delete_attachment(self, wikiId, attachmentId):
        """
        https://developer.nulab-inc.com/ja/docs/backlog/api/2/remove-wiki-attachment/

        :param wikiId: (int) Required. wiki id
        :param attachmentId: (int) Required. attachment id
        :return: Compliant with Backlog API specification
        """
        _uri = "wikis/{wiki_id}/attachments/{attachment_id}".format(
            wiki_id=wikiId,
            attachment_id=attachmentId
        )
        _method = "DELETE"

        resp = self.api.invoke_method(_method, _uri)

        return resp.json()

    def list_history(self, wikiId, minId=None, maxId=None, count=None, order=None):
        """
        https://developer.nulab.com/docs/backlog/api/2/get-wiki-page-history/

        :param wikiId: (int) wiki page ID
        :param minId: (int) Optional. minimum history ID
        :param maxId: (int) Optional. maximum history ID
        :param count: (int) Optional. number of records to retrieve (1-100), default 20
        :param order: (str) Optional. "asc" or "desc" (default)
        :return: list of the page's versions
        """
        _uri = "wikis/{wiki_id}/history".format(wiki_id=wikiId)
        _query_param = {"minId": minId, "maxId": maxId, "count": count, "order": order}

        resp = self.api.invoke_method("GET", _uri, query_param=_query_param)

        return resp.json()

    def list_stars(self, wikiId):
        """
        https://developer.nulab.com/docs/backlog/api/2/get-wiki-page-star/

        :param wikiId: (int) wiki page ID
        :return: list of the stars on the page
        """
        _uri = "wikis/{wiki_id}/stars".format(wiki_id=wikiId)

        resp = self.api.invoke_method("GET", _uri)

        return resp.json()

    def list_shared_files(self, wikiId):
        """
        https://developer.nulab.com/docs/backlog/api/2/get-list-of-shared-files-on-wiki/

        :param wikiId: (int) wiki page ID
        :return: list of the shared files linked to the page
        """
        _uri = "wikis/{wiki_id}/sharedFiles".format(wiki_id=wikiId)

        resp = self.api.invoke_method("GET", _uri)

        return resp.json()

    def link_shared_files(self, wikiId, fileId):
        """
        https://developer.nulab.com/docs/backlog/api/2/link-shared-files-to-wiki/

        :param wikiId: (int) wiki page ID
        :param fileId: (int or list of int) shared file ID(s)
        :return: list of the linked shared files
        """
        _uri = "wikis/{wiki_id}/sharedFiles".format(wiki_id=wikiId)

        resp = self.api.invoke_method("POST", _uri, request_param={"fileId[]": fileId})

        return resp.json()

    def unlink_shared_file(self, wikiId, id):
        """
        https://developer.nulab.com/docs/backlog/api/2/remove-link-to-shared-file-from-wiki/

        :param wikiId: (int) wiki page ID
        :param id: (int) shared file ID
        :return: the unlinked shared file
        """
        _uri = "wikis/{wiki_id}/sharedFiles/{id}".format(wiki_id=wikiId, id=id)

        resp = self.api.invoke_method("DELETE", _uri)

        return resp.json()
