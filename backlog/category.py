class Category(object):
    def __init__(self, api) -> None:
        self.api = api

    def list(self, projectIdOrKey: str):
        """List categories
        https://developer.nulab.com/ja/docs/backlog/api/2/get-category-list/#

        :param projectIdOrKey: project id or key
        :type projectIdOrKey: str
        """
        _url = f"projects/{projectIdOrKey}/categories"
        _method = "GET"

        resp = self.api.invoke_method(_method, _url)

        return resp.json()

    def add(self, projectIdOrKey: str, name: str):
        """Add category
        https://developer.nulab.com/docs/backlog/api/2/add-category/#add-category

        :param projectIdOrKey: project id or key
        :type projectIdOrKey: str
        """
        _url = f"projects/{projectIdOrKey}/categories"
        _method = "POST"

        resp = self.api.invoke_method(_method, _url, request_param={"name": name})

        return resp.json()

    def update(self, projectIdOrKey: str, id: int, name: str):
        """Update category
        https://developer.nulab.com/docs/backlog/api/2/update-category/#

        :param projectIdOrKey: project id or key
        :type projectIdOrKey: str
        :param id: category id
        :type id: int
        :param name: category name
        :type name: str
        """
        _url = f"projects/{projectIdOrKey}/categories/{id}"
        _method = "PATCH"

        resp = self.api.invoke_method(_method, _url, request_param={"name": name})

        return resp.json()

    def delete(self, projectIdOrKey: str, id: int):
        """Delete category
        https://developer.nulab.com/docs/backlog/api/2/delete-category/#

        :param projectIdOrKey: project id or key
        :type projectIdOrKey: str
        :param id: category id
        :type id: int
        """
        _url = f"projects/{projectIdOrKey}/categories/{id}"
        _method = "DELETE"

        resp = self.api.invoke_method(_method, _url)

        return resp.json()
